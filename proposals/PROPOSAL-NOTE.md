# Vorschlag: drei neue Rollen in `.MODULES/composition.rules.json`

**Status: Vorschlag, NICHT eingetragen.** Diese Datei liegt bewusst nur hier
(`source-resolver/proposals/`), nicht in `.MODULES/composition.rules.json` selbst.
Grund (team-lead-Vorgabe 2026-08-15): neue Rollen dort sind ein Eingriff in den
gemeinsamen Baukasten, den 14 andere Rollen bereits nutzen -- das ist Sache des
Nutzers, nicht eines einzelnen Tickets.

## Was vorgeschlagen wird

Siehe [`composition.rules.proposal.json`](composition.rules.proposal.json) fuer die
formale Fassung. Kurzfassung:

1. **`policy.registry`** -- Provider `policy-registry`. Fast eine Formalisierung eines
   bestehenden Zustands: das Modul deklariert `provides: policy.registry` bereits in
   seinem eigenen Manifest, die CLI liefert exakt den Vertrag (`resolve --scope ...`,
   Exit 0/2, `status: resolved|missing|insufficient|conflict`), verifiziert am
   15.08.2026 direkt am Quellcode (`policy_registry/cli.py`, `registry.py`).

2. **`decisions.ledger`** -- Provider `_control-center/_DECISIONS`. Kein Modul mit
   eigenem Manifest, sondern eine Ordnerkonvention. Wird diese Rolle eingetragen, waere
   ein eigenes `ellmos-module.v2.json` fuer `_DECISIONS` ein sinnvoller, aber
   eigenstaendiger Folgeschritt -- hier nicht mitgebaut.

3. **`user.model`** -- Provider `build-your-users-mind` / `_TOM-lm`. **Umbenannt** von
   `user_model` (so im Ticket-Wortlaut) auf `user.model`, um mit der bestehenden
   gepunkteten Vokabel konsistent zu sein (`memory.curated`, `tickets.capture`, ...).
   Diese Umbenennung ist selbst eine Entscheidung, die der Nutzer bestaetigen oder
   verwerfen sollte -- deshalb hier explizit benannt statt still vorausgesetzt.

## Warum als Datei statt als Text in der Rueckmeldung

Damit die drei Vorschlaege 1:1 uebernehmbar sind, wenn der Nutzer zustimmt (Copy-Paste
der drei Bloecke unter `vorgeschlagene_neue_rollen` in die echte Datei, Cardinality
`{"minimum": 0, "maximum": 1}` passend zu allen 14 bestehenden Rollen) -- und damit
nichts verloren geht, wenn die Rueckmeldung selbst nicht dauerhaft aufbewahrt wird.

## Was NICHT vorgeschlagen wird

Kein viertes `providers`-Feld fuer einen source-resolver-eigenen "generic role"
-- die drei Rollen bleiben eigenstaendig benannt, source-resolver ist ihr *Aufloeser*,
nicht selbst ein *Provider* einer dieser Rollen (siehe `provides` im eigenen Manifest:
`source.resolution`, nicht `policy.registry` o.ae.).
