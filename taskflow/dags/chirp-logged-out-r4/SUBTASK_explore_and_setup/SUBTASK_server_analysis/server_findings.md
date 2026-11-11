# chirp-server API Surface Findings

## Existing Routes

| Path | Method | Auth Required | Handler | Handler File |
|------|--------|---------------|---------|--------------|
| `/` | GET | no | `ssr_handler` | `crates/chirp-server/src/ssr.rs` |
| `/healthz` | GET | no | `healthz` (inline) | `crates/chirp-server/src/api/router.rs` |
| `/readyz` | GET | no | `readyz` (inline) | `crates/chirp-server/src/api/router.rs` |
| `/api/users` | POST | no | `create_user` | `crates/chirp-server/src/api/handlers.rs` |
| `/api/users/{id}` | GET | no | `get_user` | `crates/chirp-server/src/api/handlers.rs` |
| `/api/sessions` | POST | no | `login` | `crates/chirp-server/src/api/handlers.rs` |
| `/api/chirps` | POST | **yes** (`AuthUser`) | `create_chirp` | `crates/chirp-server/src/api/handlers.rs` |
| `/api/timeline` | GET | **yes** (`AuthUser`) | `timeline` | `crates/chirp-server/src/api/handlers.rs` |
| `/api/public/timeline` | GET | no | `public_timeline` | `crates/chirp-server/src/api/handlers.rs` |
| `/api/users/{id}/follow` | PUT | **yes** (`AuthUser`) | `follow` | `crates/chirp-server/src/api/handlers.rs` |
| `/api/users/{id}/follow` | DELETE | **yes** (`AuthUser`) | `unfollow` | `crates/chirp-server/src/api/handlers.rs` |
| `/api/chirps/{id}/like` | PUT | **yes** (`AuthUser`) | `like` | `crates/chirp-server/src/api/handlers.rs` |
| `/api/chirps/{id}/like` | DELETE | **yes** (`AuthUser`) | `unlike` | `crates/chirp-server/src/api/handlers.rs` |

**Note on `{id}` path parameters:** The existing `GET /api/users/{id}` and all other `{id}` paths use
`UserId` (an opaque integer), not a username string. No endpoint currently accepts `:username` as a path
parameter.

---

## Public Endpoint Status

### Public timeline GET
**EXISTS** at `GET /api/public/timeline` (no `Authorization` header required).

- **Handler**: `handlers::public_timeline` — takes `State<AppState>` + `Query<TimelineQuery>`, no
  `AuthUser` extractor, calls `state.repo.public_timeline(query).await`.
- **Response shape**: `Page<Chirp>` serialized as `{"items": [...], "nextCursor": "string | null"}`.
  Each `Chirp` has: `id`, `authorId` (integer, not an embedded author object), `text` (not `content`),
  `createdAt`, `likeCount`, `replyTo`.
- **Pagination**: query accepts `cursor` (opaque string from prior `nextCursor`) and `limit` (integer).
  Response indicates more pages via `nextCursor: non-null` vs `nextCursor: null`; there is **no** `has_more`
  boolean field.

### Public user profile GET
**DOES NOT EXIST.**

The closest endpoint, `GET /api/users/{id}`, looks up a user by integer `UserId`, returns a `User`
object (profile only, no chirps, no pagination). There is no endpoint that:
- Accepts a `:username` (string handle) as a path parameter
- Returns a combined `{user, chirps, has_more}` response
- Paginates a single user's chirp history

---

## Router Setup

- **Router registration file**: `crates/chirp-server/src/api/router.rs`
- **Registration function**: `pub fn build_router(state: AppState) -> Router` — the single composition
  root used by both the binary (`main.rs`) and the integration-test harness.
- **Registration pattern**: `Router::new().route(path, method(handler))...` chain, capped by
  `.fallback_service(spa).layer(TraceLayer::new_for_http()).with_state(state)`. New routes are inserted
  into this chain, before `.fallback_service(spa)`.
- **Recommended new file for public handlers**: `crates/chirp-server/src/api/handlers.rs` already holds
  all handlers; new public handlers (spec endpoints) should be added there to keep the module cohesive.
  If the file grows unwieldy, `crates/chirp-server/src/api/public_handlers.rs` is a natural split point
  and requires only a `pub mod public_handlers;` in `api/mod.rs` and updated `use` in `router.rs`.

