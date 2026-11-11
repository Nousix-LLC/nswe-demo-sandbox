# Handler Unit Test Depth — Concern 1

## Verdict

FINDING(S)

---

## Findings

### Finding A: `public_chirps_returns_chirp_with_embedded_author` does not assert `author.display_name`

- **Concern**: 1
- **Location**: `crates/chirp-server/src/api/handlers.rs`, line 474 at commit `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Principle at stake**: Assertion depth — a test that checks structure but not value does not catch a regression where the wrong value is returned
- **Why it matters**: The test creates a user with `display_name: "Alice A".to_owned()` (line 451) and the `public_chirps` handler maps the display_name conditionally at lines 183–187 (`if author.display_name.is_empty() { None } else { Some(author.display_name) }`). The test asserts `resp.chirps[0].author.username == "alice"` (line 474), which is a genuine value-level check for the wrong-author regression. However, `resp.chirps[0].author.display_name` is never asserted. A regression in the conditional branch — for example, if the handler always returned `display_name: None` — would not be caught: the test would still pass because it only checks `username`.
- **Severity**: non-blocking
- **Satisfying condition**: Add `assert_eq!(resp.chirps[0].author.display_name, Some("Alice A".to_owned()));` after the `author.username` assertion at line 474. The user is already created with a non-empty `display_name` in the test setup, so no additional setup is required.

---

## Evidence

**404 path for `user_chirps`**: The test `user_chirps_returns_404_for_missing_user` (lines 500–509) calls `user_chirps` with `Path("nobody".to_owned())` against an empty store and asserts `matches!(err, ServerError::NotFound(_))`. The assertion is behavior-level: it checks the specific error variant, not merely that the call failed. This test would fail if the handler stopped propagating `NotFound` from the repository. The 404 path is covered.

**`public_chirps_returns_chirp_with_embedded_author` assertion level**: The test at lines 445–476 creates user "alice" with `display_name: "Alice A"`, posts a chirp as that user, then calls `public_chirps`. The assertion `assert_eq!(resp.chirps[0].author.username, "alice")` at line 474 is value-level: it checks that the embedded author's username matches the created user, not merely that an `author` field was present. A regression that embedded a different user (or the wrong id) would cause this test to fail. The core "right author embedded" check is present. The gap is that `author.display_name` is set up but never verified in the assert section — examined at lines 451 and 474–475.

**Other critical error paths among the 6 new tests**: The 6 new tests cover the two new handlers, `public_chirps` and `user_chirps`. For `public_chirps`, the repository trait's `public_chirps_with_authors` method carries no documented error variants (no `# Errors` section in `repository/mod.rs`), so the two happy-path tests (empty store, store with one chirp) are adequate. For `user_chirps`, the trait's `get_user_chirps_by_username` documents one error — `NotFound` when no user has that username — and that path is tested by `user_chirps_returns_404_for_missing_user`. No critical error paths among the new tests are untested.

**What was examined**: the `handlers.rs` test module (lines 328–568), the `repository/mod.rs` trait definitions for `public_chirps_with_authors` and `get_user_chirps_by_username`, and the production `public_chirps` handler at lines 167–194 and `user_chirps` at lines 200–234.
