# _BRIEF.md — CHILD_tests

**Parent task:** SUBTASK_server_public_timeline  
**Parent hub:** `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/_GLOBAL.md`

## Objective

Write integration tests for `GET /api/public/timeline` and verify that all CI checks (`cargo fmt --check`, `cargo clippy`, `cargo test`) pass on `work/chirp-logged-out`.

## Scope

Two distinct concerns:

1. **Integration tests** — `crates/chirp-server/tests/api.rs`: add test cases covering the new public timeline endpoint. The existing harness (`TestApp`, `build_app`, `username`, `new_user`, `post_chirp` convenience methods) is already in scope via `use super::*`. Four scenarios to cover:

   - **Empty store:** `GET /api/public/timeline` with no Authorization header returns HTTP 200 and a `Page<Chirp>` with an empty `items` vec and `None` next_cursor.
   - **Multi-user, newest-first:** Register two users, have each post chirps, then call `GET /api/public/timeline` without auth. All chirps from both users appear in the response, ordered newest-first (largest chirp id first).
   - **Cursor pagination:** Create more chirps than the default page size (or pass `?limit=2` with enough chirps). The first page returns the requested limit with a non-None `next_cursor`. The second page (using `?cursor=<value>`) returns the remainder with `None` next_cursor.
   - **No auth required:** Calling `GET /api/public/timeline` with no `Authorization` header returns 200 (not 401). The existing `timeline` endpoint still returns 401 without auth (regression guard).

2. **CI verification** — run `cargo fmt --check`, `cargo clippy`, and `cargo test` (without `--features postgres`) on the branch. Fix any formatting or clippy warnings introduced by any of the CHILD_skeleton / CHILD_in_memory / CHILD_postgres commits before making the final commit.

## Inputs

- Codebase on branch `work/chirp-logged-out` (CHILD_postgres has committed; all impls are real)
- `crates/chirp-server/tests/api.rs` — existing harness to extend
- Parent hub: `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/_GLOBAL.md`

## Declared outputs

- `crates/chirp-server/tests/api.rs` — four new test cases
- Any formatting or lint fixes applied across `crates/chirp-server/`
- `cargo fmt --check`, `cargo clippy`, `cargo test` all pass
- Changes committed on `work/chirp-logged-out`
- `COMPLETE.md` at `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/COMPLETE.md`
- `COMPLETE.md` in this child workspace

## Success criteria

- All four test scenarios pass under `cargo test`.
- `cargo fmt --check` exits 0.
- `cargo clippy` exits 0 (no new warnings).
- The existing test suite (all previously passing tests) is unaffected — especially `timeline_requires_authentication` or equivalent.
- The public-timeline COMPLETE.md records that all CI checks passed.

## Constraints

- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out`
- Nothing committed contains host paths, internal addresses, SSH key paths, or taskflow references.
- Tests are infrastructure-free: they use the existing in-memory harness (`TestApp::new()` / `build_app()`), no database, no network.
