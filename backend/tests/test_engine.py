from app.models import RunRequest
from app.engine import run_agent
from app.evaluations import run_evaluations

def run(message, tenant="atlas"):
    return run_agent(RunRequest(message=message, tenant=tenant))

def test_all_acceptance_scenarios_pass():
    report = run_evaluations()
    assert report.failed == 0, report.model_dump()

def test_tenants_have_distinct_policies():
    a = run("What is the refund policy?", "atlas")
    b = run("What is the refund policy?", "beacon")
    assert a.citations[0].source_id == "AT-REF-01"
    assert b.citations[0].source_id == "BE-REF-01"

def test_abstention_when_no_evidence():
    result = run("What is the company CEO salary?")
    assert result.decision == "abstained"
    assert result.citations == []

def test_no_real_handoff_claim():
    result = run("I want to speak to a human agent")
    assert result.decision == "escalated"
    assert "No ticket was created" in result.answer
