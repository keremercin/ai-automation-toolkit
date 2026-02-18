from fastapi import FastAPI
from pydantic import BaseModel, Field

from automation_toolkit.config import settings
from automation_toolkit.services import (
    document_intake,
    enrich_lead,
    list_workflows,
    summarize_support_ticket,
)

app = FastAPI(title=settings.app_name, version="0.2.0")


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


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": settings.app_name}


@app.get("/v1/workflows")
def workflows() -> dict:
    return {"items": list_workflows()}


@app.post("/v1/webhook/support-summary")
def support_summary(req: SupportSummaryRequest) -> dict:
    return summarize_support_ticket(req.ticket_text)


@app.post("/v1/webhook/lead-enrich")
def lead_enrich(req: LeadEnrichRequest) -> dict:
    return enrich_lead(req.model_dump())


@app.post("/v1/webhook/document-intake")
def doc_intake(req: DocumentIntakeRequest) -> dict:
    return document_intake(req.model_dump())
