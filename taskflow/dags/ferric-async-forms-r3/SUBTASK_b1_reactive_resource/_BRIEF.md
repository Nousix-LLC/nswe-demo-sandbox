# Task: B1 — Reactive `create_resource` constructor

## Task Specification

**Slug**: SUBTASK_b1_reactive_resource  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Add a `create_resource(source, fetcher)` constructor to `Resource<T>` in `crates/ferric/src/async_resource.rs` that integrates with the reactive signal system: re-fetching when the source signal changes and cancelling any in-flight future before starting a new one.

### Context

This task is part of ferric-async-forms-r3 (see `_GLOBAL.md` in the parent workspace).

**Dependencies**: none — B1 is independent of B2 and B3.  
**Dependents**: `SUBTASK_b2_b3_event_dom` (runs after this commits to the branch).

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Shared constraints, branch, CI requirements |
| Current implementation | `crates/ferric/src/async_resource.rs` on branch `work/ferric-async-forms-r2` | File to modify |
| Signal primitives | `crates/ferric/src/signal.rs` | `create_signal`, `create_effect`, `Signal<T>` signatures |
| Review synthesis | `taskflow/dags/review-ferric-async-forms-r2/SYNTHESIS.md` | B1 blocker detail |

---

## Scope

### What B1 requires

`crates/ferric/src/async_resource.rs` must gain a `create_resource` constructor with the following contract:

- **Signature**: `create_resource<S, F>(source: impl Fn() -> S + 'static, fetcher: impl Fn(S) -> F + 'static) -> Resource<T>` where `F: Future<Output = T>` and `S: 'static`.
- **Reactive tracking**: `source` is called inside a `create_effect` so that any signals read by `source` are tracked; a signal change re-runs the effect.
- **Re-fetch on change**: when the effect re-runs, the fetcher is called with the new source value and a new async task is spawned.
- **Cancellation (REQ-ASYNC-016)**: an in-flight future from a prior source value must not overwrite the signal if a newer fetch has already started. A generation counter pattern (increment before spawn; check before writing result) satisfies this.
- **WASM gate**: `spawn_local` is called only under `#[cfg(target_arch = "wasm32")]`; on non-wasm targets the future is dropped and the signal stays in `Loading` state.
- **Initial state**: the signal starts as `ResourceState::Loading`.

### Existing items to preserve

- `Resource::new(fut)` and `Resource::new_fallible(fut)` are retained unchanged (backward compatibility).
- All 20 existing native tests and 3 WASM tests must continue to pass.
- `prelude` re-exports are not changed by this task.

### Tests to add

- **Native**: at least one test verifying that changing the source signal causes the resource to transition back to `Loading` (the generation counter / reactive re-trigger is exercised even if `spawn_local` is a no-op on native).
- **WASM**: at least one test verifying that `create_resource` resolves to `Ready(value)` after the async fetcher completes.

---

## Output Specification

### Declared output

Committed change(s) on branch `work/ferric-async-forms-r2` in `crates/ferric/src/async_resource.rs` that satisfy B1. The commit must be pushed to the remote before this task is declared complete.

---

## Success Criteria

- [ ] `create_resource(source, fetcher)` constructor exists on `Resource<T>`.
- [ ] Source signal change triggers a re-fetch (testable on native via `create_effect` callback; testable in WASM via `spawn_local` completion).
- [ ] In-flight future from a superseded source value does not write to the signal.
- [ ] New tests pass; all 23 existing async_resource tests continue to pass.
- [ ] `cargo test -p ferric` passes (native).
- [ ] `wasm-pack test --headless --firefox crates/ferric` passes (WASM).
- [ ] `cargo clippy -p ferric` passes with no new warnings.
- [ ] Commit(s) pushed to `work/ferric-async-forms-r2`.

---

## Constraints

- Do not change `vdom.rs`, `dom.rs`, or `form.rs` in this task.
- Do not address NB-1 (ResourceState::Failed → Error rename) in this task.
- Infrastructure details must not appear in committed files.
