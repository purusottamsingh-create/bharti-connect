import json
import os
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import datetime

router = APIRouter(
    prefix="/crm/v1/accounts",
    tags=["CRM — Billing"],
)

# Resolve the `data/` directory relative to this file's location
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


def _read(filename: str):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write(filename: str, payload):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


# ── 1. GET /crm/v1/accounts/{mobile_number}/invoices ─────────────────────────

@router.get("/{mobile_number}/invoices", summary="get_customer_invoices")
def get_customer_invoices(
    mobile_number: str,
    months: int = Query(3, ge=1, le=12, description="Number of past months to fetch (1–12). Defaults to 3."),
):
    data = _read("invoices.json")
    all_invoices = data.get(mobile_number, [])
    # Slice to the requested number of months (data is newest-first)
    invoices = all_invoices[:months]
    return {
        "status": "success",
        "mobile_number": mobile_number,
        "invoices": invoices,
    }


# ── 2. GET /crm/v1/accounts/{mobile_number}/activation-log ───────────────────

@router.get("/{mobile_number}/activation-log", summary="get_activation_log")
def get_activation_log(
    mobile_number: str,
    from_date: Optional[str] = Query(None, description="Start date filter. Format: YYYY-MM-DD"),
    to_date: Optional[str] = Query(None, description="End date filter. Format: YYYY-MM-DD"),
):
    data = _read("activation_log.json")
    logs = data.get(mobile_number, [])

    # Optional date filtering
    if from_date:
        logs = [e for e in logs if e["timestamp"][:10] >= from_date]
    if to_date:
        logs = [e for e in logs if e["timestamp"][:10] <= to_date]

    return {
        "status": "success",
        "mobile_number": mobile_number,
        "activation_log": logs,
    }


# ── 3. GET /crm/v1/accounts/{mobile_number}/balance ──────────────────────────

@router.get("/{mobile_number}/balance", summary="get_account_balance")
def get_account_balance(mobile_number: str):
    data = _read("account_balance.json")
    balance = data.get(mobile_number)
    if not balance:
        raise HTTPException(status_code=404, detail=f"No account found for mobile_number {mobile_number}")
    return {
        "status": "success",
        "mobile_number": mobile_number,
        **balance,
    }


@router.get("/{mobile_number}/plan", tags=["CRM — Billing"])
def get_account_plan(mobile_number: str):
    """
    Returns the current subscription plan for the account.
    """
    data = _read("account_balance.json")
    account = data.get(mobile_number)
    if not account:
        raise HTTPException(status_code=404, detail=f"No account found for mobile_number {mobile_number}")

    return {
        "mobile_number": mobile_number,
        "current_plan": account.get("plan_name", "₹699 Postpaid Premium"),
        "status": "active",
        "billing_cycle": "Monthly",
        "data_limit": "75 GB",
        "voice_limit": "Unlimited"
    }


# ── 4. GET /crm/v1/accounts/{mobile_number}/usage ────────────────────────────

@router.get("/{mobile_number}/usage", summary="get_usage_history")
def get_usage_history(
    mobile_number: str,
    months: int = Query(3, description="Number of months to retrieve usage for (defaults to 3)"),
):
    data = _read("usage_history.json")
    all_usage = data.get(mobile_number)
    if all_usage is None:
        raise HTTPException(status_code=404, detail=f"No usage data found for mobile_number {mobile_number}")

    # For this demo, we'll sort the usage and return the most recent N records 
    # (In a real system, we would group by calendar months. 
    # Here, we'll simply return the most recent data available.)
    all_usage.sort(key=lambda x: x["date"], reverse=True)
    
    # Simple logic: assume ~30 records per month for the demo, 
    # or just return the whole list if it's small (which our seed data is).
    # Since our demo data is limited, we will return the available records 
    # and adjust the "usage_period" description accordingly.
    
    # Filter for demo purposes: just show the data we have, capped at a reasonable limit
    filtered = all_usage[:months * 31]
    filtered.sort(key=lambda x: x["date"]) # Sort back to chronological for the response

    # Compute summary dynamically from filtered results
    total_data = round(sum(d.get("data_used_gb", 0) for d in filtered), 2)
    total_excess = round(sum(d.get("excess_gb", 0) for d in filtered), 2)
    total_calls = sum(d.get("calls_minutes", 0) for d in filtered)
    total_sms = sum(d.get("sms_count", 0) for d in filtered)
    days_exceeded = sum(1 for d in filtered if d.get("excess_gb", 0) > 0)

    return {
        "status": "success",
        "mobile_number": mobile_number,
        "months_analysed": months,
        "daily_usage": filtered,
        "summary": {
            "total_data_used_gb": total_data,
            "total_excess_gb": total_excess,
            "total_calls_minutes": total_calls,
            "total_sms_count": total_sms,
            "days_limit_exceeded": days_exceeded,
        },
    }


# ── 5. POST /crm/v1/accounts/{mobile_number}/credits ─────────────────────────

class CreditRequest(BaseModel):
    mobile_number: str
    amount: float
    currency: str
    reason: str
    credit_type: str
    applied_by: str
    reference_invoice: str


@router.post("/{mobile_number}/credits", summary="apply_account_credit")
def apply_account_credit(mobile_number: str, body: CreditRequest):
    if body.mobile_number != mobile_number:
        raise HTTPException(status_code=400, detail="mobile_number in path and body must match")

    data = _read("account_balance.json")
    account = data.get(mobile_number)
    if not account:
        raise HTTPException(status_code=404, detail=f"No account found for mobile_number {mobile_number}")

    # Deduct credit and persist
    current_balance = account["current_balance"]
    revised_balance = round(current_balance - body.amount, 2)
    account["current_balance"] = revised_balance
    data[mobile_number] = account
    _write("account_balance.json", data)

    effective_date = datetime.date.today().isoformat()

    return {
        "status": "success",
        "credit_id": "CRD-33821",
        "mobile_number": mobile_number,
        "amount_credited": body.amount,
        "revised_balance": revised_balance,
        "effective_date": effective_date,
        "confirmation_sms": True,
        "message": f"Credit of \u20b9{int(body.amount)} applied. Revised outstanding: \u20b9{int(revised_balance)}.",
    }
