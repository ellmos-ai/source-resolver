# Changelog

## [Unreleased]

### Pfad B: Visual CLI Preview & Discoverability Hardening (2026-11-04)

- **Visual CLI Session Preview** (`assets/cli-session-preview.svg`): Hochauflösendes Dark-Mode Vektor-Asset (880x540) für Terminal-Sitzung, Befehlsdemonstration (`resolve`, `confirm`, `check-pointer`), Fehlerfall-Dialoge und 5-Stufen-Leiterübersicht erstellt und in `README.md` und `README_de.md` integriert.
- **Discoverability & SEO-Keywords** (`pyproject.toml`): Metadaten-Schlagwörter um `zero-egress`, `local-first`, `agent-framework`, `pointer-check`, `staged-resolution` und `fail-closed` erweitert.
- **Badges & Dokumentation**: Badges für Zero Network Egress, Local-First Architektur, CLI-Vorschau und Verifikationsstempel (Verified/Geprüft 2026-11-04) in englischer und deutscher README verankert; Test-Badge auf 54/54 Tests aktualisiert.
- **Zero-Pollution & Git-Hygiene**: `MARKETING-LOG.txt` aus dem Git-Tracking des Ziel-Repositories entfernt (`git rm --cached`) und `.gitignore` um Schutzregeln für interne Marketing- und Prüf-Logs (`MARKETING-LOG.txt`, `CHECKS-LOG.txt`, `ANTIGRAVITY-LOG.txt`) gehärtet.
- **LLM-Kontext** (`llms.txt`): Currency-Stempel auf 2026-11-04 aktualisiert, Testanzahl auf 54/54 synchronisiert und Referenz auf das visuelle CLI-Session-Asset verankert.
- **Automatisierte Vertragstests** (`tests/test_metadata.py`): Zwei neue Vertragstests `test_visual_cli_preview_contract()` und `test_discoverability_and_seo_contract()` hinzugefügt (Gesamtsuite auf 54/54 Tests erweitert, 100% grün).

## [0.1.4] - 2026-09-16 (Care & Hygiene: 2026-11-03)

### Repository-Hygiene & Community Governance (2026-11-03)

- **Community Governance**: Zweisprachiger Verhaltenskodex (`CODE_OF_CONDUCT.md` nach Contributor Covenant v2.1) und Beitragsrichtlinie (`CONTRIBUTING.md` mit Pull-Request-Workflow, Local-First / Zero-Network-Egress Richtlinien und Testanforderungen) etabliert.
- **Issue Templates**: Standardisierte GitHub Issue-Vorlagen für Fehlerberichte (`.github/ISSUE_TEMPLATE/bug_report.md`) und Funktionswünsche (`.github/ISSUE_TEMPLATE/feature_request.md`) hinzugefügt.
- **PEP 621 Projekt-URLs**: `pyproject.toml` um direkte URLs für `Contributing` und `Code of Conduct` erweitert.
- **Dokumentation & Badges**: Shields.io Badges für Mitwirken (`Contributing: Guide`) und Verhaltenskodex (`Code of Conduct: v2.1`) sowie Sektion `Community & Governance` in `README.md` und `README_de.md` integriert; Test-Badge auf 52/52 Tests aktualisiert.
- **Automatisierte Vertragstests**: `tests/test_metadata.py` um `test_community_governance_contract()` und `test_issue_templates_contract()` erweitert und bestehende Verträge für URLs und bilaterale README-Parität gehärtet (Gesamtsuite auf 52/52 Tests erweitert, 100% grün).

### Release-Hygiene, Lizenzinventar & Gate-Bereitschaft (2026-09-22)

- **Release Gates & Hygiene**: Standard-`TODO.md` mit `## STATUS`-Tabelle etabliert und alle 10 Gates auf 10/10 PASS verifiziert (`final_gate_check.py`).
- **PEP 639 Lizenzinventar**: `THIRD_PARTY_LICENSES.md` mit Nachweis von 0 externen Laufzeitabhängigkeiten (reine Python-Standardbibliothek) erstellt und `license-files` in `pyproject.toml` deklariert.
- **.gitignore-Härtung**: Mindesteinträge um `*.pyc`, `*.db`, `*.sqlite`, `.idea/`, `.vscode/` und `data/` erweitert.
- **Pfadneutralität**: Hostspezifischen Beispielpfad in `src/source_resolver/pointer_check.py` durch generischen Platzhalter ersetzt.
- **Vertragstests & Banner-Fix**: `test_bilingual_readme_contract` für animiertes `assets/banner.gif` harmonisiert und neuen Vertragstest `test_todo_and_license_inventory_contract` hinzugefügt (50/50 Tests grün).

