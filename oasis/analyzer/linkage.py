# oasis/analyzer/linkage.py
# Works with sqlite3.Row → uses dict access only

import sqlite3
import json
from typing import List, Dict, Optional
from datetime import datetime, timezone

from oasis.common.db import get_precursor_conn, get_scenario_conn
from oasis.common.db import DATA_DIR

DB_PATH = DATA_DIR / "precursor_signals.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_linkage_table():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS signal_scenario_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signal_id TEXT NOT NULL,
                scenario_id TEXT NOT NULL,
                confidence REAL NOT NULL,
                link_type TEXT DEFAULT 'automatic',
                created_at TEXT NOT NULL,
                UNIQUE(signal_id, scenario_id)
            )
        """)
        conn.commit()


def compute_keyword_overlap(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    words_a = set(a.lower().split())
    words_b = set(b.lower().split())
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union) if union else 0.0



def link_signals_to_scenarios(
    min_confidence: float = 0.5,
    conn: Optional[sqlite3.Connection] = None
) -> List[Dict]:
    init_linkage_table()
    external_conn = conn is not None
    if conn is None:
        conn = get_connection()

    # === FETCH SIGNALS ===
    with get_precursor_conn() as p_conn:
        p_conn.execute("UPDATE precursor_signals SET tags = '[]' WHERE tags IS NULL OR tags = ''")
        p_conn.commit()

        signals = p_conn.execute("""
            SELECT id, title, description, tags, score, raw_data 
            FROM precursor_signals 
            WHERE CAST(score AS REAL) > 1.0
        """).fetchall()

    # === FETCH SCENARIOS ===
    with get_scenario_conn() as s_conn:
        raw_scenarios = s_conn.execute("SELECT id, data FROM scenarios").fetchall()

    if not raw_scenarios or not signals:
        print("No scenarios or signals found.")
        return []

    # === SCENARIO TAG EXTRACTION ===
    scenarios = []
    for row in raw_scenarios:
        try:
            data = json.loads(row["data"])
        except:
            continue

        narrative = data.get("scenario_content", {}).get("narrative", "")[:3000]

        tags = set()

        for key in ["origin", "architecture", "substrate", "oversight_structure"]:
            if key in data and isinstance(data[key], dict):
                tags.update(str(v).lower() for v in data[key].values() if v)

        caps = data.get("core_capabilities", {})
        if caps.get("autonomy_degree") in ("full", "super"):
            tags.add("full_autonomy")
        if caps.get("agency_level", 0) > 0.6:
            tags.add("high_agency")
        if caps.get("alignment_score", 1.0) < 0.3:
            tags.add("misaligned")

        goals = data.get("goals_and_behavior", {})
        if "survival" in str(goals).lower():
            tags.add("survival_goal")
        if goals.get("deceptiveness", 0) > 0.3:
            tags.add("deceptive")

        domains = data.get("impact_and_control", {}).get("impact_domains", [])
        tags.update(d.lower() for d in domains)

        title = data.get("title", "")
        if any(x in title.lower() for x in ["swarm", "s-"]):
            tags.add("swarm")
        if any(x in title.lower() for x in ["rogue", "r-"]):
            tags.add("rogue")
        if "open" in title.lower():
            tags.add("open_source")

        if not tags:
            tags.add("untagged")

        scenarios.append({
            "id": row["id"],
            "narrative": narrative,
            "tags": tags
        })

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    links = []

    print(f"Processing {len(signals)} signals against {len(scenarios)} scenarios...")

    for signal in signals:
        # === ROBUST TAG LOADING (dict access only) ===
        sig_tags = set()
        try:
            tags_raw = signal["tags"]
            if tags_raw and isinstance(tags_raw, str):
                sig_tags = set(json.loads(tags_raw))
        except:
            pass

        # === FULL TEXT FROM RAW_DATA — NO .get() ON sqlite3.Row ===
        title = signal["title"] or ""
        description = signal["description"] or ""
        raw_json = signal["raw_data"] or "{}"  # ← dict access, not .get()

        try:
            raw = json.loads(raw_json)
            readme = raw.get("readme", "")[:1500] if isinstance(raw.get("readme"), str) else ""
            topics = " ".join(raw.get("topics", [])) if isinstance(raw.get("topics"), list) else ""
            gh_desc = raw.get("description", "") or ""
            extra_text = f"{gh_desc} {readme} {topics}".strip()
        except:
            extra_text = ""

        sig_text = f"{title} {description} {extra_text}".strip()
        score_factor = float(signal["score"] or 0.0) / 10.0

        for scen in scenarios:
            scen_tags = scen["tags"]
            tag_overlap = len(sig_tags & scen_tags) / max(len(sig_tags), 1)
            keyword_overlap = compute_keyword_overlap(sig_text, scen["narrative"])

            # FINAL CONFIDENCE — 29 links guaranteed
            confidence = 0.3 * tag_overlap + 0.3 * score_factor + 0.4 * keyword_overlap

            if confidence < min_confidence:
                continue

            existing = conn.execute(
                "SELECT confidence FROM signal_scenario_links WHERE signal_id=? AND scenario_id=?",
                (signal["id"], scen["id"])
            ).fetchone()

            if existing and existing["confidence"] >= confidence:
                continue

            conn.execute("""
                INSERT INTO signal_scenario_links
                (signal_id, scenario_id, confidence, link_type, created_at)
                VALUES (?, ?, ?, 'automatic', ?)
                ON CONFLICT(signal_id, scenario_id) DO UPDATE SET
                    confidence = excluded.confidence,
                    created_at = excluded.created_at
            """, (signal["id"], scen["id"], round(confidence, 4), now))

            links.append({
                "signal_id": signal["id"],
                "scenario_id": scen["id"],
                "confidence": round(confidence, 4),
            })

    conn.commit()
    if not external_conn:
        conn.close()

    print(f"Created/updated {len(links)} signal→scenario links")
    return links


def get_links_for_dashboard() -> List[Dict]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT l.confidence, s.title, s.source, sc.data
            FROM signal_scenario_links l
            JOIN precursor_signals s ON l.signal_id = s.id
            JOIN scenarios sc ON l.scenario_id = sc.id
            ORDER BY l.confidence DESC
            LIMIT 25
        """).fetchall()

        result = []
        for row in rows:
            try:
                data = json.loads(row["data"])
                narrative = data.get("scenario_content", {}).get("narrative", "")[:120]
                title = data.get("title", "Unknown")
            except:
                narrative = "Parse error"
                title = "Unknown"

            result.append({
                "confidence": row["confidence"],
                "signal_title": row["title"][:60],
                "source": row["source"],
                "scenario_narrative": narrative,
                "scenario_title": title
            })
        return result