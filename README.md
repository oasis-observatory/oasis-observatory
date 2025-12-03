# OASIS Observatory

### *Open Artificial Superintelligence Scenario Observatory*
**Version:** 0.3 (MVP: Generators, Tracker, Report Generator) 
**Status:** Experimental — Under Active Development

---

## Overview

**OASIS Observatory** is an open research platform for **simulating, tracking, and analyzing potential trajectories of Artificial Superintelligence (ASI)**.

It integrates:

* **Speculative scenario generation**
* **Evidence-driven scenario generation** using real-world AI precursor signals
* **Signal tracking** from GitHub, ArXiv, and other sources
* **Consistency and schema validation**
* **Transparent data provenance**
* *(Planned)* Evolutionary scenario analysis and dashboards

The system supports researchers, foresight practitioners, and policymakers exploring long-horizon AI futures.

---

## Core Objectives

1. Simulate **ASI evolution from 2025–2100** using structured narrative scenarios.
2. Include **speculative early ASI precursors** (e.g., covert swarm-like ASIs 2010–2025).
3. Build a **large structured scenario database**, refined iteratively via LLM analysis.
4. Introduce **probabilistic and genetic-algorithm–inspired scenario evolution** (planned).
5. Provide **visualization dashboards and analytics** (planned).

---

## 🧪 Methodology

OASIS uses a **closed-loop probabilistic foresight model** combining:

* *Speculative foresight*
* *Real-world precursor signals*
* *LLM-generated scenario narratives*
* *JSON-schema validation*
* *Scenario ontology constraints*
* *Dynamic evolutionary updating* (future)
* *Multi-ASI interaction modeling* (future)

Conceptually, precursor signals act as **empirical weak evidence**, scenarios act as **structured hypotheses**, and the Analyzer module (v0.4+) will perform **GA-like weighting & mutation** of the scenario set.

---

# Module Overview

| Module                    | Description                                                                      |
| ------------------------- | -------------------------------------------------------------------------------- |
| **S-Generator**           | Speculative single-ASI scenario generator (randomized parameters).               |
| **M-Generator**           | Multi-ASI coexistence and interaction scenarios (speculative or evidence-based). |
| **EV-Generator**          | Evidence-based single-ASI scenarios influenced by precursor signals.             |
| **Tracker**               | Scrapes AI-relevant signals from GitHub, ArXiv; classifies and stores them.      |
| **Analyzer** *(Planned)*  | GA-inspired scenario weighting, plausibility scores, systemic complexity checks. |
| **Dashboard** *(Planned)* | Visual analytics (Streamlit/FastAPI).                                            |
| **Utils**                 | Report generation (PDF) and supplemental tools.                                  |
| **Data**                  | SQLite databases for scenarios, signals, and multi-ASI outcomes.                 |

---

