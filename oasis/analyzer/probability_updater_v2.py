# oasis/analyzer/probability_updater_v3.py
import math
import json
from collections import defaultdict
from oasis.common.db import get_scenario_conn

BASE_PRIOR = 0.05  # Lower uniform prior — more room to move
MIN_PROB = 0.001
MAX_PROB = 0.999

def update_scenario_probabilities():
    with get_scenario_conn() as conn:
        # 1. Get all current probabilities
        scenarios = conn.execute("SELECT id, data FROM scenarios").fetchall()
        scenario_map = {}
        for s in scenarios:
            try:
                data = json.loads(s["data"])
                prob = data.get("quantitative_assessment", {}).get("probability", {}).get("emergence_probability", BASE_PRIOR)
                scenario_map[s["id"]] = prob
            except:
                scenario_map[s["id"]] = BASE_PRIOR

        # 2. Count high-confidence supporting signals per scenario
        support_counts = defaultdict(int)
        total_weight = 0

        rows = conn.execute("""
            SELECT scenario_id, confidence 
            FROM signal_scenario_links 
            WHERE confidence >= 0.45
        """).fetchall()

        for row in rows:
            weight = row["confidence"] ** 2   # non-linear boosting of strong links
            support_counts[row["scenario_id"]] += weight
            total_weight += weight

        # 3. Simple logistic update (keeps probs bounded and normalized-ish)
        updated = {}
        for scen_id, prior in scenario_map.items():
            evidence = support_counts.get(scen_id, 0)
            # More evidence → steeper move toward 1.0
            logit = math.log(prior / (1 - prior)) + evidence
            posterior = 1 / (1 + math.exp(-logit))
            posterior = max(MIN_PROB, min(MAX_PROB, posterior))
            updated[scen_id] = round(posterior, 4)

        # 4. Write back into the nested JSON (preserves structure)
        for scen_id, new_prob in updated.items():
            row = conn.execute("SELECT data FROM scenarios WHERE id=?", (scen_id,)).fetchone()
            data = json.loads(row["data"])
            if "quantitative_assessment" not in data:
                data["quantitative_assessment"] = {}
            if "probability" not in data["quantitative_assessment"]:
                data["quantitative_assessment"]["probability"] = {}
            data["quantitative_assessment"]["probability"]["emergence_probability"] = new_prob
            data["quantitative_assessment"]["probability"]["last_update_reason"] = "signal_linkage_update"
            data["quantitative_assessment"]["probability"]["trend"] = "increasing" if new_prob > scenario_map.get(scen_id, 0.5) * 1.05 else "stable"

            conn.execute("UPDATE scenarios SET data = ? WHERE id = ?", (json.dumps(data), scen_id))

        conn.commit()
    print(f"Updated probabilities for {len(updated)} scenarios based on {len(rows)} strong links")