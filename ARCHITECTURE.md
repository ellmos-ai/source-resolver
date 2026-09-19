# Architecture & Design — source-resolver

Stand: 2026-09-19 | Version: 0.1.4 | Package: `ellmos-ai/source-resolver`

This document outlines the architectural structure, component responsibilities, data contracts, and the 5-stage resolution ladder of `source-resolver`.

---

## 1. Architectural Overview

`source-resolver` is a role-based, local-first source resolution system designed for autonomous AI agents and skills within the `ellmos-ai` ecosystem. Instead of hard-coding file paths or external endpoints, skills query an abstract role (e.g. `decisions.ledger` or `policy.registry`) and receive the exact runtime source location.

```mermaid
flowchart TD
    Caller["Calling Skill / Agent"] -->|"resolve(role, scope, roots)"| Core["source_resolver.resolve()"]
    
    subgraph Ladder["5-Stage Resolution Ladder"]
        S0["Stage 0: User Configuration (~/.source-resolver/config.json)"]
        S1["Stage 1: Canonical Own Modules & Adapters"]
        S2["Stage 2: Filesystem Discovery (Explicit Roots)"]
        S3["Stage 3: Foreign Providers (Reserved Interface)"]
        S4["Stage 4: Two-Part Interactive Dialogue Fallback"]
    end

    Core --> S0
    S0 -->|"active override"| ResultResolved["Result: Resolved (Stage 0)"]
    S0 -->|"no override"| S1
    S1 -->|"canonical match"| ResultResolved1["Result: Resolved (Stage 1)"]
    S1 -->|"ambiguous / missing executable"| ResultError["Result: Adapter Error / Pointer Drift"]
    S1 -->|"no match"| S2
    S2 -->|"proposal found"| ResultProposed["Result: Proposed (Stage 2)"]
    S2 -->|"empty scan"| S3
    S3 -->|"no provider configured"| S4
    S4 -->|"structured dialogue"| ResultNotFound["Result: Not Found (Stage 4)"]

    ResultProposed -.->|"confirm(role, candidate, stufe=2)"| S0
```

---

## 2. Sequence Diagram: Resolution Lifecycle

The following sequence diagram details the full lifecycle of a resolution call across all stages, including Stage-0 precedence, Stage-1 adapter invocation, Stage-2 discovery proposals, and user confirmation.

```mermaid
sequenceDiagram
    autonumber
    actor Skill as Calling Skill / Agent
    participant Resolver as source_resolver
    participant Stage0 as Stage 0 - User Config
    participant Stage1 as Stage 1 - Canonical Modules & Adapters
    participant Stage2 as Stage 2 - Discovery Scan
    participant Stage4 as Stage 4 - Dialogue Fallback

    Skill->>Resolver: resolve(role, scope, roots)
    Resolver->>Stage0: check_user_override(role)
    alt Stage 0 Active Override Exists
        Stage0-->>Resolver: override target found (active: true)
        Resolver-->>Skill: ResolutionResult(status="resolved", stufe=0, quelle=target)
    else No Active User Override
        Resolver->>Stage1: check_known_providers(role, scope)
        alt Stage 1 Canonical Match Found
            Stage1-->>Resolver: canonical module path / CLI verified
            Resolver-->>Skill: ResolutionResult(status="resolved", stufe=1, quelle=target)
        else Stage 1 Ambiguous Error (Pointer Drift / Missing CLI)
            Stage1-->>Resolver: target file missing or adapter CLI not callable
            Resolver-->>Skill: ResolutionResult(status="module_present_not_callable" / "adapter_error")
        else No Stage 1 Provider Available
            Resolver->>Stage2: scan_roots(role, candidate_patterns, roots)
            alt Stage 2 Proposed Candidates Found
                Stage2-->>Resolver: candidate filesystem paths found
                Resolver-->>Skill: ResolutionResult(status="proposed", stufe=2, kandidaten=paths)
                opt Explicit Promotion via Confirmation
                    Skill->>Resolver: confirm(role, chosen_candidate, stufe_herkunft=2)
                    Resolver->>Stage0: persist_to_config(role, chosen_candidate)
                    Stage0-->>Resolver: saved in ~/.source-resolver/config.json
                    Resolver-->>Skill: confirmed - promoted to Stage 0
                end
            else Stage 2 No Matching Paths
                Resolver->>Stage4: build_two_part_dialogue(role)
                Stage4-->>Resolver: dialogue questions (canonical source query + neubau offer)
                Resolver-->>Skill: ResolutionResult(status="not_found", stufe=4, dialog=questions)
            end
        end
    end
```

---

## 3. Component Breakdown

| Component | Module | Responsibility |
|:---|:---|:---|
| **Ladder Core** | `source_resolver.ladder` | Orchestrates the 5-stage cascade, enforces Stage-0 user precedence, evaluates adapter results. |
| **Store / Cache** | `source_resolver.store` | Manages persistent user overrides in `~/.source-resolver/config.json` with atomicity and deactivate flags. |
| **Adapters** | `source_resolver.adapters` | Specialized seams (e.g. `policy-registry`, `resources.bach.tool_registry`) invoking external CLIs or APIs fail-closed. |
| **Pointer Check** | `source_resolver.pointer_check` | Validates target existence for `type: pointer` references without silent fallback. |
| **CLI Runner** | `source_resolver.cli` | Unified command-line interface for manual inspection, debugging, and testing. |

---

## 4. Invariants & Security Guarantees

1. **User Precedence (Stage 0)**: Any active entry in `~/.source-resolver/config.json` strictly overrides built-in canonical definitions and discovery heuristics.
2. **Never Auto-Adopt Heuristics (Stage 2)**: Filesystem discovery never writes to Stage 0 silently. A human or explicit agent confirmation is required.
3. **Ambiguity Preservation**: If a provider is expected but broken (e.g. pointer drift or CLI absent), the resolver returns a distinct diagnostic status rather than masking it as "not found".
4. **Zero Network Egress**: All lookups, checks, and resolutions are entirely host-local; no remote connections or telemetries are established.
