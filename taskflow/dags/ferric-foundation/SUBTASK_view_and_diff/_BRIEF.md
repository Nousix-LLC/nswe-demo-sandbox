# Task: Implement the view layer — component model + keyed diff (`vdom.rs`, `component.rs`)

**Slug**: SUBTASK_view_and_diff
**Task Kind**: standard
**Status**: Pending

## Objective
Implement `ferric`'s **view representation and reconciliation**: the `VNode` view tree, the
`Component` abstraction (trait + function components) that produces it, and a minimal but correct
**keyed** `diff` that computes the patch list between two trees — all pure and native-testable.

## Context
Part of the `ferric-foundation` subtree (see `../_GLOBAL.md`). You run after
`SUBTASK_reactive_core`, on the shared clone at `../checkout/`, and replace the `todo!()` bodies of
the `vdom` and `component` modules. You build against the **real** reactive core (components read
real `Signal`s). The DOM runtime depends on your real `VNode`/`Patch`/`Component` output.

This task spans two related but distinct concerns — **(a)** the view/component representation and
**(b)** the keyed diff/patch algorithm. They share the `VNode` type and are tightly coupled, so
they are briefed together; run your own atomic-vs-decompose evaluation against them and split
further if your reading finds that warranted.

**Dependencies**: `SUBTASK_reactive_core`. **Dependents**: `SUBTASK_dom_runtime`, `SUBTASK_synthesis`.

## Inputs
- `../_GLOBAL.md`; `../contracts/ferric_api.rs` (read-only — the frozen `vdom`/`component` surface:
  `VNode`, `VElement`, `Key`, `EventKind`, `EventHandler`, `Patch`, `diff`, `Component`);
  `../contracts/_MANIFEST.yaml`.
- The clone at `../checkout/` with the real reactive core in place.

## Scope (what this task delivers)
- The `VNode` tree (element/text), element nodes carrying tag, optional **key**, attributes,
  event bindings (at least click + input via `EventKind`), and children.
- A `Component` abstraction: the trait with `render(&self) -> VNode`, and function-component
  support (`Fn() -> VNode`). Ergonomic enough to express SPA views later.
- A **keyed** `diff(old, new) -> Vec<Patch>` that produces a minimal, correct patch list
  (including keyed child insert/move/remove) for the DOM runtime to apply. `Patch`'s concrete
  variants are your design.
- Native `#[test]` coverage of the diff: text/attr changes, child add/remove/reorder by key, and
  no-op equality. Rustdoc on public items.
- fmt/clippy-clean; crate still builds for host and wasm.

## Outputs
- `../checkout/crates/ferric/src/vdom.rs` and `../checkout/crates/ferric/src/component.rs`
  (final implementations + the diff's native tests).
- `COMPLETE.md` recording the view/diff design and test results.

## Success criteria
- [ ] Frozen `vdom`/`component` surface implemented + documented; prelude still resolves.
- [ ] Keyed diff produces correct minimal patches; covered by passing native tests.
- [ ] Components (trait + function form) produce a `VNode` tree and may read reactive signals.
- [ ] fmt/clippy clean for your modules; crate builds host + `wasm32-unknown-unknown`.

## Suggested Methodology Files
Matched Domain-Mapping rows (verbatim): **Writing Rust code → Primary: Rust; Supporting: Core,
Code Quality**; **Writing tests → Primary: Testing; Supporting: Core**. Load on-demand:
- `rust/Rust_Trait_Design_Methodology.md` — the `Component` trait + function-component ergonomics
  are the core API-design decision of this layer.
- `rust/Rust_Type_System_Methodology.md` — modelling `VNode`/`Patch` cleanly as enums.
- `rust/Rust_Ownership_Borrowing_Methodology.md` — event handler boxing and tree ownership.
- `code-quality/Framework_Clean_Code_Methodology.md` — the diff is the trickiest logic in the
  crate; keep it readable and correct.
- `testing/Testing_Unit_Testing_Methodology.md` + `rust/Rust_Testing_Methodology.md` — table-driven
  tests for diff cases.
Consider `architecture/Architecture_Design_Notes_Methodology.md` if you decide the component/render
boundary warrants a short design note. Parent's flagged starting points; you are the final judge.

## Inherited Constraints
- Match the frozen `vdom`/`component` surface (additive-only); keep keyed-diff capability.
- Edition 2021+, stable; lean deps; API ergonomic for an eventual Twitter-style SPA.
- Work only in `../checkout/`; commit on `work/ferric-foundation`; never touch `main`.
- The diff and view tree must be **pure/native-testable** — no web-sys calls here (the DOM runtime
  applies the patches).

## Out-of-Scope Methodologies
- No DOM/web-sys rendering, `mount`, or the counter example — those are `SUBTASK_dom_runtime`.
- Do not re-implement or mock the reactive core; import and use the real `signal` surface.
