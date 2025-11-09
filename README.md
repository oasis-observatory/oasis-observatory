### 🧠 **OASIS Observatory (Open Artificial Superintelligence Scenario Observatory)**
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
oasis-observatory/
├── data/
│   └── asi_scenarios.db       # SQLite database (auto-created)
│
├── oasis/                     
│   ├── __init__.py 
│   ├── config.py              # Paths and constants (DB, schema, etc.)
│   ├── logger.py              # structlog setup for consistent logging
│   │
│   ├── common/
│   │   └── schema.py          # SchemaManager: JSON Schema validation
│   │
│   ├── s_generator/           # Core scenario generation module
│   │   ├── clients/
│   │   │   └── ollama.py      # LLM interface for narrative generation
│   │   ├── __init__.py
│   │   ├── abbreviator.py     # Creates unique scenario IDs
│   │   ├── batch_generate.py  # Batch scenario generation
│   │   ├── cli.py             # Typer CLI entrypoint: `oasis generate`
│   │   ├── consistency.py     # NarrativeChecker for internal logic
│   │   ├── core.py            # Main orchestrator: generate_scenario()
│   │   ├── params.py          # Randomly sample scenario parameters
│   │   ├── storage.py         # Initialize DB and save generated scenarios
│   │   └── timeline.py        # Generate dynamic timelines (2025–2100)
│   │   
│   ├── m_generator/           # Multi-ASI simulation
│   │   ├── __init__.py
│   │   ├── cli_m.py           # CLI entrypoint: `oasis swarm`
│   │   ├── core_m.py          # Spawn and manage multiple ASIs
│   │   ├── database.py        # DB integration for swarm data
│   │   ├── interact.py        # Detect and simulate swarm interaction patterns
│   │   ├── narrator.py        # 
│   │   ├── renderer.py        # Turn interaction events into narrative output
│   │   ├── schema_m.py        # 
│   │   ├── storage_m.py       # Save multi-ASI scenarios
│   │   └── models.py          # Dataclasses (optional)
│   │
│   ├── tracker/               # TODO: Precursors scrapers (GitHub/HF/Arxiv)
│   ├── analyzer/              # TODO: Scenario weighting via genetic approach
│   └── dashboard/             # TODO: Visualization frontend
│
├── schemas/
│   └── asi_scenario_v1.json   # JSON schema for scenario validation
│
├── tests/
│   ├── test_generator.py
│   └── test_oasis_1.py
│
├── .env.example
├── pyproject.toml
└── README.md
```

---

## ⚙️ Generator Overview (v0.2)

```
┌───────────────────────────────────────────┐
│ cli.py → generate() → generate_scenario() │
└───┬───────────────────────────────────────┘
    ▼
┌──────────────────────────────────────────────┐
│ core.py → generate_scenario()                │
│ (main orchestrator)                          │
└───┬─────────────────────┬───────────────────┬┘
    ▼                     ▼                   ▼
 params.py           timeline.py        abbreviator.py
 sample_parameters() dynamic_timeline() abbreviate()
```

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

## 🧠 Swarm Generator Flow

```
python oasis/swarm/cli_m.py
        │
        ▼
  interactive_startup() → config
        │
        ▼
   spawn_swarm(n)
        │
        ├─→ generate_scenario() × n
        │     ├─ sample_parameters()
        │     ├─ generate_narrative()
        │     └─ save_scenario()
        │
        ▼
    interact_all(swarm)
        │
        ├─ detect_pattern() → Event objects
        ├─ render_interaction() → narrative dict
        └─ save_multi_asi_scenario() → SQLite
```

---

## 💾 Data Storage

* **Database:** `data/asi_scenarios.db`
* **Table:** `scenarios`

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

## 🧑‍🔬 Credits

**Author / Maintainer:** OASIS Research Collective
**License:** MIT (provisional)
**Contact:** *[add contact or repository URL]*

---
