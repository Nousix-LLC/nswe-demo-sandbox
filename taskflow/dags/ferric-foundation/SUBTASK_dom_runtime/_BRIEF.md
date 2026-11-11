# Task: Implement the DOM runtime + counter example + README (`dom.rs`, `examples/counter.rs`)

**Slug**: SUBTASK_dom_runtime
**Task Kind**: standard
**Status**: Pending

## Objective
Implement `ferric`'s browser runtime: `mount(root, component)` that renders a component's view tree
into real DOM via `wasm-bindgen` + `web-sys`, re-renders by applying the keyed patch when signals
change, and binds click + input events — then prove it end-to-end with a small **counter** example
that builds to wasm, and document the crate in `README.md`.

## Context
Part of the `ferric-foundation` subtree (see `../_GLOBAL.md`). You run after
`SUBTASK_view_and_diff`, on the shared clone at `../checkout/`, and replace the `todo!()` body of
the `dom` module. You compose against the **real** reactive core and view/diff layers (that is why
this edge is serialized). You are the last implementation layer, so the crate should be complete
and shippable after you.

**Dependencies**: `SUBTASK_view_and_diff`. **Dependents**: `SUBTASK_synthesis`.

## Inputs
- `../_GLOBAL.md`; `../contracts/ferric_api.rs` (read-only — the frozen `dom::mount` surface, and
  the `vdom`/`signal` surfaces you consume); `../contracts/_MANIFEST.yaml`.
- The clone at `../checkout/` with the real reactive core and view/diff layers in place.

## Scope (what this task delivers)
- `mount(root, component)`: wrap rendering in a reactive effect (`create_effect`) so a signal
  change re-renders; apply the view layer's keyed `Patch` list to the live DOM via `web-sys`
  (create/update/move/remove real nodes), rather than rebuilding the subtree.
- Event binding for at least **click** and **input**, dispatching to the handlers carried on the
  view tree.
- A tiny **counter** example (`crates/ferric/examples/counter.rs`, or an `examples/counter` crate
  if you justify that layout) that mounts, increments on click, and reflects the signal — and
  **builds** for `wasm32-unknown-unknown`.
- `crates/ferric/README.md`: the counter example + a short architecture note (signals → view →
  keyed diff → DOM patch). Ensure rustdoc exists on your public items.
- A `wasm-bindgen-test` if the toolchain (`wasm-bindgen-test-runner` + a headless browser)
  installs cleanly in this environment. **If it does not, do not fail** — note it in `COMPLETE.md`
  so the synthesis gate can record it; the native tests remain the gate and the wasm **build**
  (not run) stays mandatory.
- fmt/clippy-clean; the whole crate builds host + wasm.

## Outputs
- `../checkout/crates/ferric/src/dom.rs`, `../checkout/crates/ferric/examples/counter.rs`,
  `../checkout/crates/ferric/README.md`.
- `COMPLETE.md` recording the runtime design, the wasm build result, and whether wasm-bindgen-test
  ran (and if not, why).

## Success criteria
- [ ] `mount` renders the view tree to real DOM and re-renders via keyed patch on signal change.
- [ ] Click + input events are bound and dispatch to view-tree handlers.
- [ ] The counter example builds for `wasm32-unknown-unknown`.
- [ ] `README.md` present with the counter example + architecture note; public items documented.
- [ ] fmt/clippy clean; crate builds host + wasm. wasm-bindgen-test run-or-documented-as-skipped.

## Suggested Methodology Files
Matched Domain-Mapping rows (verbatim): **Writing Rust code → Primary: Rust; Supporting: Core,
Code Quality**; **Rust FFI / unsafe code → Primary: Rust; Supporting: Security**. Load on-demand:
- `rust/Rust_Unsafe_FFI_Methodology.md` — `wasm-bindgen`/`web-sys` is the JS/DOM FFI boundary;
  keep the unsafe/boundary surface small and correct.
- `rust/Rust_Ownership_Borrowing_Methodology.md` — closures bound to DOM events + the effect that
  owns the render loop are the ownership-tricky part.
- `rust/Rust_Cargo_Ecosystem_Methodology.md` — `examples/` wiring and the wasm target/test runner.
- `core/BestPractices_Coding_Standards_Methodology.md` + `operations/BestPractices_Documentation_Methodology.md`
  — the README + rustdoc are an acceptance criterion.
- `testing/Testing_Unit_Testing_Methodology.md` — for any wasm-bindgen-test you add.
Parent's flagged starting points; you are the final judge of what you load.

## Inherited Constraints
- Match the frozen `dom::mount` surface; consume (do not redefine) the `vdom`/`signal` surfaces.
- Edition 2021+, stable; lean deps (`wasm-bindgen`, `web-sys` features as needed, `js-sys`).
- Work only in `../checkout/`; commit on `work/ferric-foundation`; never touch `main`.
- Keep the vdom/patch application small but correct; API ergonomic for a later Twitter-style SPA.

## Out-of-Scope Methodologies
- Do not re-implement the reactive core or the diff — import and use them.
- Do not push the branch or open the PR, and do not author `SYNTHESIS.md` — that is
  `SUBTASK_synthesis` (the verification gate). Your job ends at a complete, building, documented crate.
