## Findings — Concern 6 (Rust Language Idiom)

---

### Finding C6-1

**Severity:** non-blocker
**Concern:** idiom
**Location:** `crates/ferric/src/form.rs:519`

The `closure.forget()` call in the WASM test `on_input_event_handler_updates_signal_from_dom_value` is accompanied by a comment:

```rust
// `forget()` is acceptable in a test: the closure has test scope and the element is
// removed at the end of the test.
closure.forget();
```

The comment's second clause is technically inaccurate: removing the DOM element does not free the leaked Rust closure. `forget()` permanently surrenders ownership to the JS side; the Rust heap allocation lives for the WASM module's entire lifetime regardless of what happens to the DOM element. A future reader who trusts that comment may believe DOM cleanup frees the Rust side — it does not.

The usage itself is correct: the closure is wired to the element for one `dispatch_event` call, the leak is one per test invocation, and bounding the leak to the module lifetime is acceptable for test code. The gap is in the explanation.

**What would satisfy this:** Replace the comment with one that names what `forget()` actually does and why that is acceptable here — for example:

```rust
// `forget()` leaks the Rust closure (the memory lives for the WASM module lifetime).
// Acceptable in a test: the closure runs at most once, the leak is bounded, and the
// test-scope DOM element is removed afterwards to avoid cross-test interference.
closure.forget();
```

---

### Finding C6-2

**Severity:** clean
**Concern:** idiom / private field access in tests
**Location:** `crates/ferric/src/async_resource.rs` — `mod tests`, specifically `create_resource_source_change_resets_to_loading` and `create_resource_two_source_changes_stay_loading`

The tests access `resource.signal` (a private field of `Resource<T>`) and use `Resource { signal }` struct literal construction. Both work because `mod tests { use super::*; }` is a child module; Rust privacy rules allow child modules to access private items from their parent module.

The first test that introduces the technique includes:

```rust
// (The `signal` field is accessible here because this test lives in the same file.)
resource.signal.set(ResourceState::Ready(99));
```

This comment is accurate and explains the access correctly to a future reader.

**On the `force_ready()` helper question:** A `#[cfg(test)] fn force_ready(...)` or `impl Resource { #[cfg(test)] fn force_ready(...) }` helper would name the intent more explicitly and hide the struct internals from test bodies. With only two call sites the overhead is not justified today, but if the test suite grows to a third or fourth usage this would be the natural refactor point.

No action required; current approach is idiomatic.

---

### Finding C6-3

**Severity:** clean
**Concern:** `unsafe` usage
**Location:** all changed files (`async_resource.rs`, `vdom.rs`, `dom.rs`, `form.rs`)

No `unsafe {}` blocks appear anywhere in the diff. The `unchecked_ref()` and `unchecked_into()` calls in `dom.rs/set_events` are for casts that are always valid by construction (a `web_sys::Element` is always a JS `Object`; a `wasm_bindgen::Closure` is always a JS `Function`) and are the standard wasm_bindgen idiom for avoiding redundant JS-side `instanceof` checks on types whose ancestry is fixed by the Web API spec. No justification is needed beyond what the existing code comment provides.

---

### Finding C6-4

**Severity:** clean
**Concern:** `unwrap()` in production code
**Location:** all changed files

All eight `unwrap()` calls in the diff are inside `#[cfg(all(test, target_arch = "wasm32"))] mod wasm_tests` blocks. Zero appear in production code paths. The production signal and reactive machinery uses no `unwrap()`.

---

### Finding C6-5

**Severity:** clean
**Concern:** unnecessary clones / clone idiom
**Location:** `crates/ferric/src/dom.rs` — `set_events`

```rust
let handler = handler.clone();
```

`EventHandler` holds an `Rc<dyn Fn(...)>`. Cloning it is O(1) reference-count increment, not a deep copy. This is the correct approach and mirrors how `Rc` is intended to be shared across ownership boundaries.

---

### Finding C6-6

