# Task: Ferric 1.0 — component props, children, slots, and composition (authoring model, part B)

## Task Specification
**Slug**: SUBTASK_components_props_slots
**Task Kind**: standard
**Status**: Pending

### Objective
Design the component model that lets authors build and compose reusable components: how a component declares
typed **props**, accepts **children** and **named slots**, and **composes** with other components — the
authoring surface and its testable bar, not the implementation.

### Context
Part of the Ferric 1.0 authoring model (subtree hub: `../_GLOBAL.md`). This task owns the `REQ-API-*` band
**030–059** (see `../contracts/req_api_partition.yaml`). Today a component is any `Fn() -> VNode` (see
`crates/ferric/src/component.rs`): there is no props convention, no children/slots convention, and no
composition story beyond calling a closure. The bar is an expressive, documented component/composition model
(parent `REQ-FW-005`) that a library/component author (persona A3) can build on against a stable surface.

### Distinct facets this model must cover
Facets of one component model, not separate deliverables:
- **Typed props**: how a component declares its props — required, optional, and defaulted — and the ergonomic
  trade-offs against Rust's type system (a props struct, a builder, or macro sugar; stated against peers).
- **Children**: how a component accepts and renders children.
- **Named slots**: how a component accepts more than one labelled region of content and how the author fills
  them.
- **Composition**: how components nest and compose, and how this stays sound against the baseline `Component`
  trait / `Fn() -> VNode` model (additively, no redefinition of the frozen surface).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, the authoring seam. |
| Subtree contract | `../contracts/` | Your `REQ-API-*` band (030–059); the invocation seam (IA2) you define the component side of; verification vocab. READ-ONLY. |
| Parent 1.0 requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-005` (authoring), `REQ-FW-010` (stable API for A3) to specialize (read-only). |
| Ferric baseline | `crates/ferric/src/component.rs` (`Component`, `Fn() -> VNode`), `vdom.rs` (`VNode`), `lib.rs` (frozen `prelude`) | The component surface the model extends additively. Representative checkout: `taskflow/dags/ferric-foundation/checkout/crates/ferric/`. |
| Peer precedent | Leptos `#[component]`/props, Sycamore props, Dioxus props/children, Yew `Properties` | By-name comparison of Rust component-prop designs and their ergonomic trade-offs. |
| Macro seam | `../SUBTASK_view_macro/` (sibling; do not read its output — compose against the contract's invocation seam IA2) | How the macro invokes a component is fixed by the contract; you define the declaration side it corresponds to. |

### Declared output
- `components-props-slots.md` (this task's workspace) — the component model (props/children/slots/composition)
  and the `REQ-API-030..059` register slice with testable acceptance criteria. Folds into
  `../authoring-model.md` at synthesis.

### Success criteria
- [ ] Props (required/optional/defaulted), children, named slots, and composition are shown with example
      snippets of **what an author writes**, concrete enough for a code DAG to build.
- [ ] The component-side of the invocation seam (IA2) is defined so every macro-side passing form has a
      corresponding declaration form and vice versa.
- [ ] The model is additive over the baseline `Component`/`Fn() -> VNode` surface; nothing frozen is redefined.
- [ ] `REQ-API-030..059` acceptance criteria are testable and use an inherited `verification_method`,
      conforming to `../../contracts/id_and_traceability_schema.yaml`.
- [ ] Peer component-prop designs compared by name; ergonomic trade-offs against Rust's type system stated
      plainly.

### Constraints
- Write `REQ-API-*` ids only within band **030–059** (identity IA1). Design, not implementation.
- Honor the writing-voice rules; run the avoid-ai-writing pass over `components-props-slots.md` before
  finalizing.
- Select and load your own API / type-system-ergonomics design methodology if available; otherwise apply the
  discipline directly, grounded in the baseline source and named peer behavior.
