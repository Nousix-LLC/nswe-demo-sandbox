# Task: Ferric 1.0 — router design (owns REQ-RT-*; folds board issue #5)

## Task Specification
**Slug**: SUBTASK_router
**Task Kind**: standard
**Status**: Pending

### Objective
Design the Ferric 1.0 **client-side router** — the capability a Rust/WASM app author uses to navigate between
views — to a testable bar, reconciled additively with the existing frozen `ferric-router` surface, and state
how board issue #5 is superseded/extended by this design.

### Context
This is one spoke of the router + HTTP/JSON client concern of the Ferric 1.0 framework design (subtree hub:
`../_GLOBAL.md`). You own the `REQ-RT-*` register and nothing else. The HTTP/JSON client is a sibling spoke
(`SUBTASK_http`, owns `REQ-HTTP-*`); a synthesis gate composes both into one deliverable. `ferric-router`
exists today as a walking-skeleton composition root with a **frozen public `prelude` surface** — the parent
records it as exposing `Params`, `RoutePattern`, `Router`, `navigate`, `current_path`, `link`, with many leaf
bodies still `todo!()`. Read the real crate to confirm the exact surface. The 1.0 router design must build on
that frozen surface **additively** (identity SI2 / parent I9): extend it, never silently redefine or duplicate
it.

**Dependencies**: none (sibling of `SUBTASK_http`; both read the same upstream inputs).

### Scope to cover
This is the router as one coherent capability, with these facets, each carried to a testable `REQ-RT-*`:
- the **route table and matching**, with **path parameters**;
- **nested routes** (the depth a real multi-view app needs) and the **reactive outlet** that re-renders the
  matched view on path change;
- **in-app links** and **History-API navigation** (push/replace, back/forward, current path as reactive state);
- the **relationship to the frozen `ferric-router` surface**: what each existing `prelude` item is in the 1.0,
  and exactly what the 1.0 adds on top (for example nested routing, if it is not yet present) — every addition
  flagged as additive;
- the **fold of board issue #5**: what #5 becomes under the 1.0 plan (superseded or extended), so the release
  plan and backlog filing edit #5 rather than duplicate it.
Name these as the facets of one capability; your own evaluation decides whether they are one atomic design or
warrant their own sub-decomposition.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, the identities your output is held to. |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your register ownership (REQ-RT-*), the per-doc section layout, the identities. |
| Parent contract | `../../contracts/id_and_traceability_schema.yaml`, `../../contracts/_MANIFEST.yaml` | The REQ id schema, acceptance-criterion fields, `verification_method` and `stage` vocabularies. READ-ONLY. |
| 1.0 requirements frame | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-007` (routing), `REQ-FW-009` (frozen surfaces additive), the `usable_early`/`one_oh` staging, personas A1/A2, journey JA2. Specialize these; do not re-mint `REQ-FW-*`. |
| Router scaffold (#5) | `crates/ferric-router/` in `Nousix-LLC/nswe-demo` @ `276138f` (frozen `prelude`, README) | The exact frozen surface to extend additively. Read it; do not trust the summary alone. |
| Board issue #5 | `ferric-router` under epic #1, board `NSWE Delivery` | Its current scope, so you can state the fold. |
| Peer routers | leptos_router, Dioxus router | Named, honest comparison of routing models (nested routes, params, links, data/loaders where relevant). |

### Declared output
- `router.md` (this task's workspace) — the router design following the sub-contract's `doc_layout`: overview,
  relationship-to-frozen-surface (+ what 1.0 adds), the `REQ-RT-*` register with testable acceptance criteria,
  named peer comparison, and the #5 fold statement.

### Success criteria
- [ ] Route params, nested routes, and in-app links/navigation are each specified with testable `REQ-RT-*`
      acceptance criteria conforming to `../../contracts/id_and_traceability_schema.yaml` (each criterion
      checkable by a stranger, using a `verification_method` from the schema).
- [ ] The design is additive over the frozen `ferric-router` `prelude`; any change to an existing item is
      flagged additive, never a silent redefinition (SI2 / I9).
- [ ] The #5 fold is explicit — what #5 becomes under the 1.0 plan (SI3 / feeds I7).
- [ ] leptos_router and Dioxus router are compared by name.
- [ ] You write only `REQ-RT-*` ids (SI1 / I1); cross-references to other registers are read-only.

### Constraints
- Design, not implementation (what, not how). State the user-facing requirement, the architecture, and the
  testable bar; do not choose the matcher algorithm or internal data structures.
- Repository `Nousix-LLC/nswe-demo` only; nothing on GitHub carries host/cluster/SSH/path/environment detail.
- Select and load your own methodology (web routing / UI-framework API design, requirements engineering) and
  apply it. If the engine's methodology loader is unavailable, proceed on this brief and the design persona and
  record the assumption. Honor the writing-voice rules (plain, checkable prose; no machine-writing tells; run
  the avoid-ai-writing pass before finalizing).
