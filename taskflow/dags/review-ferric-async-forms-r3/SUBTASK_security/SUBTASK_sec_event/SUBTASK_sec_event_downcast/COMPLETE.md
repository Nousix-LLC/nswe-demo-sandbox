# COMPLETE: SUBTASK_sec_event_downcast

**Status**: completed  
**Task**: Assess panic-on-downcast reachability in `EventHandler::WithEvent`  
**Verdict**: clean — no DoS surface

## Summary

The `EventHandler::WithEvent` dispatch path in `crates/ferric/src/dom.rs` does not expose a panic-on-downcast Denial-of-Service surface reachable by a remote actor.

**Evidence:**

1. The `Closure` at the dispatch site is typed `Box<dyn FnMut(web_sys::Event)>`. This constrains the event parameter to `web_sys::Event` by construction; wasm-bindgen generates JS glue from this type, ensuring the Rust side always receives `web_sys::Event` regardless of JS-side subtype. The `TypeId` stored in the `&dyn Any` vtable at coercion (`f(&event as &dyn std::any::Any)`) is therefore always `TypeId::of::<web_sys::Event>()`.

2. The only unguarded `.downcast_ref::<web_sys::Event>().expect(...)` in the diff is in the `#[wasm_bindgen_test]`-annotated `event_carrying_handler_can_call_prevent_default` test closure in `dom.rs`. This is test code, not compiled into the production Wasm binary, and unreachable from browser event delivery.

3. The production handler in `crates/ferric/src/form.rs` (`on_input_event_handler`) uses a fully guarded `if let Some(event) = any.downcast_ref::<Event>()` pattern with no panic path.

## Output

- `finding_downcast.md` — sub-finding with severity `clean`, evidence cited, all four sub-checks answered
