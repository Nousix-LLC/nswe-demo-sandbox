# Scaffold + Repository — Implementation Notes (handoff to `SUBTASK_api_layer`)

This records the design decisions, the frozen seam, and the build status of the
`SUBTASK_scaffold_and_repository` spoke. The api-layer spoke composes against the **real committed
code** in the shared clone (not this prose); this file orients that work and records the calls that
are mine to make.

## Clone / branch pointers

| What | Value |
|------|-------|
| Clone path | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout` |
| Branch | `work/chirp-server` (cut off `main` @ `25e90c0`; `chirp-types` present @ `2e32aed`) |
| This commit | `6ba64d0` — `chirp-server: scaffold crate + persistence layer` |
| Base, untouched | `main` (no commits, no force-push) |

Operate on **this same clone** — do not re-clone. Keep committing to `work/chirp-server`.

## Crate module layout (as committed)

```
crates/chirp-server/
├── Cargo.toml          # workspace member (picked up by the crates/* glob); deps provisioned below
└── src/
    ├── lib.rs          # crate root: `pub mod error; pub mod repository;` + re-exports.
    │                   #   ← api-layer ADDS `pub mod api; pub use api::build_router;` here
    ├── error.rs        # ServerError enum (MINE) + code()/into_api_error() helpers (HTTP-free)
    │                   #   ← api-layer ADDS `impl IntoResponse for ServerError` here (ErrorCode→StatusCode)
    └── repository/
        ├── mod.rs      # ChirpRepository trait (the seam) + DEFAULT_TIMELINE_LIMIT/MAX_TIMELINE_LIMIT
        └── in_memory.rs# InMemoryRepository (default backing) + 18 unit tests
```

Still owned by later spokes (NOT created yet): `src/api/` or handlers, `src/main.rs`, `tests/`,
`README.md`, `static/`.

## Concurrency choice + rationale

**`async` trait, object-safe via `async-trait`; in-memory state behind a single `std::sync::Mutex`.**

- The trait exists to make persistence *replaceable*; the realistic replacement is an async DB, so
  the seam is async (`async fn` on every op). `async-trait` keeps it **object-safe**, so the
  api-layer holds `Arc<dyn ChirpRepository>` as axum state instead of threading a generic backend
  type through every handler. (Native async-fn-in-trait is not yet `dyn`-compatible — hence the
  crate, not RPITIT.)
- All methods take `&self`; the impl owns interior mutability (`Mutex<Store>`), so it lives behind a
  plain `Arc` shared across concurrent requests.
- Each method is **one synchronous critical section with no `.await` held across the lock guard**,
  so the generated futures stay `Send` and a `std::sync::Mutex` is correct and cheap. A single
  global lock is intentionally simple for demo scale (a production backing would shard / use
  `RwLock`); the seam would be unchanged.

**api-layer implication:** build `AppState` holding `repo: Arc<dyn ChirpRepository>`. Handlers are
`async` and `.await` the repo calls. Do **not** hold anything across awaits beyond what the repo
already does internally (it holds nothing across awaits).

## `ChirpRepository` trait (final signature)

`crates/chirp-server/src/repository/mod.rs`. Decorated `#[async_trait]`; `Send + Sync`. All
operations return `Result<_, ServerError>`. Types are imported from `chirp-types` (never
re-declared).

```rust
#[async_trait]
pub trait ChirpRepository: Send + Sync {
    async fn create_user(&self, request: CreateUserRequest) -> Result<User, ServerError>;
    async fn get_user(&self, id: UserId) -> Result<User, ServerError>;
    async fn login(&self, request: LoginRequest) -> Result<AuthResponse, ServerError>;
    async fn resolve_token(&self, token: &SessionToken) -> Result<UserId, ServerError>;
    async fn create_chirp(&self, author: UserId, request: CreateChirpRequest) -> Result<Chirp, ServerError>;
    async fn timeline(&self, viewer: UserId, query: TimelineQuery) -> Result<Page<Chirp>, ServerError>;
    async fn follow(&self, follower: UserId, followee: UserId) -> Result<FollowResponse, ServerError>;
    async fn unfollow(&self, follower: UserId, followee: UserId) -> Result<FollowResponse, ServerError>;
    async fn like(&self, user: UserId, chirp: ChirpId) -> Result<LikeResponse, ServerError>;
    async fn unlike(&self, user: UserId, chirp: ChirpId) -> Result<LikeResponse, ServerError>;
}
```

Behavioral contract (what the api-layer can rely on — enforced + unit-tested in `in_memory.rs`):

