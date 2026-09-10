# Security Policy / Sicherheitsrichtlinie

## Supported Versions / Unterstützte Versionen

| Version | Supported / Unterstützt |
| ------- | ----------------------- |
| 0.1.x   | :white_check_mark:      |
| < 0.1   | :x:                     |

---

## English Security Policy

### Core Security & Privacy Principles

`source-resolver` is a role-based source resolution library for AI agent skills and local automation workflows. It is engineered with strict local boundaries and fail-closed privacy guarantees:

1. **Strict Local-First Architecture & Zero Network Egress:**
   - The entire resolution ladder (Stage 0 to Stage 4) operates exclusively on local filesystem paths, registered local module paths, and local CLI executables.
   - It initiates zero outbound HTTP/HTTPS requests, contains no telemetry, and transmits no metadata or query strings over the network.

2. **User Configuration Sovereignty (Stage 0 Priority):**
   - Explicit user configurations stored in `~/.source-resolver/config.json` take absolute precedence over any built-in canonical providers (Stage 1), discovery proposals (Stage 2), or external adapters (Stage 3).
   - Local user overrides cannot be silently superseded by discovered files or package updates.

3. **Safe Discovery Proposals (Stage 2 Non-Auto-Confirmation):**
   - Stage 2 discovery proposals return candidate locations as unconfirmed suggestions (`status="proposed"`, `is_proposal=True`).
   - Discovery proposals never mutate persistent user configuration or execute unknown external code automatically without explicit confirmation (`source-resolver confirm` or programmatic confirmation).

4. **Fail-Closed Pointer & Adapter Resolution:**
   - Missing pointer targets, dangling paths, or unavailable adapter CLIs result in deterministic, fail-closed diagnostic outcomes (`status="error"`, `reason="pointer_drift"` or `reason="adapter_error"`).
   - Broken configurations never fall through silently to insecure defaults.

5. **Credential & Secret Protection:**
   - `source-resolver` resolves storage pointers and module paths; it never requires or persists plaintext API keys, passwords, or tokens.
   - Fixtures and test suites run entirely against isolated temporary directory trees (`tmp_path`).

### Reporting a Vulnerability

If you identify a potential security issue or vulnerability in `source-resolver`, please report it privately:

1. **GitHub Security Advisory (Preferred):** Open a private security advisory at [ellmos-ai/source-resolver Security Advisories](https://github.com/ellmos-ai/source-resolver/security/advisories).
2. **Email Contacts:** Send detailed technical findings to `security@open-bricks.org` and `security@ellmos.ai` (CC: `lukas@open-bricks.org`, `support@lukasgeiger.com`).

**Service Level Agreement (SLA):**
- **Acknowledgment:** Within 48 hours.
- **Triage & Risk Assessment:** Within 5 business days.
- **Remediation & Fix Release:** Handled with priority according to verified testing.

Please do not disclose security issues through public GitHub issues or public pull requests.

---

## Deutsche Sicherheitsrichtlinie (German)

### Grundsätze zu Sicherheit und Datenschutz

`source-resolver` dient der rollenbasierten Quellenauflösung für KI-Agenten-Skills und Automations-Workflows. Die Bibliothek unterliegt strikten Schutz- und Isolationsgarantien:

1. **Striktes Local-First-Prinzip und Zero-Network-Egress:**
   - Die gesamte Stufenleiter (Stufe 0 bis Stufe 4) arbeitet ausschließlich auf dem lokalen Dateisystem, lokalen Modulpfaden und lokalen CLI-Binaries.
   - Das System führt keine ausgehenden Netzwerkverbindungen (HTTP/HTTPS) durch, sendet keine Telemetriedaten und überträgt keinerlei Rollen- oder Pfadabfragen ins Internet.

2. **Souveränität der Nutzerkonfiguration (Vorrang von Stufe 0):**
   - Explizite Nutzereinträge in `~/.source-resolver/config.json` besitzen stets Vorrang vor kanonischen Modul-Providern (Stufe 1), heuristischen Suchergebnissen (Stufe 2) oder Adaptern (Stufe 3).
   - Nutzereinstellungen können nicht durch automatisierte Dateifunde oder Paketaktualisierungen stillschweigend überschrieben werden.

3. **Sichere Discovery-Vorschläge (Keine Auto-Bestätigung auf Stufe 2):**
   - Gefundene Kandidaten auf Stufe 2 werden als unverbindliche Vorschläge ausgewiesen (`status="proposed"`).
   - Heuristische Funde verändern niemals selbsttätig die persistente Konfiguration und führen keine ungeprüften Skripte aus, solange keine explizite Bestätigung vorliegt.

4. **Fail-Closed-Auflösung von Pointern und Adaptern:**
   - Nicht auffindbare Zeigerziele (Pointer-Drift) oder fehlende CLI-Adapter führen zu eindeutigen Fehlerbefunden (`pointer_drift`, `adapter_error`), statt unbemerkt auf unsichere Standardpfade zurückzufallen.

5. **Schutz von Geheimnissen und Schlüsseln:**
   - Es werden keine Passwörter, API-Schlüssel oder Tokens im Quellcode oder in den Konfigurationsdateien gespeichert.
   - Tests laufen vollständig isoliert auf temporären Dateisystempfaden.

### Meldung von Sicherheitslücken

Sollten Sie eine Sicherheitslücke oder Unregelmäßigkeit in `source-resolver` feststellen, melden Sie diese bitte vertraulich:

1. **GitHub Security Advisory (Bevorzugt):** Erstellen Sie ein vertrauliches Security Advisory unter [ellmos-ai/source-resolver Security Advisories](https://github.com/ellmos-ai/source-resolver/security/advisories).
2. **E-Mail-Kontakt:** Senden Sie den Befund an `security@open-bricks.org` und `security@ellmos.ai` (CC: `lukas@open-bricks.org`, `support@lukasgeiger.com`).

**Service Level Agreement (SLA):**
- **Erstreaktion / Empfangsbestätigung:** Innerhalb von 48 Stunden.
- **Triage & Risikobewertung:** Innerhalb von 5 Werktagen.
- **Bereitstellung eines Fixes:** Prioritäre Behebung mit verifizierten Regressionstests.

Bitte veröffentlichen Sie Sicherheitsmeldungen keinesfalls in öffentlichen Issues oder Pull Requests.
