# COMPLETE — child-hydrate-scope

**Task**: child-hydrate-scope (Concern 7 — hydrate.rs Scope and Sync Risk)
**Status**: completed
**Commit pin**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`

## Outputs

- `finding_c7.md` — scope and sync assessment for `crates/ferric/src/hydrate.rs`

## Summary

Two findings produced:

1. **Framework fix bundled in application feature PR** (non-blocking) — The hydrate.rs EventKind expansion is framework-level work in `crates/ferric/` that corrects a pre-existing implementation gap, not an addition causally required by the public timeline feature. The EventKind enum was already full-sized in `vdom.rs` before this PR; the PR aligned `hydrate.rs` with the existing `dom.rs` pattern.

2. **`static_event_kinds()` lacks a compile-time completeness guard** (non-blocking) — The function is a hand-written array that must track `EventKind` manually. The companion functions `event_name()` and `stash_key()` are compiler-enforced (exhaustive match arms), but `static_event_kinds()` is not. Omitting a new variant from the array compiles silently and causes listener leakage on re-render. The same gap exists in `dom.rs`.
