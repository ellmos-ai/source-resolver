from pathlib import Path

from source_resolver.pointer_check import check_pointer, resolve_placeholders


def test_resolve_placeholders_substitutes_home(tmp_path):
    result = resolve_placeholders("<HOME>/OneDrive/foo", home=tmp_path)
    assert result == f"{tmp_path}/OneDrive/foo"


def test_resolve_placeholders_leaves_hardcoded_path_untouched():
    raw = "C:\\Users\\User\\OneDrive\\foo"
    assert resolve_placeholders(raw) == raw


def test_check_pointer_reports_existing_target(tmp_path):
    target = tmp_path / "module"
    target.mkdir()
    result = check_pointer("<HOME>/module", home=tmp_path)
    assert result.exists is True
    assert Path(result.resolved_path) == target


def test_check_pointer_reports_missing_target_fail_closed(tmp_path):
    result = check_pointer("<HOME>/does-not-exist", home=tmp_path)
    assert result.exists is False
    assert "existiert nicht" in result.reason


def test_check_pointer_on_known_dead_pointer_case():
    """Regressions-Anker fuer T-20260815-603417673: ein pre-move Pfad ohne
    <HOME>-Platzhalter bleibt hart codiert und wird korrekt als fehlend erkannt,
    wenn er nicht mehr existiert (Verhalten dokumentiert, kein Fixversuch hier)."""
    result = check_pointer("Z:\\this\\path\\should\\never\\exist\\ticket-master")
    assert result.exists is False
