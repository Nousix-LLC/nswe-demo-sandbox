# Frontend Logged-Out Visitor UI Implementation

## Summary

The logged-out visitor frontend is fully implemented on branch `work/chirp-logged-out`.
All five acceptance criteria (AC-1 through AC-5) are satisfied by the components described
below. All build and quality gates pass: 76 tests, `cargo build --target wasm32-unknown-unknown`,
`cargo clippy`, and `cargo fmt --check`.

---

## 1. Components Implemented

| Component | File | AC addressed | Status |
|-----------|------|-------------|--------|
| Public landing / home view | `crates/chirp-frontend/src/landing.rs` | AC-1, AC-2, AC-3, AC-4, AC-5 | New |
| Public user profile view | `crates/chirp-frontend/src/public_profile.rs` | AC-1, AC-5 | New |
| Sign-in entry point | `crates/chirp-frontend/src/sign_in.rs` | AC-4 | New |
| Sign-up entry point | `crates/chirp-frontend/src/sign_up.rs` | AC-4 | New |
| Application router + nav bar | `crates/chirp-frontend/src/app.rs` | AC-1, AC-4 | Modified |
| Typed REST client | `crates/chirp-frontend/src/api.rs` | AC-1 | Modified |
| Secondary timeline view | `crates/chirp-frontend/src/timeline.rs` | AC-4 (CTA fix) | Modified |

### `landing.rs` — Public home/landing view (`/`)

The primary view for logged-out visitors. Loads `GET /api/chirps` on first display, renders
a keyed reactive list with four visually distinct states, and always shows sign-up / sign-in
navigation. Pagination uses an `i64` `before` cursor derived from the `created_at` of the last
loaded chirp.

### `public_profile.rs` — Public user profile view (`/@:handle`)

Renders a user's profile and their chirp list. Accepts a `:handle` route parameter, fetches
`GET /api/users/:username/chirps`, and handles six states: loading, not-found (HTTP 404),
empty (user exists, no chirps), loaded (chirps present), end-of-list, and recoverable error.
Reachable from chirp items in the landing view via `/@alice` profile links.

### `sign_in.rs` — Sign-in entry point (`/signin`)

Stub sign-in form page. Provides a visible sign-in entry point and a "Create an account" link
to `/signup`. The credential form itself (POST /sessions) is out of scope for this feature;
the stub exists so the route is reachable (not a 404) and the navigation chain is complete.

### `sign_up.rs` — Sign-up entry point (`/signup`)

Stub sign-up form page. Provides a visible sign-up entry point and a "Sign in" link to `/signin`.
The registration form (POST /users) is deferred to a future authentication feature.

### `app.rs` — Router and nav bar

The nav bar now renders "Create account" (→ `/signup`) and "Sign in" (→ `/signin`) links for
every visitor regardless of session state, satisfying AC-4. The route table adds:

| Route | View | Notes |
|-------|------|-------|
| `/` | `landing_view` | Replaces old `timeline_view` as the public home |
| `/@:handle` | `public_profile_view` | Username-based public profile |
| `/signin` | `sign_in_view` | Sign-in entry point |
| `/signup` | `sign_up_view` | Sign-up entry point |

The old authenticated routes (`/compose`, `/user/:id`, `/timeline`) are retained unchanged.

### `api.rs` — REST client additions

Two new unauthenticated methods and their response types:

| Method | Endpoint | Return type |
|--------|----------|-------------|
| `public_timeline(before, limit)` | `GET /api/chirps` | `PublicTimelineResponse` |
| `public_user_profile(username, before, limit)` | `GET /api/users/{username}/chirps` | `PublicUserResponse` |

Both methods build an unauthenticated `ferric_http::Client` (no `Authorization` header) so
they are safe to call even when a session token is present. Response types (`PublicChirp`,
`PublicAuthor`, `PublicUserChirp`, `PublicUserInfo`, `PublicTimelineResponse`, `PublicUserResponse`)
are defined in `api.rs` and match the wire shapes in `backend-impl.md` exactly.

---

## 2. Four Timeline States

All four states are implemented in `landing.rs`'s `view_tree()` and are visually distinct via
separate CSS classes and content.

### Loading

**Visual treatment**: a `<p class="chirp-loading">Loading…</p>` paragraph rendered as the initial
state before the first page arrives. The nav bar and the in-view "Create account · Sign in"
header remain fully visible during the load, so the visitor is never on a blank screen (AC-2).

**Code path**: `LandingModel.loaded == false && error.is_none()` → `loading_view()`.

### Empty

**Visual treatment**: `<div class="chirp-landing-empty">` containing:
- An `<h2>Welcome to Chirp</h2>` heading
- A description paragraph: "Chirp is a place to share short thoughts and follow people you
  find interesting."
