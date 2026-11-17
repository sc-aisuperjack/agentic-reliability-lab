"""Pure synthetic eligibility assessment; no financial operations."""
from datetime import date
from .knowledge import RefundPolicy

SIMULATION_DATE = date(2026, 11, 17)

def assess(order: dict, policy: RefundPolicy, assessment_date: date = SIMULATION_DATE):
    if order.get("status") == "Refunded":
        return "already_refunded", "This order is already refunded."
    if order.get("status") in ("Processing", "Shipped"):
        return "ineligible", "This order has not been delivered."
    if order.get("status") != "Delivered":
        return "needs_more_information", "The delivery status is missing or unknown."
    delivery = order.get("delivery_date")
    if delivery is not None and delivery > assessment_date:
        return "needs_more_information", "The delivery date is inconsistent with the simulation date."
    if delivery is not None and (assessment_date - delivery).days > policy.window_days:
        return "ineligible", "The return window has expired."
    if order.get("condition") == "used":
        return "ineligible", "The item is used."
    if delivery is None:
        return "needs_more_information", "The delivery date is missing."
    if order.get("condition") != "unused":
        return "needs_more_information", "The item condition is missing or unknown."
    return "eligible", "This order is eligible under the synthetic refund policy."
