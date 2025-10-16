"""Feedback monitor implementation used by the tests.

Implements a small in-memory sliding-window aggregator. The API is
kept intentionally simple to make unit tests predictable.
"""

from __future__ import annotations

from collections import deque, Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, Deque, Dict, Iterable, List, Optional


def _to_ts(value) -> float:
    """Normalize timestamp-like values to epoch seconds.

    Accepts None (now), int/float (epoch secs) or ISO date strings.
    """
    if value is None:
        return datetime.now(timezone.utc).timestamp()
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.timestamp()
    raise TypeError("timestamp must be None, int, float, or ISO string")


@dataclass
class Alert:
    alert_type: str
    timestamp: float
    window_seconds: int
    metric_value: float
    threshold: float
    details: Dict


class FeedbackMonitor:
    """Monitor feedback events and emit alerts when thresholds are hit.

    Args:
        window_seconds: aggregation window in seconds.
        threshold: fraction threshold (negative/total) to trigger an alert.
        negative_key: set of outcome values considered 'negative'.
        alert_callback: optional callable(Alert) called when alert emitted.
    """

    def __init__(
        self,
        window_seconds: int = 60,
        threshold: float = 0.2,
        negative_key: Optional[set] = None,
        alert_callback: Optional[Callable[[Alert], None]] = None,
    ) -> None:
        self.window_seconds = int(window_seconds)
        self.threshold = float(threshold)
        self.negative_key = negative_key or {"negative", "error"}
        self.alert_callback = alert_callback

        # store (ts, outcome, source)
        self._buffer: Deque[tuple[float, str, Optional[str]]] = deque()

    def ingest(self, event: Dict) -> None:
        """Ingest a single event dict with 'timestamp' and 'outcome'.

        The event must include an 'outcome' key; raise ValueError otherwise.
        """
        outcome = event.get("outcome")
        if outcome is None:
            raise ValueError("event must include an 'outcome' field")
        ts = _to_ts(event.get("timestamp"))
        source = event.get("source")
        self._buffer.append((ts, outcome, source))
        self._expire_old(ts)

    def _expire_old(self, now_ts: float) -> None:
        cutoff = now_ts - self.window_seconds
        while self._buffer and self._buffer[0][0] < cutoff:
            self._buffer.popleft()

    def summarize(self) -> Dict:
        """Return aggregated metrics for the current window."""
        total = len(self._buffer)
        counts: Counter = Counter()
        sources: Counter = Counter()
        for _ts, outcome, source in self._buffer:
            counts[outcome] += 1
            if source:
                sources[source] += 1

        negative_count = sum(counts.get(k, 0) for k in self.negative_key)
        negative_rate = negative_count / total if total > 0 else 0.0

        return {
            "total": total,
            "counts": dict(counts),
            "negative_count": negative_count,
            "negative_rate": negative_rate,
            "top_sources": sources.most_common(5),
        }

    def check(self) -> Optional[Alert]:
        """Return an Alert if the negative rate meets the threshold."""
        now_ts = datetime.now(timezone.utc).timestamp()
        self._expire_old(now_ts)
        s = self.summarize()
        if s["negative_rate"] >= self.threshold and s["total"] > 0:
            alert = Alert(
                alert_type="negative_feedback_spike",
                timestamp=now_ts,
                window_seconds=self.window_seconds,
                metric_value=s["negative_rate"],
                threshold=self.threshold,
                details={
                    "total": s["total"],
                    "negative_count": s["negative_count"],
                    "counts": s["counts"],
                    "top_sources": s["top_sources"],
                },
            )
            if self.alert_callback:
                try:
                    self.alert_callback(alert)
                except Exception:
                    # don't let callback exceptions break monitoring
                    pass
            return alert
        return None


def run_once(
    stream: Iterable[Dict], monitor: Optional[FeedbackMonitor] = None
) -> List[Alert]:
    """Process a finite stream of events and return alerts emitted."""
    mon = monitor or FeedbackMonitor()
    alerts: List[Alert] = []
    for event in stream:
        mon.ingest(event)
        a = mon.check()
        if a:
            alerts.append(a)
    return alerts


def main() -> int:
    """CLI entry point for feedback monitor.

    Usage: syntech-monitor path/to/events.jsonl
    """
    import json
    import sys

    if len(sys.argv) < 2:
        print("Usage: syntech-monitor path/to/events.jsonl")
        return 2

    path = sys.argv[1]
    events = []
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                events.append(json.loads(line))
    except FileNotFoundError:
        print(f"Error: File not found: {path}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file: {e}", file=sys.stderr)
        return 1

    monitor = FeedbackMonitor(window_seconds=60, threshold=0.2)
    alerts = run_once(events, monitor)
    for a in alerts:
        print(a)
    return 0