### Pfad B: Discoverability, Sequenzdiagramme & Architektur-Dokumentation (2026-09-19)

- **Sequenzdiagramme**: Zweisprachiges Mermaid-Sequenzdiagramm des 5-Stufen-Auflösungsablaufs (Skill -> Resolver -> Stufe 0 Nutzervorrang -> Stufe 1 Kanonische Module/Adapter -> Stufe 2 Discovery Proposal -> Stufe 4 Dialog-Fallback) in `README.md` und `README_de.md` integriert.
- **Architektur-Spezifikation** (`ARCHITECTURE.md`): Neues Dokument mit System-Flowchart, Sequenzdiagramm, Modul-Aufteilung und Local-First / Zero-Network-Egress Sicherheitsgarantien.
- **Badges**: Architektur-Badge (`Architecture: Sequence Diagram`) und Code-Stil-Badge (`Code Style: Ruff`) in englischer und deutscher README ergänzt.
- **LLM-Kontext** (`llms.txt`): Aktualisiert auf Stand 2026-09-19, Referenz auf `ARCHITECTURE.md` und Sequenzfluss verankert.
- **Vertragstests** (`tests/test_metadata.py`): Neuer Vertragstest `test_architecture_contract` zur Sicherung von `ARCHITECTURE.md` und Diagramm-Integrität.
- **Marketing & Log**: `MARKETING-LOG.txt` im Repo angelegt.

### Features & Updates (2026-09-16)

Read-only-Anbindung des BACH-Werkzeugregisters für die Ressourcenachse:

- Neue Stufe-1-Rolle `resources.bach.tool_registry` mit fail-closed Adapter.
- BACH stellt `bach_api.tool_registry.list()` über eine SQLite-Read-only-URI bereit;
  der Resolver öffnet `bach.db` nicht direkt und fragt `tool_patterns` nicht ab.
- Query- und Statusfilter, Bridge-Fehler und fehlende BACH-Installation werden als
  strukturierte, getrennte Befunde behandelt.
- 4 neue Adapter-/Ladder-Tests; Gesamtsuite auf 48 Tests erweitert.

## [0.1.3] - 2026-09-10

Pfad-A-Hygiene, CI-Matrix-Härtung, PEP 621 Metadaten und Vertragstest-Erweiterung:

- **CI-Matrix-Härtung** (`.github/workflows/ci.yml`): Neue automatisierte Matrix über `ubuntu-latest`, `windows-latest` und `macos-latest` für Python 3.10, 3.11, 3.12 und 3.13 mit `concurrency: cancel-in-progress: true`, `permissions: contents: read`, Ruff-Linter, Bytecode-Kompilierung (`compileall`) und Pytest.
- **Stale Issues & PRs Workflow** (`.github/workflows/stale.yml`): Triage-Automatisierung mit `actions/stale@v9` nach 30 Tagen Inaktivität und 7 Tagen Schließfrist.
- **PEP 621 Standardisierung** (`pyproject.toml`): Spezifikation von `[project.urls]` (Homepage, Repository, Documentation, Issues, Changelog, Security), standardisierte OS- und Python-3.10-3.13-Classifiers, optionale `dev` und `test` Dependencies sowie pytest `addopts = "-ra -v"` und Ruff-Konfiguration.
- **.gitignore-Härtung**: Multi-Host Synchronisationskonflikte (`*-conflict-*`, `*-ASUS-GEI.*`, `*-WORKSTATION-LG.*`, `Thumbs.db`, `desktop.ini`), Multi-Agent Locks (`LOCK`, `LOCK.*`, `*.lock`, `LOCK*.txt`) und Build-/Test-Artefakte abgesichert.
- **Sicherheitsrichtlinie & SLAs** (`SECURITY.md`): Bilinguale Sicherheitsrichtlinie nach P-006 mit 48-Stunden-Empfangsbestätigung und 5-Werktage-Triage-SLA, Zero-Network-Egress und Stufe-0-Nutzervorrang-Garantien.
- **CLI & Modul-Ausführung**: `src/source_resolver/__main__.py` für standardisierte `python -m source_resolver`-Aufrufe ergänzt.
- **Automatisierte Vertragstests** (`tests/test_metadata.py`): 8 neue Vertragstests für Versions-Parität, PEP 621 Struktur, Gitignore-Muster, CI/Stale-Workflows, Security-SLAs und öffentliche Kontrakt-Invarianten (Gesamtsuite auf 44/44 Tests erweitert, 100% grün).
- **Dokumentation & Badges**: Shields.io Badges, Sprachumschalter, Version 0.1.3 und Security-SLA in `README.md`, `README_de.md` und `llms.txt` synchronisiert.

