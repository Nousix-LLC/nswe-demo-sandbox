# Task: B2 — Event-carrying EventHandler (REQ-ASYNC-023)

## Task Specification

**Slug**: SUBTASK_b2_event_handler  
**Task Kind**: standard  
**Depends on**: none (within this subtree; `SUBTASK_b1_reactive_resource` is already on the branch)  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Satisfy REQ-ASYNC-023 by redesigning `EventHandler` in `vdom.rs` from a zero-argument type alias to an enum that also supports an event-carrying variant, updating `dom.rs` to pass the `web_sys::Event` to event-carrying handlers, keeping all existing zero-argument call sites working, and demonstrating `prevent_default()` callability via a WASM test.

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project constraints | `../_GLOBAL.md` | Binding constraints for this subtree |
| Parent task constraints | `../../../_GLOBAL.md` | Branch, CI requirements, no-web_sys rule |
| Current `vdom.rs` | `crates/ferric/src/vdom.rs` on `work/ferric-async-forms-r2` | `EventHandler` definition (line ~190), `VElement::on()` builder (line ~304), `VElement.events` field |
| Current `dom.rs` | `crates/ferric/src/dom.rs` on `work/ferric-async-forms-r2` | `set_events` function, event dispatch closure, stash/detach mechanism |
| Current `form.rs` | `crates/ferric/src/form.rs` on `work/ferric-async-forms-r2` | `Bind::on_input_handler()` return type (must compile after EventHandler changes) |

---

## Scope

### What changes

**`crates/ferric/src/vdom.rs`**

Change `EventHandler` from a type alias to an enum. The enum must have exactly two variants: one for zero-argument handlers and one for event-carrying handlers. The event-carrying variant must use a platform-independent type for the event parameter — the design decision in `../_GLOBAL.md` specifies `Rc<dyn Fn(&dyn std::any::Any)>` and no `web_sys` import in `vdom.rs`.

The `VElement::on()` builder currently constructs `EventHandler` by pushing `Rc::new(handler)` directly. After the change it must wrap in the zero-argument variant. Its public signature `fn on(mut self, kind: EventKind, handler: impl Fn() + 'static) -> Self` does not change — existing callers using `.on(kind, move || { ... })` must compile and behave identically.

Add a companion builder method `on_with_event(kind: EventKind, handler: impl Fn(&dyn std::any::Any) + 'static) -> Self` on `VElement` for callers that need the event-carrying variant.

`form.rs::Bind::on_input_handler()` currently returns `EventHandler` (the former type alias `Rc<dyn Fn()>`). After this change its return type is still `EventHandler` (the enum), but it must return the zero-argument variant — update its body accordingly. This is a pure compatibility fix; the behaviour and test expectations do not change.

**`crates/ferric/src/dom.rs`**

Update the event dispatch closure inside `set_events` to match on the `EventHandler` variant and call the appropriate branch. When the variant is event-carrying, pass the `web_sys::Event` as `&dyn std::any::Any`. The stash/detach mechanism and all other DOM plumbing are unchanged.

**Test for REQ-ASYNC-023**

Add at least one WASM test (marked `#[wasm_bindgen_test]`) that:

1. Constructs an event-carrying handler closure that downcasts its `&dyn Any` argument to `&web_sys::Event` and calls `prevent_default()` on it.
2. Creates a real `web_sys::Event` via `web_sys::Event::new("click")` (or equivalent).
3. Calls the handler with the event (using the closure directly or by going through the full dispatch path in `set_events`).
4. Asserts that `event.default_prevented()` returns `true`.

The test may live in `dom.rs` (alongside existing WASM tests) or in a new test module in `vdom.rs`; either is acceptable. The test must run under `wasm-pack test --headless --firefox`.

---

## Output Specification

### Declared output

Committed change(s) on `work/ferric-async-forms-r2` covering `vdom.rs`, `dom.rs`, and the compatibility fix in `form.rs`. Commits must be pushed to the remote before this task is declared complete.

---

## Success Criteria

- [ ] `EventHandler` in `vdom.rs` is an enum with a zero-argument variant and an event-carrying variant; no `web_sys` import in `vdom.rs`.
- [ ] `VElement::on()` signature is unchanged; existing callers using `.on(kind, closure)` compile without modification.
- [ ] `VElement::on_with_event()` builder method added for the event-carrying variant.
- [ ] `dom.rs` dispatch closure passes `web_sys::Event` to event-carrying handlers via `&dyn Any`.
- [ ] `form.rs::Bind::on_input_handler()` updated to return the zero-argument variant (pure compat fix; no semantic change).
- [ ] A WASM test demonstrates that a handler can call `prevent_default()` and `event.default_prevented()` returns `true` (REQ-ASYNC-023).
- [ ] All 18 existing native `form.rs` tests pass.
- [ ] All existing native and WASM tests in `async_resource.rs` pass.
- [ ] `cargo test -p ferric` passes (native).
- [ ] `cargo clippy -p ferric` passes with no new warnings.
- [ ] Commit(s) pushed to `work/ferric-async-forms-r2`.

---

## Constraints

- `vdom.rs` MUST NOT import `web_sys`.
- Zero-argument callers of `.on()` must work without syntax change.
- Do not change `Bind::set_input()` or `on_input_handler()` behaviour — only the return type wrapping.
- Do not address NB-1 through NB-6.
- Infrastructure details must not appear in committed files.
