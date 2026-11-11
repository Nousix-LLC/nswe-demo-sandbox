# chirp-server API layer — handoff notes

The axum transport/service layer of `crates/chirp-server` is committed to the shared clone on branch
`work/chirp-server`. This is the handoff `SUBTASK_integration_tests_and_docs` reads to drive the
end-to-end suite and author the crate `README.md`. Everything below describes the **real committed
code**, verified by the API-layer synthesis gate (see `SYNTHESIS.md` beside this file).

| What | Value |
|------|-------|
| Crate | `crates/chirp-server` (library + binary) |
| Branch | `work/chirp-server` |
| API-layer HEAD at verification | `d9c19f0` (router + bootstrap); foundations `6f32dc0`, handlers `8c0336f`; validation remediation `714d50f` (F1) |
| App entry point | `chirp_server::build_router(AppState) -> axum::Router` (re-exported from `lib.rs`) |
| Default backing store | `InMemoryRepository` — the server boots with **no database** |

## How the app is constructed (one shared path for binary + tests)

```rust
use std::sync::Arc;
use chirp_server::{build_router, AppState, InMemoryRepository};

let app = build_router(AppState::new(Arc::new(InMemoryRepository::new())));
```

`build_router` returns a **state-erased `Router<()>`** (state already bound via `.with_state`), so the
integration-test spoke mounts it directly and drives it with `tower::ServiceExt::oneshot`
(`tower` `util` and `http-body-util` are already in `[dev-dependencies]`). No running binary is needed
to test the app.

## Route table (authoritative — mounted verbatim in `build_router`)

All API routes are namespaced under `/api/…`; `GET /healthz` and the static/SPA fallback own the rest
of the path space. "Auth" = requires a valid `Authorization: Bearer <token>` (resolved by the
`AuthUser` extractor → `UserId`; **401** before the handler body runs). Path params use axum 0.8
`{param}` syntax. All request/response bodies are JSON.

| # | Method & path | Handler | Auth | Request payload | Response body | Success | Key error statuses |
|---|---------------|---------|------|-----------------|---------------|---------|--------------------|
| 1 | `GET /healthz` | `healthz` (local) | no | — | `{status,service,version}` | **200** | — |
| 2 | `POST /api/users` | `handlers::create_user` | no | `CreateUserRequest` (`ValidatedJson`) | `User` | **201** | 409 dup username; 400 invalid body |
| 3 | `GET /api/users/{id}` | `handlers::get_user` | no | `UserId` (`Path`) | `User` | **200** | 404 unknown id |
| 4 | `POST /api/sessions` | `handlers::login` | no | `LoginRequest` (`ValidatedJson`) | `AuthResponse` | **200** | 404 unknown handle; 400 invalid body |
| 5 | `POST /api/chirps` | `handlers::create_chirp` | yes | `CreateChirpRequest` (`ValidatedJson`) | `Chirp` | **201** | 404 absent reply target; 400 invalid body; 401 |
| 6 | `GET /api/timeline` | `handlers::timeline` | yes | `TimelineQuery` (`Query`) | `Page<Chirp>` | **200** | 401 |
| 7 | `PUT /api/users/{id}/follow` | `handlers::follow` | yes | `UserId` (`Path` = followee) | `FollowResponse` | **200** | 403 self-follow; 404 absent; 401 |
| 8 | `DELETE /api/users/{id}/follow` | `handlers::unfollow` | yes | `UserId` (`Path` = followee) | `FollowResponse` | **200** | 404 absent; 401 |
| 9 | `PUT /api/chirps/{id}/like` | `handlers::like` | yes | `ChirpId` (`Path`) | `LikeResponse` | **200** | 404 absent chirp; 401 |
| 10 | `DELETE /api/chirps/{id}/like` | `handlers::unlike` | yes | `ChirpId` (`Path`) | `LikeResponse` | **200** | 404 absent chirp; 401 |

`follow`/`unfollow` share one `.route("/api/users/{id}/follow", put(...).delete(...))`; `like`/`unlike`
share `.route("/api/chirps/{id}/like", put(...).delete(...))`. All nine `repository_seam` operations
plus `/healthz` are routed and reachable; every handler delegates through `ChirpRepository` (no
persistence bypass). The actor on authenticated mutations is always the `AuthUser` id — never taken
from the body — so a caller can only act as itself.

### REST decisions worth knowing for the tests

- `login` is `POST /api/sessions` → **200** (not 201): the session is not an addressable resource; the
  client receives its bearer token in the `AuthResponse` body.
- `follow`/`like` are idempotent `PUT` (repeat = same 200); `unfollow`/`unlike` are idempotent
  `DELETE`. The followee/chirp target is the path id.
- `timeline` is the **home** timeline (viewer self + followees, newest-first). The repository owns the
  `1..=100` limit clamp (default 20) and the opaque last-id cursor; the handler passes `TimelineQuery`
  through and echoes `Page::next_cursor` back.

## `AppState` design

```rust
#[derive(Clone)]
pub struct AppState { pub repo: Arc<dyn ChirpRepository> }
impl AppState { pub fn new(repo: Arc<dyn ChirpRepository>) -> Self }
```