# Repository Structure
## 🗂️ File Map
---
```
oasis-observatory/             # Root folder
├── data/                      # Data folder
│   ├── asi_scenarios.db       # SQLite database (auto-created) for single-ASI (precursor-based and fully speculative) and multi-ASI scenarios
│   ├── db_migrations.py       # Util for changing database tables - adding columns (temporary solution)
│   ├── deduplicate_signals.py # Util for deduplication of ASI precursors (temporary solution)
│   └── precursor_signals.db   # SQLite database (auto-created) for precursors of ASI from the real world data
│
├── oasis/                     # Project modules
│   ├── __init__.py 
│   ├── config.py              # Paths and constants (DB, schema, etc.)
│   ├── logger.py              # structlog setup for consistent logging
│   │
│   ├── common/                # Shared by different modules
│   │   ├── __init__.py 
│   │   ├── abbreviator.py     # Creates unique scenario IDs for single-ASI scenarios
│   │   ├── consistency.py     # NarrativeChecker for internal logic
│   │   ├── db.py              # Centralized database paths and connection utilities. Resolves paths relative to project root regardless of cwd.
│   │   ├── llm_client.py       # LLM interface for narrative generation
│   │   ├── storage.py         # Initialize DB and save generated scenarios into asi_scenarios.db
│   │   ├── schema.py          # SchemaManager: JSON Schema validation
│   │   └── timeline.py        # Generate dynamic timelines (2025–2100)
│   │
│   ├── analyzer/              # Scenario weighting via genetic approach
│   │   ├── cli_analyzer.py    # Link precursor signals to scenarios based on tags, text, and score.
│   │   ├── core_analyzer.py   # Evaluates scenario plausibility and systemic complexity. Estimates systemic complexity based on event density & diversity.
│   │   └── linkage.py         # Signal→scenario links.
│   │
│   ├─ dashboard/               # Visualization frontend
│   │   ├── dashboard.py        # TODO
│   │   ├── scenario_viewer.py  # TODO
│   │   └── precursor_viewer.py # TODO
│   │   
│   ├── ev_generator/                  # Evidence-based (precursor-influenced) scenario generation for a single ASI
│   │   ├── __init__.py
│   │   ├── cli_ev.py                  # CLI entrypoint for evidence-based scenario generation
│   │   ├── core_ev.py                 # Main orchestrator
│   │   └── params_ev.py               # Adjust parameters based on precursor signals
│   │   
│   ├── m_generator/           # Multi-ASI generation module (TODO - selecting speculative or evidence-based scenarios)
│   │   ├── __init__.py
│   │   ├── cli_m.py           # CLI entrypoint for multi-ASI generation
│   │   ├── core_m.py          # Spawn and manage multiple ASIs from the ASI_scenario database
│   │   ├── database_m.py      # DB integration for multi-ASI data
│   │   ├── interact.py        # Detect and simulate multiple ASI interaction patterns
│   │   ├── ollama_m.py        # Generates multi-ASI narrative
│   │   ├── renderer.py        # Turn interaction events into narrative output
│   │   ├── schema_m.py        # Creates and activates a dedicated table for multi-ASI briefings
│   │   └── storage_m.py       # Save multi-ASI scenarios
│   │
│   ├── s_generator/           # Speculative scenario generation (single ASI)
│   │   ├── __init__.py
│   │   ├── cli_s.py           # CLI entrypoint
│   │   ├── core_s.py          # Main orchestrator: generate_scenario()
│   │   └── params_s.py        # Randomly sample scenario parameters
│   │
│   └── tracker/               # Precursors scrapers and evaluators (GitHub/HF/Arxiv)
│       ├── __init__.py
│       ├── classifier_t.py      # ASI precursor signal classification and scoring.
│       ├── cli_tracker.py     # Tracker entrypoint
│       ├── core_t.py          # Fetch latest signals on superintelligence topic
│       └── database_t.py      # Unified precursor signal database with connection pooling and schema init.
│    
│   
├── schemas/
│   └── asi_scenario_v1.json   # JSON schema for scenario validation
│
├── tests/
│   ├── test_generator.py      # REWRITE
│   └── test_tracker.py        # REWRITE
│
├── tools/
│   ├── generate_report.py      # Generating scenario reports with diagrams
│   └── reports/                # PDF reports, containing 10 most diverse scenarios with visualizations
│
├── .env.example
├── pyproject.toml
└── README.md                  # You are here
```
---

# ⚙️ Execution Flow (v0.3 — Single-ASI)

### **S-Generator (speculative) & EV-Generator (signal-influenced)**

```
cli_s.py
    → core_s.py
        → sample_parameters()       # random or precursor-influenced
        → abbreviate()              # unique scenario ID
        → dynamic_timeline()        # 2025–2100
        → llm_client.generate()     # Ollama backend
        → NarrativeChecker.check()  # internal logic validation
        → SchemaManager.validate()  # JSON-schema compliance
        → save_scenario()           # SQLite (asi_scenarios.db)
```

### LLM Backend

* Local **Ollama models**:

  * llama3:8b
  * gemma2:9b
  * mistral:7b
* Output: **≈350 words** narrative + metadata.

---

# Scenario Ontology

Scenarios follow a consistent structural ontology enabling analysis:

