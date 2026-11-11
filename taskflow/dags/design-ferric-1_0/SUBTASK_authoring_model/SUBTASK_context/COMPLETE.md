# COMPLETE — SUBTASK_context (Ferric 1.0 authoring model, section C)

## What was done

Designed the Ferric 1.0 **context** mechanism — the authoring surface that lets an ancestor provide a value to a
subtree and any descendant read it without prop drilling — and its testable `REQ-API-060 … 079` bar. Design
(what the author writes and what must hold), not implementation. Output: `context.md` at this workspace. It
folds into `../authoring-model.md` at synthesis.

## Output

- `context.md` — the provide/read authoring surface (`provide_context` / `use_context -> Option<T>` /
  `expect_context -> T`), its reactivity interaction and scoped-cleanup behavior, the peer comparison, and the
  `REQ-API-060 … 070` register slice (`071 … 079` reserved) with testable acceptance criteria.

## Decompose evaluation

`Atomic`. One responsibility (design one mechanism's authoring surface + its register slice), one output. The
brief's three "facets" (provide/read, reactivity interaction, scoped cleanup) are angles on one API over one
reactive-runtime foundation, not distinct specialist concerns: the Distinct Concerns and Single-Responsibility
tests both cleared; token and output-size triggers cleared. Independent of the parent having split the authoring
model into three spokes.

## How it composes with the parent / siblings

- **Owns `REQ-API-060 … 079`** (identity IA1): assigned `060 … 070`, zero-padded 3-digit, monotonic; `071 … 079`
  reserved. No id outside the band.
- **Closes context seam IA3** (`../contracts/req_api_partition.yaml`): (1) context is read from inside a component
  body the `view!` macro renders (REQ-API-066); (2) context lifetime is bounded by the reactive owner scope, so a
  disposed scope releases it, reusing the baseline `ReactiveScope` owner tree and `no_stale_subscriber_leak`
  (REQ-API-068). Stated from the context side; synthesis asserts closure against the component/macro sides.
- **Additive over the frozen surface** (IA4 / parent `REQ-FW-009`): the only public change is three new
  `ferric::prelude` functions; `ReactiveScope` stays crate-internal; no frozen item redefined (REQ-API-069).
- **Verification** uses only the inherited vocabulary `automated_test` | `example_build` | `doc_inspection`
  (IA6), conforming to `../../contracts/id_and_traceability_schema.yaml`.
- **Specializes** parent `REQ-FW-005` (the context clause of the declarative authoring model); references
  `REQ-FW-009`, `REQ-FW-014` (the no-provider located-panic diagnostic).

## Success criteria

- [x] Provide/read, reactivity interaction, and scoped cleanup shown with author-facing snippets, including the
      no-provider case, concrete enough for a code DAG.
- [x] Context seam IA3 closed on both correspondences (readable in a component body; lifetime tied to the owner
      scope, consistent with `ReactiveScope` / `no_stale_subscriber_leak`).
- [x] Additive over the baseline; nothing frozen redefined.
- [x] `REQ-API-060 … 070` acceptance criteria testable, each naming an inherited `verification_method`.
- [x] Peers compared by name (Leptos, Dioxus, Sycamore, Yew, Solid) with trade-offs stated plainly.
- [x] avoid-ai-writing pass run over `context.md` (no P0/P1 tells).

## Notes

- Methodology syscall surface was unbound in this deployment (`agent_domain_unset`), as the hub anticipated; the
  design discipline was applied directly, grounded in the baseline `signal.rs`/`component.rs`/`lib.rs` and in
  named peer behavior verified against each framework's current documentation rather than recollection.
- Open items left for synthesis/implementation: the reserved band `REQ-API-071 … 079` for additive context
  requirements; the exact located-panic wording is stated as a shape, not fixed text.
