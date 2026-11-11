# Codebase Gap Analysis — Chirp Logged-Out Visitor Experience

Synthesized from design, backend, frontend, and Ferric surveys of `Nousix-LLC/nswe-demo`
`main` at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`.

---

## 1. Branch Status

Branch `work/chirp-logged-out` exists on the remote repository.
It was created from commit `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
(the `main` commit that includes PRs #193, #203, and #228 — the full Ferric async + router +
SSR/hydration stack). `cb1ced3` is confirmed as a git ancestor of the branch tip.

---

## 2. API Endpoint Survey

### Auth Middleware Pattern

There is **no** global auth middleware layer in the router. `build_router` applies only
`TraceLayer::new_for_http()` (request tracing). Authentication is opt-in per handler: a handler
that includes `AuthUser` as a parameter requires a valid `Bearer` token; a handler that omits it
is fully public. This means adding or removing auth on an endpoint requires only adding or removing
the `AuthUser` extractor argument — no middleware reconfiguration.

### Public Timeline Endpoint

**Status: EXISTS — no changes needed.**

| Property | Value |
|---|---|
| URL | `GET /api/chirps` |
| Handler | `public_chirps` in `src/api/handlers.rs` |
| Auth | None (no `AuthUser` extractor) |
| Response type | `PublicTimelineResponse { chirps: Vec<PublicChirp>, has_more: bool }` |
| `PublicChirp` fields | `id: ChirpId`, `content: String`, `author: PublicAuthor { username, display_name }`, `created_at: i64` (ms epoch), `like_count: u64` |
| Pagination | `before` cursor (timestamp, optional) + `limit` (1–50, default 20) |
| Empty list | Returns `{ chirps: [], has_more: false }` — not an error |

The `public_chirps` handler uses `public_chirps_with_authors` to embed the author username
directly in each chirp. All fields required by the public API contract are present.

**Note on `GET /api/public/timeline`**: a second unauthenticated timeline endpoint exists but
returns `Page<Chirp>` with only `author_id` (no username). It does not satisfy the contract.
`GET /api/chirps` is the correct endpoint.

**Recommendation**: Reuse `GET /api/chirps` as-is. No backend changes needed for the public timeline.

### Public User Profile Endpoint

**Status: EXISTS — no changes needed.**

| Property | Value |
|---|---|
| URL | `GET /api/users/{username}/chirps` |
| Handler | `user_chirps` in `src/api/handlers.rs` |
| Auth | None (no `AuthUser` extractor) |
| Response type | `PublicUserResponse { user: PublicUserProfile, chirps: Vec<PublicUserChirp>, has_more: bool }` |
| `PublicUserProfile` fields | `username: String`, `display_name: Option<String>`, `bio: Option<String>`, `chirp_count: u64` |
| `PublicUserChirp` fields | `id: ChirpId`, `content: String`, `created_at: i64`, `like_count: u64` |
| Path param | `{username}` — string, case-insensitive lookup |
| Not-found | Returns `ServerError::NotFound` → HTTP 404 for unknown usernames |

**Recommendation**: Reuse `GET /api/users/{username}/chirps` as-is. No backend changes needed.

---

## 3. Frontend Route Survey

### Router Configuration

Ferric router (`ferric-router`) in `crates/chirp-frontend/src/app.rs`. Uses HTML5 History API
(`Router::mount_history()`). Routes resolve first-match-wins in declaration order.

**Registered routes at `cb1ced3`:**

| Path | Handler | Auth gate | Logged-out visitor sees |
|------|---------|-----------|------------------------|
| `/` | `timeline_view` | None | Full timeline; loading/error/empty/paginated states |
| `/compose` | `compose_view` | View-level (checks `ctx.session`) | Login form with handle + "Log in" button |
| `/user/:id` | `profile_view` | None (actions gated) | Profile card + "Log in to follow/like" hints |
| `*` | `not_found_view` | None | Static 404 panel |

### Home / Landing Route (`/`)

