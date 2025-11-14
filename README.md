### 🧠 **OASIS Observatory (Open Artificial Superintelligence Scenario Observatory)**
[![Project Status: Alpha – MVP (Generator only)](https://img.shields.io/badge/status-alpha%20%28generator%20only%29-red.svg)](https://github.com/oasis-observatory/oasis-observatory/issues)

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

**Execution flow:**

1. **`cli.py`**

   * CLI entry: `oasis generate [--count N]`
2. **`core.py`**

   * `sample_parameters()` → Random ASI attributes (e.g., origin, emergence type)
   * `abbreviate(params)` → Generate unique scenario ID
   * `dynamic_timeline()` → 2025–2100 timeline
   * `ollama.generate_scenario()` → Request LLM-generated narrative
   * `NarrativeChecker.check()` → Consistency check
   * `SchemaManager.validate()` → JSON Schema validation
   * `save_scenario()` → Store in SQLite
3. **`ollama.py`**

   * Calls local Ollama LLMs (`llama3:8b`, `gemma2:9b`, `mistral:7b`)
   * Returns ~350-word narrative text
4. **`storage.py`**

   * Writes validated scenario into `data/asi_scenarios.db`

---

## 💾 Data Storage

* **Database:** `data/asi_scenarios.db`
* **Table:** `scenarios`
* **Table:** `multi_asi_scenarios`

  * `id` – Integer primary key
  * `title` – Scenario title (abbreviated)
  * `data` – JSON document (parameters, timeline, narrative, metadata)

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
