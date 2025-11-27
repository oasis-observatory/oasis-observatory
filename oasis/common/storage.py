#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# oasis/common/storage.py

import sqlite3
import json
import uuid
from pathlib import Path
from oasis.config import settings
from oasis.logger import log


# ------------------------------------------------------------
# DB Setup
# ------------------------------------------------------------

def _ensure_db_path():
    """Ensure database directory + file exist."""
    db_path = Path(settings.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    if not db_path.exists():
        db_path.touch()
        log.info("db.created", path=str(db_path))


def get_conn():
    """Return sqlite3 connection with row dicts enabled."""
    _ensure_db_path()
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_table(table_name: str):
    """Create the standard scenario table schema."""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id TEXT PRIMARY KEY,
            params TEXT,
            narrative TEXT,
            timeline TEXT,
            model_used TEXT,
            signals TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    conn.commit()
    conn.close()


def init_db():
    """
    Create both tables used by generators.
    Always safe to call.
    """
    _ensure_db_path()

    init_table("s_scenarios")      # s-generator storage
    init_table("ev_scenarios")     # ev-generator storage

    log.info("storage.initialized", tables=["asi_scenarios", "ev_asi_scenarios"])
    print("[storage] Database initialized and tables ensured.")


# ------------------------------------------------------------
# Saving Logic
# ------------------------------------------------------------

def save_scenario(
    table_name: str,
    *,
    params,
    narrative,
    timeline,
    model_used,
    signals=None
):
    """
    Generic save function used by both S and EV generators.
    """
    scenario_id = str(uuid.uuid4())
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        f"""
        INSERT INTO {table_name}
        (id, params, narrative, timeline, model_used, signals)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            scenario_id,
            json.dumps(params),
            narrative,
            json.dumps(timeline),
            model_used,
            json.dumps(signals or []),
        ]
    )

    conn.commit()
    conn.close()

    return scenario_id


# ------------------------------------------------------------
# Wrappers for S & EV Generators
# ------------------------------------------------------------

def save_scenario_s(*, params, narrative, timeline, model_used):
    """Wrapper for s-generator (no signals field)."""
    return save_scenario(
        "s_scenarios",
        params=params,
        narrative=narrative,
        timeline=timeline,
        model_used=model_used,
        signals=[]
    )


def save_scenario_ev(*, params, narrative, timeline, model_used, signals):
    """Wrapper for ev-generator (uses signals field)."""
    return save_scenario(
        "ev_scenarios",
        params=params,
        narrative=narrative,
        timeline=timeline,
        model_used=model_used,
        signals=signals
    )
