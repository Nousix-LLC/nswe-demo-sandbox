# SYNTHESIS — Chirp Logged-Out Visitor Experience (r7)

**Gate decision**: PASS — all five acceptance criteria are met; PR exists and is open  
**PR**: https://github.com/Nousix-LLC/nswe-demo/pull/263 (`Closes #35` confirmed in body)  
**Branch**: `work/chirp-logged-out`

---

## Per-AC Verdicts

### AC-1 — Public timeline and user profiles without forced sign-in

**Verdict: MET**

Evidence:
- `landing.rs` calls `GET /api/chirps` via `ApiClient::public_timeline(before, limit)`. The
  client is built with no `Authorization` header; no `AuthUser` extractor is present on the
  `public_chirps` handler in `handlers.rs`.
- `public_profile.rs` calls `GET /api/users/{username}/chirps` via
  `ApiClient::public_user_profile(username, before, limit)`. Likewise no auth header; the
  `user_chirps` handler has no `AuthUser` parameter.
- Chirp items in the landing view link each author's display name to `/@{username}`, making
  every public user profile reachable from the timeline.
- Verified live: `cargo test -p chirp-server` integration test
  `public_timeline::public_timeline_requires_no_auth` returns HTTP 200 with no
  `Authorization` header.

### AC-2 — Empty-timeline state shows "what Chirp is" plus sign-up/sign-in CTA

**Verdict: MET**

Evidence:
- `landing.rs` `empty_view()` renders `<div class="chirp-landing-empty">` containing:
  - `<h2>Welcome to Chirp</h2>`
  - Description paragraph: "Chirp is a place to share short thoughts and follow people you
    find interesting."
  - CTA `<div class="chirp-landing-cta">` with `link("/signup", "Create an account")` and
    `link("/signin", "Sign in")`
- Code path: `LandingModel.loaded == true && chirps.is_empty()` → `empty_view()`.
- Server confirms: `GET /api/chirps` on an empty store returns `200 { chirps: [], has_more: false }`,
  not an error; the frontend correctly treats `chirps.is_empty()` as the empty state.
- Test: `empty_model_renders_welcome_statement_and_cta_links` PASS.

### AC-3 — Timeline load failure shows clear, recoverable error message

**Verdict: MET**

Evidence:
- `landing.rs` error state renders `<p class="chirp-error" role="alert">` with
  `AppError::user_message()` (plain language; no raw HTTP codes or Rust panics) plus a
  `<button type="button">Retry</button>` that calls `reload()`, which resets `LandingModel`
  and re-fetches the first page in-place.
- Two distinct error paths: initial fetch failure (full-screen error before first load) and
  continuation error (inline below the already-loaded list).
- Test: `initial_error_renders_error_message_and_retry_button` PASS.

### AC-4 — "Create an account" route visible on landing and sign-in screen; following it reaches sign-up

**Verdict: MET**

Evidence:
- `app.rs` `nav_bar()` renders `link("/signup", "Create account")` and `link("/signin", "Sign
  in")` on every page, above the route outlet.
- `landing.rs` `header_nav()` renders `link("/signup", "Create account")` and
  `link("/signin", "Sign in")` inside the landing section for every landing state (loading,
  empty, error, loaded).
- `sign_in.rs` renders `link("/signup", "Create an account")` as a visible CTA.
- `/signup` route is registered in `app.rs` and resolves to `signup_view` from `compose.rs`
  (a full account-creation form stub), so the route is reachable and returns a usable page.
- Tests: `every_state_includes_header_nav_links` PASS; `sign_in_view_contains_link_to_signup`
  PASS.

### AC-5 — Loading, empty, error, and end-of-list states are visually distinct

**Verdict: MET**

Evidence — four distinct CSS classes and content in `landing.rs`:

| State | CSS class | Content |
|-------|-----------|---------|
| Loading | `chirp-loading` | `Loading…` paragraph |
| Empty | `chirp-landing-empty` | "Welcome to Chirp" h2 + description + CTA |
| Error | `chirp-landing-error` | `role="alert"` message + "Retry" button |
| Loaded | `chirp-landing-loaded` | Keyed chirp list |
| End-of-list | `chirp-end` (in footer) | "You're all caught up." |

No state renders a blank page; each has its own class and non-empty content.

`public_profile.rs` additionally handles 6 states (loading, not-found, empty, loaded, end-of-list, error), all distinct.

