from time import time
from syntechrev_polycodcal.feedback_monitor import FeedbackMonitor


def make_event(outcome: str):
    return {"timestamp": time(), "outcome": outcome}


def test_hysteresis_trigger_and_recovery():
    mon = FeedbackMonitor(
        window_seconds=30, threshold=0.5, trigger_threshold=0.6, clear_threshold=0.4
    )
    # Trigger: 3 negative, 2 ok -> rate 0.6
    for o in ["negative", "negative", "negative", "ok", "ok"]:
        mon.ingest(make_event(o))
    alert1 = mon.check()
    assert alert1 is not None
    assert alert1.alert_type == "negative_feedback_spike"
    assert mon._alert_active is True
    assert abs(alert1.metric_value - 0.6) < 1e-9

    # Add 2 ok -> negatives 3 / 7 ≈ 0.4286 still ABOVE clear (0.4) so no recovery
    for o in ["ok", "ok"]:
        mon.ingest(make_event(o))
    assert mon._alert_active is True
    assert mon.check() is None

    # Add one more ok -> negatives 3 / 8 = 0.375 <= 0.4 triggers recovery
    mon.ingest(make_event("ok"))
    recovery_alert = mon.check()
    assert recovery_alert is not None
    assert recovery_alert.alert_type == "negative_feedback_recovery"
    assert mon._alert_active is False
    assert abs(recovery_alert.metric_value - (3 / 8)) < 1e-9


def test_hysteresis_no_retrigger_without_recovery():
    mon = FeedbackMonitor(
        window_seconds=30, threshold=0.5, trigger_threshold=0.6, clear_threshold=0.4
    )
    for o in ["negative", "negative", "negative", "ok", "ok"]:
        mon.ingest(make_event(o))
    assert mon.check() is not None  # initial spike
    # Add one ok -> 3/6 = 0.5 still > clear => no recovery alert and no re-trigger
    mon.ingest(make_event("ok"))
    assert mon.check() is None


def test_invalid_hysteresis_config():
    # clear >= trigger should raise
    import pytest

    with pytest.raises(ValueError):
        FeedbackMonitor(trigger_threshold=0.5, clear_threshold=0.5)
    with pytest.raises(ValueError):
        FeedbackMonitor(trigger_threshold=0.6, clear_threshold=0.7)