One state type for the whole app; `Clone` is an `Arc` bump. Handlers name it `State(state):
State<AppState>` and call `state.repo.<op>(…).await`. The `AuthUser` extractor is generic over `S`
with `AppState: FromRef<S>` (axum's blanket `FromRef<S> for S` covers `S = AppState`), so no extra
`FromRef` impl is needed. The extractor owns no session state — the token store lives behind the repo
(`repo.resolve_token(&SessionToken(raw)).await -> UserId`).

## Error → HTTP mapping (as implemented in `src/error.rs`)

Handlers return `Result<_, ServerError>`; `impl IntoResponse for ServerError` renders every error as
`chirp_types::api::ApiError { code, message, details }` (camelCase; `details` omitted when empty) with
the status below — matching the parent contract `error_mapping` table exactly.

| `ServerError` variant | `ErrorCode` | HTTP | Notes |
|-----------------------|-------------|------|-------|
| `Validation(ValidationError)` | `VALIDATION_ERROR` | **400** | one `FieldError` lifted from the offending field |
| `InvalidBody(String)` | `VALIDATION_ERROR` | **400** | transport-boundary body-decode/validation rejection (F1 remediation); one generic `body` `FieldError` |
| `Unauthorized(_)` | `UNAUTHORIZED` | **401** | missing/malformed/unresolvable Bearer token |
| `Forbidden(_)` | `FORBIDDEN` | **403** | e.g. self-follow |
| `NotFound(_)` | `NOT_FOUND` | **404** | absent user/chirp/handle |
| `Conflict(_)` | `CONFLICT` | **409** | e.g. duplicate username |
| `Internal(_)` | `INTERNAL` | **500** | message logged via `tracing::error!`; wire body is the generic `"an internal server error occurred"` |

**Validation (F1) — test-relevant.** `chirp-types` value objects (`Username`, `ChirpText`) validate on
deserialization via `#[serde(try_from = "String")]`. Request bodies are extracted with the
`ValidatedJson<T>` extractor (not plain `axum::Json`), so a value-object validation failure, malformed
JSON, or a wrong/missing content type becomes `ServerError::InvalidBody` → `VALIDATION_ERROR`/**400**
as a contract `ApiError`, instead of axum's default plain-text **422**. Integration tests that POST an
invalid handle or over-long chirp body should assert **400** + an `ApiError` body with `code =
VALIDATION_ERROR` and a non-empty `details` entry.

## Static serving + SPA fallback (placeholder)

- `build_router` sets `.fallback_service(ServeDir::new(static_dir).fallback(ServeFile::new(static_dir/index.html)))`
  (`tower-http` `fs`). Explicit routes win; only unmatched paths reach the fallback. A real static file
  is served; anything else returns `index.html` with **200** (SPA client-side routing).
- **Placeholder dir**: the real SPA is work-item **#9** and is not built here. Default static root is
  the crate-local `crates/chirp-server/static/` (resolved from `CARGO_MANIFEST_DIR` at compile time, so
  it is found regardless of CWD); a committed placeholder `index.html` lives there. Override with the
  `CHIRP_STATIC_DIR` env var.
- Because the API is under `/api/…` it never collides with the static/SPA path space. Note: an unknown
  `/api/…` path also falls through to the SPA `index.html` (200), not a bare 404 — genuine API 404s
  come from the handlers (e.g. unknown id). Tests asserting 404 should hit a real handler route with an
  absent resource, not a nonexistent path.

## Running the server

```text
cargo run -p chirp-server          # binds 127.0.0.1:3000, in-memory repo, no DB
```

Environment knobs (all optional): `CHIRP_BIND_ADDR` (`host:port`, default `127.0.0.1:3000`),
`CHIRP_STATIC_DIR` (SPA static root), `RUST_LOG` (tracing env-filter, default
`info,chirp_server=debug,tower_http=info`). `main.rs` installs tracing (binary only), builds
`AppState` + `build_router`, binds a `TcpListener`, and `axum::serve`s with graceful shutdown on
Ctrl-C. The per-request `TraceLayer` lives inside `build_router`, so the app — not just the binary — is
traced; library/tests install no global subscriber.

## Module layout as committed

```
crates/chirp-server/src/
├── lib.rs        # pub mod api/error/repository; pub use api::{build_router, AppState, AuthUser, ValidatedJson}; pub use error::ServerError; pub use repository::{ChirpRepository, InMemoryRepository}
├── main.rs       # binary: init tracing, build state+router, bind, serve (graceful shutdown)
├── error.rs      # ServerError enum + code()/into_api_error() + impl IntoResponse (+ From<JsonRejection>)
├── repository/   # predecessor's ChirpRepository trait + InMemoryRepository (unchanged by this subtree)
└── api/
    ├── mod.rs      # pub mod auth/handlers/json/router/state + re-exports
    ├── state.rs    # AppState { repo: Arc<dyn ChirpRepository> }
    ├── auth.rs     # AuthUser (FromRequestParts Bearer extractor)
    ├── json.rs     # ValidatedJson<T> (FromRequest; rejection → ServerError::InvalidBody) — F1
    ├── handlers.rs # the 9 endpoint-surface handlers (+ handler-level unit tests)
    └── router.rs   # build_router + healthz + static/SPA fallback + TraceLayer
```

## Local verification status (API-layer gate, authoritative)

| Check | Command | Result |
|-------|---------|--------|
| build  | `cargo build -p chirp-server`                               | ✅ clean |
| clippy | `cargo clippy -p chirp-server --all-targets -- -D warnings` | ✅ no warnings |
| fmt    | `cargo fmt -p chirp-server --check`                         | ✅ clean |

## Lane boundary (left for the parent-level siblings — NOT the API layer)

- `SUBTASK_integration_tests_and_docs`: the end-to-end `tests/` HTTP suite driving
  `chirp_server::build_router`, and the crate `README.md`. (At gate time the clone already carried an
  integration suite + README at `ea08e73`; confirm/extend per that spoke's own charter.)
- `SUBTASK_synthesis_gate` (parent): the authoritative full-workspace `cargo test` + four-check over
  the whole crate, and the PR into `main` (`Closes #8`).
