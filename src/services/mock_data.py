"""
Domain mock data and pre-built demonstration scenarios for EstimateOS.
Reflects authentic private capital transactions (Anduin Transactions ecosystem).
"""
from src.schemas.scope import ScopeIntakeSchema, WorkstreamItem

DEMO_BRIEFS = {
    "1. Singapore PE Fund (SingaVCC) — Full LP Onboarding & Custom LPA Review": """
Subject: Kickoff: SingaCapital Growth Fund II (VCC) - LP Onboarding & Legal Review
From: implementation-liaison@singacapital.com
To: onboarding-team@anduin.tech

Hi Anduin Team,

We are launching our second Variable Capital Company (VCC) sub-fund out of Singapore next month and need to digitize our LP onboarding process. 
Here are our requirements:
1. We target 60 institutional and family office Limited Partners (LPs), roughly 40% from Singapore/Hong Kong and 60% from the US/EU.
2. Legal agreements: We have a standard 120-page Singapore VCC LPA, but we anticipate 12 custom Side Letters with specific MFN (Most Favored Nation) and bespoke reporting requirements. We need your AI review engine to verify clauses and identify conflicting obligations before execution.
3. Integrations: We must sync all completed investor subscription packs and KYC verification files into our fund administrator's SFTP pipeline (Citco format). We also use Salesforce for our investor relations team.
4. Compliance: Full MAS-compliant AML/KYC automated checks, with FATCA/CRS self-certification routing.
5. Timeline: Target first-close is in 8 weeks.

Please provide a structured scope and estimated effort for this deployment.
""",

    "2. Delaware VC Fund V — Rapid Subscription Flow with Investran API": """
Subject: Scope Request: Apex Horizon Ventures Fund V - LP Subscription Flow
From: ops@apexhorizon.vc
To: solutions@anduin.tech

Hello Team,

Apex Horizon is preparing to close Fund V (Delaware LP structure). We want to replace our manual DocuSign paper drill with Anduin's automated subscription flow.
- Scope: 35 early-stage venture LPs (predominantly US-based institutional endowments and founders).
- Documents: Standard National Venture Capital Association (NVCA) model subscription agreements. No bespoke side letters expected for this seed closing.
- System Integration: Direct two-way API integration into FIS Investran to auto-populate capital commitment ledger and investor entity IDs.
- Timeline: We need to go live within 4 weeks.

Looking forward to your implementation breakdown.
""",

    "3. Incomplete Client RFP — Ambiguous Volumes & Unspecified Systems": """
Subject: RFP Inquiry: Fund Automation Platform
From: inquiry@undisclosed-capital.com
To: contact@anduin.tech

Hi,

We are a private capital firm looking to automate our investor onboarding and legal document management.
We want to digitize our subscription workflow and connect it to our internal fund operations systems.
Can you give us a ballpark estimate of how long this implementation will take and how many engineering hours are needed?

Thanks,
Operations Team
"""
}

