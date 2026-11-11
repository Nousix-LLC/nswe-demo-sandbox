# SYNTHESIS.md — chirp-logged-out-r26

## Verdict: PASS — all 5 acceptance criteria met

PR #263 (`work/chirp-logged-out`, HEAD `decb6196c2c1e6ed421d393a642f0c844cc333ba`) satisfies every
acceptance criterion for GitHub issue #35 ("Logged-out reading and a useful landing with accurate
states"). CI is fully green (fmt, clippy, test, wasm, doc, image — 6/6). PR is OPEN and MERGEABLE.

---

## AC evidence

### AC-1 ✅ — Public timeline + user profiles accessible without login
**Requirement (REQ-PROD-013, BAR-011):** A logged-out visitor can load the home/public timeline and
open a user profile and read chirps without being forced to sign up or sign in first.

**Evidence:**
- `GET /api/chirps` handler (`crates/chirp-server/src/api/handlers.rs::public_chirps`): signature is
  `State(AppState)` + `Query` only — no auth extractor. No authentication middleware on this route.
- `GET /api/users/{username}/chirps` handler (`handlers.rs::user_chirps`): same pattern — only
  `State(AppState)`, `Path(username)`, and `Query` extractors; no auth extractor whatsoever.
- Frontend: `/` renders `landing_view` which calls `GET /api/chirps`; `/@:handle` renders
  `public_profile_view` which calls `GET /api/users/:username/chirps`. Both routes are in the public
  (unauthenticated) router section of `app.rs`. No redirect to `/signin` from either view.

---

### AC-2 ✅ — Clear landing with sign-up prompt on empty state
**Requirement (REQ-PROD-014, BAR-011):** On arrival with no content, the visitor sees a clear
statement of what Chirp is plus an obvious way to sign up or sign in — never a blank page or an
unexplained error.

**Evidence (`crates/chirp-frontend/src/landing.rs::empty_view`):**
- Renders only when `model.loaded && model.chirps.is_empty()`.
- Shows `<h2>Welcome to Chirp</h2>` — explicit product identity.
- Shows a description paragraph explaining what Chirp is.
- CTA buttons: "Create an account" → `/signup` and "Sign in" → `/signin`.
- No blank page; no unexplained error.

---

### AC-3 ✅ — Clear recoverable error message on timeline load failure
**Requirement (REQ-PROD-014, BAR-011):** If the timeline fails to load, a clear, recoverable message
is shown instead of a broken screen.

**Evidence (`crates/chirp-frontend/src/landing.rs::view_tree`):**
- Branch `!model.loaded && model.error.is_some()` → renders `error_banner()` (with `role="alert"` for
  accessibility) and a "Retry" button that re-triggers the fetch.
- The error message is human-readable (derived from `AppError` display), not a raw status code.
- `app.rs` registers both `/signin` and `/sign-in` (alias) routes, satisfying the spec path
  `/sign-in` alongside the conventional `/signin`.

---

### AC-4 ✅ — "Create an account" route visible on landing AND sign-in screen
**Requirement (REQ-PROD-015, BAR-011):** A "create an account" route is visible on the landing and
on the sign-in screen, and following it reaches sign-up.

**Evidence:**
- `app.rs::nav_bar()`: persistent navigation rendered on every screen contains "Create account" →
  `/signup` and "Sign in" → `/signin`.
- `landing.rs::header_nav()`: the landing page has its own additional nav with "Create account" →
  `/signup`, present in ALL landing states (loading, empty, error, loaded) via comment "Persistent
  sign-up / sign-in links shown in every landing-view state (AC-4)".
- `sign_in.rs::sign_in_view()`: renders a "Create an account" link → `/signup` with an accompanying
  unit test (`sign_in_view_contains_link_to_signup`) asserting its presence.
- `/signup` route is registered in `app.rs` and resolves to `signup_view`.

---

### AC-5 ✅ — Loading, empty, error, end-of-list states accurate and distinct
**Requirement (REQ-UX-002/030/031/032):** The logged-out landing/timeline exercises its loading,
empty, error, and end-of-list states accurately and distinctly.

**Evidence (`crates/chirp-frontend/src/landing.rs::view_tree` + `footer`):**

| State | Trigger | Rendered output |
|---|---|---|
| Loading | `!loaded && error.is_none()` | `<p class="chirp-loading">Loading…</p>` |
| Error (pre-load) | `!loaded && error.is_some()` | `error_banner()` (role=alert) + Retry button |
| Empty | `loaded && chirps.is_empty()` | "Welcome to Chirp" header + description + CTAs |
| Loaded (has content) | `loaded && !chirps.is_empty()` | chirp list + `footer()` |
| End-of-list | `loaded && !has_more` (in `footer()`) | "You're all caught up." |
| Load-more in-flight | `loading_more` (in `footer()`) | loading spinner |
| Inline continuation error | `continuation_error.is_some()` (in `footer()`) | inline error + "Try again" |

All states are mutually exclusive and produce distinct UI.

`crates/chirp-frontend/src/public_profile.rs` module comment: "six distinct states: loading,
not-found (HTTP 404), empty (user exists, no chirps), loaded (user and chirps), end-of-list (last
page displayed), and error (recoverable failure)" — same pattern implemented for user profile view.

---

## CI status (HEAD decb6196)

| Check | Status |
|---|---|
| fmt | ✅ pass |
| clippy | ✅ pass |
| test | ✅ pass |
| wasm | ✅ pass |
| doc | ✅ pass |
| image | ✅ pass |

---

## Recommendation

PR #263 is ready to merge. All 5 ACs are satisfied by the implementation at `decb6196`. No further
code changes are needed. Merge path: `gh pr merge 263 --squash --delete-branch -R Nousix-LLC/nswe-demo`.
