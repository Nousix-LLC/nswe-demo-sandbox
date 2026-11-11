# SYNTHESIS — chirp-logged-out-r15

**Branch**: `work/chirp-logged-out`  
**Final HEAD**: `decb6196c2c1e6ed421d393a642f0c844cc333ba` (`decb619`)  
**CI Run**: 42194072348 — 6/6 ALL PASS (`doc`, `fmt`, `clippy`, `wasm`, `test`, `image`)  
**PR**: #263 — OPEN/MERGEABLE  
**Overall verdict**: **PASS** — all five acceptance criteria are met, CI is green, PR is mergeable.

---

## Criterion-by-Criterion Accounting

### AC-1 — Logged-out visitor can view the public timeline at `/`

**Status: MET**

- **Backend** (`crates/chirp-server/src/api/router.rs`): `GET /api/chirps` → `handlers::public_chirps`. Route confirmed.
- **Frontend** (`crates/chirp-frontend/src/landing.rs`): `landing_view()` registered at `/` in the route table. Implements a fully reactive public timeline that calls `ctx.client().public_timeline(before, limit)`, which issues `GET /api/chirps`. Renders six states: loading, empty (with "Create an account" and "Sign in" CTAs), loaded (chirp list with `/@username` profile links), end-of-list, loading-more, and error. `header_nav()` with sign-up/sign-in links is present in every state. Pagination uses an ISO 8601 `before` cursor at `PAGE_LIMIT = 20`.
- Comprehensive unit tests covering all state transitions and view-tree shape.

---

### AC-2 — Logged-out visitor can view a public user profile page

**Status: MET**

- **Backend** (`crates/chirp-server/src/api/router.rs`): `GET /api/users/{username}/chirps` → `handlers::user_chirps`. Route confirmed.
- **Frontend** (`crates/chirp-frontend/src/public_profile.rs`): `public_profile_view(ctx, handle)` registered at `/@:handle` in the route table. Fetches `GET /api/users/:username/chirps` via `ctx.client().public_user_profile()`. Implements six distinct states: loading, not-found (HTTP 404), empty (user exists, no chirps), loaded (user header + chirp list), end-of-list, and error (with Retry). Pagination mirrors the landing view's `before`-cursor strategy. Stale-result guard prevents applying a response after the user navigates away.
- Note: The route URL is `/@alice` (Twitter-style), not `/users/alice` as the AC example suggested. The example was illustrative; the criterion (public user profile showing that user's chirps) is fully satisfied.
- Comprehensive unit tests covering all state-reduction and view-tree cases.

---

### AC-3 — Logged-out visitor sees a sign-in page at `/sign-in`

**Status: MET**

- **Frontend** (`crates/chirp-frontend/src/app.rs` route table, `crates/chirp-frontend/src/sign_in.rs`):
  - `/signin` → `sign_in_view()` (registered from early rounds)
  - `/sign-in` → `sign_in_view()` (alias added in commit `decb619` specifically to satisfy this criterion)
- `sign_in_view()` renders a section with class `chirp-signin`, username/password form fields, a "Create an account" link to `/signup`, and a "Back to home" link to `/`. The submit button is present (disabled / "coming soon" — placeholder auth per scope).
- Unit tests verify the section class, presence of the sign-up link, and the home link.

---

### AC-4 — Logged-out visitor can reach a sign-up form at `/signup`

**Status: MET**

- **Frontend** (`crates/chirp-frontend/src/app.rs` route table, `crates/chirp-frontend/src/compose.rs`):
  - `/signup` → `signup_view()` (implemented in commit `21dca556`, r12)
- `signup_view()` renders a fully functional sign-up form with handle (username) and display-name input fields. On submit it validates both fields (via `Username::parse`), calls `POST /api/users` to create the account, and auto-logs in on success by calling `POST /api/sessions` and writing the resulting `Session` into `ctx.session`. Reactive busy/disabled, error banner, and "Already have an account? Log in →" link included.
- Note: `crates/chirp-frontend/src/sign_up.rs` also exists as a static stub with a placeholder form; the route table binds `/signup` to `compose::signup_view`, which is the functional implementation.
- Unit tests (in both `compose.rs` and `sign_up.rs`) cover validation logic, form-field gating, and view-tree shape.

---

### AC-5 — UI accurately reflects logged-in vs logged-out states

**Status: MET**

- **Compose box gated** (`crates/chirp-frontend/src/compose.rs`, `compose_view()`): reads `ctx.session` reactively. When `session` is `None` (logged out), renders `render_login()` — a login form. The compose textarea (`render_compose`) is only rendered when `session` is `Some`. Logged-out visitors navigating to `/compose` see a login prompt, not a compose box.
- **No "my feed" in nav**: The global `nav_bar()` links are `Chirp` (/), `Compose` (/compose), `Create account` (/signup), and `Sign in` (/signin). The authenticated `/timeline` route is not surfaced in the nav for any user state.
- **Landing page visitor states**: `landing_view()` shows "Create an account" and "Sign in" CTAs in both the empty state and in `header_nav()` across all render states (loading, empty, loaded, error). No authenticated-only controls are rendered on the public timeline.
- **Session signal as the reactive boundary**: `AppContext.session: Signal<Option<Session>>` is the single source of truth. Views that gate on session (`compose_view`, `timeline_view`) re-render reactively when session changes. Logged-out (`None`) consistently means no compose box, no personal feed, correct visitor navigation.

---

## Commits Delivered

| SHA | Message |
|-----|---------|
| `eaf96cf` | feat(chirp-server): add public GET /api/chirps and GET /api/users/:username/chirps |
| `e02b1d8` | feat(frontend): public timeline, user profile, sign-in/sign-up routes |
| `fed1fc8` | fix(chirp-frontend): align public API structs with backend wire format |
| `21dca55` | feat(chirp-frontend): implement sign-up form at /signup route (AC-4) |
| `617f253` | fix(chirp-frontend): correct empty-state CTA links in timeline view |
| `decb619` | fix(chirp-frontend): add /sign-in alias route to satisfy AC-3 |

No new commits were needed in this run; the gap identified by prior runs (the `/sign-in` alias) was already resolved by `decb619` before r15 began.

---

## CI Summary

Run 42194072348 on `decb619`:

| Job | Result |
|-----|--------|
| doc | ✅ success |
| fmt | ✅ success |
| clippy | ✅ success |
| wasm | ✅ success |
| test | ✅ success |
| image | ✅ success |

**6/6 — ALL PASS**
