"""
Database Repository for EstimateOS.
Handles persistence for projects, workstreams, actuals reconciliation, and Bayesian calibration updates.
"""
import sqlite3
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "estimateos.db"

def get_connection(db_path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def commit_actuals_reconciliation(
    project_name: str,
    client_type: str,
    transaction_type: str,
    jurisdiction: Optional[str],
    estimated_hours: float,
    actual_hours: float,
    variance_reason: str,
    retro_notes: str,
    calib_factor_prior: float,
    calib_factor_posterior: float,
    db_path: Path = DB_PATH
) -> Dict[str, Any]:
    """
    Persists reconciled project actuals into projects_historical and actuals_reconciliation,
    and updates segment calibration parameters in SQLite.
    """
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # Determine sequential ID (e.g. H15)
    cursor.execute("SELECT COUNT(*) FROM projects_historical")
    count = cursor.fetchone()[0]
    new_project_id = f"H{count + 1:02d}"

    today_str = datetime.date.today().isoformat()
    variance_h = actual_hours - estimated_hours
    k_factor = round(actual_hours / estimated_hours, 2) if estimated_hours > 0 else 1.0

    outcome_status = (
        "Delivered On-Time" if abs(variance_h) <= 5.0
        else "Delivered Overrun" if variance_h > 5.0
        else "Delivered Ahead of Schedule"
    )

    # 1. Insert into projects_historical
    cursor.execute("""
        INSERT INTO projects_historical (
            project_id, project_name, client_type, transaction_type, fund_strategy,
            jurisdiction, complexity_score, estimated_hours, actual_hours,
            delivery_date, outcome_status, scope_summary, risk_tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        new_project_id,
        project_name,
        client_type,
        transaction_type,
        "Venture / PE",
        jurisdiction or "US-DE",
        3,
        estimated_hours,
        actual_hours,
        today_str,
        outcome_status,
        f"Reconciled delivery for {project_name}. Variance reason: {variance_reason}",
        "reconciled_live"
    ))

    # 2. Insert into actuals_reconciliation
    recon_id = f"REC_{new_project_id}"
    estimate_id = f"EST_{new_project_id}"
    cursor.execute("""
        INSERT INTO actuals_reconciliation (
            reconciliation_id, estimate_id, actual_hours, variance_hours,
            calibration_factor, variance_reason, lessons_learned, reconciled_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (
        recon_id,
        estimate_id,
        actual_hours,
        variance_h,
        k_factor,
        variance_reason,
        retro_notes
    ))

    # 3. Update calibration_parameters
    segment_key = f"{transaction_type.replace(' ', '_')}:General"
    cursor.execute("""
        UPDATE calibration_parameters
        SET posterior_mean = ?, sample_size = sample_size + 1, updated_at = CURRENT_TIMESTAMP
        WHERE segment_key = ?
    """, (calib_factor_posterior, segment_key))

    conn.commit()
    conn.close()

    return {
        "project_id": new_project_id,
        "variance_hours": variance_h,
        "k_factor": k_factor,
        "posterior_mean": calib_factor_posterior
    }

def get_historical_projects(db_path: Path = DB_PATH) -> pd.DataFrame:
    """Fetches all historical projects ordered chronologically."""
    if not db_path.exists():
        return pd.DataFrame()
    conn = get_connection(db_path)
    df = pd.read_sql("SELECT * FROM projects_historical ORDER BY delivery_date ASC, project_id ASC", conn)
    conn.close()
    return df
