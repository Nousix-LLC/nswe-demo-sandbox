# Transport Foundations — Implementation Notes (handoff to `SUBTASK_handlers`)

This records the **exposed symbols and their locations** the transport-foundations spoke committed
to `work/chirp-server`, so the handlers spoke composes against the **real committed code** without
guessing. Compose against the clone at
`/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout`, branch
`work/chirp-server`.

| What | Value |
|------|-------|
| Clone path | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout` |
| Branch | `work/chirp-server` |
| This commit | `6f32dc0` — `feat(chirp-server): add error IntoResponse, AppState, auth extractor` |
| Predecessor commit | `6ba64d0` — scaffold + persistence (unchanged) |

## Module layout as committed (additions marked)

```
crates/chirp-server/src/
├── lib.rs          # ADDED: `pub mod api;` + `pub use api::{AppState, AuthUser};`
├── error.rs        # ADDED: `impl IntoResponse for ServerError` (+ axum imports)
├── repository/     # predecessor's — unchanged
└── api/            # NEW module (owned by this spoke)
    ├── mod.rs      # `pub mod state; pub mod auth;` + `pub use` of AppState, AuthUser
    ├── state.rs    # AppState
    └── auth.rs     # AuthUser extractor
```

Internal module names (`state.rs`, `auth.rs`) are this spoke's choice. The handlers spoke adds its
own module(s) under `src/api/` (e.g. `handlers.rs` or per-resource modules) by appending a
`pub mod …;` line to `src/api/mod.rs` — edit that file **serially**, it is shared down the chain.

---

## Exposed symbols the handlers spoke composes against

### 1. `AppState` — the shared axum state

- **Location:** `crates/chirp-server/src/api/state.rs`; re-exported at crate root as
  `chirp_server::AppState` and as `crate::api::AppState`.
- **Shape:**
  ```rust
  #[derive(Clone)]
  pub struct AppState {
      pub repo: Arc<dyn ChirpRepository>,
  }
  impl AppState {
      pub fn new(repo: Arc<dyn ChirpRepository>) -> Self;
  }
  ```
- **How a handler names it:** `State(state): State<AppState>`, then `state.repo.<op>(…).await`.
  `AppState` is `Clone` (an `Arc` bump) and is the state type `build_router` will be generic-free
  over — the whole app uses this single state type.
- **Note for `build_router` (router spoke):** construct it as
  `Router::new()….with_state(AppState::new(repo))`.

### 2. `AuthUser` — the `Authorization: Bearer` extractor

- **Location:** `crates/chirp-server/src/api/auth.rs`; re-exported as `chirp_server::AuthUser` /
  `crate::api::AuthUser`.
- **Shape:**
  ```rust
  pub struct AuthUser(pub UserId);              // UserId = chirp_types::ids::UserId
  impl AuthUser { pub fn user_id(&self) -> UserId; }

  impl<S> FromRequestParts<S> for AuthUser
  where S: Send + Sync, AppState: FromRef<S>
  { type Rejection = ServerError; /* async */ }
  ```
- **What it yields:** the authenticated `UserId`. It reads `Authorization: Bearer <token>`,
  resolves it via `state.repo.resolve_token(&SessionToken(raw)).await`, and returns `AuthUser(id)`.
- **How a handler names it:** put it in the argument list, e.g.
  `async fn create_chirp(AuthUser(author): AuthUser, State(state): State<AppState>, Json(req): Json<CreateChirpRequest>) -> Result<Json<Chirp>, ServerError>`.
  Because it is generic over `S` with `AppState: FromRef<S>` (and axum's blanket `FromRef<S> for S`
  covers `S = AppState`), it works directly with a `Router<AppState>` — no extra `FromRef` impl
  needed. The extractor owns **no** session state; the session store lives behind the repo.
- **Failure:** any missing / malformed / non-`Bearer` / empty / unresolvable token →
  `ServerError::Unauthorized` → HTTP **401** (via the `IntoResponse` below). A token the repo
  rejects propagates the repo's `Unauthorized` unchanged.
- **Extractor-ordering tip:** `FromRequestParts` runs on request *parts*; place `AuthUser` before a
  body extractor (`Json<…>`, which is `FromRequest` and consumes the body) in the handler arg list.

### 3. `impl IntoResponse for ServerError` — error rendering

- **Location:** `crates/chirp-server/src/error.rs` (lives beside the enum; the enum itself is the
  predecessor's and is unchanged).
- **Effect:** a handler may return `Result<T, ServerError>` (or `Result<impl IntoResponse,
  ServerError>`) and errors render automatically. Body is `Json(ApiError)`; status is derived from
  `err.code()`.
- **Variant → `ErrorCode` → HTTP status (matches the parent `error_mapping` table):**

  | `ServerError` variant | `ErrorCode` | HTTP status |
  |-----------------------|-------------|-------------|
  | `Validation(_)`  | `VALIDATION_ERROR` | **400** (field `details` populated from the `ValidationError`) |
  | `Unauthorized(_)`| `UNAUTHORIZED`     | **401** |
  | `Forbidden(_)`   | `FORBIDDEN`        | **403** |
  | `NotFound(_)`    | `NOT_FOUND`        | **404** |
  | `Conflict(_)`    | `CONFLICT`         | **409** |
  | `Internal(_)`    | `INTERNAL`         | **500** (message logged via `tracing::error!`; wire body is the generic `"an internal server error occurred"`) |

- The JSON body is `chirp_types::api::ApiError { code, message, details }`, serialized camelCase
  (so `details` is omitted when empty). For `Validation`, `details` carries one `FieldError` with
  the offending field, courtesy of the predecessor's `into_api_error()`.

---

## How the pieces fit for a handler (illustrative, for the handlers spoke)

```rust
use axum::{extract::State, Json};
use chirp_server::{AppState, AuthUser, ServerError};
use chirp_types::api::CreateChirpRequest;
use chirp_types::domain::Chirp;

