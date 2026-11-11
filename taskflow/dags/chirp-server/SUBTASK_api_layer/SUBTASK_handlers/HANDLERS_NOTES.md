# Handlers — Implementation Notes (handoff to `SUBTASK_router_and_bootstrap`)

The axum handler functions for the full `repository_seam` endpoint surface are committed to the
shared clone on `work/chirp-server`. They compose against the **real committed** transport
foundations (`AppState`, `AuthUser`, `impl IntoResponse for ServerError`) and the predecessor's
`ChirpRepository`; nothing is re-declared. This file is the authoritative **route-metadata table**
the router-and-bootstrap spoke reads to mount `build_router`, and that the integration-test spoke
later exercises.

> Resumption note: this task's code was committed by a prior invocation (`8c0336f`); this
> reconstructed invocation re-verified the committed artifact against the brief and the full
> build/clippy/fmt/test gate (all clean) and authored this handoff, which had not survived the
> reconstruction. No code change was required.

| What | Value |
|------|-------|
| Clone path | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout` |
| Branch | `work/chirp-server` |
| Handlers commit | `8c0336f` — `feat(chirp-server): add axum handlers for the full endpoint surface` |
| Predecessor commit | `6f32dc0` — error `IntoResponse` + `AppState` + auth extractor (unchanged) |
| Handler module | `crates/chirp-server/src/api/handlers.rs` (all fns `pub`) |
| mod.rs wiring | `src/api/mod.rs` gained `pub mod handlers;` (serial edit of the shared file) |

## Module / symbol seam exposed for the router spoke

- Every handler lives in `crate::api::handlers` and is `pub async fn`. The router spoke imports them
  as `use crate::api::handlers::{…}` (or `chirp_server::api::handlers::…` from `tests/`).
- All handlers are generic-free over the single `AppState` state type, so `build_router` is a plain
  `Router<AppState>` → `.with_state(AppState::new(repo))` (no extra `FromRef` impls needed; the
  `AuthUser` extractor is already generic over `S: AppState: FromRef<S>`, satisfied by `AppState`).
- `src/api/mod.rs` currently re-exports `AppState` and `AuthUser` only; `handlers` is reachable as
  the `pub mod handlers`. The router spoke may add a `pub use handlers::*;` if it prefers — not
  required.

## Route-metadata table (authoritative — mount exactly these)

Method + path are this spoke's design call (REST + status-code discipline); the router spoke mounts
them verbatim. Path params use axum 0.8 `{param}` syntax. "Auth" = requires a valid
`Authorization: Bearer <token>` (resolved by the `AuthUser` extractor → `UserId`; 401 on
missing/invalid before the handler body runs).

| # | Handler fn (`crate::api::handlers::…`) | Method | Path | Auth | Request payload (extractor) | Response body | Success status | Key error statuses |
|---|----------------------------------------|--------|------|------|-----------------------------|---------------|----------------|--------------------|
| 1 | `create_user`  | POST   | `/api/users`               | no  | `CreateUserRequest` (`Json` body)           | `User`          | **201** | 409 duplicate username; 400 invalid handle |
| 2 | `get_user`     | GET    | `/api/users/{id}`          | no  | `UserId` (`Path`)                           | `User`          | **200** | 404 unknown id |
| 3 | `login`        | POST   | `/api/sessions`            | no  | `LoginRequest` (`Json` body)                | `AuthResponse`  | **200** | 404 unknown handle |
| 4 | `create_chirp` | POST   | `/api/chirps`              | yes | `CreateChirpRequest` (`Json` body)          | `Chirp`         | **201** | 404 absent reply target; 400 invalid body; 401 |
| 5 | `timeline`     | GET    | `/api/timeline`            | yes | `TimelineQuery` (`Query` string)            | `Page<Chirp>`   | **200** | 401 |
| 6 | `follow`       | PUT    | `/api/users/{id}/follow`   | yes | `UserId` (`Path` = followee)                | `FollowResponse`| **200** | 403 self-follow; 404 absent; 401 |
| 7 | `unfollow`     | DELETE | `/api/users/{id}/follow`   | yes | `UserId` (`Path` = followee)                | `FollowResponse`| **200** | 404 absent; 401 |
| 8 | `like`         | PUT    | `/api/chirps/{id}/like`    | yes | `ChirpId` (`Path`)                          | `LikeResponse`  | **200** | 404 absent chirp; 401 |
| 9 | `unlike`       | DELETE | `/api/chirps/{id}/like`     | yes | `ChirpId` (`Path`)                          | `LikeResponse`  | **200** | 404 absent chirp; 401 |

All responses are JSON (`Json<T>` or `(StatusCode, Json<T>)`). Every handler returns
`Result<_, ServerError>`; error bodies render as `chirp_types::api::ApiError` via the committed
`impl IntoResponse for ServerError`, with statuses per the parent contract `error_mapping` table.

### Exact handler signatures (for mounting)

```rust
// unauthenticated
pub async fn create_user(State<AppState>, Json<CreateUserRequest>) -> Result<(StatusCode, Json<User>), ServerError>; // 201
pub async fn get_user   (State<AppState>, Path<UserId>)           -> Result<Json<User>, ServerError>;                // 200
pub async fn login      (State<AppState>, Json<LoginRequest>)     -> Result<Json<AuthResponse>, ServerError>;        // 200

