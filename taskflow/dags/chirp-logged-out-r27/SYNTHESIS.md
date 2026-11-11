# SYNTHESIS.md — chirp-logged-out-r27

## Verdict: PASS — both blockers fixed, all 5 acceptance criteria met, CI 6/6 green

PR #263 (`work/chirp-logged-out`, HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`) fixes both
single-line regressions and satisfies all 5 acceptance criteria for GitHub issue #35 ("Logged-out
reading and a useful landing with accurate states"). CI is fully green (fmt, clippy, test, wasm,
doc, image — 6/6). PR is OPEN and MERGEABLE.

---

## Blocker remediation

### Blocker 1 ✅ FIXED — Authenticated home timeline routes through personalized feed

**File**: `crates/chirp-frontend/src/timeline.rs`, line 218  
**Before (wrong)**: `let result = ctx.client().pub_timeline(&query).await;`  
**After (fixed)**: `let result = ctx.client().timeline(&query).await;`

`ctx.client().timeline(&query)` constructs an authenticated HTTP client (includes `self.token`)
and routes to the personalized `/api/timeline` feed. Authenticated users navigating to `/timeline`
now receive their following feed, not the global unauthenticated feed. The fix matches the module
doc at `timeline.rs:4`: *"route a `Page<Chirp>` through `ctx.client().timeline(..)`"*.

No `pub_timeline` call remains in `timeline.rs` (confirmed by grep).

---

### Blocker 2 ✅ FIXED — "Log in →" CTA on sign-up page routes to `/signin`

**File**: `crates/chirp-frontend/src/compose.rs`, line 519  
**Before (wrong)**: `link("/compose", "Log in →")`  
**After (fixed)**: `link("/signin", "Log in →")`

A user clicking "Log in →" from the sign-up page now reaches `/signin` as intended by the route
table. The `/compose` route is the authenticated chirp-compose view; it was an accidental target.

---

## Acceptance criteria

### AC-1 ✅ — Public timeline + user profiles accessible without login
**Requirement (REQ-PROD-013, BAR-011):** A logged-out visitor can load the home/public timeline and
open a user profile and read chirps without being forced to sign up or sign in first.

**Evidence (unchanged from r26 — not modified by these two fixes):**
- `GET /api/chirps` handler (`handlers.rs::public_chirps`): signature is `State(AppState)` +
  `Query` only — no auth extractor; no authentication middleware on this route.
- `GET /api/users/{username}/chirps` handler (`handlers.rs::user_chirps`): same pattern — only
  `State(AppState)`, `Path(username)`, and `Query` extractors; no auth extractor.
- Frontend: `/` renders `landing_view` which calls `GET /api/chirps`; `/@:handle` renders
  `public_profile_view` which calls `GET /api/users/:username/chirps`. Both routes are in the
  public (unauthenticated) router section of `app.rs`. No redirect to `/signin` from either view.

Blocker 1 fix is orthogonal to AC-1: `timeline.rs` is the *authenticated* timeline component (`/timeline`).
The public feed routes (`landing.rs` → `GET /api/chirps`, `public_profile.rs` →
`GET /api/users/:username/chirps`) are not touched by this fix.

---

### AC-2 ✅ — Clear landing with sign-up prompt on empty state
**Requirement (REQ-PROD-014, BAR-011):** On arrival with no content, the visitor sees a clear
statement of what Chirp is plus an obvious way to sign up or sign in — never a blank page or an
unexplained error.

**Evidence (unchanged from r26):**
- `landing.rs::empty_view`: renders only when `model.loaded && model.chirps.is_empty()`.
- Shows `<h2>Welcome to Chirp</h2>` — explicit product identity.
- CTA buttons: "Create an account" → `/signup` and "Sign in" → `/signin`.
- Neither `landing.rs` nor `empty_view` was touched by either blocker fix.

---

### AC-3 ✅ — Clear recoverable error message on timeline load failure
**Requirement (REQ-PROD-014, BAR-011):** If the timeline fails to load, a clear, recoverable message
is shown instead of a broken screen.

**Evidence (unchanged from r26):**
- `landing.rs::view_tree`: branch `!model.loaded && model.error.is_some()` → renders
  `error_banner()` (with `role="alert"` for accessibility) and a "Retry" button that re-triggers
  the fetch.
- `app.rs` registers both `/signin` and `/sign-in` (alias) routes.
- Neither `landing.rs` nor `error_banner` was touched by either blocker fix.

---

### AC-4 ✅ — "Create an account" route visible on landing AND sign-in screen; sign-up "Log in →" routes to `/signin`
**Requirement (REQ-PROD-015, BAR-011):** A "create an account" route is visible on the landing and
on the sign-in screen, and following it reaches sign-up. The sign-up page "Log in →" CTA must route
to `/signin`, not `/compose`.

**Evidence:**
- `app.rs::nav_bar()`: persistent navigation contains "Create account" → `/signup` and
  "Sign in" → `/signin` (unchanged).
- `landing.rs::header_nav()`: additional nav on landing with "Create account" → `/signup` present
  in ALL landing states (unchanged).
- `sign_in.rs::sign_in_view()`: renders "Create an account" → `/signup` with accompanying unit test
  `sign_in_view_contains_link_to_signup` (unchanged; test still passes — `test` check green).
- **Blocker 2 fix**: `compose.rs:519` now `link("/signin", "Log in →")` — the sign-up page "Log in
  →" CTA correctly routes to `/signin`. Verified by code inspection.

---

### AC-5 ✅ — Loading, empty, error, end-of-list states accurate and distinct
**Requirement (REQ-UX-002/030/031/032):** The logged-out landing/timeline exercises its loading,
empty, error, and end-of-list states accurately and distinctly.

**Evidence (unchanged from r26):**

| State | Trigger | Rendered output |
|---|---|---|
| Loading | `!loaded && error.is_none()` | `<p class="chirp-loading">Loading…</p>` |
| Error (pre-load) | `!loaded && error.is_some()` | `error_banner()` (role=alert) + Retry button |
| Empty | `loaded && chirps.is_empty()` | "Welcome to Chirp" header + description + CTAs |
| Loaded (has content) | `loaded && !chirps.is_empty()` | chirp list + `footer()` |
| End-of-list | `loaded && !has_more` (in `footer()`) | "You're all caught up." |
| Load-more in-flight | `loading_more` (in `footer()`) | loading spinner |
| Inline continuation error | `continuation_error.is_some()` (in `footer()`) | inline error + "Try again" |

Neither `landing.rs` nor `public_profile.rs` was modified by either blocker fix.

---

## CI status (HEAD `7f4b684`)

| Check | Status |
|---|---|
| fmt | ✅ pass |
| clippy | ✅ pass |
| test | ✅ pass |
| wasm | ✅ pass |
| doc | ✅ pass |
| image | ✅ pass |

Run: https://github.com/Nousix-LLC/nswe-demo/actions/runs/42249419769

---

## New HEAD on `work/chirp-logged-out`

`7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`

Commit message: `fix(chirp-frontend): revert auth timeline to personalized feed, fix signup Log-in link`

Previous HEAD (verified by r26): `decb6196c2c1e6ed421d393a642f0c844cc333ba`

---

## Recommendation

PR #263 is ready to merge. All 5 ACs are satisfied. Both blockers are fixed. CI is 6/6 green on
the new HEAD `7f4b684`. No further code changes needed.

Merge path: `gh pr merge 263 --squash --delete-branch -R Nousix-LLC/nswe-demo`
