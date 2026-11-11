# Synthesis — chirp-logged-out-r10

## Verification Result: PASS

All five acceptance criteria for issue #35 (logged-out visitor experience) are satisfied at the
current branch HEAD. All six CI checks pass. PR #263 is open, conflict-free, and ready for review
and merge.

---

## Branch and PR State

| Field           | Value                                       |
|-----------------|---------------------------------------------|
| Branch          | `work/chirp-logged-out`                     |
| HEAD commit     | `617f25395eebe9475f19a90e0b1dac5921215ea3`  |
| PR              | #263 — `feat: logged-out public timeline and user profiles (#35)` |
| PR state        | OPEN / MERGEABLE / `Closes #35`             |
| CI run          | `runs/42183715802` — all 6 checks **pass**  |

### CI check summary

| Check   | Result     |
|---------|------------|
| fmt     | ✅ pass    |
| clippy  | ✅ pass    |
| test    | ✅ pass    |
| wasm    | ✅ pass    |
| doc     | ✅ pass    |
| image   | ✅ pass    |

---

## Commits Since r9 CI Base (2615ba1d)

r9 confirmed CI green at `2615ba1d`. Five further commits have landed since then, all by runs
after r9:

| SHA       | Message                                                            |
|-----------|--------------------------------------------------------------------|
| `eaf96cf` | feat(chirp-server): add public GET /api/chirps and GET /api/users/:username/chirps |
| `e02b1d8` | feat(frontend): public timeline, user profile, sign-in/sign-up routes |
| `fed1fc8` | fix(chirp-frontend): align public API structs with backend wire format |
| `21dca55` | feat(chirp-frontend): implement sign-up form at /signup route (AC-4) |
| `617f253` | fix(chirp-frontend): correct empty-state CTA links in timeline view |

---

## Acceptance-Criteria Verification

### AC-1 — Logged-out visitor can read the public timeline and user profiles without signing in

**PASS.**

- `crates/chirp-frontend/src/app.rs`: route `/` → `landing_view()` (no authentication guard).
  Route `/@:handle` → `public_profile_view()` (no authentication guard).
- `crates/chirp-server/src/api/router.rs`: `GET /api/chirps` and `GET /api/public/timeline` are
  registered as unauthenticated handlers (`handlers::public_chirps`, `handlers::public_timeline`).
  `GET /api/users/{username}/chirps` likewise requires no bearer token.
- Both `PostgresRepository` and `InMemoryRepository` implement `public_timeline()` and
  `get_user_chirps_by_username()`.

### AC-2 — On arrival with no content, visitor sees what Chirp is and an obvious way to sign up

**PASS.**

- `crates/chirp-frontend/src/landing.rs` `empty_view()` (line 287): renders a `.chirp-landing-empty`
  section that explains what Chirp is and provides prominent "Create an account" → `/signup` and
  "Sign in" → `/signin` CTA links. Test `empty_model_renders_welcome_statement_and_cta_links`
  asserts this directly.
- The persistent `nav_bar()` in `app.rs` renders "Create account" and "Sign in" links in every
  application state.

### AC-3 — Timeline load failure shows a clear, recoverable message

**PASS.**

- `landing.rs` `view_tree()`: when `model.error` is `Some`, the initial-error branch renders an
  error banner with a Retry callback (`on_retry`). Inline load-more errors also surface the banner.
- `public_profile.rs` mirrors the same pattern for user-profile load failures.
- Tests assert the error state is distinct from loading, empty, and loaded states.

### AC-4 — "Create an account" route visible on landing and on the sign-in screen; following it reaches sign-up

**PASS.**

- `app.rs` `nav_bar()`: always rendered (all routes); contains `link("/signup", "Create account")`
  and `link("/signin", "Sign in")`. Present in every application state.
- `crates/chirp-frontend/src/sign_in.rs` line 68: `link("/signup", "Create an account")` — the
  sign-in view explicitly links to sign-up.
- Route `/signup` → `signup_view()` in `compose.rs` (the full account-creation form).
- Test `sign_in_view_contains_link_to_signup` asserts this in `sign_in.rs`.

### AC-5 — Landing exercises loading, empty, error, and end-of-list states accurately and distinctly

**PASS.**

- `landing.rs` state machine (`LandingModel`) tracks `loaded`, `loading_more`, `error`, `has_more`,
  and `before_cursor` with explicit transitions. The `view_tree()` dispatch yields five visually
  distinct branches: initial-loading, initial-error, empty, loaded (with or without paginating),
  and end-of-list (when `!has_more`).
- `public_profile.rs` implements an analogous six-state model (loading, not-found, empty, loaded,
  end-of-list, error).
- 76 frontend unit tests cover all state transitions and render outputs for landing and
  public-profile; tests are grouped by state in the test modules.

---

## Test Coverage

| Crate             | Tests (native)  |
|-------------------|-----------------|
| `chirp-frontend`  | 76              |
| `chirp-server`    | 65 + 26 + 1 = 92 |
| Ferric crates     | 18 + 96 + 29 = 143 |
| **Total**         | **311**         |

All 311 tests pass locally (`cargo test --workspace`). CI `test` check confirms passage in the
wasm-aware environment.

---

## Remaining Blockers

None. The branch is implementation-complete, CI-green, and conflict-free. The PR awaits a human
review pass and merge.
