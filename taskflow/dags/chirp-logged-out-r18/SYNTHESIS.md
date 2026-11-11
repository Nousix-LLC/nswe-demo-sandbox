# SYNTHESIS.md — chirp-logged-out-r18

**Verdict: PASS**

All five acceptance criteria for issue #35 are met on branch `work/chirp-logged-out`
at HEAD `decb6196c2c1e6ed421d393a642f0c844cc333ba`. CI: 6/6 checks PASS (fmt, clippy,
test, wasm, doc, image — workflow run 42194072348). PR #263 is MERGEABLE.

---

## Per-AC Status

### AC-1 — Logged-out visitor can read the public timeline and user profiles without forced auth

**Status: MET**

Evidence:
- `crates/chirp-server/src/api/handlers.rs`: `public_chirps` (line 167) handles
  `GET /api/chirps` and `user_chirps` (line 200) handles `GET /api/users/{username}/chirps`
  — both are unauthenticated (no `AuthUser` extractor).
- `crates/chirp-server/src/api/router.rs`: those routes are mounted without auth
  middleware; the SPA fallback (`ServeDir`) serves `index.html` for all unmatched paths.
- `crates/chirp-frontend/src/app.rs`: `/` → `landing_view` and `/@:handle` →
  `public_profile_view` are registered without any auth gate. `AppContext::client()` builds
  an unauthenticated `ApiClient` when `session` is `None`.

No auth wall exists on the read path for logged-out visitors.

---

### AC-2 — Empty-state landing tells visitors what Chirp is and how to join

**Status: MET**

Evidence:
- `crates/chirp-frontend/src/landing.rs` `empty_view()` (called when
  `model.loaded && model.chirps.is_empty()`): renders a `chirp-landing-empty` section
  containing `<h2>Welcome to Chirp</h2>`, a description paragraph ("Chirp is a place to
  share short thoughts…"), and CTA links to `/signup` ("Create an account") and `/signin`
  ("Sign in").
- Unit test `empty_model_renders_welcome_statement_and_cta_links` asserts the welcome
  heading and CTA links are present in the empty state.

Blank-page or unexplained-error on first arrival with no content is not possible: the
state machine transitions from loading → empty with a fully-labelled view.

---

### AC-3 — Timeline load failure shows a clear, recoverable error instead of a broken screen

**Status: MET**

Evidence:
- `crates/chirp-frontend/src/landing.rs` `view_tree()`: when `!model.loaded &&
  model.error.is_some()`, renders `error_banner()` (a `<p role="alert">` with the
  user-readable message) plus a "Retry" button that re-triggers the load.
- `footer()`: when a continuation ("Load more") request fails, renders the error message
  plus a "Try again" button — the existing list remains visible.
- Unit test `initial_error_renders_error_message_and_retry_button` covers the initial
  error path.

---

### AC-4 — "Create an account" is visible on landing and sign-in screen and routes to sign-up

**Status: MET**

Evidence:
- `crates/chirp-frontend/src/landing.rs` `header_nav()`: present in every rendered tree;
  includes "Create account" → `/signup` and "Sign in" → `/signin` regardless of state.
  Unit test `every_state_includes_header_nav_links` asserts both links appear in loading,
  loaded, empty, and error states.
- `crates/chirp-frontend/src/sign_in.rs` `sign_in_view()` (line 68):
  `.child(link("/signup", "Create an account"))` — "New to Chirp? Create an account"
  link → `/signup`. Unit test `sign_in_view_contains_link_to_signup` asserts this.
- `crates/chirp-frontend/src/app.rs`: `/signup` → `signup_view` is a registered route;
  `signup_view` renders the sign-up form (commit `21dca556`).
- Also: `/sign-in` alias → `sign_in_view` added in commit `decb619` so deep-links to the
  hyphenated variant also work.

---

### AC-5 — Landing exercises loading, empty, error, and end-of-list states accurately and distinctly

**Status: MET**

Evidence:
`LandingModel` in `crates/chirp-frontend/src/landing.rs` is a one-state-machine: a
single `model` value drives all rendering through `view_tree()`. The four required states
plus extras are all distinct:

| State | Model condition | Rendered content |
|-------|-----------------|------------------|
| Loading | `!loaded && error.is_none()` | `<p class="chirp-loading">Loading…</p>` |
| Initial error | `!loaded && error.is_some()` | alert banner + "Retry" button |
| Empty | `loaded && chirps.is_empty()` | "Welcome to Chirp" + join CTAs |
| Loaded with more | `loaded && !chirps.is_empty() && has_more` | chirp list + "Load more" |
| Loading more | `loading_more = true` | "Loading more…" indicator |
| End of list | `loaded && !has_more && !loading_more` | "You're all caught up." |
| Continuation error | `loaded && error.is_some()` (footer) | error message + "Try again" |

Six unit tests cover all of these states:
`unloaded_model_renders_loading_state`,
`every_state_includes_header_nav_links`,
`empty_model_renders_welcome_statement_and_cta_links`,
`loaded_model_renders_chirp_list_and_load_more_button`,
`last_page_renders_end_note_not_load_more`,
`initial_error_renders_error_message_and_retry_button`.

---

## Commits on branch (since original r10 base)

| SHA | Description |
|-----|-------------|
| `eaf96cf` | Backend: unauthenticated public timeline + user chirp endpoints |
| `e02b1d8a` | Frontend: public timeline landing view + user profile route |
| `fed1fc8e` | Fix: loading/empty/error state rendering corrections |
| `21dca556` | Frontend: sign-up form and AC-4 create-account route |
| `617f253` | Fix: empty-state CTA links in landing view |
| `decb619` | Add `/sign-in` alias route for hyphenated deep-links |

All six commits are on `work/chirp-logged-out`; no commits were modified or reverted
by this run.

---

## CI

Workflow run 42194072348 on HEAD `decb6196` — all checks PASS:
`fmt` ✓  `clippy` ✓  `test` ✓  `wasm` ✓  `doc` ✓  `image` ✓

---

## Disposition

No code gaps were found. The branch satisfies all five ACs as stated in issue #35.
PR #263 is open, MERGEABLE, and passing CI. No additional commits are required.
