# Code Quality Review — PR #263

## Verdict

FINDINGS

## Summary

Ten code-quality concerns were reviewed across five parallel analysis tasks on PR #263 (`Nousix-LLC/nswe-demo`, commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`). No blockers were found. Eleven non-blocking findings surfaced across test depth, documentation accuracy, dead code, PR scope, and error message safety. Concern 3 (SQL correctness) and concern 9 (prose quality) were fully clean.

---

## Concern Findings

### Concern 1 — Handler unit test depth

`public_chirps_returns_chirp_with_embedded_author` checks `author.username` but does not assert `author.display_name`. The conditional display-name mapping in the handler (lines 183–187) is exercised by the test setup but never asserted; a regression returning `display_name: None` would pass. See `spoke-tests/FINDINGS.md` Finding 1.

### Concern 2 — Integration test pagination and auth regression

The cursor round-trip is tested: test 3 passes the cursor from page 1 and asserts the returned items. The auth-regression guard (`public_timeline_requires_no_auth`) targets the correct URL and status code. The `n == limit` boundary case — total items equal to the page size — has no test. See `spoke-tests/FINDINGS.md` Finding 2.

### Concern 3 — SQL formatting and semantic correctness

Both new methods in `postgres.rs` were reviewed across seven checks: syntax, before-filter operator (`<` for strictly-less-than), null-cursor handling via `$1::BIGINT IS NULL`, ordering and tiebreaker (`created_at DESC, id DESC`), soft-removed exclusion (`removed = FALSE`), two-query join safety, and case-insensitive username lookup (`LOWER(username) = LOWER($1)`). All checks found clean. See `spoke-correctness/FINDINGS.md` Clean Account (Concern 3).

### Concern 4 — Spec deviation: `before` as milliseconds vs ISO 8601

The server type (`Option<i64>`) is internally consistent and both callers pass the correct format. The doc comment for `pub_timeline()` in `chirp-frontend/src/api.rs` describes the parameter as "ISO 8601 cursor" when the actual wire type is a decimal integer millisecond timestamp. Any caller following that doc will receive a 422. See `spoke-correctness/FINDINGS.md` Finding 1.

### Concern 5 — `pub_timeline_url_has_correct_path_and_no_auth` test validity

The test never calls `pub_timeline()`. It reproduces the method's URL-building steps inline and asserts properties of that independent chain — a tautology with respect to the method under test. Two regressions in `pub_timeline()` (changing the path; switching the HTTP client to one that attaches an `Authorization` header) would leave this test green. See `spoke-tests/FINDINGS.md` Finding 3.

### Concern 6 — `sign_up::sign_up_view` dead-code question

`sign_up::sign_up_view` is a public export with no caller in any live code path. The `/signup` route binds to `compose::signup_view`. The `sign_up` module doc claims `/signup` as its entry point, which contradicts the route table. A contributor reading `sign_up.rs` to understand the signup flow finds a stub with a disabled button ("coming soon"), not the live code. See `spoke-code-health/FINDINGS.md` Finding 1.

### Concern 7 — `hydrate.rs` scope: framework refactor bundled with app feature

Two findings on this concern. The EventKind expansion is framework-layer work (`crates/ferric/`) bundled with an application feature PR, complicating bisect and rollback if either part needs reverting independently (Finding 2 in `spoke-code-health/FINDINGS.md`). Additionally, `static_event_kinds()` is a hand-written array without the compile-time completeness enforcement that `event_name()` and `stash_key()` have through exhaustive match arms. A developer updating the enum who follows the compiler's signal for `event_name` and `stash_key` has no corresponding signal to update the array; a missing entry causes silent listener accumulation on re-renders (Finding 3 in `spoke-code-health/FINDINGS.md`). The same gap exists in `dom.rs`.

### Concern 8 — Error message safety: `user_message()` on `AppError`

The `AppError::Api` path is clean: `Internal` and `Unavailable` are sanitized at the wire boundary; human-authored strings for `NotFound`, `Conflict`, `Unauthorized`, and `Forbidden` contain domain facts only. Two findings on the `AppError::Transport` path: JSON deserialization failures expose serde_json error text — including expected field names from the response schema — in the UI banner via the catch-all arm (Finding 1 in `spoke-safety-idiom/FINDINGS.md`); HTTP status errors with non-JSON bodies include the API endpoint URL in the banner (Finding 2). Both paths are reachable in production.

### Concern 9 — Prose quality

PR description, new docstrings, and inline comments across all changed files pass the plain-voice bar. One isolated instance of a character adjective in `postgres.rs` (`truthful` on a function name in the module docstring) was noted but is below the finding threshold. See `spoke-prose/FINDINGS.md`.

### Concern 10 — Rust idiom: `spawn_local`, `thread_local!`, `Cell<bool>`, `Closure::forget()`

