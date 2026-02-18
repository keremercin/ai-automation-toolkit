# Architecture

## Components
- FastAPI API entrypoint: `src/automation_toolkit/api/main.py`
- Workflow services: `src/automation_toolkit/services.py`
- Configuration: `src/automation_toolkit/config.py`

## Request flow
1. Webhook payload enters endpoint.
2. Pydantic validates payload contract.
3. Service layer executes deterministic enrichment/summarization logic.
4. Response returns in standard envelope (`status/data/meta/error`).

## Extensibility points
- Swap deterministic functions with model-backed providers.
- Add queue-backed async workers for heavy workflows.
- Add audit persistence for workflow run history.
