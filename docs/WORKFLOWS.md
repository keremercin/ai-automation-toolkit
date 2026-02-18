# Workflow Templates

## 1) Support Ticket Summarizer
Trigger: incoming support ticket webhook  
Action: call `/v1/webhook/support-summary`  
Output: summary + priority for Slack/CRM routing

## 2) Lead Enrichment
Trigger: new lead in form/CRM  
Action: call `/v1/webhook/lead-enrich`  
Output: lead score + segment for sales triage

## 3) Document Intake (next)
Trigger: uploaded doc event  
Action: OCR/classify/extract service call  
Output: structured metadata into database
