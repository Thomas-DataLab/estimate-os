# EstimateOS · Frontend UI/UX Specification

**Component:** Streamlit Application Interface, Visual Language, & Interactive States  
**Version:** 1.0  
**Design Paradigm:** Anduin Cybernetics Terminal (Dark Slate, Acid Green & Cyan Accents, Monospace Typography)

---

## 1. Visual Design System & Theme Directives

EstimateOS adopts a high-density, professional terminal aesthetic aligned with Anduin Cybernetics:

- **Background**: `#0F172A` (Deep Slate Navy) / Card Background `#1E293B`
- **Text**: `#F8FAFC` (Off-white) / Muted Labels `#94A3B8`
- **Primary Brand Accent**: `#10B981` (Cyber Emerald / Verified)
- **Warning / Uncalibrated Accent**: `#F59E0B` (Amber Warning)
- **Critical Blocker Accent**: `#EF4444` (Crimson Alert)
- **Informational / Analog Accent**: `#06B6D4` (Cyan Data Engine)
- **Typography**: Clean system sans-serif for UI labels, coupled with `Fira Code` / Monospace for numbers, estimates, and code snippets.

---

## 2. Global Navigation & Application Shell

### Top Navigation Bar (Header)
```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [LOGO] EstimateOS · Scope-to-Actuals Intelligence Engine    [Anduin Cybernetics Alpha] │
│ Sub-header: Deterministic Estimation & Empirical Bayesian Calibration for Private Markets  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 4-Tab Core Layout
1. **`[1] Scope Intake & Audit`**: Raw text input, LLM extraction, and Completeness Gate inspection.
2. **`[2] Estimate & Evidence Ledger`**: 3-Point PERT breakdown, role allocations, and analog evidence.
3. **`[3] Actuals Reconciliation`**: Post-delivery timesheet logging and root-cause variance analysis.
4. **`[4] Accuracy Telemetry (BI)`**: Longitudinal performance charts showing MMRE decline and Pred(25) expansion.

---

## 3. Tab-by-Tab Screen Specifications

### Tab 1 — Scope Intake & Completeness Audit

#### 1. Input Controls
- **Template Selector Dropdown**: Quick-load realistic sample briefs:
  1. *Singapore PE Fund (SingaVCC) — Full LP Onboarding & Custom LPA Review*
  2. *Delaware VC Fund V — Rapid Subscription Flow with Investran API*
  3. *Incomplete Client RFP (Ambiguous Volumes & Unspecified Integrations)*
- **Text Area**: Large multi-line editor for raw client emails or RFP snippets.
- **Action Button**: `[Deconstruct Scope & Audit Gate ➔]` (Triggers LLM structured extraction).

#### 2. Display Components (Post-Extraction)
- **Project Metadata Card**: Clean 4-column KPI cards displaying detected Client Type, Transaction Type, Jurisdiction, and Estimated Investor Count.
- **Completeness Health Banner**:
  - Score badge: e.g., `85 / 100`
  - Status indicator:
    - `CRITICAL BLOCKER`: Red banner. Blocks commitment estimate until mandatory fields are supplied.
    - `PROVISIONAL PERMITTED`: Amber banner. Displays estimate tagged with provisional uncertainty buffer.
    - `AUDIT PASSED`: Green banner. Ready for firm commercial commitment.
- **Actionable Gap Inquiries**: Expandable table listing each missing field, why it matters, and a copyable inquiry string to send back to the client.
- **Interactive WBS Table**: Editable table displaying extracted workstreams, assumptions, risks, and preliminary $O / M / P$ hours.

---

### Tab 2 — Interactive Estimate & Evidence Ledger

#### 1. Top-Level Commitment Summary
- **Primary Metric Cards**:
  - `Raw PERT Expected`: e.g. **142.5 hrs**
  - `Calibration Multiplier`: e.g. **1.12x** (Based on 14 historic projects in segment)
  - `Calibrated Commitment`: e.g. **159.6 hrs** (Firm Bidding Target)
  - `Risk Buffer (P80)`: e.g. **+18.4 hrs** ($\sigma = 11.2$)
- **Role Mix Allocation (Bar Chart / Cards)**:
  - Solutions Analyst: 38 hrs (24%)
  - Integration Engineer: 67 hrs (42%)
  - QA Engineer: 29 hrs (18%)
  - Engagement Manager: 25 hrs (16%)

#### 2. Visual Workstream Uncertainty (Plotly Chart)
- **Horizontal PERT Whisker Plot**:
  - Point marker at Most Likely ($M$).
  - Whiskers extending from Optimistic ($O$) to Pessimistic ($P$).
  - Vertical diamond marker for Calibrated Expected Hours ($E_{\text{calibrated}}$).

#### 3. Top 3 Analogous Past Projects
- Interactive cards showing matched projects from the database:
  - Similarity score badge (e.g. `92% Match`).
  - Key matching dimensions: *Same Jurisdiction (SG)*, *Identical Fund Admin (Allvue)*, *Complex Side Letters*.
  - Historical Planned vs Actual hours and resulting $K$-Factor.

#### 4. The Evidence Ledger (Provenance Table)
- Detailed line-item justification:
  | Workstream | Factor / Driver | Source Basis | Effort Impact | Provenance Confidence |
  |:---|:---|:---|:---:|:---:|
  | Document Extraction | 14 Custom Side Letters | Client Kickoff Email | +28.0h | High (Explicit) |
  | Integration Sync | Unverified Legacy SFTP | Inferred from Tech Stack | +16.0h (Buffer) | Medium (Assumption) |
  | LP Verification | Historical SG VCC Variance | Analog H02 ($K=1.22$) | +8.5h (Calibration) | High (Data Ground-Truth) |

---

### Tab 3 — Actuals Reconciliation & Variance Diagnostic

#### 1. Project Selector & Timesheet Input
- Select active in-flight estimate to reconcile.
- Workstream-by-workstream input fields for **Actual Logged Hours**.

#### 2. Automated Variance Diagnostic
- Metric Card: `Variance Hours` ($A - E$) and `Variance Percentage`.
- `Observed Project K-Factor` ($A / E$).
- **Variance Driver Taxonomy Dropdown**:
  - `Scope Expansion / Unstated Client Needs`
  - `Undiscovered Legal / Document Complexity`
  - `Third-Party API Instability / Delay`
  - `Data Cleansing & Formatting Friction`
  - `Client Decision Bottleneck`
  - `Flawless Execution / High Efficiency`
- **Root-Cause Retro Notes**: Text area for engineering lessons learned.
- **Submission Action**: `[Commit Actuals to Organizational Memory ➔]`.
  - Automatically updates database.
  - Recalculates segment Bayesian calibration factors.

---

### Tab 4 — Accuracy Telemetry & Organizational Learning

#### 1. Macro Health Scorecard
- `Total Historical Reconciliations`: **15 Projects**
- `Pre-Calibration MMRE`: **41.2%** ➔ `Post-Calibration MMRE`: **16.8%** (-59% Error Reduction)
- `Pre-Calibration Pred(25)`: **38.5%** ➔ `Post-Calibration Pred(25)`: **80.0%** (+108% Precision Gain)

#### 2. Interactive Analytical Charts (Plotly)
1. **MMRE Cohort Convergence Curve**: Line chart tracking average relative error across sequential project delivery batches (showing steady downward trend).
2. **Pred(25) Target Achievement**: Bar chart showing percentage of projects delivered within 25% of forecast across consecutive quarters.
3. **Estimate vs. Actual Scatter Plot**: 45-degree parity line showing early uncalibrated projects scattered far above the line, and recent calibrated projects hugging the target line tightly.
4. **Variance Root-Cause Pareto Chart**: Horizontal bar chart identifying top drivers of estimation overruns across all historical projects.
