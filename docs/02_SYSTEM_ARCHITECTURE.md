# EstimateOS · System Architecture & Mathematical Foundations

**Component:** System Architecture, Data Modeling, & Mathematical Core  
**Version:** 1.0  
**Domain Alignment:** Anduin Transactions / Private Capital Operations

---

## 1. Architectural Philosophy & Principles

EstimateOS adheres to three foundational engineering principles:

1. **Separation of Cognitive Extraction and Quantitative Computation**:  
   LLMs excel at extracting semantics, recognizing intent, and normalizing unstructured text into structured representations. However, LLMs fail at arithmetic, variance aggregation, and calibration persistence. Therefore:
   - *LLM Domain*: Unstructured text → Validated Pydantic Schema + Completeness Gap Detection.
   - *Deterministic Domain*: Historical Analogs Search, PERT Math, Role Mix Calculation, Variance Analysis, and Calibration Updates.

2. **Full Provenance & Traceability (The Evidence Ledger)**:  
   Every hour presented in a final estimate must be traceable to either:
   - An explicit client requirement from the source text.
   - A documented business assumption.
   - A historical analog with verified actuals.
   - A mathematically derived contingency buffer.

3. **Closed-Loop Organizational Feedback**:  
   Estimates without actuals are open-loop guesses. EstimateOS closes the loop by turning completed projects into calibration training observations.

---

## 2. High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             CLIENT LAYER (UI)                               │
│                Streamlit Web Application (Dark Cybernetics Theme)            │
│  [Tab 1: Scope Intake] [Tab 2: Estimate Ledger] [Tab 3: Actuals] [Tab 4: BI]│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          APPLICATION & SERVICE LAYER                        │
│                                                                             │
│   ┌────────────────────────┐                   ┌────────────────────────┐   │
│   │   LLM Scope Extractor  │ ◄─ Prompt Hash ── │   Pydantic Validation  │   │
│   │ (Gemini Flash / Groq)  │                   │    Schema Enforcement  │   │
│   └───────────┬────────────┘                   └────────────────────────┘   │
│               │                                                             │
│               ▼                                                             │
│   ┌────────────────────────┐                   ┌────────────────────────┐   │
│   │   Completeness Gate    │ ── Flags/Gaps ──► │  Interactive Risk Gate │   │
│   │  (Deterministic Rules) │                   │ (Provisional vs Firm)  │   │
│   └───────────┬────────────┘                   └────────────────────────┘   │
│               │                                                             │
│               ▼                                                             │
│   ┌────────────────────────┐                   ┌────────────────────────┐   │
│   │ 3-Point PERT Engine    │                   │ Analogous Search Match │   │
│   │ (O, M, P, Expected, σ) │                   │  (Metadata Similarity) │   │
│   └───────────┬────────────┘                   └───────────┬────────────┘   │
│               │                                            │                │
│               └──────────────────────┬─────────────────────┘                │
│                                      ▼                                      │
│                        ┌───────────────────────────┐                        │
│                        │    Calibrated Estimate    │                        │
│                        │    & Evidence Ledger      │                        │
│                        └─────────────┬─────────────┘                        │
│                                      │                                      │
│                                      ▼                                      │
│                        ┌───────────────────────────┐                        │
│                        │ Actuals & Calibration     │                        │
│                        │ (Bayesian Update Loop)    │                        │
│                        └─────────────┬─────────────┘                        │
└──────────────────────────────────────┼──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PERSISTENCE LAYER (DATA)                          │
│               SQLite (Operational) / DuckDB (Analytical Engine)             │
│  [projects_historical] [workstream_definitions] [calibration_parameters]    │
│  [active_estimates]    [evidence_ledger]       [actuals_reconciliation]     │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Mathematical Model & Statistical Foundations

### 3.1 3-Point PERT Workstream Estimation
For each workstream $i \in \{1, \dots, n\}$, the three-point estimates are defined as:
- $O_i$: Optimistic effort (all assumptions hold, zero exceptions).
- $M_i$: Most likely effort (standard execution based on baseline drivers).
- $P_i$: Pessimistic effort (unexpected edge cases, API ambiguities, revisions).

The **Expected Effort ($E_i$)** is calculated via the beta-distribution approximation:
$$E_i = \frac{O_i + 4M_i + P_i}{6}$$

The **Standard Deviation ($\sigma_i$)** and **Variance ($\sigma_i^2$)** quantify uncertainty:
$$\sigma_i = \frac{P_i - O_i}{6}$$
$$\text{Var}_i = \sigma_i^2 = \left(\frac{P_i - O_i}{6}\right)^2$$

### 3.2 Project-Level Aggregation & Confidence Bands
Assuming workstream independence, the total project expected effort $E_{\text{project}}$ and aggregate standard deviation $\sigma_{\text{project}}$ are:
$$E_{\text{project}} = \sum_{i=1}^n E_i$$
$$\sigma_{\text{project}} = \sqrt{\sum_{i=1}^n \sigma_i^2}$$

Confidence Intervals for client commitments:
- **P50 (Median Commitment)**: $\approx E_{\text{project}}$
- **P80 (Risk-Managed Commitment)**: $E_{\text{project}} + 0.84 \cdot \sigma_{\text{project}}$
- **P95 (Worst-Case Cap)**: $E_{\text{project}} + 1.645 \cdot \sigma_{\text{project}}$

### 3.3 Calibration Factor & Segment Multipliers
Historical actual delivery hours ($A$) rarely match initial estimates ($E$). The empirical **Calibration Factor ($K$)** is defined as:
$$K = \frac{A}{E}$$
- If $K > 1.0$: Workstream is systematically under-estimated (optimism bias).
- If $K < 1.0$: Workstream is systematically over-estimated (padding).