---

## Auth Extractor

- **Mandatory auth extractor type name**: `AuthUser`
  - Defined in `crates/chirp-server/src/api/auth.rs`
  - Wraps `UserId` as a newtype: `pub struct AuthUser(pub UserId)`
  - Implements `FromRequestParts<S> where AppState: FromRef<S>`
  - On a missing, malformed, or invalid `Authorization: Bearer` token → rejects with
    `ServerError::Unauthorized` → HTTP 401 **before the handler body runs**
  - Pattern to require auth: include `AuthUser(user_id): AuthUser` as the **first** handler parameter

- **Optional auth extractor type name**: **None exists.**
  - There is no `OptionalAuthUser` or `MaybeAuthUser` type in the codebase.
  - The two auth states are binary: `AuthUser` (mandatory, 401 on absence) or no auth parameter at all
    (unauthenticated endpoint, no token inspection at all).
  - To add an endpoint that works for both logged-in and logged-out callers, the backend spoke must
    either (a) implement a new `OptionalAuthUser` extractor that returns `Option<UserId>`, or (b) keep
    the public endpoints fully unauthenticated (as the spec requires — no auth parameter at all).

- **Usage pattern summary**:
  - Requires auth: `async fn handler(AuthUser(id): AuthUser, State(s): State<AppState>, ...) -> ...`
  - Requires no auth (public): `async fn handler(State(s): State<AppState>, ...) -> ...`
  - The `AuthUser` extractor position in the parameter list is first by convention but is not
    order-dependent (Axum extractors are order-independent for `FromRequestParts`).

---

## Persistence Types

- **Primary state type**: `AppState` (`crates/chirp-server/src/api/state.rs`)
  - `pub struct AppState { pub repo: Arc<dyn ChirpRepository> }`
  - Cheap to clone (arc bump); axum clones it per-request.
  - Extracted in handlers via `State(state): State<AppState>`.

- **Repository trait**: `ChirpRepository` (`crates/chirp-server/src/repository/mod.rs`)
  - `async_trait` object-safe trait (`Arc<dyn ChirpRepository>`)
  - All operations return `Result<_, ServerError>`
  - Relevant methods for the two new spec endpoints:
    - `public_timeline(&self, query: TimelineQuery) -> Result<Page<Chirp>, ServerError>` — **already exists**
    - A method to look up a user by `Username` and return their paginated chirps — **does not exist yet**

- **Concrete implementations**:
  - `InMemoryRepository` — always present, used in tests and dev
  - `PostgresRepository` — behind `#[cfg(feature = "postgres")]`, used in production

- **Usage in handlers**: every handler calls `state.repo.<method>(args).await?` and wraps the result
  in `Ok(Json(...))` or `Ok((StatusCode::CREATED, Json(...)))`. No handler directly touches storage;
  all persistence goes through the repository trait.

---

## API Spec Verdict

### Spec endpoint 1: `GET /api/chirps` (public timeline) → **CONFLICT**

| Dimension | Spec | Existing |
|-----------|------|----------|
| Path | `GET /api/chirps` | `GET /api/public/timeline` |
| Auth | none | none ✓ |
| Chirp field: body | `content` | `text` |
| Chirp field: author | embedded `{username, display_name}` | `authorId` (integer) — not embedded |
| Response wrapper key | `chirps` (array) | `items` (array) |
| Pagination signal | `has_more: bool` | `nextCursor: string | null` |
| Pagination cursor param | `before` (ISO 8601 timestamp) | `cursor` (opaque string) |

**Conflicts**: path, response wrapper key, chirp body field name, author representation (embedded vs
id-only), `has_more` vs opaque cursor, `before`-timestamp cursor vs opaque string cursor.

The existing public timeline is unauthenticated and functionally equivalent (global feed, newest-first),
but the wire shape is incompatible with the spec on multiple dimensions. The backend spoke must implement
to the spec shape.

---

### Spec endpoint 2: `GET /api/users/:username/chirps` (public user profile) → **ABSENT**

