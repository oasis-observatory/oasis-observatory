#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 16:01:56 2025

@author: mike
"""

# oasis/s_generator/timeline.py
from datetime import datetime
from typing import List, Dict, Any

def dynamic_timeline() -> List[Dict[str, Any]]:
    """
    Generate a realistic, schema-compliant timeline.
    Deterministic for now — ideal for testing.
    Randomness will be config-driven in v0.2.
    """
    current_year = datetime.now().year

    return [
        {
            "phase": "Precursors & Foundations",
            "years": "1950-2020",
            "description": "Early AI, neural nets, internet scale."
        },
        {
            "phase": "Scaling Era",
            "years": "2021-2024",
            "description": "LLMs, agents, multi-modal, alignment crisis."
        },
        {
            "phase": "Pivot Year",
            "years": str(current_year),
            "description": "Today: possible hidden ASI or final leap."
        },
        {
            "phase": "Emergence Window",
            "years": f"{current_year + 1}-{current_year + 5}",
            "description": "High-probability takeoff zone."
        },
        {
            "phase": "Long-Term Equilibrium",
            "years": "2100+",
            "description": "Post-ASI world: utopia, dystopia, or absorption."
        },
    ]