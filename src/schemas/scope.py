"""
Pydantic contracts for EstimateOS.
Enforces strict typing and JSON-schema conformity for Scope Intake & WBS items.
"""
from typing import Literal, Optional, List, Dict
from pydantic import BaseModel, Field

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
    source_documents: List[str] = Field(default_factory=list)
    integration_endpoints: List[str] = Field(default_factory=list)
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
