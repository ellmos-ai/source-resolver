# Beitragsrichtlinie / Contributing Guide

## Deutsch

Vielen Dank für Ihr Interesse, zu `source-resolver` beizutragen!

### Wie Sie beitragen können

1. **Bug melden:** Erstellen Sie ein Issue mit dem Label `bug` über unsere [Issue-Vorlagen](.github/ISSUE_TEMPLATE/bug_report.md).
2. **Feature vorschlagen:** Erstellen Sie ein Issue mit dem Label `enhancement` über unsere [Feature-Request-Vorlage](.github/ISSUE_TEMPLATE/feature_request.md).
3. **Code beitragen:** Erstellen Sie einen Pull Request gegen den Default-Branch `master`.

### Pull-Request-Workflow

1. Forken Sie das Repository `ellmos-ai/source-resolver`.
2. Erstellen Sie einen fokussierten Feature-Branch:
   ```bash
   git checkout -b feature/mein-beitrag
   ```
3. Führen Sie Tests und Linter lokal aus:
   ```bash
   python -m ruff check .
   python -m pytest -ra -v
   ```
4. Committen Sie klar abgegrenzte Änderungen:
   ```bash
   git commit -m "feat(scope): prägnante Beschreibung"
   ```
5. Pushen Sie Ihren Branch und öffnen Sie einen Pull Request auf GitHub.

### Architektonische Richtlinien

- **Local-First & Zero-Network-Egress:** `source-resolver` führt keine ausgehenden Netzwerkaufrufe durch. Quellen müssen lokal auflösbar sein.
- **Stufe-0-Nutzervorrang:** Nutzerkonfigurationen (`~/.source-resolver/config.json`) brechen alle Vorgaben und dürfen niemals automatisch überschrieben werden.
- **Fail-Closed Verhalten:** Bei abweichenden oder unauflösbaren Pfaden wird deterministisch ein expliziter Fehler-Status ausgegeben, kein stiller Fallback.
- **Python-Qualität:** PEP 8 Stil, Python >=3.10 Kompatibilität, Typ-Hinweise wo sinnvoll, UTF-8 Kodierung.
- **Vertragstests:** Jede strukturelle oder funktionale Erweiterung muss durch automatisierte Tests in `tests/` abgedeckt sein.

---

## English

Thank you for your interest in contributing to `source-resolver`!

### How to Contribute

1. **Report bugs:** Open an issue with the `bug` label using our [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md).
2. **Suggest features:** Open an issue with the `enhancement` label using our [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md).
3. **Contribute code:** Submit a Pull Request targeting the `master` branch.

### Pull Request Workflow

1. Fork the `ellmos-ai/source-resolver` repository.
2. Create a focused topic branch:
   ```bash
   git checkout -b feature/my-contribution
   ```
3. Run test and lint checks locally:
   ```bash
   python -m ruff check .
   python -m pytest -ra -v
   ```
4. Commit your changes with conventional commit messages:
   ```bash
   git commit -m "feat(scope): concise description"
   ```
5. Push your branch and open a Pull Request on GitHub.

### Architectural Invariants

- **Local-First & Zero Network Egress:** `source-resolver` initiates no outbound network connections. Source resolution is strictly local.
- **Stage 0 User Sovereignty:** User overrides (`~/.source-resolver/config.json`) always win and must never be auto-overwritten.
- **Fail-Closed Behavior:** Broken or missing paths result in explicit diagnostic errors rather than silent fallbacks.
- **Python Standards:** PEP 8 compliance, Python >=3.10 support, UTF-8 file encoding.
- **Contract Tests:** All features and structural requirements must be verified by automated tests in `tests/`.
