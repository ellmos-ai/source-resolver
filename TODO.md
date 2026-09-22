# TODO.md — Active work & Release Status: source-resolver

**Version:** 0.1.4
**Updated:** 2026-09-22
**Auditor:** Gemini (Antigravity)
**Reason:** Pfad A Technische Hygiene, PEP 639 Lizenzinventar, CI-Vertragstests und Gate-Bereitschaft
**Target Repo:** `ellmos-ai/source-resolver`

Erledigte Aufgaben gehören nach `CHANGELOG.md` oder in den Abschnitt „Abgeschlossene Aufgaben“.

## STATUS

| Category | Status | Evidence / next gate |
|---|---|---|
| Secrets | DONE | Keine Secrets oder Token in versionierten Dateien (0 Treffer). |
| Private Data (PII) | DONE | Keine personenbezogenen Daten; generische Platzhalter `<HOME>` und `<username>`. |
| .gitignore | DONE | Alle Mindesteinträge (`*.pyc`, `*.db`, `.idea/`, `.vscode/`, `LOCK*.txt`, Multi-Host-Muster) vorhanden. |
| Language & Parity | DONE | README.md (Englisch) und README_de.md (Deutsch) synchron und mit echter Umlautqualität. |
| BACH Internals | DONE | Nur Read-Only-Schnittstelle zum Werkzeugregister dokumentiert; keine internen Systemdokumente. |
| Database Files | DONE | Keine Datenbankdateien versioniert; `*.db` und `*.sqlite` ignoriert. |
| README.md & Architecture | DONE | Vollständige Spezifikation mit Mermaid-Sequenzdiagrammen und `ARCHITECTURE.md`. |
| LICENSE & Governance | DONE | MIT-Lizenz vorhanden; PEP 639 `license-files` deklariert; `THIRD_PARTY_LICENSES.md` angelegt. |
| Test Coverage | DONE | 100% Testabdeckung aller 5 Stufen der Quellenauflösung und Metadaten-Verträge. |
| **Overall** | **READY** | Alle 10 Release-Gates erfüllt. |

## Offene Aufgaben (nach Release)

- [ ] **TASK-SR-01: Performance-Caching für Stufe-1-Dateisystemprüfungen** (`effort=low`, `scope=caching`, priority `normal`).
  - **Ziel:** Optionales Kurzzeit-Caching für wiederholte Dateiprüfungen bei hochfrequenten Skill-Aufrufen.
  - **Definition of Done:** Thread-sicherer In-Memory-Cache; konfigurierbare TTL; 100% Testabdeckung.

- [ ] **TASK-SR-02: Erweiterte Remote-Adapter-Typisierung** (`effort=medium`, `scope=adapters`, priority `normal`).
  - **Ziel:** Einheitliche Protokoll-Definition für Netzwerk- und MCP-basierte Quellenzugriffe.
  - **Definition of Done:** PEP 544 Protokollklassen für entfernte Provider; rein standardbibliotheksbasiert.

## Abgeschlossene Aufgaben

- [x] **TASK-SR-00: Release-Hygiene, Lizenzinventar & Gate-Bereitschaft (v0.1.4)** (`effort=low`, `scope=hygiene`, priority `high`).
  - **Ergebnis:** Standard-`TODO.md` mit `## STATUS`-Tabelle etabliert, `THIRD_PARTY_LICENSES.md` angelegt, PEP 639 `license-files` in `pyproject.toml` deklariert, `.gitignore` gehärtet, Pfadneutralität in `pointer_check.py` sichergestellt, Metadatentests für Banner und Lizenzen aktualisiert und `final_gate_check.py` auf 10/10 PASS gebracht.

---
<!-- HINWEIS: Deutsche End-User-Texte immer mit echten Umlauten schreiben: ä ö ü Ä Ö Ü ß, nicht ae/oe/ue. -->
