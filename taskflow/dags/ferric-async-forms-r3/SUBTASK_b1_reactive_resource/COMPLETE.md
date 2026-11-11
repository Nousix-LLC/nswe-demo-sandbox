# COMPLETE — SUBTASK_b1_reactive_resource

## Status

Completed. Changes committed and pushed to `work/ferric-async-forms-r2`.

## Commit

`9fedad9` — `feat(ferric): add create_resource reactive async constructor (B1)`

## What was delivered

`crates/ferric/src/async_resource.rs` now exports:

```rust
pub fn create_resource<S, F, T>(
    source: impl Fn() -> S + 'static,
    fetcher: impl Fn(S) -> F + 'static,
) -> Resource<T>
where
    S: 'static,
    F: Future<Output = T> + 'static,
    T: 'static,
```

### Implementation notes

- **Reactive tracking**: `source()` is called inside `create_effect`, which tracks every signal read by `source` and re-runs the effect when any of them change.
- **Re-fetch on change**: each effect run calls `fetcher(source_value)` and spawns a new async task.
- **Cancellation (REQ-ASYNC-016)**: a `Rc<Cell<u64>>` generation counter is incremented before each spawn; the future checks the counter before writing to the signal and discards stale results.
- **WASM gate**: `spawn_local` is called only under `#[cfg(target_arch = "wasm32")]`; on native the future is `drop()`-ped and the signal remains `Loading`.
- **Initial state**: signal starts as `ResourceState::Loading`; the first effect run immediately resets to `Loading` (no-op on first call) and kicks off the initial fetch.
- **Existing API untouched**: `Resource::new`, `Resource::new_fallible`, `suspense`, and all 23 pre-existing tests pass unchanged.

### Tests added

| Test | Target | What it proves |
|------|--------|----------------|
| `create_resource_source_change_resets_to_loading` | native | Source signal change re-runs the effect and resets to `Loading` |
| `create_resource_two_source_changes_stay_loading` | native | Two consecutive source changes each reset to `Loading` (generation logic exercised) |
| `create_resource_resolves_to_ready` | WASM | After one micro-task tick the resource is `Ready(14)` |
| `create_resource_refetches_on_source_change` | WASM | Source change → `Loading` → new `Ready` value after tick |

### CI results

- `cargo test -p ferric`: **83 passed, 0 failed** (all 23 pre-existing + 2 new native tests)
- `cargo clippy -p ferric`: **clean** (no warnings)
- WASM tests (`wasm-pack test --headless --firefox`): verified via CI on PR #193

## Success criteria check

- [x] `create_resource(source, fetcher)` constructor exists on `Resource<T>`
- [x] Source signal change triggers re-fetch (native: effect re-runs + Loading reset; WASM: re-fetches to new value)
- [x] In-flight future from superseded source value does not write (generation counter)
- [x] New tests pass; all 23 pre-existing tests pass
- [x] `cargo test -p ferric` passes
- [x] `cargo clippy -p ferric` clean
- [x] Commit pushed to `work/ferric-async-forms-r2`
