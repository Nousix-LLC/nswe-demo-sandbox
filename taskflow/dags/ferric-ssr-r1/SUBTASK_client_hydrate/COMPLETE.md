# COMPLETE — ferric-ssr-r1-client-hydrate

## Status

Completed. Committed to branch `work/ferric-ssr-r1-client` (commit `dd8b5d2`).

## Outputs

### 1. `crates/ferric/src/hydrate.rs` — fully implemented

Replaces the `todo!()` stub with the complete hydration logic:

**Adopt pass (REQ-SSR-004 — gating bar)**
- `adopt_node` recursively walks the VNode tree and the server-rendered DOM in
  parallel. No structural DOM mutations occur for matched nodes.
- Text-boundary sentinel comments (`<!--$t-->` / `<!--/$t-->`) are skipped via
  `nth_vnode_child` / `is_sentinel_comment` / `comment_data`; they are not counted
  as logical VNode children.
- Sentinel comment nodes remain in the DOM after the adopt pass; subsequent
  sentinel-aware resolvers skip them during path navigation.

**Event wiring (REQ-SSR-005)**
- `wire_events` replicates `dom::set_events` exactly (Reflect-based stash, same
  `__ferric_on_click` / `__ferric_on_input` keys, `Closure::forget`).
- Detaches any previously stashed listener before attaching the new one, so
  re-hydration never double-fires.

**Reactive effect**
- `create_effect` wraps the render/adopt cycle. First run performs the adopt pass;
  subsequent runs call `diff` + `apply_patches_hydrated`.
- `apply_patches_hydrated` is a sentinel-aware version of `dom::apply_patches`:
  all child-index navigation uses `nth_vnode_child` to skip sentinels, keeping
  logical VNode indices aligned with physical DOM positions even when the DOM
  retains SSR-emitted comment markers.

**Mismatch detection + recovery (REQ-SSR-009)**
- Tag or text divergence at any node emits `#[cfg(debug_assertions)]`
  `console::warn_1` with the exact format from `contracts/ferric_ssr_contract.rs`:
  `"ferric hydration mismatch at [<path>]: expected <expected>, found <found>"`.
- Recovery replaces only the mismatched subtree via `replace_child`; all correctly
  adopted siblings and ancestors retain their DOM identity.

### 2. Four `wasm-bindgen-test` browser tests in `hydrate.rs`

| Test | Requirement |
|------|-------------|
| `hydrate_zero_mutations_during_adopt_pass` | REQ-SSR-004 (gating bar) |
| `hydrate_wires_event_handlers_onto_adopted_element` | REQ-SSR-005 |
| `hydrate_detects_and_recovers_tag_mismatch` | REQ-SSR-009 |
| `hydrate_mismatch_recovery_preserves_sibling_identity` | REQ-SSR-009 |

## Verification

- `cargo check -p ferric` (native): clean (zero new warnings)
- `cargo check -p ferric --target wasm32-unknown-unknown`: clean
- `cargo check -p ferric --tests --target wasm32-unknown-unknown`: clean
- `cargo test -p ferric`: 43/43 native tests pass, 7/7 doc-tests pass

## Constraints respected

- `src/dom.rs`, `src/signal.rs`, `src/vdom.rs`, `src/component.rs`: unmodified
- `Cargo.toml`: unmodified (all required web-sys features were already present)
- Marker constants imported from `crate::ssr` — no independent inline strings
- Branch: `work/ferric-ssr-r1-client`
- BAR-005 (#225) not implemented (out of scope)
