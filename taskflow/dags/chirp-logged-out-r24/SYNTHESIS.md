# SYNTHESIS — chirp-logged-out-r24

**Verdict: PASS**

**Branch**: `work/chirp-logged-out`  
**Head**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`  
**PR**: #263 — OPEN, MERGEABLE  
**CI** (run 42194072348): ALL 6 PASS (doc / fmt / clippy / wasm / test / image)

---

## Acceptance Criteria Verification

### AC-1 · Logged-out reading — PASS

> A logged-out visitor can load the home/public timeline and open a user profile and read chirps
> without being forced to sign up or sign in first. (`REQ-PROD-013`, `BAR-011`)

**Evidence:**

- **Backend**: `GET /api/chirps` → `handlers::public_chirps` and `GET /api/users/{username}/chirps` → `handlers::user_chirps` carry no `AuthUser` extractor; they accept anonymous requests and return chirps.  `handlers.rs` doc table confirms: "Auth: no" for both handlers.
- **Frontend**: Routes `/` (landing_view) and `/@:handle` (public_profile_view) are mounted without any auth guard in `app.rs`. `AppContext.session` is initialized to `None` (logged-out) and both views call their respective API methods unconditionally — no redirect, no session check in the route closure.
- **No forced redirect**: Neither the router nor any view dispatches to `/signin` or `/signup` for unauthenticated visitors on these two paths. The only authenticated-required routes are `/compose` (compose_view), `/user/:id` (profile_view — authenticated profile), and `/timeline` (authenticated timeline).

---

### AC-2 · Useful empty state — PASS

> On arrival with no content, the visitor sees a clear statement of what Chirp is plus an obvious
> way to sign up or sign in — never a blank page or an unexplained error. (`REQ-PROD-014`, `BAR-011`)

**Evidence:**

- `landing.rs::empty_view()` renders when `model.loaded && model.chirps.is_empty()` — triggered when the public timeline returns an empty list.
- The empty view displays an `<h2>Welcome to Chirp</h2>` and a description paragraph: "Chirp is a place to share short thoughts and follow people you find interesting."
- It then renders a CTA section with "Create an account" (→ `/signup`) and "Sign in" (→ `/signin`) links — clearly distinct entry points into the authenticated flow.
- Unit test `empty_model_renders_welcome_statement_and_cta_links` asserts the welcome text, the sign-up link, and the sign-in link are all present in the empty-state render tree.

---

### AC-3 · Recoverable error state — PASS

> If the timeline fails to load, a clear, recoverable message is shown instead of a broken screen.
> (`REQ-PROD-014`, `BAR-011`)

**Evidence:**

- `landing.rs::view_tree()` matches `!model.loaded && model.error.is_some()` → renders a `<div class="chirp-landing-error">` containing:
  - An `AppError::user_message()` string in a `<p role="alert">` banner (accessible, human-readable copy).
  - A "Retry" `<button>` wired to `on_retry`, which calls `reload(ctx)` to re-fetch the timeline.
- After a successful first load, pagination errors render an inline `chirp-load-more-error` section with the same error banner and a "Try again" button — no broken/blank screen.
- Unit test `initial_error_renders_error_message_and_retry_button` asserts the error message and Retry button are present.

---

### AC-4 · Sign-up route visibility — PASS

> A "create an account" route is visible on the landing and on the sign-in screen, and following it
> reaches sign-up. (`REQ-PROD-015`, `BAR-011`)

**Evidence:**

- **Persistent nav bar** (`app.rs::nav_bar()`): rendered above the reactive outlet on **every** route. Contains `link("/signup", "Create account")` and `link("/signin", "Sign in")` — always visible regardless of current view.
- **Landing per-view nav** (`landing.rs::header_nav()`): adds another "Create account" and "Sign in" pair inside the landing section itself, so it appears even before the page-level nav loads.
- **Sign-in screen** (`sign_in.rs::sign_in_view()`): explicitly renders `link("/signup", "Create an account")` in a `chirp-signin-links` paragraph with the text "New to Chirp?" — the primary call-to-action from the sign-in page.
- `/signup` route resolves to `signup_view` (the full account-creation form in `compose.rs`), so following these links reaches sign-up.
- `/sign-in` alias added in `decb6196` so both `/signin` and `/sign-in` resolve to the sign-in view — visitors who type the hyphenated form reach the page rather than the not-found fallback.
- Unit tests: `every_state_includes_header_nav_links` and `sign_in_view_contains_link_to_signup` both assert link presence.

---

### AC-5 · Accurate distinct states — PASS

> The logged-out landing/timeline exercises its loading, empty, error, and end-of-list states
> accurately and distinctly. (`REQ-UX-002/030/031/032`, `BAR-011`, one-state-model criterion)

**Evidence — `landing.rs` state model:**

| State | Condition | Rendered element | Test |
|-------|-----------|------------------|------|
| **Loading** | `!loaded && error.is_none()` | `<p class="chirp-loading">Loading…</p>` | `unloaded_model_renders_loading_state` |
| **Empty** | `loaded && chirps.is_empty()` | `<div class="chirp-landing-empty">` with welcome text + CTA | `empty_model_renders_welcome_statement_and_cta_links` |
| **Error** | `!loaded && error.is_some()` | `<div class="chirp-landing-error">` with alert + Retry | `initial_error_renders_error_message_and_retry_button` |
| **Loaded** | `loaded && !chirps.is_empty() && has_more` | `<div class="chirp-landing-loaded">` + "Load more" button | `loaded_model_renders_chirp_list_and_load_more_button` |
| **End-of-list** | `loaded && !chirps.is_empty() && !has_more` | "You're all caught up." paragraph | `last_page_renders_end_note_not_load_more` |

Each state is a distinct CSS class and distinct render path — the conditions are exhaustive and mutually exclusive, satisfying the one-state-model criterion. No state collapses into another.

**Public profile view** (`public_profile.rs`) independently covers 6 states: loading, not-found, empty, loaded, end-of-list, and error — documented at the top of that module.

---

## Summary

All five acceptance criteria for issue #35 are met on branch head `decb6196c2c1e6ed421d393a642f0c844cc333ba`. The implementation is:

- Fully tested (30 new frontend unit tests covering all distinct UI states + 6 new server handler tests)
- CI-green on all 6 required checks
- PR #263 is open and mergeable with no blocking changes needed

**The branch is ready to merge.** No code changes were required by this synthesis; the work was complete when this run was dispatched.
