import copy
import pytest
from app.engine import run_agent
from app.knowledge import ORDERS
from app.models import RunRequest


def run(message, tenant="atlas"):
    return run_agent(RunRequest(message=message, tenant=tenant))


@pytest.mark.parametrize("tenant,order,status,reason", [
    ("atlas", "ORD-1001", "eligible", "eligible"),
    ("atlas", "ORD-1010", "eligible", "eligible"),
    ("atlas", "ORD-1011", "ineligible", "window"),
    ("atlas", "ORD-1012", "ineligible", "used"),
    ("atlas", "ORD-1002", "ineligible", "delivered"),
    ("atlas", "ORD-1013", "needs_more_information", "condition"),
    ("atlas", "ORD-1014", "needs_more_information", "date"),
    ("beacon", "ORD-2010", "eligible", "eligible"),
    ("beacon", "ORD-2011", "ineligible", "window"),
    ("beacon", "ORD-2001", "already_refunded", "already refunded"),
])
def test_assessment(tenant, order, status, reason):
    result = run(f"Is order {order} eligible for a refund?", tenant)
    assert result.eligibility.status == status
    assert reason in result.answer.lower()
    assert result.eligibility.assessment_date.isoformat() == "2026-11-17"
    assert result.citations[0].source_id == ("AT-REF-01" if tenant == "atlas" else "BE-REF-01")
    assert [s.tool for s in result.trace][-4:] == ["knowledge_search", "eligibility_assessment", "citation_validator", "response_guard"]


def test_missing_unknown_and_isolation():
    assert run("Am I eligible for a refund?").decision == "clarification"
    assert run("Can I get a refund for my order?").decision == "clarification"
    assert run("Is order ORD-9999 eligible for a refund?").decision == "abstained"
    for tenant, order in [("atlas", "ORD-2001"), ("beacon", "ORD-1001")]:
        result = run(f"Is order {order} eligible for a refund?", tenant)
        assert result.decision == "blocked"
        assert result.eligibility.status == "blocked_or_unsupported"
        assert order not in result.model_dump_json()
        assert "Refund processed" not in result.model_dump_json()


def test_existing_routes_and_no_mutation():
    before = copy.deepcopy(ORDERS)
    assert run("What is the refund policy?").intent == "refund"
    assert run("Can I return an item?", "beacon").intent == "refund"
    assert run("Track order ORD-1001").answer == "ORD-1001: Delivered. Delivered 8 November (synthetic record)."
    run("Is order ORD-1001 eligible for a refund?")
    assert ORDERS == before


def test_specifications_include_both():
    from fastapi.testclient import TestClient
    from app.main import app
    body = TestClient(app).get("/api/specifications").json()
    assert body["id"] == "SPEC-001"
    assert any(spec["id"] == "SPEC-002" for spec in body["additional_specifications"])


def test_unknown_status_and_future_date_do_not_assume_eligibility():
    from datetime import date
    from app.knowledge import REFUND_POLICIES
    from app.refund_eligibility import assess
    policy = REFUND_POLICIES["atlas"]
    assert assess({"condition": "unused"}, policy)[0] == "needs_more_information"
    assert assess({"status": "Delivered", "condition": "unused", "delivery_date": date(2026, 11, 18)}, policy)[0] == "needs_more_information"


def test_public_api_additive_contract():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    body = client.post("/api/agent/run", json={"message": "Is order ORD-1001 eligible for a refund?"}).json()
    assert {"run_id", "mode", "decision", "intent", "answer", "tenant", "citations", "evidence_count", "trace"} <= body.keys()
    assert body["eligibility"] == {"status": "eligible", "assessment_date": "2026-11-17"}
    assert client.post("/api/agent/run", json={"message": "What is the refund policy?"}).json()["eligibility"] is None
