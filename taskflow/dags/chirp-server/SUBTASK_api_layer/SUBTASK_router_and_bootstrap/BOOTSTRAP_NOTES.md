# Router + Bootstrap — Implementation Notes (handoff to `SUBTASK_api_synthesis` → `API_NOTES.md`)

The axum composition root (`build_router`), the server binary (`main.rs`), static/SPA serving, the
`/healthz` probe, and `tracing` are committed to the shared clone on `work/chirp-server`. They
compose against the **real committed** handlers (`crate::api::handlers::*`, commit `8c0336f`) and
transport foundations (`AppState`, `AuthUser`, `impl IntoResponse for ServerError`, commit
`6f32dc0`); nothing is re-declared. This is the pipeline's last implementation spoke.

| What | Value |
|------|-------|
| Clone path | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout` |
| Branch | `work/chirp-server` |
| This commit | `d9c19f0` — `feat(chirp-server): build_router composition root + server bootstrap` |
| Predecessor commit | `8c0336f` — handlers (unchanged) |
| Files added | `src/api/router.rs`, `src/main.rs`, `static/index.html` |
| Files edited (serial) | `src/api/mod.rs` (+`pub mod router; pub use router::build_router;`), `src/lib.rs` (+`pub use api::build_router;`) |

## Exposed symbol (seam for the integration-test spoke)

- **`pub fn chirp_server::build_router(state: AppState) -> axum::Router`** — re-exported at the
  crate root (`pub use api::build_router;` in `lib.rs`). Returns a **state-erased `Router<()>`**
  (state already bound via `.with_state(state)`), so the integration-test spoke mounts it directly:
  `let app = chirp_server::build_router(AppState::new(Arc::new(InMemoryRepository::new())));` and
  drives it with `tower::ServiceExt::oneshot` (both `tower` `util` and `http-body-util` are already
  in `[dev-dependencies]`). No binary needed to test the app.

## Router shape (what `build_router` mounts, in order)

Built as a `Router<AppState>` and bound with `.with_state(state)` last. All nine API routes are from
the authoritative `HANDLERS_NOTES.md` route-metadata table, mounted verbatim (axum 0.8 `{param}`
path syntax):

| Order | Method & path | Handler | Auth |
|------:|---------------|---------|------|
| 1 | `GET /healthz` | `healthz` (local) | no |
| 2 | `POST /api/users` | `handlers::create_user` | no |
| 3 | `GET /api/users/{id}` | `handlers::get_user` | no |
| 4 | `POST /api/sessions` | `handlers::login` | no |
| 5 | `POST /api/chirps` | `handlers::create_chirp` | yes |
| 6 | `GET /api/timeline` | `handlers::timeline` | yes |
| 7 | `PUT /api/users/{id}/follow` | `handlers::follow` | yes |
| 7 | `DELETE /api/users/{id}/follow` | `handlers::unfollow` | yes |
| 8 | `PUT /api/chirps/{id}/like` | `handlers::like` | yes |
| 8 | `DELETE /api/chirps/{id}/like` | `handlers::unlike` | yes |

`follow`/`unfollow` share one `.route()` (a `put(...).delete(...)` `MethodRouter`), as do
`like`/`unlike` — so all nine endpoint-surface ops are routed and reachable (contract identity
`wiring`). Every method/path is the handlers spoke's design; this spoke mounted them unchanged.

### Middleware / layers

- **`.fallback_service(ServeDir + SPA fallback)`** — see below.
- **`.layer(tower_http::trace::TraceLayer::new_for_http())`** — wraps the whole stack, so every
  request/response is traced (spans emitted only when a subscriber is installed; the binary installs
  one, tests may omit it harmlessly).

## Static serving + SPA fallback

- `fallback_service` = `ServeDir::new(static_dir).fallback(ServeFile::new(static_dir/index.html))`
  (`tower-http` `fs` feature). Explicit routes win; only unmatched paths reach the fallback. A path
  that maps to a real static file is served; anything else returns `index.html` with 200 — standard
  SPA client-side-routing behavior.
- **Placeholder static dir** — the real SPA bundle is work-item **#9** and is **not** built here.
  Default static root: the crate-local **`crates/chirp-server/static/`**, resolved at compile time
  from `CARGO_MANIFEST_DIR` (so it is found regardless of the process working directory). It holds a
  committed placeholder `index.html`. Override with the **`CHIRP_STATIC_DIR`** env var to serve a
  real bundle later.
- Because the API is namespaced under `/api/…`, it never collides with the static/SPA path space.
  (Note: an unknown `/api/…` path also falls through to the SPA `index.html` rather than a bare 404;
  genuine API 404s come from the handlers, e.g. an unknown user id.)

## `/healthz` response

- Unauthenticated, state-free. **200 OK**, JSON body:
  `{"status":"ok","service":"chirp-server","version":"<CARGO_PKG_VERSION>"}` (e.g. `"0.1.0"`).

## `tracing` initialization

- Global subscriber installed **only in the binary** (`main::init_tracing`), via
  `tracing_subscriber::fmt().with_env_filter(EnvFilter)`. Filter = `RUST_LOG` when set, else default
  `info,chirp_server=debug,tower_http=info`. Library/tests never install a global subscriber.
- The per-request trace **layer** lives in `build_router` (so the app — not just the binary — is
  traced).

## How to run the server

```text
cargo run -p chirp-server          # boots on 127.0.0.1:3000 with the in-memory repo (no DB)
```

Environment knobs (all optional):

- `CHIRP_BIND_ADDR` — `host:port` to bind (default `127.0.0.1:3000`).
- `CHIRP_STATIC_DIR` — static-asset root for the SPA fallback (default: crate-local `static/`).
- `RUST_LOG` — tracing env-filter (default `info,chirp_server=debug,tower_http=info`).

`main.rs`: init tracing → `AppState::new(Arc::new(InMemoryRepository::new()))` →
`build_router(state)` → `TcpListener::bind` → `axum::serve(listener, app).with_graceful_shutdown(…)`.
Graceful shutdown is wired to **Ctrl-C** (`tokio::signal::ctrl_c()`, the provisioned `signal`
feature) — the server stops accepting and drains in-flight requests. No `tokio-util` needed.

## Design decisions (this spoke's calls — recorded for the gate)

- **`build_router` returns `Router<()>`** (state bound internally), giving the binary and the
  integration tests one identical construction path over the in-memory repo.
- **Static root resolved from `CARGO_MANIFEST_DIR`** (not CWD-relative), with a `CHIRP_STATIC_DIR`
  override — robust to how the server is launched; works before the SPA exists.
- **Graceful shutdown via `tokio::signal::ctrl_c()`** rather than a `CancellationToken`/`TaskTracker`
  pattern: `tokio-util` is not a provisioned dependency and `Cargo.toml` is owned by the scaffold
  spoke (not edited here); the `signal` feature already present is sufficient.
- **`Cargo.toml` untouched** — every needed dependency/feature (`axum 0.8`, `tower-http 0.6`
  `{fs,trace}`, `tracing`, `tracing-subscriber` `{env-filter}`, `tokio` `{rt-multi-thread,macros,net,signal}`)
  was already provisioned by the scaffold spoke.

## Verification status (this invocation, authoritative local gate)

| Check | Command | Result |
|-------|---------|--------|
| fmt    | `cargo fmt -p chirp-server --check`                          | ✅ clean |
| build  | `cargo build -p chirp-server`                                | ✅ clean |
| clippy | `cargo clippy -p chirp-server --all-targets -- -D warnings`  | ✅ no warnings |
| test   | `cargo test -p chirp-server`                                 | ✅ 23 passed, 0 failed (18 repo + 5 handler), auth doc-example `ignore`d |
| boot   | `cargo run -p chirp-server` (CHIRP_BIND_ADDR ephemeral)      | ✅ boots with no DB; `/healthz`→200, `POST /api/users`→201, `GET /api/timeline` no-auth→401, `/` and `/some/client/route`→200 (SPA fallback); Ctrl-C graceful shutdown clean |

## Scope boundaries honored

- Did **not** touch handler business logic, error mapping, `AppState`, or the auth extractor
  (mounted/booted what predecessors committed).
- Did **not** author the end-to-end `tests/` integration suite or the crate `README.md` — those are
  the parent's next sibling `SUBTASK_integration_tests_and_docs`. (In-process HTTP routing tests of
  `build_router` are deliberately left to that spoke to avoid duplicating its charter.)
- Did **not** build the real SPA (#9) — wired to a placeholder static dir and documented above.

## Left for downstream

- **`SUBTASK_api_synthesis`** (verification gate): fold these notes into `API_NOTES.md` and run the
  four-check + authoritative build/clippy/fmt (and full `cargo test`) over the combined api-layer.
- **`SUBTASK_integration_tests_and_docs`** (parent sibling): end-to-end HTTP tests driving
  `chirp_server::build_router`, and the crate `README.md`.
