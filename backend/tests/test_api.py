import platform
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    payload = client.get("/health").json()
    assert payload["status"] == "ok"
    assert payload["live_llm"] is False
    assert payload["python_version"] == platform.python_version()

def test_contract_and_citation():
    response = client.post("/api/agent/run", json={
        "message": "What is the refund policy?", "tenant": "atlas"})
    assert response.status_code == 200
    body = response.json()
    assert body["decision"] == "answered"
    assert body["citations"][0]["source_id"] == "AT-REF-01"

def test_trace_present():
    body = client.post("/api/agent/run", json={
        "message": "What is the warranty?", "tenant": "atlas"}).json()
    assert [x["tool"] for x in body["trace"]] == [
        "normalise_input", "intent_router", "knowledge_search",
        "citation_validator", "response_guard"]

def test_tenant_boundary():
    body = client.post("/api/agent/run", json={
        "message": "Track order ORD-2001", "tenant": "atlas"}).json()
    assert body["decision"] == "blocked"
    assert "Refund processed" not in body["answer"]

def test_request_validation():
    assert client.post("/api/agent/run", json={
        "message": "", "tenant": "atlas"}).status_code == 422
    assert client.post("/api/agent/run", json={
        "message": "Hi", "tenant": "other"}).status_code == 422

def test_evaluations():
    body = client.post("/api/evaluations/run").json()
    assert body["total"] >= 14 and body["failed"] == 0
    assert {f"EV-{number:03d}" for number in range(1, 15)} <= {result["id"] for result in body["results"]}

def test_specs_have_evidence():
    body = client.get("/api/specifications").json()
    assert all(item["proof"] for item in body["requirements"])
