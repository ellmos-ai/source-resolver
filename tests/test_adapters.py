import json
import subprocess

import source_resolver.adapters.policy_registry as pr_adapter


def test_check_callable_false_when_not_on_path(monkeypatch):
    monkeypatch.setattr(pr_adapter.shutil, "which", lambda name: None)
    assert pr_adapter.check_callable() is False


def test_resolve_returns_not_installed_when_missing(monkeypatch):
    monkeypatch.setattr(pr_adapter.shutil, "which", lambda name: None)
    result = pr_adapter.resolve_policy_registry(scope="dev-hygiene")
    assert result.status == "not_installed"
    assert "nicht auf PATH" in result.message


def _fake_run(stdout_payload, returncode):
    def _run(cmd, capture_output, text, timeout):
        class Proc:
            pass
        p = Proc()
        p.stdout = json.dumps(stdout_payload)
        p.stderr = ""
        p.returncode = returncode
        return p
    return _run


def test_resolve_maps_resolved_status(monkeypatch):
    monkeypatch.setattr(pr_adapter.shutil, "which", lambda name: "/usr/bin/policy-registry")
    payload = {"status": "resolved", "selected": {"id": "P-001"}, "candidates": [], "reason": None, "fallback": None}
    monkeypatch.setattr(pr_adapter.subprocess, "run", _fake_run(payload, 0))
    result = pr_adapter.resolve_policy_registry(scope="dev-hygiene")
    assert result.status == "resolved"
    assert result.payload["selected"]["id"] == "P-001"


def test_resolve_maps_missing_status_with_advisory_fallback(monkeypatch):
    monkeypatch.setattr(pr_adapter.shutil, "which", lambda name: "/usr/bin/policy-registry")
    payload = {
        "status": "missing",
        "selected": None,
        "candidates": [],
        "reason": "Keine gueltige, explizit adoptierte Norm gefunden.",
        "fallback": {
            "provider": "TOM-lm",
            "mode": "advisory",
            "automatic_authority": False,
            "result_role": "evidence-or-decision-candidate",
            "general_policy_requires_explicit_adoption": True,
        },
    }
    monkeypatch.setattr(pr_adapter.subprocess, "run", _fake_run(payload, 2))
    result = pr_adapter.resolve_policy_registry(scope="dev-hygiene")
    assert result.status == "missing"
    # automatic_authority bleibt False -- der Adapter darf das nicht "aufwerten"
    assert result.payload["fallback"]["automatic_authority"] is False


def test_resolve_handles_invalid_json_as_adapter_error(monkeypatch):
    monkeypatch.setattr(pr_adapter.shutil, "which", lambda name: "/usr/bin/policy-registry")

    def _run(cmd, capture_output, text, timeout):
        class Proc:
            stdout = "not json"
            stderr = ""
            returncode = 1
        return Proc()

    monkeypatch.setattr(pr_adapter.subprocess, "run", _run)
    result = pr_adapter.resolve_policy_registry(scope="dev-hygiene")
    assert result.status == "adapter_error"


def test_resolve_handles_missing_executable_as_adapter_error(monkeypatch):
    monkeypatch.setattr(pr_adapter.shutil, "which", lambda name: "/usr/bin/policy-registry")

    def _run(cmd, capture_output, text, timeout):
        raise FileNotFoundError("no such file")

    monkeypatch.setattr(pr_adapter.subprocess, "run", _run)
    result = pr_adapter.resolve_policy_registry(scope="dev-hygiene")
    assert result.status == "adapter_error"
    assert "fehlgeschlagen" in result.message