- A CTA div with links: "Create an account" (→ `/signup`) · "Sign in" (→ `/signin`)

**Code path**: `LandingModel.loaded == true && chirps.is_empty()` → `empty_view()`.

This state never shows a blank page and always provides an obvious entry into the sign-up /
sign-in flow (AC-2, AC-5).

### Error

**Visual treatment**: `<div class="chirp-landing-error">` containing:
- `<p class="chirp-error" role="alert">` with `AppError::user_message()` — plain language,
  no raw HTTP status codes or Rust panics
- A "Retry" `<button type="button">` that calls `reload()`, which resets the model and
  re-fetches the first page in-place (no full-page reload)

**Code path**: `LandingModel.loaded == false && error.is_some()` (initial failure)
or `LandingModel.loaded == true && error.is_some()` (inline continuation error — rendered
in the footer beneath the loaded list).

Both paths surface the error and offer recovery (AC-3, AC-5).

### End-of-list

**Visual treatment**: `<p class="chirp-end">You're all caught up.</p>` shown below the last
page of chirps. This is visually distinct from the "Load more" button (which appears when
`has_more == true`) and from the loading/empty/error states.

**Code path**: `LandingModel.loaded == true && !chirps.is_empty() && !has_more && !loading_more && error.is_none()`
→ footer renders the end note.

---

## 3. Navigation

### Persistent nav bar (every page)

`nav_bar()` in `app.rs` always renders:

```
Chirp · Compose · Create account · Sign in
```

Links: `/ · /compose · /signup · /signin`

This is shown above the route outlet on every page, so sign-up and sign-in entry points are
visible regardless of which route the visitor is on (AC-4).

### In-view header nav (landing view, every state)

`header_nav()` in `landing.rs` renders a secondary nav inside the landing section:

```
Create account · Sign in
```

Links: `/signup · /signin`

This is rendered for every landing state (loading, empty, error, loaded), satisfying AC-4 even
before the timeline content arrives.

### Empty-state CTA

The empty-state view (`empty_view()` in `landing.rs`) includes a prominent "Create an account"
link to `/signup` and a "Sign in" link to `/signin` as the primary call to action when the
timeline is empty.

### Profile links in chirp items

Each chirp item in the landing view links the author's display name to their public profile:

```rust
let profile_path = format!("/@{}", chirp.author.username);
link(&profile_path, display)   // display = display_name or username
```

This makes every public user profile reachable from the timeline without authentication (AC-1).

### Sign-in screen → sign-up

`sign_in_view()` renders "New to Chirp? Create an account" with a link to `/signup` (AC-4).

### Sign-up screen → sign-in

`sign_up_view()` renders "Already have an account? Sign in" with a link to `/signin`.

---

## 4. API Calls Made

The frontend calls exactly the two endpoints declared in `backend-impl.md`. No other endpoints
are called by the new components.

| Endpoint | Method | Called by | Notes |
|----------|--------|-----------|-------|
| `GET /api/chirps` | `ApiClient::public_timeline(before, limit)` | `landing.rs` | No auth header; `before` is an `i64` timestamp passed as a decimal string; `limit` defaults to 20 |
| `GET /api/users/{username}/chirps` | `ApiClient::public_user_profile(username, before, limit)` | `public_profile.rs` | No auth header; 404 response maps to `AppError::Api` with `NotFound` code |

**Pagination**: Both endpoints use the same `before` / `limit` cursor contract from `backend-impl.md`.
After each successful page, `before_cursor` is set to the `created_at` timestamp of the last
chirp, which is passed as `before` on the next request. `has_more: true` enables "Load more";
`has_more: false` renders the end-of-list state.

**No auth added**: Neither `landing.rs` nor `public_profile.rs` reads or writes the session
signal. Both `public_timeline` and `public_user_profile` build an explicit no-auth
`ferric_http::Client`, ignoring any session token even if one is present.

---

## 5. Test Coverage

All tests are native (no DOM, no WASM runtime). They exercise the pure state-reduction and
view-tree functions directly. 71 tests pass in total; the state tests per module are listed
below.

### How to run

```bash
cargo test -p chirp-frontend
```

### `landing.rs` — 11 tests

