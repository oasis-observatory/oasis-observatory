# oasis/analyzer/core_analyzer.py

import json
import numpy as np
from oasis.s_generator.consistency import NarrativeChecker
from oasis.analyzer.probability_updater_v2 import update_scenario_probabilities
from oasis.analyzer.evolution_engine import update_scenario_trends


class ScenarioAnalyzer:
    """Evaluate scenario plausibility and systemic complexity."""

    def __init__(self, scenario_json: dict):
        self.data = scenario_json

    def logic_score(self) -> float:
        """Run internal narrative consistency check."""
        checker = NarrativeChecker(self.data.get("narrative", ""))
        return checker.score()

    def complexity_index(self) -> float:
        """Estimate systemic complexity based on event density & diversity."""
        events = self.data.get("timeline", [])
        if not events:
            return 0.0
        years = [e["year"] for e in events]
        diversity = len({e["category"] for e in events})
        temporal_span = max(years) - min(years)
        return np.log1p(diversity * len(events)) / (temporal_span / 10)

    def run(self):
        """Run logic and complexity analysis."""
        return {
            "logic_score": self.logic_score(),
            "complexity_index": self.complexity_index(),
        }


def run_full_analysis():
    """
    Full OASIS foresight loop:
    1. Bayesian probability update
    2. Evolutionary scenario synthesis
    """
    print("🔄 Running Bayesian probability update...")
    update_scenario_probabilities()
    print("🧬 Running evolutionary scenario synthesis...")
    update_scenario_trends()
    print("✅ Analysis loop complete.")

# Example usage:
# analyzer = ScenarioAnalyzer(scenario_json)
# results = analyzer.run()
# run_full_analysis()  # Run the full Bayesian + evolutionary loop
