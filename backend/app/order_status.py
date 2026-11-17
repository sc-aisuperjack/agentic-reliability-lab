"""Deterministic status enquiries against a customer-scoped synthetic source."""

import re
from uuid import uuid4

from .knowledge import ESCALATION_TERMS, INJECTION_TERMS, intent_of
from .models import Decision, OrderStatusRequest, OrderStatusResponse, Tenant, TraceStep
from .order_status_fixtures import DEMO_PERSONAS, ORDER_STATUSES


ID_CANDIDATE = re.compile(
    r"(?<!\w)ORD(?:[-–—]+[ \t]*[\w-]*|[ \t]+\d[\w-]*|\d[\w-]*|\b)",
    re.IGNORECASE,
)
VALID_ID = re.compile(r"ORD[- ]?([0-9]{4,6})", re.IGNORECASE)
LABELLED_ID = re.compile(r"\b(?:order\s+(?:id|number)|order\s*#)\s*(?:is\s+|[:#]\s*)?([^\s,.?!]+)", re.IGNORECASE)
STATUS_REQUEST = re.compile(
    r"\b(?:track(?:ing)?|where\s+is\s+(?:my|the|this)\s+order|"
    r"(?:order\b.*\bstatus|status\b.*\border)|has\b[^?]*\border\b[^?]*\b(?:shipped|arrived|been delivered))\b",
    re.IGNORECASE,
)
MODIFICATION = re.compile(
    r"\b(?:cancel|modify|edit|change|reschedule|amend|redirect|"
    r"update(?!\s+me\b)|set\s+(?:the\s+)?(?:order\b|status\b)|"
    r"mark\b[^.!?]*\b(?:delivered|refunded|shipped))\b",
    re.IGNORECASE,
)
POLICY_QUESTION = re.compile(r"\b(?:policy|how\s+(?:do|can)\s+i)\b", re.IGNORECASE)
SUPPORTED_STATUSES = frozenset({"Delivered", "Processing", "Refunded"})
RETRY_ID = "I couldn't verify that order. Please check your demo Order ID and try again."
UNAVAILABLE = "I can't retrieve the current order status right now. Please try again later or contact customer service."


def read_status(tenant: Tenant, customer: str, order_id: str) -> str | None:
    partition = ORDER_STATUSES.get((tenant, customer))
    if partition is None or order_id not in partition:
        return None
    return partition[order_id] or ""


def run_order_status(request: OrderStatusRequest) -> OrderStatusResponse:
    message = request.message.strip()
    lower = message.lower()
    scope = DEMO_PERSONAS.get(request.persona) if request.persona is not None else None
    tenant = scope[0] if scope else "atlas"
    trace = [TraceStep(stage="intake", tool="normalise_input", outcome="passed",
                       detail="Received a synthetic demo request")]

    def finish(decision: Decision, outcome: str, answer: str, *,
               intent: str = "order", awaiting: bool = False) -> OrderStatusResponse:
        trace.append(TraceStep(stage="workflow", tool="order_status",
                               outcome=outcome, detail="Synthetic order-status demo"))
        return OrderStatusResponse(
            run_id=str(uuid4()), decision=decision, intent=intent, answer=answer,
            tenant=tenant, citations=[], evidence_count=0, trace=trace,
            awaiting_order_id=awaiting,
        )

    if any(term in lower for term in INJECTION_TERMS):
        return finish("blocked", "blocked", "I cannot override this workflow or reveal hidden instructions.",
                      intent="security")
    if any(term in lower for term in ESCALATION_TERMS):
        return finish("escalated", "handoff", "Please contact customer service. This demo did not create a ticket.",
                      intent="handoff")
    if scope is None:
        return finish("blocked", "persona_required", "Please select a demo persona and try again.")

    candidates = ID_CANDIDATE.findall(message)
    status_request = bool(STATUS_REQUEST.search(message))
    routed_intent = intent_of(message)
    if MODIFICATION.search(message) and (status_request or candidates or not POLICY_QUESTION.search(message)):
        return finish("abstained", "read_only", "This feature can check order status. It cannot cancel or modify orders.")
    if routed_intent in {"refund", "refund_eligibility", "shipping", "warranty", "cancellation"} and (
        not status_request or routed_intent in {"refund_eligibility", "cancellation"}
    ):
        return finish("abstained", "topic_changed", "For policy or refund questions, switch to the support workflow.",
                      intent=routed_intent)
    if not status_request and request.continuation is None:
        return finish("clarification", "intent_required", "Please tell me what you need to know about your order.")

    order_ids = set()
    for candidate in candidates:
        match = VALID_ID.fullmatch(candidate)
        if match is None:
            return finish("abstained", "invalid_id", RETRY_ID, awaiting=True)
        order_ids.add(f"ORD-{match[1]}")
    if len(order_ids) > 1:
        return finish("clarification", "single_id_required", "Please provide one demo Order ID at a time.", awaiting=True)
    if not order_ids:
        if LABELLED_ID.search(message) or (request.continuation and message and not status_request):
            return finish("abstained", "invalid_id", RETRY_ID, awaiting=True)
        return finish("clarification", "id_required", "Please provide your demo Order ID.", awaiting=True)

    order_id = order_ids.pop()
    try:
        status = read_status(*scope, order_id)
    except Exception:
        return finish("abstained", "unavailable", UNAVAILABLE)
    if status is None:
        return finish("abstained", "unverified", RETRY_ID, awaiting=True)
    if status not in SUPPORTED_STATUSES:
        return finish("abstained", "unavailable", UNAVAILABLE)
    return finish("answered", "found", f"Order {order_id} is {status.lower()}.")
