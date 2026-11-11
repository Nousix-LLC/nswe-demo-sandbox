# Verdict: AC-2, AC-3, AC-5

**ac_2_verdict**: PASS  
**ac_3_verdict**: PASS  
**ac_5_verdict**: PASS

## Evidence

### AC-2: Empty state

`landing.rs` is in the remediation diff — it is a new file (added from `/dev/null`; the prior
revision had no `landing.rs`). The new `empty_view()` function renders:

- `<h2>"Welcome to Chirp"</h2>` — matches the r1 heading requirement exactly.
- A descriptive paragraph inside `chirp-landing-description`.
- A CTA `<div class="chirp-landing-cta">` containing `link("/signup", "Create an account")` and
  `link("/signin", "Sign in")` — routes `/signup` and `/signin` match the r1 requirement.

The empty state is reached when `model.loaded == true && model.chirps.is_empty()` — the same
semantic as r1. The test `empty_model_renders_welcome_statement_and_cta_links` asserts the
"Welcome"/"Chirp" heading and both CTA links are present.

**AC-2 PASS** — new implementation satisfies the criterion.

### AC-3: Error state recoverability

`error.rs` is **not in the remediation diff** — the `AppError::user_message()` implementation
and error code coverage from r1 carry forward unchanged.

The new `landing.rs` replaces the error-handling render path. Verification:

- `error_banner(message: &str)` creates `<p class="chirp-error" role="alert">` — `role="alert"`
  is set on every call path (initial-load error branch and load-more error footer branch).
- The initial-error retry button calls `on_retry` → `reload(ctx)` → `MODEL.begin_initial()` +
  `request_load(ctx, LoadKind::Initial)` — a full re-fetch. This is the same behavior r1 found.
- The test `initial_error_renders_error_message_and_retry_button` asserts the error message
  is surfaced and "Retry" is present.

**AC-3 PASS** — error recoverability behavior preserved in new implementation.

### AC-5: State branches accurate and distinct

Both `landing.rs` and `public_profile.rs` are new files (added from `/dev/null`).

**`landing.rs`** — four named states, each with a distinct render path in `view_tree()`:

| State | Trigger condition | Render |
|---|---|---|
| Loading | `!model.loaded && model.error.is_none()` | `loading_view()` → `<p class="chirp-loading">` |
| Error (initial) | `!model.loaded && model.error.is_some()` | `error_banner + Retry` via `on_retry` |
| Empty | `model.loaded && model.chirps.is_empty()` | `empty_view()` → welcome heading + CTAs |
| Loaded / End-of-list | `model.loaded && !model.chirps.is_empty()` | chirp list + `footer()` which switches between loading-more spinner, Load-more button, inline continuation error, and end-of-list note |

All four states are present and distinct. Tests cover each: `unloaded_model_renders_loading_state`,
`empty_model_renders_welcome_statement_and_cta_links`, `loaded_model_renders_chirp_list_and_load_more_button`,
`last_page_renders_end_note_not_load_more`, `initial_error_renders_error_message_and_retry_button`.

**`public_profile.rs`** — six named states via the `LoadPhase` enum:

| State | `LoadPhase` / condition | Render function |
|---|---|---|
| Loading | `LoadPhase::Loading` | `loading_view()` — `chirp-profile-loading` |
| Not found | `LoadPhase::NotFound` | `not_found_view()` — `chirp-profile-not-found` |
| Error | `LoadPhase::Error(err)` | `error_view()` — `chirp-profile-error` + Retry |
| Empty (loaded, no chirps) | `LoadPhase::Loaded && chirps.is_empty()` | `loaded_view()` → "No chirps yet." |
| Loaded with chirps | `LoadPhase::Loaded && !chirps.is_empty()` | `loaded_view()` → `chirp-list` + footer |
| End-of-list | `LoadPhase::Loaded && !has_more` | `profile_footer()` → "No more chirps." |

All six states are distinct. Tests cover each named branch: `loading_state_renders_loading_indicator`,
`not_found_state_renders_distinct_message`, `error_state_renders_message_and_retry`,
`empty_loaded_state_renders_empty_message`, `loaded_with_chirps_renders_list_and_load_more`,
`end_of_list_renders_end_note`.

**AC-5 PASS** — all state branches present, accurate, and distinct in both files.

## Conclusion

All three criteria remain PASS at HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`. `error.rs` was
not modified; its r1 verdict carries forward. `landing.rs` and `public_profile.rs` are new
additions rather than modifications to existing passing code; both implement the required empty
state, error recoverability, and state-branch coverage correctly, with unit tests that assert
each state branch.
