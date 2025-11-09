#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  8 16:03:27 2025

@author: mike
"""

# oasis/s_generator/storage.py
import sqlite3
import json
from pathlib import Path
from oasis.config import settings
from oasis.logger import log

def _ensure_db_path():
    """Create data/ folder + empty DB file if missing."""
    db_path = Path(settings.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)  # <-- AUTO-CREATES data/
    if not db_path.exists():
        db_path.touch()  # creates empty .db file
        log.info("db.created", path=str(db_path))

def init_db():
    """Initialize DB with table — runs every time, safe."""
    _ensure_db_path()
    conn = sqlite3.connect(settings.db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scenarios (
            id TEXT PRIMARY KEY,
            title TEXT,
            data JSON
        )
    """)
    conn.commit()
    conn.close()

def save_scenario(scenario: dict):
    """Save one scenario — auto-creates DB if needed."""
    init_db()  # <-- guarantees DB exists
    conn = sqlite3.connect(settings.db_path)
    conn.execute(
        "INSERT INTO scenarios VALUES (?, ?, ?)",
        (scenario["id"], scenario["title"], json.dumps(scenario))
    )
    conn.commit()
    conn.close()