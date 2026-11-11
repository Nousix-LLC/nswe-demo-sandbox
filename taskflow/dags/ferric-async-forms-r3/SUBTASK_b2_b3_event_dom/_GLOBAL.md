# _GLOBAL.md — SUBTASK_b2_b3_event_dom subtree

**Parent task**: `ferric-async-forms-r3 / SUBTASK_b2_b3_event_dom`  
**Branch**: `work/ferric-async-forms-r2`  
**PR**: Nousix-LLC/nswe-demo#193  
**Observation seam**: `taskflow/dags/ferric-async-forms-r3/SUBTASK_b2_b3_event_dom/SUSPENSION.md`

---

## Objective

Decompose the B2 + B3 implementation into two serial child tasks that share the event dispatch path in `dom.rs`. Each child commits directly to `work/ferric-async-forms-r2`; both must land before the parent-level `SUBTASK_synthesis` runs CI verification.

---

## Repository layout (relevant files)

```
crates/ferric/src/
  vdom.rs      — VNode, VElement, EventHandler (B2 change target)
  dom.rs       — WASM bridge: set_events, event dispatch closure (B2 + B3 change target)
  form.rs      — FormField<T>, Bind<T>, on_input_handler (B2 compat fix + B3 new method)
```

---

## Shared design decisions

### EventHandler redesign (B2)

`EventHandler` changes from a type alias to an enum:

```rust
// vdom.rs — new definition (no web_sys import)
#[derive(Clone)]
pub enum EventHandler {
    NoArg(Rc<dyn Fn()>),
    WithEvent(Rc<dyn Fn(&dyn std::any::Any)>),
}
```

The `VElement::on()` builder wraps its `impl Fn() + 'static` argument in `EventHandler::NoArg(Rc::new(handler))` — existing callers passing zero-arg closures to `.on()` are unaffected syntactically.

`dom.rs`'s dispatch closure matches on the variant:
```rust
move |event: web_sys::Event| {
    match &handler {
        EventHandler::NoArg(f) => f(),
        EventHandler::WithEvent(f) => f(&event as &dyn std::any::Any),
    }
}
```

Callers wanting `prevent_default()` receive the event as `&dyn Any`, downcast to `&web_sys::Event`, and call the method.

### Bind DOM→signal path (B3)

`Bind::on_input_event_handler()` (new, `cfg(target_arch = "wasm32")`) returns `EventHandler::WithEvent(...)`. The closure downcasts the `&dyn Any` to `&web_sys::Event`, traverses `event.target()` to `HtmlInputElement`, reads `.value()`, and calls `raw.set(value)` directly. This correctly updates the field signal on user input.

The existing `on_input_handler()` (zero-arg, all platforms) and `set_input()` are preserved unchanged — the 18 native form tests use them and must continue to pass.

---

## Task summary

| Slug | Concern | Depends on | Declared output |
|------|---------|------------|-----------------|
| `SUBTASK_b2_event_handler` | B2: `EventHandler` enum in `vdom.rs`; dispatch in `dom.rs`; prevent_default test | none (within subtree) | committed changes on `work/ferric-async-forms-r2` |
| `SUBTASK_b3_bind_dom` | B3: `Bind::on_input_event_handler()` in `form.rs`; WASM bind test | `SUBTASK_b2_event_handler` | committed changes on `work/ferric-async-forms-r2` |

---

## Constraints (binding on all children)

1. `vdom.rs` MUST NOT import `web_sys` — event-carrying variant uses `dyn std::any::Any`.
2. Zero-argument callers of `.on()` must work without syntax change.
3. All 18 existing native `form.rs` tests must pass after every commit.
4. No scope creep into NB-1 through NB-6.
5. Commits go to `work/ferric-async-forms-r2`; do not open a new PR.
6. Infrastructure details must not appear in committed files or PR comments.
