# 🤖 ai-automation-toolkit

Automation-first portfolio repo for real client workflows.

## What this project shows
- API-first automation services
- Webhook ingestion patterns
- LLM-ready summarization pipeline
- Reusable workflow templates (CRM lead enrich, support summary, document intake)
- Production hygiene: tests + CI + docs

## Quickstart
```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn automation_toolkit.api.main:app --reload --port 8200
```

Open docs: <http://localhost:8200/docs>

## Endpoints
- `GET /health`
- `GET /v1/workflows`
- `POST /v1/webhook/support-summary`
- `POST /v1/webhook/lead-enrich`
- `POST /v1/webhook/document-intake`

## Why employers care
This repo proves you can turn AI ideas into automation-ready backend surfaces that can plug into n8n/Zapier/Make-style systems.