async fn create_chirp(
    AuthUser(author): AuthUser,          // 401 if no/invalid Bearer token
    State(state): State<AppState>,
    Json(req): Json<CreateChirpRequest>, // body extractor comes last
) -> Result<Json<Chirp>, ServerError> {
    let chirp = state.repo.create_chirp(author, req).await?; // ? => IntoResponse maps the error
    Ok(Json(chirp))
}
```

- Unauthenticated endpoints (`create_user`, `get_user`, `login`) simply omit `AuthUser`.
- The success **status codes** in the endpoint surface (e.g. `201` for creates) are the handlers
  spoke's responsibility to set (e.g. return `(StatusCode::CREATED, Json(..))`); the foundations
  layer fixes only the error-path statuses.
- Delegate every op through `state.repo.<op>` — no bypass. The repo's behavioral contract (errors
  per op) is in `../../SUBTASK_scaffold_and_repository/IMPLEMENTATION_NOTES.md`.

## Imports / do-not-redeclare

- Wire types from `chirp_types` (`ApiError`, `ErrorCode`, `SessionToken`, `UserId`, the DTOs …) —
  imported, never re-declared.
- `ServerError`, `ChirpRepository`, `InMemoryRepository` from the predecessor's committed modules
  (re-exported at the crate root).

## Local verification status (this spoke, all clean)

| Check | Command | Result |
|-------|---------|--------|
| build | `cargo build -p chirp-server` | ✅ |
| clippy | `cargo clippy -p chirp-server --all-targets -- -D warnings` | ✅ clean |
| fmt | `cargo fmt -p chirp-server --check` | ✅ clean |
| test | `cargo test -p chirp-server` | ✅ 18 passed, 0 failed (no DB); auth doc-example `ignore`d |

## Explicitly out of scope (left for later spokes)

- **`SUBTASK_handlers`:** the axum handler fns for the full `repository_seam` surface, success
  status codes, route metadata.
- **`SUBTASK_router_and_bootstrap`:** `build_router` + `pub use api::build_router;`, `GET /healthz`,
  static `ServeDir` + SPA fallback, `tracing` init + trace layer, `src/main.rs`.
