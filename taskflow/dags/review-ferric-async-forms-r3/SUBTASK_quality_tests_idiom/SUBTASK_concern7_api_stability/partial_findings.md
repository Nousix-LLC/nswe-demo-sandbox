## Findings

- **severity**: clean
  **concern**: api-stability
  **location**: `crates/ferric/src/vdom.rs:62`
  **description**: `VElement::on()` backward compatibility checked. The method signature (`impl Fn() + 'static`) is unchanged from before this PR. The `EventHandler::NoArg` wrapping is an internal detail invisible to callers; any pre-PR usage of `element.on(kind, closure)` continues to compile without modification.

- **severity**: clean
  **concern**: api-stability
  **location**: `crates/ferric/src/lib.rs:38`
  **description**: `EventHandler` type alias → enum change checked against the prelude surface. `EventHandler` is not re-exported from `ferric::prelude` before or after this PR; `EventKind`, `VElement`, and `VNode` remain the vdom prelude surface. The flat non-prelude re-export also excludes `EventHandler`. Callers using `use ferric::prelude::*` are unaffected by this change.

- **severity**: non-blocker
  **concern**: api-stability
  **location**: `crates/ferric/src/lib.rs:40–41`
  **description**: `Bind` and `FormField` are added to `ferric::prelude`, but `Bind::on_input_handler()` returns `EventHandler`, which is not in the prelude. Callers using `use ferric::prelude::*` who call `bind.on_input_handler()` receive a value of a type they cannot name without an additional `use ferric::vdom::EventHandler` import. This is a usability gap, not a correctness break. Satisfying condition: add `pub use crate::vdom::EventHandler;` to the prelude block in `lib.rs`.

- **severity**: clean
  **concern**: api-stability
  **location**: `crates/ferric/src/form.rs:197–259`
  **description**: `on_input_event_handler()` on `Bind<T>` checked. The method is correctly gated to `#[cfg(target_arch = "wasm32")]`. Documentation covers the four-step behavior description, the failure mode (silent no-op if `target()` is absent or the target is not `<input>`), the reason for the `wasm32` gate, and cross-links to `on_input_handler` and `set_input`. The companion WASM integration test (`on_input_event_handler_updates_signal_from_dom_value`) exercises the full DOM → signal path with a real inserted element and a dispatched synthetic event, covering REQ-ASYNC-042. Documentation and coverage are adequate.

- **severity**: clean
  **concern**: api-stability
  **location**: `crates/ferric/src/async_resource.rs`
  **description**: `create_resource` naming convention checked. The function follows the library's established `create_*` pattern: `create_signal`, `create_effect`, `create_memo`, `create_resource`. The function takes a reactive source closure and a fetcher closure, consistent with the pattern used in this space. No naming convention deviation found.

- **severity**: non-blocker
  **concern**: api-stability
  **location**: `crates/ferric/src/async_resource.rs:1`
  **description**: `ResourceState<T>` and `EventHandler` are both public enums with no `#[non_exhaustive]` attribute. Any caller writing an exhaustive `match` on either type will get a compile error if a new variant is added in a future minor version. `ResourceState` is intended to be matched by callers (the `suspense` primitive is built around reading it); adding a fourth state (e.g., `Cancelled` or `Stale`) would be a major version break without the guard. The library is pre-1.0, so the immediate semver cost is bounded — this is a forward-proofing gap, not an active break. Satisfying condition: add `#[non_exhaustive]` to both enums. (Distinct from #196, which concerns variant naming, not the exhaustiveness guard.)

## What was examined

**`VElement::on()` and `EventHandler::NoArg` transparency**
- Read `vdom.rs` diff lines covering `EventHandler` definition and `VElement::on()` implementation.
- Verified `on()` signature (`impl Fn() + 'static`) is unchanged; the `NoArg` wrapping is an internal detail invisible to callers. All pre-PR usage of `element.on(kind, closure)` continues to compile.

**EventHandler public re-export surface**
- Read `lib.rs` diff to identify all flat `pub use` and `prelude` exports.
- Confirmed `EventHandler` is not in `prelude` before or after this PR; `EventKind`, `VElement`, `VNode` remain the vdom prelude surface. The type alias → enum change does not break idiomatic prelude callers.
- Identified the gap: `Bind` is in prelude but its return type `EventHandler` is not.

**on_input_event_handler() documentation and visibility**
- Read the full `form.rs` diff (531 lines added as a new file).
- Verified `on_input_event_handler()` is `pub`, `#[cfg(target_arch = "wasm32")]`, and carries a complete doc comment with numbered behavior, failure modes, and cross-links.
- Read the WASM integration test block to confirm it exercises REQ-ASYNC-042 end-to-end with a real DOM element.

**create_resource naming and API conventions**
- Read `async_resource.rs` public API surface: `ResourceState<T>`, `Resource<T>`, `create_resource`, `suspense`.
- Compared `create_resource` name to `create_signal`, `create_effect`, `create_memo` in `signal.rs` — consistent pattern.
- Read `Resource<T>` struct: private `signal` field (struct-literal construction blocked), clean constructor methods.

**Previously filed issues #196–#201 — confirmed non-overlap**
- #196 `ResourceState::Failed` naming, #197 workspace dep, #198 static_event_kinds sync, #199 lifecycle teardown tests, #200 test name, #201 KeyPress deprecation.
- None overlap with the findings above. Findings C7-3 and C7-6 are distinct concerns not present in #196–#201.
