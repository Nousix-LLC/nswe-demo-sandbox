# SYNTHESIS.md — Chirp Logged-Out Visitor Experience (r8)

## Acceptance Criteria Verification

### AC-1 (REQ-PROD-013): Public timeline and user profiles without auth
Status: **PASS**
Evidence: `chirp-server` registers two handlers with no `AuthUser` extractor:
- `public_chirps(State, Query)` → `GET /api/chirps` — no bearer token required
- `user_chirps(State, Path, Query)` → `GET /api/users/{username}/chirps` — no bearer token required

Existing authenticated handlers (`create_chirp`, `timeline`, `follow`, `unfollow`, `like`, `unlike`) retain their `AuthUser(…): AuthUser` extractor and are unaffected. The opt-in extractor pattern means omitting it at the handler signature is sufficient to make a route unauthenticated.

---

### AC-2 (REQ-PROD-014): Empty-state landing
Status: **PASS**
Evidence: `chirp-frontend/src/landing.rs::empty_view()` renders a `chirp-landing-empty` div containing:
- `<h2>Welcome to Chirp</h2>`
- `<p class="chirp-landing-description">Chirp is a place to share short thoughts and follow people you find interesting.</p>`
- CTA links: `link("/signup", "Create an account")` and `link("/signin", "Sign in")`

This state fires when `model.loaded == true && model.chirps.is_empty()`. Unit test `empty_model_renders_welcome_statement_and_cta_links` asserts the welcome copy and both links are present.

---

### AC-3 (REQ-PROD-014): Error state
Status: **PASS**
Evidence: `chirp-frontend/src/landing.rs::view_tree()` renders a `chirp-landing-error` div when `!model.loaded && model.error.is_some()`, containing:
- `error_banner()`: `<p class="chirp-error" role="alert">{error.user_message()}</p>`
- `button("Retry", on_retry)`: re-triggers the initial load

Unit test `initial_error_renders_error_message_and_retry_button` asserts both the error message and "Retry" button are present.

---

### AC-4 (REQ-PROD-015): Sign-up navigation
Status: **PASS**
Evidence:
- **Global nav**: `app.rs::nav_bar()` renders `link("/signup", "Create account")` and `link("/signin", "Sign in")` on every route via the shared app shell.
- **Landing header**: `landing.rs::header_nav()` renders the same two links within every landing state (loading, empty, error, loaded) via the `chirp-landing-nav` div.
- **Route reachability**: `/signup` → `compose::signup_view` (fully functional account creation + auto-login); `/signin` → `sign_in::sign_in_view` (reachable stub with form inputs, full auth pending a future sprint).
- Unit test `every_state_includes_header_nav_links` asserts both links are present regardless of load state.

---

### AC-5 (REQ-UX-002/030-032): Distinct states
Status: **PASS**
Evidence: `landing.rs` implements four visually distinct CSS-class-gated states, never blank or stale:

| State | Trigger | CSS class |
|---|---|---|
| Loading | Initial fetch in flight | `chirp-loading` |
| Empty | `loaded=true`, `chirps.is_empty()` | `chirp-landing-empty` |
| Error | `!loaded`, `error.is_some()` | `chirp-landing-error` |
| Loaded | `loaded=true`, chirps present | `chirp-landing-loaded` / `chirp-list` |

Footer sub-states within Loaded: "Load more" button (`has_more=true`), "Loading more…" (`loading_more=true`), "You're all caught up." (`has_more=false`).

`public_profile.rs` additionally provides 6 distinct states: loading, not-found (404), error, loaded-empty, loaded-with-chirps, end-of-list.

Unit tests: `unloaded_model_renders_loading_state`, `empty_model_renders_welcome_statement_and_cta_links`, `initial_error_renders_error_message_and_retry_button`, `last_page_renders_end_note_not_load_more`, `loaded_model_renders_chirp_list_and_load_more_button`.

---

## Wiring Verification

**URL alignment (PASS)**:
- `api.rs::public_timeline()` calls `.get("/chirps")` with `before`/`limit` query params → matches backend `GET /api/chirps` with `PublicTimelineQuery { before: Option<i64>, limit: Option<u32> }`
- `api.rs::public_user_profile(username, …)` calls `.get(&format!("/users/{username}/chirps"))` → matches backend `GET /api/users/{username}/chirps`

**Shape alignment (PASS)**:
- Backend `PublicChirp { id: ChirpId, content, author: PublicAuthor { username, display_name }, created_at: i64 (ms epoch), like_count: u64 }` matches frontend `PublicChirp { id: u64, content, author: PublicAuthor, created_at: i64, like_count: u64 }`
- Backend `PublicTimelineResponse { chirps, has_more }` matches frontend struct exactly
- Backend `PublicUserProfile { username, display_name, bio, chirp_count }` matches frontend `PublicUserInfo` exactly
- Backend `PublicUserChirp { id, content, created_at, like_count }` matches frontend struct exactly
- Serialization: both sides use `#[serde(rename_all = "camelCase")]`; timestamps are `i64` ms-epoch on both sides

**Dead-code check (PASS)**: Both new backend routes are exercised — `GET /api/chirps` by `landing.rs` and `GET /api/users/{username}/chirps` by `public_profile.rs`.

---

## Duplication Check

The public response types (`PublicChirp`, `PublicAuthor`, `PublicTimelineResponse`, `PublicUserInfo`, `PublicUserChirp`, `PublicUserResponse`) are defined in `chirp-frontend/src/api.rs` rather than in `chirp-types`. The comment in `api.rs` notes this is intentional: "Defined here (not in chirp-types) because they serve only the two new unauthenticated endpoints." The backend types are in `chirp-types/src/api.rs`; the frontend mirrors their shapes locally. The two sets are structurally equivalent (verified by shape alignment above). This is a deliberate scoping decision, not an accidental duplication, and does not violate any project constraint.

---

## CI Status

| Check | Command | Result |
|---|---|---|
| `cargo fmt` | `cargo fmt --all --check` | **PASS** |
| `cargo clippy` | `cargo clippy --workspace --all-targets --locked -- -D warnings` | **PASS** |
| `cargo test` | `cargo test --workspace --locked` | **PASS** |
| `cargo wasm` | `cargo build -p chirp-frontend --target wasm32-unknown-unknown --locked` | **PASS** |
| `cargo doc` | `RUSTDOCFLAGS="-D warnings" cargo doc --workspace --no-deps --locked` | **PASS** |
| `image build` | `docker build .` | **PASS** |

All six checks run against `work/chirp-logged-out` HEAD `617f253`.

---

## PR

- URL: https://github.com/Nousix-LLC/nswe-demo/pull/263
- Title: `feat: logged-out visitor experience (public timeline, profiles, landing states)`
- Base: `main` ← `work/chirp-logged-out`
- Body includes: `Closes #35`
- State: OPEN

---

## Gate Decision: PASS

All five acceptance criteria are met with code evidence. All six CI checks pass. The PR is open and targets `main` with `Closes #35` in the body.

## Remediation Required

None.
