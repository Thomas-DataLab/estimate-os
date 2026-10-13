# EstimateOS · Scope-to-Actuals Intelligence Engine

> Built for the **Agent in the Shell** Hackathon (Anduin Cybernetics) · Challenge: **The Estimator** (Sales & Delivery).

---

## 1. Executive Summary & Problem Space

In modern B2B tech and financial operations, scoping incoming client projects is notoriously brittle:
1. **Unstructured & Ambiguous Inputs**: Prospective clients send vague RFPs, emails, or kickoff briefs with unstated constraints.
2. **Gut-Feel Estimation**: Project scoping relies on individual intuition without standardized work-breakdown structures.
3. **Broken Feedback Loop**: Actual delivery timesheets and ticket completion logs are rarely reconciled against initial sales estimates, preventing organizational learning.

**EstimateOS** bridges this gap:
- **LLM-Powered Scope Intake**: Ingests unstructured scopes, normalizes requirements into canonical workstreams, and triggers completeness gates to flag missing critical parameters.
- **Deterministic Estimation Engine**: Computes verifiable effort ranges, confidence scores, and line-item evidence backed by historical analogous cases.
- **Continuous Calibration Loop**: Ingests actual delivery metrics post-handover, conducts variance analysis, and proposes data-driven calibration adjustments approved by human operators.

> **Architectural Core**: *LLM interprets ambiguity; the deterministic data system owns the numbers.*

---

## 2. Core Architecture

```
[ Incoming Scope ]
(Client Email / RFP / Document Brief)
       │
       ▼
[ AI Extraction & Schema Gate ]
(JSON Schema Validation · Completeness Audit · Uncertainty Flagging)
       │
       ├─────────────────────────────────┐
       ▼                                 ▼
[ Historical Analogs Retrieval ]   [ Deterministic Effort Engine ]
(DuckDB Vector/Metadata Match)    (Workstream Multipliers & Drivers)
       │                                 │
       └────────────────┬────────────────┘
                        ▼
            [ Explainable Estimate ]
       (Workstream Breakdown · Confidence · Evidence Ledger)
                        │
                        ▼
           [ Delivery Actuals Loop ]
       (Timesheet Ingestion · Variance Audit · Parameter Calibration)
```

---

## 3. Tech Stack

- **Application & UI**: Python / Streamlit / Tailwind CSS
- **Data & Analytics Engine**: DuckDB (In-memory SQL analytics & historical ledger)
- **AI & Extraction Engine**: Google Gemini API (`gemini-2.0-flash` / `gemini-1.5-flash`) via structured JSON schema enforcement
- **Telemetry & Provenance**: Git-backed audit trail and evidence linking

---

## 4. Key Milestones

- [x] Challenge selection: The Estimator (Sales & Delivery)
- [x] Repository initialization & architectural blueprint
- [ ] Seed dataset: Realistic historical project logs & variance data
- [ ] Core extraction & completeness gate implementation
- [ ] Deterministic estimation engine & evidence ledger
- [ ] Actuals reconciliation & parameter calibration loop
- [ ] Production deployment & public demo link

---

## 5. Author

**Pham Nguyen Minh Tu (Thomas)**  
- GitHub: [@Thomas-DataLab](https://github.com/Thomas-DataLab)  
- LinkedIn: [in/thomas-data](https://www.linkedin.com/in/thomas-data/)  
- Portfolio: [minhtu.space](https://minhtu.space)
