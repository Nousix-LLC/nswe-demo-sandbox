# SUSPENSION.md — deploy-ghcr-auth-r2 (NeedsDecompose)

**Disposition**: SUSPENDED / NeedsDecompose. This root task decomposed the F1 deploy attempt #2
into a serial diagnose → remediate → verify pipeline and now waits for its subtree to resolve.

## Decompose evaluation
`NeedsDecompose`. Applied the Task Decomposition Framework triggers to the actual brief:
- **Scope / enumerated-concerns trigger FIRED** — the brief enumerates four distinct concerns, each with its own
  bar (reachability, image-pull/supply-chain, GitOps drift/selfHeal, ops).
- **Single-Responsibility Test FIRED** — the faithful shape is *observe → change → judge* (diagnose the live world →
  remediate to desired state → verify AC1–5 and author the verdict): a serial pipeline of distinct responsibilities
  over one live system (the precursor → transform → synthesis/verify shape).
- Token and output-size triggers cleared; by Trigger Precedence the fired scope/single-responsibility signals win.

## Chosen cut
Rejected the by-concern 4-spoke cut (fails ownership-disjointness — all four touch one mutable live cluster and are
causally chained, not parallelizable). Chose the bugfix/verification serial pipeline with gate-concentrated verdict
placement (Shape B). See `_GLOBAL.md` §Chosen-cut rationale.

## Children materialized (via engine_amend_plan add_task)
| Task id | Depends on | Output |
|---------|------------|--------|
| `SUBTASK_diagnose` | none | `SUBTASK_diagnose/diagnosis.md` |
| `SUBTASK_remediate` | `SUBTASK_diagnose` | `SUBTASK_remediate/remediation.md` (+ optional PR) |
| `SUBTASK_verify_synthesis` (synthesis gate) | `SUBTASK_diagnose`, `SUBTASK_remediate` | `SYNTHESIS.md` (this subtree root — fold location / observation seam) |

## Named state authored
- `_GLOBAL.md` (subtree hub, posture, chosen-cut rationale, Task Summary table)
- `contracts/_MANIFEST.yaml` (deployment-identity constants, diagnosis schema, AC1–5 + supply-chain identities)
- one `_BRIEF.md` per child

## Resumption condition
All child tasks reach terminal lifecycle state; the synthesis gate folds its `SYNTHESIS.md` into this parent
(`SUSPENDED → COMPLETED`) at the fold location `taskflow/dags/deploy-ghcr-auth-r2/SYNTHESIS.md`.
