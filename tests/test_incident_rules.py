from app.incident_rules import is_incident


def test_error_level_triggers_incident():
    assert is_incident("ERROR") is True


def test_critical_level_triggers_incident():
    assert is_incident("CRITICAL") is True


def test_info_level_does_not_trigger_incident():
    assert is_incident("INFO") is False


def test_warning_level_does_not_trigger_incident():
    assert is_incident("WARNING") is False