`timeline_view` is not auth-gated. When `ctx.session` is `None`, the view makes the API request
without a bearer token. **However, the current API call target is `GET /api/timeline` (the
authenticated home timeline endpoint), which returns 401 for unauthenticated requests.**

The public API endpoint `GET /api/chirps` is not currently called by `timeline_view`. Switching
to the correct endpoint is the primary frontend backend-integration gap.

Existing state coverage in `timeline_view`:
- Loading: spinner ("Loading timeline…")
- Error: `error_banner(err)` + "Retry" button (in-place refetch via `create_resource` counter)
- Empty: "No chirps yet." — no CTA, no context
- Content: keyed `<ul>` of chirp items; no profile links; author shown as raw numeric `author_id`
- End-of-list: footer text ("End of timeline" or equivalent) after last page

### User Profile Route (`/user/:id`)

The profile route uses a **numeric `UserId`** path parameter. There is no `/user/:username` or
handle-based route. The public backend endpoint uses `username` for lookup, but the frontend
route uses `id`. Since chirp items do not emit profile links, the profile route is currently
unreachable in normal navigation.

Logged-out visitors see the full profile card (display name, `@handle`, bio, follower/following
counts). Follow and like controls degrade to informational hints for logged-out visitors.

### Nav Bar

The persistent nav bar renders "Timeline · Compose" for every visitor regardless of session state.
It carries no Sign up, Sign in, or user identity indicator.

---

## 4. Ferric Primitives Available

### Async Resource Primitives (`crates/ferric/src/async_resource.rs` — PR #193)

| Primitive | Description |
|---|---|
| `ResourceState<T>` | Three-state enum: `Loading`, `Ready(T)`, `Failed(String)` |
| `Resource<T>` | Reactive handle; `.state()` reads current state reactively inside effects/memos |
| `Resource::new(fut)` | One-shot fallible fetch (panics on error — use `new_fallible` for recoverable errors) |
| `Resource::new_fallible(fut)` | One-shot; maps `Err` → `Failed(String)` |
| `create_resource(source, fetcher)` | Reactive re-fetch; re-runs `fetcher` when `source` signal changes; generation counter prevents stale responses |
| `suspense(fallback, children)` | Shows fallback while any `Resource` inside children is `Loading` |

### Four-State Component Pattern

The idiomatic pattern for a data-fetching component with all four states:

```rust
let refresh = create_signal(0_u32);
let data: Resource<Result<Vec<T>, String>> = create_resource(
    move || refresh.get(),
    |_gen| async move { fetch().await },
);
let on_retry = move || refresh.set(refresh.get() + 1);

suspense(
    || loading_skeleton(),
    move || match data.state() {
        ResourceState::Loading      => refreshing_indicator(),
        ResourceState::Failed(msg)  => error_panel(msg),   // defensive
        ResourceState::Ready(Err(m))=> error_panel_with_retry(m, on_retry),
        ResourceState::Ready(Ok(v)) if v.is_empty() => empty_state(),
        ResourceState::Ready(Ok(v)) => content_view(v),
    },
)
```

The `suspense` fallback covers the **initial load** (shown until first `Ready` or `Failed`).
The inner `Loading` arm handles **re-fetches** (while already rendered after a Retry click).
The `on_retry` closure increments `refresh`, which `create_resource` observes and re-fetches.

### SSR and Hydration Support (PR #228)

| Capability | Status |
|---|---|
| `ferric::render_to_string(f)` | Server: renders component to HTML string; always compiled |
| `ferric::hydrate(root, f)` | Client: adopts server-rendered DOM, wires event handlers (wasm32 only) |
| Event handlers in SSR | Silently dropped; interactivity requires WASM hydration |
| Pre-fetched data serialization | **Not yet** — deferred to BAR-005 / issue #225 |

**SSR behavior for async resources**: `render_to_string` runs all `Resource` calls in their
initial `Loading` state. The suspense fallback HTML is what the server emits. The client
re-fetches after hydration. This means a brief loading flash on page load is expected and
intentional; the loading skeleton should be designed for this transition.

