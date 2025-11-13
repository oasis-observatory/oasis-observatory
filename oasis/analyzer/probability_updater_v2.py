# oasis/analyzer/probability_updater_v2.py
"""
Update ASI scenario probabilities based on precursor signal links.
Implements Bayesian-like reweighting using signal confidence and scores.
"""

import math
from typing import Dict, List
from oasis.analyzer.linkage import get_links_for_dashboard
from oasis.common.db import get_scenario_conn

# Prior weight default
BASE_PROB = 0.5
MIN_PROB = 0.01
MAX_PROB = 0.99

def bayesian_update(prior: float, likelihood: float) -> float:
    """
    Bayesian update of probability given prior and likelihood ratio.
    """
    prior = max(MIN_PROB, min(MAX_PROB, prior))
    odds = prior / (1 - prior)
    updated_odds = odds * likelihood
    posterior = updated_odds / (1 + updated_odds)
    return max(MIN_PROB, min(MAX_PROB, posterior))


def update_scenario_probabilities(min_confidence: float = 0.3):
    """
    Update each scenario's probability based on precursor signal links.
    """
    links = get_links_for_dashboard()
    scenario_scores: Dict[str, float] = {}

    # Aggregate likelihood contribution from each signal
    for link in links:
        scenario_id = link["scenario_title"]
        confidence = link["confidence"]
        signal_score = link.get("score", 1.0)  # Default fallback
        likelihood = 1.0 + confidence * signal_score
        if scenario_id in scenario_scores:
            scenario_scores[scenario_id] *= likelihood
        else:
            scenario_scores[scenario_id] = likelihood

    # Normalize and update DB
    with get_scenario_conn() as conn:
        for title, combined_likelihood in scenario_scores.items():
            # Fetch current prior
            row = conn.execute(
                "SELECT id, probability FROM scenarios WHERE title=?",
                (title,)
            ).fetchone()
            if not row:
                continue

            prior = row["probability"] if row["probability"] is not None else BASE_PROB
            posterior = bayesian_update(prior, combined_likelihood)

            conn.execute(
                "UPDATE scenarios SET probability=? WHERE id=?",
                (round(posterior, 4), row["id"])
            )

        conn.commit()
    print(f"Updated probabilities for {len(scenario_scores)} scenarios")