## [0.1.2] - 2026-08-25

CR11=C Hoheits-Fassung (T-20260824-339847482): neue Stufe-1-Rolle `resources.inventory` fuer `.SYNC/_inventory/inventory.db` (9 Tabellen systems/software/skills/mcps/plugins/connectors/agents/pipelines/folders). Register-Hoheit liegt beim ControlRoom-Programm; ellmos-controlcenter-mcp `controlcenter_list_resources` ist nur Lese-Spiegel, keine zweite Kanonik.

- Neue Rolle `resources.inventory` in `KNOWN_MODULE_PROVIDERS`, aufgeloest per `module_path`+`target` (wie `decisions.ledger`) -- keine Query-CLI vorhanden, direkter SQLite-Zugriff.
- 1 neuer Test (36/36 gruen), README/README_de Rollentabelle nachgezogen.

## [0.1.1] - 2026-08-25

K3=C (T-20260825-342866657, User-Entscheidung "beides": Resolver-Rollen zuerst,
Doku verweist darauf statt sie zu duplizieren): zwei neue Stufe-1-Rollen fuer die
bisher dokumentierte, aber ungefuellte Luecke in `work-autonomous/
exhaustion_check.py` (dort bisher hardcodiert).

- Neue Rollen `memory.organic` (Gardener) und `memory.curated` (USMC) in
  `KNOWN_MODULE_PROVIDERS`, jeweils per einfachem CLI-Praesenzcheck
  (`shutil.which("gardener")`/`shutil.which("usmc")`) aufgeloest -- kein voller
  Adapter, da beide CLIs pip/editable-installiert sind und keinen festen
  Modulordner unter `<HOME>` haben (anders als `policy.registry`/
  `decisions.ledger`/`user.model`).
- `_try_known_module()` um einen `"cli"`-Zweig erweitert (Alternative zum
  bisherigen `"module_path"`-Zweig, gleiche Semantik: kein Treffer = echte
  Abwesenheit, faellt weiter durch die Leiter).
- 3 neue Tests (35/35 gruen), README/README_de Rollentabelle nachgezogen.

## [0.1.0] - 2026-08-15

Erstversion. Gebaut fuer Ticket T-20260815-385400870 ("Quellen-Connectorebene fuer
Skills"), inklusive beider Nutzer-Nachtraege (korrigierte Stufenordnung mit
Nutzer-Vorrang; Wiederverwendung des `type: pointer`-Musters statt Neubau).

- Stufenleiter (`ladder.py`): Stufe 0 (Nutzerkonfiguration) .. Stufe 4 (Dialog).
- Adapter fuer `policy.registry` -> delegiert an `policy-registry resolve` (CLI-Vertrag
  aus dem Quellcode verifiziert, nicht vermutet).
- Stufe-1-Provider fuer `decisions.ledger` (`_control-center/_DECISIONS`) und
  `user.model` (`_control-center/_TOM-lm`), Pfade auf diesem Host verifiziert.
- Wiederverwendbarer Pointer-Existenz-Check (`pointer_check.py`), motiviert durch den
  drei Wochen toten Pointer in `ticket-master/SKILL.md` (T-20260815-603417673) --
  bereitgestellt, aber bewusst nicht in `catalog.py`/`skill_tester.py` verdrahtet.
- CLI (`source-resolver resolve|confirm|list-roles|check-pointer`).
- 32/32 Tests gruen.
- Vorschlag fuer drei neue `composition.rules.json`-Rollen (`proposals/`, NICHT
  eingetragen).
- Bewusst nicht gebaut: Stufe-3-Fremdanbieter (Interface ja, Provider nein), MCP-Adapter,
  `skill_export`, Retrofit weiterer Skills ausser `work-autonomous`.
