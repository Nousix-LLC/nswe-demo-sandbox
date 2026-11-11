# Q2 — EventHandler Abstraction Boundary: Sub-Findings

PR #193 (`feat(ferric): async resources, expanded events, and form binding`)  
Branch: `work/ferric-async-forms-r2`  
Reviewer node: `SUBTASK_q2_eventhandler`

---

## Findings

### Finding 1 — web_sys boundary: clean

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/vdom.rs:31-33`
- **description**: The import block of `vdom.rs` is `use std::collections::{BTreeMap, HashSet}; use std::fmt; use std::rc::Rc;`. No `web_sys` import is present — not as a `use` path, not as a qualified `web_sys::` type in any type or expression position. The `web_sys::Event` name appears only in doc comments as usage guidance for callers (e.g., "downcast to `web_sys::Event` in the DOM layer"). Doc comments add no compile-time dependency. `vdom.rs` is fully native-testable as stated. The boundary hold is confirmed by the module-level comment: "it performs no `web-sys` calls, so the full view tree and the diff are exercised by the `#[cfg(test)]` suite below with ordinary `cargo test`."

---

### Finding 2 — Enum soundness: clean

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/vdom.rs` (EventHandler definition, ~line 193–200)
- **description**: The two-variant scheme models the actual use-case split cleanly. `NoArg(Rc<dyn Fn()>)` covers the common case where the handler updates signals and needs no event details. `WithEvent(Rc<dyn Fn(&dyn std::any::Any)>)` covers the cases that need the DOM event — `prevent_default()`, reading input value, keyboard key codes — via type erasure. The names are precise: `NoArg` describes the closure signature; `WithEvent` describes what distinguishes it. Both arms are short to match and unambiguous. The `#[allow(clippy::type_complexity)]` on the enum is appropriate; the type is readable as written and a type alias would add indirection without clarity. The design correctly avoids a third variant (e.g., `WithTypedEvent<T>`) that would require `vdom.rs` to know specific `web_sys` event subtypes — the erased `&dyn Any` delegates that knowledge to the caller.

---

### Finding 3 — Dispatch completeness in dom.rs: clean

- **severity**: clean
- **concern**: code-quality
- **location**: `crates/ferric/src/dom.rs` (set_events, ~line 272–275)
- **description**: The dispatch closure is:
  ```rust
  let closure = Closure::wrap(Box::new(move |event: web_sys::Event| match &handler {
      EventHandler::NoArg(f) => f(),
      EventHandler::WithEvent(f) => f(&event as &dyn std::any::Any),
  }) as Box<dyn FnMut(web_sys::Event)>);
  ```
  The match is exhaustive over both variants with no wildcard arm — the compiler guarantees every `EventHandler` case is handled. The upcast `&event as &dyn std::any::Any` is correct: `web_sys::Event` is `'static` (it owns a wasm-bindgen `JsValue`), so it implements `Any` and the `downcast_ref::<web_sys::Event>()` call in the wasm32 test confirms the round-trip. No unreachable arms, no missing arms.

---

### Finding 4 — static_event_kinds() sync gap: non-blocker

- **severity**: non-blocker
- **concern**: code-quality
- **location**: `crates/ferric/src/dom.rs` (static_event_kinds function)
- **description**: `event_name` and `stash_key` use exhaustive `match` expressions over `EventKind` — adding a new static variant without updating those functions is a **compiler error**. The detachment pass in `set_events` iterates `static_event_kinds()`, which is a manually-counted `[EventKind; 47]` array literal. The comment says the array "must be kept in sync" but the compiler enforces only that the array literal contains exactly 47 elements. If a contributor adds a new static variant, updates the exhaustive matches (compiler-forced), but forgets to add the variant to `static_event_kinds()` *and* increment the return-type annotation from `47` to `48`, the code compiles cleanly. The new variant's stash slot is never purged on a re-bind, so the previous closure leaks and the event fires twice.

  The array is currently correct — count matches the 47 non-`Custom` `EventKind` variants. This is a future-maintenance trap, not a present defect.

  What would satisfy: add a unit test that verifies the count matches the enum's non-Custom variant count, or at minimum update the comment to call out explicitly that the array length annotation must be incremented when adding a variant (the current comment says "must be kept in sync" but does not say where the update goes). A compile-time `const_assert` or a `#[test]` that constructs every static variant and checks `static_event_kinds().len()` against a known count would close the gap.

---

### Finding 5 — Abstraction boundary clarity for future contributors: clean

- **severity**: clean
- **concern**: code-quality
- **location**: `structural`
- **description**: The boundary is navigable. A new handler *variant* belongs in `vdom.rs` (`EventHandler` enum) and the dispatch match in `dom.rs` `set_events` will produce a compiler error until the new arm is added. A new event *kind* belongs in `vdom.rs` (`EventKind` enum), and the exhaustive matches in `event_name` and `stash_key` in `dom.rs` produce compiler errors until they are updated. Both directions have compiler-enforced update paths — except for the `static_event_kinds()` array noted in Finding 4. The module-level doc comment in `dom.rs` correctly places all web_sys responsibilities in that module; a contributor reading the comment and the import blocks would know not to add a `web_sys` import to `vdom.rs`.

---

## What was examined

| File | Examined | Sub-question covered |
|------|----------|----------------------|
| `crates/ferric/src/vdom.rs` (PR branch) | Import block (lines 31–33); `EventHandler` enum definition; `on` / `on_with_event` builder methods; `diff_events`, `event_kinds` helpers; test module | Q2.1 (enum soundness), Q2.2 (web_sys boundary), Q2.4 (boundary clarity) |
| `crates/ferric/src/dom.rs` (PR branch) | `set_events` closure dispatch (match arms); `static_event_kinds` array; `event_name` and `stash_key` exhaustive matches; wasm32 test for `WithEvent` downcast path | Q2.3 (dispatch completeness), Q2.4 (boundary completeness), Q2.1 (enum ergonomics in use) |
| PR #193 diff | `vdom.rs` and `dom.rs` hunks in full | Confirmed scope of changes |

**Sub-questions covered**:

1. **Enum soundness** (Q2.1): `NoArg`/`WithEvent` names examined, variant ergonomics and coverage assessed — clean (Finding 2).
2. **web_sys boundary** (Q2.2): Full import block of `vdom.rs` read, confirmed no `web_sys` import in any position — clean (Finding 1).
3. **Dispatch completeness** (Q2.3): `set_events` match arms read, confirmed exhaustive two-arm coverage, no wildcard — clean (Finding 3).
4. **Boundary completeness** (Q2.4): compiler-enforcement mechanisms for both handler-variant and event-kind additions assessed; `static_event_kinds` sync gap identified — non-blocker finding (Finding 4); overall boundary navigation assessed as clear (Finding 5).
