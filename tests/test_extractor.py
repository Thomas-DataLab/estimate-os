"""
Unit tests for the Scope Extractor in EstimateOS.
Verifies offline heuristic extraction and schema compliance.
"""
from src.services.llm_extractor import extract_scope_heuristics

def test_heuristic_extractor_parses_unstructured_email():
    raw_email = """
    Subject: Horizon Capital Fund II (Delaware)
    We are a VC firm onboarding 45 LPs for our new seed vehicle.
    Need to connect Salesforce and Investran.
    Target go-live is 6 weeks.
    """
    scope = extract_scope_heuristics(raw_email)
    assert "Horizon Capital" in scope.project_name
    assert scope.client_type == "VC"
    assert scope.jurisdiction == "US-Delaware"
    assert scope.estimated_investor_count == 45
    assert "Salesforce" in scope.integration_endpoints
    assert "Investran" in scope.integration_endpoints
    assert scope.target_go_live_weeks == 6.0
    assert len(scope.workstreams) >= 4
    # Check that all workstreams obey O <= M <= P
    for w in scope.workstreams:
        assert 0 <= w.optimistic_hours <= w.most_likely_hours <= w.pessimistic_hours