// authenticated (AuthUser is a FromRequestParts extractor — place it BEFORE any Json body extractor)
pub async fn create_chirp(AuthUser, State<AppState>, Json<CreateChirpRequest>) -> Result<(StatusCode, Json<Chirp>), ServerError>; // 201
pub async fn timeline    (AuthUser, State<AppState>, Query<TimelineQuery>)     -> Result<Json<Page<Chirp>>, ServerError>;         // 200
pub async fn follow      (AuthUser, State<AppState>, Path<UserId>)             -> Result<Json<FollowResponse>, ServerError>;       // 200
pub async fn unfollow    (AuthUser, State<AppState>, Path<UserId>)             -> Result<Json<FollowResponse>, ServerError>;       // 200
pub async fn like        (AuthUser, State<AppState>, Path<ChirpId>)            -> Result<Json<LikeResponse>, ServerError>;         // 200
pub async fn unlike      (AuthUser, State<AppState>, Path<ChirpId>)            -> Result<Json<LikeResponse>, ServerError>;         // 200
```

## Design decisions (this spoke's calls — recorded for the gate)

- **Resource layout under `/api`.** All nine routes are namespaced under `/api/…` so the router
  spoke can reserve the non-`/api` path space for the static `ServeDir` + SPA fallback without
  colliding with the API surface. (The router spoke owns that split; this is the assumption the
  paths were chosen under.)
- **Sessions are not addressable resources.** `login` is `POST /api/sessions` returning **200** (not
  201): the client receives its bearer token in the `AuthResponse` body and presents it via
  `Authorization: Bearer`; there is no session URL to redirect to.
- **Idempotent mutations use `PUT`/`DELETE`, not `POST`.** `follow`/`like` are `PUT` (repeat = no-op,
  same 200 response) and `unfollow`/`unlike` are `DELETE` (idempotent), matching the repository's
  documented idempotency and REST method semantics. The followee/chirp target is the path id; the
  actor is always the authenticated `AuthUser` (never taken from the body), so a caller can only act
  as itself.
- **Timeline is the HOME timeline**, passed through unchanged. The handler forwards `TimelineQuery`
  (`limit`, `cursor`) to `repo.timeline(viewer, query)` and echoes `page.next_cursor` back to the
  client; the repository owns the `1..=100` limit clamp (default 20) and the opaque last-id cursor —
  the handler adds no pagination logic of its own. No per-user profile feed is routed (it would be a
  thin api-layer derivation, explicitly out of scope here).
- **Success status is the handler's to set.** Creates return `(StatusCode::CREATED, Json(..))` → 201;
  everything else is axum's default 200 via `Json<T>`. The foundations layer fixes only error-path
  statuses.
- **Nothing held across `.await`.** Each handler awaits exactly one `repo` op and maps the result;
  no lock/guard/borrow is held across the await (the repo holds nothing internally either).

## Verification status (this invocation, authoritative re-run on the committed code)

| Check | Command | Result |
|-------|---------|--------|
| build  | `cargo build -p chirp-server`                                  | ✅ clean |
| clippy | `cargo clippy -p chirp-server --all-targets -- -D warnings`    | ✅ no warnings |
| fmt    | `cargo fmt -p chirp-server --check`                            | ✅ clean |
| test   | `cargo test -p chirp-server`                                   | ✅ 23 passed, 0 failed (18 repo + 5 handler), auth doc-example `ignore`d |

The 5 handler-level unit tests in `handlers.rs::tests` call each handler directly against a real
`InMemoryRepository` (no HTTP stack) and assert delegation, the 201/200 success statuses, and the
`Conflict`/`NotFound`/`Forbidden` error variants. End-to-end HTTP routing is the integration-test
spoke's job.

## Imports / do-not-redeclare (confirmed)

- DTOs & ids from `chirp_types` — `api::{AuthResponse, CreateChirpRequest, CreateUserRequest,
  FollowResponse, LikeResponse, LoginRequest, Page, TimelineQuery}`, `domain::{Chirp, User}`,
  `ids::{ChirpId, UserId}`. None re-declared.
- `AppState`, `AuthUser`, `ServerError` from the crate root (`crate::{AppState, AuthUser,
  ServerError}`) — the foundations' / predecessor's committed types.

## Explicitly left for the next spokes (not this spoke)

- **`SUBTASK_router_and_bootstrap`:** `build_router(state)` mounting the nine routes above +
  `GET /healthz` + static `ServeDir` + SPA fallback; `tracing` init + request-trace layer;
  `pub use api::build_router;` in `lib.rs`; `src/main.rs`.
- **`SUBTASK_integration_tests_and_docs`:** end-to-end HTTP tests driving `build_router`, `README.md`.
