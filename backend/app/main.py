import os
import platform
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import RunRequest, RunResponse, EvaluationReport
from .engine import run_agent
from .evaluations import run_evaluations
from .knowledge import ARTICLES

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
                {"id": "REQ-006", "text": "Run deterministic evaluations in CI.", "proof": "CI quality gate"}]}
