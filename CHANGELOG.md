# Changelog

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
