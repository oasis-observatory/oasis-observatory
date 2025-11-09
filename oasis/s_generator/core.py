#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 16:05:00 2025

@author: mike
"""

# oasis/s_generator/core.py
import uuid
from datetime import datetime, timezone
from typing import Dict, Any

from oasis.common.schema import SchemaManager
from oasis.logger import log

# NEW: Import the parameter sampler
from oasis.s_generator.params import sample_parameters
from oasis.s_generator.clients.ollama import generate_narrative
from oasis.s_generator.timeline import dynamic_timeline
from oasis.s_generator.consistency import NarrativeChecker
from oasis.s_generator.storage import save_scenario, init_db
from oasis.s_generator.abbreviator import abbreviate


def generate_scenario() -> Dict[str, Any] | None:
    """
    Generate one fully valid, schema-compliant ASI scenario.
    End-to-end: sample → prompt → LLM → check → validate → save.
    """
    init_db()

    # 1. Sample parameters (100% schema-safe)
    params = sample_parameters()
    log.debug("params.sampled", count=len(params))

    # 2. Generate title
    title = abbreviate(params)

    # 3. IDs & timestamps
    scenario_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    # 4. Timeline
    timeline_phases = dynamic_timeline()

    # 5. Prompt lives in ollama.py → edit there!

    # 6. Generate narrative
    success, narrative, model_used = generate_narrative(
        title=title,
        params=params,
        timeline=timeline_phases
    )
    if not success:
        log.error("llm.all_failed")
        return None

    # 7. Consistency check
    checker = NarrativeChecker(params)
    consistent, failures = checker.check(narrative)
    if not consistent:
        log.warning("consistency.failed", failures=failures)
        return None

    # 8. Build final scenario
    scenario: Dict[str, Any] = {
        "id": scenario_id,
        "title": title,
        "metadata": {
            "created": now,
            "last_updated": now,
            "version": 1,
            "source": "generated",
            "provenance": {
                "model_used": model_used or "unknown",
                "generation_parameters": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "prompt_version": "v1"
                }
            }
        },
        "origin": {
            "initial_origin": params["initial_origin"],
            "development_dynamics": params["development_dynamics"]
        },
        "architecture": {
            "type": params["architecture"],
            "deployment_topology": params["deployment_topology"]
        },
        "substrate": {
            "type": params["substrate"],
            "deployment_medium": params["deployment_medium"],
            "resilience": params["substrate_resilience"]
        },
        "oversight_structure": {
            "type": params["oversight_type"],
            "effectiveness": params["oversight_effectiveness"],
            "control_surface": params["control_surface"]
        },
        "core_capabilities": {
            "agency_level": params["agency_level"],
            "autonomy_degree": params["autonomy_degree"],
            "alignment_score": params["alignment_score"],
            "phenomenology_proxy_score": params["phenomenology_proxy_score"]
        },
        "goals_and_behavior": {
            "stated_goal": params["stated_goal"],
            "mesa_goals": params.get("mesa_goals", []),
            "opacity": params["opacity"],
            "deceptiveness": params["deceptiveness"],
            "goal_stability": params["goal_stability"]
        },
        "impact_and_control": {
            "impact_domains": params["impact_domains"],
            "deployment_strategy": params["deployment_strategy"]
        },
        "scenario_content": {
            "title": title,
            "narrative": narrative,
            "timeline": {"phases": timeline_phases}
        },
        "quantitative_assessment": {
            "probability": {
                "emergence_probability": 0.4,
                "detection_confidence": 0.5,
                "projection_confidence": 0.6,
                "trend": "stable",
                "last_update_reason": "initial generation"
            },
            "risk_assessment": {
                "existential": {"score": 5, "weight": 0.7}
            }
        },
        "observable_evidence": {
            "key_indicators": [],
            "supporting_signals": []
        }
    }

    # 9. Schema validation
    valid, err = SchemaManager.validate(scenario)
    if not valid:
        log.error("schema.validation.failed", error=err)
        return None

    # 10. Save
    save_scenario(scenario)
    log.info("scenario.generated", title=title, model=model_used, id=scenario_id[:8])

    return scenario