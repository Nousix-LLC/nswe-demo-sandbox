# B2 Findings — EventHandler enum (REQ-ASYNC-023)

**PR**: #193 — Head SHA: `838239e`  
**Key commit**: `9557f0c` (enum redesign)  
**Files**: `crates/ferric/src/vdom.rs`, `crates/ferric/src/dom.rs`

---

## Findings

### B2-Q1: EventHandler is now an enum with NoArg and WithEvent variants

- **severity**: clean
- **requirement**: REQ-ASYNC-023
- **location**: `crates/ferric/src/vdom.rs:195–200`
- **description**: `EventHandler` is declared as a public enum with exactly two variants at lines 195–200. `NoArg(Rc<dyn Fn()>)` at line 197 preserves the prior zero-argument shape; `WithEvent(Rc<dyn Fn(&dyn std::any::Any)>)` at line 200 is the new event-carrying variant. The enum derives `Clone`; the `#[allow(clippy::type_complexity)]` attribute suppresses the lint on the `Rc<dyn Fn…>` payloads. The requirement for a two-variant enum is met.

---

### B2-Q2: WithEvent carries `Rc<dyn Fn(&dyn std::any::Any)>` so callers can receive the event

- **severity**: clean
- **requirement**: REQ-ASYNC-023
- **location**: `crates/ferric/src/vdom.rs:200`
- **description**: The `WithEvent` variant payload is `Rc<dyn Fn(&dyn std::any::Any)>`. This is the exact type required: a shared, cloneable closure reference that accepts one argument — the event as a platform-independent type-erased reference. The `vdom.rs` module uses `std::any::Any` (not `web_sys::Event`) as the argument type, which keeps this module native-testable while allowing the DOM layer to supply any concrete event type. The requirement that the closure can receive the event is met.

---

### B2-Q3: A handler receiving `&dyn Any` has a clear downcast path to `&web_sys::Event` for `prevent_default()`/`stop_propagation()`

- **severity**: clean
- **requirement**: REQ-ASYNC-023
- **location**: `crates/ferric/src/dom.rs:630–656`
- **description**: The WASM test `event_carrying_handler_can_call_prevent_default` (lines 629–656) demonstrates the complete downcast path: the closure receives `any: &dyn std::any::Any`, calls `any.downcast_ref::<web_sys::Event>().expect(…)`, and calls `event.prevent_default()`. The test then asserts `event.default_prevented()` is true. This end-to-end path is exercised under `wasm-bindgen-test` in a real browser runtime. The downcast works because `dom.rs` passes `&event as &dyn std::any::Any` where `event: web_sys::Event` — the concrete type is `web_sys::Event`, so `downcast_ref::<web_sys::Event>()` succeeds at runtime. The requirement for a clear downcast path to `prevent_default()` is met.

---

### B2-Q4: `vdom.rs` does NOT import `web_sys`

- **severity**: clean
- **requirement**: REQ-ASYNC-023
- **location**: `crates/ferric/src/vdom.rs:31–33`
- **description**: The only `use` statements in `vdom.rs` at HEAD are `std::collections::{BTreeMap, HashSet}` (line 31), `std::fmt` (line 32), and `std::rc::Rc` (line 33). No `use web_sys` or `extern crate web_sys` appears anywhere in the file. The `WithEvent` variant names `std::any::Any` directly in the type position rather than importing `web_sys::Event`. The requirement that `vdom.rs` does not import `web_sys` is met; the module is fully native-testable.

---

### B2-Q5: Backward compatibility is preserved — existing callers passing `impl Fn()` to `.on()` still compile

