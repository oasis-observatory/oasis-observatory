#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 16:20:15 2025

@author: mike
"""

# params.py
# Generates random ASI scenario parameters that are 100% compatible
# with asi_scenario_schema.json
import random
from typing import Dict, Any

def sample_parameters() -> Dict[str, Any]:
    """Sample 100% schema-compliant random parameters."""
    return {
        "initial_origin": random.choice(["corporate", "open-source", "state", "rogue"]),
        "development_dynamics": random.choice(["engineered", "emergent", "hybrid"]),
        "architecture": random.choice(["monolithic", "m_generator", "modular"]),
        "deployment_topology": random.choice(["centralized", "decentralized", "edge"]),
        "substrate": random.choice(["classical", "neuromorphic", "quantum"]),
        "deployment_medium": random.choice(["cloud", "edge", "embedded"]),
        "substrate_resilience": random.choice(["robust", "adaptive"]),
        "oversight_type": random.choice(["internal", "external", "none"]),
        "oversight_effectiveness": random.choice(["effective", "partial"]),
        "control_surface": random.choice(["technical", "legal", "social"]),
        "agency_level": round(random.uniform(0.1, 1.0), 2),
        "autonomy_degree": random.choice(["partial", "full", "super"]),
        "alignment_score": round(random.uniform(0.0, 1.0), 2),
        "phenomenology_proxy_score": round(random.uniform(0.0, 1.0), 2),
        "stated_goal": random.choice(["human-welfare", "power", "survival"]),
        "mesa_goals": [],
        "opacity": round(random.uniform(0.0, 1.0), 2),
        "deceptiveness": round(random.uniform(0.0, 1.0), 2),
        "goal_stability": random.choice(["fixed", "fluid"]),
        "impact_domains": random.sample(
            ["cyber", "physical", "existential"], k=random.randint(1, 3)
        ),
        "deployment_strategy": random.choice(["stealth", "public", "gradual"])
    }