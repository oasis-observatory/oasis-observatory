# oasis/tracker/database_t.py  ← NEW FILE
# Unified precursor signal database with connection pooling and schema init.

import sqlite3
import os

#from typing import Dict, Any
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "precursor_signals.db"

@contextmanager
def get_connection():
    """Context manager for SQLite connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Dict-like rows
    try:
        yield conn
    finally:
        conn.close()


def init_precursor_db():
    """Initialize the precursor signals database with all tables."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS precursor_signals (
                id TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                title TEXT,
                description TEXT,
                stars INTEGER,
                authors TEXT,
                url TEXT,
                published TEXT,
                pdf_url TEXT,
                signal_type TEXT DEFAULT 'model',
                score REAL DEFAULT 0.0,
                tags TEXT,
                raw_data TEXT,
                collected_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS signal_features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id TEXT,
                risk_category TEXT,
                asi_feature TEXT,
                relevance_score REAL DEFAULT 1.0,
                FOREIGN KEY (signal_id) REFERENCES precursor_signals(id)
            );
        """)
        conn.commit()
    print("✅ Precursor database initialized.")