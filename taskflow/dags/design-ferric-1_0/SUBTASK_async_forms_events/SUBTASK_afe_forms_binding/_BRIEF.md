# Task: Forms + two-way input binding (Ferric 1.0, concern 4c)

## Task Specification
**Slug**: SUBTASK_afe_forms_binding
**Task Kind**: standard
**Status**: Pending

### Objective
Design Ferric's **forms** capability: **two-way binding** of input state to signals (the model and the
field stay in sync), together with the **validation and submission ergonomics** an author needs to build
a real form. State it as testable behavior from the app author's side, registered as `REQ-ASYNC-*`
requirements, composed on top of the payload-carrying handler form owned by the events sibling.

### Context
Part of concern 4 of the Ferric 1.0 design (see `../_GLOBAL.md`). Today an author cannot bind a field
two-way: `EventHandler = Rc<dyn Fn()>` is zero-argument, so an `input` handler cannot read the field's
value from the event. Two-way binding therefore stands on the **payload-carrying handler form** owned by
`SUBTASK_afe_events_payloads` — which is why this task depends on it and composes against its
`REQ-ASYNC-02x` requirement **read-only**. The upstream `REQ-FW-006` requires "a form binds an input
two-way so the model and the field stay in sync."

**Dependencies**: `SUBTASK_afe_events_payloads` (the payload handler form you build on).

### Scope to cover
- **Two-way binding**: how an author binds an input's value to a signal so a field edit updates the
  signal and a signal change updates the field — whatever surface you specify (a binding helper, a
  `bind`-style convention, a macro affordance). Compose it on the payload handler form; reference that
  requirement read-only, do not redefine it.
- **Validation ergonomics**: how an author expresses per-field / per-form validation and surfaces
  validity and error messages in the view (reactively).
- **Submission ergonomics**: how an author handles form submit (including preventing the default
  navigation) and reads the submitted values — stated from the author's side.
- Binding across the common input kinds an app needs (text, checkbox, select, and the like), at the
  level of what the author can express and rely on.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Baseline facts, constraints, the frame. |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your id range; the event-payload seam you compose against (J3). |
| Parent contract | `../../contracts/id_and_traceability_schema.yaml` | REQ field/stage/verification vocabularies. |
| Upstream requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-006` (the forms clause). |
| Events sibling output | `../SUBTASK_afe_events_payloads/events-and-payloads.md` | The payload-carrying handler requirement you build on (read-only). |
| Ferric baseline | `Nousix-LLC/nswe-demo` @ `276138f`, `crates/ferric/src/{signal,vdom}.rs` | The signal handles and input binding your design uses (read via `gh api`). |
| Peer precedent | Leptos `bind:`, Dioxus forms, Svelte/Vue two-way binding | Honest comparison; cite by name. |

### Declared output
- `forms-binding.md` (this task's workspace) — the forms + two-way-binding design and the
  `REQ-ASYNC-040..059` register.

### Success criteria
- [ ] Two-way binding, validation, and submission are each specified as testable `REQ-ASYNC-*`
      requirements (ids within `REQ-ASYNC-040..059`) conforming to the parent schema.
- [ ] Two-way binding references the events sibling's payload-handler `REQ-ASYNC-02x` read-only and does
      not redefine the handler form (J3).
- [ ] At least one acceptance criterion is checkable per the schema's `verification_method` vocabulary
      (e.g. a stated example where editing a field updates a signal and vice versa).
- [ ] Peer approaches compared by name.

### Constraints
- `REQ-ASYNC-*` only, within your assigned range (J1). Design, not implementation.
- Build on, do not redefine, the event-payload handler form (J3); additive over frozen surfaces (J4).
- Honor the writing-voice rules in `../_GLOBAL.md`. Select and load your own methodology.
