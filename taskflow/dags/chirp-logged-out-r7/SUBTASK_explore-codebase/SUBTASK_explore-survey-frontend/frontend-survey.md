# Frontend Route Survey — chirp-frontend

Surveyed codebase: `Nousix-LLC/nswe-demo`, `main` at `cb1ced3`.

---

## 1. Crate Structure

**Crate root**: `crates/chirp-frontend/`

### Top-level file layout

```
crates/chirp-frontend/
├── Cargo.toml
└── src/
    ├── lib.rs       — module root; re-exports `app::start`
    ├── app.rs       — composition root: Session, AppContext, router, nav, WASM mount
    ├── api.rs       — typed async REST client (ApiClient)
    ├── compose.rs   — /compose route: login form (logged-out) + compose form (logged-in)
    ├── error.rs     — AppError: single UI error type
    ├── profile.rs   — /user/:id route: user profile + follow/like actions
    └── timeline.rs  — / route: paginated chirp timeline
```

### Cargo.toml dependencies (abbreviated)

```toml
[package]
name = "chirp-frontend"
# build target: wasm32-unknown-unknown

[dependencies]
ferric          = { path = "../ferric" }          # UI framework (signals + VNode + mount/hydrate)
ferric-router   = { path = "../ferric-router" }   # client-side router (HTML5 history)
ferric-http     = { path = "../ferric-http" }      # Fetch API wrapper
chirp-types     = { path = "../chirp-types" }      # shared wire DTOs (User, Chirp, SessionToken, …)
serde_json      = { workspace = true }
wasm-bindgen    = { workspace = true }
wasm-bindgen-futures = "0.4"
js-sys          = { workspace = true }
web-sys         = { workspace = true, features = [...] }
```

All Ferric crates and `chirp-types` are workspace-local path dependencies — no external UI framework. The build target is `wasm32-unknown-unknown`; native (`std`) builds are supported for the unit-test suites only (browser-only calls are `#[cfg(target_arch = "wasm32")]`-gated).

The module-docstrings throughout note this is a "walking skeleton": route modules are real implementations, not stubs, but the per-spoke feature work is expected to extend them.

---

## 2. Router Configuration

**File**: `crates/chirp-frontend/src/app.rs`, function `start()`

### Registration pattern

The Ferric router is configuration-based: all routes are registered inline in a fluent builder chain, then activated with `.mount_history()` (HTML5 History API pushState). There are no file-system route conventions.

```rust
let router = Router::new()
    .route("/", move |_params| timeline_view(&timeline_ctx))
    .route("/compose", move |_params| compose_view(&compose_ctx))
    .route("/user/:id", move |params| {
        profile_view(&profile_ctx, params)
    })
    .fallback(|_params| not_found_view())
    .mount_history();
```

Each route handler receives a cloned `AppContext` (the shared reactive context) captured at registration time. The `AppContext` holds:

- `base_url: String` — relative API base URL (default `/api`, overridable via `CHIRP_API_BASE_URL` env var at build time)
- `session: Signal<Option<Session>>` — reactive signal initialized to `None` (logged-out)

### Authentication guards

**There are none at the router level.** Every route is reachable by any visitor regardless of session state. Authentication gating — where it exists — is performed inside the view function by checking `ctx.session`.

### Persistent nav bar

Rendered above the router outlet on every route:

```rust
fn nav_bar() -> VNode {
    // links: "Timeline" (/) · "Compose" (/compose)
}
```

The nav bar links only to `/` and `/compose`. It carries no user identity indicator, no login link, and no logout control.

### WASM mount / SSR hydration

```rust
if root.has_child_nodes() {
    ferric::hydrate(root, app);  // SSR hydration path
} else {
    mount(root, app);            // fresh client-side mount
}
```

Mounts into `#app` or falls back to `<body>`.

---

## 3. Route Inventory

