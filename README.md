---

# 🌌 **Open Artificial Superintelligence Scenario Observatory (OASIS Observatory v0.1)**
[![Project Status: Alpha – MVP (Generator only)](https://img.shields.io/badge/status-alpha%20%28generator%20only%29-red.svg)](https://github.com/oasis-observatory/oasis-observatory/issues)
---

## Overview

**OASIS Observatory** is an open research platform that **simulates, tracks, and visualizes trajectories of Artificial Superintelligence (ASI)**.
It integrates narrative foresight, real-world data signals, and transparent model provenance to help researchers, policymakers, and AI safety practitioners **anticipate high-impact futures**.

---

## 🧭 Mission Statement

> *“Transparency and rigor are non-negotiable when modeling futures that matter.”*

OASIS Observatory applies **schema-based foresight modeling** and **multi-agent simulation** to explore the emergence, coordination, and risks of advanced AI systems.
It aims to provide a reproducible, explainable foundation for **superintelligence governance research** and **ethical AI forecasting**.

---

## 🧠 Core Features

* **Structured foresight schema** — JSON-based definitions for ASI scenarios (origin, architecture, alignment, impact).
* **Quantitative + narrative integration** — Combines probability fields with timeline narratives.
* **Model provenance tracking** — Records model identity, parameters, and configuration for every generated scenario.
* **Evidence layer (future)** — Links generated scenarios with precursor signals from real-world data.
* **Open methodology** — Fully open-source and schema-driven for auditability and transparency.

---

## 🧩 System Architecture

OASIS is implemented as a modular Python monorepo:

```
oasis-observatory/
├── data/                          # gitignored runtime databases
│   ├── asi_scenarios.db           # Generated single-ASI scenarios
│   ├── multi_asi_scenarios.db     # Multi-agent ASI interactions
│   └── precursor_signals.db       # Tracker output (real-world precursors)
│
├── common/                        # Shared core utilities
│   ├── __init__.py
│   ├── db.py                      # SQLite helpers
│   ├── logger.py                  # Unified logging setup
│   ├── utils.py                   # Small helper functions
│   ├── validation.py              # JSON Schema + data validation
│   └── schemas/                   # Versioned data contracts
│       ├── asi_scenario.json
│       ├── multi_asi_scenario.json
│       └── signals.json
│
├── generator/                     # PHASE 1 — ASI Scenario Generator (MVP)
│   ├── __init__.py
│   ├── cli.py                     # Entry point: oasis-generator
│   ├── config/                    # Prompts + model settings
│   ├── single_asi_scenario.py     # Logic for one ASI scenario
│   ├── multi_asi_scenario.py      # Multi-agent simulation
│   ├── single_asi_database.py     # SQLite operations
│   ├── multi_asi_database.py      # SQLite operations for multi-ASI
│   ├── parameter_sampler.py       # Randomization and parameter control
│   └── generate_batch.py          # Batch generation script


# TODO
│
├── tracker/                       # PHASE 2 — Real-world Signal Tracker (Q4 2025)
│   ├── __init__.py
│   ├── cli.py                     # Entry point: oasis-tracker
│   ├── config/
│   │   ├── sources.yaml           # Data sources (arXiv, GitHub, news)
│   │   └── keywords.yaml          # Extraction keywords
│   ├── tracker.py                 # Orchestration
│   ├── extractor.py               # Source ingestion
│   ├── signal_parser.py           # Normalization and cleaning
│   ├── signal_classifier.py       # Mapping signals to scenarios
│   └── precursor_database.py      # Writes to precursor_signals.db
│
├── dashboard/                     # PHASE 3 — Visualization & Analytics (Q1 2026)
│   ├── __init__.py
│   ├── app.py                     # Streamlit or FastAPI web app
│   ├── config/
│   │   └── ui_settings.json       # Dashboard settings
│   ├── static/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── logo.svg
│   ├── queries.py                 # SQL → JSON converters
│   ├── analytics.py               # Probability + scenario insights
│   └── api.py                     # REST endpoints (optional)
│
├── docs/                          # Documentation and research context
│   ├── architecture.md
│   ├── methodology.md
│   ├── ethics.md
│   └── roadmap.md
│
├── tests/                         # Unit + integration tests (pytest)
│   ├── conftest.py
│   ├── test_generator.py
│   ├── test_tracker.py
│   ├── test_dashboard.py
│   └── test_utils.py
│
├── scripts/                       # Developer tools
│   ├── validate_schemas.py        # Schema validation CLI
│   ├── migrate_data.py            # DB schema migration helper
│   └── seed_demo_data.py          # Sample data for testing
│
├── demo/                          # Demo assets and screencasts
│   ├── record.mp4
│   └── screenshots/
│
├── .github/workflows/ci.yml       # Continuous Integration (lint + tests)
├── pyproject.toml                 # Build + dependencies (PEP 621)
├── requirements.txt               # Fallback dependency list
├── Makefile                       # Commands: make up, make test, make demo
├── docker-compose.yml             # Reproducible local environment
├── .gitignore                     # Ignore data/, cache/, build/
└── README.md                      # You are here 👋
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/oasis-observatory/oasis-observatory.git
cd oasis-observatory
```

### 2. Install dependencies

Recommended (modern method):

```bash
pip install .
```

or for development:

```bash
pip install -e .
```

Legacy fallback:

```bash
pip install -r requirements.txt
```

### 3. Run the generator (single ASI scenario)

```bash
oasis-generator single
```

Or directly:

```bash
python -m generator.single_asi_scenario
```

### 4. Run with Docker

```bash
docker-compose up
```

This will launch:

* the generator service
* the dashboard (port `8501`)
* an optional local Ollama container for LLM inference

### 5. Run tests

```bash
pytest -v
```

---

## 🧮 Example Workflow

1. **Generate Scenarios**

   ```bash
   make demo
   ```

   Produces narrative and structured ASI scenarios in `data/asi_scenarios.db`.

2. **Track Precursors (Phase 2)**
   Once released, run:

   ```bash
   oasis-tracker run
   ```

   Extracts real-world signals and populates `data/precursor_signals.db`.

3. **Visualize Insights (Phase 3)**

   ```bash
   streamlit run dashboard/app.py
   ```

   Explore ASI trajectories interactively in the dashboard.

---

## 🧬 Data Ethics & Transparency

OASIS Observatory adheres to the following principles:

* **Transparency:** All generated outputs record model, parameters, and date.
* **Provenance:** Every entry in `.db` is schema-validated and auditable.
* **Open Research:** No proprietary data or black-box inference used.
* **Ethical Foresight:** Scenarios are for policy research and education — *not predictions*.

See [`docs/ethics.md`](./docs/ethics.md) for details.

---

## 🧩 Roadmap

| Phase                         | Timeline   | Focus                                   |
| ----------------------------- | ---------- | --------------------------------------- |
| **Phase 1 — Generator (MVP)** | 🚧 2025 Q4 | Scenario generation, schema validation  |
| **Phase 2 — Tracker**         | 🚧 2026 Q1 | Precursor signal extraction and mapping |
| **Phase 3 — Dashboard**       | ⏳ 2026 Q2 | Visualization, analytics, reporting     |

See [`docs/roadmap.md`](./docs/roadmap.md) for full milestones.

---

## 👥 Team

| Role                              | Name                                                                           | Focus                                           |
| --------------------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------- |
| **Founder & Lead Architect**      | [**Mikhail Bukhtoyarov**](https://philpeople.org/profiles/mikhail-bukhtoyarov) | Philosophy of Technology, foresight methodology |
| **Core Contributor (Dev Lead)**   | TBD                                                                            | Software architecture, system design            |
| **Core Contributor (Governance)** | TBD                                                                            | Legal and organizational alignment              |

> Want to contribute or be publicly credited?
> Join [Discussions](https://github.com/oasis-observatory/oasis-observatory/discussions) or open an Issue.

---

## 🛠️ Development Shortcuts (Alpha)

> Only **working commands** are listed. Others are coming in future phases.

| Command       | Description                            | Status |
|---------------|----------------------------------------|--------|
| `make demo`   | Generate sample ASI scenarios          | 🚫 **Not yet** (Phase 2) |
| `make test`   | Run unit tests (Phase 1 only)          | 🚫 **Not yet** (Phase 2) |
| `make clean`  | Remove `data/` and cache               | 🚫 **Not yet** (Phase 2) |
| `make up`     | Launch full stack via Docker Compose   | 🚫 **Not yet** (Phase 3) |

> Run `make` with no args to see available targets.
---

## 📄 License

**MIT License** — open for academic, research, and educational use.

---

## 🌍 Citation

If you use OASIS Observatory in research, please cite:

> Bukhtoyarov, M. (2025). *OASIS Observatory: Open Artificial Superintelligence Scenario Modeling Platform (v0.2)*. GitHub Repository: [https://github.com/oasis-observatory/oasis-observatory](https://github.com/oasis-observatory/oasis-observatory)

---
