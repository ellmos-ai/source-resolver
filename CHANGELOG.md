# Changelog

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
