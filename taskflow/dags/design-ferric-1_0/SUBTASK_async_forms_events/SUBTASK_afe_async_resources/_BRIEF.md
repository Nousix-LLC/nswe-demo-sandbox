# Task: Async resources + suspense (Ferric 1.0, concern 4a)

## Task Specification
**Slug**: SUBTASK_afe_async_resources
**Task Kind**: standard
**Status**: Pending

### Objective
Design Ferric's reactive **async-resource** capability: a primitive that lets an app author load data
asynchronously and render its **loading / loaded / empty / error** states declaratively, composing with
the existing signal reactivity. State it as testable behavior from the app author's side — what they can
express and what must work — registered as `REQ-ASYNC-*` requirements.

### Context
Part of concern 4 of the Ferric 1.0 design (see `../_GLOBAL.md` for the baseline facts and the frame).
This is one of three sibling capabilities; it is the async/suspense one. Today `crates/ferric` has a
**synchronous** reactive core (`create_effect` is `FnMut()`) and **no async primitive**; the core
depends only on `wasm-bindgen`/`web-sys`/`js-sys`. The upstream `REQ-FW-006` requires "distinct loading,
loaded, empty, and error states (suspense)." This task makes that concrete.

**Dependencies**: none within this subtree.

### Scope to cover
- A reactive **async-resource** primitive: how an author declares an async data source and reads its
  current state (loading / loaded / empty / error) reactively, so the view renders each state
  declaratively rather than through hand-rolled loading flags.
- How a resource **re-fetches** when a reactive input it depends on changes.
- How loading and error states are expressed in the view (the suspense-style boundary, whatever shape
  you specify), including nested/multiple pending resources.
- **Composition with reactivity** — how the resource's state participates in the signal/effect graph.
- **Composition with SSR by reference only** — how a resource resolves during a server render and hands
  its resolved state to the client so hydration does not refetch. Reference `REQ-SSR-*` read-only; do
  **not** mint any `REQ-SSR-*` id or design the hydration mechanism (that is `SUBTASK_ssr_hydration`).
- The data source is abstract: compose with a fetch/async source by reference; do **not** define the
  HTTP/JSON client (`REQ-HTTP-*`).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Baseline facts (reactive core, no async today), constraints, the frame. |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your id range and the identities you must satisfy. |
| Parent contract | `../../contracts/id_and_traceability_schema.yaml` | REQ field/stage/verification vocabularies. |
| Upstream requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-006` (the async clause) and the `usable_early`/`one_oh` staging. |
| Ferric baseline | `Nousix-LLC/nswe-demo` @ `276138f`, `crates/ferric/src/{signal,dom}.rs` | The reactive core your primitive composes with (read via `gh api`). |
| Peer precedent | Leptos `Resource`/`Suspense`, Solid `createResource`/`Suspense`, Dioxus `use_resource` | Honest comparison; cite by name. |

### Declared output
- `async-resources.md` (this task's workspace) — the async-resource + suspense design and the
  `REQ-ASYNC-001..019` register.

### Success criteria
- [ ] The async-resource primitive and its loading/empty/loaded/error states are specified as testable
      `REQ-ASYNC-*` requirements (ids within `REQ-ASYNC-001..019`) conforming to the parent schema.
- [ ] Re-fetch-on-dependency-change and the suspense/error boundary behavior are specified.
- [ ] Composition with reactivity is stated; SSR resolution is addressed **by reference** to
      `REQ-SSR-*`, not designed here and not left as an owl.
- [ ] At least one acceptance criterion is checkable the way the schema's `verification_method`
      vocabulary allows (e.g. `example_build`, `automated_test`).
- [ ] Peer approaches (Leptos/Solid/Dioxus) compared by name.

### Constraints
- `REQ-ASYNC-*` only, within your assigned range (sub-identity J1). Design, not implementation.
- Additive over the frozen `ferric` surface; never redefine a frozen item (J4).
- Mint no `REQ-SSR-*` / `REQ-HTTP-*` id; cross-references are read-only (J5, parent I1).
- Honor the writing-voice rules in `../_GLOBAL.md`. Select and load your own methodology.
