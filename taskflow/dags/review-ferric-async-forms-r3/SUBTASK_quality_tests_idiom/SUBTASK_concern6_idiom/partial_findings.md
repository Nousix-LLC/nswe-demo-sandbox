# Concern 6 — Rust Language Idiom: PR #193

## Findings

- **severity**: clean
  **concern**: idiom
  **location**: crates/ferric/src/form.rs:515
  **description**: `closure.forget()` in the WASM integration test is commented at lines 513–514: `// 'forget()' is acceptable in a test: the closure has test scope and the element is removed at the end of the test.` This names the reason and the bounding condition. The DOM element is removed at line 529, which eliminates the browser's event-listener reference. The pattern is standard wasm-bindgen practice for closures whose lifetime is managed by the browser within a bounded test scope.

- **severity**: clean
  **concern**: idiom
  **location**: crates/ferric/src/async_resource.rs:634
  **description**: `resource.signal.set(ResourceState::Ready(99))` and the similar calls at lines 662 and 667 access the private `signal` field of `Resource<T>`. Rust's module visibility rules allow child modules (`mod tests`) to read and write private fields of types defined in the parent module — this is correct. The comment at lines 632–633 (`// (The 'signal' field is accessible here because this test lives in the same file.)`) correctly states this. The pattern is consistent with the rest of the test module, which also uses struct-literal construction `Resource { signal }` (e.g., lines 448–449, 475–476) to bypass the public constructor. A `#[cfg(test)] fn force_ready(...)` helper would add an indirection layer without readability benefit for two tests in the same file; direct field access in same-file test modules is the established pattern here.

- **severity**: clean
  **concern**: idiom
  **location**: "structural"
  **description**: Scanned `async_resource.rs`, `form.rs`, `dom.rs`, and `vdom.rs` for `unsafe` blocks. None were found in any of the four files. `dom.rs` uses wasm-bindgen's `unchecked_ref::<js_sys::Function>()` and `unchecked_into()` in WASM-gated production code at lines 255 and 276; these are safe functions in Rust's type system and are applied to values the framework placed there itself (closures stashed via `Reflect::set` by the same call path, elements created by the DOM layer). No `unsafe {}` blocks were introduced by this PR.

- **severity**: clean
  **concern**: idiom
  **location**: "structural"
  **description**: Checked `unwrap()` usage in production code paths (non-`#[cfg(test)]`) across all four files. No bare `unwrap()` calls appear in production paths. `form.rs`'s `on_input_event_handler()` uses `if let` chains that silently no-op on a missing or mistyped event target — appropriate for DOM event handling. `dom.rs`'s `set_events()` uses `.expect("set_events: add_event_listener failed")` for the event-listener registration — an appropriate choice for a condition that indicates a programming error (calling on a valid element), not a user-input error path. `async_resource.rs` production code handles both `Ok` and `Err` variants explicitly in `new_fallible()`. `unwrap()` appears freely in test code, which is acceptable.

- **severity**: clean
  **concern**: idiom
  **location**: "structural"
  **description**: Checked `.clone()` calls in production code paths across all four files. All are structurally required: `dom.rs:271` clones `EventHandler` (which wraps `Rc<dyn Fn...>`) to move it into a `move` closure — this is an Rc refcount increment, not a deep copy; `dom.rs:290` clones a `String` from an iterator reference to push into a `Vec<String>`; `dom.rs:437` clones the contained `String` from `EventKind::Custom(s)` where the return type requires an owned value; `async_resource.rs:71–72` clones the payload in the `Clone` impl for `ResourceState<T>`, which is the correct implementation. `vdom.rs` clone calls in the diff/patch paths are inherent to a structural VDOM diff algorithm. No unnecessary copies appear in production paths.

- **severity**: non-blocker
  **concern**: idiom
  **location**: crates/ferric/src/dom.rs:287
  **description**: `closure.forget()` in the production `set_events()` function has no inline comment at the call site. The lifecycle is managed: the closure reference is stashed on the DOM element via `Reflect::set` at lines 282–286 (under `stash_key(kind)`), and the cleanup path at lines 215–263 retrieves that stash key to call `remove_event_listener_with_callback` before rebinding. This is not a leak. However, a reader encounters the `forget()` after a comment about stashing and must connect those two code regions to confirm cleanup will occur. The analogous test-side `closure.forget()` at `form.rs:515` carries an explicit inline comment explaining why the forget is bounded. Adding a note at the call site — such as `// Ownership transferred to JS: the browser holds the closure via the event listener; the stash slot above provides the reference for future detachment.` — would make the lifecycle self-evident without requiring the reader to follow the cleanup path. Readability observation, not a correctness issue.

## What was examined

- `crates/ferric/src/form.rs` — full file (531 lines)
  - Production code: `FormField<T>`, `Bind<T>`, `on_input_event_handler()` (~lines 1–228)
  - Native test module: `mod tests` (~lines 230–455)
  - WASM integration test block (~lines 457–531)
  - `closure.forget()` at line 515 and inline comment at lines 513–514
  - `unwrap()` scan in production: none found
  - `.clone()` scan in production: none found
- `crates/ferric/src/async_resource.rs` — full file (832 lines)
  - Production code: `ResourceState<T>`, `Resource<T>`, `create_resource`, `suspense` (~lines 1–315)
  - Native test module: `mod tests` (~lines 316–end)
  - `resource.signal.set(...)` calls at lines 634, 662, 667 and surrounding context
  - `unsafe` scan: none found
  - `unwrap()` scan in production: none found
  - `.clone()` in production: `ResourceState::Clone` impl at lines 71–72 (necessary)
- `crates/ferric/src/dom.rs` — production and test sections
  - `set_events()` production function (~lines 215–302): `closure.forget()` at line 287, stash logic at lines 282–286, cleanup loop at lines 215–263
  - `event_name()` helper (~lines 390–439): `s.clone()` at line 437
  - `unsafe` scan: none found (only `unchecked_ref`, `unchecked_into` — not `unsafe` blocks)
  - `unwrap()` scan in production: none found; `.expect()` with message at line 280
  - WASM test block (~lines 605–621): `unwrap()` and `.clone()` acceptable in test context
- `crates/ferric/src/vdom.rs` — production and test sections
  - `unsafe` scan: none found
  - `.clone()` scan: all production clones are in VDOM diff/patch paths where structural copies are required by the algorithm
  - `unwrap()` scan: only in test code at line 761
- Sub-questions addressed:
  - [x] Is `closure.forget()` in `form.rs` WASM test commented to explain the bounded lifetime?
  - [x] Does `resource.signal.set(...)` in `async_resource.rs` use Rust-valid private field access? Is a `force_ready` helper warranted?
  - [x] Does any added code use `unsafe` blocks? Are they justified with invariant comments?
  - [x] Are there `unwrap()` calls in non-test production paths that should use `?`?
  - [x] Are there unnecessary `.clone()` calls in production paths?
  - [x] Does any non-test code leak memory (closures registered but never freed)?