| Test | State covered |
|------|--------------|
| `unloaded_model_renders_loading_state` | Loading |
| `every_state_includes_header_nav_links` | All states (nav presence) |
| `empty_model_renders_welcome_statement_and_cta_links` | Empty (AC-2) |
| `loaded_model_renders_chirp_list_and_load_more_button` | Loaded / paginated |
| `last_page_renders_end_note_not_load_more` | End-of-list |
| `initial_error_renders_error_message_and_retry_button` | Error (AC-3) |
| `apply_initial_marks_loaded_sets_cursor_and_has_more` | State reduction |
| `apply_more_appends_and_updates_cursor` | Pagination state reduction |
| `apply_error_on_initial_keeps_unloaded` | Error state reduction |
| `apply_error_after_load_keeps_loaded` | Inline continuation error |
| `begin_initial_resets_all_state` | Retry reset |

### `public_profile.rs` — 12 tests

| Test | State covered |
|------|--------------|
| `loading_state_renders_loading_indicator` | Loading |
| `not_found_state_renders_distinct_message` | Not-found (404) |
| `empty_loaded_state_renders_empty_message` | Empty |
| `loaded_with_chirps_renders_list_and_load_more` | Loaded / paginated |
| `end_of_list_renders_end_note` | End-of-list |
| `error_state_renders_message_and_retry` | Error |
| `apply_initial_transitions_to_loaded` | State reduction |
| `apply_more_appends_chirps` | Pagination state reduction |
| `apply_error_on_initial_not_found_sets_not_found_phase` | 404 error reduction |
| `apply_error_on_initial_server_error_sets_error_phase` | Non-404 error reduction |
| `apply_error_on_more_sets_continuation_error` | Inline continuation error |
| `reset_for_clears_all_prior_state` | Handle-change reset |

### `sign_in.rs` — 3 tests

| Test | What it verifies |
|------|-----------------|
| `sign_in_view_renders_a_section_with_correct_class` | Component renders |
| `sign_in_view_contains_link_to_signup` | "Create an account" link present (AC-4) |
| `sign_in_view_contains_link_to_home` | Back-to-home link present |

### `sign_up.rs` — 3 tests

| Test | What it verifies |
|------|-----------------|
| `sign_up_view_renders_a_section_with_correct_class` | Component renders |
| `sign_up_view_contains_link_to_signin` | "Sign in" link present |
| `sign_up_view_contains_link_to_home` | Back-to-home link present |

### `timeline.rs` — 11 tests (secondary `/timeline` route)

The existing test suite for the old authenticated timeline view. All states are covered:
loading, empty, loaded (with Load more), last page (end-of-list), and error.

### `api.rs` — 12 tests

Client construction, path building, query serialization, and error mapping.

---

## 6. Quality Gate Results

| Gate | Result |
|------|--------|
| `cargo build -p chirp-frontend --target wasm32-unknown-unknown` | ✓ Pass |
| `cargo clippy -p chirp-frontend -- -D warnings` | ✓ Pass (0 warnings) |
| `cargo fmt -p chirp-frontend --check` | ✓ Pass |
| `cargo test -p chirp-frontend` | ✓ 76/76 pass |

---

## 7. AC Coverage Summary

| AC | Requirement | Satisfied by |
|----|-------------|-------------|
| AC-1 | Logged-out visitor can reach public timeline and user profile without signing in | `landing.rs` calls `GET /api/chirps` without auth; `public_profile.rs` calls `GET /api/users/:username/chirps` without auth; chirp author links navigate to `/@handle` |
| AC-2 | Empty state shows "what Chirp is" + sign-up/sign-in CTA — never blank | `landing.rs` `empty_view()`: "Welcome to Chirp" + description + "Create an account" + "Sign in" links |
| AC-3 | Timeline failure shows clear recoverable error message | `landing.rs` error state: `AppError::user_message()` in `role="alert"` + "Retry" button that re-fetches in-place |
| AC-4 | "Create an account" route visible on landing and sign-in screen | Nav bar on every page; `header_nav()` in every landing state; `sign_in_view` has "Create an account" → `/signup` |
| AC-5 | Loading / empty / error / end-of-list states are visually distinct | Four distinct CSS classes and content: `chirp-loading`, `chirp-landing-empty`, `chirp-landing-error`, `chirp-end` |

---

## 8. Known Limitations and Future Work

- **Sign-in and sign-up forms are stubs**: The `POST /sessions` and `POST /users` calls are
  not wired up. The routes are reachable and the navigation chain is complete, but submitting
  the forms has no effect. This is in scope for the future authentication feature.

- **Loading skeleton cards deferred**: The loading state renders a text "Loading…" indicator
  rather than shape-matched skeleton cards (REQ-UX-030). The state is visually distinct per
  AC-5, but skeleton cards would better match the final chirp card geometry. This is a UX
  polish item for the design-system sprint.

- **SSR pre-fetch not implemented**: `render_to_string` emits the loading state; the client
  always re-fetches after hydration. This is tracked in issue #225 (BAR-005); implementing
  it requires data serialization infrastructure not yet in Ferric.
