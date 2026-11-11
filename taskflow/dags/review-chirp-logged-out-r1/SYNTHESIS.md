# SYNTHESIS.md — PR #263: feat: logged-out public timeline and user profiles

**Repository**: Nousix-LLC/nswe-demo  
**PR**: #263 (`work/chirp-logged-out`)  
**Head**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`  
**Issue**: #35  
**Verdict**: **REQUEST-CHANGES**

Two blockers must be fixed before this merges. Both are single-line changes. Both are regressions in correct pre-existing behavior introduced by this PR, not gaps in the new feature.

---

## Per-AC verdict

| AC | Concern | Verdict | Key evidence |
|----|---------|---------|--------------|
| AC-1 | Public access without forced auth | **FAIL** | New public endpoints are correctly unguarded (no `AuthUser` extractor). But `timeline.rs:218` was changed from `ctx.client().timeline(&query)` to `ctx.client().pub_timeline(&query)`, routing authenticated `/timeline` through the global unauthenticated feed. See Blocker 1. |
| AC-2 | Empty state | **PASS** | `empty_view()` at `landing.rs:286–306` renders "Welcome to Chirp" with correct copy and two correctly-routed CTAs (`/signup`, `/signin`). Test `empty_model_renders_welcome_statement_and_cta_links` is behavioral. |
| AC-3 | Error state recoverability | **PASS** | `AppError::user_message()` returns plain-English text on all three arms; `error_banner` sets `role="alert"` on every call path; "Retry" button wired to a full re-fetch. One non-blocking test gap (UI-NB1 below). |
| AC-4 | Sign-up / sign-in CTAs | **FAIL** | `header_nav` is structurally guaranteed (hoist-before-branch). Sign-in-to-sign-up path correct. Sign-up-to-sign-in path broken: `compose.rs:519` renders `link("/compose", "Log in →")` — wrong destination. See Blocker 2. |
| AC-5 | State branches accurate and distinct | **PASS** | All four required states present in both `landing.rs` (7 branches) and `public_profile.rs` (8 branches). Every state has a unique CSS class + text combination. State machines are mutually exclusive. Non-blocking test gaps in footer sub-states (SM-F1, SM-F2). |

---

## Blockers

### Blocker 1 — Authenticated home timeline routes through global unauthenticated feed

**File**: `crates/chirp-frontend/src/timeline.rs:218`  
**Commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`  
**Spoke**: access-auth

```rust
// line 218 — fn request_load
let result = ctx.client().pub_timeline(&query).await;   // ← was timeline()
```

`pub_timeline()` constructs a fresh unauthenticated HTTP client — it explicitly omits `self.token`. An authenticated user navigating to `/timeline` now receives the full reverse-chronological list of all chirps from all users (via `/api/public/timeline`) instead of their personalized following feed (via `/api/timeline`). The module doc at `timeline.rs:4` documents the correct call as `ctx.client().timeline(..)`, making this change inconsistent with the module's own stated contract.

**What would satisfy this finding**: Revert line 218 to `ctx.client().timeline(&query).await`. The integration test at `api.rs:915–919` guards the server side. The fix needs a frontend test or manual verification confirming `timeline_view` calls `timeline()`, not `pub_timeline()`.

---

### Blocker 2 — "Log in →" CTA on sign-up page routes to compose view

**File**: `crates/chirp-frontend/src/compose.rs:519`  
**Commit**: `decb6196c2c1e6ed421d393a642f0c844cc333ba`  
**Spoke**: ui-states

```rust
link("/compose", "Log in →")   // ← should be /signin
```

A user on the sign-up page who clicks "Log in →" reaches `/compose` instead of `/signin`. The URL reads `/compose`; any sign-in-specific redirect or UX logic in `sign_in_view` is bypassed; the route table names `/signin` / `/sign-in` as the canonical sign-in destinations, making this link inconsistent with that decision.

**What would satisfy this finding**: Change to `link("/signin", "Log in →")` at `compose.rs:519`.

---

## Non-blocking findings

### Test coverage gaps

