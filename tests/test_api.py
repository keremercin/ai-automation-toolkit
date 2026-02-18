from fastapi.testclient import TestClient

from automation_toolkit.api.main import app


def test_health() -> None:
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200


def test_workflows() -> None:
    client = TestClient(app)
    r = client.get("/v1/workflows")
    assert r.status_code == 200
    assert len(r.json().get("items", [])) >= 3


def test_support_summary() -> None:
    client = TestClient(app)
    payload = {"ticket_text": "Urgent: checkout is failing with payment error on mobile."}
    r = client.post("/v1/webhook/support-summary", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["priority"] in {"high", "normal"}


def test_lead_enrich() -> None:
    client = TestClient(app)
    payload = {"name": "Alice", "company": "Acme", "domain": "acme.ai", "employees": 80}
    r = client.post("/v1/webhook/lead-enrich", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "lead_score" in body


def test_document_intake() -> None:
    client = TestClient(app)
    payload = {"document_id": "d-1", "document_text": "This agreement includes payment of USD 5000."}
    r = client.post("/v1/webhook/document-intake", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert body["document_type"] in {"contract", "other"}
