"""Fictional personas and order statuses reserved for Feature 003."""

from types import MappingProxyType

from .models import Tenant


DEMO_PERSONAS: dict[str, tuple[Tenant, str]] = {
    "atlas-demo-a": ("atlas", "customer-a"),
    "atlas-demo-b": ("atlas", "customer-b"),
    "beacon-demo-a": ("beacon", "customer-a"),
}

ORDER_STATUSES = MappingProxyType({
    ("atlas", "customer-a"): MappingProxyType({
        "ORD-3101": "Delivered",
        "ORD-3102": "Processing",
    }),
    ("atlas", "customer-b"): MappingProxyType({"ORD-3201": "Processing"}),
    ("beacon", "customer-a"): MappingProxyType({"ORD-3301": "Refunded"}),
})
