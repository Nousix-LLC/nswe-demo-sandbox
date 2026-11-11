# SUSPENSION.md — SUBTASK_landing-states

## Status: SUSPENDED (NeedsDecompose)

## Decomposition summary

SUBTASK_landing-states was decomposed into four child tasks because its brief
enumerates three distinct acceptance-criteria checks (AC-2, AC-3, AC-4-partial) —
each checking a different part of `landing.rs`. The enumerated-concerns rule fired;
three parallel spoke tasks cover each concern, with a synthesis gate combining
them into `FINDINGS.md`.

## Children materialized

| Task id | Concern | Depends on |
|---------|---------|------------|
| `SUBTASK_check-ac2` | AC-2: empty_view() content and CTA | none (parallel) |
| `SUBTASK_check-ac3` | AC-3: error-state recoverability and role="alert" | none (parallel) |
| `SUBTASK_check-ac4p` | AC-4-partial: header_nav() in every rendered state | none (parallel) |
| `SUBTASK_synthesis-findings` | Verification gate + FINDINGS.md assembly | check-ac2, check-ac3, check-ac4p |

## Resumption condition

This task resumes when all four children reach terminal lifecycle states and
SUBTASK_synthesis-findings produces `FINDINGS.md` at this workspace root.

## Authored artifacts

- `_GLOBAL.md` (subtree hub)
- `contracts/_MANIFEST.yaml` (contract — ownership, identities)
- `contracts/concern_findings_schema.yaml` (per-concern output schema)
- `SUBTASK_check-ac2/_BRIEF.md`
- `SUBTASK_check-ac3/_BRIEF.md`
- `SUBTASK_check-ac4p/_BRIEF.md`
- `SUBTASK_synthesis-findings/_BRIEF.md`
