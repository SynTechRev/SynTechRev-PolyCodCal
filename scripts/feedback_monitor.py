"""Simple CLI to run FeedbackMonitor over a JSONL file.

Usage: python scripts/feedback_monitor.py path/to/events.jsonl
"""

import json
import sys
from syntechrev_polycodcal.feedback_monitor import FeedbackMonitor, run_once


def main(path: str) -> int:
    events = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))

    monitor = FeedbackMonitor(window_seconds=60, threshold=0.2)
    alerts = run_once(events, monitor)
    for a in alerts:
        print(a)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: scripts/feedback_monitor.py path/to/events.jsonl")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
