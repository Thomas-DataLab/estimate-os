# EstimateOS · Backend Specification & Data Pipeline

**Component:** Python Services, Schema Contracts, & Algorithmic Engines  
**Version:** 1.0  
**Stack:** Python 3.11+, Pydantic v2, SQLite / DuckDB, Google GenAI / Groq SDK

---

## 1. Domain-Driven Pydantic Schemas

```python
"""
Pydantic contracts for EstimateOS.
Enforces strict typing and JSON-schema conformity between LLM output and internal engines.
"""
from typing import Literal, Optional, List, Dict
from pydantic import BaseModel, Field

# Taxonomy of standardized implementation workstreams in Capital Operations
WorkstreamCategory = Literal[
    "discovery_kickoff",
    "document_ocr_extraction",
    "rules_engine_configuration",
    "integration_api_sftp",
    "data_migration_reconciliation",
    "quality_assurance_uat",
    "project_management_coordination"
]

class WorkstreamItem(BaseModel):
    name: str = Field(..., description="Human-readable workstream title")
    category: WorkstreamCategory
    description: str
    assumptions: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    optimistic_hours: float = Field(..., ge=0)
    most_likely_hours: float = Field(..., ge=0)
    pessimistic_hours: float = Field(..., ge=0)

class ScopeIntakeSchema(BaseModel):
    project_name: str
    client_type: Literal["VC", "PE", "Fund Administrator", "Law Firm", "LP"]
    transaction_type: str = Field(..., description="e.g. 'LP Onboarding', 'Subscription Flow', 'LPA Digitization'")
    fund_strategy: Optional[str] = Field(None, description="e.g. 'Venture Capital', 'Growth Equity', 'Buyout'")
    jurisdiction: Optional[str] = Field(None, description="e.g. 'US-Delaware', 'Singapore', 'Cayman Islands', 'Luxembourg'")
    estimated_investor_count: Optional[int] = Field(None, description="Number of LPs/investors to onboard")
    source_documents: List[str] = Field(default_factory=list, description="e.g. ['LPA (120 pages)', 'Side Letters (8 docs)']")
    integration_endpoints: List[str] = Field(default_factory=list, description="e.g. ['Investran API', 'Salesforce CRM']")
    target_go_live_weeks: Optional[float] = None
    known_constraints: List[str] = Field(default_factory=list)
    workstreams: List[WorkstreamItem]

class CompletenessGap(BaseModel):
    severity: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW"]
    field_name: str
    finding: str
    impact_explanation: str
    suggested_inquiry: str

class CompletenessAuditResult(BaseModel):
    score: int = Field(..., ge=0, le=100)
    status: Literal["BLOCKED_CRITICAL", "PROVISIONAL_PERMITTED", "READY_FOR_COMMITMENT"]
    gaps: List[CompletenessGap]
    assumed_contingency_hours: float = 0.0

class AnalogousMatch(BaseModel):
    project_id: str
    project_name: str
    transaction_type: str
    similarity_score: float
    historical_estimated: float
    historical_actual: float
    historical_k_factor: float
    matching_dimensions: List[str]

class RoleAllocation(BaseModel):
    solutions_analyst_hours: float
    integration_engineer_hours: float
    qa_engineer_hours: float
    engagement_manager_hours: float

class WorkstreamEstimate(BaseModel):
    workstream_name: str
    category: WorkstreamCategory
    optimistic: float
    most_likely: float
    pessimistic: float
    expected_hours: float
    standard_deviation: float
    variance: float
    calibration_factor: float
    calibrated_hours: float
    role_mix: RoleAllocation

class FullProjectEstimate(BaseModel):
    estimate_id: str
    project_name: str
    raw_pert_hours: float
    calibrated_commitment_hours: float
    aggregate_std_dev: float
    confidence_interval_p80: float
    confidence_interval_p95: float
    completeness_score: int
    estimate_status: Literal["Provisional", "Firm Commitment", "Blocked"]
    workstreams: List[WorkstreamEstimate]
    analogous_projects: List[AnalogousMatch]
    total_role_allocation: RoleAllocation
```

---

## 2. LLM Extraction Prompt & Schema Enforcement

