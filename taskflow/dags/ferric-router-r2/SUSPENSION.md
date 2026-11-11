# SUSPENSION — ferric-router-r2

**Status**: Suspended / NeedsDecompose  
**Decompose evaluation**: NeedsDecompose  
**Suspended at**: 2026-11-04

---

## Decomposition Summary

The ferric-router-r2 remediation DAG has been decomposed into three child tasks:

| Task | Group | Dependencies | Output |
|------|-------|--------------|--------|
| `SUBTASK_router-branch` | 0 (parallel) | none | `SUBTASK_router-branch/outputs/router-pr.md` |
| `SUBTASK_macros-assessment` | 0 (parallel) | none | `SUBTASK_macros-assessment/outputs/macros-assessment.md` |
| `SUBTASK_synthesis` | 1 (gate) | SUBTASK_router-branch, SUBTASK_macros-assessment | `SYNTHESIS.md` |

## Authored Artifacts

- `_GLOBAL.md` — hub document for the subtree
- `contracts/_MANIFEST.yaml` — ownership manifest with 3 contract identities
- `SUBTASK_router-branch/_BRIEF.md` — brief for the router-only branch + PR spoke
- `SUBTASK_macros-assessment/_BRIEF.md` — brief for the macros scope assessment spoke
- `SUBTASK_synthesis/_BRIEF.md` — brief for the synthesis verification gate

## Resumption Condition

This node resumes when SUBTASK_synthesis completes and calls `engine_resume_suspended` with:
- `target_task_id`: this task (ferric-router-r2)
- `seam_path`: `/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-router-r2/SYNTHESIS.md`

The observation seam for the overseer is:
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-router-r2/SYNTHESIS.md`
