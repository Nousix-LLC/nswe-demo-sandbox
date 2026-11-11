# COMPLETE — SUBTASK_b2_event_handler

**Task**: B2 — Event-carrying EventHandler (REQ-ASYNC-023)  
**Status**: COMPLETED  
**Commit**: `9557f0c` on `work/ferric-async-forms-r2`

---

## Work done

### `crates/ferric/src/vdom.rs`
- Replaced `pub type EventHandler = Rc<dyn Fn()>` with an enum:
  ```rust
  #[allow(clippy::type_complexity)]
  #[derive(Clone)]
  pub enum EventHandler {
      NoArg(Rc<dyn Fn()>),
      WithEvent(Rc<dyn Fn(&dyn std::any::Any)>),
  }
  ```
- Updated `VElement::on()` to wrap `Rc::new(handler)` in `EventHandler::NoArg(...)` — existing callers unchanged.
- Added `VElement::on_with_event()` builder that wraps in `EventHandler::WithEvent(...)`.
- No `web_sys` import added (module remains fully native-testable).

### `crates/ferric/src/dom.rs`
- Updated `set_events` dispatch closure to match on the `EventHandler` variant:
  - `NoArg(f)` → `f()`
  - `WithEvent(f)` → `f(&event as &dyn std::any::Any)`
- Added WASM test `event_carrying_handler_can_call_prevent_default` (REQ-ASYNC-023):
  constructs a `WithEvent` handler that downcasts `&dyn Any` to `&web_sys::Event` and calls
  `prevent_default()`; asserts `event.default_prevented()` returns `true`.

### `crates/ferric/src/form.rs`
- `Bind::on_input_handler()` now returns `EventHandler::NoArg(Rc::new(move || { ... }))`.
- Updated 4 test call sites from `handler()` to `if let EventHandler::NoArg(f) = &handler { f(); }`.

### `crates/ferric/src/component.rs`
- Updated one test call site from `(e.events[0].1)()` to match on `EventHandler::NoArg(f) { f(); }`.

---

## Verification

- `cargo test -p ferric`: 83 passed, 0 failed
- `cargo clippy -p ferric`: 0 warnings
- `cargo build -p ferric --target wasm32-unknown-unknown`: success (WASM test compiles)
- All 18 native `form.rs` tests pass
- All `async_resource.rs` native tests pass
