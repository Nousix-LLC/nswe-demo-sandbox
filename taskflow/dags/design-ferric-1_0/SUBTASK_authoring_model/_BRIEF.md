# Task: Ferric 1.0 — authoring model: view! macro, props/children/slots, context (concern 3)

## Task Specification
**Slug**: SUBTASK_authoring_model
**Task Kind**: standard
**Status**: Pending

### Objective
Design the declarative authoring model that lets real applications be written ergonomically without
builder-call boilerplate: a `view!`/JSX-style macro; the component model's props, children/slots, and
composition; and context for sharing state without prop drilling. State the authoring surface and its testable
bar — what the author writes and what must work, not the macro's internal expansion.

### Context
Part of the Ferric 1.0 framework design (see `../_GLOBAL.md`); owns `REQ-API-*`. Today components are plain
`Fn() -> VNode` closures built with `VElement::new(...).child(...)` builder calls (see
`crates/ferric/examples/counter.rs`); the bar is that **real apps can be written ergonomically without that
boilerplate.**

**Dependencies**: `SUBTASK_scope_and_requirements`.

### Distinct concerns to cover (name them; let your own evaluation decide how to split)
- **The view macro**: a declarative `view!`/JSX-style syntax for element trees, attributes, event handlers,
  conditionals, lists/keys, and interpolated reactive values; how it lowers onto the existing `VNode` model;
  compile-time diagnostics quality (a `trybuild`-checkable story).
- **Component props/children/slots/composition**: how components declare typed props, accept children and named
  slots, and compose; ergonomics vs. Rust's type system.
- **Context**: sharing state down the tree without prop drilling, and its interaction with reactivity and
  scoped cleanup.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Contract | `../contracts/` | `REQ-API-*` schema; your namespace. |
| 1.0 requirements | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` | The frame to specialize. |
| Ferric baseline | `crates/ferric/` (`component`, `vdom`, `signal`) + `examples/counter.rs` | The builder-call model the macro replaces and the `VNode`/component surface it lowers onto. |
| Peer precedent | Leptos `view!`, Sycamore `view!`, Dioxus `rsx!`, Yew `html!` | Honest comparison of Rust view-macro designs; cite by name. |

### Declared output
- `authoring-model.md` (this task's workspace) — the authoring model + the `REQ-API-*` register.
  Repo target `design/ferric/authoring-model.md`.

### Success criteria
- [ ] The macro's authoring surface, the props/children/slots/composition model, and context are specified
      concretely enough for a code DAG to build, with example snippets of what an author writes.
- [ ] `REQ-API-*` acceptance criteria are testable (e.g. example builds, `trybuild` diagnostics), conforming to
      `../contracts/id_and_traceability_schema.yaml`.
- [ ] The macro's relationship to the existing `VNode`/keyed-diff model is stated (additive over the foundation).
- [ ] Peer view-macros compared by name; ergonomic trade-offs stated plainly.

### Constraints
- Write `REQ-API-*` only (identity I1). Design, not implementation. Load your own macro/DSL-design methodology.
- Honor the writing-voice rules; run the avoid-ai-writing pass before finalizing.