The **Calibrated Commitment Effort ($E_{\text{calibrated}}$)** is:
$$E_{\text{calibrated}} = E_i \times K_{\text{segment}}$$

### 3.4 Empirical Bayesian Calibration Update
As new completed projects with verified actuals are reconciled, the segment calibration factor is updated without erratic fluctuations using a conjugate Bayesian belief update:
$$K_{\text{posterior}} = \frac{S \times K_{\text{prior}} + \sum_{j=1}^m K_j}{S + m}$$
Where:
- $K_{\text{prior}}$: The historical baseline calibration factor for that segment (default $1.00$).
- $S$: The prior strength (pseudo-observation weight, set to $5.0$).
- $m$: The number of newly observed reconciled projects in that segment.
- $K_j$: The observed variance factor of project $j$ ($A_j / E_j$).

### 3.5 Organizational Learning Telemetry: MMRE & Pred(25)
To evaluate whether the organization is becoming more accurate over time, two international benchmark metrics are tracked across delivery cohorts:

1. **Mean Magnitude of Relative Error (MMRE)**:
   $$\text{MRE}_k = \frac{|A_k - E_k|}{A_k}$$
   $$\text{MMRE} = \frac{1}{N} \sum_{k=1}^N \text{MRE}_k$$
   *Target*: Reduce MMRE from $>40\%$ down to $<18\%$.

2. **Prediction Level within 25% (Pred(25))**:
   $$\text{Pred}(25) = \frac{\#\{k \mid \text{MRE}_k \le 0.25\}}{N} \times 100\%$$
   *Target*: Increase Pred(25) from $35\%$ to $>75\%$.

---

## 4. Relational Database Schema (DDL)

```sql
-- 1. Historical Projects Repository
CREATE TABLE IF NOT EXISTS projects_historical (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    client_type TEXT NOT NULL,          -- 'VC', 'PE', 'Fund Admin', 'Law Firm'
    transaction_type TEXT NOT NULL,     -- 'LP Onboarding', 'LPA Digitization', 'Integration'
    fund_strategy TEXT,                 -- 'Venture', 'Buyout', 'Real Estate', 'Credit'
    jurisdiction TEXT,                  -- 'US-DE', 'SG', 'Cayman', 'LUX', 'UK'
    complexity_score INTEGER CHECK(complexity_score BETWEEN 1 AND 5),
    estimated_hours REAL NOT NULL,
    actual_hours REAL NOT NULL,
    delivery_date DATE NOT NULL,
    outcome_status TEXT NOT NULL,       -- 'Delivered On-Time', 'Delayed Scope Creep', etc.
    scope_summary TEXT NOT NULL,
    risk_tags TEXT NOT NULL,            -- Comma-separated or JSON tags
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Standardized Workstream Definitions & Task Baselines
CREATE TABLE IF NOT EXISTS workstream_definitions (
    workstream_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    workstream_name TEXT NOT NULL,
    workstream_type TEXT NOT NULL,      -- 'discovery', 'ocr_extraction', 'rules_config', 'integration', 'qa', 'pm'
    role_mix_json TEXT NOT NULL,        -- {"analyst": 0.4, "engineer": 0.4, "qa": 0.1, "pm": 0.1}
    optimistic_hours REAL NOT NULL,
    most_likely_hours REAL NOT NULL,
    pessimistic_hours REAL NOT NULL,
    expected_hours REAL NOT NULL,
    actual_hours REAL,
    confidence_score REAL NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects_historical(project_id)
);

-- 3. Segment Calibration Parameters Ledger
CREATE TABLE IF NOT EXISTS calibration_parameters (
    parameter_id TEXT PRIMARY KEY,
    segment_key TEXT UNIQUE NOT NULL,   -- e.g., 'LP_Onboarding:US-DE:Medium'
    transaction_type TEXT NOT NULL,
    workstream_type TEXT NOT NULL,
    prior_mean REAL NOT NULL DEFAULT 1.00,
    prior_strength REAL NOT NULL DEFAULT 5.0,
    posterior_mean REAL NOT NULL DEFAULT 1.00,
    sample_size INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Active In-Flight Estimates
CREATE TABLE IF NOT EXISTS active_estimates (
    estimate_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    client_type TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    raw_brief TEXT NOT NULL,
    structured_scope_json TEXT NOT NULL,
    completeness_score REAL NOT NULL,
    estimate_status TEXT NOT NULL,      -- 'Draft', 'Provisional', 'Approved', 'Delivered'
    total_pert_hours REAL NOT NULL,
    calibrated_hours REAL NOT NULL,
    confidence_band TEXT NOT NULL,      -- 'Low', 'Medium', 'High'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Evidence Ledger (Line-Item Provenance)
CREATE TABLE IF NOT EXISTS evidence_ledger (
    evidence_id TEXT PRIMARY KEY,
    estimate_id TEXT NOT NULL,
    workstream_name TEXT NOT NULL,
    evidence_type TEXT NOT NULL,        -- 'Client Brief Explicit', 'Missing Input Assumption', 'Analog Match'
    statement TEXT NOT NULL,
    impact_hours REAL NOT NULL,
    confidence_score REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estimate_id) REFERENCES active_estimates(estimate_id)
);

-- 6. Actuals Reconciliation & Variance Records
CREATE TABLE IF NOT EXISTS actuals_reconciliation (
    reconciliation_id TEXT PRIMARY KEY,
    estimate_id TEXT NOT NULL,
    actual_hours REAL NOT NULL,
    variance_hours REAL NOT NULL,
    calibration_factor REAL NOT NULL,
    variance_reason TEXT NOT NULL,      -- Structured taxonomy
    lessons_learned TEXT NOT NULL,
    reconciled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estimate_id) REFERENCES active_estimates(estimate_id)
);
```
