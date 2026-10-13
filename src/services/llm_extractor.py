"""
AI & Heuristic Scope Extractor for EstimateOS.
Supports:
1. Direct Google Gemini 2.0 Flash REST API (Zero external pip dependencies).
2. Advanced Local Rule-Based & Heuristic Extractor (Offline / Zero-API-Key fallback).
"""
import re
import json
import urllib.request
from typing import Optional
from src.schemas.scope import ScopeIntakeSchema, WorkstreamItem
from src.services.mock_data import PARSED_SCENARIOS

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

SYSTEM_PROMPT = """
You are the Lead Solutions & Scoping Architect for Anduin Transactions.
Analyze incoming client requests (emails, kickoff briefs, RFPs) for private capital transaction digitization, LP onboarding, and legal workflow automation.

Output a valid JSON object matching this exact schema:
{
  "project_name": "string",
  "client_type": "VC" | "PE" | "Fund Administrator" | "Law Firm" | "LP",
  "transaction_type": "string (e.g. LP Onboarding, Subscription Flow, LPA Digitization, Integration)",
  "fund_strategy": "string or null",
  "jurisdiction": "string or null",
  "estimated_investor_count": integer or null,
  "source_documents": ["string"],
  "integration_endpoints": ["string"],
  "target_go_live_weeks": float or null,
  "known_constraints": ["string"],
  "workstreams": [
    {
      "name": "string",
      "category": "discovery_kickoff" | "document_ocr_extraction" | "rules_engine_configuration" | "integration_api_sftp" | "data_migration_reconciliation" | "quality_assurance_uat" | "project_management_coordination",
      "description": "string",
      "assumptions": ["string"],
      "risks": ["string"],
      "dependencies": ["string"],
      "optimistic_hours": float,
      "most_likely_hours": float,
      "pessimistic_hours": float
    }
  ]
}

Enforce:
1. 0 <= optimistic_hours <= most_likely_hours <= pessimistic_hours.
2. If facts are unmentioned, set null or empty array. DO NOT hallucinate investor counts or systems.
3. Return ONLY pure JSON.
"""

def extract_scope_with_gemini(raw_text: str, api_key: str) -> Optional[ScopeIntakeSchema]:
    """Calls Google Gemini 2.0 Flash via standard HTTP REST API."""
    url = f"{GEMINI_API_URL}?key={api_key.strip()}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{SYSTEM_PROMPT}\n\nClient Brief:\n\"\"\"\n{raw_text}\n\"\"\""}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "responseMimeType": "application/json"
        }
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            candidate = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed_json = json.loads(candidate)
            return ScopeIntakeSchema(**parsed_json)
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None

