# SUSPENSION.md — chirp-frontend (#9) decomposed (NeedsDecompose)

**Task**: chirp-frontend code-writing DAG (root of this forked subtree, persona `swe-coder`).
**Terminal state**: SUSPENDED, `decompose_evaluation = NeedsDecompose`.
**Resumption**: implicit — resume when the entire child subtree reaches terminal lifecycle
states (the synthesis gate folds this parent `SUSPENDED → COMPLETED` via `resume_suspended`).

## Why decomposed
Every decomposition trigger fired against the brief: the work composes four landed crates
(whose public APIs must be read) and authors a full WASM SPA (HTTP client layer, timeline /
compose / profile views, router wiring, error handling, wasm entry, README, tests) plus a
build/test verification gate — multiple distinct components (Scope + Distinct-Concerns +
Single-Responsibility all fire), far exceeding one invocation's token/output/tool-call envelope.
The brief itself enumerates *scaffold → http/api client layer → views/router wiring → synthesis
gate*. Verdict: `NeedsDecompose`.

## Shape (contract-first fan-out, greenfield build in an existing workspace)
A frozen contract (`contracts/`) at the hub → a Group-0 walking skeleton that owns the
composition root and pre-mounts each feature behind the frozen seam → N parallel feature spokes
with disjoint file ownership → a Group-2 synthesis verification gate that folds.

## Children materialized (6)
| Task id | Group | Depends on | Owns |
|---|---|---|---|
| `SUBTASK_scaffold` | 0 | — | crate skeleton, composition root, `error.rs`, `index.html`, README, compiling stubs; checkout+branch+initial commit |
| `SUBTASK_api_client` | 1 | scaffold | `src/api.rs` (real ApiClient) |
| `SUBTASK_timeline` | 1 | scaffold | `src/timeline.rs` |
| `SUBTASK_compose` | 1 | scaffold | `src/compose.rs` |
| `SUBTASK_profile` | 1 | scaffold | `src/profile.rs` |
| `SUBTASK_synthesis_gate` | 2 | all of the above | `SYNTHESIS.md` + PR `Closes #9` + fold |

## Contract (the frozen seam)
`contracts/_MANIFEST.yaml` (kind `rust_api`; ownership; identities; L1 derived mocks),
`contracts/app_api.rs` (frozen in-crate signatures: `AppError`, `Session`, `AppContext`,
`ApiClient` + 7 methods, the three route-view fns, the mount entry — all grounded in the real
ferric / ferric-router / ferric-http APIs), and `contracts/rest_endpoints.md` (the REST
method+path ⇄ chirp-types DTO map and the base-URL/auth assumptions chirp-server #8 must honor).
chirp-types DTOs are an external contract used directly and never redefined.

## Named state authored this invocation
- `_GLOBAL.md`, `contracts/_MANIFEST.yaml`, `contracts/app_api.rs`, `contracts/rest_endpoints.md`
- `SUBTASK_{scaffold,api_client,timeline,compose,profile,synthesis_gate}/_BRIEF.md`
- this `SUSPENSION.md`

The subtree now executes; the synthesis gate writes the `SYNTHESIS.md` verdict at this
workspace and folds this parent to COMPLETED.
