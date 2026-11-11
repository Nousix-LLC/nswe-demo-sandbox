# Chirp Logged-Out: Codebase Analysis

## Branch Status

Branch `work/chirp-logged-out` exists and already carries a complete implementation of the
logged-out visitor experience. It was created from `main` at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
("Merge pull request #193: Async resources, expanded events, form binding (ferric-async-forms-r3)").

Current HEAD on the branch: `21dca55` ("feat(chirp-frontend): implement sign-up form at /signup route (AC-4)")

Commits added on the branch beyond the base (oldest → newest):

| SHA | Message |
|-----|---------|
| `1d8edab` | feat(chirp-server): add public_timeline capability seam (skeleton) |
| `7160514` | Implement InMemoryRepository::public_timeline |
| `ec70b78` | Implement PostgresRepository::public_timeline |
| `d57335d` | test(chirp-server): add integration tests for public_timeline endpoint |
| `ac3471c` | style(chirp-server): rustfmt public_timeline stub signature in api.rs |
| `908d703` | feat(chirp-frontend): logged-out visitor experience (AC-1–AC-5) |
| `5982429` | Merge remote-tracking branch 'origin/main' into work/chirp-logged-out |
| `2615ba1` | fix(ferric): update hydrate.rs for new EventHandler enum and full EventKind set |
| `eaf96cf` | feat(chirp-server): add public GET /api/chirps and GET /api/users/:username/chirps |
| `e02b1d8` | feat(frontend): public timeline, user profile, sign-in/sign-up routes |
| `fed1fc8` | fix(chirp-frontend): align public API structs with backend wire format |
| `21dca55` | feat(chirp-frontend): implement sign-up form at /signup route (AC-4) |

All acceptance criteria for BAR-011 (AC-1 through AC-5) are present in the branch. No
further implementation is required by downstream tasks; this analysis documents the
design contract as-built for SUBTASK_backend reference.

---

## Backend: Existing API Routes

The full route table (from `crates/chirp-server/src/api/router.rs`) with authentication status:

| Method | Path | Auth | Handler | Notes |
|--------|------|------|---------|-------|
| `GET` | `/` | no | `ssr_handler` | SSR entry point; server-renders application document |
| `GET` | `/healthz` | no | `healthz` | Liveness probe; returns `200 { status: "ok" }` |
| `GET` | `/readyz` | no | `readyz` | Readiness probe; `200` or `503` based on store health |
| `POST` | `/api/users` | no | `create_user` | Register new user |
| `GET` | `/api/users/{id}` | no | `get_user` | Fetch user by opaque numeric id |
| `GET` | `/api/users/{username}/chirps` | no | `user_chirps` | **NEW** — public user profile + chirps by username |
| `POST` | `/api/sessions` | no | `login` | Authenticate by handle; returns bearer token |
| `GET` | `/api/chirps` | no | `public_chirps` | **NEW** — public timeline with embedded author info |
| `POST` | `/api/chirps` | yes | `create_chirp` | Post a chirp as authenticated caller |
| `GET` | `/api/timeline` | yes | `timeline` | Authenticated home timeline |
| `GET` | `/api/public/timeline` | no | `public_timeline` | Older public timeline (cursor-based, no author embed) |
| `PUT` | `/api/users/{id}/follow` | yes | `follow` | Follow a user |
| `DELETE` | `/api/users/{id}/follow` | yes | `unfollow` | Unfollow a user |
| `PUT` | `/api/chirps/{id}/like` | yes | `like` | Like a chirp |
| `DELETE` | `/api/chirps/{id}/like` | yes | `unlike` | Unlike a chirp |

Unmatched paths fall through to the static/SPA fallback (serves `index.html`).

**Public endpoint status**: Both required public endpoints exist and are implemented:
- `GET /api/chirps` — public timeline with embedded author (the primary frontend endpoint)
- `GET /api/users/{username}/chirps` — public user profile + chirp list by username

The earlier `GET /api/public/timeline` endpoint also exists (opaque-cursor pagination,
no author embedding); it predates the logged-out feature and serves the older
`timeline_view` component.

---

## Backend: Data Models

### Core domain types (`crates/chirp-types/src/domain.rs`)

**`User`** — user account and public profile:
```
id:               UserId      (opaque, server-assigned integer; camelCase: "id")
username:         Username    (1–15 ASCII alphanumeric/underscore; camelCase: "username")
display_name:     String      (free-form; camelCase: "displayName")
bio:              Option<String>  (camelCase: "bio"; null when unset)
created_at:       Timestamp   (ms since Unix epoch; camelCase: "createdAt")
follower_count:   u64         (denormalized; camelCase: "followerCount")
following_count:  u64         (denormalized; camelCase: "followingCount")
```

