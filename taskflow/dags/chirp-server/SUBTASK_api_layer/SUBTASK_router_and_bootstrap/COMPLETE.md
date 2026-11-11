# COMPLETE — SUBTASK_router_and_bootstrap

**Task**: Router composition + server bootstrap (the api-layer subtree's last implementation spoke).
**Evaluation**: Atomic (one responsibility — assemble the app into a runnable server; all triggers
cleared, both concern tests passed).
**Status**: COMPLETED.

## What was done

Authored the axum composition root and server bootstrap, composing against the **real committed**
handlers (`8c0336f`) and transport foundations (`6f32dc0`) — nothing re-declared — and committed to
the shared clone on `work/chirp-server` as **`d9c19f0`**:

- `src/api/router.rs` — `build_router(state) -> Router`: mounts all nine `/api/…` handlers +
  `GET /healthz` + a static `ServeDir` with SPA `index.html` fallback, wrapped in a `tower-http`
  `TraceLayer`; returns a state-bound `Router<()>`. Plus the local `healthz` handler and the
  `CHIRP_STATIC_DIR`-overridable static-root resolver.
- `src/main.rs` — binary entrypoint: `tracing` init (env-filter), in-memory `AppState`, build
  router, bind `CHIRP_BIND_ADDR` (default `127.0.0.1:3000`), `axum::serve` with Ctrl-C graceful
  shutdown.
- `src/api/mod.rs` / `src/lib.rs` — serial edits adding `pub mod router;` and the
  `pub use api::build_router;` crate-root re-export (the seam the integration-test spoke mounts).
- `static/index.html` — committed placeholder page (real SPA is work-item #9).

`Cargo.toml` was **not** edited (all deps/features were pre-provisioned by the scaffold spoke).
`main` was never touched.

## Declared outputs

- `BOOTSTRAP_NOTES.md` (this workspace) — router shape, static/SPA wiring + placeholder path,
  `/healthz` response, tracing init, run instructions, design decisions, verification status.
- Code committed to `work/chirp-server` (commit `d9c19f0`).

## Success criteria (all met)

- [x] `build_router(state)` mounts every route-metadata handler + `GET /healthz` + static `ServeDir`
      + SPA fallback (placeholder dir), re-exported from `lib.rs`.
- [x] `tracing` initialized with a request-trace layer; `main.rs` inits tracing, builds state +
      router, binds, serves (Ctrl-C graceful shutdown).
- [x] `cargo build` + `cargo clippy --all-targets -- -D warnings` + `cargo fmt --check` clean;
      `cargo run -p chirp-server` boots with no DB (verified: `/healthz`→200, create→201,
      unauth timeline→401, SPA fallback→200).
- [x] Committed to `work/chirp-server`; `BOOTSTRAP_NOTES.md` written.

## Contract identities advanced (for the synthesis gate)

- `wiring` — every `endpoint_surface` op has exactly one routed, reachable handler delegating
  through `ChirpRepository`; no detached dead code (every handler mounted).
- `lib_api` — `pub use api::build_router;` present in `src/lib.rs`.
- `build` / `clippy` / `fmt` — all clean locally (the gate re-runs them authoritatively).
- `contract` — no DTO/trait/error re-declared; all wire types from `chirp-types`, trait/error from
  predecessor modules.