**Severity:** clean
**Concern:** leaked memory in non-test code
**Location:** `crates/ferric/src/dom.rs` — `set_events` (pre-existing, not introduced by this PR)

The production `closure.forget()` in `set_events` is intentional: the closure is stashed on the DOM element via `Reflect::set` so the next `set_events` call can retrieve the JS function reference, call `remove_event_listener_with_callback`, and then delete the stash property. This stash-and-detach cycle is the correct WASM pattern for event listeners that must survive beyond a single call frame. The comment "Stash the closure under its key so a later re-bind or detach can find it" explains this accurately. This line predates the PR; the PR preserves it correctly.

---

### Finding C6-7

**Severity:** clean
**Concern:** `EventHandler` enum idiom (vdom.rs)
**Location:** `crates/ferric/src/vdom.rs`

The old `pub type EventHandler = Rc<dyn Fn()>` type alias is replaced by:

```rust
#[allow(clippy::type_complexity)]
#[derive(Clone)]
pub enum EventHandler {
    NoArg(Rc<dyn Fn()>),
    WithEvent(Rc<dyn Fn(&dyn std::any::Any)>),
}
```

This is idiomatic. The enum makes the two dispatch shapes explicit where the type alias forced the DOM layer to either ignore the event or add an ad-hoc convention. `Clone` is correctly derived (clones the `Rc`, not the closure). `#[allow(clippy::type_complexity)]` is appropriately scoped to the item, not the whole module. The `&dyn Any` erasure keeps `vdom.rs` free of `web_sys` imports, preserving native testability.

---

### Finding C6-8

**Severity:** non-blocker
**Concern:** unnecessary allocation in `event_name` / `stash_key`
**Location:** `crates/ferric/src/dom.rs` — `event_name()` and `stash_key()`

Both functions now return `String`, allocating from `&'static str` literals via `.into()` for every static variant. The previous versions returned `&'static str` with zero allocation. This change was required to handle the `Custom(String)` variant uniformly, but it means the 47-element detachment loop in `static_event_kinds()` allocates 47 short strings on every call to `set_events`, even when most stash slots are empty and the `Reflect::get` / `is_function()` fast-exit runs immediately.

The idiomatic alternative is `Cow<'static, str>`:

```rust
fn event_name(kind: &EventKind) -> Cow<'static, str> {
    match kind {
        EventKind::Click => "click".into(),         // Cow::Borrowed
        // ...
        EventKind::Custom(s) => s.clone().into(),   // Cow::Owned
    }
}
```

This eliminates allocations for all static variants while keeping the API uniform. The impact today is bounded (small strings, DOM mutations are infrequent), but the pattern is worth noting for a framework that aims to be low-overhead.

No action required before merge; appropriate as a follow-on issue if the team is tracking allocation profiles.

---

## What was examined

| File | Lines / scope | Question examined |
|------|--------------|-------------------|
| `crates/ferric/src/form.rs` | WASM test module (~line 492–531) | `closure.forget()` at ~line 519: presence and accuracy of explanatory comment; whether usage is in a loop (it is not); whether DOM cleanup frees the Rust closure (it does not) |
| `crates/ferric/src/async_resource.rs` | `mod tests` lines 370–540 (diff) | `resource.signal.set(...)` and `Resource { signal }` struct literal: Rust privacy rules for child modules; comment accuracy; whether a `force_ready()` helper is warranted |
| `crates/ferric/src/dom.rs` | `set_events` function (diff lines 900–1050); `event_name` / `stash_key` (diff lines 1050–1300) | Pre-existing `closure.forget()` in production: stash-and-detach pattern correctness; `unchecked_ref` safety; allocation profile of `event_name` / `stash_key` returning `String` |
| `crates/ferric/src/vdom.rs` | `EventHandler` enum definition (diff lines 1930–1970) | Enum idiom vs type alias; `Clone` derivation; `#[allow(clippy::type_complexity)]` scope |
| All changed files | Full diff | `unsafe {}` blocks: none found; `unwrap()` in production paths: none found; unnecessary deep clones: none found |