**`Chirp`** — a single post:
```
id:        ChirpId          (opaque integer)
author_id: UserId           (camelCase: "authorId")
text:      ChirpText        (1–280 chars; validated on construction and serde)
created_at: Timestamp
like_count: u64              (camelCase: "likeCount")
reply_to:   Option<ChirpId> (camelCase: "replyTo"; null for top-level)
```

All JSON field names are `camelCase` (enforced by `#[serde(rename_all = "camelCase")]` on every type).

### Public (logged-out) API types (`crates/chirp-types/src/api.rs`)

These types serve the two new unauthenticated endpoints. They are defined in `chirp-types`
so both server and frontend share the identical wire contract.

**`PublicTimelineQuery`** — query params for `GET /api/chirps` and `GET /api/users/{username}/chirps`:
```
before: Option<i64>   — pagination cursor: ms-since-epoch of last seen chirp (omit for page 1)
limit:  Option<u32>   — page size 1–50; server default 20
```
Note: the external spec describes `before` as an ISO 8601 string; the implementation uses
milliseconds-since-epoch (consistent with the domain `Timestamp` type). This is a documented
spec deviation.

**`PublicChirp`** — one item in the public timeline:
```
id:         ChirpId (u64 wire)
content:    String
author:     PublicAuthor { username: String, display_name: Option<String> }
created_at: i64 (ms since Unix epoch)
like_count: u64 (camelCase: "likeCount")
```

**`PublicTimelineResponse`** — `GET /api/chirps` body:
```
chirps:   Vec<PublicChirp>   (reverse-chronological)
has_more: bool               (camelCase: "hasMore")
```

**`PublicUserProfile`** — user info embedded in user-chirps response:
```
username:     String
display_name: Option<String>  (camelCase: "displayName")
bio:          Option<String>
chirp_count:  u64             (camelCase: "chirpCount")
```

**`PublicUserChirp`** — one item in user-chirps response (no author embed; author is the profile subject):
```
id:         u64 (wire)
content:    String
created_at: i64
like_count: u64
```

**`PublicUserResponse`** — `GET /api/users/{username}/chirps` body:
```
user:     PublicUserProfile
chirps:   Vec<PublicUserChirp>  (reverse-chronological)
has_more: bool
```

---

## Backend: Auth Middleware

Authentication uses the `AuthUser` extractor pattern — not a tower middleware layer. It is
declared at the handler signature level:

```rust
// Requires auth — AuthUser extractor fires before handler body:
pub async fn create_chirp(
    AuthUser(author): AuthUser,
    State(state): State<AppState>,
    …
) -> Result<…, ServerError>

// No auth — no AuthUser in the signature:
pub async fn public_chirps(
    State(state): State<AppState>,
    Query(query): Query<PublicTimelineQuery>,
) -> Result<…, ServerError>
```

**How it works**: `AuthUser` implements `FromRequestParts`. When present in a handler's
argument list, axum calls it before invoking the handler. It reads the `Authorization: Bearer
<token>` header, resolves the token against the repository's `resolve_token` capability, and
either yields a `UserId` or short-circuits with `ServerError::Unauthorized` (HTTP 401).

**What public routes need**: Nothing beyond not declaring `AuthUser` in the handler signature.
There is no route-group or middleware configuration to modify — public endpoints simply omit
the extractor. The two new handlers (`public_chirps`, `user_chirps`) are already correctly
declared without `AuthUser`.

---

## Proposed Backend API Contract

The following API shapes are what was actually implemented (this is a record of the
as-built contract, not a proposal).

### `GET /api/chirps` — public timeline

| Attribute | Value |
|-----------|-------|
| Method | `GET` |
| Path | `/api/chirps` |
| Auth required | No |
| Handler | `handlers::public_chirps` |

**Query parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `before` | i64 (ms since epoch) | — | Return chirps created before this timestamp |
| `limit` | u32 | 20 | Page size; clamped 1–50 |

**Response (200 OK):**
```json
{
  "chirps": [
    {
      "id": 42,
      "content": "Hello, world!",
      "author": {
        "username": "alice",
        "displayName": "Alice A."
      },
      "createdAt": 1700000000000,
      "likeCount": 7
    }
  ],
  "hasMore": true
}
```