| Path | Handler | Auth gate | Logged-out visitor sees |
|------|---------|-----------|------------------------|
| `/` | `timeline_view` | None | Full timeline: loading spinner → paginated chirp list (or empty state / error banner). No login prompt. |
| `/compose` | `compose_view` | Conditional (view-level) | Login form with handle input and "Log in" button. Not redirected; content changes. |
| `/user/:id` | `profile_view` | None (actions gated) | Full profile card (display name, @handle, bio, follower/following counts) + inline hints "Log in to follow this user." and "Log in to like chirps." Action buttons are absent; content is fully visible. |
| `*` (fallback) | `not_found_view` | None | Static "404 Not Found" message. |

---

## 4. Home / Landing Route Assessment

**Route**: `/` → `timeline_view`

### Is it gated behind authentication?

No. `timeline_view` reads `ctx.session` only once — via `ctx.client()` — to determine whether to attach a bearer token to the API request. When `session` is `None`, `ctx.client()` returns a no-auth `ApiClient` and the request is made unauthenticated.

### Does it show timeline content?

Yes, unconditionally. On first display, `timeline_view` immediately kicks off `GET /timeline` (page size 20, no cursor). The view branches on its `TimelineModel`:

| State | What the visitor sees |
|-------|-----------------------|
| Initial load in progress | "Loading timeline…" spinner |
| First page loaded, non-empty | Keyed `<ul>` of chirp items with "Load more" / end-of-timeline footer |
| First page loaded, empty | "No chirps yet." |
| First page failed | Error banner + "Retry" button |
| Continuation error (after first load) | Chirp list visible; inline error banner + "Try again" below |

Chirp items render: `author_id` (numeric UserId as text), body text, like count, and created-at timestamp in milliseconds. There is no display name, no @handle, and no link to the author's profile.

### Does it show a useful empty / signup state?

No. The empty state is "No chirps yet." — a neutral message with no signup prompt, no login CTA, and no explanation of what the app is for. The error state likewise carries no login prompt. There is no landing page content for a first-time logged-out visitor.

### Assessment

The timeline works for a logged-out visitor as long as the backend allows unauthenticated `GET /timeline`. The frontend always sends the request and renders whatever the server returns. There is no session check that would prevent loading or display. The gap is UX: a logged-out visitor gets no context for the app, no path to sign up, and cannot navigate to any user's profile from the chirp list.

---

## 5. User Profile Route Assessment

**Route**: `/user/:id` → `profile_view`

### Does it exist?

Yes, at `/user/:id`. The `:id` parameter is parsed as a `u64` → `UserId`. A non-numeric segment renders "Invalid profile / The user id in the address is not a valid number." (no redirect).

### What does it currently render for a logged-out visitor?

The profile loads for anyone. After `GET /users/{id}` succeeds:

**Visible to all (including logged-out)**:
- `<h1>` — display name
- `@handle` paragraph
- Bio paragraph (if present)
- Follower and following counts

**Gated by session**:
- Follow control: when `viewer_id` is `None` → `hint("Log in to follow this user.")` (no button)
- Like control: when `!logged_in` → `hint("Log in to like chirps.")` (no button)
- When viewer is the same as the profile subject → `note("This is you.")` instead of a follow button

### Is it gated?

No. The profile data is loaded regardless of session state. Only the interactive actions (follow, like) are gated — and they degrade gracefully to informational hints rather than hard guards or redirects.

### Notes on the `:id` convention

The route uses a numeric `UserId` (`u64`), not a username or handle. There is currently no route `/user/:username` and no mechanism in the app to navigate to a profile from a chirp item (chirp items render `author_id` as plain text, not a link). Discovery of profiles requires knowing a numeric id.

---

## 6. Component Inventory

### Shared reactive context

