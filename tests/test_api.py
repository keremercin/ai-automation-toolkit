import json
from pathlib import Path

from fastapi.testclient import TestClient

from automation_toolkit.api.main import app

FIXTURES = Path(__file__).parent / "fixtures"


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def test_health() -> None:
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "service" in body["data"]


def test_version() -> None:
    client = TestClient(app)
    r = client.get("/version")
    assert r.status_code == 200
    assert r.json()["data"]["version"] == "0.5.0"


def test_workflows() -> None:
    client = TestClient(app)
    r = client.get("/v1/workflows")
    assert r.status_code == 200
    assert len(r.json()["data"].get("items", [])) >= 3


def test_support_summary_contract() -> None:
    client = TestClient(app)
    r = client.post("/v1/webhook/support-summary", json=_fixture("support_summary_payload.json"))
    assert r.status_code == 200
    body = r.json()["data"]
    assert body["priority"] in {"high", "normal"}


def test_lead_enrich_contract() -> None:
    client = TestClient(app)
    r = client.post("/v1/webhook/lead-enrich", json=_fixture("lead_enrich_payload.json"))
    assert r.status_code == 200
    body = r.json()["data"]
    assert "lead_score" in body


def test_document_intake_contract() -> None:
    client = TestClient(app)
    r = client.post("/v1/webhook/document-intake", json=_fixture("document_intake_payload.json"))
    assert r.status_code == 200
    body = r.json()["data"]
    assert body["document_type"] in {"contract", "other"}


def test_invalid_payload_returns_standard_error() -> None:
    client = TestClient(app)
    r = client.post("/v1/webhook/support-summary", json={"ticket_text": ""})
    assert r.status_code == 422
    body = r.json()
    assert body["status"] == "error"
    assert body["error"]["code"] == "VALIDATION_ERROR"
