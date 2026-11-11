# SUSPENSION.md — ferric-router DAG node (NeedsDecompose)

## Why suspended
The `ferric-router` work-item (issue #5) fired multiple decomposition triggers at the dispatch-time
evaluation — distinct components (pure matcher / web-sys History integration / reactive view),
enumerated concerns, output > 400 lines, a serial pipeline of distinct responsibilities, and a
tool-call envelope far exceeding the atomic floor. `decompose_evaluation = NeedsDecompose`.

This node authored its subtree hub, the frozen contract, and five child briefs, and materialized the
five children via `engine_amend_plan { add_task }`. It now suspends pending their resolution.

## Chosen cut
A **contract-first SERIAL pipeline** (mirroring the landed sibling `ferric-foundation`): one frozen
public-API contract (`contracts/ferric_router_api.rs`, kind `rust_trait`), internal layer seams
serialized at mock depth **L0** (each layer reads its predecessor's REAL output in the shared clone
`checkout/`), disjoint per-file ownership. Rationale in `_GLOBAL.md`.

## Children materialized (execution groups)
| Group | Task id | Depends on | Owns |
|-------|---------|-----------|------|
| 0 | `SUBTASK_scaffold` | — | clone + branch `work/ferric-router` + crate skeleton (Cargo.toml, lib.rs+prelude, stubs, example stub) |
| 1 | `SUBTASK_matcher` | scaffold | `src/matcher.rs` (pure matcher + param extraction + native tests) |
| 2 | `SUBTASK_navigation` | matcher | `src/router.rs` (Router, navigate, current_path, History API, outlet) |
| 3 | `SUBTASK_view` | navigation | `src/link.rs` + `examples/app.rs` + `README.md` |
| 4 | `SUBTASK_synthesis` | all above | verification gate + push + PR into `main` (`Closes #5`) + `SYNTHESIS.md` |

## Named state authored before this suspension
- `_GLOBAL.md` (subtree hub) — context, chosen-cut rationale, task summary DAG, methodology posture, subtree constraints
- `contracts/_MANIFEST.yaml` — ownership map + the identities the synthesis gate asserts
- `contracts/ferric_router_api.rs` — the FROZEN public API surface (read-only for descendants)
- `SUBTASK_{scaffold,matcher,navigation,view,synthesis}/_BRIEF.md` — the five child briefs

## Resumption condition
All child tasks reach terminal lifecycle states. The subtree resolves via the synthesis fold:
`SUBTASK_synthesis` authors `SYNTHESIS.md` at this subtree root (the observation seam
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-router/SYNTHESIS.md`) carrying the PASS/FAIL
verdict + the PR URL, and resumes this parent `SUSPENDED → COMPLETED`.
