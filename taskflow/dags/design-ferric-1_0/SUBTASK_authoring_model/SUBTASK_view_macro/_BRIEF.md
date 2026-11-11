# Task: Ferric 1.0 — the `view!` macro authoring surface (authoring model, part A)

## Task Specification
**Slug**: SUBTASK_view_macro
**Task Kind**: standard
**Status**: Pending

### Objective
Design the `view!`/JSX-style macro that lets an author describe an element tree declaratively instead of
hand-building `VElement::new(...).child(...)` calls — the authoring **surface** and its testable bar (what the
author writes and what must work), not the proc-macro's internal token expansion.

### Context
Part of the Ferric 1.0 authoring model (subtree hub: `../_GLOBAL.md`). This task owns the `REQ-API-*` band
**001–029** (see `../contracts/req_api_partition.yaml`). Today an author composes view trees by hand with the
builder calls in `crates/ferric/src/vdom.rs` and `examples/counter.rs`; the bar is that a real app's views can
be written ergonomically and declaratively, lowering onto the existing `VNode` model with no change to the
frozen surface.

### Distinct facets this surface must cover
Name them in the design; they are facets of one macro surface, not separate deliverables:
- **Element trees**: elements, text, and nesting; attributes; event handlers (the baseline binds `click` and
  `input`; the macro's handler syntax should be open to the additive event set `REQ-ASYNC-*` adds, named as a
  read-only cross-reference).
- **Control flow**: conditional rendering and lists with keys (the baseline's keyed diff reconciles sibling
  lists only when every child carries a `key` — the macro's list/key syntax must make producing keyed children
  natural).
- **Interpolated reactive values**: how a `Signal`/`Memo` read is embedded in the view so the mount effect
  re-renders on change, consistent with the baseline reactive runtime.
- **Lowering**: how the surface lowers onto `VNode`/`VElement` (additively; stated as *what it produces*, not
  how the macro is written).
- **Compile-time diagnostics**: the quality bar for macro errors on malformed views — a `trybuild`-checkable
  story that names the author's mistake in terms of their code (parent `REQ-FW-014`).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, the authoring seam. |
| Subtree contract | `../contracts/` | Your `REQ-API-*` band (001–029); the invocation seam (IA2); verification vocab. READ-ONLY. |
| Parent 1.0 requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-005`, `REQ-FW-014` to specialize (read-only). |
| Ferric baseline | `crates/ferric/src/vdom.rs`, `examples/counter.rs`, `src/lib.rs` (frozen `prelude`) | The builder model the macro replaces and the `VNode` surface it lowers onto. Representative checkout: `taskflow/dags/ferric-foundation/checkout/crates/ferric/`. |
| Peer precedent | Leptos `view!`, Sycamore `view!`, Dioxus `rsx!`, Yew `html!` | By-name comparison of Rust view-macro designs. |
| Component-model seam | `../SUBTASK_components_props_slots/` (sibling; do not read its output — compose against the contract's invocation seam IA2) | How the macro invokes a component is fixed by the contract, not by reading the sibling. |

### Declared output
- `view-macro.md` (this task's workspace) — the macro authoring surface, its lowering onto `VNode`, the
  diagnostics story, and the `REQ-API-001..029` register slice with testable acceptance criteria. Folds into
  `../authoring-model.md` at synthesis.

### Success criteria
- [ ] The macro surface (elements, attrs, events, conditionals, lists/keys, interpolated reactive values) is
      shown with example snippets of **what an author writes**, concrete enough for a code DAG to build.
- [ ] The lowering onto the existing `VNode`/keyed-diff model is stated as additive; nothing in the frozen
      `prelude` is redefined.
- [ ] The compile-diagnostics bar is a `trybuild`-checkable story with stated example failures.
- [ ] `REQ-API-001..029` acceptance criteria are testable and use an inherited `verification_method`
      (`automated_test` / `example_build` / `doc_inspection`), conforming to
      `../../contracts/id_and_traceability_schema.yaml`.
- [ ] Peer view-macros compared by name; ergonomic trade-offs stated plainly.

### Constraints
- Write `REQ-API-*` ids only within band **001–029** (identity IA1). Design, not implementation.
- Compose against the contract's invocation seam (IA2) for how the macro passes props/children/slots to a
  component; do not redefine the component model.
- Honor the writing-voice rules; run the avoid-ai-writing pass over `view-macro.md` before finalizing.
- Select and load your own macro/DSL-design methodology if the methodology surface is available; otherwise
  apply the discipline directly and ground every claim in the baseline source and named peer behavior.
