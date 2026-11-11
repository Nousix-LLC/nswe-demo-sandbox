## Findings — Concern 7 (API and Contract Stability)

---

### Finding C7-1

- **severity**: clean
- **concern**: api-stability
- **location**: `crates/ferric/src/vdom.rs:62` (`VElement::on`)

`VElement::on()` accepts `impl Fn() + 'static` and wraps the closure in `EventHandler::NoArg` internally. The method signature is **unchanged from before this PR**. Any caller written as:

```rust
element.on(EventKind::Click, || { /* ... */ })
```

continues to compile without modification. The `NoArg` wrapping is an implementation detail; callers never see `EventHandler` through this path.

---

### Finding C7-2

- **severity**: clean
- **concern**: api-stability
- **location**: `crates/ferric/src/lib.rs:38`

`EventHandler` is not re-exported from `ferric::prelude` — before this PR or after. The idiomatic import path (`use ferric::prelude::*`) never exposed `EventHandler` as a nameable type to external callers. Callers who built their applications through the prelude are unaffected by the type alias → enum change.

The flat non-prelude re-export (`pub use crate::vdom::{EventKind, VElement, VNode}`) also does not include `EventHandler`, before or after this PR.

A caller who had explicitly imported `ferric::vdom::EventHandler` and treated it as `Rc<dyn Fn()>` (the old type alias) would break — but that pathway was never part of the documented prelude surface and the library is pre-1.0. No action needed for the PR gate; the note below on `#[non_exhaustive]` is the forward-proofing concern.

---

### Finding C7-3

- **severity**: non-blocker
- **concern**: api-stability
- **location**: `crates/ferric/src/lib.rs:40–41` and `crates/ferric/src/form.rs:224`

`Bind` and `FormField` are added to `ferric::prelude`:

```rust
pub use crate::form::{Bind, FormField};
```

`Bind::on_input_handler()` returns `EventHandler`. Callers who write `use ferric::prelude::*` and call `bind.on_input_handler()` receive a value of a type they cannot name without an additional import — `EventHandler` is only reachable at `ferric::vdom::EventHandler`.

The same applies to `on_input_event_handler()` on WASM targets.

Adding `EventHandler` to the prelude (alongside `Bind`) would remove the extra import requirement. This is a usability gap, not a correctness gap.

**What satisfies this finding**: add `pub use crate::vdom::EventHandler;` to the `prelude` block in `lib.rs`.

---

### Finding C7-4

- **severity**: clean
- **concern**: api-stability
- **location**: `crates/ferric/src/form.rs:197–259`

`on_input_event_handler()` on `Bind<T>` is correctly gated to `#[cfg(target_arch = "wasm32")]` because it references `web_sys::Event` and `HtmlInputElement`, which do not exist on native targets. The method is documented with:

- a numbered four-step behavior description
- the failure mode (silent no-op if `target()` is absent or the target is not `<input>`)
- the reason for the `wasm32` gate
- cross-links to `on_input_handler` and `set_input`

The companion WASM integration test (`on_input_event_handler_updates_signal_from_dom_value`) exercises the full DOM → signal path with a real inserted element and a dispatched synthetic event, covering REQ-ASYNC-042. Documentation and coverage are adequate.

---

### Finding C7-5

- **severity**: clean
- **concern**: api-stability
- **location**: `crates/ferric/src/async_resource.rs`

`create_resource` follows the library's established `create_*` naming convention: `create_signal`, `create_effect`, `create_memo`, now `create_resource`. The function takes a reactive source closure and a fetcher closure, matching the pattern used by reactive libraries in this space. No naming convention deviation.

---

### Finding C7-6

- **severity**: non-blocker
- **concern**: api-stability
- **location**: `crates/ferric/src/async_resource.rs:1` (`ResourceState<T>`) and `crates/ferric/src/vdom.rs` (`EventHandler`)

`ResourceState<T>` and `EventHandler` are both public enums with no `#[non_exhaustive]` attribute:

```rust
pub enum ResourceState<T> {
    Loading,
    Ready(T),
    Failed(String),
}

pub enum EventHandler {
    NoArg(Rc<dyn Fn()>),
    WithEvent(Rc<dyn Fn(&dyn std::any::Any)>),
}
```

Any caller who writes an exhaustive `match` on either type will get a compile error if a new variant is added in a future minor version. `ResourceState` in particular is intended to be matched by callers (the `suspense` primitive is built around reading it). Without `#[non_exhaustive]`, adding a fourth state (e.g., `Cancelled` or `Stale`) is a major version break.

The library is pre-1.0, so the immediate semver cost is bounded. This is a forward-proofing gap rather than an active break.

**What satisfies this finding**: add `#[non_exhaustive]` to both enums.

Note: issue #196 (rename `Failed` → `Error`) is a distinct concern about variant naming, not the exhaustiveness guard. This finding is not a re-raise of #196.

---

## What was examined

**`VElement::on()` and `EventHandler::NoArg` transparency**
- Read `vdom.rs` diff lines covering `EventHandler` definition and `VElement::on()` implementation.
- Verified `on()` signature (`impl Fn() + 'static`) is unchanged; the `NoArg` wrapping is an internal detail invisible to callers. All pre-PR usage of `element.on(kind, closure)` continues to compile.

**EventHandler public re-export surface**
- Read `lib.rs` diff to identify all flat `pub use` and `prelude` exports.
- Confirmed `EventHandler` is not in `prelude` before or after this PR; `EventKind, VElement, VNode` remain the vdom prelude surface. The type alias → enum change does not break idiomatic prelude callers.
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
- None of these overlap with the findings above. Findings C7-3 and C7-6 are distinct concerns not present in #196–#201.
