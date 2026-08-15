# source-resolver

> Rollenbasierte Quellenaufloesung fuer Skills: statt jede Informationsquelle (Policy,
> Entscheidung, Nutzermodell, ...) hart zu verdrahten, ruft ein Skill eine Rolle auf --
> `source_resolver.resolve("decisions.ledger")` -- und bekommt zurueck, WO das fuer
> diesen Nutzer, auf diesem System, gerade herkommt.

**Nicht zu verwechseln mit** `.MODULES/.CONNECTORS/connectors` (Messaging-Kanaele wie
Telegram/Discord). source-resolver verbindet Skills mit Informationsquellen, nicht mit
Kommunikationskanaelen -- getrennter Name, getrennter Zweck.

## Warum

Am 15.08.2026 traten am selben Tag drei Vorfaelle derselben Fehlerklasse auf: ein
Werkzeug legte still einen falschen Ordner an, ein Skript schrieb still "0 Skills"
statt zu scheitern, und ein Pointer-Skill zeigte seit drei Wochen unbemerkt ins Leere.
Gemeinsamer Nenner: ein stiller Fehlschlag, der wie ein gueltiger Zustand aussieht.

Skills, die ihre Quellen hart verdrahten, haben genau dieses Risiko eingebaut -- zieht
ein Modul um oder aendert sich sein Pfad, merkt das niemand, bis ein Agent ins Leere
laeuft. source-resolver macht die Aufloesung explizit, gestuft und pruefbar.

## Die Stufenleiter

| Stufe | Name | Bedeutung |
|---|---|---|
| 0 | Nutzer-Konfiguration | `~/.source-resolver/config.json`, `aktiv: true`. Gewinnt IMMER -- auch gegen ein vorhandenes, funktionierendes eigenes Modul. |
| 1 | Eigenes Modul | Unsere kanonischen Module (siehe `KNOWN_MODULE_PROVIDERS` in `ladder.py`). Bei Fund automatisch massgeblich, keine Rueckfrage noetig. Fuer Rollen mit registriertem Adapter (aktuell: `policy.registry`) delegiert diese Stufe vollstaendig an das fremde Modul. |
| 2 | Discovery-Vorschlag | Dateisystem-Suche in explizit uebergebenen Wurzeln. Ergebnis ist ein **Vorschlag** -- wird NIE automatisch uebernommen, sondern muss per `confirm()` bestaetigt werden, bevor er Stufe 0 wird. |
| 3 | Fremdanbieter | Registrierte externe Provider. Aktuell **keine** -- siehe "Was hier bewusst fehlt". |
| 4 | Nichts gefunden | Kein Report, sondern ein zweiteiliger Dialog: (a) "wo ist das fuer dich kanonisch?", (b) falls unbekannt: "sollen wir dir ein eigenes Zusatzmodul dafuer einrichten?". |

**Kernregel (aus dem Auftrag):** *Was sich beim Kopieren unbemerkt auseinanderentwickeln
kann, wird nicht kopiert, sondern aufgerufen.* Deshalb ist die Stufenleiter EINE
Komponente, die Skills aufrufen -- nicht ein Muster, das jeder Skill fuer sich kopiert.

Jeder nicht-eindeutige Stufe-1-Befund (Modul vorhanden, aber CLI nicht installiert;
Modul-Ordner da, Zieldatei fehlt/Pointer-Drift; Aufrufer-Fehler wie fehlender `scope`)
wird als **eigenes, spezifisches Ergebnis** zurueckgegeben -- nicht still im generischen
"nichts gefunden"-Dialog versteckt.

## Nutzung

```python
from pathlib import Path
from source_resolver import resolve, confirm

result = resolve("decisions.ledger")
if result.status == "resolved":
    print(result.quelle)          # {"id": "_DECISIONS-chain", "module_path": "...", ...}
elif result.status == "proposed":
    # Stufe 2: Nutzer fragen, dann:
    confirm("decisions.ledger", result.kandidaten[0], stufe_herkunft=2)
elif result.status == "not_found":
    print(result.dialog["frage_1"])
    print(result.dialog["frage_2_falls_unbekannt"])
```

