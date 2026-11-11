# _GLOBAL.md — authoring-model subtree hub (Ferric 1.0, concern 3)

## Project Context

**Status**: Active

### Objective

Design Ferric 1.0's **declarative authoring model** — what an app author writes to build real UI without
builder-call boilerplate — to a testable `REQ-API-*` bar, and deliver it as **one** design document
`authoring-model.md` (repo target `design/ferric/authoring-model.md`). This subtree writes **design, not
framework code**, and states the **authoring surface and its testable bar — what the author writes and what
must work — not the macro's internal expansion**.

This is concern 3 of the Ferric 1.0 framework design (parent hub: `../../_GLOBAL.md`). This spoke owns the
`REQ-API-*` register (parent identity I1). Today, components are plain `Fn() -> VNode` closures hand-built with
`VElement::new("div").child(...)` builder calls (see the baseline below); the bar this subtree must meet is
that **real apps can be written ergonomically without that boilerplate** (parent `REQ-FW-005`), with
**actionable compile-time diagnostics** (parent `REQ-FW-014`), **additively over the frozen `VNode`/component
surface** (parent `REQ-FW-009`).

### Why this is decomposed

My brief names three genuinely distinct design concerns, each with its own design methodology and its own
specialist shape: a **macro/DSL grammar + lowering + compile-diagnostics** problem; a **Rust type-system
component-API ergonomics** problem; and a **reactivity + scoped-cleanup** problem. The scope and
distinct-concerns triggers fire on that enumeration, so the concern is split into three parallel design spokes
plus a synthesis that folds them into the single `authoring-model.md`. The seam between them — how the macro
invokes a component, how a component declares what it accepts, and how context is read inside a component — is
fixed up front in `contracts/` so the three sections compose into one coherent authoring story rather than
diverging and being reconciled late.

### Scope

**In Scope:**
- The `view!` macro authoring surface: elements, attributes, event handlers, conditionals, lists/keys,
  interpolated reactive values; how it lowers onto the existing `VNode` model; compile-time diagnostics
  quality (a `trybuild`-checkable story). (`SUBTASK_view_macro`)
- The component model: typed props declaration, children, named slots, and composition; ergonomics against
  Rust's type system. (`SUBTASK_components_props_slots`)
- Context: sharing state down the tree without prop drilling, and its interaction with reactivity and scoped
  cleanup. (`SUBTASK_context`)
- The consolidated `authoring-model.md` + the merged, de-duplicated `REQ-API-*` register, with the macro's
  relationship to the existing `VNode`/keyed-diff model stated as additive, and named peer view-macros
  compared. (`SUBTASK_synthesis`)

**Out of Scope:**
- The macro's internal token-level expansion as an implementation (the design states *what the author writes*
  and *what must hold*, not how the proc-macro is built).
- Any `REQ-*` register other than `REQ-API-*` (parent identity I1). Cross-references to `REQ-FW-*`,
  `REQ-SSR-*`, `REQ-ASYNC-*`, etc. are read-only.
- SSR-specific hydration of the macro output (owned by `REQ-SSR-*`); async/suspense and forms/events authoring
  (owned by `REQ-ASYNC-*`). Where the macro must interoperate with those, this subtree states the seam from
  the authoring side and names the owning area.

### Success Criteria

- [ ] The macro's authoring surface, the props/children/slots/composition model, and context are specified
      concretely enough for a code DAG to build, each with example snippets of **what an author writes**.
- [ ] `REQ-API-*` acceptance criteria are testable (example builds, `trybuild` macro diagnostics, headless
      `wasm-bindgen-test`), conforming to `../../contracts/id_and_traceability_schema.yaml`.
- [ ] The macro's relationship to the existing `VNode`/keyed-diff model is stated (additive over the
      foundation; nothing in the frozen `prelude` is redefined).
- [ ] Peer view-macros (Leptos `view!`, Sycamore `view!`, Dioxus `rsx!`, Yew `html!`) are compared **by
      name**, with ergonomic trade-offs stated plainly.
- [ ] One `authoring-model.md` is produced at this workspace root; the three section drafts fold into it with
      no section unplaced or double-placed, and the merged `REQ-API-*` register has no id collision.

---

## Constraints and Requirements

