"""Stufe 0: der Nutzer-Konfigurationsspeicher.

Der Nutzer ueberschreibt jede automatische Aufloesung -- auch unsere eigenen
kanonischen Module (Stufe 1). Was hier unter `aktiv: true` fuer eine Rolle steht,
ist massgeblich, Punkt. Discovery-Ergebnisse (Stufe 2) landen NIE automatisch
hier -- sie muessen erst per `confirm()` vom Nutzer bestaetigt werden.

Ablage: ~/.source-resolver/config.json (analog zu ~/.policy-registry/registry.json).
Ueberschreibbar per SOURCE_RESOLVER_STORE Umgebungsvariable (fuer Tests / andere Hosts).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_ID = "ellmos.source-resolver.user-config.v1"


def default_store_path() -> Path:
    override = os.environ.get("SOURCE_RESOLVER_STORE")
    if override:
        return Path(override)
    return Path.home() / ".source-resolver" / "config.json"


@dataclass
class RoleEntry:
    """Ein vom Nutzer bestaetigter oder manuell eingetragener Eintrag fuer eine Rolle."""

    rolle: str
    aktiv: bool
    quelle: dict[str, Any]
    stufe: int
    bestaetigt_am: str
    bestaetigt_von: str
    herkunft: str = "manuell"  # "manuell" | "discovery-bestaetigt" | "eigenes-modul-bestaetigt"

    def to_dict(self) -> dict[str, Any]:
        return {
            "rolle": self.rolle,
            "aktiv": self.aktiv,
            "quelle": self.quelle,
            "stufe": self.stufe,
            "bestaetigt_am": self.bestaetigt_am,
            "bestaetigt_von": self.bestaetigt_von,
            "herkunft": self.herkunft,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "RoleEntry":
        return RoleEntry(
            rolle=data["rolle"],
            aktiv=bool(data.get("aktiv", True)),
            quelle=data.get("quelle", {}),
            stufe=int(data.get("stufe", 0)),
            bestaetigt_am=data.get("bestaetigt_am", ""),
            bestaetigt_von=data.get("bestaetigt_von", "user"),
            herkunft=data.get("herkunft", "manuell"),
        )


class UserSourceStore:
    """Lesend/schreibend gegen die Stufe-0-Datei. Kein Cache -- jede Operation liest neu,
    Konfigurationsdateien dieser Groessenordnung rechtfertigen keine Cache-Invalidierungslogik."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or default_store_path()

    def _read_raw(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"schema": SCHEMA_ID, "version": 1, "rollen": {}}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(
                f"Stufe-0-Speicher ist beschaedigt (kein gueltiges JSON): {self.path} -- {error}"
            ) from error

    def _write_raw(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def get(self, rolle: str) -> RoleEntry | None:
        raw = self._read_raw()
        entry = raw.get("rollen", {}).get(rolle)
        if entry is None:
            return None
        return RoleEntry.from_dict(entry)

    def list_roles(self) -> dict[str, RoleEntry]:
        raw = self._read_raw()
        return {name: RoleEntry.from_dict(data) for name, data in raw.get("rollen", {}).items()}

    def set(self, entry: RoleEntry) -> None:
        raw = self._read_raw()
        raw.setdefault("rollen", {})[entry.rolle] = entry.to_dict()
        raw["schema"] = SCHEMA_ID
        raw["version"] = raw.get("version", 1)
        self._write_raw(raw)

    def deactivate(self, rolle: str) -> bool:
        """Setzt aktiv=false statt zu loeschen -- die Entscheidung 'Nutzer hat das abgewaehlt'
        bleibt sichtbar, statt wie ein 'nie konfiguriert' auszusehen."""
        raw = self._read_raw()
        entry = raw.get("rollen", {}).get(rolle)
        if entry is None:
            return False
        entry["aktiv"] = False
        self._write_raw(raw)
        return True


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