CLI:

```bash
source-resolver resolve decisions.ledger
source-resolver resolve policy.registry --scope dev-hygiene
source-resolver confirm decisions.ledger '{"pfad": "/eigener/Ort/DECISIONS.md"}'
source-resolver list-roles
source-resolver check-pointer "<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.CONTROL/ticket-master"
```

`check-pointer` ist der wiederverwendbare Existenz-Check fuer `type: pointer`-Skills
(siehe `pointer_check.py`) -- direkter Bezug zu T-20260815-603417673 (drei Wochen toter
Pointer in `ticket-master/SKILL.md`). Diese Funktion ist eigenstaendig aufrufbar, z.B.
von `catalog.py` oder `skill_tester.py`, falls das Nachziehen dort in einem eigenen
Ticket erfolgt -- **das ist hier bewusst NICHT verdrahtet**, nur bereitgestellt.

## Vorhandene Stufe-1-Rollen

| Rolle | Quelle | Weg |
|---|---|---|
| `policy.registry` | Modul `policy-registry` | Adapter -> `policy-registry resolve --scope ...` (CLI), faellt auf `module_present_not_callable` zurueck, wenn nicht installiert |
| `decisions.ledger` | `_control-center/_DECISIONS/TO-DECIDE-USER.txt` | Datei-Check |
| `user.model` | `_control-center/_TOM-lm/avatar/START.md` | Datei-Check. **Einwilligung ist NICHT Teil dieser Aufloesung** -- die Consent-Regel von tom-lm/decision-avatar ("blosse Erreichbarkeit ist keine Einwilligung") bleibt Sache des aufrufenden Skills. |

## Was hier bewusst fehlt (Schnitt vom advisor-Review 2026-08-15)

- **Stufe-3-Fremdanbieter:** das Interface existiert (`FOREIGN_PROVIDERS` in
  `ladder.py`), die Liste ist leer. Ein halb funktionierender Fremdanbieter erzeugt
  Vertrauen, das er nicht verdient hat -- ein ehrliches "keine Fremdanbieter
  konfiguriert" ist im Sinn von Stufe 4 richtiger als ein Beispiel-Stub.
- **`skill_export`** (Modul->Skill-Haelfte der Asymmetrie) -- Papierstand, zurueckgestellt
  per Entscheid D-20260731-005. Diese Repo baut nur die Skill->Quelle-Haelfte.
- **Retrofit von `tom-lm`/`decide`/`load-project` auf diese Bibliothek** -- nur
  `work-autonomous` wurde als Referenzbeispiel umgestellt (siehe dortiges Changelog).
- **MCP-Adapter** -- Surface-Liste im Manifest traegt aktuell nur `library`+`cli`.

## Vorschlag fuer `.MODULES/composition.rules.json`

Die drei im Auftrag genannten Rollen (`policy.registry`, `decisions.ledger`,
`user.model` -- letztere umbenannt von `user_model` fuer Konsistenz mit der
existierenden gepunkteten Vokabel, z.B. `memory.curated`) werden **nur vorgeschlagen**,
nicht eingetragen -- das ist ein Eingriff in den Baukasten und liegt beim Nutzer. Datei:
[`proposals/composition.rules.proposal.json`](proposals/composition.rules.proposal.json),
Begruendung: [`proposals/PROPOSAL-NOTE.md`](proposals/PROPOSAL-NOTE.md).

## Tests

```bash
python -m pytest tests/ -q
```

32/32 gruen (Stand 2026-08-15), inkl. Regressionsanker fuer die Pointer-Drift-Klasse
und expliziter Test, dass Stufe 0 auch ein Modul mit Adapter ueberschreibt.
