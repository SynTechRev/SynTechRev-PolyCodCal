from datetime import datetime, timezone

import pytest

from syntechrev_polycodcal.feedback_monitor import (
    _to_ts,
    FeedbackMonitor,
    run_once,
    Alert,
)


def test_to_ts_now_and_numeric():
    t0 = _to_ts(None)
    assert isinstance(t0, float)
    assert abs(t0 - datetime.now(timezone.utc).timestamp()) < 5

    assert _to_ts(123.0) == 123.0
    assert _to_ts(123) == 123.0


def test_to_ts_iso_strings():
    iso = "2025-01-01T00:00:00+00:00"
    assert _to_ts(iso) == datetime.fromisoformat(iso).timestamp()

    naive = "2025-01-01T00:00:00"
    # naive parsed as UTC in implementation
    assert (
        _to_ts(naive)
        == datetime.fromisoformat(naive).replace(tzinfo=timezone.utc).timestamp()
    )


def test_to_ts_type_error():
    with pytest.raises(TypeError):
        _to_ts(object())


def test_ingest_missing_outcome_raises():
    mon = FeedbackMonitor()
    with pytest.raises(ValueError):
        mon.ingest({})


def test_summarize_and_top_sources():
    mon = FeedbackMonitor(window_seconds=60)
    now = datetime.now(timezone.utc).timestamp()
    mon.ingest({"timestamp": now - 1, "outcome": "ok", "source": "a"})
    mon.ingest({"timestamp": now - 2, "outcome": "error", "source": "b"})
    s = mon.summarize()
    assert s["total"] == 2
    assert s["counts"]["ok"] == 1
    assert s["counts"]["error"] == 1
    assert s["negative_count"] == 1


def test_check_triggers_alert_and_callback_exception():
    events = [
        {"timestamp": None, "outcome": "error"},
        {"timestamp": None, "outcome": "ok"},
        {"timestamp": None, "outcome": "error"},
    ]

    called = []

    def cb(alert: Alert):
        called.append(alert)
        raise RuntimeError("callback fail")

    mon = FeedbackMonitor(window_seconds=60, threshold=0.3, alert_callback=cb)
    for e in events:
        mon.ingest(e)
    a = mon.check()
    assert a is not None
    # callback exception should not bubble
    assert len(called) == 1


def test_run_once_collects_alerts():
    # construct stream that triggers alerts
    stream = [
        {"timestamp": None, "outcome": "error"},
        {"timestamp": None, "outcome": "error"},
        {"timestamp": None, "outcome": "ok"},
    ]
    alerts = run_once(stream, monitor=FeedbackMonitor(window_seconds=60, threshold=0.5))
    assert isinstance(alerts, list)
    assert len(alerts) >= 1
