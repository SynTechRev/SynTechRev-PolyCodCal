# SynTechRev-PolyCodCal
Polymathic CodCal

## Quick start

Set up the workspace virtual environment (we use `.venv`):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r dev-requirements.txt
```

Run tests:

```powershell
pytest -q
```

Run pre-commit hooks locally:

```powershell
.venv\Scripts\pre-commit run --all-files
```

## FeedbackMonitor usage

The repository includes a small `FeedbackMonitor` utility in `src/syntechrev_polycodcal/feedback_monitor.py`.

Example (programmatic):

```python
from syntechrev_polycodcal.feedback_monitor import FeedbackMonitor

mon = FeedbackMonitor(window_seconds=60, threshold=0.2)
mon.ingest({"timestamp": None, "outcome": "ok"})
alert = mon.check()
if alert:
	print("Alert:", alert)
```

CLI example (one-off processing of newline-delimited JSON):

```powershell
python scripts\feedback_monitor.py examples\events.jsonl
```


