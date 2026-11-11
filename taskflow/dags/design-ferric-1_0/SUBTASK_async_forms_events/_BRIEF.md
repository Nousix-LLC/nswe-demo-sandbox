# Task: Ferric 1.0 — async resources, forms, and events (concern 4)

## Task Specification
**Slug**: SUBTASK_async_forms_events
**Task Kind**: standard
**Status**: Pending

### Objective
Design three capabilities a real app needs beyond static rendering: async resources with suspense-style loading
and error states; forms with two-way input binding; and full DOM event coverage. State each as testable
behavior from the app author's side — what they can express and what must work.

### Context
Part of the Ferric 1.0 framework design (see `../_GLOBAL.md`); owns `REQ-ASYNC-*`. Today the framework binds
only `click` and `input` events and has no async or form-binding story. These are distinct capabilities grouped
because each is "dynamic app behavior"; treat them as distinct concerns, each with its own bar.

**Dependencies**: `SUBTASK_scope_and_requirements`.

### Distinct concerns to cover (name them; let your own evaluation decide how to split)
- **Async resources + suspense**: a reactive async-data primitive with loading / loaded / error states an app
  renders declaratively; how it composes with reactivity and (by reference) with SSR resolution.
- **Forms + two-way binding**: binding input state to signals two-way; validation/submission ergonomics.
- **Full DOM event coverage**: extending beyond `click`/`input` to the full event surface, with handlers that
  can receive event payloads where needed (today's handlers are `Fn()` with no payload).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Contract | `../contracts/` | `REQ-ASYNC-*` schema; your namespace. |
| 1.0 requirements | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` | The frame to specialize. |
| Ferric baseline | `crates/ferric/` (`signal`, `vdom` `EventKind`, `dom`) | The reactive core and the current event binding to extend. |
| Peer precedent | Leptos `Resource`/`Suspense`, Solid resources, Dioxus events/forms | Honest comparison; cite by name. |

### Declared output
- `async-forms-events.md` (this task's workspace) — the design + the `REQ-ASYNC-*` register.
  Repo target `design/ferric/async-forms-events.md`.

### Success criteria
- [ ] Async resources (with loading/error states), two-way form binding, and full event coverage are each
      specified with testable `REQ-ASYNC-*` acceptance criteria, conforming to the contract schema.
- [ ] The event-payload story is stated (how a handler receives event data when it needs it).
- [ ] Composition with reactivity and (by reference) SSR is addressed, not left as an owl.
- [ ] Peer approaches compared by name.

### Constraints
- Write `REQ-ASYNC-*` only (identity I1). Design, not implementation. Load your own methodology.
- Honor the writing-voice rules.
