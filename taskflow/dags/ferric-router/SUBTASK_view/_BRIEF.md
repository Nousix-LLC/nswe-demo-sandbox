# Task: ferric-router Link helper + wasm example + README

## Task Specification
**Slug**: SUBTASK_view
**Task Kind**: standard
**Status**: Pending

### Objective
Implement the declarative `link` navigation helper in `src/link.rs`, a 2–3 route wasm example in
`examples/app.rs` that exercises the whole router end-to-end, and a `README.md` with the example and an
architecture note.

### Context
Part of the `ferric-router` work-item (see `../_GLOBAL.md`, `../contracts/`). Fourth task in the serial
pipeline: the real `matcher` and `router` modules now exist — compose against them directly. You fill the
`link` module body, replace the scaffold's example stub, and write the README.

**Dependencies**: `SUBTASK_navigation`. **Dependents**: `SUBTASK_synthesis`.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | context + the verified ferric event constraint |
| Frozen contract | `../contracts/ferric_router_api.rs` (link module + prelude) | the `link` signature to MATCH; the prelude you import in the example |
| Real router + matcher | `checkout/crates/ferric-router/src/{router,matcher}.rs` (COMPLETED) | `Router`, `navigate`, `current_path`, outlet you compose with |
| `ferric` surface + counter example | cloned `crates/ferric` src, README, `examples/counter.rs` | the `VElement`/`EventKind`/`mount` idioms to mirror |
| Shared clone | `<subtree_root>/checkout/` on `work/ferric-router` | the tree you edit + commit in |

## What to do (approach — your design, not a script)
- **`src/link.rs`**: implement `link(to, label) -> VNode` per the contract. **ferric event constraint
  (verified, see hub):** the click handler is `Fn()` with no event arg, so you CANNOT `preventDefault()`.
  Emit an element the browser will not full-page-navigate on (e.g. a styled non-`<a>` element, or an
  `<a>` without a followed href) carrying a `ferric` `EventKind::Click` handler that calls `navigate(to)`.
  Document the choice in rustdoc. You MAY additionally expose a richer builder additively.
- **`examples/app.rs`**: a small SPA with 2–3 routes (e.g. `/`, `/about`, `/user/:id`) that builds a
  `Router` (`route`/`fallback`/`mount_history`), mounts `router.outlet()` with `ferric::mount`, and uses
  `link(...)` for a nav bar and `navigate(...)` for a programmatic jump. Must build to
  `wasm32-unknown-unknown`. Mirror the counter example's structure.
- **`README.md`**: the example walk-through + a short architecture note (route table/matcher, reactive
  current-path, History API integration, outlet, `<Link>`), how to build to wasm, and the documented
  `preventDefault` composition constraint. Keep it concise.
Commit on `work/ferric-router` when the example builds to wasm and fmt/clippy are clean.

## Outputs (you own)
- `checkout/crates/ferric-router/src/link.rs` (final implementation)
- `checkout/crates/ferric-router/examples/app.rs` (the 2–3 route example)
- `checkout/crates/ferric-router/README.md`
- a commit; `COMPLETE.md` recording the design + the example wasm build result.

## Success Criteria
- [ ] `link` matches the frozen signature (compiler-checked); rustdoc explains the non-anchor/preventDefault choice.
- [ ] `examples/app.rs` uses `Router` + outlet + `link` + `navigate`; `cargo build -p ferric-router --example app --target wasm32-unknown-unknown` exits 0.
- [ ] `README.md` present with example + architecture note + wasm build instructions.
- [ ] `cargo fmt` clean; no clippy warnings in owned files; all public items documented.

## Constraints
- `../contracts/` READ-ONLY; MATCH `link`'s signature. Compose with the REAL `router`/`matcher` and with `ferric`.
- Edit only `src/link.rs`, `examples/app.rs`, `README.md`; NEVER touch `main`; no attribution trailers.

## Suggested Methodology Files (parent's flags — you are the final judge)
Task type: **Writing Rust code** (UI-composition helper) + documentation → primary **Rust**, **Core**,
supporting **Code Quality**.
- `rust` — `rust/Rust_Ownership_Borrowing_Methodology.md` (`'static` click closures over `to`),
  `rust/Rust_Trait_Design_Methodology.md` (composing the `Component`/`VNode` surface).
- `code-quality` — `code-quality/Framework_Clean_Code_Methodology.md` (an ergonomic, example-driven API).
- `core` — `core/BestPractices_Coding_Standards_Methodology.md`; `operations/BestPractices_Documentation_Methodology.md` for the README.

## Inherited Constraints
Compose with `ferric` + the real router; lean deps; edition 2021/stable; rustdoc required; the
`preventDefault`-unavailable constraint is binding and must be handled + documented, not worked around by
editing `ferric`.

## Out-of-Scope Methodologies
Do NOT load `decomposition`/`synthesis`. Do NOT edit `ferric` to add event-arg support (out of scope for
this work-item; note it as a future enhancement if relevant).
