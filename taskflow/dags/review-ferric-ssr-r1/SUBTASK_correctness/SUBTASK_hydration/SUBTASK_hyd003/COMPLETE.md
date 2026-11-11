# SUBTASK_hyd003 — Completion Record

**Task**: REQ-HYD-003: Is hydrate() called once from the WASM entry point? Integration test/demo?

**Status**: completed

**Output**: `criterion_003.md` (this workspace)

## Verdict Summary

**FINDING (BLOCKER)**: `hydrate()` is not called from the WASM entry point. PR #228 implements
`ferric::hydrate()` correctly and adds the SSR document shell, but does not update
`crates/chirp-frontend/src/app.rs::start()` (or the binary entry `chirp.rs`). The entry point
still calls `mount()`, which replaces the server-rendered DOM rather than adopting it.

**FINDING (NON-BLOCKER)**: No integration test or `wasm_bindgen_test` harness exercises the
full SSR→hydrate path end-to-end.

## Evidence locations (all in Nousix-LLC/nswe-demo)

- `crates/chirp-frontend/examples/chirp.rs:16` — entry point, calls `start()` not `hydrate()`
- `crates/chirp-frontend/src/app.rs` (~line 114–135) — `start()` calls `mount()`, not `hydrate()`
- `crates/ferric/src/hydrate.rs:43–70` — `hydrate()` function (correctly implemented, not called)
- `crates/chirp-server/src/ssr.rs:141` — false docstring claiming bundle calls `hydrate()`

## Files produced

- `criterion_003.md`
