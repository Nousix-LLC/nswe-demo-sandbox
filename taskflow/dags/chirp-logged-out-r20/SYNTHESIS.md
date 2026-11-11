# SYNTHESIS.md — chirp-logged-out-r20

**Verdict: PASS**

All five acceptance criteria for issue #35 (Logged-out reading and a useful landing with accurate states) are met at the current branch head `decb6196c2c1e6ed421d393a642f0c844cc333ba` on `work/chirp-logged-out`.

No code changes were required; the work from r10–r19 is complete and correct at this head. Zero commits added in r20.

---

## Verification Summary

### AC-1: Logged-out visitor can load the home/public timeline and open a user profile without being gated

**Status: MET**

Evidence:
- `app.rs` registers `/` → `landing_view` and `/@:handle` → `public_profile_view` with no auth gate — no session guard wraps either route entry point.
- `landing_view` (`crates/chirp-frontend/src/landing.rs`) calls `ctx.client().public_timeline(...)`, which builds a bare `Client` (no bearer token) against `GET /api/chirps`.
- `public_profile_view` (`crates/chirp-frontend/src/public_profile.rs`) calls `ctx.client().public_user_profile(...)`, which builds a bare `Client` against `GET /api/users/:username/chirps`.
- Both `handlers::public_chirps` and `handlers::user_chirps` in `chirp-server/src/api/handlers.rs` take only `State` and `Query`/`Path` extractors — no `BearerToken` or authentication extractor — confirming the endpoints are unauthenticated.

### AC-2: Empty-state landing explains what Chirp is and provides sign-up / sign-in entry points

**Status: MET**

Evidence — `empty_view()` in `landing.rs`:
- Renders `<h2>Welcome to Chirp</h2>`.
- Renders `<p class="chirp-landing-description">Chirp is a place to share short thoughts and follow people you find interesting.</p>` — a clear, non-technical description of the service.
- Renders `<div class="chirp-landing-cta">` containing `link("/signup", "Create an account")` and `link("/signin", "Sign in")` — prominent, correct entry points.
- Unit test `empty_model_renders_welcome_statement_and_cta_links` asserts all three elements.

The global nav bar additionally renders "Create account" and "Sign in" on every page, ensuring the visitor is never stranded.

### AC-3: Timeline load failure shows a clear, recoverable message

**Status: MET**

Evidence — `view_tree()` in `landing.rs`:
- Pre-load path, `model.error.is_some()` branch: renders `<div class="chirp-landing-error">` containing `error_banner(err.user_message())` (which sets `role="alert"`) and a `button("Retry", on_retry)`.
- The "Retry" handler calls `reload(ctx)`, which resets model state to initial and triggers a fresh API call — the error is recoverable.
- For post-load / inline continuation failures, `footer()` renders `<div class="chirp-load-more-error">` with an error banner and a "Try again" button.
- Unit test `initial_error_renders_error_message_and_retry_button` asserts the error message and Retry button are both present in the error state.

The commit `decb6196` added the `/sign-in` alias route; that commit's message references AC-3 but the error-handling implementation was already present from prior rounds. AC-3 is met independently.

### AC-4: "Create an account" route is visible from landing and sign-in screen, and reaches sign-up

**Status: MET**

Evidence:
- Landing view: `header_nav()` in `landing.rs` is rendered in every state branch of `view_tree`. It contains `link("/signup", "Create account")` and `link("/signin", "Sign in")`.
- Global nav bar in `app.rs`'s `nav_bar()` always shows `link("/signup", "Create account")` and `link("/signin", "Sign in")` above every route.
- Sign-in view (`sign_in.rs`): renders `link("/signup", "Create an account")` inside `<p class="chirp-signin-links">New to Chirp? Create an account</p>`. Unit test `sign_in_view_contains_link_to_signup` asserts this.
- `/signup` route is registered in `app.rs` and routes to `compose::signup_view` (`sign_up.rs`), which renders a `<section class="chirp-signup">` with a placeholder form titled "Create an account".

### AC-5: Loading, empty, error, and end-of-list states are implemented as distinct, accurate UI states

**Status: MET**

Evidence — `view_tree()` and `footer()` in `landing.rs`:

| State | Condition | CSS class | Distinguishing UI |
|---|---|---|---|
| **Loading** | `!model.loaded && model.error.is_none()` | `chirp-loading` | "Loading…" paragraph |
| **Error** | `!model.loaded && model.error.is_some()` | `chirp-landing-error` | Error banner (`role="alert"`) + "Retry" button |
| **Empty** | `model.loaded && model.chirps.is_empty()` | `chirp-landing-empty` | "Welcome to Chirp" headline + description + CTA links |
| **End-of-list** | `model.loaded && !model.chirps.is_empty() && !model.has_more && !model.loading_more && model.error.is_none()` | `chirp-end` | "You're all caught up." |

The four states are mutually exclusive (each is guarded by a distinct branch of the `view_tree` / `footer` decision trees). They carry distinct CSS classes and produce distinct UI elements. No two are conflated.

The `LandingModel` state machine is a single reduced model (not duplicated flag sets): transitions in `begin_initial`, `apply_initial`, `apply_more`, and `apply_error` keep the model internally consistent. The view derives its one active state from the model's current values without ambiguity.

Unit test coverage: each of the four states is covered by a dedicated test in `landing.rs`'s `#[cfg(test)]` block; all pass in CI run `42194072348`.

---

## CI Status

Branch head `decb6196c2c1e6ed421d393a642f0c844cc333ba`:
- `fmt`: ✓ SUCCESS
- `clippy`: ✓ SUCCESS
- `test`: ✓ SUCCESS
- `wasm`: ✓ SUCCESS
- `doc`: ✓ SUCCESS
- `image`: ✓ SUCCESS

PR #263 is OPEN / MERGEABLE / CLEAN.

---

## Commits added in r20

None. All acceptance criteria were already met at the branch head inherited from prior rounds. r20's contribution is this synthesis record and the confirmation that the work is complete.