Tests: `unloaded_model_renders_loading_state`, `empty_model_renders_welcome_statement_and_cta_links`,
`initial_error_renders_error_message_and_retry_button`, `last_page_renders_end_note_not_load_more` all PASS.

---

## Four-Check Results

### Check 1 — Behavioral Contract Verification

**Result: PASS**

All five ACs verified as met with direct evidence from the source code (read on the
`work/chirp-logged-out` branch) and from the passing test suites.

### Check 2 — Wiring Verification

**Result: PASS**

- **api_coverage**: The frontend's new components (`landing.rs`, `public_profile.rs`) call
  exactly two endpoints: `GET /api/chirps` and `GET /api/users/{username}/chirps`. Both are
  declared in `backend-impl.md` and implemented in `handlers.rs`. No other unauthenticated
  API endpoints are called by the new components.
- **ac_coverage**: Every AC (AC-1 through AC-5) is covered by at least one implementation
  artifact (`landing.rs`, `public_profile.rs`, `app.rs`, `sign_in.rs`, `handlers.rs`). No
  AC is addressed by `analysis.md` alone without a corresponding implementation.
- **No unmatched calls**: confirmed by reading `api.rs` (the two new client methods) and
  cross-referencing with `router.rs` (both routes registered).

### Check 3 — Duplication Detection

**Result: PASS (minor observation documented)**

No behavioral duplication that affects AC compliance or CI.

Observation: `sign_up.rs` exports `sign_up_view` (a form stub) but this function is not
wired into the route table. The `/signup` route uses `signup_view` from `compose.rs` (the
full validated account-creation form). Both are compiled (declared in `lib.rs`) but only
`compose.rs::signup_view` is reachable. This is a minor dead-code/documentation discrepancy;
`cargo clippy -D warnings` does not flag it because the item is `pub`. No duplicate
endpoint, no duplicate state logic.

A pre-existing `GET /api/public/timeline` endpoint remains from before this branch; the new
`GET /api/chirps` endpoint returns a different response shape (embedded author info,
cursor-based pagination). They are distinct and not duplicates.

### Check 4 — Code Review / CI Gates

**Result: PASS**

| Gate | Command | Result |
|------|---------|--------|
| `fmt` | `cargo fmt --check` (workspace) | ✓ PASS — no diff output |
| `clippy` | `cargo clippy -p chirp-frontend -- -D warnings` | ✓ PASS — 0 warnings |
| `test (frontend)` | `cargo test -p chirp-frontend` | ✓ PASS — 76/76 |
| `test (server unit)` | `cargo test -p chirp-server --lib` | ✓ PASS — 65/65 |
| `test (server integration)` | `cargo test -p chirp-server` (integration) | ✓ PASS — 26/26 integration, 1/1 concurrency, 3/3 doc |
| `wasm` | `cargo build -p chirp-frontend --target wasm32-unknown-unknown` | ✓ PASS |

Total: 171 tests pass, 0 fail.

---

## Contract Identity Verification

| Identity | Assertion | Verdict |
|----------|-----------|---------|
| `api_coverage` | Every public API endpoint that the frontend calls is a declared and implemented endpoint from SUBTASK_backend-api's output | **VERIFIED** — `GET /api/chirps` and `GET /api/users/{username}/chirps` are the only endpoints called by new frontend components; both appear in `backend-impl.md` and `router.rs` |
| `ac_coverage` | Each AC (AC-1 through AC-5) has a corresponding implementation artifact | **VERIFIED** — see per-AC verdicts above; all five ACs have source-code evidence |
| `ci_pass` | CI checks (fmt, clippy, test, wasm) pass on `work/chirp-logged-out` | **VERIFIED** — all gates ran and passed; see Check 4 table |

---

## PR

**URL**: https://github.com/Nousix-LLC/nswe-demo/pull/263  
**State**: OPEN  
**Branch**: `work/chirp-logged-out` → `main`  
**Closes issue**: `Closes #35` present as plain text in PR body  
**Attribution**: `🤖 Generated with [Claude Code](https://claude.com/claude-code)` present in PR body

---

## Remediation Items

None. All five ACs are met, all CI gates pass, and the PR is open with the required
`Closes #35` text.

Minor non-blocking observation: `sign_up.rs::sign_up_view` is compiled but not currently
mounted in the route table (the `/signup` route uses `compose.rs::signup_view`). This is
cosmetic dead code and does not affect any AC or CI gate. It is a candidate for removal or
wiring in a future authentication sprint.
