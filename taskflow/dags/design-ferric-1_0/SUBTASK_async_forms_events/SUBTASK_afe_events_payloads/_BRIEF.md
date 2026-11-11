# Task: Full DOM event coverage + the payload-carrying handler form (Ferric 1.0, concern 4b)

## Task Specification
**Slug**: SUBTASK_afe_events_payloads
**Task Kind**: standard
**Status**: Pending

### Objective
Design Ferric's **full DOM event coverage** — extending the event surface beyond today's `click` and
`input` — and the **payload-carrying handler form** that lets a handler receive the triggering event's
data when it needs it, while the frozen zero-argument handler form stays valid. State both as testable
behavior from the app author's side, registered as `REQ-ASYNC-*` requirements. You **own the
event-payload seam** that the forms sibling composes against.

### Context
Part of concern 4 of the Ferric 1.0 design (see `../_GLOBAL.md`). Today `crates/ferric/src/vdom.rs`
defines `EventKind` as a **closed enum of only `Click` and `Input`**, and `EventHandler = Rc<dyn Fn()>`
— **zero-argument, so a handler cannot read the event** (it cannot get an input's value, a key pressed,
or a submit target). `dom.rs` binds only `click`/`input` and its internal wrapper already receives a
`web_sys::Event` but discards it; the `vdom.rs` module doc explicitly sanctions an **additive** handler
enrichment "to carry a `web_sys::Event` when it needs the event payload." The keyed `diff` emits
`SetEvents` on a change in the **set of bound `EventKind`s**, so widening `EventKind` interacts with that.
This capability is the foundation the forms sibling (`SUBTASK_afe_forms_binding`) builds two-way binding
on, which is why the payload handler form is a frozen seam in the sub-contract.

**Dependents**: `SUBTASK_afe_forms_binding` (reads your payload-handler requirement read-only).

### Scope to cover
- **Full event coverage**: how an author binds the range of DOM events a real app needs beyond
  click/input (for example submit, keyboard, focus/blur, change, and the broader surface) — whether
  through a widened `EventKind`, a named-event escape hatch, or whatever shape you specify — additive
  over the frozen `EventKind` enum.
- **The payload-carrying handler form** (the seam you own): how a handler optionally receives the
  triggering event's data (e.g. a `web_sys::Event` or a typed view of it) while `EventHandler = Rc<dyn
  Fn()>` (zero-arg) remains valid and unbroken. This is the single definition of the handler-payload
  story for the whole concern; specify it as a `REQ-ASYNC-02x` requirement the forms sibling references.
- How widening the event surface composes with the keyed diff's `SetEvents` semantics (stated from the
  author's side — what re-binding they can rely on — not as diff implementation).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Baseline facts (EventKind/EventHandler today), constraints, the frame. |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your id range, and that you OWN the event-payload seam (J3). |
| Parent contract | `../../contracts/id_and_traceability_schema.yaml` | REQ field/stage/verification vocabularies. |
| Upstream requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-006` (the events clause). |
| Ferric baseline | `Nousix-LLC/nswe-demo` @ `276138f`, `crates/ferric/src/{vdom,dom}.rs` | The `EventKind`/`EventHandler` form and the binding to extend (read via `gh api`). |
| Peer precedent | Leptos / Dioxus / Yew event handling and typed-event payloads | Honest comparison; cite by name. |

### Declared output
- `events-and-payloads.md` (this task's workspace) — the event-coverage + payload-handler design and the
  `REQ-ASYNC-020..039` register.

### Success criteria
- [ ] Full event coverage beyond click/input is specified as testable `REQ-ASYNC-*` requirements (ids
      within `REQ-ASYNC-020..039`), additive over the frozen `EventKind` (J4).
- [ ] The payload-carrying handler form is specified once as a `REQ-ASYNC-02x` requirement, with the
      frozen zero-arg `EventHandler` form explicitly preserved (additive, not a redefinition).
- [ ] The interaction with the keyed diff's `SetEvents`/re-binding behavior is stated from the author's
      side.
- [ ] At least one acceptance criterion is checkable per the schema's `verification_method` vocabulary.
- [ ] Peer approaches compared by name.

### Constraints
- `REQ-ASYNC-*` only, within your assigned range (J1). Design, not implementation.
- The payload handler form is defined **only here** (J3); do not redefine any frozen `ferric` item (J4).
- Honor the writing-voice rules in `../_GLOBAL.md`. Select and load your own methodology.
