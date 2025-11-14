# 🧠 **OASIS Observatory (Open Artificial Superintelligence Scenario Observatory)**
**Version:** 0.1.1-alpha (MVP: Generator Only)
**Status:** Experimental / Under Active Development
---

## 📘 Overview

**OASIS Observatory** is an open research platform that **simulates, tracks, and visualizes trajectories of Artificial Superintelligence (ASI)**.
It integrates **narrative foresight**, **real-world AI development signals**, and **transparent model provenance** to support researchers, policymakers, and AI safety practitioners in exploring and anticipating high-impact AI futures.

The platform currently focuses on **scenario generation**, simulating possible ASI development paths and their global impacts.

---

## 🎯 Core Goals

1. Simulate ASI evolution (2025–2100) through narrative scenarios. 
2. Includes speculative early precursors (e.g., covert swarm-like ASIs in 2010–2025).
3. Populate a scenario database with diverse speculative futures, then iteratively refine them using LLM-assisted evaluation.
4. Evaluate generated scenarios with logic and feasibility checks, supported by LLM-based meta-analysis layers.

---
## Methodology

A closed-loop probabilistic evolution system for Artificial Superintelligence (ASI) foresight modeling, where: 
precursor signals act as empirical evidence (real-world weak signals), scenarios are structured hypotheses (simulation-based or LLM-generated futures), 
and the system evolves the scenario set dynamically, weighting and mutating them according to updated evidence — 
just like a genetic algorithm (GA) applied to a dynamic world model.

---
## 🧩 Module Structure

| Module                    | Description                                                                                               |
|---------------------------|-----------------------------------------------------------------------------------------------------------|
| **S-Generator**           | Creates and stores ASI scenario narratives. Generates single-ASI trajectories.                            |
| **M-Generator**           | Creates and stores ASI scenario narratives. Generates muli-ASI trajectories.                              |
| **Tracker** *(Planned)*   | Extracts real-world AI development precursors from GitHub, Hugging Face, ArXiv, and blogs.                |
| **Analyzer** *(Planned)*  | Uses genetic algorithm-style weighting and LLMs to assess scenario plausibility and update probabilities. |
| **Dashboard** *(Planned)* | Provides visualization, mapping, and analytical tools via Streamlit or FastAPI.                           |
| **Data**                  | SQLite databases for scenario and precursor storage, reusable for research and creative exploration.      |
---

## 🗂️ File Map
```
oasis-observatory/             # Root folder
├── data/                      # Data folder
│   ├── asi_scenarios.db       # SQLite database (auto-created) for single-ASI and multi-ASI scenarios
│   ├── deduplicate_signals.py # Util for deduplication of ASI precursors (temporary solution)
│   └── precursor_signals.db   # SQLite database (auto-created) for precursors of ASI from the real world data
│
├── oasis/                     # Project modules
│   ├── __init__.py 
│   ├── config.py              # Paths and constants (DB, schema, etc.)
│   ├── logger.py              # structlog setup for consistent logging
│   │
│   ├── common/                # Shared by different modules
│   │   ├── db.py              # Centralized database paths and connection utilities. Resolves paths relative to project root regardless of cwd.
│   │   └── schema.py          # SchemaManager: JSON Schema validation
│   │
│   ├── analyzer/              # Scenario weighting via genetic approach
│   │   ├── cli_analyzer.py    # Link precursor signals to scenarios based on tags, text, and score.
│   │   ├── core_analyzer.py   # Evaluates scenario plausibility and systemic complexity. Estimates systemic complexity based on event density & diversity.
│   │   └── linkage.py         # Signal→scenario links.
│   │
│   ├─ dashboard/             # Visualization frontend
│   │   ├── asi_scenario_viewer.py # 
│   │   └── precursor_viewer.py # TODO
│   │   
│   ├── m_generator/           # Multi-ASI generation module
│   │   ├── __init__.py
│   │   ├── cli_m.py           # CLI entrypoint for multi-ASI generation
│   │   ├── core_m.py          # Spawn and manage multiple ASIs from the ASI_scenario database
│   │   ├── database.py        # DB integration for multi-ASI data
│   │   ├── interact.py        # Detect and simulate multiple ASI interaction patterns
│   │   ├── narrator.py        # Generates multi-ASI narrative
│   │   ├── renderer.py        # Turn interaction events into narrative output
│   │   ├── schema_m.py        # Creates and activates a dedicated table for multi-ASI briefings
│   │   └── storage_m.py       # Save multi-ASI scenarios
│   │
│   ├── s_generator/           # Core scenario generation module
│   │   ├── clients/
│   │   │   └── ollama.py      # LLM interface for narrative generation
│   │   ├── __init__.py
│   │   ├── abbreviator.py     # Creates unique scenario IDs
│   │   ├── batch_generate.py  # Batch scenario generation
│   │   ├── cli.py             # CLI entrypoint
│   │   ├── consistency.py     # NarrativeChecker for internal logic
│   │   ├── core.py            # Main orchestrator: generate_scenario()
│   │   ├── params.py          # Randomly sample scenario parameters
│   │   ├── storage.py         # Initialize DB and save generated scenarios
│   │   └── timeline.py        # Generate dynamic timelines (2025–2100)
│   │
│   └── tracker/               # Precursors scrapers and evaluators (GitHub/HF/Arxiv)
│       ├── __init__.py
│       ├── classifier.py      # ASI precursor signal classification and scoring.
│       ├── cli_tracker.py     # Tracker entrypoint
│       ├── core_t.py          # Fetch latest signals on superintelligence topic
│       └── database_t.py      # Unified precursor signal database with connection pooling and schema init.
│
├── schemas/
│   └── asi_scenario_v1.json   # JSON schema for scenario validation
│
├── tests/
│   ├── test_generator.py      # REWRITE
│   └── test_tracker.py        # REWRITE
│
├── .env.example
├── pyproject.toml
└── README.md                  # You are here
```
---
## Execution flow (REWRITE, NOW SINGLE-ASI GENERATOR ONLY):

    cli_s.py
        CLI entry: oasis generate [--count N]

    core_s.py
        sample_parameters() → Random ASI attributes (e.g., origin, emergence type)
        abbreviate(params) → Generate unique scenario ID
        dynamic_timeline() → 2025–2100 timeline
        ollama.generate_scenario() → Request LLM-generated narrative
        NarrativeChecker.check() → Consistency check
        SchemaManager.validate() → JSON Schema validation
        save_scenario() → Store in SQLite

    ollama.py
        Calls local Ollama LLMs (llama3:8b, gemma2:9b, mistral:7b)
        Returns ~350-word narrative text

    storage_s.py
        Writes validated scenario into data/asi_scenarios.db

