from typing import Literal
from datetime import date
from pydantic import BaseModel, Field

Tenant = Literal["atlas", "beacon"]
Decision = Literal["answered", "clarification", "abstained", "escalated", "blocked"]

class RunRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    tenant: Tenant = "atlas"

class TraceStep(BaseModel):
    stage: str
    tool: str
    outcome: str
    detail: str

class Citation(BaseModel):
    source_id: str
    title: str
    quote: str

class EligibilityResult(BaseModel):
    status: Literal["eligible", "ineligible", "needs_more_information", "already_refunded", "blocked_or_unsupported"]
    assessment_date: date | None = None

class RunResponse(BaseModel):
    run_id: str
    mode: str = "deterministic"
    decision: Decision
    intent: str
    answer: str
    tenant: Tenant
    citations: list[Citation]
    evidence_count: int
    trace: list[TraceStep]
    eligibility: EligibilityResult | None = None

class EvaluationResult(BaseModel):
    id: str
    name: str
    category: str
    expected: str
    actual: str
    passed: bool
    explanation: str

class EvaluationReport(BaseModel):
    total: int
    passed: int
    failed: int
    pass_rate: float
    results: list[EvaluationResult]
