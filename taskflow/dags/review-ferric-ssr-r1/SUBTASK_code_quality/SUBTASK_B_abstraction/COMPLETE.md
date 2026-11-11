# COMPLETE — SUBTASK_B_abstraction

**Task**: Area B: Abstraction Boundaries — PR #228
**Verdict**: FINDING (NON-BLOCKER)
**Output**: `area_b_abstraction.md`

## Summary

Reviewed the SSR/client-side separation across `ferric/src/ssr.rs`, `ferric/src/hydrate.rs`,
`ferric/src/dom.rs`, `ferric/src/lib.rs`, `chirp-server/src/ssr.rs`, and both Cargo manifests.

The SSR module is clean: no `web_sys` or `wasm_bindgen` references. The hydration module is
correctly gated at compile time. One non-blocking finding: `pub mod dom;` in `lib.rs` lacks
the `#[cfg(target_arch = "wasm32")]` gate that the PR correctly applies to `pub mod hydrate;`.
Now that `ferric` is a native dependency of `chirp-server`, `ferric::dom` and
`ferric::prelude::mount` are reachable from native code (they compile via panicking stubs but
would panic at runtime if called). The fix is to add the cfg gate to `pub mod dom;` and the
prelude re-export of `dom::mount`.
