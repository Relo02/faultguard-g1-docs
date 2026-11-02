# FaultGuard-G1 documentation

Source of the technical documentation site for FaultGuard-G1, a dependable, extensible, real-time diagnostic system for a Unitree G1 humanoid (Software Engineering for Automation project, Politecnico di Milano).

**Site:** https://relo02.github.io/faultguard-g1-docs/

The site runs from the high-level objectives down to the low-level architecture, and ends with the step-by-step plan for building the system.

## Build locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-docs.txt
python tools/check_traceability.py   # every requirement ID must be traced
mkdocs serve                         # http://127.0.0.1:8000
```

Each push to `main` is checked and deployed to GitHub Pages by `.github/workflows/docs.yml`.

## Tools

| Script | Purpose |
|---|---|
| `tools/dataset_probe.py` | Measures the dataset properties the design relies on; the numbers on the *Telemetry data* page come from it. Needs `numpy` and `pyarrow`. |
| `tools/check_traceability.py` | Fails if a requirement is missing from the traceability page, and reports goal-mapping gaps. Standard library only. |

## Source of truth

The formal deliverables (RASD, Design Document) remain authoritative and are kept in the team's private repository. Pages marked *Proposed* on this site are design input for review, not agreed decisions.