Pagination: request the next page by passing `before=<createdAt of last chirp>`.
`hasMore: false` signals end of list.

### `GET /api/users/{username}/chirps` — public user profile

| Attribute | Value |
|-----------|-------|
| Method | `GET` |
| Path | `/api/users/{username}/chirps` |
| Auth required | No |
| Handler | `handlers::user_chirps` |
| Path param | `username` — the user's handle (case-insensitive match) |

**Query parameters:** same `before` and `limit` as above.

**Response (200 OK):**
```json
{
  "user": {
    "username": "alice",
    "displayName": "Alice A.",
    "bio": "Engineer, reader.",
    "chirpCount": 42
  },
  "chirps": [
    {
      "id": 99,
      "content": "My latest thought.",
      "createdAt": 1700000000000,
      "likeCount": 3
    }
  ],
  "hasMore": false
}
```

**404 when username not found:**
```json
{
  "code": "NOT_FOUND",
  "message": "user not found"
}
```

---

## Frontend: Existing Structure

### Router registration (`crates/chirp-frontend/src/app.rs`)

The `Router` from `ferric-router` is assembled in `start()` via a builder chain:

```rust
let router = Router::new()
    .route("/",           move |_params| landing_view(&landing_ctx))       // NEW
    .route("/@:handle",   move |params| public_profile_view(&public_profile_ctx, handle)) // NEW
    .route("/signin",     move |_params| sign_in_view(&signin_ctx))        // NEW
    .route("/signup",     move |_params| signup_view(&signup_ctx))         // NEW (sign-up form)
    .route("/compose",    move |_params| compose_view(&compose_ctx))       // existing
    .route("/user/:id",   move |params| profile_view(&profile_ctx, params))// existing
    .route("/timeline",   move |_params| timeline_view(&timeline_ctx))     // existing
    .fallback(|_params| not_found_view())
    .mount_history();
```

The router uses history-API (HTML5 `pushState`) mode. Each `.route()` takes a path pattern
and a closure `|params| -> VNode`; the `:segment` syntax captures named parameters.

### App component structure

The application root renders:
1. A persistent `nav_bar()` (links: Chirp home, Compose, Create account `/signup`, Sign in `/signin`)
2. The router outlet (`router.outlet().render()`) — the route-matched component

Both are wrapped in a `<div class="chirp-app">` root.

Mount strategy: if `#app` already has child nodes (SSR markup present), `ferric::hydrate` is
called; otherwise `mount` is used for a fresh client-side mount.

### Shared application context (`AppContext`)

```rust
pub struct AppContext {
    pub base_url: String,              // "/api" by default; override via CHIRP_API_BASE_URL
    pub session: Signal<Option<Session>>,  // None = logged out
}
```

Every route view receives `&AppContext`. Logged-out views use `ctx.client()` without a token.
Authenticated views call `ctx.session.with(…)` to gate actions.

### Module layout (`crates/chirp-frontend/src/`)

| File | Route | Status |
|------|-------|--------|
| `app.rs` | — | Composition root; router; AppContext |
| `api.rs` | — | ApiClient; public API DTOs (frontend-side) |
| `landing.rs` | `/` | Public home and timeline — **NEW** |
| `public_profile.rs` | `/@:handle` | Public user profile — **NEW** |
| `sign_in.rs` | `/signin` | Sign-in form — **NEW** |
| `sign_up.rs` / `compose.rs` | `/signup` | Sign-up form (also exposes `compose_view`) — **NEW** |
| `timeline.rs` | `/timeline` | Authenticated home timeline |
| `profile.rs` | `/user/:id` | Authenticated user profile |
| `compose.rs` | `/compose` | Compose (authenticated) |
| `error.rs` | — | `AppError` type |

---

## Frontend: Ferric API Patterns

### VDOM building

```rust
VElement::new("section")
    .attr("class", "chirp-landing")
    .attr("role", "main")
    .child(some_vnode)
    .children(iter_of_vnodes)
    .key("unique-key")            // for keyed list reconciliation
    .on(EventKind::Click, || { }) // event handler (Fn() + 'static)
    .into()                       // VElement → VNode
```

Text nodes: `ferric::vdom::text("some string")` → `VNode`.

### Signals and reactive state

```rust
// Create a reactive signal
let sig: Signal<T> = create_signal(initial_value);

// Read (subscribes the current reactive scope to this signal)
let val: T = sig.get();

// Inspect without cloning (read-only borrow)
sig.with(|v| v.some_field.clone());

// Write (triggers re-render of subscribed scopes)
sig.set(new_value);
sig.update(|v| *v = v.wrapping_add(1));
```

