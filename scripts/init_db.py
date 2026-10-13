"""
Database initialization and seeding script for EstimateOS.
Creates SQLite tables and populates baseline historical projects.
"""
import os
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "estimateos.db"
SEED_CSV = DATA_DIR / "seed_historical_projects.csv"

DDL_STATEMENTS = """
CREATE TABLE IF NOT EXISTS projects_historical (
    project_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    client_type TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    fund_strategy TEXT,
    jurisdiction TEXT,
    complexity_score INTEGER CHECK(complexity_score BETWEEN 1 AND 5),
    estimated_hours REAL NOT NULL,
    actual_hours REAL NOT NULL,
    delivery_date DATE NOT NULL,
    outcome_status TEXT NOT NULL,
    scope_summary TEXT NOT NULL,
    risk_tags TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workstream_definitions (
    workstream_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    workstream_name TEXT NOT NULL,
    workstream_type TEXT NOT NULL,
    role_mix_json TEXT NOT NULL,
    optimistic_hours REAL NOT NULL,
    most_likely_hours REAL NOT NULL,
    pessimistic_hours REAL NOT NULL,
    expected_hours REAL NOT NULL,
    actual_hours REAL,
    confidence_score REAL NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects_historical(project_id)
);

CREATE TABLE IF NOT EXISTS calibration_parameters (
    parameter_id TEXT PRIMARY KEY,
    segment_key TEXT UNIQUE NOT NULL,
    transaction_type TEXT NOT NULL,
    workstream_type TEXT NOT NULL,
    prior_mean REAL NOT NULL DEFAULT 1.00,
    prior_strength REAL NOT NULL DEFAULT 5.0,
    posterior_mean REAL NOT NULL DEFAULT 1.00,
    sample_size INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS active_estimates (
    estimate_id TEXT PRIMARY KEY,
    project_name TEXT NOT NULL,
    client_type TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    raw_brief TEXT NOT NULL,
    structured_scope_json TEXT NOT NULL,
    completeness_score REAL NOT NULL,
    estimate_status TEXT NOT NULL,
    total_pert_hours REAL NOT NULL,
    calibrated_hours REAL NOT NULL,
    confidence_band TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evidence_ledger (
    evidence_id TEXT PRIMARY KEY,
    estimate_id TEXT NOT NULL,
    workstream_name TEXT NOT NULL,
    evidence_type TEXT NOT NULL,
    statement TEXT NOT NULL,
    impact_hours REAL NOT NULL,
    confidence_score REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estimate_id) REFERENCES active_estimates(estimate_id)
);

CREATE TABLE IF NOT EXISTS actuals_reconciliation (
    reconciliation_id TEXT PRIMARY KEY,
    estimate_id TEXT NOT NULL,
    actual_hours REAL NOT NULL,
    variance_hours REAL NOT NULL,
    calibration_factor REAL NOT NULL,
    variance_reason TEXT NOT NULL,
    lessons_learned TEXT NOT NULL,
    reconciled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estimate_id) REFERENCES active_estimates(estimate_id)
);
"""

def init_db(db_path: Path = DB_PATH, seed_csv: Path = SEED_CSV) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute DDL
    cursor.executescript(DDL_STATEMENTS)
    conn.commit()
    print(f"Database schema initialized at {db_path}")

    # Seed historical projects if empty
    cursor.execute("SELECT COUNT(*) FROM projects_historical")
    count = cursor.fetchone()[0]
    if count == 0 and seed_csv.exists():
        df = pd.read_csv(seed_csv)
        df.to_sql("projects_historical", conn, if_exists="append", index=False)
        conn.commit()
        print(f"Seeded {len(df)} historical projects from {seed_csv}")
    else:
        print(f"projects_historical table already contains {count} records.")

    # Initialize default calibration parameters
    segments = [
        ("LP_Onboarding:General", "LP Onboarding", "general", 1.05, 5.0, 1.05, 4),
        ("Subscription_Flow:General", "Subscription Flow", "general", 1.10, 5.0, 1.10, 3),
        ("Legal_Workflow:General", "Legal Workflow", "general", 1.25, 5.0, 1.25, 3),
        ("Integration:General", "Integration", "general", 1.12, 5.0, 1.12, 2),
        ("Data_Migration:General", "Data Migration", "general", 1.08, 5.0, 1.08, 2),
    ]
    for seg_id, t_type, w_type, p_mean, p_str, post_mean, n in segments:
        cursor.execute("""
            INSERT OR IGNORE INTO calibration_parameters 
            (parameter_id, segment_key, transaction_type, workstream_type, prior_mean, prior_strength, posterior_mean, sample_size)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (f"CALIB_{seg_id}", seg_id, t_type, w_type, p_mean, p_str, post_mean, n))
    conn.commit()
    print("Baseline calibration parameters initialized.")
    conn.close()

if __name__ == "__main__":
    init_db()
