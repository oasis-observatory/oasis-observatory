# oasis/m_generator/v3/database.py

from oasis.m_generator.storage_m import save_multi_asi_briefing

def save_multi_asi_scenario(scenario: dict):
    """Wrapper for v3 — saves to dedicated table."""
    # Add required fields if missing
    if "quantitative_assessment" not in scenario:
        scenario["quantitative_assessment"] = {"threat_index": 0.0}
    if "metadata" not in scenario:
        scenario["metadata"] = {}

    save_multi_asi_briefing(scenario)