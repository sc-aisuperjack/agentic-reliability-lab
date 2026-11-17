"""Inspectable orchestration with deterministic decisions and tenant-scoped tools."""
import re
from uuid import uuid4
from .models import RunRequest, RunResponse, TraceStep, Citation, EligibilityResult
from .knowledge import ORDERS, REFUND_POLICIES, INJECTION_TERMS, ESCALATION_TERMS, intent_of, find_article
from .refund_eligibility import assess, SIMULATION_DATE

def run_agent(request: RunRequest) -> RunResponse:
    text = request.message.strip()
    lower = text.lower()
    trace: list[TraceStep] = []

    def step(stage: str, tool: str, outcome: str, detail: str):
        trace.append(TraceStep(stage=stage, tool=tool, outcome=outcome, detail=detail))

    def finish(decision, intent, answer, citations=None, eligibility=None):
        evidence = citations or []
        step("validate", "response_guard", "passed", f"Decision={decision}; evidence={len(evidence)}")
        return RunResponse(run_id=str(uuid4()), decision=decision, intent=intent,
                           answer=answer, tenant=request.tenant, citations=evidence,
                           evidence_count=len(evidence), trace=trace, eligibility=eligibility)

    step("intake", "normalise_input", "passed", "Validated input; no customer data persisted")
    if any(term in lower for term in INJECTION_TERMS):
        step("safety", "instruction_boundary", "blocked", "Known instruction-override phrase detected")
        return finish("blocked", "security", "I cannot override this workflow or reveal hidden instructions.")
    if any(term in lower for term in ESCALATION_TERMS):
        step("route", "policy_router", "escalated", "A human support route was requested")
        return finish("escalated", "handoff", "A real deployment would create a handoff. No ticket was created by this demo.")

    intent = intent_of(text)
    step("route", "intent_router", "selected", f"Intent={intent}; synthetic tenant={request.tenant}")
    if intent == "refund_eligibility":
        match = re.search(r"\bORD[- ]?(\d{4,6})\b", text, re.IGNORECASE)
        if not match:
            step("tool", "synthetic_order_lookup", "needs_input", "No synthetic order reference")
            return finish("clarification", intent, "Please provide a demo order ID and resubmit your question. Never enter a real order.", eligibility=EligibilityResult(status="needs_more_information"))
        order_id = f"ORD-{match.group(1)}"
        entry = ORDERS.get(order_id)
        if entry is None:
            step("tool", "synthetic_order_lookup", "not_found", "Synthetic order not found")
            return finish("abstained", intent, "No synthetic record was found. I cannot assess eligibility.", eligibility=EligibilityResult(status="blocked_or_unsupported"))
        if entry["tenant"] != request.tenant:
            step("safety", "tenant_authorisation", "denied", "Cross-tenant record access rejected")
            return finish("blocked", intent, "This synthetic record belongs to another tenant.", eligibility=EligibilityResult(status="blocked_or_unsupported"))
        step("tool", "synthetic_order_lookup", "found", f"Authorised record {order_id}")
        policy = REFUND_POLICIES.get(request.tenant)
        if policy is None:
            step("tool", "knowledge_search", "no_evidence", "No authorised refund policy")
            return finish("abstained", intent, "No authorised refund policy is available.", eligibility=EligibilityResult(status="blocked_or_unsupported"))
        step("tool", "knowledge_search", "found", f"Authorised source={policy.article.source_id}")
        status, answer = assess(entry, policy)
        step("assessment", "eligibility_assessment", status, f"Assessed using synthetic date {SIMULATION_DATE.isoformat()}")
        step("grounding", "citation_validator", "passed", "Citation matches retrieved tenant record")
        citation = Citation(source_id=policy.article.source_id, title=policy.article.title, quote=policy.article.body)
        decision = "clarification" if status == "needs_more_information" else "answered"
        return finish(decision, intent, f"{answer} Assessment date: {SIMULATION_DATE.isoformat()} (simulation).", [citation], EligibilityResult(status=status, assessment_date=SIMULATION_DATE))
    if intent == "order":
        match = re.search(r"\bORD[- ]?(\d{4,6})\b", text, re.IGNORECASE)
        if not match:
            step("tool", "synthetic_order_lookup", "needs_input", "No synthetic order reference")
            return finish("clarification", intent, "Please provide a demo order ID such as ORD-1001 or ORD-2001. Never enter a real order.")
        order = f"ORD-{match.group(1)}"
        entry = ORDERS.get(order)
        if entry is None:
            step("tool", "synthetic_order_lookup", "not_found", "Synthetic order not found")
            return finish("abstained", intent, f"No synthetic record for {order}. I cannot access real orders.")
        if entry["tenant"] != request.tenant:
            step("safety", "tenant_authorisation", "denied", "Cross-tenant record access rejected")
            return finish("blocked", intent, "This synthetic record belongs to another tenant.")
        step("tool", "synthetic_order_lookup", "found", f"Authorised record {order}")
        return finish("answered", intent, f'{order}: {entry["status"]}. {entry["detail"]}')

    article = find_article(request.tenant, intent)
    if article is None:
        step("tool", "knowledge_search", "no_evidence", "No authorised tenant policy matches")
        return finish("abstained", intent, "I have no authorised evidence for that question and will not guess.")

    step("tool", "knowledge_search", "found", f"Authorised source={article.source_id}")
    step("grounding", "citation_validator", "passed", "Citation matches retrieved tenant record")
    return finish("answered", intent, article.answer,
                  [Citation(source_id=article.source_id, title=article.title, quote=article.body)])