* **Architecture**
* **Substrate**
* **Deployment medium/topology**
* **Autonomy degree**
* **Goal stability**
* **Oversight effectiveness**
* **Behavioral indicators**

  * Agency
  * Deception
  * Alignment
  * Opacity

---
# Tracker Module (Precursors)

Pipeline:

```
core_t.py → fetch → classify → store
precursor_signals.db
↓
linkage.py (planned) → signal-to-scenario matching
↓
dashboard (planned) → “Scenario X gained +7 new signals”
```

Sources:

* GitHub repositories
* ArXiv papers
* (Planned) Hugging Face
* (Planned) Technical blogs / research hubs

Each signal includes metadata such as title, description, tags, scores, and raw-source content.

---

# Evidence-Based Scenario Generation Flow

The EV-generator transforms precursor signals → numeric features → weighted parameters → narrative.

### High-Level Diagram

```
Precursor Signals (DB)
    ↓ fetch
Signal Feature Extraction
    ↓ transform
SignalInfluenceModel (blend with base params)
    ↓ input to LLM
LLM Scenario Generation
    ↓ validate & save
ev_scenarios table
```

### Feature Extraction

Signals are mapped to features such as:

* modularity
* decentralization
* embodiment
* agentic behavior
* alignment indicators
* risk factors
* power/safety relevance

These are blended with speculative parameters (~35% influence weight).

---

# Data Storage

### Databases (SQLite)

OASIS uses **two lightweight SQLite databases**:

---

### **1. `data/precursor_signals.db` — Real-World Signals**

Example schema:

```sql
CREATE TABLE precursor_signals (
    id            TEXT PRIMARY KEY,
    source        TEXT,
    title         TEXT,
    description   TEXT,
    stars         INTEGER,
    authors       TEXT,
    url           TEXT,
    published     TEXT,
    pdf_url       TEXT,
    signal_type   TEXT,
    score         REAL,
    tags          TEXT,
    raw_data      TEXT,
    collected_at  TEXT
);
```

---

### **2. `asi_scenarios.db` — Speculative & Evidence-Based Scenarios**

* `s_scenarios` table:
Example schema:

```sql
            id TEXT PRIMARY KEY,
            params TEXT,
            narrative TEXT,
            timeline TEXT,
            model_used TEXT,
            signals TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```
* `ev_scenarios` table:
Example schema:

```sql
            id TEXT PRIMARY KEY,
            params TEXT,
            narrative TEXT,
            timeline TEXT,
            model_used TEXT,
            signals TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

* `multi_asi_scenarios` table - under development
---

# Development Notes

* **Language:** Python 3.10+
* **CLI:** Typer
* **Database:** SQLite
* **Logging:** structlog
* **LLM Client:** Ollama (local inference)
* **Testing:** pytest

---

# Roadmap

| Phase     | Focus                                       |
| --------- | ------------------------------------------- |
| **v0.4**  | Scenario weighting & evolutionary selection |
| **v0.5**  | Dashboard for visualization & mapping       |
| **v0.6+** | Public interface, web API, dataset exports  |

---
# License

Released under the **MIT License**.

---
# Disclaimer
The scenarios generated by OASIS Observatory are based on **speculative modeling and hypothesis testing** using
parameterized inputs and evidence traceability from non-verified signals. The results (including X-Risk scores)
are **synthetic projections** and should not be interpreted as accurate predictions of future events. This tool is
for **research, academic, and educational purposes only** to explore the parameter space of potential ASI
risks. Reliance on this data for real-world policy or investment decisions is strictly discouraged.

OASIS Observatory does not predict future. It offers structured exploration of ASI possibility space.
*This is a scenario planning tool, not a prediction engine
*Outputs are illustrative hypotheticals, not forecasts
*Value lies in expanding thinking, not narrowing probabilities

---

# Citation

> Bukhtoyarov, M. (2025). *OASIS Observatory: Open Artificial Superintelligence Scenario Modeling Platform (v0.3).* GitHub: [https://github.com/oasis-observatory/oasis-observatory](https://github.com/oasis-observatory/oasis-observatory)

---
