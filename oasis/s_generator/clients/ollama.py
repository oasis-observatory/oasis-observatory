#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 16:01:56 2025

@author: mike
"""

# oasis/s_generator/clients/ollama.py
import subprocess
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)

AVAILABLE_MODELS = [
    ("llama3:8b", 300),
    ("gemma2:9b", 300),
    ("mistral:7b", 300),
    ("phi3:medium", 300),
]

SYSTEM_PROMPT = """
You a strategic foresight analyst researching Artificial Superintelligence futures.
Write a 350-word speculative scenario in third-person, formal, analytical tone.

Structure:
1. Origin & Development
2. Architecture & Deployment
3. Emergence & Autonomy
4. Risks & Outcome

CRITICAL: You MUST follow this timeline:
{timeline}
Parameters:
{params}
""".strip()

USER_PROMPT = "Title: {title}\nWrite the scenario now."

def generate(prompt: str, model: str, timeout: int) -> Tuple[bool, str, str]:
    try:
        proc = subprocess.Popen(
            ["ollama", "run", model],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(prompt, timeout=timeout)
        if proc.returncode == 0 and len(stdout) > 100:
            return True, stdout.strip(), model
        else:
            return False, stderr or "empty", model
    except Exception as e:
        return False, str(e), model

def generate_narrative(title: str, params: dict, timeline: List[dict]) -> Tuple[bool, str, str]:
    params_str = "\n".join([f"- {k.replace('_', ' ').title()}: {v}" for k, v in params.items()])
    timeline_str = "\n".join([f"- {p['phase']}: {p['years']}" for p in timeline])
    full_prompt = f"{SYSTEM_PROMPT.format(timeline=timeline_str, params=params_str)}\n\n{USER_PROMPT.format(title=title)}"

    for model, timeout in AVAILABLE_MODELS:
        success, text, used = generate(full_prompt, model, timeout)
        if success:
            logger.info(f"Success with {used}")
            return True, text, used
        else:
            logger.warning(f"{model} failed: {text[:100]}")
    return False, "All models failed", "none"