.PHONY: install run test lint

install:
	python -m venv .venv && . .venv/bin/activate && pip install -e .[dev]

run:
	uvicorn automation_toolkit.api.main:app --reload --port 8200

test:
	pytest

lint:
	ruff check src tests
