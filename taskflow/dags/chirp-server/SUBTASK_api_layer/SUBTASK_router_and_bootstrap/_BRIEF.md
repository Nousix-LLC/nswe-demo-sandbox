# Task: Router composition + server bootstrap

## Task Specification

**Slug**: SUBTASK_router_and_bootstrap
**Task Kind**: standard
**Status**: Pending

### Objective

Assemble the application into a runnable server: a `build_router` that mounts every handler plus
`GET /healthz`, static-file serving, and the SPA fallback; `tracing` structured logging; and the
`main.rs` entrypoint — exposing `build_router` from `lib.rs` for integration testing.

### Context

This task is part of the chirp-server API-layer subtree (see `../_GLOBAL.md`) — the composition root
and server entrypoint, the pipeline's last implementation spoke. The predecessor spokes have committed
the foundations (`AppState`, auth extractor, error `IntoResponse`) and all handler functions into the
shared clone; read `../SUBTASK_handlers/HANDLERS_NOTES.md` for the route-metadata table (method + path
+ handler fn) and `../SUBTASK_transport_foundations/FOUNDATIONS_NOTES.md` for `AppState`. Compose
against the real committed code.

**Dependencies**: `SUBTASK_handlers`.
**Dependents**: `SUBTASK_api_synthesis` (verifies the assembled layer); downstream, the parent's
`../../SUBTASK_integration_tests_and_docs` mounts your `build_router`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, success criteria |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your ownership, the `build_router` symbol you expose, `/healthz` ownership |
| Handlers handoff | `../SUBTASK_handlers/HANDLERS_NOTES.md` | The route-metadata table (what to mount: method + path + handler fn) |
| Foundations handoff | `../SUBTASK_transport_foundations/FOUNDATIONS_NOTES.md` | `AppState` to thread into the router + `main` |
| Committed code | the shared clone at the contract's `clone_path` | The real handlers + foundations to mount/boot |
| Module-layout note | `../../contracts/_MANIFEST.yaml` (`module_layout`) | `main.rs` role; `static/` placeholder expectation |

---

## Process / Approach

- **`build_router(state: AppState) -> axum::Router`** in the `api` module, re-exported from `lib.rs`
  (`pub use api::build_router;`): mount every handler from the route-metadata table, add a
  `GET /healthz` handler returning a health response, add a static-file service (`tower-http`
  `ServeDir`) with an SPA fallback route serving from a **placeholder static dir** (create/point to
  it; document that #9 lands the real SPA later). Attach the request-trace layer (`tower-http` trace).
- **`tracing` init** — `tracing-subscriber` with env-filter; a request-trace middleware layer.
- **`main.rs`** — init tracing, build `AppState` (in-memory repo default), build the router, bind,
  and serve (graceful shutdown optional). Exposing `build_router` from `lib.rs` is what lets the
  integration-test spoke mount the app without the binary.

Build locally (`cargo build -p chirp-server`, `clippy --all-targets -- -D warnings`, `fmt --check`)
and commit to `work/chirp-server`. Router module structure, the health-response shape, the static dir
location, and shutdown handling are your calls — document them.

### Methodology

Apply the suggested methodology below; you are the final judge of what you load.

---

## Output Specification

### Primary Output (handoff)

| Attribute | Value |
|-----------|-------|
| Filename | `BOOTSTRAP_NOTES.md` |
| Location | this workspace (`SUBTASK_router_and_bootstrap/`) |

Record: the router shape (what `build_router` mounts, in what order; middleware layers), how static
serving + SPA fallback are wired (and the placeholder dir path), the `/healthz` response, how `tracing`
is initialized, and how to run the server (`cargo run -p chirp-server`, bind address/env). The
synthesis spoke folds this into `API_NOTES.md`.

### Code output

`build_router` (exposed from `lib.rs`), `/healthz`, static + SPA serving, tracing init + layer, and
`main.rs`, committed to `work/chirp-server`.

---

## Success Criteria

- [ ] `build_router(state)` mounts every handler in the route-metadata table + `GET /healthz` + static `ServeDir` + SPA fallback (placeholder dir), and is re-exported from `lib.rs`.
- [ ] `tracing` initialized with a request-trace layer; `main.rs` inits tracing, builds state + router, binds, and serves.
- [ ] `cargo build -p chirp-server` + `clippy --all-targets -- -D warnings` + `fmt --check` clean; `cargo run -p chirp-server` boots with no DB.
- [ ] Committed to `work/chirp-server`; `BOOTSTRAP_NOTES.md` written (router shape, serving/fallback, run instructions).

---

## Suggested Methodology Files

Matched Domain-Mapping rows: **Writing Rust code → primary `rust`; supporting `core`** and
**Architecture styles (layering; how static serving + SPA fallback compose) → `architecture`.**
Load via `engine_load_methodology { name: "<bundle_id>" }`.

- `rust` — `rust/Rust_Async_Tokio_Methodology.md` (tokio runtime, `serve`, graceful shutdown).
- `architecture` — `architecture/Architecture_Styles_Methodology.md` (transport→service→repository layering; composing static serving + API + SPA fallback in one router).
- `core` — `core/BestPractices_Coding_Standards_Methodology.md`, `core/CodeManagement_Commit_Practices_Methodology.md`.
- Optional: `operations` — `operations/Observability_Logging_Methodology.md` (structured `tracing` setup) if you want logging-level guidance.

These are the parent's flagged methodologies; load them as a starting point and exercise your own judgment.

## Inherited Constraints

- Compose against the REAL committed handlers + `AppState`; re-export, do not re-implement. Re-declare no DTO/trait/error.
- In-memory repo is the default; the server boots with no DB. SPA assets (#9) are not built — wire to a placeholder static dir and document it.
- Edition 2021 / rust 1.82 / stable; `clippy --all-targets -- -D warnings` clean. ONE shared clone; branch `work/chirp-server`; never touch `main`; no commit-attribution trailers. Do NOT edit `Cargo.toml`.

## Out-of-Scope Methodologies

- Do NOT add or change handler business logic (that is `SUBTASK_handlers`) or the error mapping / `AppState` / extractor (that is `SUBTASK_transport_foundations`); mount and boot what is committed.
- Do NOT author the integration tests or the `README.md` — those are the parent's next sibling.