### Process / quality constraints (inherited from `../../_GLOBAL.md`)
- **What, not how.** Each requirement reads as something a stranger could check against the framework: a
  surface the author writes, a build that succeeds, a diagnostic that fires. No chosen internal data structure
  or code path.
- **Additive over the frozen surface.** Everything lowers onto the baseline `VNode` / `VElement` /
  `EventKind` / `EventHandler` / `Component` model and the frozen `ferric::prelude`; new items are additive,
  nothing is redefined (parent `REQ-FW-009`, parent identity I9 analog).
- **Evidence over memory.** Peer view-macros are cited by name; "common practice" rests on documented peer
  behavior, not recollection.
- **Writing voice.** Plain, checkable prose. No machine-writing tells. Each child runs the avoid-ai-writing
  pass over its section draft before finalizing; the synthesis runs it over the consolidated document.

### Methodology
No methodology is named by the parent. Each child **selects and loads its own** design methodology for its
concern (macro/DSL design for the view macro; API / type-system-ergonomics design for the component model;
reactive-scope design for context) and applies it. The methodology syscall surface may be unbound in this
deployment; if so, the child applies its design discipline directly and grounds every claim in the baseline
source and named peer behavior.

---

## Input Specifications

| Source | Location | Purpose |
|--------|----------|---------|
| Parent hub | `../../_GLOBAL.md` | Framework-wide context, constraints, the parent contract. |
| Parent contract | `../../contracts/` | `REQ-*` id/traceability schema, stage + verification vocab, artifact map. READ-ONLY. |
| This subtree's contract | `contracts/` | The `REQ-API-*` sub-partition + the authoring-seam identities. READ-ONLY for children. |
| 1.0 requirements | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` | The cross-cutting frame to specialize (esp. `REQ-FW-005`, `REQ-FW-009`, `REQ-FW-014`). |
| Ferric baseline | `crates/ferric/` — `vdom.rs` (`VNode`/`VElement`/`EventKind`/`EventHandler`/keyed `diff`), `component.rs` (`Component`, `Fn() -> VNode`), `signal.rs` (`Signal`/`Memo`/`create_effect`/`ReactiveScope` owner tree), `examples/counter.rs`, `lib.rs` (frozen `prelude`) | The builder-call model the macro replaces and the surface it lowers onto. A representative checkout is under `taskflow/dags/ferric-foundation/checkout/crates/ferric/`. |
| Peer precedent | Leptos `view!`, Sycamore `view!`, Dioxus `rsx!`, Yew `html!` (Rust); Solid/Vue JSX/templates (analog) | Honest, by-name comparison of Rust view-macro designs. |

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/                         (REQ-API-* partition + authoring-seam identities — READ-ONLY)
│   ├── _MANIFEST.yaml
│   └── req_api_partition.yaml
├── SUBTASK_view_macro/                (the view! macro surface, lowering, diagnostics — REQ-API band A)
├── SUBTASK_components_props_slots/     (props/children/slots/composition — REQ-API band B)
├── SUBTASK_context/                   (context + reactivity/scoped-cleanup — REQ-API band C)
└── SUBTASK_synthesis/                 (fold → authoring-model.md + merged register; gate; resume parent)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_view_macro` | none | The `view!`/JSX-style macro authoring surface: elements, attributes, event handlers, conditionals, lists/keys, interpolated reactive values; how it lowers onto `VNode`; the `trybuild`-checkable compile-diagnostics story. Writes `REQ-API-*` band A. | `view-macro.md` |
| `SUBTASK_components_props_slots` | none | The component model: typed props declaration, children, named slots, composition; ergonomics against Rust's type system. Writes `REQ-API-*` band B. | `components-props-slots.md` |
| `SUBTASK_context` | none | Context: sharing state down the tree without prop drilling; interaction with reactivity and the reactive owner scope / scoped cleanup. Writes `REQ-API-*` band C. | `context.md` |
| `SUBTASK_synthesis` | `SUBTASK_view_macro`, `SUBTASK_components_props_slots`, `SUBTASK_context` | Verify the authoring-seam identities (IA1–IA6), fold the three section drafts + their register slices into one `authoring-model.md` with a merged `REQ-API-*` register and a by-name peer comparison; run the avoid-ai-writing pass; fold the parent. | `../authoring-model.md`, `../SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_view_macro ─────────────┐
SUBTASK_components_props_slots ──┼─► SUBTASK_synthesis ─► (authoring-model.md + fold parent)
SUBTASK_context ────────────────┘
```

