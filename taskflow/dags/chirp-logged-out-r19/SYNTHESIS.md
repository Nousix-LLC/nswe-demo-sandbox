# SYNTHESIS.md — chirp-logged-out-r19

**Verdict: PASS**

All five acceptance criteria for issue #35 (Logged-out reading and a useful landing with
accurate states) are MET at branch HEAD `decb6196c2c1e6ed421d393a642f0c844cc333ba` on
`work/chirp-logged-out`. CI is green, no new commits were required during this round (r19
confirms the r18 PASS verdict with no regressions), and PR #263 remains OPEN/MERGEABLE/CLEAN.

---

## Per-AC Status

### AC-1 — Logged-out visitor can read the public timeline and user profiles without forced auth
**Status: MET**
Evidence: Backend: `crates/chirp-server/src/api/handlers.rs` line 167 defines `public_chirps`
(no `AuthUser` extractor) handling `GET /api/chirps`, and line 200 defines `user_chirps`
(no `AuthUser` extractor) handling `GET /api/users/{username}/chirps`. Both are mounted
in `router.rs` with `get(handlers::public_chirps)` and `get(handlers::user_chirps)` with
no auth middleware. Frontend: `crates/chirp-frontend/src/app.rs` registers `/` →
`landing_view` and `/@:handle` → `public_profile_view` with no auth gate; `AppContext::client()`
builds an unauthenticated `ApiClient` when `session` is `None`. Logged-out visitors reach
both the public timeline and user profile routes without forced authentication.

---

### AC-2 — Empty-state shows Chirp description + sign-up/sign-in CTA — never blank or error
**Status: MET**
Evidence: `crates/chirp-frontend/src/landing.rs` `empty_view()` is called when
`model.loaded && model.chirps.is_empty()` and renders a `chirp-landing-empty` section
containing `<h2>Welcome to Chirp</h2>`, a description paragraph ("Chirp is a place to
share short thoughts and follow people you find interesting."), and CTA links to `/signup`
("Create an account") and `/signin` ("Sign in"). Unit test
`empty_model_renders_welcome_statement_and_cta_links` asserts the welcome heading and both
CTA links are present. Blank-page or unexplained state on empty first visit is impossible:
the state machine transitions loading → empty with a fully-labelled explanatory view.

---

### AC-3 — Timeline load failure shows a clear, recoverable message instead of a broken screen
**Status: MET**
Evidence: `crates/chirp-frontend/src/landing.rs` `view_tree()`: when `!model.loaded &&
model.error.is_some()`, renders `error_banner()` (a `<p role="alert">` with the
user-readable message) plus `button("Retry", on_retry)`. The existing list remains
visible in the loaded+error case. `footer()`: when a continuation request fails
(`model.error.is_some()` and `model.loaded`), renders `error_banner()` plus
`button("Try again", on_load_more)`. Unit test
`initial_error_renders_error_message_and_retry_button` covers the initial error path.
No broken or blank screen is possible on load failure; the error state is always
recoverable via the displayed action button.

---

### AC-4 — "Create an account" is visible on landing/sign-in and routes to sign-up
**Status: MET**
Evidence: `crates/chirp-frontend/src/landing.rs` `header_nav()` is called unconditionally from
`view_tree()` in every state, rendering `link("/signup", "Create account")` and
`link("/signin", "Sign in")`. Unit test `every_state_includes_header_nav_links` asserts
both links in loading, empty, error, and loaded states. `crates/chirp-frontend/src/sign_in.rs`
line 68: `link("/signup", "Create an account")` — "New to Chirp?" CTA present on the
sign-in screen, with unit test `sign_in_view_contains_link_to_signup`. `app.rs` line 148:
`.route("/signup", move |_params| signup_view(&signup_ctx))` — `/signup` is a registered
route that renders the full sign-up form.

---

### AC-5 — The four states (loading, empty, error, end-of-list) are implemented as distinct UI states
**Status: MET**
Evidence: `crates/chirp-frontend/src/landing.rs` `LandingModel` is a single struct (`loaded`,
`chirps`, `has_more`, `loading_more`, `error`) that drives all rendering through
`view_tree()`. The four required states are distinct and exhaustive: loading
(`!loaded && error.is_none()` → `<p class="chirp-loading">Loading…</p>`), initial
error (`!loaded && error.is_some()` → alert banner + "Retry" button), empty
(`loaded && chirps.is_empty()` → "Welcome to Chirp" + join CTAs), and end-of-list
(`loaded && !has_more && !loading_more` in `footer()` → "You're all caught up.").
Six unit tests cover all states: `unloaded_model_renders_loading_state`,
`every_state_includes_header_nav_links`, `empty_model_renders_welcome_statement_and_cta_links`,
`loaded_model_renders_chirp_list_and_load_more_button`, `last_page_renders_end_note_not_load_more`,
`initial_error_renders_error_message_and_retry_button`.

---

## CI Status

**PASS** — CI run confirmed green at HEAD `decb6196c2c1e6ed421d393a642f0c844cc333ba`.
PR #263 is OPEN/MERGEABLE/CLEAN. All checks passed (consistent with r18 CI run 42194072348).

---

## Commits on Branch

None — no new commits were added during r19. The branch remains at HEAD
`decb6196c2c1e6ed421d393a642f0c844cc333ba` (same as r18).

---

## Disposition

No code gaps found. All five acceptance criteria are MET at the current HEAD. No
remediation was required. PR #263 on `work/chirp-logged-out` is ready for merge.

---

## Contract Verification (Four-Check Gate)

| Check | Result |
|-------|--------|
| Ownership coverage — `ac-verdicts.yaml` exists and owned by `SUBTASK_ac-verify-remediate` | ✓ PASS |
| Ownership coverage — `SYNTHESIS.md` authored by `SUBTASK_synthesis` | ✓ PASS |
| Ownership respect — no cross-ownership violations detected | ✓ PASS |
| Identity: `ac-verdicts.yaml` contains exactly AC-1 through AC-5 | ✓ PASS |
| Identity: each entry has `verdict: MET \| NOT-MET` | ✓ PASS |
| Identity: `SYNTHESIS.md` references all verdicts and carries overall verdict | ✓ PASS |
| **Overall verdict** | **PASS** |