### Gaps and Limitations Relevant to This Feature

| Gap | Impact |
|---|---|
| No pre-fetched data serialization | Client always re-fetches after hydration; loading state always shown initially |
| `ferric-router` link is `<span>` not `<a href>` | No right-click → open-in-new-tab; no SEO-crawlable links |
| `suspense` not SSR-aware | Loading skeleton is always the server-rendered output |
| No SSR-aware route renderer | Server-side route resolution requires manual wiring |

---

## 5. Per-AC Gap Analysis

### AC-1 — Unauthenticated timeline and profile reading (REQ-PROD-013 / BAR-011)

**Requirement**: A logged-out visitor can read the public timeline and user profiles without
signing in.

| What exists | What must change |
|---|---|
| `GET /api/chirps` exists, unauthenticated, returns timeline with embedded author | Frontend `timeline_view` currently calls the authenticated `GET /api/timeline` endpoint; must switch to `GET /api/chirps` |
| `GET /api/users/{username}/chirps` exists, unauthenticated | Frontend profile route uses numeric `UserId`, not username; must add `/user/:username` route or update existing route to username-based param |
| Frontend `/` route is not auth-gated | Chirp items render raw numeric `author_id` with no link; must render `@handle` and link to profile |
| Frontend `/user/:id` route is not auth-gated | No existing mechanism to navigate to a profile from the timeline; profile links must be added to chirp items |

**Task ownership**: SUBTASK_backend-api confirms/documents the endpoints; SUBTASK_frontend-ui
fixes the API call target, adds profile links, and updates the profile route.

---

### AC-2 — Useful empty-state landing (REQ-PROD-014 / BAR-011)

**Requirement**: First screen shows either real content or a clear statement of what chirp is
with a prominent sign-up / sign-in action — never a blank page or spinner with no exit.

| What exists | What must change |
|---|---|
| `timeline_view` has an `empty` state branch | Empty state renders only "No chirps yet." — no CTA, no context, no "what chirp is" copy |
| Nav bar renders on every page | Nav bar has no Sign up / Sign in links for logged-out visitors |

**What to add**:
- Empty state: one-line "what chirp is" statement + "be the first" copy + prominent **Create account** button/link (→ `/signup`) + **Sign in** link (→ `/signin`)
- Nav bar: persistent **Sign up** and **Sign in** links on all logged-out surfaces

**Task ownership**: SUBTASK_frontend-ui

---

### AC-3 — Recoverable timeline error state (REQ-PROD-014 / BAR-011)

**Requirement**: Timeline failure shows a plain, honest message and a **Try again** that
refetches without a full-page reload.

| What exists | What must change |
|---|---|
| `timeline_view` has error state: `error_banner(err)` + "Retry" button | Retry mechanism uses `create_resource` counter — in-place refetch already works |
| `AppError::user_message()` for user-facing text | Verify error message copy is plain language (not raw HTTP status codes or Rust panics) |
| Nav chrome remains visible during error | No change needed |

