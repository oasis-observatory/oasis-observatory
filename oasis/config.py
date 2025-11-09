#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 15:33:57 2025

@author: mike
"""

# oasis/config.py
from pydantic_settings import BaseSettings
from pathlib import Path

ROOT = Path(__file__).parent.parent

class Settings(BaseSettings):
    ollama_timeout: int = 300
    ollama_preferred_model: str = "llama3.1:8b"
    db_path: Path = ROOT / "data" / "asi_scenarios.db"
    schema_path: Path = ROOT / "schemas" / "asi_scenario_v1.json"
    log_level: str = "INFO"

    model_config = {"env_file": ".env"}

settings = Settings()