# Task: B2 + B3 — Event-carrying handlers and Bind DOM plumbing

## Task Specification

**Slug**: SUBTASK_b2_b3_event_dom  
**Task Kind**: standard  
**Depends on**: SUBTASK_b1_reactive_resource  
**Status**: Pending  
**Assigned To**: swe-coder

### Objective

Satisfy REQ-ASYNC-023 (B2) and REQ-ASYNC-042 (B3) by: (a) adding an event-carrying variant to `EventHandler` so handlers can call `prevent_default()` and `stop_propagation()`; (b) fixing the `Bind` DOM→signal direction so that an input event on a bound `<input>` element updates the signal to the typed value in the WASM runtime.

### Context

This task is part of ferric-async-forms-r3 (see `_GLOBAL.md` in the parent workspace).

**Dependencies**: `SUBTASK_b1_reactive_resource` — both tasks commit to the same branch (`work/ferric-async-forms-r2`); this task must start from the commit that includes the B1 fix.  
**Dependents**: `SUBTASK_synthesis` (CI verification and final verdict).

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Shared constraints, branch, CI requirements |
| Current vdom.rs | `crates/ferric/src/vdom.rs` on branch | EventHandler type, VElement.events |
| Current dom.rs | `crates/ferric/src/dom.rs` on branch | set_events, event dispatch closure, stash/detach |
| Current form.rs | `crates/ferric/src/form.rs` | Bind<T>, on_input_handler, input_buf contract |
| Review synthesis | `taskflow/dags/review-ferric-async-forms-r2/SYNTHESIS.md` | B2 and B3 blocker detail |

---

## Scope

This task has two distinct concerns that share the event dispatch path in `dom.rs` and must be addressed together:

### Concern 1 — B2: event-carrying `EventHandler` (REQ-ASYNC-023)

The current `EventHandler = Rc<dyn Fn()>` type alias in `vdom.rs` is zero-argument. `dom.rs` discards the event in `move |_event: web_sys::Event| { handler(); }`. Handlers cannot call `prevent_default()` or `stop_propagation()`.

**What is required**:
- `EventHandler` in `vdom.rs` must support an event-carrying form in addition to the existing zero-argument form.
- `vdom.rs` MUST NOT import `web_sys`. The event-carrying variant must use a platform-independent type (e.g., `Rc<dyn Fn(&dyn std::any::Any)>`) so `vdom.rs` remains fully native-testable.
- All existing zero-argument handler call sites must remain backward-compatible (no caller breakage).
- In `dom.rs`, the DOM closure must pass the `web_sys::Event` to event-carrying handlers. Callers that need `prevent_default()` can downcast the `dyn Any` reference to `web_sys::Event`.
- REQ-ASYNC-023 must be verifiable by a test that calls `prevent_default()` and confirms `event.default_prevented()` is `true`.

### Concern 2 — B3: Bind DOM→signal plumbing (REQ-ASYNC-042)

The DOM event plumbing in `dom.rs` discards the event and has no reference to the DOM input element. `Bind::on_input_handler()` reads `input_buf` (unchanged at DOM event time), so the typed value is never propagated to the signal.

**What is required**:
- When an `Input` or `Change` event fires on a bound `<input>` element in the WASM runtime, the signal must be updated to the element's current value (`HtmlInputElement::value()`).
- One valid approach (entangled with B2): construct a bind-time handler closure that is of the event-carrying form, reads `HtmlInputElement::value()` from `event.target()`, and writes it directly to the field signal. This requires `form.rs` to produce an `EventHandler` variant that carries the event (now possible once B2 is in place).
- The existing `on_input_handler()` (zero-arg) and `set_input()` are retained for native testability.
- At least one WASM test must: create a bound `<input>` element, set its `value` property, dispatch a synthetic `input` event on the element, and assert the field signal was updated to the typed value.

### Items to preserve

- All 18 existing native `form.rs` tests must continue to pass.
- All existing native and WASM tests in other modules must continue to pass.
- The `prelude` re-exports are not changed by this task (unless a new public item needs to be re-exported).

---

## Output Specification

### Declared output

Committed change(s) on branch `work/ferric-async-forms-r2` covering `vdom.rs`, `dom.rs`, and `form.rs` that satisfy B2 and B3. Commits must be pushed to the remote before this task is declared complete.

---

## Success Criteria

- [ ] `EventHandler` in `vdom.rs` supports both zero-arg and event-carrying forms; no `web_sys` import in `vdom.rs`.
- [ ] `dom.rs` passes the event to event-carrying handlers.
- [ ] A test demonstrates `prevent_default()` callable from a handler (REQ-ASYNC-023).
- [ ] A WASM test fires a synthetic `input` event on a bound `<input>` and verifies the signal updates to the typed value (REQ-ASYNC-042).
- [ ] All 18 existing native form.rs tests pass.
- [ ] All existing native and WASM tests in async_resource.rs pass.
- [ ] `cargo test -p ferric` passes (native).
- [ ] `wasm-pack test --headless --firefox crates/ferric` passes (WASM).
- [ ] `cargo clippy -p ferric` passes with no new warnings.
- [ ] Commit(s) pushed to `work/ferric-async-forms-r2`.

---

## Constraints

- Do not regress any currently passing test.
- `vdom.rs` must remain free of `web_sys` dependency.
- Zero-argument callers of `EventHandler` must work unchanged.
- Do not address NB-1 through NB-6 in this task.
- Infrastructure details must not appear in committed files.
