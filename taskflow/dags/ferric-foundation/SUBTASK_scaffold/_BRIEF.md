# Task: Scaffold the workspace + `ferric` crate skeleton (walking skeleton)

**Slug**: SUBTASK_scaffold
**Task Kind**: standard
**Status**: Pending

## Objective
Stand up the shared working tree and a **compiling** skeleton of the `ferric` crate — the
composition root every later layer fills in — so that `cargo build` (native) and
`cargo build -p ferric --target wasm32-unknown-unknown` are both green before any framework logic
exists.

## Context
Part of the `ferric-foundation` subtree (see `../_GLOBAL.md`). You are the **walking skeleton**:
you own the shared files the layer spokes would otherwise fight over. Downstream spokes
(`reactive_core`, `view_and_diff`, `dom_runtime`) depend on your output and each replaces the
`todo!()` body of exactly one module you stub here.

**Dependencies**: none. **Dependents**: all other subtasks.

## Inputs
- `../_GLOBAL.md` — subtree context, chosen cut, constraints.
- `../contracts/ferric_api.rs` (read-only) — the frozen public API your `lib.rs` + stubs must
  expose. **Match these signatures; do not redefine them.**
- `../contracts/_MANIFEST.yaml` (read-only) — your owned paths.

## Scope (what this task establishes)
- A git clone of `Nousix-LLC/nswe-demo` at `../checkout/` (i.e. the subtree root's `checkout/`),
  on a new branch `work/ferric-foundation` cut from `main`. Use `gh repo clone` / `git`.
- The **virtual workspace** root `Cargo.toml` (no root package; `members = ["crates/*"]`),
  with sensible shared `[workspace.lints]` / `[profile.*]` and the workspace laid out so the
  future crates named in the inherited constraints slot in cleanly.
- `crates/ferric/Cargo.toml` — edition 2021+, lean deps (`wasm-bindgen`, `web-sys` with the
  features the DOM layer will need, `js-sys`), an `examples/` and test setup compatible with
  `wasm-bindgen-test`, and the crate typed so it builds for `wasm32-unknown-unknown`.
- `crates/ferric/src/lib.rs` — module declarations (`signal`, `vdom`, `component`, `dom`) and a
  `pub mod prelude` re-exporting the frozen surface named in `ferric_api.rs`.
- Compiling **stub** module files (`signal.rs`, `vdom.rs`, `component.rs`, `dom.rs`) carrying the
  frozen public signatures with `todo!()`/placeholder bodies — just enough that the crate compiles
  for BOTH the host target and `wasm32-unknown-unknown` (ensure `rustup target add
  wasm32-unknown-unknown`).
- A commit on `work/ferric-foundation` capturing the skeleton. (Do not push; the synthesis child
  pushes and opens the PR.)

Prove the skeleton: both `cargo build` and the wasm `cargo build -p ferric --target
wasm32-unknown-unknown` succeed. If the frozen contract cannot be expressed as a compiling stub,
that is a contract-inadequacy signal — request an additive plan amendment rather than deviating.

## Outputs
- The prepared `../checkout/` clone + branch, the two `Cargo.toml`s, `src/lib.rs`, and the four
  compiling stub modules (per `_MANIFEST.yaml` ownership).
- `COMPLETE.md` recording what was scaffolded and the two build results.

## Success criteria
- [ ] `../checkout/` is a clone of the repo on branch `work/ferric-foundation` (not `main`).
- [ ] Virtual workspace + `crates/ferric` skeleton present; `cargo build` green.
- [ ] `cargo build -p ferric --target wasm32-unknown-unknown` green.
- [ ] `src/lib.rs` prelude re-exports the frozen surface; stub signatures match `ferric_api.rs`.
- [ ] Skeleton committed on the work branch; `main` untouched.

## Suggested Methodology Files
Matched Domain-Mapping row (verbatim): **Writing new code → Primary: Core; Supporting: Code Quality**;
and **Writing Rust code → Primary: Rust; Supporting: Core, Code Quality**. Load on-demand via
`engine_load_methodology`:
- `rust/Rust_Cargo_Ecosystem_Methodology.md` — Cargo **workspace** layout, member crates, feature
  flags, and the wasm target setup are the heart of this task.
- `core/BestPractices_Coding_Standards_Methodology.md` — baseline standards for the public skeleton.
- `core/CodeManagement_Commit_Practices_Methodology.md` — the scaffold commit on the work branch.
- `code-quality/Framework_SOLID_Principles_Methodology.md` — the module boundaries you fix here are
  a long-lived public surface; keep them cohesive.
These are the parent's flagged starting points based on the task type; you are the final judge of
what you load — load fewer if clearly inapplicable, more if your reading reveals additional surface.

## Inherited Constraints
- Crate is **`ferric`** at `crates/ferric`; lay the workspace out so `crates/ferric-router`,
  `crates/ferric-http`, `crates/chirp-types`, `crates/chirp-server`, `crates/chirp-frontend` slot
  in later.
- Edition **2021+**, **stable** toolchain; deps lean (`wasm-bindgen`, `web-sys`, `js-sys`).
- Work only in `../checkout/`; branch `work/ferric-foundation`; **never** commit to / force-push
  `main`; no commit-attribution trailers.
- Expose the frozen `contracts/ferric_api.rs` surface exactly; it is read-only and additive-only.

## Out-of-Scope Methodologies
- Do **not** implement reactive logic, the vdom/diff, or DOM rendering — those are downstream
  spokes. Your stubs are `todo!()` only. (`testing` beyond "it compiles" is not your concern;
  the leak/diff/runtime tests belong to the respective spokes.)