| ID | Location | Severity | Description |
|----|----------|----------|-------------|
| SM-F1 | `landing.rs` `mod tests` | Non-blocking | No view-tree test for the continuation-error state (State 4: `loaded=true`, chirps non-empty, `error=Some`) or loading-more state (State 5). If `footer` dropped either branch, no test would catch it. |
| SM-F2 | `public_profile.rs` `mod tests` | Non-blocking | Same gap: no view-tree test for continuation-error or loading-more states. The transition test `apply_error_on_more_sets_continuation_error` verifies the model but doesn't render the tree. |
| SM-F3 | `landing.rs:487` | Non-blocking | `begin_initial_resets_all_state` does not assert `!m.loading_more`, though the implementation resets the field. |
| SM-F4 | `landing.rs:456` | Non-blocking | `apply_more_appends_and_updates_cursor` does not cover the empty-response guard: an empty-chirp continuation should leave `before_cursor` unchanged. |
| UI-NB1 | `landing.rs:584–598` | Non-blocking | `initial_error_renders_error_message_and_retry_button` checks text content but not `role="alert"`. Removing the ARIA attribute would leave the test green. |
| CQ-A | `handlers.rs:474` | Non-blocking | Handler unit test checks `author.username` but not `author.display_name`. The conditional display-name mapping (lines 183–187) is set up but never asserted; a regression returning `None` passes. |
| CQ-B | `api.rs:869–903` | Non-blocking | Pagination test covers `n > limit`; `n == limit` (cursor emission at the exact boundary) has no test. |
| **CQ-C** ⚑ | `api.rs:434` | Non-blocking | `pub_timeline_url_has_correct_path_and_no_auth` never calls `pub_timeline()`. It reproduces the method inline; a path change or auth-header addition in the method would not fail this test. File an issue to rewrite to call the method and assert the URL path and absence of `Authorization` header. |

### Documentation errors

| ID | Location | Severity | Description |
|----|----------|----------|-------------|
| **CQ-D** ⚑ | `api.rs:217`, `landing.rs:19`, `public_profile.rs:15` | Non-blocking | Method doc describes `before` as "ISO 8601 cursor"; the wire type is `Option<i64>` (Unix milliseconds). A caller following the doc passes an ISO 8601 string and receives a 422. |
| UI-NB2 | `app.rs:13` | Non-blocking | Route annotation reads `(alias for AC-3)`. AC-3 is about recoverable error messages; the alias is for sign-in navigation (AC-4). |

### Code health

| ID | Location | Severity | Description |
|----|----------|----------|-------------|
| **CQ-E** ⚑ | `sign_up.rs:23` | Non-blocking | `sign_up::sign_up_view` is a public export with no caller in any live code path. The `/signup` route binds to `compose::signup_view`. The module doc claims `/signup`, contradicting the route table. |
| CQ-F | `hydrate.rs:417–490` | Non-blocking | EventKind expansion is framework work in `crates/ferric/` bundled with an application feature PR. Correct as written; the concern is bisect/rollback coupling if either part needs reverting independently. |
| **CQ-G** ⚑ | `hydrate.rs:494`, `dom.rs:309` | Non-blocking | `static_event_kinds()` is a hand-written array checked only by a count assertion. `event_name()` and `stash_key()` enforce completeness through exhaustive match arms; the compiler rejects the build if either is out of sync with `EventKind`. A developer updating the enum who follows the compiler's signal for those two has no equivalent signal for the array. A missing entry causes silent listener accumulation on re-renders. Apply a compile-time guard to both files. |
| CQ-J | `hydrate.rs:473` | Non-blocking | `Closure::forget()` carries the same bounded-leak behavior as `dom.rs` but lacks `dom.rs`'s module-level explanation. A maintainer updating event-handler lifecycle in `hydrate.rs` has no prompt to check whether a planned future migration would need to cover it. |
| CQ-K | `async_resource.rs:112, 133` | Non-blocking | `Resource::new` and `Resource::new_fallible` call `spawn_local` unconditionally with no API doc noting the `wasm32` restriction. `create_resource` documents the restriction and provides a native-compatible pattern. |

### Error message safety

