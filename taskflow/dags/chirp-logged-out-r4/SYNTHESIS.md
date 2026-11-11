# SYNTHESIS — Chirp Logged-Out Experience

**Subtree**: `chirp-logged-out-r4`  
**Synthesized at**: 2026-11-05  
**Branch**: `work/chirp-logged-out`  
**PR**: https://github.com/Nousix-LLC/nswe-demo/pull/263

---

## Verification Gate Results

### Check 1 — Wiring Verification

Evidence sources: `crates/chirp-server/src/api/router.rs`, `crates/chirp-server/src/api/handlers.rs`, `crates/chirp-frontend/src/app.rs`, `crates/chirp-frontend/src/landing.rs`.

- **GET /api/chirps**: PASS — registered as `get(handlers::public_chirps)` in router.rs; handler signature is `State(state): State<AppState>, Query(query): Query<PublicTimelineQuery>` with no `AuthUser` extractor.
- **GET /api/users/:username/chirps**: PASS — registered as `get(handlers::user_chirps)` in router.rs; handler signature is `State(state): State<AppState>, Path(username): Path<String>, Query(query): Query<PublicTimelineQuery>` with no `AuthUser` extractor.
- **Home route registered**: PASS — `.route("/", move |_params| landing_view(&landing_ctx))` in `app.rs::start()`.
- **User profile route registered**: PASS — `.route("/@:handle", move |params| { ... public_profile_view(...) })` in `app.rs::start()`.
- **Sign-up/sign-in navigation**: PASS — `nav_bar()` in `app.rs` renders "Create account" (→ `/signup`) and "Sign in" (→ `/signin`) links and is wrapped around the router outlet on **every** screen; `header_nav()` in `landing.rs` adds the same links within the landing view itself.

**Check 1 verdict: PASS** (all 5 assertions satisfied)

---

### Check 2 — Contract Verification

Evidence sources: `crates/chirp-types/src/api.rs` (backend DTOs), `crates/chirp-frontend/src/api.rs` (frontend deserialization structs), `crates/chirp-frontend/src/landing.rs`, `crates/chirp-frontend/src/public_profile.rs`.

- **Backend matches spec**: PARTIAL — Backend implements the correct route paths, response envelope structure (`chirps`, `has_more`, `user`), and field names. Three deviations from `contracts/public_api_spec.md` were intentional and documented in `SUBTASK_backend/COMPLETE.md`:
  1. `id` is a JSON number (`u64` via `ChirpId`) not a UUID string
  2. `created_at` is a JSON number (milliseconds since Unix epoch, `i64`) not an ISO 8601 string
  3. `before` query param is `Option<i64>` (ms since epoch) not an ISO 8601 string
  Additionally, all backend DTOs carry `#[serde(rename_all = "camelCase")]`, producing camelCase JSON keys (`createdAt`, `likeCount`, `hasMore`, `displayName`, `chirpCount`).

- **Frontend matches spec**: PARTIAL — Frontend structs match the spec's described types (String for `id`, String for `created_at`) and use Rust's default snake_case field names for JSON keys. Because the spec was written with string types and no camelCase note, the frontend is spec-conformant but **not wire-compatible with the backend's actual output**.

- **Cross-spoke wire compatibility**: **FAIL** — The backend serializes `id` as a JSON number and uses camelCase keys; the frontend expects `id: String` (type mismatch) and snake_case keys (name mismatch). Serde will produce deserialization errors for every API response at runtime. Specific mismatches:

  | JSON key backend sends | Frontend field name expected | Type backend sends | Type frontend expects | Issue |
  |------------------------|------------------------------|--------------------|-----------------------|-------|
  | `id` (number) | `id` | `u64` | `String` | Type mismatch |
  | `createdAt` (number) | `created_at` | `i64` (ms) | `String` (ISO 8601) | Key + type mismatch |
  | `likeCount` | `like_count` | `u64` | `u64` | Key name mismatch |
  | `hasMore` | `has_more` | `bool` | `bool` | Key name mismatch |
  | `displayName` | `display_name` | `Option<String>` | `Option<String>` | Key name mismatch |
  | `chirpCount` | `chirp_count` | `u64` | `u64` | Key name mismatch |

  **Fix-task injected**: `FIXTASK_frontend_contract` — update frontend structs with `#[serde(rename_all = "camelCase")]` and correct integer types.

- **Five states implemented distinctly**: PASS — Landing implements 5 required states (loading, empty, loaded, end-of-list, error) each with distinct CSS classes. Public profile implements 6 states (loading, not-found, empty, loaded, end-of-list, error). All states have dedicated tests.

**Check 2 verdict: FAIL** (wire-format mismatch — fix-task FIXTASK_frontend_contract injected)

---

### Check 3 — Acceptance Criteria

