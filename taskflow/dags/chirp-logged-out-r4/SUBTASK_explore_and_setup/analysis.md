# Chirp Logged-Out — Codebase Analysis

## Branch Status

- **Branch**: `work/chirp-logged-out`
- **HEAD**: `908d7033ea3994236e129b6af5a2521a3037f098`
- **Status**: already existed (locally and on origin; local is up to date with `origin/work/chirp-logged-out`)

**Base-commit discrepancy**: The branch was created from `62febf5faf6023b3492365d246c7ac39c9f659a3`
(feat: SSR render_to_string + client-side hydration + Axum integration), not the planning-time base
`cb1ced3ffe6efc678d96a26ae16a63cb948d4237` (Merge PR #193: ferric-async-forms-r3). Both share
merge-base `62febf5`. The branch already contains 6 commits of logged-out visitor experience work
(AC-1–AC-5); implementation was in progress before this taskflow ran. The backend and frontend
spokes **MUST inspect the branch state** before modifying files — some items below may already be
present on the branch.

---

## Design Requirements Summary

### Key Screen States Required

**Public home/timeline (`/`, no session)**
- **Loading**: Skeleton `ChirpCard` rows at real dimensions; shell and explanatory hero render immediately on first paint — no layout jump when content arrives.
- **Empty** (no public content): Explanatory hero (what chirp is) + Sign up and Sign in actions; never a blank area.
- **Error** (failed load): Inline "couldn't load — try again" with retry; visibly distinct from empty; already-loaded content stays on screen; never a frozen screen.
- **End-of-list**: Load-older control at bottom; absent when no more items remain (no phantom spinner).

**Sign up (`/signup`)**
- **Empty**: Fresh form with labels/placeholders; `Create account` disabled; required-but-empty fields not shown as errors until touched.
- **Error**: `InlineError` per field — e.g. taken handle → "That handle's already taken — try another"; ill-formed handle → "Handles can use letters, numbers, and underscores, up to 15". Values preserved on failed submit.
- **Loading**: Handle availability check shows pending state.

**Sign in (`/signin`)**
- **Empty**: Labelled fields, no values, `Sign in` disabled.
- **Error**: Not-found and wrong-credential are distinguishable; neither reveals account existence beyond what public profile already shows; no raw system codes.

**All surfaces (REQ-UX-031 / BAR-260)**: Three visually distinct states — an explained empty block
(never blank), a loading skeleton (never a plain spinner), and an inline "couldn't load — try again"
error (never a frozen screen). Each is visibly different from the others.

### Route Names (from design docs — `experience-design.md` §1 IA)

| Screen | Route | Auth State |
|--------|-------|------------|
| Landing (public home/timeline) | `/` (no session) | signed-out |
| Sign up | `/signup` | signed-out |
| Sign in | `/signin` | signed-out |
| Public profile | `/@:handle` | both (signed-out & signed-in) |
| Recover access | `/recover` | signed-out |
| Set new credential | `/recover/confirm` | signed-out |
| Home timeline | `/` (session present) | signed-in |

**Note**: Current codebase uses `/user/:id` (integer `UserId`) for profiles. Design specifies
`/@:handle` (string handle as URL segment). Frontend will need to route `/@:handle`.

### BAR-011 Checklist Items (AC-1 through AC-5)

| AC | BAR | Type | Requirement |
|----|-----|------|-------------|
| AC-1 | BAR-006 | `automated_test` | Public profile viewable with no session (REQ-PROD-007) |
| AC-2 | BAR-026 | `manual_user_check` | Visitor with no account sees "what chirp is" + sign-up path (REQ-PROD-030) |
| AC-3 | BAR-028 | `manual_user_check` | Empty/loading/failed states show designed treatment, not blank/frozen (REQ-PROD-033) |
| AC-4 | BAR-200 | `manual_user_check` | Every signed-out screen carries Sign in + Sign up entries (REQ-UX-001) |
| AC-5 | BAR-260 | `manual_user_check` | Loading, empty, error, end-of-list states each visually distinct (REQ-UX-085/086, REQ-PROD-033/034) |

---

## chirp-server: Existing API Surface

### All Existing Routes

| Path | Method | Auth Required | Handler | Handler File |
|------|--------|---------------|---------|--------------|
| `/` | GET | no | `ssr_handler` | `crates/chirp-server/src/ssr.rs` |
| `/healthz` | GET | no | inline | `crates/chirp-server/src/api/router.rs` |
| `/readyz` | GET | no | inline | `crates/chirp-server/src/api/router.rs` |
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

**Note**: All `{id}` parameters use `UserId` (opaque integer). No endpoint accepts a string username as a path parameter.

### Does a public timeline GET exist?

**YES** — `GET /api/public/timeline` (no auth required).
- Handler: `handlers::public_timeline` — `State<AppState>` + `Query<TimelineQuery>`, no `AuthUser`.
- Response: `Page<Chirp>` → `{"items": [...], "nextCursor": "string | null"}`. Each `Chirp`: `id`, `authorId` (integer), `text`, `createdAt`, `likeCount`, `replyTo`.
- Pagination: `cursor` (opaque string) + `limit` query params; `nextCursor: null` signals last page; **no** `has_more` boolean.
- **Conflicts with the frozen spec** — see API Spec Verdict.

### Does a public user profile GET exist?

**NO.** The existing `GET /api/users/{id}` accepts an integer `UserId` only and returns a profile-only
`User` object (no chirps, no pagination). No endpoint accepts a string handle or returns
`{user, chirps, has_more}`. Must be added from scratch by SUBTASK_backend.

### Router Registration File

**`crates/chirp-server/src/api/router.rs`** — `pub fn build_router(state: AppState) -> Router`.
New routes are inserted into the `.route(path, method(handler))` chain before `.fallback_service(spa)`.

### Recommended New File for Public Handlers

Add new handlers into the existing `crates/chirp-server/src/api/handlers.rs` to keep the module
cohesive. If the file grows unwieldy, `crates/chirp-server/src/api/public_handlers.rs` is a natural
split point (requires `pub mod public_handlers;` in `api/mod.rs` and updated `use` in `router.rs`).

### Auth Extractor Type Name

- **Mandatory auth**: `AuthUser` (defined in `crates/chirp-server/src/api/auth.rs`)
  - `pub struct AuthUser(pub UserId)` — rejects missing/invalid tokens with HTTP 401 before handler body runs.
  - Pattern: `async fn handler(AuthUser(id): AuthUser, State(s): State<AppState>, ...) -> ...`
- **Optional auth**: **None exists.** No `OptionalAuthUser` / `MaybeAuthUser`. Public endpoints simply omit the `AuthUser` parameter entirely.
  - For the new spec endpoints (fully public, no auth required): do **NOT** add an `AuthUser` parameter.
  - For a future auth-aware endpoint (optional login): implement a new `OptionalAuthUser` extractor returning `Option<UserId>`.

### Persistence Types Used in Route Handlers

- **State type**: `AppState { pub repo: Arc<dyn ChirpRepository> }` (`crates/chirp-server/src/api/state.rs`). Cheap to clone; Axum clones per-request.
- **Repository trait**: `ChirpRepository` (`crates/chirp-server/src/repository/mod.rs`) — `async_trait` object-safe.
  - `public_timeline(&self, query: TimelineQuery) -> Result<Page<Chirp>, ServerError>` — **already exists**.
  - New method needed: `get_user_chirps_by_username(&self, username: &Username, before: Option<Timestamp>, limit: u32) -> Result<(User, Vec<Chirp>, bool), ServerError>` — **does not exist yet**.
- Implementations: `InMemoryRepository` (always) + `PostgresRepository` (behind `#[cfg(feature = "postgres")]`).
- Handler pattern: `state.repo.<method>(args).await?` → `Ok(Json(...))` or `Ok((StatusCode::CREATED, Json(...)))`.

---

## chirp-frontend: Existing Structure

### Router Registration File

**`crates/chirp-frontend/src/app.rs`** — `start()` function.

```rust
let router = Router::new()
    .route("/", move |_params| timeline_view(&timeline_ctx))
    .route("/compose", move |_params| compose_view(&compose_ctx))
    .route("/user/:id", move |params| profile_view(&profile_ctx, params))
    .fallback(|_params| not_found_view())
    .mount_history();
```

New routes: insert `.route(path, handler_closure)` before `.fallback(...)`. Each new view needs a
matching `AppContext` clone created in `start()` before the router chain.

### Existing Routes

| Route | View | File | Notes |
|-------|------|------|-------|
| `/` | `timeline_view` | `crates/chirp-frontend/src/timeline.rs` | Currently calls authenticated `ctx.client().timeline(...)`; needs to branch on session for public visitors |
| `/compose` | `compose_view` | `crates/chirp-frontend/src/compose.rs` | Dual-state: login form (logged-out) or compose form (logged-in) |
| `/user/:id` | `profile_view` | `crates/chirp-frontend/src/profile.rs` | Integer `id`; design spec wants `/@:handle` |
| (fallback) | `not_found_view` | `crates/chirp-frontend/src/app.rs` | 404 |

- **Existing sign-in route path**: **not found** — no `/signin`, `/sign-in`, or `/login` route.
- **Existing sign-up route path**: **not found** — no `/signup`, `/sign-up`, or `/register` route.
- **Existing home/landing route**: `/` → `timeline_view` (currently authenticated-only).

### API Call Pattern

- **HTTP client**: Custom `ApiClient` in `crates/chirp-frontend/src/api.rs`, wrapping `ferric_http::Client`. Not `reqwest`, not raw `web-sys` fetch.
- **Base URL**: `/api` (compile-time default via `option_env!("CHIRP_API_BASE_URL")`), stored in `AppContext.base_url`.
- **Auth**: Bearer token from `ctx.session.get().map(|s| s.token)` injected as default header when present. When `self.token` is `None`, requests are unauthenticated — the same `http_client()` builder is used for public endpoints.
- **Unauthenticated GET pattern**: `self.http_client().get("/path").send_json().await` (no token set when session is absent).
- **Error handling**: `AppError` → `Api(ApiError)` / `Network(String)` / `Transport(String)`. Use `err.user_message()` for display strings.
- **Missing methods**: No `public_timeline` or `public_user_profile` method on `ApiClient`. Both must be added.

### Component Module Layout

Flat, feature-based, all files directly under `crates/chirp-frontend/src/`:

| Module | File | Role |
|--------|------|------|
| `app` | `src/app.rs` | Router setup, `AppContext`, `start()`, nav bar |
| `api` | `src/api.rs` | `ApiClient` — single HTTP wrapper |
| `error` | `src/error.rs` | `AppError` unified error type |
| `timeline` | `src/timeline.rs` | Timeline view (`/`) |
| `compose` | `src/compose.rs` | Compose + login view (`/compose`) |
| `profile` | `src/profile.rs` | User profile view (`/user/:id`) |

Convention: `<feature>_view(ctx: &AppContext) -> VNode`. Add `pub mod <feature>;` in `lib.rs` for each
new module.

---

## Ferric Framework: Relevant APIs

### Resource API

**No `Resource<T, E>` type exists.** Ferric has no built-in reactive async data wrapper (unlike
Leptos/Solid's `create_resource`). Sources: `crates/ferric/src/signal.rs` (Signal),
`crates/ferric-http/src/` (HTTP client).

**Idiomatic pattern** — `Signal<Option<Result<T, E>>>` + `spawn_local`:

```rust
use ferric::prelude::*;
use ferric_http::Client;
use wasm_bindgen_futures::spawn_local;

// State machine:
//   None           → Loading
//   Some(Err(e))   → Error
//   Some(Ok(resp)) → Loaded (empty when resp.chirps.is_empty())
let state: Signal<Option<Result<PublicTimelineResponse, String>>> = create_signal(None);

let state_writer = state;
spawn_local(async move {
    let client = Client::builder().base_url("/api").build();
    match client.get("/chirps").send_json::<PublicTimelineResponse>().await {
        Ok(resp) => state_writer.set(Some(Ok(resp))),
        Err(e)   => state_writer.set(Some(Err(e.to_string()))),
    }
});

// In render closure:
match state.get() {
    None             => loading_skeleton(),
    Some(Err(msg))   => error_banner_with_retry(msg),
    Some(Ok(r)) if r.chirps.is_empty() => empty_hero_with_cta(),
    Some(Ok(r))      => chirp_list_with_pagination(r),
}
```

### Router API

Import: `use ferric_router::prelude::*;`  
Sources: `crates/ferric-router/src/router.rs`, `crates/ferric-router/src/matcher.rs`,
`crates/ferric-router/src/link.rs`.

```rust
let router = Router::new()
    .route("/", |_| landing_view())              // public home / logged-out landing
    .route("/signin", |_| sign_in_view())
    .route("/signup", |_| sign_up_view())
    .route("/@:handle", |params| {
        let handle = params.get("handle").unwrap_or("").to_string();
        public_profile_view(handle)
    })
    .fallback(|_| not_found_view())
    .mount_history();                            // seeds path from window.location; popstate listener

let outlet = router.outlet();                   // consumes Router into Component
mount(root, app);
```

Programmatic navigation: `navigate("/path")` (pushState, back-button works),
`navigate_replace("/path")` (replaceState, no back entry — use for login redirects).  
In-app links: `link("/about", "About")` → `<span role="link" data-to="/about">` (adds
`aria-current="page"` on match).  
Route params: `params.get("key") -> Option<&str>`.

### SSR Recommendation

**Do NOT use SSR for the public timeline in this iteration.**

1. `crates/ferric/src/ssr.rs` and `crates/ferric/src/hydrate.rs` are "walking skeleton" with `todo!()` stubs — not production stable.
2. SSR requires the Axum server binary to call into ferric's native build in the hot request path, introducing cross-compilation requirements and a new failure mode.
3. The public timeline is async data; SSR would render a loading skeleton that immediately mismatches on client hydration — paying full SSR cost for zero first-paint benefit.
4. CSR with `spawn_local` + `Signal<Option<Result<T,E>>>` is correct for this feature.
5. Add SSR later as an optimization if SEO or FCP metrics require it. The API (`render_to_string` / `hydrate`) is stable.

### Hydration API (reference only)

If SSR is added later:
```rust
// Server: use ferric::render_to_string;
let html = render_to_string(|| my_component());

// Client (wasm32): use ferric::hydrate;
hydrate(root_element, || my_component());
```

Sources: `crates/ferric/src/ssr.rs` (server), `crates/ferric/src/hydrate.rs` (wasm32 only).

---

## API Spec Verdict

### Existing public timeline endpoint: **CONFLICT**

| Dimension | Frozen spec (`GET /api/chirps`) | Existing (`GET /api/public/timeline`) |
|-----------|----------------------------------|---------------------------------------|
| Path | `GET /api/chirps` | `GET /api/public/timeline` |
| Auth | none | none ✓ |
| Chirp body field | `content` | `text` |
| Author representation | embedded `{username, display_name}` | `authorId` (integer only) |
| Response wrapper key | `chirps` (array) | `items` (array) |
| Pagination signal | `has_more: bool` | `nextCursor: string \| null` |
| Pagination cursor param | `before` (ISO 8601 timestamp) | `cursor` (opaque string) |

**Recommendation**: Add `GET /api/chirps` as a **new route** implementing the spec shape.
Leave `GET /api/public/timeline` unchanged for existing consumers. Both coexist.

### Existing public user profile endpoint: **ABSENT**

No endpoint of this form exists. Must be added from scratch.

### Pagination approach (`before` + `has_more`): **INCONSISTENT with existing**

New spec endpoints use `before` (ISO 8601 timestamp query param) + `has_more: bool` (response).  
Existing endpoints use `cursor` (opaque string) + `nextCursor: string | null`.  
Both are cursor-based / reverse-chronological; wire contract differs.  
**Rule**: New spec endpoints use spec shape; existing endpoints retain their cursor scheme.

### Recommended final endpoint paths for SUBTASK_backend

| Endpoint | Path | Shape | Status |
|----------|------|-------|--------|
| Public timeline | `GET /api/chirps` | Spec shape (new route, new DTOs) | Add as new route |
| Public user profile + chirps | `GET /api/users/:username/chirps` | Spec shape (new route, new DTOs, new repo method) | Add from scratch |

---

## Implementation Guidance for SUBTASK_backend

### Files to Modify

| File | Change |
|------|--------|
| `crates/chirp-types/src/api.rs` | Add new response DTOs: `PublicChirp { id, content, author: PublicAuthor, created_at, like_count }`, `PublicAuthor { username, display_name }`, `PublicTimelineResponse { chirps: Vec<PublicChirp>, has_more: bool }`, `PublicUserResponse { user: PublicUserProfile, chirps: Vec<PublicUserChirp>, has_more: bool }`, `PublicUserProfile { username, display_name, bio, chirp_count }`, `PublicUserChirp { id, content, created_at, like_count }` |
| `crates/chirp-server/src/repository/mod.rs` | Add `ChirpRepository` trait method: `get_user_chirps_by_username(&self, username: &Username, before: Option<Timestamp>, limit: u32) -> Result<(User, Vec<Chirp>, bool), ServerError>` |
| `crates/chirp-server/src/repository/in_memory.rs` | Implement the new trait method |
| `crates/chirp-server/src/repository/postgres.rs` | Implement the new trait method (behind `#[cfg(feature = "postgres")]`) |
| `crates/chirp-server/src/api/handlers.rs` | Add `public_chirps` handler (unauthenticated `GET /api/chirps`) and `user_chirps` handler (unauthenticated `GET /api/users/:username/chirps`); both omit `AuthUser` parameter entirely |
| `crates/chirp-server/src/api/router.rs` | Register two new routes: `.route("/api/chirps", get(handlers::public_chirps))` and `.route("/api/users/{username}/chirps", get(handlers::user_chirps))` |

### Auth Extractor Guidance

New spec endpoints are **fully public** — do **NOT** add `AuthUser` to their handler parameters.
Use only `State<AppState>` + `Query<SpecQueryParams>`.

The two auth states in this codebase are binary:
- Authenticated: `AuthUser(user_id): AuthUser` as a handler parameter (HTTP 401 on absent/invalid token).
- Unauthenticated: no auth parameter at all (no token inspection).

For future auth-aware endpoints (optional login): implement a new `OptionalAuthUser` extractor
returning `Option<UserId>`.

### Path Parameter Notes

`GET /api/users/{username}/chirps` uses a string `username` segment followed by `/chirps` suffix.
This is structurally distinct from `GET /api/users/{id}` (integer `id`, no suffix). Axum routes by
suffix match; no collision. Use `Path<String>` or `Path<Username>` for the `{username}` segment.

---

## Implementation Guidance for SUBTASK_frontend

### Files to Create

| File | Purpose |
|------|---------|
| `crates/chirp-frontend/src/sign_in.rs` | Standalone sign-in page at `/signin` — `sign_in_view(ctx: &AppContext) -> VNode` |
| `crates/chirp-frontend/src/sign_up.rs` | Sign-up / registration page at `/signup` — `sign_up_view(ctx: &AppContext) -> VNode` |
| `crates/chirp-frontend/src/landing.rs` | Public home page for logged-out `/` visitors — `landing_view(ctx: &AppContext) -> VNode` (see Option B below) |
| `crates/chirp-frontend/src/public_profile.rs` | Public user profile at `/@:handle` — `public_profile_view(ctx: &AppContext, handle: String) -> VNode` |

Declare each with `pub mod <module>;` in `crates/chirp-frontend/src/lib.rs`.

### Files to Modify

| File | Change |
|------|--------|
| `crates/chirp-frontend/src/app.rs` | (1) Add route registrations for `/signin`, `/signup`, `/@:handle`, and `/` landing (or session-branch on `/`); (2) Add "Sign in" and "Sign up" nav entries in the signed-out shell (the nav bar lives here); (3) Create `AppContext` clones for each new view in `start()` |
| `crates/chirp-frontend/src/lib.rs` | Add `pub mod sign_in;`, `pub mod sign_up;`, `pub mod landing;`, `pub mod public_profile;` |
| `crates/chirp-frontend/src/api.rs` | Add `public_timeline(&self, before: Option<&str>, limit: u32) -> Result<PublicTimelineResponse, AppError>` calling `GET /chirps`; add `public_user_profile(&self, username: &str, before: Option<&str>, limit: u32) -> Result<PublicUserResponse, AppError>` calling `GET /users/{username}/chirps` |

### Suggested Component Structure for the Home/Landing Route

The `/` route currently dispatches to `timeline_view` which calls the authenticated `timeline` API.
Two approaches:

**Option A — Branch in `timeline.rs`** (smaller diff):
```rust
// In timeline_view:
match ctx.session.get() {
    None     => public_landing_panel(&ctx),  // spawn_local + GET /chirps (no auth)
    Some(_)  => authenticated_timeline_panel(&ctx),  // existing authenticated call
}
```

**Option B — New `landing.rs` + updated router** (recommended — cleaner separation):
Route `/` to `landing_view` for all visitors; inside `landing_view` branch on session:
```rust
// In landing_view:
match ctx.session.get() {
    None    => public_home(&ctx),   // public timeline + hero
    Some(_) => navigate_replace("/timeline_or_home"), // redirect to signed-in experience
}
```
Or register two routes sharing the `/` path with session-aware dispatch in the closure:
```rust
.route("/", move |_params| {
    if ctx_clone.session.get().is_some() {
        timeline_view(&timeline_ctx_clone)
    } else {
        landing_view(&landing_ctx_clone)
    }
})
```

Recommendation: **Option B** — the two panels have different data sources (authenticated timeline vs
public `GET /api/chirps`), different nav shells (signed-in vs signed-out), and different empty states.
Keeping them in separate files matches the flat module convention.

**Public landing panel structure**:
1. `Signal<Option<Result<PublicTimelineResponse, String>>>` initialized to `None`.
2. `spawn_local` to `GET /chirps?limit=20` (no auth token).
3. Match signal: `None` → loading skeleton; `Some(Err(msg))` → "couldn't load — try again" + retry; `Some(Ok(r))` where `r.chirps.is_empty()` → explanatory hero with "what chirp is" + Sign up / Sign in actions; `Some(Ok(r))` → chirp list + load-older control (if `r.has_more`).
4. Hero/explanatory block visible in ALL states (loading, empty, error, populated) per BAR-200 (AC-4): every signed-out screen carries Sign in + Sign up entries.
5. Use `navigate("/signup")` and `navigate("/signin")` for the CTA action buttons.

### Suggested Component Structure for the User Profile Route

New route: `/@:handle` (at-sign prefix, string handle).

```rust
// In app.rs start():
let public_profile_ctx = ctx.clone();
// ...
.route("/@:handle", move |params| {
    let handle = params.get("handle").unwrap_or("").to_string();
    public_profile_view(&public_profile_ctx, handle)
})
```

Component structure for `public_profile_view`:
1. `Signal<Option<Result<PublicUserResponse, String>>>` initialized to `None`.
2. `spawn_local` to `GET /users/{handle}/chirps?limit=20` (no auth).
3. Match signal: `None` → skeleton header + skeleton feed; `Some(Err(msg))` → error with retry; `Some(Ok(r))` → profile header + chirp list.
4. Profile header: `r.user.display_name`, `r.user.username` (`@handle`), `r.user.bio`, `r.user.chirp_count`.
5. Chirp list: show each `r.chirps[i]` as a card (content, created_at, like_count). If `r.has_more`, append a load-older button that triggers a second `spawn_local` with `before=last_chirp.created_at`.
6. Per BAR-200 (AC-4): public profile pages are signed-out screens and MUST carry Sign in + Sign up entries in the nav shell.

**Route parameter note**: Ferric-router parses `/@:handle` by matching the literal `/@` prefix on the
path segment, then extracting `:handle` as the remaining text. Use `params.get("handle")` to read it.
Verify the router handles the leading `/@` correctly in the existing version; if not, consider `/profile/:handle` as a fallback path (adjusting the design route).
