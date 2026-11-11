# _BRIEF.md — ferric-ssr-r3 (swe-coder) — CI fix: fmt, clippy, doc failures on PR #228

**Repo**: Nousix-LLC/nswe-demo
**Branch**: `work/ferric-ssr-r1` (same branch as PR #228; no force-push)
**Goal**: Fix the 3 CI failures blocking PR #228 (`work/ferric-ssr-r1` → `main`) so the PR passes all CI checks while keeping all previously-passing checks passing.

## Background

PR #228 (`work/ferric-ssr-r1` → `main`) implements SSR/hydration support for the ferric framework (issues #223, #224, #226). The functional implementation is correct (all 7 internal identity assertions pass per the ferric-ssr-r2 `SYNTHESIS.md` fold). Three CI checks are currently failing:

1. **fmt** — `cargo fmt --all --check` fails: `crates/ferric/src/lib.rs` line 25 is missing a blank line between `pub mod ssr;` and the `#[cfg(target_arch = "wasm32")] pub mod hydrate;` block.
2. **clippy** — `cargo clippy --workspace --all-targets --locked -- -D warnings` fails with 3 `clippy::useless_conversion` errors in `crates/ferric/src/ssr.rs`: lines 178, 202, and 209 each have `.into()` on a `VNode`-returning `text(...)` call that does not need it.
3. **doc** — `cargo doc --workspace --no-deps --locked` fails (with `RUSTDOCFLAGS=-D warnings`): line ~16 of `crates/ferric/src/ssr.rs` has a module-level doc comment referencing the private item `crate::signal::ReactiveScope` as a backtick-linked intra-doc link, which triggers `rustdoc::private_intra_doc_links`.

## Objective and acceptance criteria

Produce one commit on `work/ferric-ssr-r1` that fixes all three CI failures with minimal, targeted edits. After the fix:

- `cargo fmt --all --check` exits 0 (no formatting errors)
- `cargo clippy --workspace --all-targets --locked -- -D warnings` exits 0 (no warnings or errors)
- `cargo doc --workspace --no-deps --locked` with `RUSTDOCFLAGS=-D warnings` exits 0 (no doc warnings)
- `cargo test -p ferric` passes (regression guard: all previously-passing tests still pass)
- `cargo check --target wasm32-unknown-unknown -p ferric` passes (WASM target unbroken)
- `cargo build -p chirp-server` passes (server build unbroken)

The PR closes issues #223, #224, #226 (unchanged from ferric-ssr-r2 — the functional implementation is not modified).

## Issues covered (unchanged acceptance criteria from ferric-ssr-r2)

- **#223** — SSR rendering: ferric can render component trees to HTML strings on the server
- **#224** — Hydration: rendered HTML is hydrated without full re-render on the client
- **#226** — SSR integration: chirp-server can render components and serve them

## Inputs

- Branch `work/ferric-ssr-r1` in `Nousix-LLC/nswe-demo`, which is the branch tracked by PR #228
- ferric-ssr-r2 `SYNTHESIS.md` (all 7 identity assertions passing; functional implementation is complete and correct)
- The 3 failing CI checks described above

## Declared output

1. One commit on `work/ferric-ssr-r1` pushed to origin that fixes the 3 CI failures. The commit must not reference host paths or taskflow internals in its message.
2. No new PR — this pushes to the existing branch tracked by PR #228.
3. A root `SYNTHESIS.md` accounting for all three fixes, confirming each CI check's outcome, and reporting the regression guard results.

## What to fix and verify — distinct concerns

### Concern 1: fmt — missing blank line in lib.rs

In `crates/ferric/src/lib.rs`, add a blank line between `pub mod ssr;` and the `#[cfg(target_arch = "wasm32")] pub mod hydrate;` line (or block). The exact change is one blank line insertion to separate these two items.

Verify: run `cargo fmt --all --check` and confirm exit 0.

### Concern 2: clippy — useless `.into()` on VNode returns in ssr.rs

In `crates/ferric/src/ssr.rs`, remove the `.into()` suffix from the three test-only VNode returns identified by clippy:
- line ~178: `text("<>&\"'").into()` → `text("<>&\"'")`
- line ~202: `text("world").into()` → `text("world")`
- line ~209: `text("").into()` → `text("")`

These are inside `#[cfg(test)]` test functions; no functional code is changed.

Verify: run `cargo clippy --workspace --all-targets --locked -- -D warnings` and confirm exit 0.

### Concern 3: doc — private intra-doc link in ssr.rs module doc

In `crates/ferric/src/ssr.rs`, find the module-level doc comment (at the top of the file, before `use` statements) that contains a backtick-linked reference to `crate::signal::ReactiveScope` (a private item). Replace that linked reference with plain text that does not form an intra-doc link. For example, replace `` [`crate::signal::ReactiveScope`] `` with `a per-request reactive scope` (or equivalent plain text that preserves the sentence's meaning).

Verify: run `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --locked` and confirm exit 0.

### Concern 4: Regression guard

After all three fixes are applied and committed, verify:
- `cargo test -p ferric` passes
- `cargo check --target wasm32-unknown-unknown -p ferric` passes
- `cargo build -p chirp-server` passes

## Constraints

- Branch: `work/ferric-ssr-r1` only — do not touch `main` or any other branch.
- Do not modify the functional implementation in `crates/ferric/src/ssr.rs` (only the test helper lines and the module doc comment are touched — the SSR rendering logic is not changed).
- Do not modify `crates/ferric/src/hydrate.rs`, or any frozen prelude file (`signal.rs`, `dom.rs`, `router.rs`, or the signal/dom/router/vdom declarations in `lib.rs`) beyond the single blank-line insertion.
- No force-push.
- Commit message must not reference host paths or taskflow internals.
