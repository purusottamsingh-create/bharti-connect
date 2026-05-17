from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import crm, ticketing, plan_advisor
from app.seed import ensure_seed_data

# Reset data to clean baseline on every startup
ensure_seed_data(force=True)

app = FastAPI(
    title="Bharti Connect API",
    description=(
        "Billing agent APIs for Kore.ai integration. "
        "Call sequence: get_customer_invoices → get_activation_log → "
        "get_account_balance → apply_account_credit → create_ticket"
    ),
    version="1.0.0",
)

app.include_router(plan_advisor.router)
app.include_router(crm.router)
app.include_router(ticketing.router)

# Serve the Knowledge Base static files
app.mount("/kb", StaticFiles(directory="knowledge_base", html=True), name="kb")

# Serve the Demo Verification Dashboard static files
app.mount("/dashboard", StaticFiles(directory="dashboard", html=True), name="dashboard")



@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Bharti Connect API is running"}
