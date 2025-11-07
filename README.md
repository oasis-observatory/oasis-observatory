---
# **Open Artificial Superintelligence Scenario Observatory (OASIS Observatory v0.1)**
[![Project Status: Alpha – MVP (Generator only)](https://img.shields.io/badge/status-alpha%20%28generator%20only%29-red.svg)](https://github.com/oasis-observatory/oasis-observatory/issues)
---

## Overview

**OASIS Observatory** is an open research platform that **simulates, tracks, and visualizes trajectories of Artificial Superintelligence (ASI)**.
It integrates narrative foresight, real-world data signals, and transparent model provenance to help researchers, policymakers, and AI safety practitioners **anticipate high-impact futures**.

---

## Mission Statement

> *“Transparency and rigor are non-negotiable when modeling futures that matter.”*

OASIS Observatory applies **schema-based foresight modeling** and **multi-agent simulation** to explore the emergence, coordination, and risks of advanced AI systems.
It aims to provide a reproducible, explainable foundation for **superintelligence governance research** and **ethical AI forecasting**.

---

## Core Features

* **Structured foresight schema** — JSON-based definitions for ASI scenarios (origin, architecture, alignment, impact).
* **Quantitative + narrative integration** — Combines probability fields with timeline narratives.
* **Model provenance tracking** — Records model identity, parameters, and configuration for every generated scenario.
* **Evidence layer (future)** — Links generated scenarios with precursor signals from real-world data.
* **Open methodology** — Fully open-source and schema-driven for auditability and transparency.

---

## System Architecture

OASIS is implemented as a modular Python monorepo:

```

oasis-observatory/                     # Root: one repo
├── data/                              # Runtime data — NEVER committed
│   ├── asi_scenarios.db               # SQLite: single-ASI narratives
│   ├── multi_asi_scenarios.db         # SQLite: multi-agent interaction logs
│   └── precursor_signals.db           # SQLite: real-world AI precursor events
│
├── common/                            # Shared, versioned core — imported everywhere
│   ├── __init__.py                    # Exposes: log, db, abbreviate_title, sample_params
│   ├── db.py                          # get_conn(name), auto-migrate, thread-safe
│   ├── logger.py                      # Rich + rotating file handler, one-liner: log.info()
│   ├── text_utils.py                       # abbreviate_title(), slugify(), truncate()
│   ├── validation.py                  # validate_asi_scenario(data), validate_signal()
│   ├── parameter_sampler.py           # sample_one(), sample_batch(), --seed support
│   └── schemas/                       # JSON Schema contracts (peer-reviewed)
│       ├── asi_scenario.json          # Required fields, enums, patterns
│       ├── multi_asi_scenario.json
│       └── signals.json
│
├── generator/                         # PHASE 1 — MVP (works today)
│   ├── __init__.py                    # from .generate_batch import run_batch
│   ├── cli.py                         # typer CLI → oasis-generator
│   ├── config/
│   │   ├── __init__.py
│   │   ├── ollama_settings.json       # model, temp, top_p
│   │   └── prompts/
│   │       ├── single_asi.txt         # {{params}} → narrative
│   │       └── multi_asi.txt
│   ├── single_asi_scenario.py         # prompt → JSON → validate → DB
│   ├── single_asi_ollama_client.py    # retry, streaming, timeout
│   ├── single_asi_database.py         # INSERT with upsert
│   ├── multi_asi_scenario.py          # orchestrates N single runs
│   ├── multi_asi_ollama_client.py
│   ├── multi_asi_database.py
│   ├── generate_batch.py              # reads data/params.json OR samples live
│   └── _demo_scenarios.py             # 5 hand-crafted examples for make demo
│
├── tracker/                           # PHASE 2 — Q4 2025
│   ├── __init__.py
│   ├── cli.py                         # oasis-tracker --once / --watch
│   ├── config/
│   │   ├── sources.yaml               # arXiv CS, Hacker News, GitHub trending
│   │   └── keywords.yaml
│   ├── tracker.py                     # scheduler + dispatcher
│   ├── extractor.py                   # RSS/JSON → raw text
│   ├── signal_parser.py               # LLM-free regex + heuristics
│   ├── signal_classifier.py           # maps to ASI scenario categories
│   ├── precursor_database.py          # writes to precursor_signals.db
│   └── metrics.py                     # daily signal velocity dashboard
│
├── dashboard/                         # PHASE 3 — Q1 2026
│   ├── __init__.py
│   ├── app.py                         # Streamlit UI (default)
│   ├── api.py                         # FastAPI REST (optional)
│   ├── config/
│   │   └── ui_settings.json
│   ├── static/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── logo.svg
│   ├── queries.py                     # SQL → pandas → JSON
│   ├── map_projection.py              # 2D UMAP of scenario space
│   └── analytics.py                   # Monte-Carlo risk curves
│
├── docs/                              # Publish-ready
│   ├── architecture.md                # Mermaid diagrams
│   ├── roadmap.md                     # Gantt + milestones
│   ├── ethics.md                      # Bias, dual-use, transparency
│   └── methodology.md                 # Why narrative + schema beats pure LLM
│
├── tests/                             # pytest — CI passes → funding gate
│   ├── conftest.py                    # fixtures: temp_db, mock_ollama
│   ├── test_generator.py
│   ├── test_tracker.py
│   ├── test_dashboard.py
│   ├── test_utils.py
│   └── test_validation.py
│
├── scripts/                           # One-off tools
│   ├── oasis-params                   # CLI → common/parameter_sampler.py
│   ├── validate_schemas.py
│   ├── migrate_data.py
│   └── seed_demo_data.py
│
├── demo/                              # 60-second pitch
│   ├── record.mp4
│   └── screenshots/
│       ├── generator-cli.png
│       ├── dashboard-map.png
│       └── params-dist.png
│
├── .github/
│   └── workflows/
│       └── ci.yml                     # lint (ruff) → test → docker build
│
├── .gitignore                         # data/, __pycache__, .env, *.db
├── pyproject.toml                     # PEP 621 + entry-points
├── Makefile                           # make demo → 10 seconds to wow
├── docker-compose.yml                 # generator + dashboard + volume
└── README.md                          # Hero section + one-liner install
```

## 🧬 Data Ethics & Transparency

OASIS Observatory adheres to the following principles:

* **Transparency:** All generated outputs record model, parameters, and date.
* **Provenance:** Every entry in `.db` is schema-validated and auditable.
* **Open Research:** No proprietary data or black-box inference used.
* **Ethical Foresight:** Scenarios are for policy research and education — *not predictions*.

---

## Roadmap

| Phase                         | Timeline   | Focus                                   |
| ----------------------------- | ---------- | --------------------------------------- |
| **Phase 1 — Generator (MVP)** | 🚧 2025 Q4 | Scenario generation, schema validation  |
| **Phase 2 — Tracker**         | 🚧 2026 Q1 | Precursor signal extraction and mapping |
| **Phase 3 — Dashboard**       | ⏳ 2026 Q2 | Visualization, analytics, reporting     |

---

## Team

| Role                              | Name                                                                           | Focus                                           |
| --------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------- |
| **Founder & Lead Architect**      | [**Mikhail Bukhtoyarov**](https://philpeople.org/profiles/mikhail-bukhtoyarov) | Philosophy of Technology, foresight methodology |
| **Core Contributor (Dev Lead)**   | TBD                                                                            | Software architecture, system design            |
| **Core Contributor (Governance)** | TBD                                                                            | Legal and organizational alignment              |

> Want to contribute or be publicly credited?
> Join [Discussions](https://github.com/oasis-observatory/oasis-observatory/discussions) or open an Issue.

## 📄 License

**MIT License** — open for academic, research, and educational use.

---

## Citation

If you use OASIS Observatory in research, please cite:

> Bukhtoyarov, M. (2025). *OASIS Observatory: Open Artificial Superintelligence Scenario Modeling Platform (v0.2)*. GitHub Repository: [https://github.com/oasis-observatory/oasis-observatory](https://github.com/oasis-observatory/oasis-observatory)