```python
"""
Prompt template for Scope Intake Extraction.
Enforces zero hallucination and strict JSON output.
"""
EXTRACTION_SYSTEM_PROMPT = """
You are the Lead Implementation & Scoping Architect for Anduin Transactions.
Your responsibility is to analyze incoming client requests (emails, kickoff briefs, RFPs) for private capital transaction digitization, LP onboarding, subscription flows, and fund operations integrations.

Deconstruct the incoming text into a structured Work Breakdown Structure (WBS) matching the exact JSON schema provided.

CRITICAL EXTRACTION DIRECTIVES:
1. DO NOT fabricate client facts, unmentioned software systems, or investor counts. If a parameter is unstated, output null or an empty list.
2. Separate explicit customer statements from unverified assumptions and known risk factors.
3. For effort sizing (Optimistic, Most Likely, Pessimistic):
   - Optimistic (O): Ideal conditions with zero unstated exceptions.
   - Most Likely (M): Standard execution based on stated complexity.
   - Pessimistic (P): Substantial revision cycles, dirty data, or integration blockers.
   - Strict constraint: 0 <= O <= M <= P.
4. Output ONLY valid JSON adhering strictly to the schema. No conversational prose or markdown formatting outside the JSON block.
"""
```

---

## 3. Completeness Gate Engine (Rules-Based Invariants)

The Completeness Gate executes deterministic audits to safeguard the organization from committing to ungrounded estimates:

```python
def evaluate_completeness(scope: ScopeIntakeSchema) -> CompletenessAuditResult:
    gaps: List[CompletenessGap] = []
    contingency = 0.0

    # Rule 1: Investor/LP Volume check
    if scope.transaction_type in ["LP Onboarding", "Subscription Flow"] and not scope.estimated_investor_count:
        gaps.append(CompletenessGap(
            severity="CRITICAL",
            field_name="estimated_investor_count",
            finding="Missing investor count for onboarding workflow.",
            impact_explanation="Directly drives KYC/AML review volume and document routing workload. Volatility exceeds 50%.",
            suggested_inquiry="How many distinct Limited Partners (LPs) are targeted for this initial fund close?"
        ))

    # Rule 2: Source Documents Clarity
    if not scope.source_documents:
        gaps.append(CompletenessGap(
            severity="HIGH",
            field_name="source_documents",
            finding="Source legal agreement types and page lengths not specified.",
            impact_explanation="LPA clause parsing and custom Side Letter extraction variance accounts for 35% of historic overruns.",
            suggested_inquiry="Will the onboarding include standard LPA templates or multi-jurisdictional Side Letters?"
        ))
        contingency += 18.0

    # Rule 3: Integration Specification
    if not scope.integration_endpoints and any(w.category == "integration_api_sftp" for w in scope.workstreams):
        gaps.append(CompletenessGap(
            severity="HIGH",
            field_name="integration_endpoints",
            finding="Integration workstream identified without specific target endpoints.",
            impact_explanation="API documentation quality across fund administrators varies from modern REST to legacy batch SFTP.",
            suggested_inquiry="Which fund admin or CRM platforms (e.g. Investran, Allvue, Salesforce) require automated sync?"
        ))
        contingency += 24.0

    # Rule 4: Jurisdiction / Regulatory Environment
    if not scope.jurisdiction:
        gaps.append(CompletenessGap(
            severity="MEDIUM",
            field_name="jurisdiction",
            finding="Fund jurisdiction unspecified.",
            impact_explanation="Cayman and Luxembourg fund vehicles introduce specific FATCA/CRS compliance complexities.",
            suggested_inquiry="Under which governing jurisdiction is the fund entity formed (e.g. US Delaware, Cayman, SG VCC)?"
        ))
        contingency += 8.0

    # Determine status & score
    critical_count = sum(1 for g in gaps if g.severity == "CRITICAL")
    high_count = sum(1 for g in gaps if g.severity == "HIGH")
    
    score = max(10, 100 - (critical_count * 30 + high_count * 15 + len(gaps) * 5))
    
    if critical_count > 0:
        status = "BLOCKED_CRITICAL"
    elif high_count > 0:
        status = "PROVISIONAL_PERMITTED"
    else:
        status = "READY_FOR_COMMITMENT"

    return CompletenessAuditResult(
        score=score,
        status=status,
        gaps=gaps,
        assumed_contingency_hours=contingency
    )
```

---

## 4. Analogous Project Matching Algorithm

The similarity matching engine ranks past historical projects to supply ground-truth evidence:

