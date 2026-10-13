# EstimateOS · Tools, Technologies & Engineering Skills Manifest

**Document:** Tools & Skills Specification  
**Version:** 1.0  
**Scope:** Runtime Tech Stack, AI Integrations, and Development Engineering Protocols

---

## 1. Production Runtime Stack & Tooling Ecosystem

### 1.1 AI & LLM Inference Engines
- **Primary Extraction Engine**: **Google Gemini 2.0 Flash** (`google-genai` SDK)
  - Role: Structured JSON extraction, ambiguity normalization, and completeness gap auditing.
  - Configuration: Temperature 0.1, strict `response_schema` enforcement matching Pydantic contracts.
  - Rationale: High context window, sub-second latency, zero hallucinations on structured formatting, generous free tier via Google AI Studio.
- **High-Speed Secondary / Fallback Engine**: **Groq API** (`groq` SDK with `llama-3.3-70b-versatile`)
  - Role: Ultra-low latency fallback when Google API quotas or network latency thresholds are triggered.
  - Configuration: JSON object mode enabled.
- **Offline / Mock Extractor**: Built-in deterministic mock engine for zero-token local testing and automated CI pipelines.

### 1.2 Data Persistence & Analytical Engine
- **Operational Data Store (OLTP)**: **SQLite 3** (`sqlite3` stdlib / `SQLAlchemy`)
  - Role: ACID transactions for active project scopes, workstream definitions, evidence ledgers, and audit trails.
  - Portability: Zero external server dependencies; instantly portable to Streamlit Community Cloud.
- **Analytical & Telemetry Engine (OLAP)**: **DuckDB** (`duckdb`)
  - Role: In-memory analytical queries, cohort variance aggregation, historical similarity vector/metadata scoring, and MMRE/Pred(25) trend computation.
  - Advantage: Vectorized SQL execution directly over SQLite tables or Parquet/CSV seed files.

### 1.3 Frontend & Data Visualization Framework
- **Application Framework**: **Streamlit** (v1.38+)
  - Role: Pure Python reactive web interface with 4 dedicated workflow tabs.
  - Custom Theme: Dark Cybernetics styling (`.streamlit/config.toml`), responsive wide layout.
- **Visualization Library**: **Plotly** (`plotly.graph_objects` & `plotly.express`)
  - Chart Types:
    1. Interactive PERT Horizontal Whisker Plots ($O \to M \to P$).
    2. Role Mix Stacked Allocation Charts (Analyst, Engineer, QA, PM).
    3. Longitudinal MMRE Error Convergence Line Charts.
    4. Pred(25) Compliance Bar Gauges across sequential delivery cohorts.
    5. Parity Scatter Plots with $45^\circ$ perfect-accuracy reference lines.

### 1.4 Contract Validation & Quality Suite
- **Data Contracts**: **Pydantic v2** (`BaseModel`, `Field`, `Literal`)
  - Role: Runtime validation between LLM output and the deterministic math engine.
- **Testing & Verification**: **Pytest** (v8.3+)
  - Role: Automated unit testing of PERT equations, Bayesian updates, and Completeness Gate blocking logic.

---

## 2. Development Engineering Skills & Quality Protocols

During the engineering of EstimateOS, the following structured engineering skills and protocols are enforced:

### 2.1 `test-driven-development` (TDD Protocol)
- **Principle**: RED ➔ GREEN ➔ REFACTOR.
- **Application**:
  - Write test contracts for 3-Point PERT math ($E = (O+4M+P)/6$), standard deviation ($\sigma = (P-O)/6$), and variance calculations *before* implementing `pert_engine.py`.
  - Write test assertions for Bayesian calibration adjustments ($K_{\text{posterior}}$) to verify smooth mathematical updates without divergence.
  - Write boundary tests for the Completeness Gate to ensure critical gaps strictly block firm commitments.

### 2.2 `data-engineering-pipeline` (Data Pipeline Invariants)
- **Tidy Relational Schema**: 1 Table = 1 Entity. Primary and Foreign keys strictly enforced.
- **Zero-Synthetic Hallucination**: Seed dataset (`seed_historical_projects.csv`) models authentic private capital transaction structures (LP Onboarding, LPA Extraction, Fund Admin Integration) with verifiable timestamps and variance drivers.
- **Atomic Dimensional Cleansing**: Disaggregating complex projects into discrete workstream drivers and role ratios.

### 2.3 `bi-dashboard-engineering` (Executive Telemetry)
- **Zero-Fluff KPI Architecture**: Clean executive metric cards (MMRE, Pred(25), Variance Hours, Calibration Factor).
- **Actionable Interventions**: Providing structured retrospective taxonomy for engineering variance instead of unsearchable free-text notes.

### 2.4 Multi-Agent Delegation Protocol (Gus + Pi Roster)
- **Gus (gemini-3.8-flash-high)**: System architecture, Pydantic contracts, UI design, Git lifecycle management, and prompt engineering.
- **Pi (`pi -p --model cliproxy/gemini-3.8-flash-high`)**: Primary Python developer for TDD test suites, DuckDB queries, and database seeding scripts.
