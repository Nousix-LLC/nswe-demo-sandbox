## Sub-Finding: Downcast Reachability

- **severity**: clean
- **concern**: EventHandler::WithEvent downcast safety
- **location**: N/A
- **description**: The `EventHandler::WithEvent` dispatch path in `dom.rs` does not expose a panic-on-downcast DoS surface. The dispatch site passes `&event as &dyn std::any::Any` to the handler; the downcast occurs in the handler, not in `dom.rs` itself. The concrete type at the coercion point is always `web_sys::Event`, enforced by the `Closure` type parameter: `Closure::wrap(... as Box<dyn FnMut(web_sys::Event)>)` in `set_events()`. wasm-bindgen generates JS glue from this type, so the value arriving on the Rust side of the boundary carries `TypeId::of::<web_sys::Event>()` in its `dyn Any` vtable. Any `downcast_ref::<web_sys::Event>()` on that value succeeds by construction — the browser has no mechanism to inject a different concrete type.

  The only unguarded `.expect("expected web_sys::Event")` on a `downcast_ref` in the diff is inside the `#[wasm_bindgen_test]` test closure in `dom.rs`'s `wasm_tests` module (`event_carrying_handler_can_call_prevent_default`). That attribute gates the code out of the production Wasm binary; it is unreachable from browser event delivery. Even in its test context it cannot panic, because the test manually constructs `web_sys::Event::new("click")` and passes it through the same `&event as &dyn Any` coercion, so the TypeId matches.

  Production code in `form.rs` (`on_input_event_handler`) uses a fully guarded pattern throughout: `if let Some(event) = any.downcast_ref::<Event>()`. If the downcast were somehow to fail (which the type constraint prevents), the closure returns without updating the signal — no panic, no DoS.

  Sub-check answers:
  1. **Concrete type at dispatch site**: always `web_sys::Event`. The `Closure<Box<dyn FnMut(web_sys::Event)>>` type parameter is the proof; it is not polymorphic.
  2. **Dispatch mechanism in `dom.rs`**: not a downcast at all — it coerces `&web_sys::Event` to `&dyn Any` and delegates. The choice of guarded vs. unguarded is in the caller-supplied handler, not in `dom.rs`.
  3. **Unguarded path reachability**: the only unguarded `.expect()` is in `#[wasm_bindgen_test]` test code. A remote actor cannot reach test code. Even if reachable, it cannot panic because the TypeId is `web_sys::Event` by construction.
  4. **Panic reachability from browser event delivery**: no panic path exists. Type guarantee and test-only scope both independently rule it out.

## What was examined

- `crates/ferric/src/dom.rs` diff (commit `9557f0c`): `set_events()` function — the `Closure::wrap(... as Box<dyn FnMut(web_sys::Event)>)` declaration establishing the type constraint, and the `EventHandler::WithEvent(f) => f(&event as &dyn std::any::Any)` dispatch arm.
- `crates/ferric/src/dom.rs` diff (commit `9557f0c`): `wasm_tests` module — the `#[wasm_bindgen_test]` annotated test `event_carrying_handler_can_call_prevent_default`, which contains the only unguarded `.downcast_ref::<web_sys::Event>().expect(...)` in the diff. Confirmed attribute scope limits this to test compilation.
- `crates/ferric/src/vdom.rs` diff (commit `9557f0c`): `EventHandler` enum definition — `WithEvent(Rc<dyn Fn(&dyn std::any::Any)>)` variant and the absence of `web_sys` imports, confirming type erasure is intentional for native testability.
- `crates/ferric/src/form.rs` diff (commit `838239e`): `on_input_event_handler()` — production `WithEvent` handler; confirmed guarded `if let Some(event) = any.downcast_ref::<Event>()` with no panic path.
- wasm-bindgen `Closure` type parameter contract: the type parameter of `Closure` determines the generated JS glue; a `Closure<dyn FnMut(web_sys::Event)>` guarantees the Rust side receives `web_sys::Event` on every call, regardless of which JS `Event` subtype the browser delivers.
