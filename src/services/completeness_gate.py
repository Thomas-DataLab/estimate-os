"""
Completeness Gate Service for EstimateOS.
Executes deterministic audits against incoming scopes to flag critical gaps,
quantify missing input risk, and calculate provisional contingencies.
"""
from typing import List
from src.schemas.scope import ScopeIntakeSchema, CompletenessAuditResult, CompletenessGap

def evaluate_completeness(scope: ScopeIntakeSchema) -> CompletenessAuditResult:
    """
    Audits structured scope for missing dimensions and calculates risk scores.
    """
    gaps: List[CompletenessGap] = []
    contingency = 0.0

    # 1. Check Investor / LP Volume
    if any(k in scope.transaction_type.lower() for k in ["onboarding", "subscription"]) and not scope.estimated_investor_count:
        gaps.append(CompletenessGap(
            severity="CRITICAL",
            field_name="estimated_investor_count",
            finding="Missing investor count for onboarding workflow.",
            impact_explanation="Directly drives KYC/AML review volume and document routing workload. Volatility exceeds 50%.",
            suggested_inquiry="How many distinct Limited Partners (LPs) are targeted for this initial fund close?"
        ))
        contingency += 25.0

    # 2. Check Source Documents
    if not scope.source_documents:
        gaps.append(CompletenessGap(
            severity="HIGH",
            field_name="source_documents",
            finding="Source legal agreement types and document lengths not specified.",
            impact_explanation="LPA clause parsing and custom Side Letter extraction variance accounts for 35% of historic overruns.",
            suggested_inquiry="Will the onboarding include standard LPA templates or multi-jurisdictional bespoke Side Letters?"
        ))
        contingency += 18.0

    # 3. Check Integration Endpoints
    has_integration_workstream = any(w.category == "integration_api_sftp" for w in scope.workstreams)
    if has_integration_workstream and not scope.integration_endpoints:
        gaps.append(CompletenessGap(
            severity="HIGH",
            field_name="integration_endpoints",
            finding="Integration workstream identified without specific target endpoints.",
            impact_explanation="API documentation quality across fund administrators varies from modern REST to legacy batch SFTP.",
            suggested_inquiry="Which fund admin or CRM platforms (e.g. Investran, Allvue, Salesforce) require automated sync?"
        ))
        contingency += 24.0

    # 4. Check Governing Jurisdiction
    if not scope.jurisdiction:
        gaps.append(CompletenessGap(
            severity="MEDIUM",
            field_name="jurisdiction",
            finding="Fund governing jurisdiction unspecified.",
            impact_explanation="Cayman and Luxembourg fund vehicles introduce specific FATCA/CRS and depositary bank complexities.",
            suggested_inquiry="Under which governing jurisdiction is the fund entity formed (e.g. US Delaware, Cayman, SG VCC)?"
        ))
        contingency += 8.0

    # 5. Check Target Timeline
    if not scope.target_go_live_weeks:
        gaps.append(CompletenessGap(
            severity="LOW",
            field_name="target_go_live_weeks",
            finding="Go-live timeline not specified.",
            impact_explanation="Unspecified deadlines risk delivery compression and unbudgeted sprint overtime.",
            suggested_inquiry="What is the targeted first-close or go-live deadline for this implementation?"
        ))

    # Evaluate overall score
    critical_count = sum(1 for g in gaps if g.severity == "CRITICAL")
    high_count = sum(1 for g in gaps if g.severity == "HIGH")
    medium_count = sum(1 for g in gaps if g.severity == "MEDIUM")
    low_count = sum(1 for g in gaps if g.severity == "LOW")

    deductions = (critical_count * 35) + (high_count * 18) + (medium_count * 10) + (low_count * 5)
    score = max(10, 100 - deductions)

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
        assumed_contingency_hours=round(contingency, 1)
    )