**What to add**: Only UX copy polish may be needed. The in-place retry mechanism is already
correct. Confirm the error banner message is "plain, honest" (e.g. "Couldn't load the timeline.
Check your connection and try again." — not "401 Unauthorized" or "NetworkError").

**Task ownership**: SUBTASK_frontend-ui (copy verification + minor polish)

---

### AC-4 — Visible "create an account" route (REQ-PROD-015 / BAR-011)

**Requirement**: "Create an account" is visible on the landing and on the sign-in screen;
following it reaches sign-up.

| What exists | What must change |
|---|---|
| `ApiClient::create_user` method exists | No `/signup` route exists in the router |
| `compose_view` embeds a login form for logged-out visitors | No `/signin` route; login is embedded in `/compose` only — a logged-out visitor on `/` has no visible path to sign in |
| Nav bar always rendered | Nav bar has no Sign up / Sign in links |

**What to add**:
- `/signin` route: standalone sign-in form + "Create an account" link → `/signup`
- `/signup` route: sign-up form + "Sign in" link → `/signin`
- Nav bar: **Sign up** (→ `/signup`) and **Sign in** (→ `/signin`) visible on every logged-out surface
- The existing login form in `compose_view` can be extracted or repurposed

**Task ownership**: SUBTASK_frontend-ui

---

### AC-5 — Visually distinct loading / empty / error / end-of-list states (REQ-UX-032 / BAR-011)

**Requirement**: All four states render distinctly; none is a blank page or stale view.
`loading` state uses shape-matched skeleton placeholders.

| State | What exists | What must change |
|---|---|---|
| `loading` | "Loading timeline…" text spinner | Replace with shape-matched skeleton cards matching chirp card geometry; nav chrome must remain usable |
| `content` | Keyed chirp list with like count + timestamp | Add `@handle` link to profile; show display name. Satisfies `content` state. |
| `empty` | "No chirps yet." | Must be redesigned: "what chirp is + be the first" copy + Create account CTA |
| `error` | `error_banner(err)` + "Retry" in-place | Verify plain-language copy; already structurally correct |
| `end_of_list` | Footer after last page | Must be visually distinct from `empty` — explicit "you're all caught up" (or equivalent) marker |

The one-state-model vocabulary (`loading`, `content`, `empty`, `error`, `end_of_list`) is
already largely implemented in `timeline_view`. The state **transitions** are correct; the
**content** of the empty and loading states needs redesign.

**Task ownership**: SUBTASK_frontend-ui

---

## 6. Implementation Plan Summary

### SUBTASK_backend-api — `crates/chirp-server/`

**No new endpoints needed.** Both required public API endpoints already exist and satisfy the
contract declared in `contracts/public_api_contract.md`:

| Endpoint | Handler file | Action |
|---|---|---|
| `GET /api/chirps` | `src/api/handlers.rs` (`public_chirps`) | Document as-is in `backend-impl.md` |
| `GET /api/users/{username}/chirps` | `src/api/handlers.rs` (`user_chirps`) | Document as-is in `backend-impl.md` |

The task should read the existing handler implementations, confirm the response shapes match the
contract, and produce `backend-impl.md` with the confirmed URL patterns and type shapes.
No handler, route, or auth changes required.

---

### SUBTASK_frontend-ui — `crates/chirp-frontend/`

The following files require changes. No new crates are needed.

| File | Changes required |
|---|---|
| `src/api.rs` | Add `pub_timeline(before, limit)` calling `GET /api/chirps`; add `pub_user_profile(username, before, limit)` calling `GET /api/users/{username}/chirps`; add `PublicTimelineResponse`, `PublicChirp`, `PublicUserResponse`, `PublicUserProfile`, `PublicUserChirp` wire types |
| `src/app.rs` | Update nav bar to include **Sign up** (→ `/signup`) and **Sign in** (→ `/signin`) for logged-out visitors; register `/signin` and `/signup` routes; update or add `/user/:username` route (username-based, not numeric ID) |
| `src/timeline.rs` | Switch timeline fetch from `GET /api/timeline` to `GET /api/chirps` using `pub_timeline`; update chirp items to render `@author.username` as a link to `/user/{username}`; redesign `loading_view` to skeleton placeholders; redesign `empty_view` to include "what chirp is" copy + Create account CTA; update end-of-list marker text to "You're all caught up" (or equivalent); verify error message is plain language |
| `src/profile.rs` | Update route handler signature to accept `username: String` from params (not numeric `u64`); switch API call to `pub_user_profile(username)`; add `not_found` state using `message_view`; update any profile URL generation to username-based |
| `src/signin.rs` *(new)* | Standalone sign-in route view: handle + password form, login action, "Create an account" link → `/signup`; reuse or extract the existing login form from `compose_view` |
| `src/signup.rs` *(new)* | Standalone sign-up route view: handle + password form, `ApiClient::create_user` action, "Sign in" link → `/signin` |
