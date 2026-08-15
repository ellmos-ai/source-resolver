"""Die Stufenleiter: EINE Komponente fuer die Quellenaufloesung, die Skills aufrufen --
statt dass jeder Skill sie fuer sich kopiert (Nachtrag 2 des Tickets: die Stufenordnung
ist VERHALTEN, nicht FORM, und gehoert deshalb nicht als Copy-Paste-Vorlage verteilt).

Reihenfolge (korrigiert durch Nachtrag 1 des Tickets -- der Nutzer steht ueber allem,
auch ueber unseren eigenen kanonischen Modulen):

  Stufe 0  Nutzer-Konfiguration (`~/.source-resolver/config.json`, `aktiv: true`).
           Gewinnt IMMER, auch gegen ein vorhandenes eigenes Modul.
  Stufe 1  Eigene kanonische Module (KNOWN_MODULE_PROVIDERS / registrierte Adapter).
           Bei Fund automatisch massgeblich -- keine Rueckfrage noetig, das IST unser
           Standardweg. Fuer Rollen mit Adapter (aktuell: policy.registry) delegiert
           diese Stufe vollstaendig an das fremde Modul, statt selbst zu pruefen.
  Stufe 2  Discovery im Dateisystem (konfigurierte Wurzeln). Ergebnisse sind
           VORSCHLAEGE -- werden NIE automatisch uebernommen, sondern muessen per
           `confirm()` vom Nutzer bestaetigt werden, bevor sie Stufe 0 werden.
  Stufe 3  Registrierte Fremdanbieter (aktuell: keine -- siehe README, bewusster
           Schnitt). Jedes Ergebnis traegt "fremd, ungeprueft".
  Stufe 4  Nichts gefunden. Kein Report, sondern ein zweiteiliger Dialog: (a) den
           Nutzer nach dem kanonischen Ort fragen, (b) falls unbekannt, unsere
           Zusatzmodule als Angebot nennen (Datenkaskade-Muster, siehe .AI/CLAUDE.md
           "Software als Speicherpunkt und GUI").
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Any

from source_resolver.adapters import ADAPTERS
from source_resolver.store import RoleEntry, UserSourceStore, now_iso


class Stufe(IntEnum):
    NUTZER_KONFIGURATION = 0
    EIGENES_MODUL = 1
    DISCOVERY_VORSCHLAG = 2
    FREMDANBIETER = 3
    NICHT_GEFUNDEN = 4


class ResolutionStatus:
    RESOLVED = "resolved"
    PROPOSED = "proposed"
    MODULE_PRESENT_NOT_CALLABLE = "module_present_not_callable"
    NO_FOREIGN_PROVIDERS = "no_foreign_providers"
    NOT_FOUND = "not_found"
    ADAPTER_ERROR = "adapter_error"


@dataclass
class ResolutionResult:
    rolle: str
    stufe: Stufe
    status: str
    quelle: dict[str, Any] | None
    herkunft: str
    nachricht: str
    kandidaten: list[dict[str, Any]] = field(default_factory=list)
    dialog: dict[str, Any] | None = None  # nur bei Stufe 4 gefuellt

    def to_dict(self) -> dict[str, Any]:
        return {
            "rolle": self.rolle,
            "stufe": int(self.stufe),
            "stufe_name": self.stufe.name,
            "status": self.status,
            "quelle": self.quelle,
            "herkunft": self.herkunft,
            "nachricht": self.nachricht,
            "kandidaten": self.kandidaten,
            "dialog": self.dialog,
        }


# Stufe 1 -- unsere eigenen kanonischen Module je Rolle. `<HOME>` wird zur Laufzeit
# aufgeloest (dieselbe Konvention wie beim Pointer-Fix, siehe pointer_check.py).
KNOWN_MODULE_PROVIDERS: dict[str, list[dict[str, Any]]] = {
    "policy.registry": [
        {
            "id": "policy-registry",
            "module_path": "<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.CONTROL/policy-registry",
            "adapter": "policy.registry",
        }
    ],
    "decisions.ledger": [
        {
            "id": "_DECISIONS-chain",
            "module_path": "<HOME>/OneDrive/.TOPICS/_control-center/_DECISIONS",
            "target": "<HOME>/OneDrive/.TOPICS/_control-center/_DECISIONS/TO-DECIDE-USER.txt",
            "hinweis": (
                "Zentraler Entscheidungsregister-Einstieg (TO-DECIDE-USER*.txt-Kette, "
                "DECIDED-AND-DONE.md). Host-spezifische Varianten (TO-DECIDE-USER-<HOST>.txt) "
                "moeglich -- Aufrufer sollte alle TO-DECIDE-USER*.txt im Ordner beruecksichtigen."
            ),
        }
    ],
    "user.model": [
        {
            "id": "tom-lm",
            "module_path": "<HOME>/OneDrive/.TOPICS/_control-center/_TOM-lm",
            "target": "<HOME>/OneDrive/.TOPICS/_control-center/_TOM-lm/avatar/START.md",
            "hinweis": (
                "Entscheidungs-Avatar-Loop (Theory of Mind ueber Lukas' Entscheidungen). "
                "Nutzungs-Einwilligung ist NICHT Teil dieser Aufloesung -- das bleibt beim "
                "aufrufenden Skill (Consent-Regel aus tom-lm/decision-avatar: 'blosse "
                "Erreichbarkeit einer Profildatei ist keine Einwilligung')."
            ),
        }
    ],
}


# Stufe 3 -- Fremdanbieter-Interface. Jeder Eintrag ist ein Callable(rolle, query)
# -> dict|None. Bewusst LEER (advisor-Review 2026-08-15: ein halb funktionierender
# Fremdanbieter erzeugt Vertrauen, das er nicht verdient hat -- Ehrliches "keine
# Fremdanbieter konfiguriert" ist im Sinn von Stufe 4 richtiger als ein Beispiel-Stub).
# Registrierung fuer spaeter: FOREIGN_PROVIDERS.append(mein_provider).
FOREIGN_PROVIDERS: list[Any] = []


def _resolve_home_path(raw: str, home: Path) -> Path:
    return Path(raw.replace("<HOME>", str(home)))


def _try_known_module(rolle: str, home: Path) -> ResolutionResult | None:
    for candidate in KNOWN_MODULE_PROVIDERS.get(rolle, []):
        adapter_name = candidate.get("adapter")
        if adapter_name and adapter_name in ADAPTERS:
            # Rolle hat einen Adapter -- das fremde Modul IST die Aufloesung fuer diese
            # Rolle, nicht bloss ein Vorhandensein-Check. Siehe adapters/policy_registry.py.
            continue  # wird vom Aufrufer separat behandelt (braucht scope/query)
        module_path = _resolve_home_path(candidate["module_path"], home)
        if not module_path.exists():
            continue
        target = candidate.get("target")
        if target is not None:
            target_path = _resolve_home_path(target, home)
            if not target_path.exists():
                # Modul-Ordner da, aber die konkrete Zieldatei fehlt -- genau die Klasse
                # Fehler aus T-20260815-603417673 (toter Pointer). Nicht als "gefunden" melden.
                return ResolutionResult(
                    rolle=rolle,
                    stufe=Stufe.EIGENES_MODUL,
                    status=ResolutionStatus.MODULE_PRESENT_NOT_CALLABLE,
                    quelle={"id": candidate["id"], "module_path": str(module_path)},
                    herkunft="eigenes-modul",
                    nachricht=(
                        f"Modul '{candidate['id']}' vorhanden, aber Zieldatei fehlt: "
                        f"{target_path} (Pointer-Drift? siehe pointer_check.check_pointer)."
                    ),
                )
        return ResolutionResult(
            rolle=rolle,
            stufe=Stufe.EIGENES_MODUL,
            status=ResolutionStatus.RESOLVED,
            quelle={
                "id": candidate["id"],
                "module_path": str(module_path),
                "target": str(_resolve_home_path(target, home)) if target else None,
                "hinweis": candidate.get("hinweis", ""),
            },
            herkunft="eigenes-modul",
            nachricht=f"Rolle '{rolle}' aufgeloest ueber eigenes Modul '{candidate['id']}'.",
        )
    return None


def _try_adapter(rolle: str, *, scope: str | None, query: str) -> ResolutionResult | None:
    adapter = ADAPTERS.get(rolle)
    if adapter is None:
        return None
    if scope is None:
        return ResolutionResult(
            rolle=rolle,
            stufe=Stufe.EIGENES_MODUL,
            status=ResolutionStatus.ADAPTER_ERROR,
            quelle=None,
            herkunft="adapter",
            nachricht=(
                f"Rolle '{rolle}' hat einen Adapter, der 'scope' braucht "
                f"(z.B. resolve(rolle='policy.registry', scope='dev-hygiene'))."
            ),
        )
    result = adapter(scope=scope, query=query)
    status_map = {
        "resolved": ResolutionStatus.RESOLVED,
        "not_installed": ResolutionStatus.MODULE_PRESENT_NOT_CALLABLE,
        "adapter_error": ResolutionStatus.ADAPTER_ERROR,
    }
    status = status_map.get(result.status, ResolutionStatus.NOT_FOUND)
    return ResolutionResult(
        rolle=rolle,
        stufe=Stufe.EIGENES_MODUL,
        status=status,
        quelle=result.payload,
        herkunft="adapter:policy-registry",
        nachricht=result.message,
    )


def discover(rolle: str, roots: list[Path], *, max_depth: int = 2) -> list[dict[str, Any]]:
    """Stufe 2: begrenzte Dateisystem-Discovery in EXPLIZIT uebergebenen Wurzeln.

    Bewusst NICHT rekursiv unbegrenzt und NICHT selbststaendig OneDrive-weit suchend --
    das ist Aufgabe von ellmos-filecommander (fc_search_files), nicht dieser Bibliothek
    (siehe CLAUDE.md: Glob/find timeouten auf grossen OneDrive-Baeumen). Der Aufrufer
    liefert sinnvoll eingegrenzte Wurzeln.
    """
    terms = [part.lower() for part in rolle.split(".") if part]
    found: list[dict[str, Any]] = []
    for root in roots:
        if not root.exists():
            continue
        for depth_path in _walk_bounded(root, max_depth):
            name_lower = depth_path.name.lower()
            if any(term in name_lower for term in terms):
                found.append({"pfad": str(depth_path), "gefundene_begriffe": terms})
    return found


def _walk_bounded(root: Path, max_depth: int):
    stack = [(root, 0)]
    while stack:
        current, depth = stack.pop()
        try:
            entries = list(current.iterdir())
        except (PermissionError, OSError):
            continue
        for entry in entries:
            yield entry
            if entry.is_dir() and depth < max_depth:
                stack.append((entry, depth + 1))


def resolve(
    rolle: str,
    *,
    scope: str | None = None,
    query: str = "",
    discovery_roots: list[Path] | None = None,
    store: UserSourceStore | None = None,
    home: Path | None = None,
) -> ResolutionResult:
    """Loest eine Rolle nach der Stufenleiter auf. Nie eine Ausnahme fuer 'nicht
    gefunden' -- das ist Stufe 4 und ein gueltiges, dialogfaehiges Ergebnis, kein Fehler."""
    store = store or UserSourceStore()
    home = home or Path.home()

    # Stufe 0
    entry = store.get(rolle)
    if entry is not None and entry.aktiv:
        return ResolutionResult(
            rolle=rolle,
            stufe=Stufe.NUTZER_KONFIGURATION,
            status=ResolutionStatus.RESOLVED,
            quelle=entry.quelle,
            herkunft=entry.herkunft,
            nachricht=(
                f"Rolle '{rolle}' durch Nutzerkonfiguration festgelegt "
                f"(bestaetigt {entry.bestaetigt_am} von {entry.bestaetigt_von}). "
                f"Ueberschreibt jedes eigene Modul."
            ),
        )

    # Stufe 1 -- zuerst Adapter (falls Rolle einen hat), sonst bekannte Module.
    # Grundsatz: JEDER nicht-None Stufe-1-Befund wird SOFORT zurueckgegeben, auch wenn
    # er kein voller Erfolg ist (Modul nicht installiert, Zieldatei fehlt/Pointer-Drift,
    # Aufrufer-Fehler wie fehlender scope). Das sind eigene, spezifische Ergebnisse --
    # sie in einem generischen "nichts gefunden"-Dialog zu verstecken waere genau die
    # stille Irrefuehrung, die dieses Ticket vermeiden soll (advisor-Review 2026-08-15:
    # "treat 'module present but not callable' as a distinct result rather than
    # silently falling to Stufe 2"). Nur ECHTE Abwesenheit (module_fallback is None)
    # faellt weiter durch die Leiter.
    if rolle in ADAPTERS:
        module_fallback = _try_adapter(rolle, scope=scope, query=query)
    else:
        module_fallback = _try_known_module(rolle, home)
    if module_fallback is not None:
        return module_fallback

    # Stufe 2 -- Discovery, nur wenn Wurzeln uebergeben wurden
    if discovery_roots:
        kandidaten = discover(rolle, discovery_roots)
        if kandidaten:
            return ResolutionResult(
                rolle=rolle,
                stufe=Stufe.DISCOVERY_VORSCHLAG,
                status=ResolutionStatus.PROPOSED,
                quelle=None,
                herkunft="discovery",
                nachricht=(
                    f"{len(kandidaten)} Kandidat(en) fuer Rolle '{rolle}' gefunden. "
                    f"Das ist ein VORSCHLAG -- bitte per confirm() bestaetigen, bevor er "
                    f"kanonisch wird."
                ),
                kandidaten=kandidaten,
            )

    # Stufe 3 -- Fremdanbieter. Interface existiert (siehe FOREIGN_PROVIDERS unten),
    # Liste ist bewusst leer -- siehe README, Abschnitt "Was hier fehlt". Ein Ergebnis
    # von hier muesste "fremd, ungeprueft" tragen; da FOREIGN_PROVIDERS leer ist,
    # wird dieser Zweig nie mit einem Treffer erreicht.
    for provider in FOREIGN_PROVIDERS:  # pragma: no cover -- keine Provider registriert
        kandidat = provider(rolle, query)
        if kandidat is not None:
            kandidat.setdefault("herkunft_hinweis", "fremd, ungeprueft")
            return ResolutionResult(
                rolle=rolle,
                stufe=Stufe.FREMDANBIETER,
                status=ResolutionStatus.PROPOSED,
                quelle=None,
                herkunft="fremdanbieter",
                nachricht=f"Fremdanbieter-Treffer fuer '{rolle}' -- fremd, ungeprueft.",
                kandidaten=[kandidat],
            )

    # Stufe 4 -- nichts gefunden (module_fallback ist an dieser Stelle immer None,
    # siehe Stufe-1-Kurzschluss oben). Dialog statt Report.
    known_ids = [c["id"] for c in KNOWN_MODULE_PROVIDERS.get(rolle, [])]
    dialog = {
        "frage_1": (
            f"Fuer die Rolle '{rolle}' wurde nichts gefunden. Welcher Ort/welche Datei/welches "
            f"Werkzeug ist fuer dich hier massgeblich? (Antwort wird per confirm() als "
            f"Stufe 0 gespeichert und ueberschreibt alles Weitere.)"
        ),
        "frage_2_falls_unbekannt": (
            "Falls du das nicht benennen kannst: sollen wir dir dafuer ein eigenes "
            "Zusatzmodul einrichten? " + (
                f"Kandidat(en) dafuer: {', '.join(known_ids)}." if known_ids else
                "Fuer diese Rolle existiert noch kein passendes Modul -- das waere ein Neubau."
            )
        ),
    }
    return ResolutionResult(
        rolle=rolle,
        stufe=Stufe.NICHT_GEFUNDEN,
        status=ResolutionStatus.NOT_FOUND,
        quelle=None,
        herkunft="keine",
        nachricht=f"Rolle '{rolle}' konnte auf keiner Stufe aufgeloest werden.",
        dialog=dialog,
    )


def confirm(
    rolle: str,
    quelle: dict[str, Any],
    *,
    stufe_herkunft: int,
    bestaetigt_von: str = "user",
    store: UserSourceStore | None = None,
) -> RoleEntry:
    """Hebt ein Stufe-2/3-Ergebnis (oder eine manuelle Angabe) auf Stufe 0.

    Ab hier ist die Wahl kanonisch fuer diesen Nutzer und ueberschreibt jede
    zukuenftige automatische Aufloesung -- exakt das, was Nachtrag 1 des Tickets
    verlangt: Discovery ist ein Vorschlag, keine Festlegung."""
    store = store or UserSourceStore()
    herkunft = {
        0: "manuell",
        1: "eigenes-modul-bestaetigt",
        2: "discovery-bestaetigt",
        3: "fremdanbieter-bestaetigt",
    }.get(stufe_herkunft, "manuell")
    entry = RoleEntry(
        rolle=rolle,
        aktiv=True,
        quelle=quelle,
        stufe=0,
        bestaetigt_am=now_iso(),
        bestaetigt_von=bestaetigt_von,
        herkunft=herkunft,
    )
    store.set(entry)
    return entry
