from openai import OpenAI

from automation_toolkit.config import settings


def summarize_support_ticket(text: str) -> dict:
    if settings.openai_api_key:
        client = OpenAI(api_key=settings.openai_api_key)
        resp = client.chat.completions.create(
            model=settings.openai_chat_model,
            temperature=0.2,
            messages=[
                {"role": "system", "content": "Summarize customer support ticket in concise bullets."},
                {"role": "user", "content": text[:5000]},
            ],
        )
        summary = (resp.choices[0].message.content or "").strip()
    else:
        summary = text[:240] + ("..." if len(text) > 240 else "")

    priority = "high" if any(k in text.lower() for k in ["urgent", "down", "failed", "error"]) else "normal"

    return {
        "summary": summary,
        "priority": priority,
    }


def enrich_lead(payload: dict) -> dict:
    name = payload.get("name", "Unknown")
    company = payload.get("company", "Unknown")
    domain = payload.get("domain", "")

    score = 50
    if domain.endswith(".io") or domain.endswith(".ai"):
        score += 20
    if payload.get("employees", 0) and payload.get("employees", 0) > 50:
        score += 15

    return {
        "name": name,
        "company": company,
        "domain": domain,
        "lead_score": min(score, 100),
        "segment": "mid-market" if score >= 70 else "smb",
    }


def document_intake(payload: dict) -> dict:
    text = payload.get("document_text", "")
    doc_type = "contract" if "agreement" in text.lower() or "contract" in text.lower() else "other"
    has_amount = any(x in text.lower() for x in ["usd", "$", "eur", "try", "amount", "payment"])

    return {
        "document_id": payload.get("document_id", "temp-doc"),
        "document_type": doc_type,
        "has_monetary_terms": has_amount,
        "length": len(text),
    }


def list_workflows() -> list[dict]:
    return [
        {
            "name": "support-summary",
            "endpoint": "/v1/webhook/support-summary",
            "description": "Summarize support tickets and assign priority",
        },
        {
            "name": "lead-enrich",
            "endpoint": "/v1/webhook/lead-enrich",
            "description": "Score incoming leads for sales routing",
        },
        {
            "name": "document-intake",
            "endpoint": "/v1/webhook/document-intake",
            "description": "Classify incoming document text and flag monetary terms",
        },
    ]
