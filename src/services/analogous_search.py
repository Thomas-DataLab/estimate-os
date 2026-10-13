"""
Analogous Project Matching Service for EstimateOS.
Ranks historical projects from SQLite by multidimensional similarity
and explains matching drivers.
"""
import sqlite3
from typing import List, Dict, Any
from pathlib import Path
from src.schemas.scope import ScopeIntakeSchema

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "estimateos.db"

def find_analogous_projects(scope: ScopeIntakeSchema, db_path: Path = DB_PATH, limit: int = 3) -> List[Dict[str, Any]]:
    """
    Computes explainable similarity against historical projects.
    """
    if not db_path.exists():
        return []

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT project_id, project_name, client_type, transaction_type, 
               fund_strategy, jurisdiction, complexity_score, 
               estimated_hours, actual_hours, outcome_status, scope_summary, risk_tags
        FROM projects_historical
    """)
    rows = cursor.fetchall()
    conn.close()

    scored_projects = []
    for row in rows:
        score = 0.0
        matching_dimensions = []

        # 1. Transaction Type (35%)
        row_t_type = row["transaction_type"].lower()
        target_t_type = scope.transaction_type.lower()
        if target_t_type in row_t_type or row_t_type in target_t_type:
            score += 0.35
            matching_dimensions.append(f"Same Transaction Type ({row['transaction_type']})")
        elif any(w in row_t_type for w in target_t_type.split()):
            score += 0.20
            matching_dimensions.append("Overlapping Transaction Domain")

        # 2. Client Type (15%)
        if scope.client_type.lower() == row["client_type"].lower():
            score += 0.15
            matching_dimensions.append(f"Matching Client Profile ({row['client_type']})")

        # 3. Jurisdiction (15%)
        if scope.jurisdiction and row["jurisdiction"]:
            if scope.jurisdiction.lower() == row["jurisdiction"].lower():
                score += 0.15
                matching_dimensions.append(f"Shared Jurisdiction ({row['jurisdiction']})")

        # 4. Complexity delta (20%)
        target_complexity = min(5, max(1, len(scope.workstreams)))
        comp_delta = abs(target_complexity - row["complexity_score"])
        comp_score = max(0.0, 0.20 - (comp_delta * 0.05))
        score += comp_score
        if comp_delta <= 1:
            matching_dimensions.append(f"Comparable Complexity ({row['complexity_score']}/5)")

        # 5. Risk tags overlap (15%)
        hist_tags = set(t.strip().lower() for t in row["risk_tags"].split(",") if t.strip())
        target_tags = set(r.lower() for w in scope.workstreams for r in w.risks)
        overlap = len(hist_tags.intersection(target_tags))
        if overlap > 0:
            score += min(0.15, overlap * 0.075)
            matching_dimensions.append(f"Shared Risk Factors ({overlap} tags)")

        k_factor = round(row["actual_hours"] / row["estimated_hours"], 2)

        scored_projects.append({
            "project_id": row["project_id"],
            "project_name": row["project_name"],
            "client_type": row["client_type"],
            "transaction_type": row["transaction_type"],
            "jurisdiction": row["jurisdiction"],
            "complexity_score": row["complexity_score"],
            "estimated_hours": row["estimated_hours"],
            "actual_hours": row["actual_hours"],
            "k_factor": k_factor,
            "outcome_status": row["outcome_status"],
            "similarity_score": round(score * 100.0, 1),
            "matching_dimensions": matching_dimensions
        })

    # Sort descending by similarity score
    scored_projects.sort(key=lambda x: x["similarity_score"], reverse=True)
    return scored_projects[:limit]