---

## Contract

**REQUIRED and present** at `contracts/` (read-only for every child). The three spokes are parts of one
authoring model and share a tight seam: they all write into the one `REQ-API-*` register, and the macro
invokes components whose props/children/slots the component spoke defines and whose context the context spoke
defines. The contract fixes that seam before any child runs so the three sections recompose mechanically into
`authoring-model.md`.

**Contract location**: `contracts/` · **Contract kind**: `yaml_schema` (a `REQ-API-*` band partition + the
authoring-seam identities). It **extends** the parent contract (`../../contracts/`) and overrides nothing:
`REQ-API-*` id shape, the `verification_method` vocabulary, the `stage` vocabulary (`usable_early` | `one_oh`),
and `release_gating` are all inherited.

### Inherited contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Ferric 1.0 id/traceability schema | `../../contracts/id_and_traceability_schema.yaml` | `REQ-API-*` id pattern; `verification_method` vocab; `stage` vocab; `release_gating`. |
| Ferric 1.0 manifest | `../../contracts/_MANIFEST.yaml` | `REQ-API-*` ownership (this spoke); parent identities I1 (disjoint registers) and I9 (frozen surfaces). |

### Ownership (REQ-API band + output per child)

| Child | Owns `REQ-API-*` band | Output |
|---|---|---|
| `SUBTASK_view_macro` | `REQ-API-001` … `REQ-API-029` | `view-macro.md` |
| `SUBTASK_components_props_slots` | `REQ-API-030` … `REQ-API-059` | `components-props-slots.md` |
| `SUBTASK_context` | `REQ-API-060` … `REQ-API-079` | `context.md` |
| `SUBTASK_synthesis` | (mints no new `REQ-API-*`; consolidates) | `../authoring-model.md`, `../SYNTHESIS.md` |

### Identities (the synthesis gate asserts these; no silent plugs)

- [ ] **IA1 — disjoint REQ-API bands.** Each spoke writes only its own `REQ-API-*` band; the three bands do
      not overlap; every id is zero-padded 3-digit and monotonically assigned within its band.
- [ ] **IA2 — component-invocation seam closes.** Every way the `view!` macro passes a prop, a child, or a
      named slot to a component corresponds to a declaration form the component model defines, and every
      component declaration form is reachable from the macro. No orphan on either side.
- [ ] **IA3 — context access seam closes.** The way an author provides and reads context is expressible from
      inside a component body (the unit the macro renders), and context lifetime is tied to the reactive owner
      scope so a disposed scope releases its context — consistent with the baseline `ReactiveScope` owner tree
      and the `no_stale_subscriber_leak` soundness property.
- [ ] **IA4 — additive over the frozen surface.** Every authoring construct lowers onto the baseline
      `VNode`/`VElement`/`EventKind`/`EventHandler`/`Component` model and the frozen `ferric::prelude`
      additively; no frozen item is redefined (parent `REQ-FW-009` / I9).
- [ ] **IA5 — one consolidated deliverable.** `authoring-model.md` contains all three sections and the merged
      `REQ-API-*` register exactly once; no section unplaced or double-placed; no id collision across bands.
- [ ] **IA6 — testable diagnostics + criteria.** The macro's diagnostics story is `trybuild`-checkable, and
      every `REQ-API-*` acceptance criterion uses a `verification_method` from the inherited vocabulary
      (`automated_test` | `example_build` | `doc_inspection`).

### Derived artifacts

- `req_api_partition.yaml` is the band map the synthesis gate runs IA1 and IA5 against.
- The three section drafts (`view-macro.md`, `components-props-slots.md`, `context.md`) are the sources the
  synthesis folds into `../authoring-model.md`.

---

## Output Specifications

| Deliverable | Location | Description |
|-------------|----------|-------------|
| `authoring-model.md` | `../authoring-model.md` (this spoke's workspace root) | The consolidated authoring model + merged `REQ-API-*` register. The outer `SUBTASK_design_pr` places it at `design/ferric/authoring-model.md`. |
| `SYNTHESIS.md` | `../SYNTHESIS.md` (fold location = this spoke's workspace root) | The fold record: how the three sections composed, IA1–IA6 assertions, the merged register. |