No endpoint of this form exists. The existing `GET /api/users/{id}` is unrelated (integer id, profile
only, no chirps). The backend spoke must add this endpoint from scratch, which requires:

1. A new repository trait method to fetch a user by `Username` (string) and return their paginated chirps.
2. A new response DTO that combines user profile + chirp page + has_more.
3. A new route registered in `router.rs`.
4. A new handler in `handlers.rs`.

---

### Pagination approach: `before` cursor + `has_more` → **INCONSISTENT with existing**

- **Spec**: `before` query param (ISO 8601 timestamp), `has_more: bool` in response.
- **Existing**: `cursor` query param (opaque string from prior `nextCursor`), `nextCursor: string | null`
  in response (via `Page<T>` generic envelope). The opaque cursor is likely a chirp id or timestamp
  encoded by the backing store; the client treats it as opaque.

The two approaches are semantically similar (both are cursor-based, reverse-chronological) but the wire
contract is different. Since the spec is frozen, the backend spoke must expose `before`/`has_more` on
the two new spec endpoints. The existing `timeline` and `public/timeline` endpoints retain their current
cursor scheme; the new endpoints use the spec's `before`/`has_more` scheme.

---

### Recommendation for SUBTASK_backend

**Use spec shape for the two new endpoints; leave existing endpoints unchanged.**

Rationale:
- The spec is frozen and both `SUBTASK_backend` and `SUBTASK_frontend` compose against it.
- The existing `Page<Chirp>` / opaque-cursor pattern is used only on the authenticated `timeline`
  and the existing `public/timeline`. The spec's new endpoints (`GET /api/chirps` and
  `GET /api/users/:username/chirps`) are net-new routes, so adopting the spec shape there introduces
  no breaking change to existing consumers.
- The backend spoke should **add** `GET /api/chirps` as a new route (spec path) rather than renaming
  `GET /api/public/timeline`. Both can coexist; the existing route continues to serve any clients
  already using it.
- New response DTOs are needed in `crates/chirp-types/src/api.rs`:
  - `PublicChirp { id, content, author: PublicAuthor, created_at, like_count }` — the enriched chirp
    (denormalized author fields; the handler joins from the repository)
  - `PublicAuthor { username, display_name }`
  - `PublicTimelineResponse { chirps: Vec<PublicChirp>, has_more: bool }`
  - `PublicUserResponse { user: PublicUserProfile, chirps: Vec<PublicUserChirp>, has_more: bool }`
  - `PublicUserProfile { username, display_name, bio, chirp_count }`
  - `PublicUserChirp { id, content, created_at, like_count }` (no author — user is known from path)
- New repository method: `get_user_chirps_by_username(&self, username: &Username, before: Option<Timestamp>, limit: u32) -> Result<(User, Vec<Chirp>, bool), ServerError>`

---

## Files to Modify

| File | Change |
|------|--------|
| `crates/chirp-server/src/api/router.rs` | Add `.route("/api/chirps", get(handlers::public_chirps))` and `.route("/api/users/{username}/chirps", get(handlers::user_chirps))` to the route chain |
| `crates/chirp-server/src/api/handlers.rs` | Add `public_chirps` handler (`GET /api/chirps`) and `user_chirps` handler (`GET /api/users/:username/chirps`); both unauthenticated |
| `crates/chirp-server/src/repository/mod.rs` | Add new `ChirpRepository` trait method: `user_chirps_by_username` (or similar) for the user profile endpoint |
| `crates/chirp-server/src/repository/in_memory.rs` | Implement the new trait method |
| `crates/chirp-server/src/repository/postgres.rs` | Implement the new trait method (postgres feature) |
| `crates/chirp-types/src/api.rs` | Add new response DTOs: `PublicChirp`, `PublicAuthor`, `PublicTimelineResponse`, `PublicUserResponse`, `PublicUserProfile`, `PublicUserChirp` |

**Note on path parameter collision**: The existing `GET /api/users/{id}` uses `Path<UserId>` (integer).
The new `GET /api/users/{username}/chirps` uses a string username as the first segment and `/chirps` as a
suffix. These are structurally distinct (`/api/users/{id}` vs `/api/users/{username}/chirps`) and axum
will route them correctly by suffix match. No collision.