| ID | Location | Severity | Description |
|----|----------|----------|-------------|
| **CQ-H** ⚑ | `ferric-http/src/error.rs:111`, `chirp-frontend/src/error.rs:60` | Non-blocking | JSON deserialization failures reach the catch-all arm, exposing serde_json error text — including expected field names from the response schema — in the UI banner. This path is reachable during rolling deployments with mismatched client/server types. Fix: handle `HttpError::Deserialize` explicitly before the catch-all with a fixed message such as "failed to process server response"; retain the serde error for logging. |
| **CQ-I** ⚑ | `chirp-frontend/src/error.rs:53–57` | Non-blocking | HTTP status errors with non-JSON bodies include the full API endpoint URL in the banner string. The URL adds no actionable information for the user. Fix: emit status code only (`"HTTP status {status}"`); log the URL for diagnostics. |

Findings marked ⚑ are recommended for issue filing.

---

## What each spoke examined and found clean

### spoke-access-auth

- **New public endpoints**: Three new handlers (`public_chirps`, `user_chirps`, `public_timeline`) have no `AuthUser` extractor and are mounted without any auth layer. Axum's extractor mechanism means absence of `AuthUser` is the correct implementation of "no auth required."
- **Auth-gated handlers unchanged**: `create_chirp`, `timeline`, `follow`, `unfollow`, `like`, `unlike` all retain their `AuthUser(…): AuthUser` extractor. The integration test at `api.rs:915–919` confirms `GET /api/timeline` returns 401 without a token.
- **No auth bypass surface**: Public and authenticated routes are mounted as siblings; no shared `from_fn` or `layer` would propagate auth state across route boundaries.
- **Frontend route table**: `/` → `landing_view` and `/@:handle` → `public_profile_view` are unguarded. No previously unguarded page had a gate added.

### spoke-ui-states

- **AC-2 empty_view()**: Product-specific heading and description, two correctly-routed CTAs, behavioral test.
- **AC-3 implementation**: `AppError::user_message()` returns readable text on all arms. `error_banner` sets `role="alert"` on every call path. Retry wired to `model.begin_initial()` → full re-fetch.
- **AC-4 header_nav**: Hoist-before-branch at `landing.rs:264` makes the guarantee structural. `every_state_includes_header_nav_links` at line 509 covers it.
- **AC-4 sign-in-to-sign-up**: `sign_in.rs:68` → `/signup` → `compose::signup_view` (the live registration form). The `sign_up.rs` placeholder stub is unrouted.

### spoke-state-machine

- **State enumeration**: All four AC-5 states (loading, empty, error, end-of-list) confirmed present in both `landing.rs` and `public_profile.rs` with distinct CSS classes and text.
- **State distinctness**: Every pair of states produces a different combination of class and content. The cases most likely to collapse (loading vs. empty; initial error vs. continuation error) are unambiguous.
- **begin_initial reset**: All six rendering-relevant fields reset correctly.
- **apply_error 404 vs. non-404**: `ErrorCode::NotFound` check correctly routes initial-load 404 to `LoadPhase::NotFound` and other errors to `LoadPhase::Error(err)`. Three distinct tests cover three branches.
- **apply_more empty-page guard**: Cursor advances only when `resp.chirps` is non-empty.
- **One-state-model criterion**: `loading_more` and `error` are mutually exclusive through the state machine in both `LandingModel` and `ProfileModel`.
- **STARTED re-visit behavior**: By-design caching for `/`; correct for AC-5. See §Design note.

### spoke-code-quality

- **SQL correctness** (`postgres.rs`): Both new methods checked across seven dimensions — syntax, before-filter operator (`<` for strictly-less-than), null-cursor handling via `$1::BIGINT IS NULL`, ordering and tiebreaker (`created_at DESC, id DESC`), soft-removed row exclusion, two-query join safety, and case-insensitive username lookup (`LOWER(username) = LOWER($1)`). All found sound.
- **Prose quality**: PR description, new docstrings, and inline comments across all changed files pass the plain-voice bar. No clusters of AI-writing tells detected.
- **spawn_local, thread_local!, Cell\<bool\>, RefCell**: Correct for the WASM target. Structurally sound.

---

## Design note

**Re-visit caching at `/`**: `STARTED: Cell<bool>` at `landing.rs:129` is set on first render and never reset, so returning to `/` after navigating away shows the cached model state rather than triggering a re-fetch. The behavior is intentional (module doc: "Loads GET /api/chirps on first display") and correct for AC-5. If the product later requires fresh-on-return, the fix is resetting `STARTED` on `landing_view` re-entry, or adding an explicit route lifecycle hook.
