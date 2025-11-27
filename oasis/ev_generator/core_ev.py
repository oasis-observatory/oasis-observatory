# oasis/ev_generator/core_ev.py

import uuid
import json
from collections import defaultdict
from oasis.common.storage import save_scenario, init_db
from oasis.logger import log
from oasis.common.llm_client import generate_narrative  # your wrapper

# Import precursor DB connection
from oasis.tracker.database_t import get_connection as get_precursor_conn

# -----------------------------
# Fetch precursors
# -----------------------------
def fetch_precursor_signals(limit=5):
    """
    Fetch the top-rated precursor signals from precursor_signals.db
    """
    signals = []
    with get_precursor_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT raw_data, score, tags
            FROM precursor_signals
            ORDER BY score DESC, collected_at DESC
            LIMIT ?
        """, (limit,))
        rows = cur.fetchall()

        for row in rows:
            try:
                data = json.loads(row["raw_data"]) if row["raw_data"] else {}
            except json.JSONDecodeError:
                data = {}
            signals.append({
                "title": data.get("title", ""),
                "description": data.get("description", ""),
                "tags": json.loads(row["tags"]) if row["tags"] else [],
                "score": row["score"] or 1.0
            })

    return signals

# -----------------------------
# Weighted precursor influence
# -----------------------------
def precursor_to_parameters(precursors):
    """
    Convert precursors into scenario parameters using weighted influence.
    Each precursor's score determines its influence.
    """
    default_params = {
        "initial_origin": "open-source",
        "development_dynamics": "emergent",
        "architecture": "hybrid",
        "deployment_topology": "centralized",
        "substrate": "classical",
        "deployment_medium": "embedded",
        "substrate_resilience": "robust",
        "oversight_type": "external",
        "oversight_effectiveness": "partial",
        "control_surface": "technical",
        "autonomy_degree": "medium",
        "alignment_score": "medium",
    }

    weighted_votes = defaultdict(lambda: defaultdict(float))

    for p in precursors:
        score = p.get("score", 1.0)
        tags = p.get("tags") or []
        description = (p.get("description") or "").lower()

        if "asi_direct" in tags:
            weighted_votes["autonomy_degree"]["high"] += score
        if "misalignment" in tags:
            weighted_votes["alignment_score"]["low"] += score
        if "edge" in description:
            weighted_votes["deployment_topology"]["edge"] += score
        if "quantum" in description:
            weighted_votes["substrate"]["quantum"] += score
        if "state" in description:
            weighted_votes["initial_origin"]["state"] += score
        if "corporate" in description:
            weighted_votes["initial_origin"]["corporate"] += score

    final_params = default_params.copy()
    for key, votes in weighted_votes.items():
        if votes:
            chosen_value = max(votes.items(), key=lambda x: x[1])[0]
            final_params[key] = chosen_value

    return final_params

# -----------------------------
# Generate a full EV scenario
# -----------------------------
def generate_ev_scenario():
    init_db()

    # 1️⃣ Get precursor signals
    signals = fetch_precursor_signals()

    # 2️⃣ Generate parameters influenced by precursors
    params = precursor_to_parameters(signals)

    # 3️⃣ Generate a unique scenario ID and title
    scenario_id = str(uuid.uuid4())
    title = f"EV-{scenario_id[:8]}"

    # 4️⃣ Generate timeline placeholder
    timeline = [{"phase": "Initial", "years": "2025+", "description": "EV scenario"}]

    # 5️⃣ Generate narrative using LLM
    success, narrative, model_used = generate_narrative(title=title, params=params, timeline=timeline)
    if not success:
        narrative = "LLM narrative generation failed."

    # 6️⃣ Save full scenario
    save_scenario(
        table_name="ev_scenarios",
        params=params,
        narrative=narrative,
        timeline=timeline,
        model_used=model_used,
        signals=signals
    )

    scenario = {
        "id": scenario_id,
        "title": title,
        "params": params,
        "timeline": timeline,
        "narrative": narrative,
        "signals": signals,
        "model_used": model_used,
    }

    log.info("ev_scenario.generated", title=title, id=scenario_id)
    return scenario