### Reactive component pattern (thread_local + bump signal)

The idiomatic pattern for a view that owns async-loaded state is:

```rust
thread_local! {
    static MODEL: RefCell<MyModel> = const { RefCell::new(MyModel::new()) };
    static RERENDER: RefCell<Option<Signal<u32>>> = const { RefCell::new(None) };
    static STARTED: Cell<bool> = const { Cell::new(false) };
}

pub fn my_view(ctx: &AppContext) -> VNode {
    // Recreate the trigger each render; subscribe this render to it.
    let tick = create_signal(0u32);
    RERENDER.with(|cell| *cell.borrow_mut() = Some(tick));
    let _ = tick.get();  // subscribe

    // Kick off the first async load exactly once.
    STARTED.with(|s| {
        if !s.get() { s.set(true); kick_off_load(ctx.clone()); }
    });

    MODEL.with(|m| view_tree(&m.borrow()))
}

fn bump() {
    RERENDER.with(|cell| {
        if let Some(tick) = *cell.borrow() {
            tick.update(|n| *n = n.wrapping_add(1));
        }
    });
}

fn kick_off_load(ctx: AppContext) {
    wasm_bindgen_futures::spawn_local(async move {
        let result = ctx.client().some_api_call().await;
        MODEL.with(|m| m.borrow_mut().apply_result(result));
        bump();
    });
}
```

The `ROUTE_PATH` guard in `bump` avoids touching a disposed signal after the user navigates
away while a request is in-flight:

```rust
fn bump() {
    if current_path().as_str() != ROUTE_PATH { return; }
    // ... bump signal
}
```

### Async HTTP calls

`ApiClient` (in `crates/chirp-frontend/src/api.rs`) wraps `ferric_http::Client`:

```rust
Client::builder()
    .base_url(self.base_url.clone())
    .build()
    .get("/chirps")
    .query(&[("before", "1700000000000"), ("limit", "20")])
    .send_json::<PublicTimelineResponse>()
    .await
    .map_err(AppError::from_http)
```

The builder configures the base URL; each call adds path, query params, and optional JSON
body. The `Authorization: Bearer` header is added by `Client::builder().auth_token(token)` for
authenticated clients. Public endpoints explicitly omit the token even when a session is active.

### SSR + hydration

The entry point (`start()`) detects server-rendered content and chooses:
```rust
if root.has_child_nodes() {
    ferric::hydrate(root, app);  // attaches event handlers to existing DOM
} else {
    mount(root, app);            // fresh client-side render
}
```

---

## Proposed Frontend Structure

This section documents the actual structure that was implemented.

### Home / landing route

| Attribute | Value |
|-----------|-------|
| Path | `/` |
| Component | `landing_view` in `crates/chirp-frontend/src/landing.rs` |
| Data source | `GET /api/chirps?limit=20[&before=<cursor>]` |

**State machine:**

```
Initial render
    └─ loaded=false, error=None   → renders: "Loading…" spinner

Async fetch completes:
    success, 0 chirps
        └─ loaded=true, chirps.empty()  → renders: empty-state welcome + sign-up/sign-in CTA
    success, N chirps, has_more=true
        └─ loaded=true, chirps=[…], has_more=true  → renders: chirp list + "Load more" button
    success, N chirps, has_more=false
        └─ loaded=true, chirps=[…], has_more=false → renders: chirp list + "You're all caught up."
    failure (not yet loaded)
        └─ loaded=false, error=Some(e)  → renders: error banner + "Retry" button
    failure (continuation after first load)
        └─ loaded=true, error=Some(e)   → renders: chirp list + inline error + "Try again" button
```

Pagination cursor: `created_at` (ms since epoch) of the last chirp in the current page, passed
as `before` to fetch the next page.

Sign-up and sign-in links appear in every landing state via `header_nav()` (AC-4).

### Public user profile route

| Attribute | Value |
|-----------|-------|
| Path | `/@:handle` |
| Component | `public_profile_view` in `crates/chirp-frontend/src/public_profile.rs` |
| Data source | `GET /api/users/{handle}/chirps?limit=20[&before=<cursor>]` |

**States:** loading, not-found (HTTP 404), error (recoverable), empty (user exists, 0 chirps),
loaded (user profile + chirps), end-of-list.

The `:handle` parameter is captured from the router and passed into the view; when the handle
changes, the model resets and a new fetch is triggered.

