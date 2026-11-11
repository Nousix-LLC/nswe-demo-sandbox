# SUSPENSION.md — SUBTASK_live_measurement (NeedsDecompose)

## Disposition
Decomposed. This node evaluated `NeedsDecompose` and suspended pending its child subtree. It executed no measurement
itself; the measurement is carried by the children below and consolidated by the fold into this node's declared
output, `outputs/live-measurement.md`.

## Why decomposed
The work is 278 `BAR-*` across five areas, verified by four distinct methods, each requiring a real observation of the
live product at `c805525` or a repository artifact. Against the brief:
- **Output Size** fired — 278 verdict rows with observations far exceed the single-invocation output floor.
- **Scope-Based / Distinct Concerns** fired by enumeration — five areas and four verification methods.
- **Single-Responsibility** fired — exercising a running UI, running/reading repository tests, reading declared
  config/code properties, and observing running-service survival are distinct kinds of observation.
- **Token** and the **100-tool-call runtime floor** would both be exceeded by an atomic attempt.

Being a spoke the gate already split out is not evidence of atomicity; the evaluation was made against this node's own
brief and the real shape of the work.

## Decomposition shape
Partitioned by each `BAR-*`'s own declared `verification_method` — disjoint by construction (each `BAR-*` names one
method) and total (the four methods are the whole closed vocabulary). One measurement child per method, plus a
synthesis fold. The seam (per-row schema, partition, ownership, totality identity) is frozen in
`contracts/_MANIFEST.yaml` before any child runs.

| Child | Task Kind | Depends on | Partition (verification_method) | Count | Output |
|-------|-----------|------------|----------------------------------|------:|--------|
| `SUBTASK_live_journeys` | standard | none | `manual_user_check` | 139 | `outputs/live-journeys-measurement.md` |
| `SUBTASK_automated_tests` | standard | none | `automated_test` | 36 | `outputs/automated-test-measurement.md` |
| `SUBTASK_inspection_checks` | standard | none | `inspection` | 35 | `outputs/inspection-measurement.md` |
| `SUBTASK_operational_checks` | standard | none | `operational_check` | 68 | `outputs/operational-measurement.md` |
| `SUBTASK_measurement_fold` | synthesis | the four above | union + totality assertion + fold | 278 | `outputs/live-measurement.md` (+ `SYNTHESIS.md`) |

Partition total: 139 + 36 + 35 + 68 = 278.

## Authored named state
- `_GLOBAL.md` — this subtree's hub.
- `contracts/_MANIFEST.yaml` — the sub-contract (row schema, method partition, ownership, totality/vocab/hygiene
  identities, expected per-method counts).
- `SUBTASK_live_journeys/_BRIEF.md`, `SUBTASK_automated_tests/_BRIEF.md`, `SUBTASK_inspection_checks/_BRIEF.md`,
  `SUBTASK_operational_checks/_BRIEF.md` — the four measurement briefs.
- `SUBTASK_measurement_fold/_BRIEF.md` — the synthesis-fold brief (`Task Kind: synthesis`).

## Resumption
All five children were materialized via `engine_amend_plan { add_task }`. This node remains SUSPENDED until the
subtree reaches terminal states; the fold writes this node's `outputs/live-measurement.md` and folds
`SUBTASK_live_measurement` SUSPENDED → COMPLETED with that output as its result.
