import os
import json
import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

router = APIRouter(prefix="/crm/v1", tags=["CRM — Plan Advisor"])

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

def _read(filename: str):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _write(filename: str, payload):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

# ── 1. GET /crm/v1/accounts/{mobile_number}/recharges ────────────────────────

@router.get("/accounts/{mobile_number}/recharges", summary="get_recharge_history")
def get_recharge_history(
    mobile_number: str,
    months: int = Query(3, ge=1, le=12)
):
    """
    Returns the recharge and spend history for the account.
    """
    data = _read("recharge_history.json")
    history = data.get(mobile_number)
    if not history:
        raise HTTPException(status_code=404, detail=f"No recharge history found for mobile_number {mobile_number}")

    # Slice to requested months (newest-first)
    sliced = history[:months]

    if not sliced:
        return {
            "status": "success",
            "mobile_number": mobile_number,
            "months_analysed": 0,
            "recharge_history": [],
            "summary": None
        }

    # Dynamic summary calculation
    total_base = sum(r["base_recharge_rs"] for r in sliced)
    total_topup = sum(r.get("total_top_up_spend_rs", 0) for r in sliced)
    count = len(sliced)

    avg_base = round(total_base / count, 2)
    avg_topup = round(total_topup / count, 2)
    effective_spend = round(avg_base + avg_topup, 2)

    return {
        "status": "success",
        "mobile_number": mobile_number,
        "months_analysed": count,
        "recharge_history": sliced,
        "summary": {
            "average_base_recharge_rs": avg_base,
            "average_top_up_spend_rs": avg_topup,
            "effective_monthly_spend_rs": effective_spend,
            "recharge_consistency": sliced[0].get("recharge_consistency", "regular"),
            "next_recharge_due": sliced[0].get("next_recharge_due")
        }
    }

# ── 2. GET /crm/v1/accounts/{mobile_number}/plan ─────────────────────────────

@router.get("/accounts/{mobile_number}/plan", summary="get_current_plan")
def get_current_plan(mobile_number: str):
    """
    Returns the full details of the current plan active on the account.
    """
    data = _read("current_plan.json")
    plan = data.get(mobile_number)
    if not plan:
        raise HTTPException(status_code=404, detail=f"No plan found for mobile_number {mobile_number}")

    return {
        "status": "success",
        "mobile_number": mobile_number,
        "current_plan": plan
    }

# ── 3. GET /crm/v1/plans ─────────────────────────────────────────────────────

@router.get("/plans", summary="get_available_plans")
def get_available_plans(
    circle: str = Query(..., description="Telecom circle (e.g., Maharashtra, Karnataka, Delhi)"),
    type: str = Query(..., description="Plan type (postpaid or prepaid)")
):
    """
    Returns the catalogue of available plans filtered by circle and type.
    """
    data = _read("available_plans.json")
    filtered = [p for p in data if p.get("circle") == circle and p.get("plan_type") == type]

    if not filtered:
        raise HTTPException(status_code=404, detail=f"No plans found for circle {circle} and type {type}")

    return {
        "status": "success",
        "circle": circle,
        "plan_type": type,
        "available_plans": filtered
    }

# ── 4. POST /crm/v1/accounts/{mobile_number}/plan-change ─────────────────────

class PlanChangeRequest(BaseModel):
    mobile_number: str
    current_plan_id: str
    new_plan_id: str
    effective_date: str
    reason: str
    scheduled_by: str

@router.post("/accounts/{mobile_number}/plan-change", summary="schedule_plan_change")
def schedule_plan_change(mobile_number: str, body: PlanChangeRequest):
    """
    Schedules a plan change for a future date.
    """
    if body.mobile_number != mobile_number:
        raise HTTPException(status_code=400, detail="mobile_number in path and body must match")

    # Look up new plan name for the confirmation message
    all_plans = _read("available_plans.json")
    new_plan = next((p for p in all_plans if p["plan_id"] == body.new_plan_id), None)
    new_plan_name = new_plan["plan_name"] if new_plan else "New Plan"

    # Save the change record
    changes = _read("plan_changes.json")
    now = datetime.datetime.now()
    change_id = f"PLN-CHG-{now.strftime('%Y%m%d')}-{len(changes) + 1:03d}"

    record = {
        "change_reference": change_id,
        "created_at": now.isoformat(),
        **body.dict()
    }
    changes.append(record)
    _write("plan_changes.json", changes)

    return {
        "status": "success",
        "mobile_number": mobile_number,
        "change_reference": change_id,
        "current_plan_id": body.current_plan_id,
        "new_plan": new_plan_name,
        "effective_date": body.effective_date,
        "confirmation_sms": True,
        "message": f"Plan change scheduled. {new_plan_name} will activate automatically on {body.effective_date}. Customer will receive SMS confirmation."
    }

# ── 5. PATCH /crm/v1/accounts/{mobile_number}/notes ──────────────────────────

class AccountNoteRequest(BaseModel):
    mobile_number: str
    note: str
    note_type: str
    outcome: str
    recommended_plan_id: str
    change_reference: Optional[str] = None
    noted_by: str

@router.patch("/accounts/{mobile_number}/notes", summary="add_account_note")
def add_account_note(mobile_number: str, body: AccountNoteRequest):
    """
    Adds a detailed interaction note to the account.
    """
    if body.mobile_number != mobile_number:
        raise HTTPException(status_code=400, detail="mobile_number in path and body must match")

    data = _read("account_notes.json")
    if mobile_number not in data:
        data[mobile_number] = []

    # Calculate total notes for ID generation
    total_notes = sum(len(notes) for notes in data.values())
    now = datetime.datetime.now()
    note_id = f"NOTE-{now.strftime('%Y%m%d')}-{total_notes + 1:03d}"

    record = {
        "note_id": note_id,
        "created_at": now.isoformat() + "Z",
        **body.dict()
    }
    data[mobile_number].append(record)
    _write("account_notes.json", data)

    return {
        "status": "success",
        "mobile_number": mobile_number,
        "note_id": note_id,
        "note_type": body.note_type,
        "created_at": record["created_at"],
        "message": "Account note written successfully."
    }


@router.get("/accounts/notes", summary="get_all_notes")
def get_all_notes():
    """
    Returns all interaction notes across all accounts.
    """
    return _read("account_notes.json")


@router.get("/accounts/plan-changes", summary="get_all_plan_changes")
def get_all_plan_changes():
    """
    Returns all scheduled plan changes in the system.
    """
    return _read("plan_changes.json")


@router.get("/accounts/plans", summary="get_all_plans")
def get_all_plans():
    """
    Returns the current plans configuration for all customers.
    """
    return _read("current_plan.json")

