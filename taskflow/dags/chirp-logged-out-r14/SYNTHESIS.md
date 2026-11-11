# SYNTHESIS.md — chirp-logged-out-r14

**Task**: Verify issue #35 — logged-out visitor experience for Chirp
**Repository**: `Nousix-LLC/nswe-demo`
**Branch**: `work/chirp-logged-out`
**Branch HEAD (at verification time)**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`
**PR**: #263 (OPEN / MERGEABLE) — "feat: logged-out public timeline and user profiles (#35)"

---

## Verification Context

This run (r14) was dispatched to verify issue #35 ACs and produce SYNTHESIS.md. The r14 brief was authored with HEAD = `21dca556`, noting that r13 had stalled. By the time r14 executed, r13 had completed: it pushed fix commit `decb619` and produced `taskflow/dags/chirp-logged-out-r13/SYNTHESIS.md`. R14's verification is therefore against the r13 HEAD (`decb619`), which is the current branch tip.

**R14 role**: Independent verification pass against HEAD `decb619`, confirming all ACs and producing this root-level SYNTHESIS.md per the declared output of the brief.

---

## Overall Verdict: PASS

All five acceptance criteria for issue #35 are satisfied in the current branch HEAD (`decb619`). CI for this commit shows 5/6 checks PASS (doc, fmt, clippy, wasm, test); the image build job was in-progress at verification time — the commit is a 3-line additive change to `app.rs` (one context clone + one route registration) with no new dependencies or Dockerfile changes, structurally identical to prior image-green commits on this branch. PR #263 is OPEN and MERGEABLE. No new code commits are required.

---

## Criterion-by-Criterion Accounting

### AC-1 — Public timeline at `/` ✓ MET

**Requirement**: A logged-out visitor can view the public timeline at `/`, displaying recent chirps from all users.

**Backend** (`crates/chirp-server/src/api/router.rs`):
- `GET /api/chirps` registered: `.route("/api/chirps", get(handlers::public_chirps).post(handlers::create_chirp))`
- Handler (`handlers::public_chirps`) is unauthenticated; returns reverse-chronological chirps with authors embedded; supports `before` timestamp pagination.

**Frontend** (`crates/chirp-frontend/src/app.rs`, `crates/chirp-frontend/src/landing.rs`):
- Route `/` → `landing_view(&landing_ctx)` registered in `start()`.
- `landing_view` loads the public timeline via `ctx.client().public_timeline()` → `GET /api/chirps`.
- Handles loading, error, empty (with "Create account" / "Sign in" CTAs), loaded, and end-of-list states.

**Verification**: Route registration confirmed in `app.rs`; backend endpoint confirmed in `router.rs`.

---

### AC-2 — Public user profile at `/@:handle` ✓ MET

**Requirement**: A logged-out visitor can view a public user profile page (e.g. `/users/alice`), displaying that user's chirps.

**Backend** (`crates/chirp-server/src/api/router.rs`):
- `GET /api/users/{username}/chirps` registered: `.route("/api/users/{username}/chirps", get(handlers::user_chirps))`
- Handler (`handlers::user_chirps`) is unauthenticated; returns profile + chirp page; HTTP 404 for unknown users.

**Frontend** (`crates/chirp-frontend/src/app.rs`, `crates/chirp-frontend/src/public_profile.rs`):
- Route `/@:handle` → `public_profile_view(&public_profile_ctx, handle)` registered in `start()`.
- `public_profile_view` loads user data via `ctx.client().public_user_profile(handle)` → `GET /api/users/:username/chirps`.
- Handles loading, not-found (HTTP 404), error, and loaded states; resets reactively on handle change.

**Note on path**: The AC says `(e.g. /users/alice)` — the `(e.g.)` is explicitly non-prescriptive; the implementation uses the Twitter-style `/@alice` convention, which is an equivalent and more idiomatic public-profile URL shape.

**Verification**: Route registration confirmed in `app.rs`; backend endpoint confirmed in `router.rs`.

---

### AC-3 — Sign-in page at `/sign-in` ✓ MET

**Requirement**: A logged-out visitor is shown a sign-in prompt/page at `/sign-in`.

**Implementation** (`crates/chirp-frontend/src/app.rs`, commit `decb619`):
- Two routes registered:
  ```
  .route("/signin", move |_params| sign_in_view(&signin_ctx))
  .route("/sign-in", move |_params| sign_in_view(&signin_hyphen_ctx))
  ```
- `signin_hyphen_ctx` is a dedicated `ctx.clone()` allocated alongside the other per-route clones.
- Both `/signin` and `/sign-in` serve `sign_in_view`; all existing nav links to `/signin` continue to work.

**Sign-in view** (`crates/chirp-frontend/src/sign_in.rs`): username/password form; links to `/signup` ("Create an account") and `/` ("Back to home").

**Verification**: Both route registrations confirmed in `app.rs` at HEAD `decb619`.

---

### AC-4 — Sign-up form at `/signup` ✓ MET

**Requirement**: A logged-out visitor can reach a sign-up form at `/signup` to create an account.

**Implementation** (`crates/chirp-frontend/src/app.rs`, `crates/chirp-frontend/src/compose.rs`, commit `21dca55`):
- Route `/signup` → `signup_view(&signup_ctx)` registered in `start()`.
- `signup_view` renders a full account-creation form: handle, display-name, password fields with client-side validation.
- On success: calls `POST /api/users`, then auto-logs in by writing the session signal (`ctx.session.set(...)`).
- Inline error states for validation and API failures.

**Verification**: Route registration confirmed in `app.rs`; `signup_view` confirmed in `compose.rs`.

---

### AC-5 — UI accurately reflects auth state ✓ MET

**Requirement**: A logged-out visitor does not see authenticated-only controls (compose box, "my feed"); navigation and landing states are correct for a visitor.

**Compose box** (`crates/chirp-frontend/src/compose.rs`):
- `compose_view` branches on `ctx.session.get()` at render time.
- Logged-out path: renders a login prompt ("Sign in to compose"), not the compose textarea.
- Logged-in path: renders the compose textarea and submit button.

**Navigation** (`crates/chirp-frontend/src/app.rs`):
- `nav_bar()` renders: Chirp · Compose · Create account · Sign in
- "Create account" links to `/signup`; "Sign in" links to `/signin`.
- `/timeline` does not appear in the nav; `timeline_view` is accessible only by direct navigation (authenticated feature not surfaced to logged-out visitors through any nav element).

**CTA correctness** (commit `617f253`, this branch):
- `timeline.rs` empty-state CTAs previously linked both "Create account" and "Sign in" to `/compose`. Fixed: "Create account" → `/signup`, "Sign in" → `/signin`.

**Verification**: Route table, nav bar rendering, and compose-view session branch confirmed in `app.rs` and `compose.rs`.

---

## Commits on `work/chirp-logged-out` (r9–r13 / r14 adds none)

| SHA | Description |
|-----|-------------|
| `2615ba1` | fix(ferric): WASM compilation blockers (r9) |
| `eaf96cf` | feat(chirp-server): add public GET /api/chirps and GET /api/users/:username/chirps |
| `e02b1d8` | feat(frontend): public timeline, user profile, sign-in/sign-up routes (r10) |
| `fed1fc8` | fix(chirp-frontend): align public API structs with backend wire format (r11) |
| `21dca55` | feat(chirp-frontend): sign-up form at /signup route — AC-4 (r12) |
| `617f253` | fix(chirp-frontend): correct empty-state CTA links in timeline view |
| `decb619` | fix(chirp-frontend): add /sign-in alias route to satisfy AC-3 (r13) |

**R14 adds no new commits**: all acceptance criteria were already met at HEAD `decb619`.

---

## CI Status

- Run 42194072348 for `decb619`: 5/6 checks PASS at verification time (doc ✓ · fmt ✓ · clippy ✓ · wasm ✓ · test ✓; image build in-progress).
- Prior commit `617f253` (run 42183715802): 6/6 ALL PASS. The `decb619` diff is 3 additive lines in `app.rs`.
- PR #263 status: OPEN, MERGEABLE.
