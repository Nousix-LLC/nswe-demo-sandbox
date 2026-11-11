# _BRIEF.md — ferric-ssr-r1-skeleton

## Objective

Establish the new module structure for the SSR + hydration work in `crates/ferric` on branch
`work/ferric-ssr-r1`. This task takes sole ownership of `crates/ferric/src/lib.rs` and
`crates/ferric/Cargo.toml`, adds the module declarations for `ssr` and `hydrate` with correct
compile-target gating, creates stub files at `src/ssr.rs` and `src/hydrate.rs` that satisfy
the contract signatures, and leaves the branch in a clean build state on both native and
wasm32-unknown-unknown targets.

The parallel spokes (server-render, client-hydrate, axum-integration) depend on this task
completing first. After it commits, they can proceed concurrently with no further changes to
`lib.rs` or `Cargo.toml`.

## Inputs

- **Repository**: `Nousix-LLC/nswe-demo`, branch `work/ferric-ssr-r1` (create from
  `main` at `945fade38abd6b053268501f3801734756f02502` if the branch does not exist).
- **Owned files to modify**:
  - `crates/ferric/src/lib.rs`
  - `crates/ferric/Cargo.toml`
- **Owned files to create** (stubs):
  - `crates/ferric/src/ssr.rs`
  - `crates/ferric/src/hydrate.rs`
- **Contract** (read-only): `contracts/ferric_ssr_contract.rs` — the function signatures and
  marker constants the stubs must declare.
- **Existing module files** (read-only, for context):
  - `crates/ferric/src/vdom.rs`
  - `crates/ferric/src/signal.rs`

## Declared Output

Commits on branch `work/ferric-ssr-r1` that:

1. Add `src/ssr.rs` — a stub file exported as `pub mod ssr` from `lib.rs`. The stub must
   export `render_to_string` with exactly the signature declared in the contract, implemented
   as `todo!()`. The file must NOT import `web_sys` or `wasm_bindgen`.

2. Add `src/hydrate.rs` — a stub file exported as `pub mod hydrate` (gated to
   `target_arch = "wasm32"`) from `lib.rs`. The stub must export `hydrate` with exactly the
   signature declared in the contract, implemented as `todo!()`.

3. `lib.rs` updated with the two new module declarations. The frozen prelude block and all
   existing exports are unchanged. `render_to_string` and `hydrate` are re-exported from their
   respective modules (but not added to the frozen `prelude` block unless that is required by
   the design spec — check `design/ferric/ssr-hydration.md`).

4. `Cargo.toml` updated if needed to allow the crate to compile on a native (non-wasm) host
   target — specifically, `web_sys` and `wasm_bindgen` dependencies must be gated to
   `cfg(target_arch = "wasm32")` or `[target.'cfg(target_arch = "wasm32")'.dependencies]`
   so `cargo check --lib -p ferric` succeeds on native.

## Success Criteria

- `cargo check --lib -p ferric` exits zero on the native (non-wasm) host target.
- `cargo check --target wasm32-unknown-unknown -p ferric` exits zero.
- `cargo test -p ferric` (native) exits zero (no regressions in existing tests).
- `src/ssr.rs` and `src/hydrate.rs` exist and are reachable via the module tree.
- The frozen files (`src/dom.rs`, `src/signal.rs`, `src/vdom.rs`, `src/component.rs`) are
  unmodified: `git diff HEAD -- crates/ferric/src/dom.rs [...]` produces no output.
- The existing frozen prelude surface (including `mount`) compiles and exports unchanged.

## Constraints

- **Owns**: `crates/ferric/src/lib.rs`, `crates/ferric/Cargo.toml`, the new stub files
  `src/ssr.rs` and `src/hydrate.rs`. Do not modify any other file.
- **Frozen files** (must not be touched): `src/dom.rs`, `src/signal.rs`, `src/vdom.rs`,
  `src/component.rs`.
- **Stubs only** — do not implement any SSR or hydration logic. The stubs exist only to let
  the branch compile; the spokes fill in the implementations.
- Do not create or modify anything in `crates/chirp-server`.
- BAR-005 (#225) is out of scope; do not introduce any state-serialization surface.
- Branch: `work/ferric-ssr-r1`. Do not force-push to `main`.
- Commit attribution: end commit messages with `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`.
