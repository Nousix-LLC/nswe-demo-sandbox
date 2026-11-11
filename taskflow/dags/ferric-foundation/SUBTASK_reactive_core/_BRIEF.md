# Task: Implement the reactive core (`signal.rs`)

**Slug**: SUBTASK_reactive_core
**Task Kind**: standard
**Status**: Pending

## Objective
Implement `ferric`'s reactive state graph in `crates/ferric/src/signal.rs` — signals, derived/
computed values, reactive effects, and batched updates — such that it is **sound** (no stale
subscriber leaks) and fully exercised by native unit tests that run without a browser.

## Context
Part of the `ferric-foundation` subtree (see `../_GLOBAL.md`). You run after `SUBTASK_scaffold`,
on the shared clone at `../checkout/`, and replace the `todo!()` body of the `signal` module it
stubbed. The view layer and DOM runtime depend on your **real** behavior (that is why this edge is
serialized, not mocked), so correctness and soundness here are load-bearing for everything above.

**Dependencies**: `SUBTASK_scaffold`. **Dependents**: `SUBTASK_view_and_diff`, `SUBTASK_dom_runtime`,
`SUBTASK_synthesis`.

## Inputs
- `../_GLOBAL.md`; `../contracts/ferric_api.rs` (read-only — the frozen `signal` surface you
  implement: `Signal<T>` get/with/set/update, `create_signal`, `Memo`/`create_memo`,
  `create_effect`, `batch`); `../contracts/_MANIFEST.yaml`.
- The scaffolded clone at `../checkout/` (your predecessor's real output).

## Scope (what this task delivers)
- A working fine-grained reactive runtime behind the frozen `signal` API: reads inside a reactive
  observer (effect/memo) subscribe automatically; writes notify; `create_memo` gives lazy
  memoized derived values; `batch` coalesces notifications into one flush; `create_effect` runs
  once then re-runs on dependency change.
- **Soundness**: dropping an effect/scope must unsubscribe it — setting a signal after its only
  subscriber is gone must not touch freed state or grow the subscriber set unboundedly. This is
  the `no_stale_subscriber_leak` identity; prove it with a native test.
- Native `#[test]` coverage of signals, computed values, batching, and subscriber cleanup.
- Rustdoc on all public items you own.
- Internal representation (arena / slotmap / `Rc<RefCell<…>>` / generational keys) is **your
  design** — only the frozen public signatures are fixed. If a frozen signature proves wrong,
  request an additive amendment; do not edit `contracts/` or diverge silently.

Keep the module cohesive and clippy/fmt-clean so the downstream layers and the synthesis gate
build on green.

## Outputs
- `../checkout/crates/ferric/src/signal.rs` (final implementation + its native tests).
- `COMPLETE.md` recording the design chosen and the test results.

## Success criteria
- [ ] Frozen `signal` surface implemented and documented; `use ferric::prelude::*;` still resolves.
- [ ] `cargo test` for the reactive core passes natively (signals, computed, batching, cleanup).
- [ ] A native test demonstrates no stale-subscriber leak after a subscriber is dropped.
- [ ] `cargo fmt --check` and `cargo clippy --all-targets -- -D warnings` clean for your module.
- [ ] Crate still builds for host and `wasm32-unknown-unknown`.

## Suggested Methodology Files
Matched Domain-Mapping rows (verbatim): **Writing Rust code → Primary: Rust; Supporting: Core,
Code Quality**; **Writing tests → Primary: Testing; Supporting: Core**. Load on-demand:
- `rust/Rust_Ownership_Borrowing_Methodology.md` — the subscriber graph lives or dies on ownership
  and interior-mutability choices; soundness is the whole game here.
- `rust/Rust_Type_System_Methodology.md` — ergonomic generic `Signal<T>`/`Memo<T>` handles.
- `rust/Rust_Error_Handling_Methodology.md` — avoid panics in the public surface; model failure.
- `rust/Rust_Testing_Methodology.md` + `testing/Testing_Unit_Testing_Methodology.md` — strategy for
  unit-testing a reactive core (observing notifications, asserting cleanup) without a browser.
- `core/BestPractices_Coding_Standards_Methodology.md` — baseline standards.
Parent's flagged starting points; you are the final judge of what you load.

## Inherited Constraints
- Match the frozen `signal` surface in `contracts/ferric_api.rs` (additive-only).
- Edition 2021+, stable; no new heavy deps (lean core — `wasm-bindgen`/`web-sys`/`js-sys` only
  unless you justify a tiny, well-scoped addition and note it in `COMPLETE.md`).
- Work only in `../checkout/`; commit on `work/ferric-foundation`; never touch `main`.
- Public API must stay ergonomic for an eventual Twitter-style SPA.

## Out-of-Scope Methodologies
- No vdom/diff, component, or DOM/web-sys work — those are later spokes. Do not add browser-only
  code paths to `signal.rs`; the reactive core must be native-testable.
