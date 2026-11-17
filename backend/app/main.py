import os
import platform
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import RunRequest, RunResponse, EvaluationReport, OrderStatusRequest, OrderStatusResponse
from .engine import run_agent
from .evaluations import run_evaluations
from .knowledge import ARTICLES
from .order_status import run_order_status

app = FastAPI(title="Agentic Reliability Lab", version="0.1.0",
              description="Synthetic policy-driven workflows with inspectable traces.")
origins = ["http://localhost:5173", "http://127.0.0.1:5173",
           "https://agentic-reliability-lab.onrender.com"]
origins += [x.strip() for x in os.getenv("CORS_ORIGINS", "").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=False,
                   allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

@app.get("/health")
def health():
    return {"status": "ok", "mode": "deterministic", "live_llm": False,
            "synthetic_data_only": True, "python_version": platform.python_version()}

@app.post("/api/agent/run", response_model=RunResponse)
def run(payload: RunRequest):
    return run_agent(payload)

@app.post("/api/order-status/run", response_model=OrderStatusResponse,
          summary="Check a fictional order as a demo persona",
          description="Anyone can choose a fictional customer to simulate an authenticated request. "
                      "This endpoint uses synthetic fixtures only.")
def order_status(payload: OrderStatusRequest):
    return run_order_status(payload)

@app.post("/api/evaluations/run", response_model=EvaluationReport)
def evaluate():
    return run_evaluations()

@app.get("/api/knowledge")
def knowledge(tenant: str = "atlas"):
    return {"articles": [{"source_id": a.source_id, "title": a.title} for a in ARTICLES
                         if a.tenant == tenant]}

@app.get("/api/specifications")
def specifications():
    return {"id": "SPEC-001", "feature": "Reliable support",
            "documents": [
                {"name": "intent.md", "purpose": "Why: problem, goals and exclusions"},
                {"name": "spec.md", "purpose": "What: requirements and acceptance evidence"},
                {"name": "plan.md", "purpose": "How: implementation and verification"},
                {"name": "ADR-001", "purpose": "Why: architecture and trade-offs"}],
            "requirements": [
                {"id": "REQ-001", "text": "Answer only using authorised tenant knowledge.", "proof": "EV-001–EV-004"},
                {"id": "REQ-002", "text": "Block cross-tenant synthetic order access.", "proof": "EV-007, EV-014"},
                {"id": "REQ-003", "text": "Abstain on unsupported questions.", "proof": "EV-009, EV-013"},
                {"id": "REQ-004", "text": "Expose ordered routing and tool traces.", "proof": "test_trace_present"},
                {"id": "REQ-005", "text": "Reject known instruction override attempts.", "proof": "EV-008"},
                {"id": "REQ-006", "text": "Run deterministic evaluations in CI.", "proof": "CI quality gate"}],
            "additional_specifications": [{"id": "SPEC-002", "feature": "Refund eligibility",
                "documents": [{"name": "intent.md", "purpose": "Synthetic refund eligibility intent"}, {"name": "spec.md", "purpose": "Eligibility requirements"}, {"name": "plan.md", "purpose": "Implementation and verification"}, {"name": "ADR-002", "purpose": "Architecture and trade-offs"}],
                "requirements": [{"id": f"REQ-{number:03d}", "text": description, "proof": "test_refund_eligibility.py"} for number, description in [
                    (7, "Route refund eligibility questions."), (8, "Clarify missing order references."), (9, "Isolate tenants."), (10, "Select the authorised policy."), (11, "Assess eligible orders."), (12, "Explain ineligible orders."), (13, "Do not assume missing evidence."), (14, "Do not execute refunds."), (15, "Cite policy and trace operations."), (16, "Preserve existing workflows.")]]},
                {"id": "SPEC-003", "feature": "Customer order status",
                 "documents": [{"name": name, "purpose": purpose} for name, purpose in [
                     ("intent.md", "Customer need and demo scope"),
                     ("spec.md", "Order-status requirements and acceptance scenarios"),
                     ("plan.md", "Implementation and verification"),
                     ("ADR-003", "Synthetic identity and isolation decision"),
                 ]],
                 "requirements": [
                     {"id": f"REQ-{number:03d}", "text": description,
                      "proof": f"AC-{scenario:03d} · test_order_status.py"}
                     for number, scenario, description in [
                         (17, 1, "Prompt for an Order ID before lookup."),
                         (18, 2, "Read an authorised current order status."),
                         (19, 3, "Handle an invalid or unknown Order ID."),
                         (20, 4, "Enforce simulated customer ownership."),
                         (21, 5, "Handle source outages safely."),
                         (22, 2, "Display the Order ID and status."),
                         (23, 6, "Keep order enquiries read-only."),
                     ]
                 ]}]}