```python
def compute_similarity(target: ScopeIntakeSchema, hist_row: dict) -> float:
    score = 0.0
    
    # 1. Transaction Type exact match (35%)
    if target.transaction_type.lower() == hist_row['transaction_type'].lower():
        score += 0.35
    elif any(word in hist_row['transaction_type'].lower() for word in target.transaction_type.lower().split()):
        score += 0.20
        
    # 2. Client Type match (15%)
    if target.client_type == hist_row['client_type']:
        score += 0.15
        
    # 3. Jurisdiction match (15%)
    if target.jurisdiction and hist_row['jurisdiction']:
        if target.jurisdiction.lower() == hist_row['jurisdiction'].lower():
            score += 0.15
            
    # 4. Complexity delta (20%)
    target_complexity = 3 # Default or derived from workstream count
    comp_delta = abs(target_complexity - hist_row['complexity_score'])
    score += max(0.0, 0.20 - (comp_delta * 0.05))
    
    # 5. Overlapping risk tags (15%)
    hist_tags = set(hist_row['risk_tags'].lower().split(','))
    target_tags = set(r.lower() for w in target.workstreams for r in w.risks)
    overlap = len(hist_tags.intersection(target_tags))
    score += min(0.15, overlap * 0.05)
    
    return round(score, 3)
```

---

## 5. Seed Dataset: 14 Historical Anduin Projects

To showcase organizational learning, the seed dataset reflects a clear chronological trajectory: Early projects (H01–H06) suffered significant optimism bias ($K = 1.20 - 1.45$). Later projects (H09–H14), benefited from calibrated baselines ($K = 1.02 - 1.07$).

| ID | Project Name | Type | Jurisdiction | Comp | Est (h) | Act (h) | K Factor | Outcome Status |
|:---|:---|:---|:---|:---:|:---:|:---:|:---:|:---|
| **H01** | Apex Venture IV LP Intake | LP Onboarding | US-DE | 4 | 82.0 | 116.0 | **1.41** | Delayed: Underestimated Side Letters |
| **H02** | SingaCapital PE Fund I | Subscription Flow | SG (VCC) | 4 | 104.0 | 127.0 | **1.22** | Margin compressed: Custom AML |
| **H03** | BlackRock Parallel Vehicle LPA | LPA Digitization | Cayman | 5 | 74.0 | 101.0 | **1.36** | Rework: Complex MFN clauses |
| **H04** | Horizon Credit Fund Side Letters | Legal Workflow | US-DE | 4 | 91.0 | 132.0 | **1.45** | Scope overrun: 14 bespoke drafts |
| **H05** | Bain Capital Investor Migration | Data Migration | UK | 3 | 128.0 | 149.0 | **1.16** | Minor delay: Legacy CSV formatting |
| **H06** | Allvue Fund Admin REST Sync | Integration | US-DE | 4 | 156.0 | 181.0 | **1.16** | Sandbox API schema mismatch |
| **H07** | Sequoia Asia KYC Automation | Compliance | SG | 3 | 89.0 | 103.0 | **1.16** | Delivered: Secondary review cycle |
| **H08** | Lightspeed GP Portal Reporting | Reporting | US-DE | 2 | 67.0 | 72.0 | **1.07** | On-Time: Template reuse |
| **H09** | Nordic PE Buyout Fund VI | LP Onboarding | LUX | 4 | 121.0 | 128.0 | **1.06** | Calibrated: Accurate contingency |
| **H10** | Carlyle Growth LPA Rule Engine | Legal Workflow | US-DE | 4 | 144.0 | 154.0 | **1.07** | Delivered: Pre-vetted clause models |
| **H11** | Temasek Backlog Exception Flow | Subscription | SG | 3 | 77.0 | 79.0 | **1.03** | On-Time: Calibrated buffer |
| **H12** | KKR Secondary Portfolio Reconcile | Data Migration | US-DE | 3 | 109.0 | 114.0 | **1.05** | On-Time: Automated schema checks |
| **H13** | Citco Fund Admin SFTP Pipeline | Integration | Cayman | 3 | 93.0 | 95.0 | **1.02** | On-Time: Reused parser template |
| **H14** | Golden Gate Seed Fund LP Intake | LP Onboarding | US-DE | 2 | 65.0 | 66.0 | **1.02** | Perfect calibration: Zero variance |
