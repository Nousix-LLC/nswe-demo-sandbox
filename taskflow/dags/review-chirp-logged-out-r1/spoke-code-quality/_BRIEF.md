# _BRIEF.md — Spoke: Code Quality, Tests, Security, Idiom, and Prose

## Objective

Review the code quality, test depth, language idiom, security surface, and prose quality of
PR #263, covering all files in the diff that are not specifically assigned to the AC-behavioral
spokes.

## Inputs

- PR #263 diff: `Nousix-LLC/nswe-demo`, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- Global context: `taskflow/dags/review-chirp-logged-out-r1/_GLOBAL.md`
- Code areas:
  - `crates/chirp-types/src/api.rs` — new wire types (`PublicTimelineQuery`, `PublicChirp`,
    `PublicAuthor`, `PublicTimelineResponse`, `PublicUserProfile`, `PublicUserChirp`,
    `PublicUserResponse`); spec deviation note (`before` as milliseconds vs. ISO 8601)
  - `crates/chirp-server/src/api/handlers.rs` — handler unit tests (6 new tests)
  - `crates/chirp-server/src/repository/in_memory.rs` — `public_timeline`,
    `public_chirps_with_authors`, `get_user_chirps_by_username` implementations
  - `crates/chirp-server/src/repository/postgres.rs` — same three methods for PostgreSQL;
    SQL queries for `public_chirps_with_authors` and `get_user_chirps_by_username` are written as
    very long single-line strings with embedded whitespace, unlike the multi-line format used
    elsewhere
  - `crates/chirp-server/src/repository/mod.rs` — trait extension
  - `crates/chirp-server/tests/api.rs` — integration tests in `mod public_timeline`
  - `crates/chirp-frontend/src/api.rs` — `pub_timeline_url_has_correct_path_and_no_auth` test
    still asserts the OLD `/api/public/timeline` path; `pub_timeline()` is now used by
    `timeline.rs` for the authenticated home feed
  - `crates/ferric/src/hydrate.rs` — large framework refactor (EventKind expansion,
    EventHandler::WithEvent variant, `static_event_kinds()` table)
  - PR description prose and all module/function docstrings in new files

## Specific concerns this spoke must resolve

1. **Test depth — server handler unit tests**: Do the 6 new unit tests in `handlers.rs` cover
   the 404 path for `user_chirps`? Does `public_chirps_returns_chirp_with_embedded_author` check
   that the `author` field in the response matches the created user? Are any critical error paths
   untested?

2. **Test depth — integration tests**: Do `api.rs` integration tests for the public timeline
   cover pagination correctly (cursor round-trip, boundary at exactly `limit` items)? Does the
   regression guard (`GET /api/timeline` returns 401 without auth) actually test the right
   endpoint?

3. **SQL formatting**: The PostgreSQL implementations of `public_chirps_with_authors` and
   `get_user_chirps_by_username` embed SQL as single-line strings with mangled whitespace (spaces
   instead of `\` line continuations). Is the SQL syntactically correct despite the formatting?
   Does it match the semantics specified in the trait docstrings?

4. **Spec deviation**: `PublicTimelineQuery.before` is documented in the type as milliseconds
   since epoch; the external spec describes it as ISO 8601. This deviation is acknowledged in the
   code comment. Is the client-side usage consistent with the server-side expectation? Does the
   frontend pass a millisecond integer string where the server expects a millisecond integer?

5. **`pub_timeline_url_has_correct_path_and_no_auth` test in `api.rs`**: This test was written
   for the old `pub_timeline()` method, which calls `/api/public/timeline`. Now `pub_timeline()`
   is used by the authenticated `timeline.rs`. Is the test still meaningful, or does it now test
   dead-to-the-public-timeline-feature code?

6. **`sign_up.rs` dead-code question**: `sign_up.rs` exports `sign_up_view` (a stub with
   disabled button). The route table routes `/signup` to `signup_view` from `compose.rs`, not to
   `sign_up::sign_up_view`. Is `sign_up::sign_up_view` reachable from any route? If not, is the
   module dead code?

7. **Ferric hydrate.rs scope**: The `hydrate.rs` changes (EventKind expansion from 2 to 47+
   variants, EventHandler::WithEvent variant, `static_event_kinds()` table) are framework-level
   changes bundled with the application feature. Are they related to the feature or scope creep?
   Do they introduce any correctness risk (e.g., the `static_event_kinds()` table must be kept in
   sync with the enum)?

8. **Error message safety**: `user_message()` on `AppError` — verify that error messages surfaced
   in the UI (e.g., in `error_banner`) do not expose internal details (stack traces, internal
   server paths, raw database errors).

9. **Prose quality**: Check module docstrings, function docstrings, inline comments, and the PR
   description for AI-writing tells: moral/character adjectives attached to technical things
   ("honest", "genuine"), narrated candor ("stated plainly", "to be clear"), unnamed contrast
   pairs, slot-fill templates, and stacked padding filler. Report by cluster and density.

10. **Rust idiom**: `spawn_local` for async effects, `thread_local!` + `RefCell` for reactive
    state, `Cell<bool>` for the started guard, `Closure::forget()` in hydrate.rs — are these
    idiomatic for Rust/WASM or do any create leak/panic risks?

## Declared output

A `REVIEW.md` at `taskflow/dags/review-chirp-logged-out-r1/spoke-code-quality/REVIEW.md`
containing:

- Verdict for this concern: PASS or FINDINGS
- For each finding: location (file + line at the pinned commit), what principle is at stake, why
  it matters, severity (blocker / non-blocking), and what would satisfy it
- An account of what each sub-concern checked and found clean

## Success criteria

- Each of the 10 sub-concerns above is explicitly addressed
- SQL correctness in postgres.rs is verified (not assumed from formatting)
- Test depth verdict covers each new handler and state branch
- Prose quality judgment covers both code comments and the PR description
- No internal infrastructure details appear in findings

## Constraints

- Repository: `Nousix-LLC/nswe-demo` only
- Do not post to the PR; that is the synthesis child's responsibility
- Findings point at repository file paths and lines; do not name host paths, private IPs, or
  internal infrastructure details
