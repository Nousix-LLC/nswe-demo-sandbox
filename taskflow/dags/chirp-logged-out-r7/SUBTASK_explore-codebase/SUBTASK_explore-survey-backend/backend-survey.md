# Backend API Survey — `crates/chirp-server`

## 1. Crate Structure

### File Layout

```
crates/chirp-server/
├── Cargo.toml
├── static/
│   └── index.html          (placeholder SPA; replaced by real build)
├── src/
│   ├── lib.rs              (crate root: re-exports build_router, AppState, error types)
│   ├── main.rs             (binary entrypoint: tokio runtime, tracing, serve)
│   ├── error.rs            (ServerError enum + IntoResponse impl)
│   ├── ssr.rs              (SSR handler: render_to_string via Ferric)
│   └── api/
│       ├── mod.rs          (pub re-exports: build_router, handlers, auth, state, json)
│       ├── router.rs       (build_router: composes all routes + middleware)
│       ├── handlers.rs     (all handler functions)
│       ├── auth.rs         (AuthUser extractor: FromRequestParts)
│       ├── state.rs        (AppState: Arc<dyn ChirpRepository>)
│       └── json.rs         (ValidatedJson extractor: FromRequest body)
│   └── repository/
│       ├── mod.rs          (ChirpRepository trait + argon2 helpers)
│       ├── in_memory.rs    (InMemoryRepository: default, no DB)
│       ├── postgres.rs     (PostgresRepository: behind `postgres` feature flag)
│       └── export.rs       (shared data-export shape)
└── tests/
    ├── api.rs              (end-to-end integration tests)
    └── concurrency_invariants.rs
```

### Entrypoint

`main.rs` is the binary entrypoint. It installs a `tracing` subscriber, constructs an `AppState`
with either `PostgresRepository` (when `--features postgres` is enabled and a connection string is
configured) or `InMemoryRepository` (default), calls `build_router(state)`, and passes the result
to `axum::serve()`.

The library root re-exports `build_router` and `AppState` so integration tests construct the app
identically to the binary.

### Routing and Auth Dependencies (Cargo.toml)

| Dependency | Version | Role |
|---|---|---|
| `axum` | `0.8` | HTTP framework: Router, handlers, extractors, middleware |
| `tower` | `0.5` | Middleware trait foundation |
| `tower-http` | `0.6` (features: `fs`, `trace`) | `ServeDir`/`ServeFile` for SPA; `TraceLayer` for request tracing |
| `chirp-types` | path dep | All wire types (DTOs, ids, errors) — never re-declared in server |
| `ferric` | path dep | SSR render_to_string (native, non-WASM) |
| `argon2` | `0.5` | Argon2id password hashing (credential storage) |
| `async-trait` | `0.1` | Makes `async fn` in `ChirpRepository` dyn-compatible |
| `thiserror` | `2` | `#[derive(Error)]` on `ServerError` |
| `serde` / `serde_json` | current | JSON serialization |
| `sqlx` | `0.8` | Optional async Postgres driver (behind `postgres` feature) |

---

## 2. Endpoint Inventory

All routes are registered in `build_router` in `src/api/router.rs`. Auth is **not** a middleware
layer — it is opt-in per handler via the `AuthUser` extractor (see §5).

| Method | URL Pattern | Handler | File | Auth | Description |
|---|---|---|---|---|---|
| `GET` | `/` | `ssr_handler` | `src/ssr.rs` | none | SSR-rendered root document (Ferric) |
| `GET` | `/healthz` | `healthz` | `src/api/router.rs` | none | Liveness probe: 200 OK |
| `GET` | `/readyz` | `readyz` | `src/api/router.rs` | none | Readiness probe: calls `store_health()`; 200/503 |
| `POST` | `/api/users` | `create_user` | `src/api/handlers.rs` | none | Register a new user; 201 Created |
| `GET` | `/api/users/{id}` | `get_user` | `src/api/handlers.rs` | none | Fetch user by id (UserId); 200 |
| `GET` | `/api/users/{username}/chirps` | `user_chirps` | `src/api/handlers.rs` | none | Public user profile + chirps by username; 200/404 |
| `POST` | `/api/sessions` | `login` | `src/api/handlers.rs` | none | Authenticate by handle; returns session token; 200 |
| `GET` | `/api/chirps` | `public_chirps` | `src/api/handlers.rs` | none | Public timeline with embedded author info; 200 |
| `POST` | `/api/chirps` | `create_chirp` | `src/api/handlers.rs` | **required** | Post a new chirp as the authenticated user; 201 |
| `GET` | `/api/timeline` | `timeline` | `src/api/handlers.rs` | **required** | Authenticated home timeline (own + followed); 200 |
| `GET` | `/api/public/timeline` | `public_timeline` | `src/api/handlers.rs` | none | Global timeline (domain Chirp objects, no embedded author); 200 |
| `PUT` | `/api/users/{id}/follow` | `follow` | `src/api/handlers.rs` | **required** | Follow a user; idempotent; 200 |
| `DELETE` | `/api/users/{id}/follow` | `unfollow` | `src/api/handlers.rs` | **required** | Unfollow a user; idempotent; 200 |
| `PUT` | `/api/chirps/{id}/like` | `like` | `src/api/handlers.rs` | **required** | Like a chirp; idempotent; 200 |
| `DELETE` | `/api/chirps/{id}/like` | `unlike` | `src/api/handlers.rs` | **required** | Unlike a chirp; idempotent; 200 |
| `*` | `/*` | SPA fallback | `tower-http ServeDir` | none | Static files; falls back to `index.html` |

