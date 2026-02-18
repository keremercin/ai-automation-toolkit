from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from automation_toolkit.config import settings
from automation_toolkit.services import (
    document_intake,
    enrich_lead,
    list_workflows,
    summarize_support_ticket,
)

APP_VERSION = "0.5.0"
app = FastAPI(title=settings.app_name, version=APP_VERSION)


class SupportSummaryRequest(BaseModel):
    ticket_text: str = Field(min_length=1)


class LeadEnrichRequest(BaseModel):
    name: str
    company: str
    domain: str = ""
    employees: int = 0


class DocumentIntakeRequest(BaseModel):
    document_id: str = "temp-doc"
    document_text: str = Field(min_length=1)


def api_response(*, data: Any = None, status: str = "ok", error: Any = None, latency_ms: int = 0) -> dict:
    return {
        "status": status,
        "data": data if data is not None else {},
        "meta": {"model_version": APP_VERSION, "latency_ms": latency_ms},
        "error": error,
    }


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=api_response(
            status="error",
            error={"code": "VALIDATION_ERROR", "message": "Invalid request payload", "details": exc.errors()},
        ),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=api_response(status="error", error={"code": "HTTP_ERROR", "message": str(exc.detail)}),
    )


@app.get("/health")
def health() -> dict:
    return api_response(data={"service": settings.app_name})


@app.get("/version")
def version() -> dict:
    return api_response(data={"service": settings.app_name, "version": APP_VERSION})


@app.get("/v1/workflows")
def workflows() -> dict:
    return api_response(data={"items": list_workflows()})


@app.post("/v1/webhook/support-summary")
def support_summary(req: SupportSummaryRequest) -> dict:
    return api_response(data=summarize_support_ticket(req.ticket_text))


@app.post("/v1/webhook/lead-enrich")
def lead_enrich(req: LeadEnrichRequest) -> dict:
    return api_response(data=enrich_lead(req.model_dump()))


@app.post("/v1/webhook/document-intake")
def doc_intake(req: DocumentIntakeRequest) -> dict:
    return api_response(data=document_intake(req.model_dump()))
