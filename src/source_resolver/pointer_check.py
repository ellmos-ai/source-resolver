"""Wiederverwendbare Existenzpruefung fuer `type: pointer`-Skills.

Ausgangsbefund (2026-08-15, Ticket T-20260815-603417673): der Pointer in
`ticket-master/SKILL.md` zeigte drei Wochen lang ins Leere, weil `module_path` beim
Umzug des Moduls nicht nachgezogen wurde -- und das fiel nur zufaellig auf. Diese
Funktion ist der reusable Baustein fuer die dort geforderte Pruefung: sie loest die
`<HOME>`-Platzhalterkonvention auf und meldet fail-closed, wenn das Ziel fehlt.

Wird von der Stufenleiter (ladder.py) fuer Rollenquellen vom Typ "pointer" genutzt,
ist aber bewusst eigenstaendig nutzbar -- z.B. von catalog.py oder skill_tester.py,
falls das Nachziehen dieses Checks dort in einem eigenen Ticket erfolgt.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class PointerCheckResult:
    raw_path: str
    resolved_path: str
    exists: bool
    reason: str


def resolve_placeholders(raw_path: str, *, home: Path | None = None) -> str:
    """Loest `<HOME>` (und den literalen Nutzernamen als Altlast-Fallback) auf.

    Pointer-Skills, die vor der Platzhalterkonvention geschrieben wurden, tragen
    noch host-spezifische absolute Pfade (`C:\\Users\\User\\...`). Diese Funktion
    normalisiert NICHT rueckwirkend -- sie loest nur `<HOME>` auf, wenn vorhanden.
    Ein hart codierter Fremdpfad bleibt hart codiert und wird als solcher (mutmasslich
    falsch auf anderen Hosts) sichtbar, statt stillschweigend "repariert" zu werden.
    """
    home = home or Path.home()
    return raw_path.replace("<HOME>", str(home))


def check_pointer(raw_module_path: str, *, home: Path | None = None) -> PointerCheckResult:
    """Prueft, ob ein `pointer.module_path` nach Platzhalter-Aufloesung existiert.

    Fail-closed im Sinn des Aufrufers: der Rueckgabewert macht die Nichtexistenz
    explizit (`exists=False` + `reason`), statt sie zu verschlucken. Was der Aufrufer
    daraus macht (Exit 1, Warnung, Stufe-Herabstufung), entscheidet der Aufrufer.
    """
    resolved = resolve_placeholders(raw_module_path, home=home)
    path = Path(resolved)
    exists = path.exists()
    reason = "gefunden" if exists else "Pfad existiert nicht (nach Platzhalter-Aufloesung geprueft)"
    return PointerCheckResult(
        raw_path=raw_module_path, resolved_path=resolved, exists=exists, reason=reason
    )