| Op | Semantics | Error(s) |
|----|-----------|----------|
| `create_user` | assigns id, `created_at`, zeroed counts | `Conflict` on duplicate username |
| `get_user` | fetch profile by id | `NotFound` |
| `login` | handle-based; returns `AuthResponse { user, token }`; mints + stores an opaque `SessionToken` | `NotFound` for unknown handle |
| `resolve_token` | maps a presented bearer token → `UserId` (session store lives behind the trait) | `Unauthorized` for unknown/invalid token |
| `create_chirp` | assigns id, `created_at`, zeroed `like_count`; `reply_to` validated | `NotFound` for absent author or absent reply target |
| `timeline` | **home timeline** = viewer's own chirps + followees', newest-first; `limit` clamped `1..=100` (default 20); `cursor` = opaque last-id, continues strictly older; `next_cursor` set iff more remain; malformed cursor fails safe to first page | `NotFound` for absent viewer |
| `follow` | idempotent; updates both denormalized counts | `Forbidden` on self-follow; `NotFound` if either user absent |
| `unfollow` | idempotent; decrements counts (saturating) | `NotFound` if either user absent |
| `like` | idempotent; increments `like_count` | `NotFound` for absent chirp/user |
| `unlike` | idempotent; decrements `like_count` (saturating) | `NotFound` for absent chirp/user |

Notes for the api-layer:
- **Auth extractor:** resolve the `Authorization: Bearer <token>` header via
  `repo.resolve_token(&SessionToken(raw)).await` → `UserId`. On `Err`, that is a 401. This is the
  intended wiring for the `auth_note` in the contract — no separate session store needed.
- **`timeline` is a *home* timeline** (self + followees), not a global firehose and not a
  single-user profile feed. If the acceptance surface wants a per-user profile feed, that is a thin
  additional concern for the api/service layer to derive; the repository exposes the home timeline.
- **Pagination cursor** is the decimal chirp id of the last item returned; treat it as opaque and
  echo `page.next_cursor` back in the next `TimelineQuery`.

## `ServerError` enum + error mapping

`crates/chirp-server/src/error.rs`. `#[derive(thiserror::Error)]`, `#[non_exhaustive]`. **I own the
enum; the api-layer owns `impl IntoResponse`.**

```rust
pub enum ServerError {
    Validation(#[from] chirp_types::domain::ValidationError), // VALIDATION_ERROR / 400
    Unauthorized(String),                                     // UNAUTHORIZED     / 401
    Forbidden(String),                                        // FORBIDDEN        / 403
    NotFound(String),                                         // NOT_FOUND        / 404
    Conflict(String),                                         // CONFLICT         / 409
    Internal(String),                                         // INTERNAL         / 500
}
```

Helpers provided for the transport layer (both HTTP-free, both over `chirp-types`):
- `fn code(&self) -> chirp_types::api::ErrorCode` — the machine-readable category.
- `fn into_api_error(&self) -> chirp_types::api::ApiError` — ready-to-serialize body; for
  `Validation` it lifts the offending field into a single `FieldError` in `details`.

**api-layer `IntoResponse` recipe:** map `err.code()` → `StatusCode` using the table above
(`ValidationError→400, Unauthorized→401, Forbidden→403, NotFound→404, Conflict→409, Internal→500`),
and serialize `err.into_api_error()` as the JSON body. `?` on a `chirp-types::ValidationError`
already yields `ServerError::Validation` (e.g. when parsing a DTO field fails). For `Internal`, log
the message but keep the wire body generic.

## Dependencies provisioned in `Cargo.toml`

Provisioned for the whole crate so the api-layer need not edit the manifest (which this spoke owns):
`chirp-types` (path), `async-trait`, `thiserror 2`, `tokio` (`rt-multi-thread, macros, net,
signal`), `serde`/`serde_json` (workspace), and the transport set the api-layer will use —
`axum 0.8`, `tower 0.5`, `tower-http 0.6` (`fs, trace`), `tracing 0.1`, `tracing-subscriber 0.3`
(`env-filter`). Dev-deps: `tower` (`util`), `http-body-util` for the in-process integration tests.
These transport crates are declared but not yet used by this layer — that is intentional scaffolding
(the workspace lints do not enable `unused_crate_dependencies`, so clippy stays clean).

## Local verification status (all clean)

| Check | Command | Result |
|-------|---------|--------|
| build (pkg) | `cargo build -p chirp-server` | ✅ |
| build (workspace) | `cargo build --workspace` | ✅ (ferric/ferric-http/ferric-router unaffected) |
| test | `cargo test -p chirp-server` | ✅ 18 passed, 0 failed (no DB) |
| fmt | `cargo fmt -p chirp-server --check` | ✅ clean |
| clippy | `cargo clippy -p chirp-server --all-targets -- -D warnings` | ✅ clean |

## What I deliberately left for later spokes

- **api-layer:** axum handlers for every endpoint over `chirp-types` DTOs, router + `AppState`
  (`Arc<dyn ChirpRepository>`), `impl IntoResponse for ServerError`, static-file + SPA-fallback
  serving, `GET /healthz`, `tracing` init, and `src/main.rs`. Add `pub mod api;` +
  `pub use api::build_router;` to `lib.rs`.
- **integration_tests_and_docs:** `tests/` end-to-end API tests (drive `build_router` against an
  `InMemoryRepository`), `README.md`, rustdoc polish.
- **synthesis_gate:** authoritative build/test/fmt/clippy + four-check wiring verification, push,
  PR into `main` (`Closes #8`).
