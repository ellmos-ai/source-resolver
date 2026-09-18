from __future__ import annotations

import json
import os
from pathlib import Path

import source_resolver.adapters.bach_tool_registry as bach_adapter
from source_resolver.ladder import Stufe, resolve
from source_resolver.store import UserSourceStore


def _fake_bach_root(tmp_path: Path) -> Path:
    root = tmp_path / "bach"
    (root / "system" / "hub").mkdir(parents=True)
    (root / "bach_api.py").write_text("# test bridge marker\n", encoding="utf-8")
    (root / "system" / "bach_api.py").write_text("# test bridge marker\n", encoding="utf-8")
    (root / "system" / "hub" / "bach_paths.py").write_text("# test bridge marker\n", encoding="utf-8")
    return root


def _completed_process(payload, returncode=0, stderr=""):
    class Process:
        pass

    process = Process()
    process.stdout = json.dumps(payload, ensure_ascii=False)
    process.returncode = returncode
    process.stderr = stderr
    return process


def test_missing_bach_provider_is_explicit(monkeypatch):
    monkeypatch.delenv("SOURCE_RESOLVER_BACH_ROOT", raising=False)
    monkeypatch.delenv("BACH_ROOT", raising=False)
    monkeypatch.setattr(bach_adapter.importlib.util, "find_spec", lambda name: None)

    result = bach_adapter.resolve_bach_tool_registry()

    assert result.status == "not_installed"
    assert "BACH bach_api" in result.message


def test_adapter_uses_read_only_bach_api_bridge(monkeypatch, tmp_path):
    root = _fake_bach_root(tmp_path)
    monkeypatch.setenv("SOURCE_RESOLVER_BACH_ROOT", str(root))
    payload = {
        "status": "resolved",
        "role": "resources.bach.tool_registry",
        "provider": "bach",
        "table": "tool_registry",
        "read_only": True,
        "query": "OCR",
        "items": [{"name": "PDF-OCR", "status": "aktiv"}],
        "count": 1,
    }
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured["kwargs"] = kwargs
        return _completed_process(payload)

    monkeypatch.setattr(bach_adapter.subprocess, "run", fake_run)

    result = bach_adapter.resolve_bach_tool_registry(query="OCR")

    assert result.status == "resolved"
    assert result.payload["read_only"] is True
    assert result.payload["table"] == "tool_registry"
    assert result.payload["items"][0]["name"] == "PDF-OCR"
    assert captured["command"][:2] == [bach_adapter.sys.executable, "-c"]
    assert "tool_registry" in captured["command"][2]
    assert "tool_patterns" not in captured["command"][2]
    assert captured["kwargs"]["cwd"] == str(root)
    assert captured["kwargs"]["env"]["PYTHONPATH"].split(os.pathsep)[0] == str(root)


def test_adapter_rejects_invalid_bridge_output(monkeypatch, tmp_path):
    root = _fake_bach_root(tmp_path)
    monkeypatch.setenv("SOURCE_RESOLVER_BACH_ROOT", str(root))

    class Process:
        stdout = "not json"
        stderr = "bridge failure"
        returncode = 1

    monkeypatch.setattr(bach_adapter.subprocess, "run", lambda *args, **kwargs: Process())

    result = bach_adapter.resolve_bach_tool_registry()

    assert result.status == "adapter_error"
    assert "kein gültiges JSON" in result.message


def test_ladder_resolves_bach_role_at_stage_one(monkeypatch, tmp_path):
    root = _fake_bach_root(tmp_path)
    monkeypatch.setenv("SOURCE_RESOLVER_BACH_ROOT", str(root))
    payload = {
        "status": "resolved",
        "role": "resources.bach.tool_registry",
        "provider": "bach",
        "table": "tool_registry",
        "read_only": True,
        "query": "",
        "items": [],
        "count": 0,
    }
    monkeypatch.setattr(
        bach_adapter.subprocess,
        "run",
        lambda *args, **kwargs: _completed_process(payload),
    )
    store = UserSourceStore(tmp_path / "store.json")

    result = resolve("resources.bach.tool_registry", store=store, home=tmp_path / "home")

    assert result.stufe == Stufe.EIGENES_MODUL
    assert result.status == "resolved"
    assert result.quelle["read_only"] is True
