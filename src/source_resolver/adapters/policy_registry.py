"""Adapter fuer die Rolle `policy.registry` -- delegiert an das Modul `policy-registry`
statt eine zweite Richtlinien-Aufloesung zu bauen.

`policy-registry` deklariert in seinem Manifest bereits
`provides: ["policy.registry", "policy.resolve", "policy.discovery"]` und die CLI
liefert exakt den Vertrag, den die Stufenleiter braucht:

    policy-registry resolve --scope <scope> [--query <query>] [--consumer <c>]
                             [--require-kind <k>]

Exit 0 + `status: "resolved"` -> gefunden und massgeblich.
Exit 2 + `status: "missing"|"insufficient"|"conflict"` -> nicht (eindeutig) gefunden,
    ggf. mit `fallback: {"provider": "TOM-lm", "mode": "advisory",
    "automatic_authority": false, ...}` -- diese Advisory-Auskunft wird durchgereicht,
    aber NIE selbst als massgeblich behandelt (automatic_authority bleibt false).

Quelle des Vertrags: `policy_registry/cli.py::main()` und `registry.py::resolve()`
im kanonischen Klon (gelesen 2026-08-15, nicht vermutet) -- die CLI ist auf diesem
Host nicht installiert (`policy-registry` nicht auf PATH), daher wird der Vertrag
hier nachgebildet, aber jeder Aufruf faengt Installations-/Parsing-Fehler explizit
ab, statt sie als "nicht gefunden" zu verschleiern.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from typing import Any


@dataclass
class AdapterResult:
    status: str  # "resolved" | "missing" | "insufficient" | "conflict" | "not_installed" | "adapter_error"
    payload: dict[str, Any] | None
    message: str


def check_callable() -> bool:
    return shutil.which("policy-registry") is not None


def resolve_policy_registry(
    *, scope: str, query: str = "", consumer: str | None = None, require_kind: str | None = None
) -> AdapterResult:
    if not check_callable():
        return AdapterResult(
            status="not_installed",
            payload=None,
            message=(
                "policy-registry ist nicht auf PATH aufrufbar. Modul kann trotzdem vorhanden "
                "sein (Pointer/Manifest in .MODULES/.CONTROL/policy-registry) -- das ist ein "
                "eigener Zustand ('Modul vorhanden, CLI nicht installiert'), keine Abwesenheit."
            ),
        )
    cmd = ["policy-registry", "resolve", "--scope", scope]
    if query:
        cmd += ["--query", query]
    if consumer:
        cmd += ["--consumer", consumer]
    if require_kind:
        cmd += ["--require-kind", require_kind]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired) as error:
        return AdapterResult(
            status="adapter_error",
            payload=None,
            message=f"Aufruf von policy-registry fehlgeschlagen: {error}",
        )
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return AdapterResult(
            status="adapter_error",
            payload=None,
            message=(
                f"policy-registry lieferte kein gueltiges JSON (exit {proc.returncode}). "
                f"stdout={proc.stdout[:200]!r} stderr={proc.stderr[:200]!r}"
            ),
        )
    status = payload.get("status", "adapter_error")
    return AdapterResult(status=status, payload=payload, message=f"policy-registry: {status}")