---

## 3. Public Timeline Endpoint Assessment

### Finding: endpoint exists and satisfies the contract

**Contract requirement**: unauthenticated GET returning chirps with `id`, `content/text`,
`author username`, `created_at`, pagination, and an empty list (not an error) when no chirps exist.

**Satisfying endpoint**: `GET /api/chirps` → handler `public_chirps`

Response type: `PublicTimelineResponse`
```rust
pub struct PublicTimelineResponse {
    pub chirps: Vec<PublicChirp>,
    pub has_more: bool,
}

pub struct PublicChirp {
    pub id: ChirpId,
    pub content: String,            // chirp text
    pub author: PublicAuthor,       // { username: String, display_name: Option<String> }
    pub created_at: i64,            // milliseconds since epoch
    pub like_count: u64,
}
```

Query parameters: `before` (optional `i64` timestamp cursor — only chirps older than this value
are returned), `limit` (optional, clamped to 1–50, defaults to 20).

Verification:
- ✅ No `AuthUser` extractor — no authentication required
- ✅ Returns `author.username` embedded in each chirp (via `public_chirps_with_authors` join)
- ✅ Pagination supported via `before` cursor + `has_more` flag
- ✅ Returns empty `chirps: []` with `has_more: false` when no chirps exist (confirmed by unit test)
- ✅ All required fields present: `id`, `content`, `author.username`, `created_at`

**Note on `GET /api/public/timeline`**: a second unauthenticated timeline endpoint exists but
returns `Page<Chirp>` (the internal domain `Chirp` type), which carries only `author_id` (a
`UserId`), not `author_username`. It does not satisfy the contract as written. The
`public_chirps` handler is the correct endpoint.

---

## 4. Public User Profile Endpoint Assessment

### Finding: endpoint exists and satisfies the contract

**Contract requirement**: unauthenticated GET returning user profile (`username`, `display_name`,
`bio`) + that user's public chirps + 404 for unknown usernames.

**Satisfying endpoint**: `GET /api/users/{username}/chirps` → handler `user_chirps`

The `{username}` path segment is a string (not a `UserId`). Lookup is case-insensitive.

Response type: `PublicUserResponse`
```rust
pub struct PublicUserResponse {
    pub user: PublicUserProfile,
    pub chirps: Vec<PublicUserChirp>,
    pub has_more: bool,
}

pub struct PublicUserProfile {
    pub username: String,
    pub display_name: Option<String>,
    pub bio: Option<String>,
    pub chirp_count: u64,          // total chirps authored (not just this page)
}

pub struct PublicUserChirp {
    pub id: ChirpId,
    pub content: String,
    pub created_at: i64,           // milliseconds since epoch
    pub like_count: u64,
}
```

Query parameters: same as `GET /api/chirps` — `before` cursor (timestamp), `limit` (1–50, default 20).

Verification:
- ✅ No `AuthUser` extractor — no authentication required
- ✅ Returns `username`, `display_name`, `bio`
- ✅ Returns the user's chirps (paginated)
- ✅ Returns `ServerError::NotFound` → HTTP 404 for unknown usernames
- ✅ Case-insensitive username lookup (confirmed by unit test)

---

## 5. Auth Middleware Pattern

### No global auth middleware — auth is per-handler via extractor

There is **no** auth middleware layer applied at the router level. `build_router` applies only one
cross-cutting layer: `TraceLayer::new_for_http()` (request/response tracing). Authentication is
opt-in per handler by declaring the `AuthUser` extractor as a handler argument.

### `AuthUser` — `FromRequestParts` extractor

```rust
pub struct AuthUser(pub UserId);

impl<S> FromRequestParts<S> for AuthUser
where
    S: Send + Sync,
    AppState: FromRef<S>,
{
    type Rejection = ServerError;

    async fn from_request_parts(parts: &mut Parts, state: &S) -> Result<Self, Self::Rejection> {
        let state = AppState::from_ref(state);
        // 1. Read the Authorization header
        let header = parts.headers.get(AUTHORIZATION)
            .ok_or_else(|| ServerError::Unauthorized("missing Authorization header"))?;
        // 2. Parse "Bearer <token>"
        let (scheme, token) = raw.split_once(' ') ...;
        if !scheme.eq_ignore_ascii_case("bearer") { return Err(Unauthorized); }
        // 3. Resolve the token to a UserId via the repository
        let user_id = state.repo.resolve_token(&SessionToken(token)).await?;
        Ok(AuthUser(user_id))
    }
}
```

