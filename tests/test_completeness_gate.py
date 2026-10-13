"""
Unit tests for the Completeness Gate service in EstimateOS.
Verifies critical blocking logic, provisional allowances, and inquiry generation.
"""
from src.schemas.scope import ScopeIntakeSchema, WorkstreamItem
from src.services.completeness_gate import evaluate_completeness

def test_completeness_gate_passes_full_scope():
    scope = ScopeIntakeSchema(
        project_name="Verified Project",
        client_type="PE",
        transaction_type="LP Onboarding",
        jurisdiction="Singapore",
        estimated_investor_count=50,
        source_documents=["Standard LPA"],
        integration_endpoints=["Citco SFTP"],
        target_go_live_weeks=8.0,
        workstreams=[
            WorkstreamItem(
                name="Integration",
                category="integration_api_sftp",
                description="SFTP Sync",
                optimistic_hours=10.0,
                most_likely_hours=15.0,
                pessimistic_hours=20.0
            )
        ]
    )
    audit = evaluate_completeness(scope)
    assert audit.status == "READY_FOR_COMMITMENT"
    assert audit.score == 100
    assert audit.assumed_contingency_hours == 0.0
    assert len(audit.gaps) == 0

def test_completeness_gate_blocks_missing_investor_count():
    scope = ScopeIntakeSchema(
        project_name="Missing Volume Project",
        client_type="VC",
        transaction_type="LP Onboarding",
        jurisdiction="US-Delaware",
        estimated_investor_count=None,  # Missing critical volume
        source_documents=["LPA"],
        integration_endpoints=[],
        target_go_live_weeks=4.0,
        workstreams=[
            WorkstreamItem(
                name="Discovery",
                category="discovery_kickoff",
                description="Kickoff",
                optimistic_hours=5.0,
                most_likely_hours=8.0,
                pessimistic_hours=12.0
            )
        ]
    )
    audit = evaluate_completeness(scope)
    assert audit.status == "BLOCKED_CRITICAL"
    assert audit.assumed_contingency_hours >= 25.0
    gap_fields = [g.field_name for g in audit.gaps]
    assert "estimated_investor_count" in gap_fields