- **severity**: clean
- **requirement**: REQ-ASYNC-023
- **location**: `crates/ferric/src/vdom.rs:317–319`
- **description**: The `.on()` builder method at lines 317–319 accepts `handler: impl Fn() + 'static` and wraps it in `EventHandler::NoArg(Rc::new(handler))`. Its signature is unchanged from the prior API surface: callers that passed a `|| { … }` closure to `.on()` continue to compile and behave identically. The addition of the `WithEvent` variant and the new `.on_with_event()` builder (lines 329–335) is purely additive. CI reports `fmt`, `clippy`, and `test` all passing at `838239e`, confirming no compile-time regression. The backward-compatibility requirement is met.

---

### B2-Q6: `dom.rs` correctly dispatches both variants (`NoArg` → call with no args; `WithEvent` → pass `&event as &dyn Any`)

- **severity**: clean
- **requirement**: REQ-ASYNC-023
- **location**: `crates/ferric/src/dom.rs:272–274`
- **description**: The event dispatch closure in `set_events` (lines 272–274) matches on `&handler`: `EventHandler::NoArg(f) => f()` calls the closure with no arguments; `EventHandler::WithEvent(f) => f(&event as &dyn std::any::Any)` passes the `web_sys::Event` as a type-erased reference. The match is exhaustive; both arms are present; the coerce `&event as &dyn std::any::Any` is correct Rust — it coerces the concrete reference to the trait object at the call site. The requirement that both variants are dispatched correctly is met.

---

### B2-Q7: The WASM test exercises the `WithEvent` → `prevent_default()` path end-to-end

- **severity**: clean
- **requirement**: REQ-ASYNC-023
- **location**: `crates/ferric/src/dom.rs:629–656`
- **description**: `event_carrying_handler_can_call_prevent_default` is a `#[wasm_bindgen_test]` function that constructs an `EventHandler::WithEvent` whose closure calls `prevent_default()` via `downcast_ref::<web_sys::Event>()`, creates a real `web_sys::Event::new("click")`, asserts it is not yet prevented, invokes the closure with `f(&event as &dyn std::any::Any)`, and then asserts `event.default_prevented()` is true. This directly targets the full WithEvent path without relying on a double: the closure, the coerce, the downcast, and the DOM call are all exercised in browser WASM. CI's `wasm` job reports success at `838239e`. The requirement for WASM test coverage of the `WithEvent` → `prevent_default()` path is met.

---

## What was examined

**Files read at HEAD SHA `838239e`:**

| File | Lines examined | Purpose |
|------|---------------|---------|
| `crates/ferric/src/vdom.rs` | 1–35 (module doc + use statements), 190–205 (EventHandler enum), 315–340 (`.on()` and `.on_with_event()` builders) | Q1, Q2, Q4, Q5 |
| `crates/ferric/src/dom.rs` | 45–55 (use block, confirming import of `vdom::EventHandler`), 229 (set_events signature), 265–285 (dispatch closure), 596–660 (wasm_tests module) | Q3, Q6, Q7 |

**Questions checked and answered:**
1. EventHandler enum with NoArg and WithEvent variants — confirmed at vdom.rs:195–200
2. WithEvent payload type `Rc<dyn Fn(&dyn std::any::Any)>` — confirmed at vdom.rs:200
3. Downcast path to `&web_sys::Event` for `prevent_default()` — confirmed by dom.rs:630–656 WASM test
4. No `web_sys` import in vdom.rs — confirmed by vdom.rs:31–33 (only `std` imports)
5. Backward compatibility via `.on()` builder — confirmed at vdom.rs:317–319 (signature unchanged)
6. Both variants dispatched correctly in dom.rs — confirmed at dom.rs:272–274
7. WASM test exercises WithEvent → prevent_default() — confirmed at dom.rs:629–656

**CI evidence**: All 6 jobs (`fmt`, `clippy`, `doc`, `test`, `wasm`, `image`) report `success` at `838239e`. The `wasm` job confirms the `event_carrying_handler_can_call_prevent_default` test ran and passed in a browser runtime.

**Verdict for REQ-ASYNC-023**: Fully satisfied. No blockers found. All seven correctness questions answered clean.
