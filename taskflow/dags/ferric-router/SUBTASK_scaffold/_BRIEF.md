# Task: ferric-router scaffold (walking skeleton)

## Task Specification
**Slug**: SUBTASK_scaffold
**Task Kind**: standard
**Status**: Pending

### Objective
Stand up the shared clone and the `crates/ferric-router` member crate as a compiling **walking
skeleton**, so `cargo build --workspace` is green end-to-end before any routing logic exists.

### Context
Part of the `ferric-router` work-item (see `../_GLOBAL.md` and `../contracts/`). First task in a serial
pipeline; every later spoke fills in the body of exactly ONE module you stub here. You own the shared
files the layers would otherwise fight over.

**Dependencies**: none. **Dependents**: `SUBTASK_matcher`, `SUBTASK_navigation`, `SUBTASK_view`, `SUBTASK_synthesis`.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Hub | `../_GLOBAL.md` | project context, constraints, shared-clone location |
| Frozen contract | `../contracts/ferric_router_api.rs`, `../contracts/_MANIFEST.yaml` | the exact module layout, public items, prelude, and your owned paths |
| Landed `ferric` | the cloned repo's `crates/ferric` (src + README + Cargo.toml) | the surface you compose with; the workspace manifest conventions to mirror |

## What to do (approach — not a line-by-line script)
1. Clone `Nousix-LLC/nswe-demo` into **`<subtree_root>/checkout/`** where
   `<subtree_root>` = `/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-router/`
   (use `gh repo clone Nousix-LLC/nswe-demo <subtree_root>/checkout`). Do NOT reuse any other
   process's clone. Create and check out branch **`work/ferric-router`** off `main`.
2. Add the new workspace member crate `crates/ferric-router`:
   - `Cargo.toml`: package `ferric-router`, edition/rust-version/repository from `workspace`,
     `[lints] workspace = true`; dependencies — `ferric = { path = "../ferric" }`, plus
     `wasm-bindgen`, `js-sys`, `web-sys` (`.workspace = true`; enable the `web-sys` features the
     router needs — `Window`, `History`, `Location`, `PopStateEvent`, `Event`, `EventTarget`; the
     navigation spoke may extend this list additively), and dev-dep `wasm-bindgen-test`.
   - `src/lib.rs`: crate docs, `pub mod matcher; pub mod router; pub mod link;` and the **frozen
     `prelude`** exactly as `../contracts/ferric_router_api.rs` declares it.
   - `src/matcher.rs`, `src/router.rs`, `src/link.rs`: compiling **stubs** that declare every frozen
     public item with `todo!()` / placeholder bodies, matching the contract signatures so the crate
     compiles. (Each later spoke replaces its module body.)
   - `examples/app.rs`: a minimal stub that compiles (and builds to wasm); the view spoke fleshes it out.
3. Confirm the member is picked up by the workspace (`members = ["crates/*"]` — no root edit expected;
   note it if one is needed) and that **`cargo build --workspace`** and **`cargo build -p ferric-router
   --target wasm32-unknown-unknown`** both succeed on the skeleton. Add the `wasm32-unknown-unknown`
   target if needed (`rustup target add wasm32-unknown-unknown`).
4. Commit on `work/ferric-router` (e.g. "scaffold: ferric-router walking skeleton"). No attribution trailers.

## Outputs (you own these)
- `checkout/` clone on branch `work/ferric-router`
- `checkout/crates/ferric-router/Cargo.toml`
- `checkout/crates/ferric-router/src/lib.rs` (module decls + frozen prelude)
- `checkout/crates/ferric-router/src/{matcher,router,link}.rs` (stubs)
- `checkout/crates/ferric-router/examples/app.rs` (stub)
- a commit containing the above
- `COMPLETE.md` recording what was built + the build result

## Success Criteria
- [ ] Clone exists at `<subtree_root>/checkout/`, branch `work/ferric-router` checked out off `main`.
- [ ] `crates/ferric-router` is a workspace member; `src/lib.rs` prelude matches the frozen contract verbatim.
- [ ] `cargo build --workspace` and `cargo build -p ferric-router --target wasm32-unknown-unknown` both exit 0.
- [ ] Owned files committed; `main` untouched.

## Constraints
- Treat `../contracts/` as READ-ONLY; MATCH its signatures, do not copy the contract file into src.
- Stub bodies only — do NOT implement matcher/router/link logic (those are owned by other spokes).
- Lean deps; edition 2021 / stable; NEVER touch `main`; no commit-attribution trailers.

## Suggested Methodology Files (parent's flags — you are the final judge)
Task type (Domain Mapping): **Writing new code** → primary **Core**, supporting **Code Quality**.
Load on-demand via `engine_load_methodology`:
- `core` — `core/BestPractices_Coding_Standards_Methodology.md` (manifest/module conventions),
  `core/CodeManagement_Commit_Practices_Methodology.md` (the commit you make).
- `rust` — `rust/Rust_Cargo_Ecosystem_Methodology.md` (workspace member crate, features, path deps).
These are the parent's flags based on the task type; load fewer if clearly inapplicable, more if your
reading of the brief reveals additional surface.

## Inherited Constraints
Crate name/path fixed (`crates/ferric-router`); path-dep on `crates/ferric`; shared clone at
`<subtree_root>/checkout/`; compose with `ferric` (do not re-implement); workspace lints enforce
`missing_docs` — give public stub items rustdoc. ferric click handlers are `Fn()` (no preventDefault) —
relevant to the view spoke, not scaffold.

## Out-of-Scope Methodologies
Do NOT load `testing`/`tdd-patterns`/`decomposition`/`synthesis` — you write stubs, not tests, logic, or gates.
