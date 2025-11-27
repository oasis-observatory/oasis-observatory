# oasis/tracker/core_t.py

import time
import uuid
import json
import requests
import feedparser
import urllib.parse
from datetime import datetime, timezone
from typing import Dict, Any

from oasis.tracker.classifier_t import classify_and_score
from oasis.tracker.database_t import init_precursor_db, get_connection


# Initialize DB (ensure table exists)
init_precursor_db()


def _signal_exists(source: str, url: str) -> bool:
    """Return True if a signal with the same source+url exists."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM precursor_signals WHERE source = ? AND url = ?",
            (source, url)
        ).fetchone()
        return row is not None


def _store_signal(signal_record: Dict[str, Any]) -> None:
    """Insert signal only if not exists; update score/tags if higher."""
    with get_connection() as conn:
        if _signal_exists(signal_record["source"], signal_record["url"]):
            # Update score/tags if higher
            conn.execute("""
                UPDATE precursor_signals
                SET score = MAX(score, ?),
                    tags = ?,
                    collected_at = ?,
                    stars = ?
                WHERE source = ? AND url = ?
            """, (
                signal_record["score"],
                signal_record["tags"],
                signal_record["collected_at"],
                signal_record.get("stars"),
                signal_record["source"],
                signal_record["url"]
            ))
            conn.commit()
            print(f"Updated: {signal_record['title'][:60]} → {signal_record['score']:.1f}")
        else:
            # Insert new signal
            conn.execute("""
                INSERT INTO precursor_signals
                (id, source, title, description, stars, authors, url, published, pdf_url,
                 signal_type, score, tags, raw_data, collected_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                signal_record.get("id") or str(uuid.uuid4()),
                signal_record["source"],
                signal_record["title"],
                signal_record["description"],
                signal_record.get("stars"),
                signal_record.get("authors"),
                signal_record["url"],
                signal_record.get("published"),
                signal_record.get("pdf_url"),
                signal_record["signal_type"],
                signal_record["score"],
                signal_record["tags"],
                signal_record["raw_data"],
                signal_record["collected_at"]
            ))
            conn.commit()
            print(f"New signal: {signal_record['title'][:60]} (score: {signal_record['score']:.1f})")

def safe_entry_field(entry, field, default=None):
    return getattr(entry, field, entry.get(field, default)) if hasattr(entry, field) or field in entry else default

def fetch_and_store_github_signals(limit: int = 20) -> int:
    """Fetch GitHub repos and store new signals."""
    url = "https://api.github.com/search/repositories"
    query = "(superintelligence OR artificial general intelligence OR ASI OR AGI) language:Python pushed:>2024-01-01"
    params = {
        "q": query,
        "sort": "updated",
        "order": "desc",
        "per_page": min(limit, 100)
    }
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, params=params, headers=headers, timeout=15)
    response.raise_for_status()
    items = response.json().get("items", [])

    stored = 0
    for item in items:
        if _signal_exists("github", item["html_url"]):
            continue

        metadata = {
            "title": item["name"],
            "description": item.get("description") or "",
            "url": item["html_url"],
            "stars": item["stargazers_count"],
            "authors": item["owner"]["login"]
        }
        classified = classify_and_score(metadata)

        signal_record = {
            "id": str(uuid.uuid4()),
            "source": "github",
            "title": metadata["title"],
            "description": metadata["description"],
            "stars": metadata["stars"],
            "authors": metadata["authors"],
            "url": metadata["url"],
            "signal_type": classified["signal_type"],
            "score": classified["score"],
            "tags": json.dumps(classified["tags"]),
            "raw_data": json.dumps(metadata),
            "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds")
        }
        _store_signal(signal_record)
        stored += 1
        time.sleep(0.5)  # Stay under GitHub secondary rate limit

    print(f"github: {stored} new/updated signals stored")
    return stored

def fetch_and_store_arxiv_signals(limit: int = 15) -> int:
    """Fetch latest arXiv papers on superintelligence."""
    query = (
        "superintelligence OR ASI OR AGI OR \"artificial general intelligence\" OR "
        "\"autonomous agent\" OR \"self-improving\""
    )
    encoded_query = urllib.parse.quote(query)
    base_url = f"http://export.arxiv.org/api/query?search_query={encoded_query}&max_results={limit}&sortBy=submittedDate&sortOrder=descending"

    stored = 0
    for attempt in range(3):  # Retry up to 3x
        try:
            feed = feedparser.parse(base_url)
            if feed.bozo:  # Parse error (e.g., invalid XML)
                raise ValueError(f"Feed parse error: {feed.get('bozo_exception', 'Unknown')}")
            entries = feed.entries or []
            if not entries and attempt == 0:
                print(f"arXiv API returned 0 entries (possible transient error); retrying...")
                time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s
                continue

            for entry in entries:
                # Skip if it's the error page (heuristic)
                if "error" in (getattr(entry, "title", "").lower() or getattr(entry, "summary", "").lower()):
                    print("Skipping arXiv error page entry.")
                    continue

                if _signal_exists("arxiv", entry.link):
                    continue

                metadata = {
                    "title": getattr(entry, "title", "Untitled"),
                    "description": getattr(entry, "summary", "")[:2000],
                    "url": getattr(entry, "id", entry.link),  # Use .id if available (canonical)
                    "authors": ", ".join(getattr(a, "name", "") for a in getattr(entry, "authors", [])),
                    "published": safe_entry_field(entry, "published", safe_entry_field(entry, "updated"))
                }

                classified = classify_and_score(metadata)

                signal_record = {
                    "id": str(uuid.uuid4()),
                    "source": "arxiv",
                    "title": metadata["title"],
                    "description": metadata["description"],
                    "authors": metadata["authors"],
                    "url": metadata["url"],
                    "published": metadata["published"],
                    "pdf_url": metadata["url"].replace("/abs/", "/pdf/") + ".pdf" if metadata["url"] else "",
                    "signal_type": classified["signal_type"],
                    "score": classified["score"],
                    "tags": json.dumps(classified["tags"]),
                    "raw_data": json.dumps(metadata),
                    "collected_at": datetime.now(timezone.utc).isoformat(timespec="seconds")
                }
                _store_signal(signal_record)
                stored += 1

            print(f"arXiv: {stored} new/updated signals stored")
            return stored  # Success – exit retry loop

        except Exception as e:
            print(f"arXiv fetch attempt {attempt + 1} failed: {e}")
            if attempt == 2:
                print("All retries exhausted – skipping arXiv this sweep.")
                return 0
            time.sleep(2 ** attempt)

    return stored