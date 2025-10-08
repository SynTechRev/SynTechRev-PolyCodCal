import time
from syntechrev_polycodcal.feedback_monitor import FeedbackMonitor


def _make_event(offset_seconds=0, outcome="ok", source=None):
    return {
        "timestamp": time.time() + offset_seconds,
        "outcome": outcome,
        "source": source,
    }


def test_no_alert_below_threshold():
    mon = FeedbackMonitor(window_seconds=10, threshold=0.5)
    for _ in range(5):
        mon.ingest(_make_event(outcome="ok"))
    assert mon.summarize()["negative_rate"] == 0.0
    assert mon.check() is None


def test_alert_at_threshold():
    mon = FeedbackMonitor(window_seconds=10, threshold=0.4)
    # 3 negative, 2 ok => negative rate 0.6
    events = [
        {"timestamp": time.time(), "outcome": "negative"},
        {"timestamp": time.time(), "outcome": "negative"},
        {"timestamp": time.time(), "outcome": "negative"},
        {"timestamp": time.time(), "outcome": "ok"},
        {"timestamp": time.time(), "outcome": "ok"},
    ]
    for e in events:
        mon.ingest(e)

    assert mon.check() is not None


def test_malformed_event_raises():
    mon = FeedbackMonitor()
    try:
        mon.ingest({"timestamp": None})
        assert False, "Expected ValueError for missing outcome"
    except ValueError:
        pass
