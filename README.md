# EstimateOS · Scope-to-Actuals Intelligence Engine

> Built for the **Agent in the Shell** Hackathon (Anduin Cybernetics) · Challenge: **The Estimator** (Sales & Delivery).

---

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-10B981?logo=streamlit&logoColor=white)](https://estimate-os-rbaaveipfjfeqnlstxznow.streamlit.app/)
[![Tests](https://img.shields.io/badge/Tests-11%20Passed-10B981?logo=pytest&logoColor=white)](https://pytest.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

> 🌐 **Production Live Demo URL**: [https://estimate-os-rbaaveipfjfeqnlstxznow.streamlit.app/](https://estimate-os-rbaaveipfjfeqnlstxznow.streamlit.app/)

---

## 1. Executive Summary & Problem Space

In enterprise B2B delivery and venture operations (specifically within Anduin's domain of Private Markets, VC/PE fund setup, LP onboarding, and legal document digitization), project scoping is notoriously brittle:
1. **Unstructured & Ambiguous Inputs**: Prospective funds, legal counsels, and general partners (GPs) submit vague emails, unformatted RFPs, and fragmented kickoff briefs with unstated constraints.
2. **Subjective "Gut-Feel" Estimation**: Sizing relies on individual intuition without standardized work-breakdown structures.
3. **Broken Feedback Loop**: Actual delivery timesheets and ticket completion histories are rarely reconciled against initial sales estimates. Consequently, organizational estimation does not improve over time.

**EstimateOS** bridges this gap:
- **LLM & Heuristic Scope Intake**: Ingests unstructured briefs, normalizes requirements into canonical WBS workstreams, and triggers completeness gates to flag missing critical parameters.
- **Deterministic Estimation Engine**: Computes verifiable 3-Point PERT effort ranges, confidence scores, and line-item evidence backed by historical analogous cases.
- **Continuous Calibration Loop**: Ingests actual delivery metrics post-handover, conducts variance analysis, and executes Bayesian parameter calibration approved by human operators.

> **Architectural Core**: *LLM interprets ambiguity; the deterministic data system owns the numbers.*

---

## 2. High-Level Architecture & Lifecycle

```
[ Incoming Scope ] ──────────► [ AI / Heuristic Extraction ]
(Client Email / RFP Brief)       (JSON Schema Enforcement)
                                            │
                                            ▼
                               [ Completeness Gate Audit ]
                               (Score: 0-100 · Critical Blockers · Contingency)
                                            │
               ┌────────────────────────────┴───────────────────────────┐
               ▼                                                        ▼
[ Historical Analogs Matching ]                            [ 3-Point PERT Engine ]
(SQLite / DuckDB Precedent Search)                         (O, M, P, Beta Expected, σ)
               │                                                        │
               └────────────────────────────┬───────────────────────────┘
                                            ▼
                             [ Calibrated Commitment & Evidence Ledger ]
                             (Segment Multiplier K · P80 Cap · Squad Role Mix)
                                            │
                                            ▼
                             [ Actuals Reconciliation & Variance Retro ]
                             (Timesheet Logging · Root-Cause Variance Diagnostic)
                                            │
                                            ▼
                             [ Organizational Learning & Telemetry ]
                             (Bayesian Posterior Update · MMRE Decline · Pred(25) Expansion)
```

---

## 3. Core Modules & Innovations

### 1. The Completeness Gate
- Audits unstructured scopes against domain invariants (LP volume, document complexity, integration endpoints, timeline constraints).
- Flags severity levels (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) and generates explicit inquiry questions for clients before commercial commitments are locked.

### 2. 3-Point PERT & Evidence Ledger
- Calculates Beta distribution expected hours: $E = \frac{O + 4M + P}{6}$ and uncertainty $\sigma = \frac{P - O}{6}$.
- Pairs every workstream with line-item provenance linked to historical Anduin transactions (e.g. Cayman LPA digitization, Citco SFTP sync, Investran REST API).

### 3. Bayesian Calibration Loop
- Updates segment calibration factors smoothly via conjugate Bayesian belief updates:
  $$K_{\text{posterior}} = \frac{S \cdot K_{\text{prior}} + \sum K_{\text{obs}}}{S + N}$$
- Eliminates wild estimation swings while ensuring persistent institutional memory.

### 4. Telemetry: MMRE & Pred(25)
- Tracks international software estimation benchmarks:
  - **MMRE (Mean Magnitude of Relative Error)**: Proves systematic reduction in forecast error.
  - **Pred(25)**: Demonstrates increasing proportion of projects delivered within 25% of forecast.

---

## 4. Quick Start (Run Locally)

```bash
# 1. Clone repository
git clone https://github.com/Thomas-DataLab/estimate-os.git
cd estimate-os

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize SQLite database & seed 14 historical projects
python scripts/init_db.py

# 4. Run automated test suite (11 unit tests)
pytest tests/ -v

# 5. Launch EstimateOS Streamlit web application
streamlit run app.py
```

App will run locally at `http://localhost:8501`.

---

## 5. Repository Structure

```
estimate-os/
├── .streamlit/
│   └── config.toml             # Dark Cybernetics UI theme
├── data/
│   ├── estimateos.db           # SQLite database
│   └── seed_historical_projects.csv # 14 seeded Anduin historical cases
├── docs/
│   ├── 01_PRODUCT_REQUIREMENTS_DOCUMENT.md
│   ├── 02_SYSTEM_ARCHITECTURE.md
│   ├── 03_BACKEND_SPECIFICATION.md
│   ├── 04_FRONTEND_UIUX_SPECIFICATION.md
│   ├── 05_IMPLEMENTATION_ROADMAP_AND_MILESTONES.md
│   └── 06_TOOLS_AND_SKILLS_MANIFEST.md
├── scripts/
│   └── init_db.py              # DDL schema & seed loader
├── src/
│   ├── schemas/
│   │   └── scope.py            # Pydantic contracts
│   ├── services/
│   │   ├── pert_engine.py      # Core math (PERT, Bayesian, MMRE)
│   │   ├── completeness_gate.py# Deterministic risk auditor
│   │   ├── analogous_search.py # Precedent similarity ranker
│   │   ├── llm_extractor.py    # Gemini REST + Offline Heuristics
│   │   └── mock_data.py        # Domain preset scenarios
│   └── repositories/
│       └── db_repository.py    # SQLite persistence
├── tests/
│   ├── test_pert_engine.py
│   ├── test_completeness_gate.py
│   └── test_extractor.py
├── app.py                      # 4-Tab Streamlit Web Application
├── requirements.txt
└── README.md
```

---

## 6. Author

**Pham Nguyen Minh Tu (Thomas)**  
- GitHub: [@Thomas-DataLab](https://github.com/Thomas-DataLab)  
- LinkedIn: [in/thomas-data](https://www.linkedin.com/in/thomas-data/)  
- Portfolio: [minhtu.space](https://minhtu.space)
