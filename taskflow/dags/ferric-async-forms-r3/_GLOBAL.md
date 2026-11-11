# _GLOBAL.md — ferric-async-forms-r3

**Project**: ferric async-forms-events — code remediation of review blockers B1, B2, B3  
**Branch**: `work/ferric-async-forms-r2`  
**PR**: Nousix-LLC/nswe-demo#193  
**Observation seam**: `taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md`

---

## Objective

Remediate three blocking findings from code review `review-ferric-async-forms-r2` on PR #193.
All changes land on branch `work/ferric-async-forms-r2`; all 6 CI checks (fmt, clippy, doc, test, wasm, image) must continue to pass.

---

## Shared Context

### Repository layout (relevant crates)

```
crates/ferric/
  src/
    async_resource.rs   — Resource<T>, suspense() — B1 target
    vdom.rs             — VNode, VElement, EventHandler — B2 target
    dom.rs              — WASM bridge, set_events, mount — B2 + B3 target
    form.rs             — FormField<T>, Bind<T> — B3 target
    signal.rs           — Signal<T>, create_effect, create_signal
    component.rs        — Component trait, function components
    lib.rs              — module declarations, prelude
  Cargo.toml
```

### Reactive system design invariants
- `Signal<T>` is a `Copy` handle into a thread-local arena.
- `create_effect(f)` runs `f` immediately, tracks all signals read during `f`, and re-runs `f` on signal change.
- `spawn_local(fut)` is WASM-only (panics on non-wasm); gate with `#[cfg(target_arch = "wasm32")]`.
- `vdom.rs` MUST NOT import `web_sys` — it is fully native-testable.
- `dom.rs` owns the WASM bridge; it imports from `web_sys` and `wasm_bindgen`.

### Current state (branch HEAD before this remediation)
- `Resource<T>` wraps `Signal<ResourceState<T>>`. `Resource::new(fut)` spawns once — fire-once, not reactive.
- `EventHandler = Rc<dyn Fn()>` — zero-argument type alias. DOM closure discards the event.
- `Bind::on_input_handler()` reads `input_buf` signal; `input_buf` is only updated by `Bind::set_input()`. The DOM layer never calls `set_input`, so typed values are never propagated.

### Blocking requirements to satisfy
- **B1 — REQ-ASYNC-001, 003, 005**: Add `create_resource(source, fetcher)` constructor; resource must re-fetch reactively; in-flight futures must be cancelled before re-fetch.
- **B2 — REQ-ASYNC-023**: Handlers must be able to call `prevent_default()` and `stop_propagation()` on the triggering event; zero-arg handlers must remain backward-compatible.
- **B3 — REQ-ASYNC-042**: In the WASM runtime, an input event on a bound `<input>` element must update the signal to the user-typed value. B3 is entangled with B2 (requires event-carrying closures).

### Non-blocking backlog issues (out of scope)
Issues #196–#201 are filed separately and are not to be touched in this remediation.

---

## Task Summary

| Slug | Concern | Depends on | Declared output |
|------|---------|------------|-----------------|
| `SUBTASK_b1_reactive_resource` | B1: reactive `create_resource` constructor in `async_resource.rs` | none | committed changes on `work/ferric-async-forms-r2` |
| `SUBTASK_b2_b3_event_dom` | B2 + B3: event-carrying `EventHandler` enum + Bind DOM plumbing | `SUBTASK_b1_reactive_resource` | committed changes on `work/ferric-async-forms-r2` |
| `SUBTASK_synthesis` | CI verification, verdict, and `SYNTHESIS.md` | `SUBTASK_b2_b3_event_dom` | `taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md` |

---

## Constraints (binding on all children)

1. Change only what is needed to satisfy B1, B2, B3 — no scope creep into NB-1 through NB-6.
2. All 6 CI checks must pass on the final HEAD of `work/ferric-async-forms-r2`.
3. `vdom.rs` must not import `web_sys` — event-carrying handler form must use a platform-independent erasure (`dyn Any` or equivalent).
4. Zero-argument `EventHandler` callers must remain backward-compatible after B2.
5. Commits go to `work/ferric-async-forms-r2`; do not open a new PR — PR #193 is the target.
6. Infrastructure details (server address, SSH key path, host paths) must not appear in committed files or PR comments.