| Item | File | Description |
|------|------|-------------|
| `AppContext` | `app.rs` | Shared by clone to every route; holds `base_url: String` and `session: Signal<Option<Session>>`. The session signal is the single reactive render anchor for all views. |
| `Session` | `app.rs` | `user: User` + `token: SessionToken`. `None` = logged out. |
| `ApiClient` | `api.rs` | Typed async REST client. Attaches bearer token when `session` is `Some`. Methods: `login`, `create_user`, `create_chirp`, `timeline`, `get_user`, `set_follow`, `set_like`. |
| `AppError` | `error.rs` | Three variants: `Api(ApiError)`, `Network(String)`, `Transport(String)`. `user_message()` for inline display; `code()` for `NOT_FOUND` etc. |

### Route views

| Item | File | Reuse potential |
|------|------|----------------|
| `timeline_view` | `timeline.rs` | Full timeline with loading/error/empty/paginated states; keyed chirp list. The whole view could serve a public timeline with no changes if the backend allows unauthenticated reads. |
| `compose_view` | `compose.rs` | Dual-mode: login form (logged-out) or compose form (logged-in). The login form is a usable login UI that can be adapted or extracted. |
| `profile_view` | `profile.rs` | Full public profile view. Already gracefully degrades for logged-out visitors. Only action controls need adjustment for a richer logged-out experience. |

### Reusable UI primitives

| Item | File | Description |
|------|------|-------------|
| `error_banner(err)` | `timeline.rs` | `<p class="chirp-error" role="alert">` — reusable error banner |
| `button(label, on_click)` | `timeline.rs` | `<button type="button">` with click handler |
| `chirp_list(chirps)` / `chirp_item(chirp)` | `timeline.rs` | Keyed `<ul>/<li>` chirp list; can be embedded in any view |
| `loading_view()` / `empty_view()` | `timeline.rs` | "Loading timeline…" / "No chirps yet." — reusable loading/empty states |
| `hint(message)` | `profile.rs` | `<p class="chirp-hint">` — dimmed informational hint |
| `note(message)` | `profile.rs` | `<p class="chirp-note">` — neutral note |
| `stat(label, value)` | `profile.rs` | `<strong>count</strong> label` stat display |
| `message_view(class, title, body)` | `profile.rs` | Titled message panel (not-found, invalid id) |
| `banner(class, role, msg)` | `compose.rs` | Generic error/success inline banner |
| `nav_bar()` | `app.rs` | Persistent top nav; currently Timeline · Compose only |
| `not_found_view()` | `app.rs` | Static 404 panel |

---

## 7. Gaps

The following gaps are relevant to supporting a full logged-out visitor experience.

### Routes and navigation

| Gap | Detail |
|-----|--------|
| No dedicated login route | Login is embedded inside `/compose` only. A logged-out visitor who lands on `/` gets no path to log in without navigating to Compose. |
| No logout mechanism | `AppContext.session` can be set to `None` to log out, but no UI control does this. |
| No profile links from timeline | `chirp_item` renders `author_id` as plain text. There is no `<a href="/user/{id}">` or any other navigation to a profile. |
| Nav bar is session-unaware | Shows "Timeline · Compose" for everyone; no login link, no user identity, no logout. |
| No signup / registration flow | `ApiClient::create_user` exists but no UI routes or components drive it. |

### Logged-out timeline UX

| Gap | Detail |
|-----|--------|
| No landing / onboarding content | The root route renders only the chirp list. First-time visitors have no context for what the app is or how to participate. |
| Empty state has no CTA | "No chirps yet." provides no call to action for a logged-out visitor. |
| Author display is unfriendly | Chirp items show a raw numeric `UserId`. Showing `@handle` or display name, as a link to `/user/:id`, would significantly improve discoverability. |

### Profile route discoverability

| Gap | Detail |
|-----|--------|
| Numeric `:id` not surfaced anywhere | `/user/:id` requires knowing the numeric user ID. No existing UI generates or displays these links. The timeline would need to emit profile links (see above) to make this route reachable. |

### Session state on initial load

| Gap | Detail |
|-----|--------|
| No session persistence | `AppContext::new` always starts with `session: None`. There is no `localStorage` read or cookie check on mount. A page refresh logs the user out. This is out of scope for the logged-out feature but affects any logged-in state added for the public views. |
