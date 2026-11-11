# COMPLETE — ferric-ssr-r1-skeleton

## Status

Completed. Branch `work/ferric-ssr-r1` created from `main` at `945fade` and
pushed to `origin/work/ferric-ssr-r1`. Commit `156d9e9`.

## Outputs Delivered

| File | Action | Notes |
|---|---|---|
| `crates/ferric/src/ssr.rs` | Created | Exports `render_to_string<F: FnOnce()->VNode>->String` as `todo!()`; defines `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` seam constants. No `web_sys`/`wasm_bindgen` imports. |
| `crates/ferric/src/hydrate.rs` | Created | Exports `#[cfg(target_arch="wasm32")] hydrate<F: Fn()->VNode+'static>` as `todo!()`. Only compiled on wasm32 target. |
| `crates/ferric/src/lib.rs` | Modified | Added `pub mod ssr`, `#[cfg(target_arch="wasm32")] pub mod hydrate`, and their top-level re-exports. Frozen prelude block and all existing exports unchanged. |
| `crates/ferric/Cargo.toml` | Unchanged | No change needed: `cargo check --lib -p ferric` already passed on native before changes (web-sys/wasm-bindgen compile fine on native targets), and `hydrate.rs` is gated at the module declaration so it is never compiled on native. |

## Verification Results

- `cargo check --lib -p ferric` (native): ✓ exit 0
- `cargo check --target wasm32-unknown-unknown -p ferric`: ✓ exit 0
- `cargo test -p ferric` (native): ✓ exit 0 — 43 unit tests + 7 doc tests, 0 failures
- Frozen files (`dom.rs`, `signal.rs`, `vdom.rs`, `component.rs`): zero diff confirmed

## Branch State

Branch `work/ferric-ssr-r1` is at `156d9e9` on `origin`. The parallel spokes
(`ferric-ssr-r1-server-render`, `ferric-ssr-r1-client-hydrate`,
`ferric-ssr-r1-axum-integration`) can now branch from `work/ferric-ssr-r1`
and proceed concurrently — `lib.rs` and `Cargo.toml` are finalized and owned
by no spoke.

## Design Decisions

- **TEXT_OPEN_MARKER / TEXT_CLOSE_MARKER** defined in `ssr.rs` (the natural
  owner of server seam constants). `hydrate.rs` will import from `crate::ssr`
  as the _GLOBAL.md specifies.
- **Cargo.toml not changed**: the native check already passed without gating
  `wasm-bindgen`/`web-sys` to wasm32. The brief's "if needed" qualifier applies
  correctly here — no change is needed.
- **Not added to frozen prelude**: per `design/ferric/ssr-hydration.md` §REQ-SSR-012,
  `render_to_string` and `hydrate` are additive new items alongside `mount`, not
  additions to the frozen prelude surface.