Key properties:
- **`FromRequestParts`** (not `FromRequest`) — reads only headers, not the body. Per Axum 0.8
  extractor ordering rules, it can safely be placed before or after body extractors in a handler
  signature.
- **Generic over state** with `AppState: FromRef<S>` — works against any router state from which
  `AppState` is projectable (including `S = AppState` via the blanket impl).
- **Failure path**: missing header, malformed header, empty token, or token not found in the
  repository all produce `ServerError::Unauthorized` → HTTP 401. The rejection short-circuits
  the handler before the body runs.
- **No JWT** — tokens are opaque session tokens issued by `ChirpRepository::login` and stored
  in the repository. There is no JWT parsing, signing, or verification in the server crate.

### `ValidatedJson` — `FromRequest` body extractor

A second custom extractor (`ValidatedJson<T>`) wraps `axum::Json<T>` to convert deserialization
errors (including `chirp-types` value-object validation failures that surface via
`#[serde(try_from = "String")]`) into `ServerError::InvalidBody` → HTTP 400, rather than axum's
default plain-text 422.

---

## 6. Recommendations for Target Endpoints

### Public Timeline

**Recommendation: Reuse `GET /api/chirps` as-is. No changes needed.**

The `public_chirps` handler and its supporting repository method
(`public_chirps_with_authors`) already implement the full contract:
unauthenticated access, embedded author username, `before`-cursor pagination,
and empty-list semantics. The `SUBTASK_backend-api` task should document this
URL in `backend-impl.md` as the established endpoint. No new handler, no new
route, no changes to auth.

The older `GET /api/public/timeline` endpoint serves a different shape
(`Page<Chirp>` with no embedded author) and should be ignored for logged-out
use cases; it is kept for authenticated clients that already consume it.

### Public User Profile

**Recommendation: Reuse `GET /api/users/{username}/chirps` as-is. No changes needed.**

The `user_chirps` handler returns `PublicUserResponse` with the full contract
surface: username-based lookup, `username` / `display_name` / `bio` profile
fields, paginated chirps, and 404 for unknown handles. Case-insensitive lookup
is already implemented. The `SUBTASK_backend-api` task should document this
URL in `backend-impl.md` as the established endpoint.

---

## 7. Handler Patterns

Three implementations that illustrate the patterns `SUBTASK_backend-api` should follow
(in order of increasing complexity):

### Pattern A — Unauthenticated, path param, single repo call

```rust
/// `GET /api/users/{id}` — fetch a user's public profile by id. Unauthenticated.
pub async fn get_user(
    State(state): State<AppState>,
    Path(id): Path<UserId>,
) -> Result<Json<User>, ServerError> {
    let user = state.repo.get_user(id).await?;
    Ok(Json(user))
}
```

The pattern: `State<AppState>` always comes first; path and query extractors follow.
No `AuthUser` = no authentication. `?` propagates `ServerError` to the `IntoResponse` impl.

### Pattern B — Authenticated, body, non-200 success status

```rust
/// `POST /api/chirps` — post a new chirp as the authenticated caller.
pub async fn create_chirp(
    AuthUser(author): AuthUser,
    State(state): State<AppState>,
    ValidatedJson(request): ValidatedJson<CreateChirpRequest>,
) -> Result<(StatusCode, Json<Chirp>), ServerError> {
    let chirp = state.repo.create_chirp(author, request).await?;
    Ok((StatusCode::CREATED, Json(chirp)))
}
```

The pattern: `AuthUser` before `State` before `ValidatedJson` (body extractor must be last).
Return `(StatusCode, Json<T>)` for non-200 success codes. `AuthUser(author)` destructures
the `UserId` inline.

### Pattern C — Unauthenticated, path + query, response assembly with mapping

```rust
/// `GET /api/users/{username}/chirps` — public user profile and chirps. Unauthenticated.
pub async fn user_chirps(
    State(state): State<AppState>,
    Path(username): Path<String>,
    Query(query): Query<PublicTimelineQuery>,
) -> Result<Json<PublicUserResponse>, ServerError> {
    let limit = query.limit.unwrap_or(20).clamp(1, 50);
    let (user, chirp_count, chirps, has_more) = state
        .repo
        .get_user_chirps_by_username(&username, query.before, limit)
        .await?;
    // Map domain types → wire types in the handler body
    let chirps = chirps.into_iter().map(|chirp| PublicUserChirp { ... }).collect();
    let profile = PublicUserProfile { username: user.username.into_string(), ... };
    Ok(Json(PublicUserResponse { user: profile, chirps, has_more }))
}
```

The pattern: when the repository returns domain types that don't match the wire type, map them
in the handler body before wrapping in `Json(...)`. Keep the mapping simple and mechanical;
no business logic belongs in the handler.
