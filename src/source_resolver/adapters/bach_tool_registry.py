"""Adapter für BACHs kanonische, read-only ``tool_registry``-Quelle.

Die Rolle wird nicht über eine zweite Datenbankverbindung aufgelöst. Der
Adapter startet einen kurzen Python-Bridge-Aufruf gegen BACHs öffentliche
``bach_api.tool_registry``-Oberfläche. Ist BACH nicht installiert oder nicht
über ``SOURCE_RESOLVER_BACH_ROOT``/``BACH_ROOT`` auffindbar, bleibt der
Befund explizit und fail-closed.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROLE = "resources.bach.tool_registry"
_CONFIGURED_ROOT_VARS = ("SOURCE_RESOLVER_BACH_ROOT", "BACH_ROOT")
_TIMEOUT_SECONDS = 15


@dataclass
class AdapterResult:
    status: str
    payload: dict[str, Any] | None
    message: str


def _valid_root(raw: str | None) -> Path | None:
    if not raw:
        return None
    root = Path(raw).expanduser()
    required = (
        root / "bach_api.py",
        root / "system" / "bach_api.py",
        root / "system" / "hub" / "bach_paths.py",
    )
    return root if all(path.is_file() for path in required) else None


def _configured_root() -> Path | None:
    for variable in _CONFIGURED_ROOT_VARS:
        root = _valid_root(os.environ.get(variable))
        if root is not None:
            return root
    return None


def _installed_api_available() -> bool:
    return importlib.util.find_spec("bach_api") is not None


def check_callable() -> bool:
    """Return whether a BACH API bridge can be started on this host."""
    return _configured_root() is not None or _installed_api_available()


def _bridge_source(query: str) -> str:
    query_literal = json.dumps(query, ensure_ascii=True)
    return f"""import json
from bach_api import tool_registry

try:
    items = tool_registry.list(query={query_literal})
except Exception as error:
    print(json.dumps({{"status": "adapter_error", "error": str(error)}}, ensure_ascii=False))
    raise SystemExit(2)

print(json.dumps({{
    "status": "resolved",
    "role": {ROLE!r},
    "provider": "bach",
    "table": "tool_registry",
    "read_only": True,
    "query": {query_literal},
    "items": items,
    "count": len(items),
}}, ensure_ascii=False, default=str))
"""


def _bridge_environment(root: Path | None) -> dict[str, str]:
    environment = os.environ.copy()
    if root is not None:
        root_text = str(root)
        current = environment.get("PYTHONPATH")
        environment["PYTHONPATH"] = os.pathsep.join(
            value for value in (root_text, current) if value
        )
    return environment


def resolve_bach_tool_registry(*, scope: str | None = None, query: str = "") -> AdapterResult:
    """Resolve active BACH tools through the public API bridge.

    ``scope`` is accepted to satisfy the common resolver adapter contract but
    intentionally has no meaning for this source. BACH filtering is limited to
    a read-only name/path query; ``tool_patterns`` is never queried.
    """
    if not isinstance(query, str):
        return AdapterResult(
            status="adapter_error",
            payload=None,
            message="BACH tool_registry query muss ein String sein.",
        )

    root = _configured_root()
    if root is None and not _installed_api_available():
        configured = ", ".join(_CONFIGURED_ROOT_VARS)
        return AdapterResult(
            status="not_installed",
            payload=None,
            message=(
                "BACH bach_api ist nicht auflösbar. Konfiguriere einen gültigen "
                f"BACH-Root ueber {configured} oder installiere BACH."
            ),
        )

    command = [sys.executable, "-c", _bridge_source(query)]
    try:
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=_TIMEOUT_SECONDS,
            cwd=str(root) if root is not None else None,
            env=_bridge_environment(root),
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return AdapterResult(
            status="adapter_error",
            payload=None,
            message=f"BACH bach_api-Bridge fehlgeschlagen: {error}",
        )

    raw_output = process.stdout.strip()
    try:
        payload = json.loads(raw_output)
    except json.JSONDecodeError:
        return AdapterResult(
            status="adapter_error",
            payload=None,
            message=(
                f"BACH bach_api-Bridge lieferte kein gültiges JSON (exit {process.returncode}). "
                f"stdout={raw_output[:200]!r} stderr={process.stderr[:200]!r}"
            ),
        )

    if not isinstance(payload, dict):
        return AdapterResult(
            status="adapter_error",
            payload=None,
            message="BACH bach_api-Bridge lieferte kein JSON-Objekt.",
        )
    if process.returncode != 0 or payload.get("status") != "resolved":
        return AdapterResult(
            status="adapter_error",
            payload=payload,
            message=f"BACH tool_registry: {payload.get('error', 'unaufgelöst')}",
        )
    if payload.get("read_only") is not True or payload.get("table") != "tool_registry":
        return AdapterResult(
            status="adapter_error",
            payload=payload,
            message="BACH tool_registry-Bridge verletzte den read-only Quellenvertrag.",
        )
    if not isinstance(payload.get("items"), list):
        return AdapterResult(
            status="adapter_error",
            payload=payload,
            message="BACH tool_registry-Bridge lieferte keine Item-Liste.",
        )

    return AdapterResult(
        status="resolved",
        payload=payload,
        message=f"BACH tool_registry aufgelöst ({len(payload['items'])} aktive Einträge).",
    )


__all__ = ["ROLE", "AdapterResult", "check_callable", "resolve_bach_tool_registry"]
