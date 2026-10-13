# EstimateOS · Implementation Roadmap, Milestones & Demo Playbook

**Timeline:** Tuesday, Oct 13, 2026 — Sunday, Oct 18, 2026 (23:59 GMT+7)  
**Final Submission Deliverable:** 01 Live Streamlit App URL + 01 Public GitHub Repo  
**Event:** Agent in the Shell (Anduin Cybernetics) · Demo Day at Sala Office (Oct 22)

---

## 1. 5-Day Sprint Breakdown

### Day 1 (Tuesday, Oct 13) — Architecture, Repo Linking & Data Foundations
- [x] Select challenge track on portal: **The Estimator** (Sales & Delivery).
- [x] Initialize public GitHub repository: `Thomas-DataLab/estimate-os`.
- [x] Link repository URL into Anduin Portal (4/5 checklist items verified).
- [x] Author comprehensive architecture specifications (PRD, System Arch, Backend, Frontend, Roadmap).
- [ ] Scaffold folder structure (`src/`, `data/`, `tests/`, `scripts/`).
- [ ] Implement SQLite schema initialization script (`scripts/init_db.py`).
- [ ] Seed 14 realistic Anduin-like historical projects (`data/seed_historical_projects.csv`).
- [ ] Write unit tests for core math: PERT calculations, variance, MMRE, and Pred(25).

### Day 2 (Wednesday, Oct 14) — Data Layer, Schema Validation & Completeness Gate
- [ ] Build database repository layer (`src/repositories/`).
- [ ] Define complete Pydantic models for Scope Intake and WBS items.
- [ ] Implement deterministic Completeness Gate with structured gap taxonomy.
- [ ] Build Analogous Search matching algorithm (weighted metadata similarity).
- [ ] Unit tests for Completeness Gate (verifying critical blocking vs provisional states).

### Day 3 (Thursday, Oct 15) — LLM Extraction Adapter & Tab 1 / Tab 2 UI
- [ ] Integrate Google Gemini API / Groq client with structured JSON output enforcement.
- [ ] Implement fallback parser and mock extractor for resilient zero-token testing.
- [ ] Build Streamlit layout shell with dark Cybernetics styling (`.streamlit/config.toml`).
- [ ] Implement **Tab 1: Scope Intake & Completeness Audit** (with pre-loaded demo briefs).
- [ ] Implement **Tab 2: Interactive Estimate & Evidence Ledger** (Plotly PERT whiskers & analog cards).

### Day 4 (Friday, Oct 16) — Learning Loop (Actuals & Bayesian Calibration) & Tab 3 / Tab 4 UI
- [ ] Implement Actuals Reconciliation service and database updates.
- [ ] Implement Bayesian Calibration update engine ($K_{\text{posterior}}$ calculation).
- [ ] Implement Telemetry computation (MMRE and Pred(25) cohort metrics).
- [ ] Implement **Tab 3: Actuals Reconciliation** (timesheet inputs and variance classification).
- [ ] Implement **Tab 4: Accuracy Telemetry Dashboard** (convergence charts, parity scatter plots).

### Day 5 (Saturday, Oct 17 – Sunday, Oct 18) — Cloud Deployment, Hardening & Submission
- [ ] Deploy web application to **Streamlit Community Cloud** (configured with secrets).
- [ ] Perform end-to-end user journey smoke tests across all 3 demo scenarios.
- [ ] Finalize repository documentation (`README.md`, badges, architecture diagrams, user guide).
- [ ] Record 2-minute backup demo video / GIF walkthrough for submission card.
- [ ] Submit official live app link and public repository before **Sunday, Oct 18 at 23:59 GMT+7**.

---

## 2. Testing & Quality Assurance Gates

All algorithmic contracts must be rigorously verified using `pytest`:

```bash
# Run automated verification suite
pytest tests/ -v
```

### Essential Test Cases
1. **`test_pert_calculations`**:
   - Asserts $E = (O + 4M + P)/6$ and $\sigma = (P - O)/6$.
   - Validates mathematical exception when $O > M$ or $M > P$.
2. **`test_completeness_gate_blocking`**:
   - Asserts missing `estimated_investor_count` flags `CRITICAL` and sets `status="BLOCKED_CRITICAL"`.
   - Asserts full input sets `status="READY_FOR_COMMITMENT"`.
3. **`test_bayesian_calibration_update`**:
   - Asserts that an overrun ($A/E = 1.40$) smoothly increases posterior calibration factor without wild swings.
4. **`test_mmre_and_pred25_metrics`**:
   - Validates mathematical correctness of cohort MMRE and Pred(25) against known benchmark tables.

---

## 3. Streamlit Cloud Deployment Architecture

1. **Repository Structure**:
   - Root `app.py` acts as the primary entry point.
   - `requirements.txt` specifies lightweight dependencies (`streamlit`, `pydantic`, `pandas`, `plotly`, `google-genai`).
2. **Secrets Management**:
   - `GEMINI_API_KEY` or `GROQ_API_KEY` configured securely via Streamlit Cloud Secrets dashboard:
     ```toml
     # .streamlit/secrets.toml (Local development only, git-ignored)
     GEMINI_API_KEY = "AIzaSy..."
     ```
3. **Database Portability**:
   - SQLite database initializes automatically on first boot if not present, seeding historical records seamlessly.

---

## 4. Judges Demo Presentation Script (Sala Demo Day, Oct 22)

### Hook (0:00 – 0:30): The Unspoken Pain of Scope Sizing
*"Good afternoon Anduin team. In private capital transactions, every new fund client arrives with messy, ambiguous expectations. Today, when an RFP arrives, someone spends hours reading it, guesses a number by gut feel, and nobody ever checks if that estimate was right 3 months later. When we underbid, our engineering and operations teams drown. When we overbid, we lose the fund."*

### The Solution (0:30 – 1:15): EstimateOS & Completeness Gate
*"EstimateOS turns that ambiguity into a learning engine. Watch this: I paste a real kickoff email from a Singapore PE fund. In 2 seconds, EstimateOS extracts the Work Breakdown Structure. But notice what happens here: The Completeness Gate flashes an alert. The client didn't specify their investor volume or fund admin API. Instead of guessing, EstimateOS flags a +24h provisional contingency and drafts exact questions for the client."*

### The Differentiation (1:15 – 2:00): Evidence Ledger & The Closed Feedback Loop
*"Here in the Estimate Ledger, every hour has a receipt: we match 3 past Anduin onboarding projects. Notice this 1.12x calibration factor. Where did it come from? It came from Tab 3. When Project H02 finished last month, we logged the actual timesheets. The system noticed we consistently underestimate custom Side Letter extraction by 22%, so it automatically updated our institutional memory."*

### Close (2:00 – 2:30): The Institutional Learning Curve
*"Looking at Tab 4: Over the last 15 projects, our Mean Relative Error dropped from 41% to 16%, and our Pred(25) hit 80%. EstimateOS does not make false promises of magic precision. It turns messy client briefs into explicit assumptions, estimates into traceable evidence, and completed work into a smarter company. Thank you."*
