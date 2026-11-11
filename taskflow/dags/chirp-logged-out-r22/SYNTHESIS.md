# SYNTHESIS.md — chirp-logged-out-r22

## Overall verdict: PASS

All five acceptance criteria for issue #35 are met by the code at head `617f25395eebe9475f19a90e0b1dac5921215ea3`. CI run 42183715802 is fully green (clippy, doc, fmt, image, test, wasm). PR #263 is OPEN/MERGEABLE/CLEAN. No code changes were required.

**Final head SHA**: `617f25395eebe9475f19a90e0b1dac5921215ea3`

---

## Per-criterion assessment

### AC-1 — Unauthenticated reading: **MET**

> A logged-out visitor can load the home/public timeline and open a user profile and read chirps without being forced to sign up or sign in first. (REQ-PROD-013, BAR-011)

**Evidence:**
- `crates/chirp-frontend/src/app.rs`: `/` routes to `landing_view` (public home/timeline) and `/@:handle` routes to `public_profile_view` — both are accessible without authentication.
- `crates/chirp-frontend/src/api.rs`: `public_timeline()` builds an unauthenticated `ApiClient` (no Authorization header) and calls `GET /api/chirps`. `public_user_profile()` likewise calls `GET /api/users/{username}/chirps` with no auth.
- `crates/chirp-server/src/api/handlers.rs` + `router.rs`: `GET /api/chirps` → `public_chirps` handler and `GET /api/users/{username}/chirps` → `user_chirps` handler are both mounted as unauthenticated routes (no auth middleware on these endpoints).
- Neither the landing route nor the profile route gate on session presence; `AppContext.client()` returns an unauthenticated `ApiClient` when `session` is `None`.

---

### AC-2 — Empty-state clarity: **MET**

> On arrival with no content, the visitor sees a clear statement of what chirp is plus an obvious way to sign up or sign in — never a blank page or an unexplained error. (REQ-PROD-014, BAR-011)

**Evidence:**
- `crates/chirp-frontend/src/landing.rs`: `empty_view()` renders a "Welcome to Chirp" section with a description of the product, a "Create an account" link targeting `/signup`, and a "Sign in" link targeting `/signin`. This state is entered when `model.loaded && model.chirps.is_empty()`.
- The empty state is distinct from the loading state (spinner) and error state (error banner + Retry button).
- Unit test `test_landing_empty_view` verifies the empty state renders correctly and independently of the other states.

---

### AC-3 — Recoverable error state: **MET**

> If the timeline fails to load, a clear, recoverable message is shown instead of a broken screen. (REQ-PROD-014, BAR-011)

**Evidence:**
- `crates/chirp-frontend/src/landing.rs`: when `model.error` is set, the view renders a visible error banner with the error message and a "Retry" button that calls `ctx.reload()` — which re-dispatches the initial load action without a full page reload (satisfying REQ-UX-032's "plain message with Try Again that refetches without full reload" requirement).
- Unit test `test_landing_error_view` verifies the error state renders the error message and retry affordance.
- The error state is explicitly distinct from the empty and loaded states; the model transitions between these states via reducers, never leaving both `error` set and `loaded` true simultaneously.

---

### AC-4 — Create-account route visible on landing and sign-in: **MET**

> A "create an account" route is visible on the landing and on the sign-in screen, and following it reaches sign-up. (REQ-PROD-015, BAR-011)

**Evidence:**
- `crates/chirp-frontend/src/landing.rs`: `header_nav()` renders "Create account" → `/signup` and "Sign in" → `/signin` links unconditionally in the page header. These appear in every landing state (loading, empty, error, loaded) because `header_nav()` is called at the top of `landing_view()` before the state branch.
- `crates/chirp-frontend/src/app.rs`: `nav_bar()` includes "Create account" → `/signup` and "Sign in" → `/signin` as persistent nav links on every screen (REQ-UX-002: persistent on every logged-out surface).
- `crates/chirp-frontend/src/sign_in.rs`: the sign-in screen contains a "Create an account" link targeting `/signup`, satisfying AC-4's explicit "visible on the sign-in screen" requirement.
- `crates/chirp-frontend/src/app.rs`: `/signup` → `signup_view` is registered in the route table; following the link does reach sign-up.
- Unit tests in `sign_in.rs` (`test_sign_in_has_signup_link`) verify the "Create an account" link is present on the sign-in screen.

---

### AC-5 — Distinct loading/empty/error/end-of-list states: **MET**

> The logged-out landing/timeline exercises its loading, empty, error, and end-of-list states accurately and distinctly. (REQ-UX-002/030/031/032, BAR-011, one-state-model criterion)

**Evidence:**
- `crates/chirp-frontend/src/landing.rs`: `LandingModel` has explicit independent flags: `loaded: bool`, `chirps: Vec<PublicChirp>`, `before_cursor: Option<Uuid>`, `has_more: bool`, `loading_more: bool`, `error: Option<AppError>`. The view branches cleanly:
  - `!model.loaded && model.error.is_none()` → loading state: `<p class="chirp-loading">Loading…</p>`
  - `model.loaded && model.chirps.is_empty()` → empty state: description + join links
  - `model.error.is_some()` → error state: error banner + Retry button
  - `model.loaded && !model.chirps.is_empty()` → loaded state: chirp list + footer
  - Within loaded state, `model.has_more` controls whether "Load more" or "You've reached the end" appears — end-of-list is visibly distinct from the empty state (REQ-UX-032).
- 11 unit tests cover each state independently: `test_landing_loading_view`, `test_landing_empty_view`, `test_landing_error_view`, `test_landing_loaded_view`, `test_landing_end_of_list_view`, plus model-reduction tests.
- `crates/chirp-frontend/src/public_profile.rs`: `ProfileModel` uses a `LoadPhase` enum (`Loading`, `NotFound`, `Error(AppError)`, `Loaded`) ensuring exactly one state at any time — this satisfies the one-state-model criterion. The public profile renders 6 distinct states: loading, not-found (HTTP 404), empty (user exists, no chirps), loaded, end-of-list, error.
- Both the landing and public profile view trees have no path that renders a blank screen or silently fails to communicate state.

---

## CI assessment

CI run 42183715802 (on head `617f2539`) passed all checks:
- `clippy` — no lint failures
- `doc` — documentation builds clean
- `fmt` — formatting consistent
- `image` — Docker image builds
- `test` — all unit tests pass (includes the 11 landing-state tests and profile-state tests above)
- `wasm` — WASM frontend compiles

The test suite covers the state branches and model reductions that are the substance of AC-5.

---

## Conclusion

The branch `work/chirp-logged-out` at `617f25395eebe9475f19a90e0b1dac5921215ea3` satisfies all five acceptance criteria for issue #35. PR #263 is ready to merge. No further code changes are required.
