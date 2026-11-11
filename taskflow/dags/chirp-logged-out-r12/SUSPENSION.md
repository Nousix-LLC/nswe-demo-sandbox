# SUSPENSION — chirp-logged-out-r12

**Status**: Suspended / NeedsDecompose  
**Suspended at**: 2026-11-06  
**Resumption condition**: SUBTASK_backend_check and SUBTASK_frontend_check reach COMPLETED; then SUBTASK_synthesis reaches COMPLETED with SYNTHESIS.md written at the observation seam.

## Decomposition Summary

This node evaluated as `NeedsDecompose` because the task spans two distinct system
components with disjoint file ownership: `crates/chirp-server` (AC-5) and
`crates/chirp-frontend` (AC-1–4). Scope trigger fired; decomposition is mandatory.

**Shape chosen**: B (gate-concentrated verdict) — synthesis task hosts the final
PASS/FAIL verdict. Each check task produces a per-component verdict file.

## Children Materialized

| Task id | Depends on | Output |
|---------|------------|--------|
| `SUBTASK_backend_check` | none | `SUBTASK_backend_check/backend_verdict.md` |
| `SUBTASK_frontend_check` | none | `SUBTASK_frontend_check/frontend_verdict.md` |
| `SUBTASK_synthesis` | `SUBTASK_backend_check`, `SUBTASK_frontend_check` | `SYNTHESIS.md` (root workspace) |

## Authored Artifacts

- `_GLOBAL.md` — subtree hub with context, constraints, cut rationale, task structure
- `contracts/_MANIFEST.yaml` — verdict file schema contract
- `SUBTASK_backend_check/_BRIEF.md` — backend check brief (AC-5)
- `SUBTASK_frontend_check/_BRIEF.md` — frontend check brief (AC-1–4)
- `SUBTASK_synthesis/_BRIEF.md` — synthesis gate brief

## Observation Seam

The overseer reads: `taskflow/dags/chirp-logged-out-r12/SYNTHESIS.md`  
(authored by `SUBTASK_synthesis` after both check tasks complete)