`spawn_local`, `thread_local! + RefCell`, and `Cell<bool>` for reactive state are correct for the WASM target and structurally sound. Two documentation gaps: `Closure::forget()` in `hydrate.rs` carries the same bounded-leak behavior as `dom.rs` but lacks `dom.rs`'s module-level explanation (Finding 3 in `spoke-safety-idiom/FINDINGS.md`). `Resource::new` and `Resource::new_fallible` call `spawn_local` unconditionally with no API doc noting the `wasm32` restriction, while `create_resource` documents it explicitly (Finding 4 in `spoke-safety-idiom/FINDINGS.md`).

---

## Findings Log

No blockers. All eleven findings are non-blocking.

---

**Finding A** *(spoke-tests F1 — Concern 1)*
- **Location**: `crates/chirp-server/src/api/handlers.rs`, line 474 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: Assertion depth — a test that checks structure but not value leaves a regression path open
- **Why it matters**: The conditional display-name mapping (handler lines 183–187) is exercised by setup but never asserted. A regression returning `display_name: None` would pass.
- **Severity**: non-blocking
- **Satisfying condition**: Add `assert_eq!(resp.chirps[0].author.display_name, Some("Alice A".to_owned()));` after the `author.username` assertion at line 474. The user is already created with a non-empty `display_name` in the test setup.

---

**Finding B** *(spoke-tests F2 — Concern 2)*
- **Location**: `crates/chirp-server/tests/api.rs`, lines 869–903 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: Pagination cursor emission at the `n == limit` boundary
- **Why it matters**: The existing test covers `n > limit` (3 items, `limit=2`); it does not cover `n == limit`. Whether the server emits a cursor at that boundary affects consumer behavior and is a known off-by-one failure site.
- **Severity**: non-blocking
- **Satisfying condition**: Add a test in `mod public_timeline` with exactly `limit` items and explicitly assert the intended behavior of `next_cursor` at that boundary.

---

**Finding C** *(spoke-tests F3 — Concern 5)*
- **Location**: `crates/chirp-frontend/src/api.rs`, line 434 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: A unit test must invoke the unit under test
- **Why it matters**: The test body never calls `pub_timeline()`. It reproduces the URL-building chain inline and asserts properties of that independent reproduction. Two regressions in the method (path change; client switch to one that attaches an `Authorization` header) are invisible to this test.
- **Severity**: non-blocking
- **Satisfying condition**: Rewrite the test to call `client.pub_timeline(&query)` and assert the URL path is `/public/timeline` and no `Authorization` header is present on the request the method constructs.

---

**Finding D** *(spoke-correctness F1 — Concern 4)*
- **Location**: `crates/chirp-frontend/src/api.rs`, line 217; `crates/chirp-frontend/src/landing.rs`, line 19; `crates/chirp-frontend/src/public_profile.rs`, line 15 — all at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: A method's documentation must describe the wire contract it implements
- **Why it matters**: The method doc describes `before` as "ISO 8601 cursor"; the server type is `Option<i64>` (Unix milliseconds). A caller following the doc passes an ISO 8601 string and receives a 422.
- **Severity**: non-blocking
- **Satisfying condition**: Replace "before (ISO 8601 cursor)" in `api.rs` line 217 with wording matching the actual format, e.g. "before (Unix timestamp in milliseconds as a decimal integer string)." Apply the same correction to pagination notes in `landing.rs` line 19 and `public_profile.rs` line 15.

---

**Finding E** *(spoke-code-health F1 — Concern 6)*
- **Location**: `crates/chirp-frontend/src/sign_up.rs`, line 23 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: Dead exports — a `pub` function no caller can reach is dead code
- **Why it matters**: `sign_up::sign_up_view` has no caller in any live code path; the `/signup` route binds to `compose::signup_view`. The `sign_up` module doc claims `/signup`, contradicting the route table. A contributor reading `sign_up.rs` to understand the signup flow finds a stub with a disabled button, not the live registration code.
- **Severity**: non-blocking
- **Satisfying condition**: Remove the unreachable export and correct the `sign_up` module doc to reflect that `/signup` is handled by `compose::signup_view`, or add an explicit note that the current export is unrouted and that `compose::signup_view` is the active handler.

---

**Finding F** *(spoke-code-health F2 — Concern 7)*
- **Location**: `crates/ferric/src/hydrate.rs`, lines 417–490 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: PR scope — framework changes belong in framework PRs
- **Why it matters**: The EventKind expansion is framework-layer work in `crates/ferric/`, bundled with an application feature. Mixing the two couples a framework fix to a feature review and complicates bisect and rollback.
- **Severity**: non-blocking
- **Satisfying condition**: Accept the bundled change (the fix is correct and matches the `dom.rs` pattern), or extract the ferric changes into a preceding framework PR and rebase this PR onto it. No code correction is required if the team accepts the scope.

---

