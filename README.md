# digital-twin-analytics-agent

A runnable starter project for a telemetry mining + digital twin workflow using:

- **CrewAI-style orchestration** for deterministic processing
- **AutoGen-style deliberation** for corrective action planning
- **Stubbed framework imports** so the repo runs even when those packages are not installed

## What runs now

This repo runs end-to-end with pure Python stubs:
- telemetry feature extraction
- phase detection
- golden run comparison
- risk assessment
- safety evaluation
- action planning
- audit log generation

When you later install and wire real `crewai` and `autogen`, you can replace the stub behavior without changing the core domain structure.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

## Optional real frameworks

The code uses compatibility wrappers in `framework_stubs.py`.

If you install real frameworks later, update the imports or adapters there and keep the rest of the repo stable.

## Layout

```text
digital_twin_ai_starter/
├── app.py
├── requirements.txt
├── framework_stubs.py
├── config.py
├── domain/
├── crews/
├── autogen_layer/
├── orchestrator/
└── tests/
```
