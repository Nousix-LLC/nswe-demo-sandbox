# SUSPENSION.md — chirp-server (work-item #8) decomposed

**Status**: SUSPENDED / NeedsDecompose
**Resumption**: all child tasks reach terminal lifecycle state; the synthesis gate's `SYNTHESIS.md`
fold at this workspace resolves this node `SUSPENDED → COMPLETED`.

## Decompose evaluation

Applied the TASK_DECOMPOSITION_FRAMEWORK triggers to the chirp-server brief:

- **Scope-Based (multiple system components)** — FIRED: persistence/repository layer, HTTP transport+service
  layer, static/SPA serving, API integration tests, and verification/PR are distinct components.
- **Distinct Concerns / Single-Responsibility** — FIRED: the faithful description joins many distinct verbs
  (scaffold AND define the repository trait AND implement the store AND write handlers AND wire routing AND
  serve static+SPA AND write integration tests AND verify+PR).
- **Output Size** — FIRED: well over 400 lines across many source files.
- **Tool-call envelope** — executing atomically would far exceed the ~100-call collapse threshold.

Multiple triggers fired ⇒ **NeedsDecompose**.

## Decomposition shape

A **layered serial pipeline** (the transport → service → repository layering the brief itself calls out),
with cross-sibling edges serialized so each stage composes against the real committed clone (keeping the
contract thin), mirroring the engagement's implement→gate precedent (chirp-types) but cutting the oversized
"implement" into its genuine layers:

```
SUBTASK_scaffold_and_repository ─► SUBTASK_api_layer ─► SUBTASK_integration_tests_and_docs ─► SUBTASK_synthesis_gate
```

| Child | Responsibility | Output |
|---|---|---|
| `SUBTASK_scaffold_and_repository` | Clone + branch + crate scaffold + `ChirpRepository` trait + `ServerError` enum + in-memory impl + unit tests | `IMPLEMENTATION_NOTES.md` |
| `SUBTASK_api_layer` | axum handlers, router, `AppState`, error `IntoResponse`, static+SPA serving, `/healthz`, tracing, `main.rs` | `API_NOTES.md` |
| `SUBTASK_integration_tests_and_docs` | End-to-end API integration tests + `README.md` + rustdoc polish | `TEST_NOTES.md` |
| `SUBTASK_synthesis_gate` (synthesis) | Authoritative build/test/fmt/clippy + four-check gate; push + PR (`Closes #8`); PASS/FAIL | `SYNTHESIS.md` (this workspace — fold/observation seam) |

## Named state authored before suspending

- `_GLOBAL.md` — subtree hub (context, constraints, methodology posture, task summary, identities).
- `contracts/_MANIFEST.yaml` — thin `yaml_schema` contract: shared conventions (clone path, branch, crate id,
  module layout), the repository-trait capability seam, the error-mapping table, the ownership map, and the
  gate's assertion set.
- `SUBTASK_*/_BRIEF.md` for all four children (synthesis child authored AS a verification gate).
- Four `engine_amend_plan { add_task }` calls applied — the serial chain is reflected in execution groups 0→1→2→3.

## Observation seam

The overseer observes `SYNTHESIS.md` at `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/SYNTHESIS.md`
(the PASS/FAIL verdict + PR URL), per `_FORK.md`.
