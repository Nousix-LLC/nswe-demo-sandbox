# COMPLETE — SUBTASK_q1_coupling

**Task**: Q1 — Responsibility Partitioning and Coupling Review
**Status**: completed

## Output

- `sub_findings.md` — 5 findings (2 non-blocker, 3 clean) covering all four files and the cross-module dependency graph

## Summary

All four files were examined for responsibility partitioning and cross-layer coupling. The principal finding is that `async_resource.rs` imports `crate::vdom::VNode` because `suspense()` — which uses internal thread-local sentinels shared with `create_resource` — lives in that module. This introduces a sideways dependency from the resource-lifecycle module into the view-representation layer. The coupling is mechanically necessary (splitting `suspense()` out would require exporting private sentinels) and no `web_sys` boundary is crossed, so the severity is non-blocker. A doc note naming the reason would close the legibility gap.

The other three files are clean: `vdom.rs` has no `web_sys` imports (the `dyn Any` in `WithEvent` is a std trait, not a browser type); `dom.rs` imports only from `crate::vdom` and correctly contains all concrete DOM coupling; `form.rs` imports `crate::vdom::EventHandler` and `crate::signal` with `web_sys` types gated to `#[cfg(target_arch = "wasm32")]`, and does not reach into `async_resource` at any point.

No cycles in the dependency graph. No unexpected cross-layer imports beyond the one documented in Finding 1.
