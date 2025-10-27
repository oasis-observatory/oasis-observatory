# Open Artificial Superintelligence Scenario Observatory v0.1 / OASIS Observatory v0.1

This project simulates the development and trajectories of Artificial Superintelligence (ASI) systems by generating narrative scenarios and tracking real-world AI development signals.
---
## Structure

- `oasis_generator/`: Generate and store ASI scenario narratives.
- `oasis_tracker_lite/`: Extract real-world precursors.
- `oasis_dashboard_lite/`: Assess probabilities and map the scenario landscape based on the precursor strengths, generate reports and visualizations.
- `oasis_data/`: SQLite databases used for storage.
---
## Usage

1. Install dependencies:
pip install -r requirements.txt

2. Run a single ASI scenario generation:
python oasis_generator/single_asi_scenario.py

3. Generate a multiple ASI scenarion:
python multi_asi_scenario_/generate_batch.py


## TODO
- [x] Add JSON schema for validation
- [ ] Add more LLM agents for better scenario generation and evaluation
- [ ] Design signal parsers
- [ ] Link scenarios to real-world precursor signals, using multiagent precursor and scenario
- [ ] Develop a probability assessment module


## File Structure
```
oasis_observatory/
├── README.md                            # Project overview, setup instructions, usage
├── requirements.txt                     # Python dependencies for entire project
│
├── oasis_generator/                     # Module: generates narrative scenarios of ASI systems
│   ├── config/
│   │   └── asi_scenario_schema.json     # JSON schema definition for validating scenario structure
│   ├── utils/
│   │   └── abbreviator.py               # Utility to generate shortened ASI scenario titles
│   ├── single_asi_scenario.py           # Main script to generate a single scenario
│   ├── single_asi_batch.py              # Batch scenario generation utility
│   ├── parameter_sampler.py             # Defines how scenario parameters are randomly or manually sampled
│   ├── single_asi_database.py           # Handles SQLite operations for sinle-ASI scenarios storage at asi_scenarios.db
│   ├── single_asi_ollama_client.py      # Connects to local Ollama LLM for single-ASI scenarios
│   ├── multi_asi_scenario.py            # Generator logic for multi-agent (multi-ASI) scenario narratives based on the single-ASI scenarios from asi_scenarios.db
│   ├── multi_asi_database.py            # Handles SQLite operations for multu-ASI scenarios storage at multi_asi_scenarios.db
│   └── ollama_multi_asi_client.py       # Connects to local Ollama LLM for multi-ASI scenarios
```
---
### TODO
```
│
├── main.py                              # (Optional) CLI or central orchestration entry point
├── common/                              # Shared utilities and helpers across all modules
│   └── logger.py                        # Logging setup and wrappers
│
├── oasis_tracker/                       # Module: tracks real-world precursors to ASI emergence
│   ├── config/
│   │   ├── hf_model_list.jsonc          # List of Hugging Face models to monitor
│   │   └── precursor_signal.jsonc       # Signal definitions and keywords for classification
│   ├── extractor.py                     # Orchestrator for extracting and classifying signals
│   ├── parser_A.py                      # Extracts relevant signals
│   ├── parser_B.py                      # Extracts relevant signals
│   ├── precursor_db.py                  # Manages signal storage in SQLite database
│   └── signal_classifier.py             # Classifies project metadata into scenario features
│
├── oasis_dashboard_lite/                # Module: maps and visualizes ASI scenario landscape
│   ├── config/
│   │   └── mapping_weights.json         # Weights and heuristics for mapping scenario axes
│   ├── map_AA.py                        # Maps scenarios in a 2D agency-autonomy space
│   ├── single_asi_safety_analyzer.py    # Generates a report based on the last multi-ASI scenario in the database
│   └── multi_asi_safety_analyzer.py     # Generates a report based on the last multi-ASI scenario in the database
│
├── data/                                # Project-local databases and signal logs
│   ├── asi_scenarios.db                 # DB for generated single-ASI scenarios
│   ├── multi_asi_scenario.db            # DB for multi-ASI interaction scenarios
│   └── precursor_signals.db             # DB for storing tracked precursor signals
│
└── tests/                               # Unit and integration tests (recommended for v0.2+)
    ├── test_extractor.py                # Test cases for signal extraction and parsing
    ├── test_mapper.py                   # Tests for scenario mapping and visualization
    └── test_scenario_generator.py       # Tests for scenario creation and schema validation
```
---

## External Requirements
- Python 3.8+
- Ollama installed and configured locally (used for LLM inference)
- SQLite3
---

## MIT License

---
<!--
**oasis-observatory/OASIS-observatory** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->
