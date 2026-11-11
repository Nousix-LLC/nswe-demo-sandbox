# Task: Ferric 1.0 — context (sharing state without prop drilling) (authoring model, part C)

## Task Specification
**Slug**: SUBTASK_context
**Task Kind**: standard
**Status**: Pending

### Objective
Design **context** — the mechanism that lets an author provide a value to a subtree and read it from any
component beneath without threading it through every call — and its interaction with reactivity and scoped
cleanup. The authoring surface and its testable bar, not the implementation.

### Context
Part of the Ferric 1.0 authoring model (subtree hub: `../_GLOBAL.md`). This task owns the `REQ-API-*` band
**060–079** (see `../contracts/req_api_partition.yaml`). Today there is no context mechanism: shared values
must be passed through every component call. The bar (parent `REQ-FW-005`) is that an author can read a value
an ancestor provided without prop drilling. The design must sit soundly on the baseline reactive runtime
(`crates/ferric/src/signal.rs`), whose `ReactiveScope` owns reactive nodes and disposes them (with the
`no_stale_subscriber_leak` soundness property) when a scope is dropped.

### Distinct facets this mechanism must cover
Facets of one context mechanism, not separate deliverables:
- **Provide / read**: how a value is provided around a subtree and read from inside a component body, typed
  by the value's type (how lookup resolves, and what happens when no provider exists).
- **Reactivity interaction**: a context value may itself be a `Signal`/`Memo`, so a consumer that reads it
  re-renders on change — state how context composes with the reactive runtime rather than bypassing it.
- **Scoped cleanup**: context lifetime tied to the reactive owner scope, so a disposed scope releases its
  provided values and no stale reference survives — consistent with the baseline `ReactiveScope` owner tree.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, the authoring seam. |
| Subtree contract | `../contracts/` | Your `REQ-API-*` band (060–079); the context seam (IA3); verification vocab. READ-ONLY. |
| Parent 1.0 requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-005` to specialize (read-only). |
| Ferric baseline | `crates/ferric/src/signal.rs` (`Signal`/`Memo`/`create_effect`/`ReactiveScope` owner tree, `no_stale_subscriber_leak`), `component.rs`, `lib.rs` (frozen `prelude`) | The reactive runtime context must sit soundly on, additively. Representative checkout: `taskflow/dags/ferric-foundation/checkout/crates/ferric/`. |
| Peer precedent | Leptos `provide_context`/`use_context`, Sycamore context, Dioxus context, Solid context | By-name comparison of context designs in signal-based frameworks. |
| Seams | `../SUBTASK_view_macro/`, `../SUBTASK_components_props_slots/` (siblings; do not read their outputs — compose against the contract's context seam IA3) | Context is read from inside a component body the macro renders; the contract fixes that correspondence. |

### Declared output
- `context.md` (this task's workspace) — the context provide/read surface, its reactivity and scoped-cleanup
  interactions, and the `REQ-API-060..079` register slice with testable acceptance criteria. Folds into
  `../authoring-model.md` at synthesis.

### Success criteria
- [ ] Provide/read, reactivity interaction, and scoped cleanup are shown with example snippets of **what an
      author writes**, concrete enough for a code DAG to build, including the no-provider case.
- [ ] The context seam (IA3) is closed: context is readable from inside a component body and its lifetime is
      tied to the reactive owner scope (a disposed scope releases it), consistent with the baseline
      `ReactiveScope` / `no_stale_subscriber_leak` property.
- [ ] The design is additive over the baseline reactive surface; nothing frozen is redefined.
- [ ] `REQ-API-060..079` acceptance criteria are testable and use an inherited `verification_method`,
      conforming to `../../contracts/id_and_traceability_schema.yaml`.
- [ ] Peer context designs compared by name; trade-offs stated plainly.

### Constraints
- Write `REQ-API-*` ids only within band **060–079** (identity IA1). Design, not implementation.
- Honor the writing-voice rules; run the avoid-ai-writing pass over `context.md` before finalizing.
- Select and load your own reactive-scope / state-sharing design methodology if available; otherwise apply the
  discipline directly, grounded in the baseline reactive runtime and named peer behavior.
