# FaultGuard-G1 documentation

Source of the technical documentation site for FaultGuard-G1, a dependable, extensible, real-time diagnostic system for a Unitree G1 humanoid (Software Engineering for Automation project, Politecnico di Milano).

**Site:** https://relo02.github.io/faultguard-g1-docs/

The site runs from the high-level objectives down to the low-level architecture, and ends with the step-by-step plan for building the system.

## Read the documentation

To read the documentation, open the [published site](https://relo02.github.io/faultguard-g1-docs/). You don't need to install anything.

## Run the site on your laptop

Run a local copy to read the documentation offline, or to preview changes before pushing them. You need [Git](https://git-scm.com/downloads) and [Python](https://www.python.org/downloads/) 3.10 or later.

**1. Download the repository**

```bash
git clone https://github.com/Relo02/faultguard-g1-docs.git
cd faultguard-g1-docs
```

**2. Create a virtual environment and install the dependencies** (first time only)

Linux and macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-docs.txt
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-docs.txt
```

**3. Start the site**

```bash
mkdocs serve
```

Open <http://127.0.0.1:8000> in your browser. The page reloads each time you save a file. Press `Ctrl+C` in the terminal to stop the server.

**Next time**, go to the `faultguard-g1-docs` folder, activate the environment again (`source .venv/bin/activate`, or `.venv\Scripts\Activate.ps1` on Windows), and run `mkdocs serve`.

Diagrams load their rendering library from the internet, so they need a connection to display, even in a local copy. The text works offline.

### Troubleshooting

| Problem | Fix |
|---|---|
| `mkdocs: command not found` | The environment is not active. Run the activate command from step 2. |
| `ensurepip is not available` on Debian or Ubuntu | Run `sudo apt install python3-venv`, delete the `.venv` folder, and repeat step 2. |
| `Address already in use` | Port 8000 is taken. Run `mkdocs serve -a 127.0.0.1:8001` and open that address instead. |
| PowerShell refuses to run `Activate.ps1` | Run `Set-ExecutionPolicy -Scope Process RemoteSigned`, then activate again. |

## Change the documentation

Pages are Markdown files in `docs/`, and the menu is defined under `nav` in `mkdocs.yml`. Before pushing, run the same checks as CI:

```bash
python tools/check_traceability.py   # every requirement must be traced
mkdocs build --strict                # broken links and anchors fail the build
```

Each push to `main` is checked and then deployed to the published site by `.github/workflows/docs.yml`.

## Tools

| Script | Purpose |
|---|---|
| `tools/dataset_probe.py` | Measures the dataset properties the design relies on; the numbers on the *Telemetry data* page come from it. Needs `numpy` and `pyarrow`. |
| `tools/check_traceability.py` | Fails if a requirement is missing from the traceability page, and reports goal-mapping gaps. Standard library only. |

## Source of truth

The formal deliverables (RASD, Design Document) remain authoritative and are kept in the team's private repository. Pages marked *Proposed* on this site are design input for review, not agreed decisions.