### Sign-in route

| Attribute | Value |
|-----------|-------|
| Path | `/signin` |
| Component | `sign_in_view` in `crates/chirp-frontend/src/sign_in.rs` |
| Flow | Username form → `POST /api/sessions` → sets `AppContext::session` → redirect to `/` |

### Sign-up route

| Attribute | Value |
|-----------|-------|
| Path | `/signup` |
| Component | `signup_view` in `crates/chirp-frontend/src/compose.rs` |
| Flow | Username + display name + bio form → `POST /api/users` → `POST /api/sessions` → sets session → redirect |

### Navigation approach

The persistent nav bar (in `app.rs`) renders on every page:
```
Chirp · Compose · Create account · Sign in
```

The landing view additionally renders a `chirp-landing-nav` section at the top of the page
body with "Create account" and "Sign in" links, ensuring they remain visible regardless of
scroll position (AC-4).

---

## Implementation Notes for SUBTASK_backend

### Status

The backend implementation is complete on `work/chirp-logged-out`. The following changes were
made:

**Files modified:**
- `crates/chirp-server/src/api/router.rs` — added routes for `GET /api/chirps` and `GET /api/users/{username}/chirps`
- `crates/chirp-server/src/api/handlers.rs` — added `public_chirps` and `user_chirps` handlers
- `crates/chirp-types/src/api.rs` — added `PublicTimelineQuery`, `PublicChirp`, `PublicAuthor`, `PublicTimelineResponse`, `PublicUserProfile`, `PublicUserChirp`, `PublicUserResponse`
- `crates/chirp-server/src/repository/` — `public_chirps_with_authors` and `get_user_chirps_by_username` capabilities added to both `InMemoryRepository` and `PostgresRepository`

**Key design decisions already made:**
- Pagination cursor is `created_at` as milliseconds-since-epoch (not an opaque cursor string)
- Both endpoints accept the same `PublicTimelineQuery` (before, limit)
- Author data is embedded in `PublicChirp` (not a separate lookup)
- Username lookup in `user_chirps` is case-insensitive
- The spec's ISO 8601 `before` format was simplified to ms-epoch; this is a known deviation

### If further changes are needed

To add a new unauthenticated API endpoint:
1. Add handler function in `crates/chirp-server/src/api/handlers.rs` — no `AuthUser` extractor
2. Register the route in `build_router` in `crates/chirp-server/src/api/router.rs`
3. Add any new DTO types to `crates/chirp-types/src/api.rs`
4. Add repository capability to `ChirpRepository` trait (`crates/chirp-server/src/repository/mod.rs`), then implement in both `InMemoryRepository` and `PostgresRepository`

---

## Implementation Notes for SUBTASK_frontend

### Status

The frontend implementation is complete on `work/chirp-logged-out`. The following changes were
made:

**Files created:**
- `crates/chirp-frontend/src/landing.rs` — public home / timeline view
- `crates/chirp-frontend/src/public_profile.rs` — public user profile view
- `crates/chirp-frontend/src/sign_in.rs` — sign-in form

**Files modified:**
- `crates/chirp-frontend/src/app.rs` — added routes for `/`, `/@:handle`, `/signin`, `/signup`; added nav links
- `crates/chirp-frontend/src/api.rs` — added `ApiClient::public_timeline`, `ApiClient::public_user_profile`, and the public API DTO types
- `crates/chirp-frontend/src/compose.rs` — added `signup_view` function

**Ferric APIs used:**
- `ferric::prelude::*` — `VElement`, `VNode`, `create_signal`, `Signal`, `mount`, `EventKind`
- `ferric::vdom::text` — text nodes
- `ferric::hydrate` — SSR hydration
- `ferric_router::prelude::*` — `Router`, `link`, `current_path`
- `wasm_bindgen_futures::spawn_local` — launching async tasks
- `ferric_http::Client` — HTTP requests

**Pattern to follow for a new async view:**
1. Define a model struct with fields for all view states (loaded, error, data, pagination)
2. Store it in `thread_local! { static MODEL: RefCell<MyModel> }` with a bump-signal in `RERENDER`
3. Write pure reducer methods on the model (no DOM, unit-testable)
4. Kick off the initial load once via a `STARTED` guard
5. Spawn async fetch with `wasm_bindgen_futures::spawn_local`; call `bump()` after updating MODEL
6. Build the pure `view_tree(&model)` function that maps model state → VNode
7. Guard `bump()` with `current_path()` to avoid stale updates after navigation
