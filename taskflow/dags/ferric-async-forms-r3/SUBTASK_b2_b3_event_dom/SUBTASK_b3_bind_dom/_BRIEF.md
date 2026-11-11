# Task: B3 — Bind DOM→signal plumbing (REQ-ASYNC-042)

## Task Specification

**Slug**: SUBTASK_b3_bind_dom  
**Task Kind**: standard  
**Depends on**: `SUBTASK_b2_event_handler` (must be committed and pushed before this task starts)  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Satisfy REQ-ASYNC-042 by adding an event-carrying input handler to `Bind<T>` in `form.rs` that reads the DOM element's current value and writes it directly to the field signal, and verifying the DOM→signal direction with a WASM integration test.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project constraints | `../_GLOBAL.md` | Binding constraints for this subtree |
| Parent task constraints | `../../../_GLOBAL.md` | Branch, CI requirements |
| Current `form.rs` | `crates/ferric/src/form.rs` on `work/ferric-async-forms-r2` (after B2 commit) | `Bind<T>` struct, `on_input_handler()`, `input_buf`, `set_input()`, existing 18 tests |
| Current `vdom.rs` | `crates/ferric/src/vdom.rs` on `work/ferric-async-forms-r2` (after B2 commit) | `EventHandler` enum, `VElement::on_with_event()` builder (added by B2) |
| Current `dom.rs` | `crates/ferric/src/dom.rs` on `work/ferric-async-forms-r2` (after B2 commit) | Existing WASM test pattern and imports |

---

## Scope

### What changes

**`crates/ferric/src/form.rs`**

Add a new method `Bind::on_input_event_handler()` that returns `EventHandler::WithEvent(...)`. This method is gated with `#[cfg(target_arch = "wasm32")]` because it references `web_sys` DOM types that are not available on native targets.

The closure captures the field's raw signal (`self.raw`, a `Signal<String>`). When called with `&dyn Any`, the closure:
1. Downcasts the argument to `&web_sys::Event`.
2. Calls `event.target()` to get the `EventTarget`.
3. Casts the target to `HtmlInputElement` using `wasm_bindgen::JsCast::dyn_into`.
4. Reads `input_el.value()`.
5. Calls `raw.set(value)` to update the field signal directly.

The `dyn_into` cast consumes the target; use `unchecked_into` only if the type is guaranteed. If any step fails (e.g., target is not an `HtmlInputElement`), the closure returns without updating the signal — no panic.

The existing `on_input_handler()` (zero-argument, all platforms) and `set_input()` are preserved unchanged. All 18 existing native tests that call `bind.set_input(value)` and then invoke `on_input_handler()` must continue to pass.

The `form.rs` file may add `#[cfg(target_arch = "wasm32")]` imports for `web_sys::{Event, HtmlInputElement}` and `wasm_bindgen::JsCast`. These imports are platform-gated and do not affect native compilation.

**WASM test for REQ-ASYNC-042**

Add at least one WASM test (marked `#[wasm_bindgen_test]`) that exercises the full DOM→signal path:

1. Create a `web_sys::HtmlInputElement` by creating an `<input>` element via `web_sys::window().unwrap().document().unwrap().create_element("input")`.
2. Set the element's `value` property to a known string (e.g., `"hello"`).
3. Construct a `Bind<String>` (or equivalent `Signal<String>` and use `on_input_event_handler` directly).
4. Create an `EventHandler` by calling `bind.on_input_event_handler()`.
5. Dispatch the handler by calling the inner closure with `&event as &dyn std::any::Any`, where `event` is a `web_sys::Event` whose `target()` returns the `<input>` element. (This requires the input element to be inserted into the document and a real input event dispatched, or the handler called directly with a synthetically constructed invocation.)
6. Assert that the signal value equals `"hello"`.

The test may live in `form.rs` or `dom.rs` alongside the existing WASM tests. The test must run under `wasm-pack test --headless --firefox`.

**Note on test approach**: The simplest approach is to insert the `<input>` into the document body, set its value, dispatch a synthetic `InputEvent` using `web_sys::Event::new("input")`, and wire up the handler via `add_event_listener_with_callback`. Alternatively, the closure can be called directly with a hand-constructed `Event` reference if the target can be set. Either approach is acceptable as long as the test verifies that `bind.on_input_event_handler()` correctly propagates the DOM value to the signal.

---

## Output Specification

### Declared output

Committed change(s) on `work/ferric-async-forms-r2` covering `form.rs`. Commits must be pushed to the remote before this task is declared complete.

---

## Success Criteria

- [ ] `Bind::on_input_event_handler()` added to `form.rs`, gated with `#[cfg(target_arch = "wasm32")]`.
- [ ] The handler closure reads `HtmlInputElement::value()` from `event.target()` and calls `raw.set(value)`.
- [ ] A WASM test fires an `input` event on a bound `<input>` and verifies the signal updates to the typed value (REQ-ASYNC-042).
- [ ] All 18 existing native `form.rs` tests pass.
- [ ] All existing native and WASM tests in `async_resource.rs` pass.
- [ ] `cargo test -p ferric` passes (native).
- [ ] `wasm-pack test --headless --firefox crates/ferric` passes (WASM).
- [ ] `cargo clippy -p ferric` passes with no new warnings.
- [ ] Commit(s) pushed to `work/ferric-async-forms-r2`.

---

## Constraints

- Do not modify `on_input_handler()`, `set_input()`, or any existing test.
- `cfg(target_arch = "wasm32")` gate must be applied to any `web_sys` imports added to `form.rs`.
- Do not address NB-1 through NB-6.
- Infrastructure details must not appear in committed files.