**Finding G** *(spoke-code-health F3 — Concern 7)*
- **Location**: `crates/ferric/src/hydrate.rs`, line 494; `crates/ferric/src/dom.rs`, line 309 — at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: Compile-time enforcement over advisory counts for enum-to-table mappings
- **Why it matters**: `event_name()` and `stash_key()` enforce completeness through exhaustive match arms; the compiler rejects the build if either is out of sync with `EventKind`. `static_event_kinds()` is a hand-written array checked only by a count assertion. A developer forced by the compiler to update `event_name()` or `stash_key()` has no signal to also update the array. A missing entry causes silent listener accumulation on re-renders.
- **Severity**: non-blocking
- **Satisfying condition**: Add a guard making omission a build or test failure. Options: (a) a `#[cfg(test)]` count assertion that iterates `static_event_kinds()` and calls `event_name()` and `stash_key()` on each — it will fail to compile when a new variant is added to those exhaustive matches but absent from the array; (b) derive `strum::IntoEnumIterator` and filter to skip `Custom`; (c) derive `strum::EnumCount` and assert `static_event_kinds().len() + 1 == EventKind::COUNT`. Apply to both `hydrate.rs` and `dom.rs`.

---

**Finding H** *(spoke-safety-idiom F1 — Concern 8)*
- **Location**: `crates/ferric-http/src/error.rs`, line 111; `crates/chirp-frontend/src/error.rs`, line 60 — at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: User-facing errors must not expose internal implementation details
- **Why it matters**: JSON deserialization failures (e.g., during a rolling deployment with mismatched client and server types) reach the catch-all arm at line 60, producing `"Something went wrong: failed to deserialize response body: missing field \`chirps\` at line 1 column 2"` in the UI banner. This exposes expected JSON field names from the response schema. The path is reachable in production during deployments.
- **Severity**: non-blocking
- **Satisfying condition**: Handle `HttpError::Deserialize` explicitly before the catch-all arm, producing a fixed message such as `"failed to process server response"`. Retain the serde error for logging.

---

**Finding I** *(spoke-safety-idiom F2 — Concern 8)*
- **Location**: `crates/chirp-frontend/src/error.rs`, lines 53–57 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: User-facing error messages should not embed implementation details the user cannot act on
- **Why it matters**: HTTP status errors with non-JSON bodies include the full API endpoint URL in the banner string, e.g., `"Something went wrong: HTTP status 502 Bad Gateway for /api/timeline"`. The URL adds no actionable information.
- **Severity**: non-blocking
- **Satisfying condition**: Emit a message that includes the status code but omits the URL — e.g., `"HTTP status {status}"` or `"HTTP status {status} {status_text}"`. Log the URL and body for diagnostics.

---

**Finding J** *(spoke-safety-idiom F3 — Concern 10)*
- **Location**: `crates/ferric/src/hydrate.rs`, line 473 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: Intentional memory leaks must be documented at or near the call site
- **Why it matters**: `dom.rs` explains the bounded leak from `Closure::forget()` at lines 27–33. `hydrate.rs` carries the same leaking call without that documentation. A maintainer updating event-handler lifecycle in `hydrate.rs` has no prompt to check whether a future migration (described in `dom.rs` line 33 as a planned improvement) would need to cover `hydrate.rs` as well.
- **Severity**: non-blocking
- **Satisfying condition**: Add a comment to `hydrate.rs` — in the module doc or immediately above `set_events` — matching the note at `dom.rs` lines 27–33: `Closure::forget()` permanently leaks the closure allocation (bounded: one per active handler slot per element).

---

**Finding K** *(spoke-safety-idiom F4 — Concern 10)*
- **Location**: `crates/ferric/src/async_resource.rs`, lines 112 and 133 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle**: WASM-only entry points should state their target restriction in their API documentation
- **Why it matters**: `create_resource` documents its `wasm32` restriction and native fallback explicitly. `Resource::new` and `Resource::new_fallible` call `spawn_local` unconditionally with no API doc noting the restriction. A developer following the `Resource::new` pattern when extending the API will produce a WASM-only constructor without noticing that `create_resource` establishes a different convention.
- **Severity**: non-blocking
- **Satisfying condition**: Either (a) add a `# Platform notes` or `# WASM gate` section to both doc comments stating these methods require `wasm32` and citing `create_resource` for the native-compatible pattern, or (b) add `#[cfg(target_arch = "wasm32")]` to both methods with native stubs matching `create_resource`'s behavior.

---

## Clean Account

- **Concern 3 — SQL correctness**: Both new methods in `crates/chirp-server/src/repository/postgres.rs` were checked in full: syntax, before-filter operator, null-cursor handling, ordering and tiebreaker, soft-removed exclusion, two-query join safety (strict error propagation on missing author — stricter than the in-memory reference), and case-insensitive username lookup. All checks found sound. See `spoke-correctness/FINDINGS.md` Clean Account (Concern 3).

- **Concern 9 — Prose quality**: PR description, new docstrings, and inline comments across all changed files pass the plain-voice bar. No clusters of AI-writing tells detected. One isolated instance of a character adjective in `postgres.rs` (`truthful` on a function name) is below the finding threshold. See `spoke-prose/FINDINGS.md`.
