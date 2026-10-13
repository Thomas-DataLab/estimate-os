# EstimateOS · Product Requirements Document (PRD)

**Project Name:** EstimateOS (Scope-to-Actuals Intelligence Engine)  
**Hackathon:** Agent in the Shell (Anduin Cybernetics)  
**Challenge Track:** The Estimator (Sales & Delivery)  
**Author:** Pham Nguyen Minh Tu (Thomas) — BBA + Data/Operations Builder  
**Version:** 1.0 (Draft)  
**Target Completion Date:** Sunday, October 18, 2026 (23:59 GMT+7)

---

## 1. Executive Summary & Problem Space

In modern enterprise B2B software delivery and venture operations (specifically within Anduin's domain of Private Markets, VC/PE fund setup, LP onboarding, and legal document digitization), scoping incoming client requests is fraught with systemic failures:

1. **Unstructured & Ambiguous Inputs**: Prospective funds, legal counsels, and general partners (GPs) submit vague emails, unformatted RFPs, and fragmented kickoff briefs with unstated constraints.
2. **Subjective "Gut-Feel" Estimation**: Project scoping relies on individual intuition and personal memory, varying wildly depending on which solution architect or implementation manager reviews the request.
3. **Broken Feedback Loop**: Actual delivery timesheets, ticket completion histories, and engineering logs are rarely reconciled against initial sales estimates. Consequently, organizational estimation does not improve over time, perpetuating either overbidding (lost deals) or underbidding (margin collapse and team burnout).

---

## 2. Core Value Proposition & System Mission

**EstimateOS** transforms unstructured client requests into calibrated, explainable, and continuously improving delivery commitments.

> **Architectural Invariant**:  
> *"LLM interprets ambiguity; the deterministic data system owns the numbers."*

### Key Value Pillars
- **Speed**: Ingests and decomposes complex kickoff briefs into a structured Work Breakdown Structure (WBS) within seconds.
- **Consistency**: Eliminates estimator subjectivity via standardized workstream taxonomy, baseline effort drivers, and rigorous Completeness Gates.
- **Continuous Improvement**: Ingests post-delivery actuals, analyzes root-cause variances, and automatically updates empirical calibration factors, driving down Mean Magnitude of Relative Error (MMRE).

---

## 3. Target User Personas & Use Cases

### Persona 1: Solutions Architect / Implementation Lead (Alex)
- **Role**: Scopes new customer implementations during pre-sales and kickoff.
- **Pain Point**: Spends 3–5 hours per RFP deciphering customer systems, drafting WBS manually, and fearing unstated legal/technical surprises.
- **Needs**: Instant extraction of scope, immediate alerts on missing critical facts, and reference to similar past customer onboardings.

### Persona 2: Delivery / Operations Manager (Sarah)
- **Role**: Tracks delivery health, resource allocation across squads, and project margins.
- **Pain Point**: Projects constantly slip because initial sales estimates missed edge-case complexities (e.g. customized Side Letters, custom CRM sync).
- **Needs**: Reconciliation tool to input actual delivery hours, diagnose variance drivers, and calibrate future bidding parameters.

### Persona 3: Head of Cybernetics / VP of Operations (David)
- **Role**: Executive overseeing operational scalability, automation, and delivery accuracy.
- **Pain Point**: Has zero visibility into organizational estimation error rates across teams and quarters.
- **Needs**: Macro telemetry dashboard proving that estimation error is declining systematically over time.

---

## 4. End-to-End User Journey (The 5-Stage Lifecycle)

1. **Stage 1 — Intake & Structuring**:
   - User pastes a raw customer brief (e.g., Singapore PE fund requesting LP onboarding + LPA/Side Letter extraction + Fund Admin integration).
   - System extracts structured metadata and decomposes requirements into standardized WBS workstreams.
2. **Stage 2 — Completeness Audit**:
   - The Completeness Gate audits the structured scope against domain invariants (LP volume, document complexity, integration endpoints, timeline constraints).
   - If critical information is missing, the system blocks firm commitment and outputs explicit clarification questions.
3. **Stage 3 — Explainable Estimation**:
   - System retrieves top 3 historical analogous projects from the database.
   - Computes 3-Point PERT estimates $(O, M, P)$ per workstream and applies calibrated segment multipliers.
   - Generates an Evidence Ledger detailing why every single hour was assigned.
4. **Stage 4 — Delivery & Actuals Ingestion**:
   - Post-handover, the team logs actual delivery hours per workstream alongside root-cause variance tags (e.g., "Unexpected Side Letter clause complexity").
5. **Stage 5 — Continuous Calibration & Organizational Learning**:
   - System recalculates empirical calibration factors via Bayesian updates.
   - Organizational accuracy metrics (MMRE and Pred(25)) update dynamically, proving institutional learning.

---

## 5. Acceptance Criteria & Definition of Done

- [ ] **Functional Web App**: Shipped as a responsive, polished Streamlit application with a clean, dark-themed Cybernetics aesthetic.
- [ ] **Zero Fabricated Precision**: LLM outputs structured scope and metadata; all mathematical derivations (PERT, variance, calibration) are executed deterministically.
- [ ] **Domain Credibility**: Demonstration datasets and brief templates reflect real-world Anduin transactions (VC/PE Fund Onboarding, LPA/Side Letter Digitization, Fund Admin SFTP/API Integration).
- [ ] **Complete Loop**: Demonstrates both the initial estimation phase and the post-project actuals reconciliation phase updating subsequent predictions.
- [ ] **Public Source Code**: Public GitHub repository with clean commit history, MIT License, architecture diagrams, and comprehensive README.