Evidence sources: `SUBTASK_backend/COMPLETE.md`, `SUBTASK_frontend/COMPLETE.md`, code inspection of `crates/chirp-server/src/api/handlers.rs`, `crates/chirp-frontend/src/app.rs`, `crates/chirp-frontend/src/landing.rs`.

- **AC-1** (no auth required for public timeline and profiles): **PASS** — Both `public_chirps` and `user_chirps` handlers carry no `AuthUser` extractor. Backend unit tests `public_chirps_returns_200_without_auth_and_empty_timeline` and `user_chirps_returns_200_for_existing_user_with_no_chirps` verify 200 responses are returned without any auth header.

- **AC-2** (empty state shows "what chirp is" + sign-up/sign-in route): **PASS** — `landing.rs` empty state renders `<div class="chirp-landing-empty">` with a "Welcome to Chirp" heading, description text, and CTA links to `/signup` ("Create an account") and `/signin` ("Sign in"). Test `empty_model_renders_welcome_statement_and_cta_links` asserts this.

- **AC-3** (error state shows recoverable message, not broken screen): **PASS** — `landing.rs` error state renders `<p class="chirp-error" role="alert">` with the error message and a "Retry" button. `public_profile.rs` error state renders a section with class `chirp-profile chirp-profile-error` with error message + "Retry". Tests `initial_error_renders_error_message_and_retry_button` and `error_state_renders_message_and_retry` verify this.

- **AC-4** ("Create an account" visible on landing and sign-in screen, leads to sign-up): **PASS** — `nav_bar()` in `app.rs` renders "Create account" and "Sign in" links on every screen via the persistent nav above the router outlet. `header_nav()` in `landing.rs` adds them within the view in every state. Test `every_state_includes_header_nav_links` asserts the nav is present in all landing view states. `sign_in.rs` includes a link to `/signup`.

- **AC-5** (loading, empty, error, end-of-list states each visually distinct): **PASS** — Each state has a distinct CSS class: `chirp-loading`, `chirp-landing-empty`, `chirp-error` (with `role="alert"`), `chirp-end` (end-of-list), and `chirp-list` (loaded). These are mutually exclusive renderings of the same view slot. Tests cover each state separately with class-name assertions.

**Check 3 verdict: PASS** (all 5 ACs verified)

---

### Check 4 — CI Quality Gates

Run via SSH on the build server against `work/chirp-logged-out` (packages: `chirp-types`, `chirp-server`, `chirp-frontend`):

- **cargo fmt --check**: PASS — exit 0, no formatting changes required (confirmed fresh run)
- **cargo clippy -- -D warnings**: PASS — exit 0, 0 warnings across all three packages (confirmed fresh run)
- **cargo test**: PASS — all tests pass:
  - `chirp-frontend`: 71 unit tests (11 landing + 13 profile + 3 sign-in + 3 sign-up + existing)
  - `chirp-server`: 65 handler unit tests + 26 integration tests (3 public timeline, 3 public chirps/user chirps)
  - `chirp-types`: 18 tests
  - Doc tests: all pass or ignored
- **wasm tests**: SKIPPED — `wasm-pack test --headless --chrome crates/chirp-frontend` requires a browser WebDriver harness not available on the build server in headless mode. All state-machine logic and view-tree output is covered by native tests. Browser-only code is `#[cfg(target_arch = "wasm32")]`-gated.

**Check 4 verdict: PASS** (fmt, clippy, test all pass; wasm skipped with documented reason)

---

## Gate Verdict: FAIL

**Failing check**: Check 2 — Contract Verification  
**Reason**: The frontend's public API deserialization structs are wire-incompatible with the backend's actual JSON output. The backend serializes with camelCase field names (`createdAt`, `likeCount`, `hasMore`, etc.) and integer types for `id` and `created_at`; the frontend expects snake_case keys and String types. Serde will error on every API response at runtime.  
**Mitigation**: Fix-task `FIXTASK_frontend_contract` has been injected. All other checks (wiring, ACs, CI) pass cleanly. The PR is open and CI passes.

---

## PR URL

https://github.com/Nousix-LLC/nswe-demo/pull/263

---

## Injected Fix-Tasks

- **FIXTASK_frontend_contract** — Fix frontend public API deserialization structs to match backend camelCase/integer wire format. See `taskflow/dags/chirp-logged-out-r4/FIXTASK_frontend_contract/_BRIEF.md` for full scope.

---

## Duplications Detected

Both `crates/chirp-types/src/api.rs` (backend) and `crates/chirp-frontend/src/api.rs` (frontend) define parallel public API DTO structs for the same two endpoints. This is architecturally intentional — the backend owns serialization and the frontend owns deserialization in a client-server system; sharing a crate between server and WASM client would significantly increase build complexity. However, the independent definition of these structs means a backend wire-format change cannot be enforced at compile time on the frontend, which is precisely how the Check 2 violation arose. The fix-task resolves the current mismatch; the longer-term mitigation is a cross-crate round-trip test that serializes a backend struct and deserializes it into the frontend struct in a single test.