PARSED_SCENARIOS = {
    "1. Singapore PE Fund (SingaVCC) — Full LP Onboarding & Custom LPA Review": ScopeIntakeSchema(
        project_name="SingaCapital Growth Fund II (VCC)",
        client_type="PE",
        transaction_type="LP Onboarding",
        fund_strategy="Growth Equity",
        jurisdiction="Singapore",
        estimated_investor_count=60,
        source_documents=["Singapore VCC LPA (120 pages)", "12 Bespoke Side Letters"],
        integration_endpoints=["Citco SFTP", "Salesforce CRM"],
        target_go_live_weeks=8.0,
        known_constraints=["MAS AML/KYC regulatory deadline", "Multi-jurisdictional tax reporting (FATCA/CRS)"],
        workstreams=[
            WorkstreamItem(
                name="Project Discovery & Regulatory Kickoff",
                category="discovery_kickoff",
                description="Align onboarding questionnaire with MAS VCC guidelines and investor tax requirements.",
                assumptions=["Dedicated client compliance officer available for sign-off"],
                risks=["Delays in client stakeholder approvals"],
                optimistic_hours=12.0,
                most_likely_hours=16.0,
                pessimistic_hours=24.0
            ),
            WorkstreamItem(
                name="LPA & Side Letter Clause Extraction",
                category="document_ocr_extraction",
                description="Digitize 120-page LPA and ingest 12 custom Side Letters into the clause rules engine.",
                assumptions=["Side letters provided in searchable PDF format"],
                risks=["Ambiguous MFN clause language requiring external legal counsel confirmation"],
                optimistic_hours=24.0,
                most_likely_hours=36.0,
                pessimistic_hours=54.0
            ),
            WorkstreamItem(
                name="Subscription Workflow & KYC Rules Config",
                category="rules_engine_configuration",
                description="Configure multi-tier investor qualification logic and automated FATCA/CRS verification.",
                assumptions=["Standard MAS AML checklist"],
                risks=["Complex corporate entity ownership chains (UBO verification)"],
                optimistic_hours=20.0,
                most_likely_hours=28.0,
                pessimistic_hours=42.0
            ),
            WorkstreamItem(
                name="Citco SFTP & Salesforce Integration",
                category="integration_api_sftp",
                description="Build automated daily batch synchronization to Citco SFTP and bi-directional Salesforce sync.",
                assumptions=["Citco test sandbox environment available in Week 2"],
                risks=["API schema discrepancies and firewall whitelisting delays"],
                optimistic_hours=32.0,
                most_likely_hours=46.0,
                pessimistic_hours=68.0
            ),
            WorkstreamItem(
                name="Quality Assurance & End-to-End UAT",
                category="quality_assurance_uat",
                description="Dry-run 5 mock LP investor test journeys across institutional and individual profiles.",
                assumptions=["Client participates in 2 scheduled UAT rounds"],
                risks=["Late-stage changes to subscription questionnaire"],
                optimistic_hours=18.0,
                most_likely_hours=24.0,
                pessimistic_hours=36.0
            ),
            WorkstreamItem(
                name="Go-Live Orchestration & Engagement PM",
                category="project_management_coordination",
                description="Manage 8-week delivery cadence, status reporting, and launch coordination.",
                assumptions=["Weekly stakeholder check-ins"],
                risks=["First-close investor deadline shift"],
                optimistic_hours=16.0,
                most_likely_hours=20.0,
                pessimistic_hours=28.0
            )
        ]
    ),

    "2. Delaware VC Fund V — Rapid Subscription Flow with Investran API": ScopeIntakeSchema(
        project_name="Apex Horizon Ventures Fund V",
        client_type="VC",
        transaction_type="Subscription Flow",
        fund_strategy="Venture Capital",
        jurisdiction="US-Delaware",
        estimated_investor_count=35,
        source_documents=["NVCA Model Subscription Agreement"],
        integration_endpoints=["FIS Investran API"],
        target_go_live_weeks=4.0,
        known_constraints=["Strict 4-week go-live deadline"],
        workstreams=[
            WorkstreamItem(
                name="Kickoff & Workflow Baseline",
                category="discovery_kickoff",
                description="Review NVCA agreement fields and define data mapping to Investran.",
                assumptions=["Standard NVCA terms with zero bespoke amendments"],
                risks=["None identified"],
                optimistic_hours=8.0,
                most_likely_hours=10.0,
                pessimistic_hours=14.0
            ),
            WorkstreamItem(
                name="Subscription Template Digitization",
                category="rules_engine_configuration",
                description="Configure smart forms, e-sign anchors, and accredited investor checks.",
                assumptions=["Pre-vetted NVCA templates available"],
                risks=["Minor field re-mapping"],
                optimistic_hours=14.0,
                most_likely_hours=18.0,
                pessimistic_hours=26.0
            ),
            WorkstreamItem(
                name="Investran REST API Sync",
                category="integration_api_sftp",
                description="Connect webhooks to push completed subscriptions into Investran.",
                assumptions=["Active Investran REST API credentials provided on Day 1"],
                risks=["Rate limits on bulk investor push"],
                optimistic_hours=20.0,
                most_likely_hours=26.0,
                pessimistic_hours=38.0
            ),
            WorkstreamItem(
                name="UAT & Pilot Launch",
                category="quality_assurance_uat",
                description="Verification of end-to-end data flow with 3 pilot investors.",
                assumptions=["Pilot testers available in Week 3"],
                risks=["Rework on field validation"],
                optimistic_hours=10.0,
                most_likely_hours=14.0,
                pessimistic_hours=20.0
            ),
            WorkstreamItem(
                name="Delivery Management",
                category="project_management_coordination",
                description="Sprint management and handover documentation.",
                assumptions=["Single client point of contact"],
                risks=["None"],
                optimistic_hours=8.0,
                most_likely_hours=10.0,
                pessimistic_hours=14.0
            )
        ]
    ),

    "3. Incomplete Client RFP — Ambiguous Volumes & Unspecified Systems": ScopeIntakeSchema(
        project_name="Undisclosed Capital Automation",
        client_type="PE",
        transaction_type="LP Onboarding",
        fund_strategy=None,
        jurisdiction=None,
        estimated_investor_count=None,
        source_documents=[],
        integration_endpoints=[],
        target_go_live_weeks=None,
        known_constraints=["Unspecified timeline and volumes"],
        workstreams=[
            WorkstreamItem(
                name="High-Level Scope Discovery",
                category="discovery_kickoff",
                description="Clarify requirements, investor volumes, and target jurisdictions.",
                assumptions=["Client will participate in scoping workshop"],
                risks=["High ambiguity in core requirements"],
                optimistic_hours=14.0,
                most_likely_hours=20.0,
                pessimistic_hours=32.0
            ),
            WorkstreamItem(
                name="Provisional Subscription Flow Configuration",
                category="rules_engine_configuration",
                description="Generic investor onboarding flow setup.",
                assumptions=["Standard templates will suffice"],
                risks=["Substantial scope creep once actual legal documents are revealed"],
                optimistic_hours=25.0,
                most_likely_hours=40.0,
                pessimistic_hours=70.0
            ),
            WorkstreamItem(
                name="Unspecified Integration Provision",
                category="integration_api_sftp",
                description="Estimated integration budget without endpoint specifications.",
                assumptions=["REST API available"],
                risks=["Legacy systems or custom batch files required"],
                optimistic_hours=30.0,
                most_likely_hours=50.0,
                pessimistic_hours=85.0
            )
        ]
    )
}
