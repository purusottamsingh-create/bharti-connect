import json
import os
import datetime
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/ticketing/v1",
    tags=["Ticketing"],
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")


def _read_tickets():
    path = os.path.join(DATA_DIR, "tickets.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_tickets(tickets: list):
    path = os.path.join(DATA_DIR, "tickets.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2, ensure_ascii=False)


# ── 5. POST /ticketing/v1/tickets ─────────────────────────────────────────────

class TicketRequest(BaseModel):
    mobile_number: str
    type: str
    issue_summary: str
    root_cause: str
    action_taken: str
    credit_amount: float
    credit_id: str
    priority: str
    resolution_status: str
    raised_by: str


@router.post("/tickets", summary="create_ticket")
def create_ticket(body: TicketRequest):
    tickets = _read_tickets()

    # Generate a sequential ticket ID
    ticket_id = f"BTC-{88103 + len(tickets)}"
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    sla_due = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")

    new_ticket = {
        "ticket_id": ticket_id,
        "created_at": now,
        **body.model_dump(),
    }
    tickets.append(new_ticket)
    _write_tickets(tickets)

    return {
        "status": "success",
        "ticket_id": ticket_id,
        "mobile_number": body.mobile_number,
        "priority": body.priority,
        "sla_due_by": sla_due,
        "assigned_team": "billing_ops",
        "created_at": now,
    }
