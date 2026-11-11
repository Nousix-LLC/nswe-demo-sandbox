# SUSPENSION — SUBTASK_api_layer (NeedsDecompose)

**Task**: `SUBTASK_api_layer` (the axum transport/service layer of `chirp-server`)
**Terminal state**: SUSPENDED · `decompose_evaluation = NeedsDecompose`
**Resumption condition**: all child tasks reach terminal lifecycle state; the subtree's synthesis gate
folds its result into this task via `engine_resume_suspended`, flipping it `SUSPENDED → COMPLETED`.

## Why this task decomposed

Applying the Task Decomposition Framework triggers to the brief:

- **Scope-Based / Distinct Concerns** — FIRES. The brief enumerates distinct pieces (per-endpoint
  handlers, typed-error→HTTP response mapping, static/SPA serving, server bootstrap); enumerated-concerns
  rule fires by that enumeration alone.
- **Single-Responsibility** — FAILS. Faithful description joins distinct verbs (render errors *and*
  write handlers *and* assemble router/serving *and* bootstrap the binary), emitting multiple kinds of
  output (a trait impl, handler fns, a router builder, a binary).
- **Output-Size** — FIRES (MUST decompose). Combined Rust output ≈ 500–600 lines (> 400 floor).
- **Trigger precedence** — the single declared `API_NOTES.md` handoff (output-size clear) does not
  override the fired scope/responsibility/size signals.

The pieces are coupled (handlers compile against the error `IntoResponse`, `AppState`, and the auth
extractor; the router mounts the handlers; `main` wires the router) and the subtree writes one shared
clone, so the decomposition is a **serial pipeline**, not a parallel fan-out.

## Children materialized (serial chain)

| Task id | Depends on | Responsibility |
|---------|------------|----------------|
| `SUBTASK_transport_foundations` | none | error `IntoResponse` + `AppState` + Bearer auth extractor |
| `SUBTASK_handlers` | `SUBTASK_transport_foundations` | axum handlers for the full `repository_seam` surface |
| `SUBTASK_router_and_bootstrap` | `SUBTASK_handlers` | `build_router` + `/healthz` + static/SPA + tracing + `main.rs` |
| `SUBTASK_api_synthesis` (synthesis) | all three above | four-check gate; `API_NOTES.md` + `SYNTHESIS.md` at this workspace; fold |

```
SUBTASK_transport_foundations ──► SUBTASK_handlers ──► SUBTASK_router_and_bootstrap ──► SUBTASK_api_synthesis
```

## Authored named state

- `_GLOBAL.md` — subtree hub (context, constraints, task structure, methodology posture, identities).
- `contracts/_MANIFEST.yaml` — `yaml_schema` sub-contract (extends parent): ownership + symbol seam +
  endpoint surface + the identities the gate asserts.
- `SUBTASK_transport_foundations/_BRIEF.md`, `SUBTASK_handlers/_BRIEF.md`,
  `SUBTASK_router_and_bootstrap/_BRIEF.md`, `SUBTASK_api_synthesis/_BRIEF.md` — one per child.

## Fold / resumption

The synthesis gate (`SUBTASK_api_synthesis`) authors `API_NOTES.md` (this task's declared handoff) and
`SYNTHESIS.md` at this workspace (the fold location), then calls
`engine_resume_suspended { target_task_id: "SUBTASK_api_layer", synthesized_task_id: "SUBTASK_api_synthesis", seam_path: ".../SUBTASK_api_layer/SYNTHESIS.md" }`,
flipping this task `SUSPENDED → COMPLETED` and unblocking the parent-level dependent
`../SUBTASK_integration_tests_and_docs`.
