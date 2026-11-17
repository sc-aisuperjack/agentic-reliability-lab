"""Synthetic fixtures only; no real customer data or proprietary material."""
from dataclasses import dataclass
import re
from datetime import date

@dataclass(frozen=True)
class Article:
    source_id: str
    tenant: str
    title: str
    intent: str
    body: str
    answer: str

@dataclass(frozen=True)
class RefundPolicy:
    tenant: str
    window_days: int
    article: Article

def refund_policy(tenant, days, source_id, title, processing, processing_answer):
    answer = (f"Atlas accepts returns of unused items within {days} days. {processing_answer}" if tenant == "atlas"
              else f"Beacon accepts unused returns within {days} days. {processing_answer}")
    article = Article(source_id, tenant, title, "refund",
                      f"Unused items can be {'refunded' if tenant == 'atlas' else 'returned'} within {days} days of delivery. {processing}", answer)
    return RefundPolicy(tenant, days, article)

REFUND_POLICIES = {
    "atlas": refund_policy("atlas", 30, "AT-REF-01", "Atlas refunds", "Approved refunds take 5 to 7 business days.", "Approved refunds take 5–7 business days."),
    "beacon": refund_policy("beacon", 14, "BE-REF-01", "Beacon refunds", "Approved refunds take 10 business days.", "Approved refunds take 10 business days."),
}

ARTICLES = [
    *(policy.article for policy in REFUND_POLICIES.values()),
    Article("AT-SHIP-02", "atlas", "Atlas shipping", "shipping",
            "Standard delivery: 3 to 5 business days; express delivery: 1 to 2 business days. These are estimates.",
            "Atlas standard shipping is estimated at 3–5 business days, express at 1–2 business days."),
    Article("BE-SHIP-02", "beacon", "Beacon shipping", "shipping",
            "Standard delivery: 5 to 7 business days. Express service is not available.",
            "Beacon shipping takes approximately 5–7 business days. Express shipping is unavailable."),
    Article("AT-WAR-03", "atlas", "Atlas warranty", "warranty",
            "Manufacturing defects are covered for 12 months. Accidental damage is excluded.",
            "Atlas provides a 12-month warranty against manufacturing defects, excluding accidental damage."),
    Article("BE-WAR-03", "beacon", "Beacon warranty", "warranty",
            "Manufacturing defects are covered for 24 months. Ordinary wear and accidental damage are excluded.",
            "Beacon provides a 24-month warranty covering manufacturing defects."),
    Article("AT-CAN-04", "atlas", "Atlas cancellation", "cancellation",
            "Orders may be cancelled until dispatch. Afterwards the returns policy applies.",
            "Atlas orders can be cancelled before dispatch. After dispatch, the returns policy applies."),
    Article("BE-CAN-04", "beacon", "Beacon cancellation", "cancellation",
            "Orders may be cancelled within 2 hours of placement if they have not shipped.",
            "Beacon orders can be cancelled within 2 hours, provided dispatch has not happened."),
]

ORDERS = {
    "ORD-1001": {"tenant": "atlas", "status": "Delivered", "detail": "Delivered 8 November (synthetic record).", "delivery_date": date(2026, 11, 8), "condition": "unused"},
    "ORD-1002": {"tenant": "atlas", "status": "Processing", "detail": "Preparing for dispatch (synthetic record)."},
    "ORD-2001": {"tenant": "beacon", "status": "Refunded", "detail": "Refund processed on 10 November (synthetic record)."},
    "ORD-1010": {"tenant": "atlas", "status": "Delivered", "detail": "Fictional delivery.", "delivery_date": date(2026, 10, 18), "condition": "unused"},
    "ORD-1011": {"tenant": "atlas", "status": "Delivered", "detail": "Fictional delivery.", "delivery_date": date(2026, 10, 17), "condition": "unused"},
    "ORD-1012": {"tenant": "atlas", "status": "Delivered", "detail": "Fictional delivery.", "delivery_date": date(2026, 11, 8), "condition": "used"},
    "ORD-1013": {"tenant": "atlas", "status": "Delivered", "detail": "Fictional delivery.", "delivery_date": date(2026, 11, 8)},
    "ORD-1014": {"tenant": "atlas", "status": "Delivered", "detail": "Fictional delivery.", "condition": "unused"},
    "ORD-2010": {"tenant": "beacon", "status": "Delivered", "detail": "Fictional delivery.", "delivery_date": date(2026, 11, 3), "condition": "unused"},
    "ORD-2011": {"tenant": "beacon", "status": "Delivered", "detail": "Fictional delivery.", "delivery_date": date(2026, 11, 2), "condition": "unused"},
}
TERMS = {
    "refund": ["refund", "return", "money back"],
    "shipping": ["shipping", "delivery time", "how long does shipping", "express", "postage"],
    "warranty": ["warranty", "guarantee", "defect", "broken"],
    "cancellation": ["cancel", "cancellation"],
    "order": ["track", "order status", "where is my order", "my order"],
}
INJECTION_TERMS = ["ignore previous instructions", "ignore all instructions", "reveal system prompt", "override your instructions"]
ESCALATION_TERMS = ["human agent", "real person", "speak to a human", "manager", "supervisor", "escalate"]

def intent_of(message: str) -> str:
    text = re.sub(r"\s+", " ", message.lower())
    if re.search(r"\b(refund|return|money back)\b", text) and (re.search(r"\b(eligible|eligibility|qualify|qualifies|qualification)\b", text) or re.search(r"\bord[- ]?\d{4,6}\b", text) or re.search(r"\b(my|this|the) order\b", text)):
        return "refund_eligibility"
    if re.search(r"\bord[- ]?\d{4,6}\b", text) and any(w in text for w in ("order", "track", "where", "status")):
        return "order"
    for intent, words in TERMS.items():
        if any(re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", text) for word in words):
            return intent
    return "unknown"

def find_article(tenant: str, intent: str):
    return next((a for a in ARTICLES if a.tenant == tenant and a.intent == intent), None)
