# SUSPENSION.md — design-ferric-1_0 (NeedsDecompose)

## Disposition
`decompose_evaluation = NeedsDecompose`. This root node decomposed the Ferric 1.0 framework design into a
hub-and-spoke subtree and suspends pending its resolution. It executes none of the children's work.

## Why decomposed
The brief enumerates **nine distinct framework design concerns**, each with its own goal and its own acceptance
bar, plus delivery (a PR + a board backlog) and a synthesis/fold. Applying the Task Decomposition Framework
triggers to the actual brief: the **Scope-Based trigger fires by enumeration alone** (≥2 distinct concerns),
the **Token** and **Output-Size** triggers fire (a whole-framework design + many artifacts + a PR + a backlog),
and the **Distinct Concerns** test passes to decompose (SSR, authoring, async, router/http, docs/DX, release,
performance could each be designed by a different specialist in parallel). The single folded `SYNTHESIS.md`
output does not confer atomicity. Verdict: `NeedsDecompose`.

## What was authored before suspending
- Subtree hub `_GLOBAL.md` (context, scope, task tree with the machine-readable Task Summary table, contract).
- Contract (`contracts/_MANIFEST.yaml`, `contracts/id_and_traceability_schema.yaml`,
  `contracts/design_artifact_map.yaml`) — the shared `REQ-<AREA>-*`/`BAR-FERRIC-*` scheme, verification/stage
  vocabularies, epic/work-item schema, artifact-path map, and identities I1–I9.
- One `_BRIEF.md` per child, at each child's workspace.

## Children materialized (13), by execution group
- **G0** — `SUBTASK_scope_and_requirements` (REQ-FW-*; the requirements spine).
- **G1** (dep: scope) — `SUBTASK_ssr_hydration` (REQ-SSR-*, the must-have), `SUBTASK_authoring_model`
  (REQ-API-*), `SUBTASK_async_forms_events` (REQ-ASYNC-*), `SUBTASK_router_and_http` (REQ-RT-*/REQ-HTTP-*,
  absorbs #5/#6), `SUBTASK_docs_and_dx` (REQ-DX-*), `SUBTASK_release_and_distribution` (REQ-REL-*),
  `SUBTASK_performance_and_benchmark` (REQ-PERF-*).
- **G2** — `SUBTASK_release_bar` (BAR-FERRIC-*).
- **G3** — `SUBTASK_release_plan` (epics/work-items under #1, folding #5/#6).
- **G4** — `SUBTASK_design_pr` (assemble design/ferric/ + open the PR).
- **G5** — `SUBTASK_file_backlog` (file/extend board issues under #1).
- **G6** — `SUBTASK_synthesis` (Task Kind synthesis; asserts I1–I9, authors root `SYNTHESIS.md`, folds parent).

## Resumption condition
All child tasks reach terminal lifecycle state. `SUBTASK_synthesis` authors `SYNTHESIS.md` at this hub root
(the overseer's observation seam) and folds this parent `SUSPENDED → COMPLETED` via `engine_resume_suspended`.
