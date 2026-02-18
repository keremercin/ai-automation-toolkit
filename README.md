# ai-automation-toolkit

[![CI](https://github.com/keremercin/ai-automation-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/keremercin/ai-automation-toolkit/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-009688)

Webhook-first automation backend for support summarization, lead enrichment, and document intake.

## Problem
Automation workflows break when payload formats are inconsistent and logic is duplicated across integrations.

## Architecture
- API entrypoint: `src/automation_toolkit/api/main.py`
- Workflow service layer: `src/automation_toolkit/services.py`
- Config via environment: `src/automation_toolkit/config.py`

See: `docs/ARCHITECTURE.md`

## Local Run
```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn automation_toolkit.api.main:app --reload --port 8200
```

## API Spec
- `GET /health`
- `GET /version`
- `GET /v1/workflows`
- `POST /v1/webhook/support-summary`
- `POST /v1/webhook/lead-enrich`
- `POST /v1/webhook/document-intake`

Standard response envelope:
```json
{
  "status": "ok",
  "data": {},
  "meta": {"model_version": "0.5.0", "latency_ms": 0},
  "error": null
}
```

## Evaluation
```bash
pytest
```

Contract test fixtures are under `tests/fixtures`.

## Results
- Consistent payload contracts across three workflow types
- Error schema standardized for invalid requests
- CI with lint + coverage gate

## Limitations
- Current workflow logic is deterministic and lightweight
- No persistence layer for workflow run history
- External timeout/circuit breaker policy is documented but not fully implemented

## Roadmap
- Add queue-backed async execution for heavy workflows
- Add workflow run audit store
- Add provider abstraction for multi-LLM backends

## Docs
- `docs/WORKFLOWS.md`
- `docs/CASE_STUDY.md`
- `docs/ARCHITECTURE.md`
- `docs/FAILURE_MODES.md`
- `docs/DEMO_SCRIPT_90S.md`
