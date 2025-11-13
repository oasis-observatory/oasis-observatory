# oasis/analyzer/evolution_engine.py
"""
Simulate scenario evolution & trends (increasing, decreasing, stable)
based on probability changes over time.
"""

from oasis.common.db import get_scenario_conn
from datetime import datetime

TREND_THRESH = 0.05  # Change in probability to count as trend

def compute_trend(current: float, previous: float) -> str:
    delta = current - previous
    if delta > TREND_THRESH:
        return "increasing"
    elif delta < -TREND_THRESH:
        return "decreasing"
    else:
        return "stable"


def update_scenario_trends():
    """
    Updates scenario trends based on last probability value.
    Stores result in 'trend' column of scenarios table.
    """
    with get_scenario_conn() as conn:
        rows = conn.execute(
            "SELECT id, probability, trend FROM scenarios"
        ).fetchall()

        for row in rows:
            current_prob = row["probability"] or 0.5
            previous_trend = row["trend"]
            previous_prob = getattr(row, "_last_prob", 0.5)  # default fallback
            trend = compute_trend(current_prob, previous_prob)

            conn.execute(
                "UPDATE scenarios SET trend=? WHERE id=?",
                (trend, row["id"])
            )

        conn.commit()
    print(f"Updated trends for {len(rows)} scenarios")
