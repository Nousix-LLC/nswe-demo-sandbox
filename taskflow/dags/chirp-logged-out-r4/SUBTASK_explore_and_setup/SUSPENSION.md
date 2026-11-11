# Suspension Record — SUBTASK_explore_and_setup

## Status

SUSPENDED (NeedsDecompose) — waiting for 6 child tasks to reach terminal lifecycle states.

## Decomposition Decision

**Trigger**: Enumerated-concerns rule fired — the brief explicitly named 5 distinct analysis
areas (A through E: design requirements, chirp-server API surface, chirp-frontend structure,
ferric framework APIs, API spec verdict) plus a git setup step. These 5 reading concerns pass
the Distinct Concerns Test (each can be executed by a different specialist concurrently) and
the brief explicitly states "this task does two things."

**Verdict**: NeedsDecompose — parallel fan-out of 5 reading tasks + 1 synthesis gate.

## Children Materialized

| Task ID | Description | Dependencies |
|---------|-------------|--------------|
| `SUBTASK_git_branch` | Create/verify work/chirp-logged-out branch | none |
| `SUBTASK_design_analysis` | Extract requirements from design docs | none |
| `SUBTASK_server_analysis` | Map chirp-server routes, auth, API spec comparison | none |
| `SUBTASK_frontend_analysis` | Map chirp-frontend router, routes, API patterns | none |
| `SUBTASK_ferric_analysis` | Document ferric Resource/Router/SSR APIs | none |
| `SUBTASK_synthesis` | Verification gate → write analysis.md + SYNTHESIS.md fold | all 5 above |

## Resumption Condition

All 6 child tasks must reach a terminal lifecycle state. The synthesis child
(`SUBTASK_synthesis`) folds this parent SUSPENDED → COMPLETED by writing `SYNTHESIS.md`
at this workspace and calling `engine_resume_suspended`.

## Authored Named State

- `_GLOBAL.md` — subtree hub at this workspace
- `contracts/_MANIFEST.yaml` — seam contract (ownership, identities)
- `SUBTASK_git_branch/_BRIEF.md`
- `SUBTASK_design_analysis/_BRIEF.md`
- `SUBTASK_server_analysis/_BRIEF.md`
- `SUBTASK_frontend_analysis/_BRIEF.md`
- `SUBTASK_ferric_analysis/_BRIEF.md`
- `SUBTASK_synthesis/_BRIEF.md`
