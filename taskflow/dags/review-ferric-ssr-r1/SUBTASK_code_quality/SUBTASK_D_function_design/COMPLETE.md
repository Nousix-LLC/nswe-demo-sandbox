# SUBTASK_D_function_design — Completed

**Status**: completed
**Verdict**: FINDING (NON-BLOCKER)

## Output

`area_d_function_design.md` — conforms to `../contracts/findings_schema.yaml`

## Summary

Two non-blocking findings:

**D-1 (Duplication)**: Seven private helper functions in `crates/ferric/src/hydrate.rs` replicate private helpers in `crates/ferric/src/dom.rs` (`create_node`, `apply_patches_impl`, `resolve_impl`, `resolve_element_impl`, `set_events`, `event_name`, `stash_key`). The code acknowledges the duplication in comments. Rust's exhaustive match protects enum variant additions; `create_node` body drift and the hardcoded event-detachment array in `set_events` are unprotected. Resolution: extract shared helpers to `pub(crate)` visibility or a `dom_ops.rs` module.

**D-2 (Extensibility)**: `render_to_string` (`crates/ferric/src/ssr.rs:135`) is synchronous with signature `FnOnce() -> VNode`; no hook for async resource injection. When #130 lands, the signature will require a breaking change. The `chirp-server` layer carries an explicit BAR-005 seam; the ferric library layer does not. Resolution: add a provisional resource-context parameter or trait at the start of #130 planning.

**Function sizes**: CLEAN. All functions are individually reviewable. `apply_patches_impl` and `adopt_children` are the longest (~65 and ~54 lines) but are exhaustive match dispatchers — idiomatic Rust for the enum widths involved.

## Coverage

All functions in `crates/ferric/src/ssr.rs`, `crates/ferric/src/hydrate.rs`, `crates/ferric/src/dom.rs`, and `crates/chirp-server/src/ssr.rs` were examined for size, duplication, and extensibility.
