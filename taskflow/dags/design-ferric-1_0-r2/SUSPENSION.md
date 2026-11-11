# Suspension Record — design-ferric-1_0-r2

**Status**: SUSPENDED / NeedsDecompose  
**Suspended at**: 2026-11-03

## Why this node is suspended

This is the hub node for the Ferric 1.0 design recovery DAG. It decomposed into three serial spokes and is
waiting on their completion before being folded to COMPLETED by the synthesis gate.

## Children materialized

| Task id | Purpose | Depends on | Output |
|---|---|---|---|
| `SUBTASK_review-validate` | Validate all ten design docs + issue traceability | none | `SUBTASK_review-validate/review-report.md` |
| `SUBTASK_remediate` | Apply identified gaps; confirm PR readiness | `SUBTASK_review-validate` | `SUBTASK_remediate/remediation-report.md` |
| `SUBTASK_synthesize-root` | Produce root SYNTHESIS.md; fold parent | `SUBTASK_remediate` | `SYNTHESIS.md` (at this workspace) |

## Resumption condition

All three children reach a terminal state. The synthesis gate (`SUBTASK_synthesize-root`) will call
`mcp__hal__resume_suspended` to fold this node from SUSPENDED to COMPLETED once it has written `SYNTHESIS.md`.

## Context for the synthesis gate

The root `SYNTHESIS.md` must be written at:
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-ferric-1_0-r2/SYNTHESIS.md`

The overseer reads only that file (the observation seam). The disposition is `reap-whole-after-land`:
this subtree is reaped once PR #128 has landed and the tickets are on the board.