---
## Tracker

oasis track all
       ↓
  core_t.py → fetch → classify → store
       ↓
  precursor_signals.db ← linked via signal_scenario_links (v0.4)
       ↓
  analyzer/linkage.py → matches signals → scenarios
       ↓
  dashboard/asi_scenario_viewer.py → "This scenario now has +7 new signals"

---
## Analyzer Module – How Signals Connect to Scenarios

The `oasis analyze` command runs a **real-time linkage engine** that connects real-world precursor signals (GitHub repos, papers, news) to generated ASI scenarios.

---
## 💾 Data Storage

* **Database:** `data/asi_scenarios.db`
* **Table:** `scenarios`
  * `id` – Text, primary key
  * `title` – Text, Scenario title (abbreviated)
  * `data` – JSON document (parameters, timeline, narrative, metadata)
* **Table:** `multi_asi_scenarios`
  * `id` – Text, primary key
  * `created` – Timestamp
  * `last_updated` – Timestamp
  * `asi_count` – Integer, number of interacting ASIs
  * `source` – Text, source of the scenario (project, version)
  * `id` – Integer primary key
  * `title` – Scenario title (abbreviated)
  * `data` – JSON document (parameters, timeline, narrative, metadata)
  * `threat_index` – Real

* **Database:** `data/precursor_signals.db`

## Database Specifications

OASIS uses **three SQLite databases** — lightweight, zero-config, and perfect for real-time observability.

### 1. `data/precursor_signals.db` – Real-World Signals
Stores GitHub repos, papers, news — anything that hints at ASI progress.

```sql
CREATE TABLE precursor_signals (
    id            TEXT PRIMARY KEY,        -- UUID or GitHub repo ID
    source        TEXT,                    -- "github", "arxiv", "news"
    title         TEXT,                    -- Repo name or paper title
    description   TEXT,                    -- Short description
    stars         INTEGER,                 -- GitHub stars (if applicable)
    authors       TEXT,                    -- JSON array or comma-separated
    url           TEXT,                    -- Source URL
    published     TEXT,                    -- ISO date
    pdf_url       TEXT,                    -- If paper
    signal_type   TEXT,                    -- "technical", "funding", "policy"
    score         REAL,                    -- Relevance score (1.0–10.0)
    tags          TEXT,                    -- JSON array: ["asi_direct", "alignment"]
    raw_data      TEXT,                    -- Full JSON from API (readme, topics, etc.)
    collected_at  TEXT                     -- ISO timestamp
);

---

## 🧪 Development Notes

* **Language:** Python 3.10+
* **CLI Framework:** Typer
* **Database:** SQLite
* **Logging:** structlog
* **LLM Client:** Ollama (local models)
* **Testing:** pytest

---

## 🧭 Roadmap

| Phase     | Focus                                                 |
| --------- | ----------------------------------------------------- |
| **v0.3**  | Integrate real-world precursors (GitHub, HF)          |
| **v0.4**  | Scenario weighting and evolutionary selection         |
| **v0.5**  | Visualization dashboard (Streamlit/FastAPI)           |
| **v0.6+** | Collaborative web interface and public dataset export |

---

## License

**MIT License** — open for academic, research, and educational use.

---

## Citation

If you use OASIS Observatory in research, please cite:

> Bukhtoyarov, M. (2025). *OASIS Observatory: Open Artificial Superintelligence Scenario Modeling Platform (v0.1.1)*. GitHub Repository: [https://github.com/oasis-observatory/oasis-observatory](https://github.com/oasis-observatory/oasis-observatory)

---
