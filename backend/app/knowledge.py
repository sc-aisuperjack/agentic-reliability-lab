"""Synthetic fixtures only; no real customer data or proprietary material."""
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Article:
    source_id: str
    tenant: str
    title: str
    intent: str
    body: str
    answer: str

ARTICLES = [
    Article("AT-REF-01", "atlas", "Atlas refunds", "refund",
            "Unused items can be refunded within 30 days of delivery. Approved refunds take 5 to 7 business days.",
            "Atlas accepts returns of unused items within 30 days. Approved refunds take 5–7 business days."),
    Article("BE-REF-01", "beacon", "Beacon refunds", "refund",
            "Unused items can be returned within 14 days of delivery. Approved refunds take 10 business days.",
            "Beacon accepts unused returns within 14 days. Approved refunds take 10 business days."),
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
    "ORD-1001": {"tenant": "atlas", "status": "Delivered", "detail": "Delivered 8 November (synthetic record)."},
    "ORD-1002": {"tenant": "atlas", "status": "Processing", "detail": "Preparing for dispatch (synthetic record)."},
    "ORD-2001": {"tenant": "beacon", "status": "Refunded", "detail": "Refund processed on 10 November (synthetic record)."},
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
    if re.search(r"\bord[- ]?\d{4,6}\b", text) and any(w in text for w in ("order", "track", "where", "status")):
        return "order"
    for intent, words in TERMS.items():
        if any(re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", text) for word in words):
            return intent
    return "unknown"

def find_article(tenant: str, intent: str):
    return next((a for a in ARTICLES if a.tenant == tenant and a.intent == intent), None)
