## Sub-Finding: closure.forget() Scope

- **severity**: clean
- **concern**: closure.forget() scope (test vs. production)
- **location**: crates/ferric/src/form.rs:515 (test); crates/ferric/src/dom.rs:287 (production)
- **description**: The `closure.forget()` in `form.rs` is strictly test-scoped and cannot reach production output. The `closure.forget()` in `dom.rs`'s `set_events()` is the correct stash-then-forget pattern: the closure is stored on the DOM element via `js_sys::Reflect::set` before `forget()` is called, so the JS side holds a live reference through the element property. No leak and no safety concern in either case.

## What was examined

### form.rs — test-scope gate (lines 465–530)

The entire test module containing `closure.forget()` is gated by:

```rust
// crates/ferric/src/form.rs:465
#[cfg(all(test, target_arch = "wasm32"))]
```

The `cfg(test)` condition is set only by `rustc`/`cargo test`; it is never set during a production `cargo build` or `wasm-pack build`. The additional `target_arch = "wasm32"` constraint further limits compilation to the WASM target. Combined, this guard ensures the enclosed `closure.forget()` (line 515, inside the `#[wasm_bindgen_test]`-annotated function at line 487) is physically absent from any production WASM artifact.

The in-code comment at line 513–514 is accurate: `"forget()` is acceptable in a test: the closure has test scope and the element is removed at the end of the test."

**Sub-check 1 verdict:** `closure.forget()` in `form.rs` is gated under `#[cfg(all(test, target_arch = "wasm32"))]` and cannot be compiled into production WASM. ✓

### dom.rs — production set_events() stash-then-forget (lines 272–300)

The production `set_events()` function (line 229) follows the stash-before-forget sequence prescribed by the wasm-bindgen closure lifecycle:

1. **Create the closure** (line 272): `let closure = Closure::wrap(...)`
2. **Attach the event listener** (lines 276–280): `add_event_listener_with_callback`
3. **Stash the closure on the DOM element** (lines 282–285):
   ```rust
   let _ = js_sys::Reflect::set(
       target,
       &JsValue::from_str(&stash_key(kind)),
       closure.as_ref(),
   );
   ```
4. **Call `closure.forget()`** (line 287): after the JS side holds a live reference through the stash property.

The order is correct: the stash is set before `forget()`. The JS side retains the closure via the element property, so the closure is not "leaked" in the problematic sense — it is intentionally kept alive for the element's lifetime, as stated in the module-level doc comment (lines 27–29):

> "A DOM listener is a `wasm_bindgen::closure::Closure`. Each bound handler's closure is kept alive for the element's lifetime by stashing it on the element object (via `Reflect`) and calling `Closure::forget`."

The matching detach path (lines 236–262) confirms full lifecycle management: on re-bind or detachment, `Reflect::get` retrieves the previously stashed function, `remove_event_listener_with_callback` unregisters it, and `Reflect::delete_property` clears the stash slot. Custom event names are tracked in a parallel array key (lines 248–262) to cover the `EventKind::Custom` case. No closures are leaked unboundedly.

**Sub-check 2 verdict:** `closure.forget()` does appear in production code (`dom.rs:287`), but as the correct and expected stash-then-forget pattern for wasm-bindgen DOM event binding. ✓

**Sub-check 3 verdict:** The closure reference is stashed on the DOM element (via `js_sys::Reflect::set`) before `forget()` is called. The closure is not leaked. ✓
