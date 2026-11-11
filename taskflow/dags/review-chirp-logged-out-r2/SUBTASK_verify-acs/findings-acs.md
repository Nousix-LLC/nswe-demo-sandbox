# Findings: AC Re-Verification

**PR**: #263 (`work/chirp-logged-out`)
**HEAD reviewed**: 7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4

## AC verdicts

| AC | Verdict | Evidence |
|----|---------|----------|
| AC-1 | PASS | `timeline.rs:218` reads `ctx.client().timeline(&query)` at HEAD (not `pub_timeline`); public handlers `public_chirps`, `user_chirps`, `public_timeline` carry no `AuthUser` extractor; frontend routes `/` and `/@:handle` are unguarded bare closures |
| AC-2 | PASS | New `landing.rs` `empty_view()` renders "Welcome to Chirp" heading and `/signup`/`/signin` CTAs when `model.loaded && model.chirps.is_empty()`; test `empty_model_renders_welcome_statement_and_cta_links` asserts heading and both links |
| AC-3 | PASS | `error.rs` not in remediation diff — r1 verdict carries forward; new `landing.rs` `error_banner()` sets `role="alert"` on every call path; retry triggers `reload(ctx)` → full re-fetch; test `initial_error_renders_error_message_and_retry_button` asserts message and Retry present |
| AC-4 | PASS | `compose.rs:519` reads `link("/signin", "Log in →")` confirmed by direct file read at HEAD and PR diff; `/signin` resolves to `sign_in_view` via new `app.rs` route; `landing.rs` `header_nav()` renders both "Create account" and "Sign in" CTAs unconditionally |
| AC-5 | PASS | `landing.rs` has 4 distinct named states (Loading, Error-initial, Empty, Loaded) with separate render paths and tests; `public_profile.rs` has 6 distinct states via `LoadPhase` enum, each covered by a named unit test |

## Per-AC detail

### AC-1: PASS

**B1 fix check**

`timeline.rs:218` at HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4` reads:

```rust
        let result = ctx.client().timeline(&query).await;
```

Confirmed by direct file read via GitHub API. At r1 HEAD `decb6196` the same line read `ctx.client().pub_timeline(&query)`. The B1 bug is gone at this HEAD.

Note on PR diff: this single-line revert does not appear in `gh pr diff 263` because the aggregate diff computes from the merge base (`cb1ced3`, `main`) where the bug never existed. The introduction and the fix are both intra-branch commits that cancel in the aggregate diff. Direct file verification at the respective SHAs is the decisive evidence.

**Public endpoint guard status**

All three newly added public backend handlers are in the remediation diff with no `AuthUser` extractor:

| Handler | Extractors | Auth? |
|---|---|---|
| `public_chirps` | `State(state): State<AppState>`, `Query(query): Query<PublicTimelineQuery>` | None ✓ |
| `user_chirps` | `State(state): State<AppState>`, `Path(username): Path<String>`, `Query(query): Query<PublicTimelineQuery>` | None ✓ |
| `public_timeline` | `State(state): State<AppState>`, `Query(query): Query<TimelineQuery>` | None ✓ |

All three mounted in `router.rs` without auth middleware:

```rust
.route("/api/users/{username}/chirps", get(handlers::user_chirps))
.route("/api/chirps", get(handlers::public_chirps).post(handlers::create_chirp))
.route("/api/public/timeline", get(handlers::public_timeline))
```

The only `.layer()` applied to the whole router is `TraceLayer::new_for_http()` — no auth `from_fn` or bearer-token extraction layer. Auth-gated handlers (`create_chirp`, `timeline`, `follow`, `unfollow`, `like`, `unlike`) — not modified by remediation diff — still carry `AuthUser(…): AuthUser` as their first extractor argument. r1 finding carries forward.

**Frontend route table**

The `Router` in `app.rs` registers:

```rust
.route("/", move |_params| landing_view(&landing_ctx))
.route("/@:handle", move |params| { … public_profile_view(&public_profile_ctx, handle) })
```

No auth check, no session guard, no redirect closure on either entry. The router uses only `.mount_history()` as a terminator. No new auth layer — r1 finding carries forward (confirmed at HEAD).

**Conclusion**: At HEAD `7f4b684`, `timeline.rs:218` correctly calls `ctx.client().timeline(&query)`, restoring the authenticated feed for `/timeline` and leaving the public home route (`/` → `landing_view`) calling the unauthenticated `public_timeline` API client. The public backend endpoints carry no `AuthUser` extractor and are mounted without an auth layer; the frontend routes `/` and `/@:handle` are unguarded. AC-1 passes.

---

### AC-2: PASS

`landing.rs` is in the remediation diff — a new file (added from `/dev/null`). The new `empty_view()` function renders:

- `<h2>"Welcome to Chirp"</h2>` — matches the r1 heading requirement exactly.
- A descriptive paragraph inside `chirp-landing-description`.
- A CTA `<div class="chirp-landing-cta">` containing `link("/signup", "Create an account")` and `link("/signin", "Sign in")` — routes `/signup` and `/signin` match the r1 requirement.

The empty state is reached when `model.loaded == true && model.chirps.is_empty()` — the same semantic as r1. The test `empty_model_renders_welcome_statement_and_cta_links` asserts the "Welcome"/"Chirp" heading and both CTA links are present.

**Conclusion**: New implementation satisfies the criterion. AC-2 passes.

---

### AC-3: PASS

`error.rs` is **not in the remediation diff** — the `AppError::user_message()` implementation and error code coverage from r1 carry forward unchanged.

The new `landing.rs` replaces the error-handling render path:

- `error_banner(message: &str)` creates `<p class="chirp-error" role="alert">` — `role="alert"` is set on every call path (initial-load error branch and load-more error footer branch).
- The initial-error retry button calls `on_retry` → `reload(ctx)` → `MODEL.begin_initial()` + `request_load(ctx, LoadKind::Initial)` — a full re-fetch. This is the same behavior r1 found.
- The test `initial_error_renders_error_message_and_retry_button` asserts the error message is surfaced and "Retry" is present.

**Conclusion**: Error recoverability behavior preserved in new implementation. AC-3 passes.

---

### AC-4: PASS

**B2 fix check**

`compose.rs:519` at HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4` reads:

```rust
                .child(link("/signin", "Log in →")),
```

Confirmed by direct read of the file at HEAD via the GitHub API (lines 515–519 of `compose.rs`). The PR 263 diff also shows the corrected line as an addition (`+`) in the `compose.rs` hunk. B2 is fixed.

**`/signin` route resolution**

`app.rs` is in the PR 263 diff. The diff adds:

```rust
.route("/signin", move |_params| sign_in_view(&signin_ctx))
```

The module-level doc comment in the same diff hunk documents the entry:

```
//! - `/signin`    -- sign_in_view
//! - `/sign-in`   -- sign_in_view (alias for AC-3)
```

`/signin` resolves to `sign_in_view`.

**Sign-in-to-sign-up path**

`sign_in.rs` is a new file in PR 263. At HEAD `7f4b684`, line 68 reads:

```rust
                .child(link("/signup", "Create an account"))
```

The sign-in view presents a "New to Chirp? Create an account" link routing to `/signup`.

**Header nav on landing page**

`landing.rs` adds a `header_nav()` function called unconditionally from `landing_view` before the branch on page state:

```rust
fn header_nav() -> VNode {
    VElement::new("div")
        .attr("class", "chirp-landing-nav")
        .child(link("/signup", "Create account"))
        .child(text(" · "))
        .child(link("/signin", "Sign in"))
        .into()
}
```

Both "Create account" (→ `/signup`) and "Sign in" (→ `/signin`) CTAs are present and structurally guaranteed on every render of the landing view.

**Conclusion**: All four AC-4 checks pass at HEAD `7f4b684`. The B2 regression is corrected (`compose.rs:519` routes "Log in →" to `/signin`), the `/signin` route resolves to `sign_in_view`, the sign-in page links back to `/signup`, and the landing-page header nav exposes both entry points on every render. AC-4 passes.

---

### AC-5: PASS

Both `landing.rs` and `public_profile.rs` are new files in PR 263 (added from `/dev/null`).

**`landing.rs`** — four named states, each with a distinct render path in `view_tree()`:

| State | Trigger condition | Render |
|---|---|---|
| Loading | `!model.loaded && model.error.is_none()` | `loading_view()` → `<p class="chirp-loading">` |
| Error (initial) | `!model.loaded && model.error.is_some()` | `error_banner + Retry` via `on_retry` |
| Empty | `model.loaded && model.chirps.is_empty()` | `empty_view()` → welcome heading + CTAs |
| Loaded / End-of-list | `model.loaded && !model.chirps.is_empty()` | chirp list + `footer()` switching between loading-more spinner, Load-more button, inline continuation error, and end-of-list note |

Tests cover each: `unloaded_model_renders_loading_state`, `empty_model_renders_welcome_statement_and_cta_links`, `loaded_model_renders_chirp_list_and_load_more_button`, `last_page_renders_end_note_not_load_more`, `initial_error_renders_error_message_and_retry_button`.

**`public_profile.rs`** — six named states via the `LoadPhase` enum:

| State | `LoadPhase` / condition | Render function |
|---|---|---|
| Loading | `LoadPhase::Loading` | `loading_view()` — `chirp-profile-loading` |
| Not found | `LoadPhase::NotFound` | `not_found_view()` — `chirp-profile-not-found` |
| Error | `LoadPhase::Error(err)` | `error_view()` — `chirp-profile-error` + Retry |
| Empty (loaded, no chirps) | `LoadPhase::Loaded && chirps.is_empty()` | `loaded_view()` → "No chirps yet." |
| Loaded with chirps | `LoadPhase::Loaded && !chirps.is_empty()` | `loaded_view()` → `chirp-list` + footer |
| End-of-list | `LoadPhase::Loaded && !has_more` | `profile_footer()` → "No more chirps." |

Tests cover each: `loading_state_renders_loading_indicator`, `not_found_state_renders_distinct_message`, `error_state_renders_message_and_retry`, `empty_loaded_state_renders_empty_message`, `loaded_with_chirps_renders_list_and_load_more`, `end_of_list_renders_end_note`.

**Conclusion**: All state branches present, accurate, and distinct in both files. `error.rs` was not modified; its r1 verdict carries forward. `landing.rs` and `public_profile.rs` are new additions, both implementing the required empty state, error recoverability, and state-branch coverage correctly, with unit tests asserting each state branch. AC-5 passes.

---

## Non-blocking findings

| ID | Location | Severity | Description |
|----|----------|----------|-------------|
| — | — | — | No new non-blockers surfaced by any spoke. Issues #264–#271 remain already-tracked from r1; not re-filed. |
