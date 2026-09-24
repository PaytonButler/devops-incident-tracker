from app.incident_rules import is_incident, is_high_latency


def test_error_level_triggers_incident():
    assert is_incident("ERROR") is True


def test_critical_level_triggers_incident():
    assert is_incident("CRITICAL") is True


def test_info_level_does_not_trigger_incident():
    assert is_incident("INFO") is False


def test_warning_level_does_not_trigger_incident():
    assert is_incident("WARNING") is False

from app.incident_rules import is_high_latency


def test_response_time_above_threshold_is_high_latency():
    assert is_high_latency(2001) is True


def test_response_time_at_threshold_is_not_high_latency():
    assert is_high_latency(2000) is False


def test_response_time_below_threshold_is_not_high_latency():
    assert is_high_latency(150) is False