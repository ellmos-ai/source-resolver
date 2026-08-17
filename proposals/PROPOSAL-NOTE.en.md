# Proposal: three new roles in `.MODULES/composition.rules.json`

**Status: proposal, NOT entered.** This file deliberately lives only here
(`source-resolver/proposals/`), not in `.MODULES/composition.rules.json`
itself. Reason (team-lead directive 2026-08-15): new roles there are an
intervention in the shared toolkit that 14 other roles already use -- that is
the user's call, not a single ticket's.

## What is proposed

See [`composition.rules.proposal.json`](composition.rules.proposal.json) for
the formal version. Short version:

1. **`policy.registry`** -- provider `policy-registry`. Almost a
   formalization of an existing state: the module already declares
   `provides: policy.registry` in its own manifest, and the CLI delivers
   exactly the contract (`resolve --scope ...`, exit 0/2,
   `status: resolved|missing|insufficient|conflict`), verified on 2026-08-15
   directly against the source code (`policy_registry/cli.py`,
   `registry.py`).

2. **`decisions.ledger`** -- provider `_control-center/_DECISIONS`. Not a
   module with its own manifest, but a folder convention. If this role is
   entered, a dedicated `ellmos-module.v2.json` for `_DECISIONS` would be a
   sensible but separate follow-up step -- not built here.

3. **`user.model`** -- provider `build-your-users-mind` / `_TOM-lm`.
   **Renamed** from `user_model` (as worded in the ticket) to `user.model`,
   to stay consistent with the existing dotted vocabulary
   (`memory.curated`, `tickets.capture`, ...). This rename is itself a
   decision the user should confirm or reject -- named explicitly here
   rather than silently assumed.

## Why a file instead of text in the report

So the three proposals can be adopted 1:1 if the user agrees (copy-paste the
three blocks under `vorgeschlagene_neue_rollen` into the real file,
cardinality `{"minimum": 0, "maximum": 1}` matching all 14 existing roles) --
and so nothing is lost if the report itself isn't kept around.

## What is NOT proposed

No fourth `providers` field for a source-resolver-own "generic role" -- the
three roles stay named independently; source-resolver is their *resolver*,
not itself a *provider* of any of these roles (see `provides` in its own
manifest: `source.resolution`, not `policy.registry` etc.).
