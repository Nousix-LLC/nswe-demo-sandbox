# COMPLETE — SUBTASK_afe_async_resources (Ferric 1.0, concern 4a)

**Task**: Design Ferric's async-resource + suspense capability as testable `REQ-ASYNC-*` requirements.
**Status**: completed (Atomic).
**Output**: `async-resources.md` (this workspace).

## What was done

Specified the async-resource primitive and its four declaratively-rendered states (loading / loaded /
empty / error) as the register `REQ-ASYNC-001 .. REQ-ASYNC-016`, within this child's assigned range
`001..019` (J1). The design states what an app author can express and the testable bar, not how the
framework is built, grounded in the real Ferric baseline at `Nousix-LLC/nswe-demo @ 276138f` (the
synchronous reactive core in `signal.rs`, verified via `gh api`: `create_signal` / `create_memo` /
`create_effect(impl FnMut)` / `batch`, `Copy` `Signal`/`Memo` handles, no async primitive, no
`wasm-bindgen-futures`).

## Coverage against success criteria

- Primitive + loading/loaded/empty/error states as testable requirements conforming to the parent schema:
  REQ-ASYNC-001 (primitive), 002 (four states), 003 (declarative render), 004 (empty first-class), 005
  (error carriage).
- Re-fetch on dependency change: REQ-ASYNC-006 (with out-of-order supersession) and 016 (cleanup);
  imperative refetch 007. Suspense/error boundary: 009 (aggregate), 010 (nested), 005 (error); 011
  (reload-vs-first-load).
- Composition with reactivity stated (008, 015); SSR addressed **by reference** to `REQ-SSR-*` (012, 013)
  — no `REQ-SSR-*` id minted, mechanism not designed, not left as an owl. Data source abstract (014) —
  `REQ-HTTP-*` referenced read-only, no `REQ-HTTP-*` minted.
- Checkable acceptance criteria use the schema's `example_build`, `automated_test`, and `doc_inspection`
  methods throughout.
- Peers compared by name (§4): Leptos `Resource`/`Suspense`, Solid `createResource`/`Suspense`, Dioxus
  `use_resource` — with the one deliberate divergence (empty as a first-class declared state) called out.

## Identities honored

J1 (ids within `001..019`, no overlap), J2 (covers the async clause of `REQ-FW-006`), J4 (additive over
the frozen surface — REQ-ASYNC-015), J5 (SSR and HTTP by reference only; no out-of-range id minted).
J3/J6/J7 are the synthesis child's to evaluate; every requirement carries the parent-schema fields for
that check.

## Composition with downstream

`async-resources.md` is one of the three fragments `SUBTASK_afe_synthesis` merges into the single
`../async-forms-events.md` register (repo target `design/ferric/async-forms-events.md`). This fragment
touches neither the event-payload seam (J3, owned by `SUBTASK_afe_events_payloads`) nor the forms range,
so it composes with the siblings without contention.

## Notes / assumptions

- This invocation ran as a reconstructed taskflow node. The methodology domain was unresolvable in this
  context (`engine_methodology_glob` / `engine_load_methodology` returned `agent_domain_unset`) and the
  app bundle exposed no filesets; the design was produced from the persona's product-design discipline and
  the inherited contracts/requirements. The `avoid-ai-writing` pass was applied by hand (no skill
  available) against the P0/P1 rules.
- SSR-composition requirements (012, 013) are staged `one_oh` because they are realizable only once
  `REQ-SSR-*` (SSR+hydration, itself `one_oh`) lands; the core resource/suspense surface is `usable_early`
  per `REQ-FW-006`.
