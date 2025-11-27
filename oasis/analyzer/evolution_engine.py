# oasis/analyzer/evolution_engine.py
"""
Simulate scenario evolution & trends (increasing, decreasing, stable)
based on probability changes over time.
"""


# oasis/analyzer/evolution_engine.py   ← FIXED & SIMPLIFIED
from oasis.analyzer.probability_updater import update_scenario_probabilities
import json
from oasis.common.db import get_scenario_conn

TREND_THRESH = 0.05  # Change in probability to count as trend

def compute_trend(current: float, previous: float) -> str:
    delta = current - previous
    if delta > TREND_THRESH:
        return "increasing"
    elif delta < -TREND_THRESH:
        return "decreasing"
    else:
        return "stable"


# In evolution_engine.py — replace the broken version
def update_scenario_trends():
    with get_scenario_conn() as conn:
        rows = conn.execute("SELECT id, data FROM scenarios").fetchall()
        for row in rows:
            try:
                data = json.loads(row["data"])
                prob = data["quantitative_assessment"]["probability"]["emergence_probability"]
                old_prob = data.get("_previous_probability", prob)
                delta = prob - old_prob
                trend = "increasing" if delta > 0.02 else "decreasing" if delta < -0.02 else "stable"

                data["quantitative_assessment"]["probability"]["trend"] = trend
                data["_previous_probability"] = prob  # store for next run
                conn.execute("UPDATE scenarios SET data = ? WHERE id = ?", (json.dumps(data), row["id"]))
            except:
                pass
        conn.commit()
    print(f"Updated trends for {len(rows)} scenarios")


def run_full_analysis_cycle():
    """One-click full foresight loop."""
    print("OASIS Full Analysis Cycle")
    update_scenario_probabilities()
    print("Cycle complete.")