def extract_scope_heuristics(raw_text: str) -> ScopeIntakeSchema:
    """
    Advanced offline heuristic extractor for EstimateOS.
    Analyzes arbitrary text without requiring an external API key.
    """
    # 1. Check if matches one of the preset scenarios
    for title, parsed_scope in PARSED_SCENARIOS.items():
        if parsed_scope.project_name.lower() in raw_text.lower():
            return parsed_scope

    # 2. Extract Project Name
    project_name = "Custom Ingested Transaction"
    subj_match = re.search(r"(?:subject|project|fund|kickoff):\s*([^\n\r]+)", raw_text, re.IGNORECASE)
    if subj_match:
        project_name = subj_match.group(1).strip()
    else:
        first_line = raw_text.strip().split("\n")[0][:40]
        if first_line:
            project_name = first_line.strip()

    # 3. Client Type
    client_type = "PE"
    if re.search(r"\b(vc|venture|seed)\b", raw_text, re.IGNORECASE):
        client_type = "VC"
    elif re.search(r"\b(fund admin|administrator|accounting)\b", raw_text, re.IGNORECASE):
        client_type = "Fund Administrator"
    elif re.search(r"\b(law firm|legal counsel|attorney)\b", raw_text, re.IGNORECASE):
        client_type = "Law Firm"

    # 4. Transaction Type
    t_type = "LP Onboarding"
    if re.search(r"\bsubscription\b", raw_text, re.IGNORECASE):
        t_type = "Subscription Flow"
    elif re.search(r"\blpa\b|\bdigitiz", raw_text, re.IGNORECASE):
        t_type = "LPA Digitization"
    elif re.search(r"\bintegrat|api|sftp\b", raw_text, re.IGNORECASE):
        t_type = "Integration Pipeline"

    # 5. Investor Count
    investor_count = None
    inv_match = re.search(r"(\d+)\s*(?:lps|investors|limited partners|subscribers)", raw_text, re.IGNORECASE)
    if inv_match:
        investor_count = int(inv_match.group(1))

    # 6. Jurisdiction
    jurisdiction = None
    if re.search(r"\b(singapore|sg|vcc)\b", raw_text, re.IGNORECASE):
        jurisdiction = "Singapore"
    elif re.search(r"\b(delaware|us|united states)\b", raw_text, re.IGNORECASE):
        jurisdiction = "US-Delaware"
    elif re.search(r"\b(cayman|ky)\b", raw_text, re.IGNORECASE):
        jurisdiction = "Cayman Islands"
    elif re.search(r"\b(luxembourg|lux)\b", raw_text, re.IGNORECASE):
        jurisdiction = "Luxembourg"

    # 7. Documents
    docs = []
    if re.search(r"\blpa\b", raw_text, re.IGNORECASE):
        docs.append("Limited Partnership Agreement (LPA)")
    side_letters = re.search(r"(\d+)?\s*(?:bespoke\s*)?side letters?", raw_text, re.IGNORECASE)
    if side_letters:
        docs.append(f"Custom Side Letters ({side_letters.group(0)})")
    if re.search(r"\bsubscription agreement|pack\b", raw_text, re.IGNORECASE):
        docs.append("Model Subscription Pack")

    # 8. Integrations
    endpoints = []
    for ep in ["Investran", "Citco", "Salesforce", "Allvue", "FIS", "REST API", "SFTP"]:
        if re.search(rf"\b{ep}\b", raw_text, re.IGNORECASE):
            endpoints.append(ep)

    # 9. Timeline
    timeline = None
    t_match = re.search(r"(\d+)\s*(?:weeks?|wks)", raw_text, re.IGNORECASE)
    if t_match:
        timeline = float(t_match.group(1))

    # 10. Generate Dynamic Workstreams based on extracted features
    workstreams = [
        WorkstreamItem(
            name="Project Discovery & Requirements Alignment",
            category="discovery_kickoff",
            description="Align questionnaire and compliance rules with governing regulatory standards.",
            assumptions=["Client stakeholders available for weekly sign-offs"],
            risks=["Scope changes during discovery"],
            optimistic_hours=10.0,
            most_likely_hours=14.0,
            pessimistic_hours=20.0
        )
    ]

    if docs:
        has_side_letters = any("side letter" in d.lower() for d in docs)
        workstreams.append(WorkstreamItem(
            name="Legal Document & Clause Extraction",
            category="document_ocr_extraction",
            description="Digitize agreement templates and extract custom clause covenants.",
            assumptions=["Documents provided in high-quality format"],
            risks=["Ambiguous MFN clauses requiring legal clarification"] if has_side_letters else [],
            optimistic_hours=20.0 if has_side_letters else 12.0,
            most_likely_hours=32.0 if has_side_letters else 18.0,
            pessimistic_hours=48.0 if has_side_letters else 26.0
        ))

    workstreams.append(WorkstreamItem(
        name="Workflow & Rules Engine Configuration",
        category="rules_engine_configuration",
        description="Configure qualification smart forms, tax self-certifications, and routing logic.",
        assumptions=["Standard KYC/AML requirements"],
        risks=["Complex entity structures"] if (investor_count and investor_count > 40) else [],
        optimistic_hours=16.0,
        most_likely_hours=24.0,
        pessimistic_hours=36.0
    ))

    if endpoints:
        workstreams.append(WorkstreamItem(
            name="Target System Integration & API Pipeline",
            category="integration_api_sftp",
            description=f"Automate data synchronization with {', '.join(endpoints)}.",
            assumptions=["Sandbox access available in Week 2"],
            risks=["Schema mismatch and authentication delays"],
            optimistic_hours=24.0,
            most_likely_hours=38.0,
            pessimistic_hours=56.0
        ))

    workstreams.extend([
        WorkstreamItem(
            name="End-to-End Quality Assurance & UAT",
            category="quality_assurance_uat",
            description="Execute multi-persona dry run testing and edge-case validation.",
            assumptions=["Client joins scheduled UAT sessions"],
            risks=["Late-stage changes to onboarding fields"],
            optimistic_hours=14.0,
            most_likely_hours=20.0,
            pessimistic_hours=30.0
        ),
        WorkstreamItem(
            name="Launch Orchestration & Delivery PM",
            category="project_management_coordination",
            description="Coordinate delivery cadence, sprint tracking, and final sign-off.",
            assumptions=["Weekly delivery cadence"],
            risks=[],
            optimistic_hours=12.0,
            most_likely_hours=16.0,
            pessimistic_hours=22.0
        )
    ])

    return ScopeIntakeSchema(
        project_name=project_name,
        client_type=client_type,
        transaction_type=t_type,
        fund_strategy=None,
        jurisdiction=jurisdiction,
        estimated_investor_count=investor_count,
        source_documents=docs,
        integration_endpoints=endpoints,
        target_go_live_weeks=timeline,
        known_constraints=[],
        workstreams=workstreams
    )

def extract_scope(raw_text: str, api_key: Optional[str] = None) -> ScopeIntakeSchema:
    """Unified entry point: tries Gemini Flash if key is provided, else uses heuristic parser."""
    if api_key and api_key.strip():
        gemini_result = extract_scope_with_gemini(raw_text, api_key.strip())
        if gemini_result:
            return gemini_result
    # Fallback to local heuristic extractor
    return extract_scope_heuristics(raw_text)
