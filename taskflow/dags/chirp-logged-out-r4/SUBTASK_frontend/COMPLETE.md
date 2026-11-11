# COMPLETE — SUBTASK_frontend

**Task**: Implement the public (logged-out) user experience in `crates/chirp-frontend`.  
**Status**: Completed  
**Commit**: `e02b1d8` on branch `work/chirp-logged-out`

---

## Files Created

| File | Purpose |
|------|---------|
| `crates/chirp-frontend/src/landing.rs` | Public home/landing view at `/` — public timeline with 5 states |
| `crates/chirp-frontend/src/public_profile.rs` | Public user profile view at `/@:handle` with 6 states |
| `crates/chirp-frontend/src/sign_in.rs` | Sign-in entry point at `/signin` (form stub) |
| `crates/chirp-frontend/src/sign_up.rs` | Sign-up entry point at `/signup` (form stub) |

## Files Modified

| File | Changes |
|------|---------|
| `crates/chirp-frontend/src/api.rs` | Added `PublicAuthor`, `PublicChirp`, `PublicTimelineResponse`, `PublicUserInfo`, `PublicUserChirp`, `PublicUserResponse` types; added `public_timeline()` (`GET /api/chirps`) and `public_user_profile()` (`GET /api/users/:username/chirps`) methods; added `public_chirps_query_params()` helper |
| `crates/chirp-frontend/src/app.rs` | Updated route table: `/` → `landing_view`, `/@:handle` → `public_profile_view`, `/signin` → `sign_in_view`, `/signup` → `sign_up_view`; kept `/compose`, `/user/:id`, `/timeline`; nav bar updated with correct "Create account" and "Sign in" links |
| `crates/chirp-frontend/src/lib.rs` | Added `pub mod landing`, `pub mod public_profile`, `pub mod sign_in`, `pub mod sign_up` |
| `crates/chirp-frontend/Cargo.toml` | Added `serde = { workspace = true }` for `Deserialize` derives on new API types |

---

## UI States Implemented

### Landing view (`/`) — 5 states
| State | Visual |
|-------|--------|
| `Loading` | `<p class="chirp-loading">Loading…</p>` beneath the sign-up/sign-in nav |
| `Empty` | `<div class="chirp-landing-empty">` with "Welcome to Chirp" heading, description, and "Create an account · Sign in" CTAs |
| `Loaded` | `<ul class="chirp-list">` keyed by chirp UUID, each row showing display name, content, like count, ISO 8601 timestamp; author links to `/@username` |
| `EndOfList` | List + `<p class="chirp-end">You're all caught up.</p>` (has_more = false after first page) |
| `Error` | `<p class="chirp-error" role="alert">` with message + "Retry" button (full-screen on initial failure, inline after a loaded first page) |

Sign-up and sign-in links are present in **every** state via `header_nav()` (AC-4 satisfied).

### Public profile view (`/@:handle`) — 6 states
| State | Visual |
|-------|--------|
| `Loading` | Section with class `chirp-profile chirp-profile-loading` and "Loading…" indicator |
| `NotFound` | Section with class `chirp-profile chirp-profile-not-found` and "This user does not exist." message |
| `Empty` | Loaded state with user header visible but `<p class="chirp-profile-empty">No chirps yet.</p>` |
| `Loaded` | User header (display name, handle, bio, chirp count) + `<ul class="chirp-list">` keyed by chirp UUID |
| `EndOfList` | List + `<p class="chirp-end">No more chirps.</p>` (has_more = false) |
| `Error` | Section with class `chirp-profile chirp-profile-error`, error message + "Retry" button |

---

## Tests Written

**71 total native tests** (all passing). New tests added:

### `landing::tests` (11 tests)
- `apply_initial_marks_loaded_sets_cursor_and_has_more` — reducer: initial page stored + cursor set
- `apply_more_appends_and_updates_cursor` — reducer: continuation appended + cursor advanced
- `apply_error_on_initial_keeps_unloaded` — reducer: first-load error stays unloaded
- `apply_error_after_load_keeps_loaded` — reducer: continuation error stays loaded
- `begin_initial_resets_all_state` — reducer: retry resets all fields
- `unloaded_model_renders_loading_state` — view: loading indicator present
- `every_state_includes_header_nav_links` — view: nav always has Create account + Sign in
- `empty_model_renders_welcome_statement_and_cta_links` — view: empty state explains Chirp + shows CTAs
- `loaded_model_renders_chirp_list_and_load_more_button` — view: list + Load more when has_more
- `last_page_renders_end_note_not_load_more` — view: end note when has_more=false
- `initial_error_renders_error_message_and_retry_button` — view: error message + Retry

### `public_profile::tests` (13 tests)
- `reset_for_clears_all_prior_state` — model keying: new handle resets everything
- `apply_initial_transitions_to_loaded` — reducer: initial response sets Loaded phase
- `apply_more_appends_chirps` — reducer: continuation appended
- `apply_error_on_initial_not_found_sets_not_found_phase` — 404 → NotFound phase
- `apply_error_on_initial_server_error_sets_error_phase` — non-404 → Error phase
- `apply_error_on_more_sets_continuation_error` — continuation error is inline
- `loading_state_renders_loading_indicator` — view: loading state distinct
- `not_found_state_renders_distinct_message` — view: not-found state explains user absent
- `error_state_renders_message_and_retry` — view: error message + Retry visible
- `empty_loaded_state_renders_empty_message` — view: no chirp-list in empty state
- `loaded_with_chirps_renders_list_and_load_more` — view: list + Load more when has_more
- `end_of_list_renders_end_note` — view: end note when has_more=false
- (1 additional assertion in reset_for)

### `sign_in::tests` (3 tests)
- `sign_in_view_renders_a_section_with_correct_class`
- `sign_in_view_contains_link_to_signup`
- `sign_in_view_contains_link_to_home`

### `sign_up::tests` (3 tests)
- `sign_up_view_renders_a_section_with_correct_class`
- `sign_up_view_contains_link_to_signin`
- `sign_up_view_contains_link_to_home`

---

## SSR Decision

**SSR skipped** for the public timeline. Rationale: the SSR stubs in the codebase have `todo!()` bodies and the analysis identified CSR with `spawn_local` as the correct approach. The `start()` function retains the existing `hydrate`/`mount` conditional for future use, but the landing and profile views use pure CSR (`spawn_local` + `thread_local` model).

---

## Quality Gate Results

| Check | Result |
|-------|--------|
| `cargo fmt --check -p chirp-frontend` | ✅ clean (no formatting changes needed) |
| `cargo clippy -p chirp-frontend -- -D warnings` | ✅ clean (0 warnings) |
| `cargo test -p chirp-frontend` | ✅ 71 passed, 0 failed |
| `cargo check -p chirp-frontend` | ✅ 0 warnings, 0 errors |

**Note on wasm tests**: The `wasm-pack test` suite requires a browser harness (Chrome/Firefox via WebDriver). The native test suite above covers all state-machine logic, reducer transitions, and view-tree output without a DOM. Browser-only code (`spawn_local`, DOM mount) is `#[cfg(target_arch = "wasm32")]`-gated, matching the pattern in `ferric` and `ferric-router`. The command to run wasm tests in a headless browser environment is: `wasm-pack test --headless --chrome crates/chirp-frontend`.

---

## API Contract Conformance

Both new API methods compose against the frozen spec (`contracts/public_api_spec.md`) exactly:

- `public_timeline(before, limit)` → `GET /api/chirps?before=...&limit=...` (no auth header)
- `public_user_profile(username, before, limit)` → `GET /api/users/:username/chirps?...` (no auth header)
- Response deserialization uses the struct shapes defined in the spec verbatim.
