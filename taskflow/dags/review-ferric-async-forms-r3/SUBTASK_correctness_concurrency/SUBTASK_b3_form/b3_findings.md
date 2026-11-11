# B3 Findings — Bind::on_input_event_handler (form.rs)

**Requirement**: REQ-ASYNC-042  
**Commit**: `838239e` — "B3 (REQ-ASYNC-042): add Bind::on_input_event_handler() + WASM test"  
**File reviewed**: `crates/ferric/src/form.rs`

---

## Findings

### 1. Method existence and signature

- **severity**: clean
- **requirement**: REQ-ASYNC-042
- **location**: `crates/ferric/src/form.rs:215–216`
- **description**: `Bind<T>` has `on_input_event_handler(&self) -> EventHandler`. The method is `pub` and declared inside `impl<T: FromStr + Clone + 'static> Bind<T>`. Signature matches the requirement.

---

### 2. Return type is EventHandler::WithEvent

- **severity**: clean
- **requirement**: REQ-ASYNC-042
- **location**: `crates/ferric/src/form.rs:218`
- **description**: The method constructs and returns `EventHandler::WithEvent(Rc::new(...))`. Satisfies the requirement that the handler is event-carrying.

---

### 3. Downcast chain: &dyn Any → &web_sys::Event → target → HtmlInputElement → value()

- **severity**: clean
- **requirement**: REQ-ASYNC-042
- **location**: `crates/ferric/src/form.rs:219–222`
- **description**: The closure body is:
  ```rust
  if let Some(event) = any.downcast_ref::<Event>() {         // line 219
      if let Some(target) = event.target() {                 // line 220
          if let Ok(input_el) = target.dyn_into::<HtmlInputElement>() { // line 221
              raw.set(input_el.value());                     // line 222
          }
      }
  }
  ```
  All three legs of the downcast chain are present and in the correct order. `HtmlInputElement::value()` is called on the successfully cast element, and its result is written to the field's raw signal. Each step in the chain is exactly as REQ-ASYNC-042 specifies.

---

### 4. Signal write ordering — synchronous on each input event

- **severity**: clean
- **requirement**: REQ-ASYNC-042
- **location**: `crates/ferric/src/form.rs:222`
- **description**: `raw.set(input_el.value())` is called synchronously within the event closure, with no deferral (no `spawn_local`, no `create_effect`, no batching). The write happens on every `input` event that reaches the handler and completes the downcast chain. Reactive subscribers are notified immediately.

---

### 5. cfg(target_arch = "wasm32") gate — compatibility with REQ-ASYNC-042

- **severity**: clean
- **requirement**: REQ-ASYNC-042
- **location**: `crates/ferric/src/form.rs:215`
- **description**: `#[cfg(target_arch = "wasm32")]` gates the method. This is correct: the method uses `web_sys::Event` and `web_sys::HtmlInputElement`, which are browser-only types unavailable on native targets. The requirement is a browser-binding requirement — it specifies a DOM interaction that only exists on WASM. Gating to `wasm32` is therefore compatible with REQ-ASYNC-042. The WASM CI job (`wasm`) passes (run https://github.com/Nousix-LLC/nswe-demo/actions/runs/42126720006).

---

### 6. WASM test coverage — full DOM→signal path

- **severity**: clean
- **requirement**: REQ-ASYNC-042
- **location**: `crates/ferric/src/form.rs:488–530`
- **description**: The test `on_input_event_handler_updates_signal_from_dom_value` exercises the full path:

  - **(a) Real DOM element**: `document.create_element("input")` + `document.body().unwrap().append_child(&input_el)` at lines 493–496. Attaching to the document body ensures `event.target()` resolves to the element when the event is dispatched.
  - **(b) Element value set**: `input_el.set_value("hello")` at line 499 simulates user input directly on the DOM property.
  - **(c) Synthetic input event dispatched**: `web_sys::Event::new("input")` + `input_el.dispatch_event(&event)` at lines 517–518. The dispatch is synchronous in the browser; the registered `Closure` fires before `dispatch_event` returns.
  - **(d) Signal asserted**: `assert_eq!(field.raw(), "hello", "REQ-ASYNC-042: ...")` at lines 521–524 confirms the signal equals the DOM value.

  The event passing path is: browser dispatch → `Closure<dyn FnMut(web_sys::Event)>` → `f(&event as &dyn std::any::Any)` → inside `on_input_event_handler` closure → `downcast_ref::<Event>()` succeeds → `event.target()` returns the element → `dyn_into::<HtmlInputElement>()` succeeds → `raw.set(input_el.value())`. The full DOM→signal path is covered. `closure.forget()` at line 515 is the standard wasm-bindgen pattern for event listeners whose lifetime is controlled by the browser; acceptable in a test where the element is explicitly removed at the end (line 528).

---

### 7. Graceful failure on downcast chain errors

- **severity**: clean
- **requirement**: REQ-ASYNC-042
- **location**: `crates/ferric/src/form.rs:219–222`
- **description**: All three fallible steps use `if let` patterns:
  - `if let Some(event) = any.downcast_ref::<Event>()` — if the `&dyn Any` does not hold a `web_sys::Event`, the closure returns without touching the signal.
  - `if let Some(target) = event.target()` — if the event has no target, same.
  - `if let Ok(input_el) = target.dyn_into::<HtmlInputElement>()` — if the target is not an `HtmlInputElement`, same.
  
  No `unwrap()`, no `expect()`, no `panic!()` in the production closure. Failure at any step leaves the signal unchanged — no crash.

---

## What was examined

| File | Lines | Questions checked |
|------|-------|-------------------|
| `crates/ferric/src/form.rs` | 1–36 | Module-level doc, imports, cfg-gated WASM imports |
| `crates/ferric/src/form.rs` | 112–157 | `Bind<T>` struct fields (`raw`, `input_buf`) |
| `crates/ferric/src/form.rs` | 160–192 | `Bind::new`, `value_attr`, `on_input_handler`, `set_input` — context for the WASM method |
| `crates/ferric/src/form.rs` | 193–226 | `on_input_event_handler` doc comment and full implementation |
| `crates/ferric/src/form.rs` | 215 | `#[cfg(target_arch = "wasm32")]` gate |
| `crates/ferric/src/form.rs` | 216–226 | Method signature, `EventHandler::WithEvent` return, downcast chain, signal write, error paths |
| `crates/ferric/src/form.rs` | 466–530 | `wasm_tests` module: `on_input_event_handler_updates_signal_from_dom_value` test, full flow |

**REQ-ASYNC-042 verdict**: fully satisfied. All seven B3 correctness questions are clean. No blockers.
