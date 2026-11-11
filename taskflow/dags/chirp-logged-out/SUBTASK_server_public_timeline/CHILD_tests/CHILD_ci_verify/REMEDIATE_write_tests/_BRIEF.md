# _BRIEF.md — REMEDIATE_write_tests

**Parent task:** CHILD_ci_verify (failed — this task is remediation)
**Parent hub:** `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/_GLOBAL.md`

## Task Specification

**Slug:** REMEDIATE_write_tests
**Task Kind:** standard
**Depends on:** REMEDIATE_implementation
**Status:** Pending

## Objective

Add the `public_timeline` stub to `UnhealthyStore` and four integration tests in `crates/chirp-server/tests/api.rs` on branch `work/chirp-logged-out`. Commit the changes.

## Background

The original `CHILD_write_tests` claimed to have committed these tests (commit `d57335d`) but that commit does not exist. `REMEDIATE_implementation` will have created the branch and all implementation code. This task adds the test layer on top.

## Inputs

- `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/_GLOBAL.md` — contains the exact test cases to write (function signatures, test logic, assertion shape) and the exact `UnhealthyStore` stub to add.
- Branch `work/chirp-logged-out` on the build server with implementation committed by REMEDIATE_implementation.
- `crates/chirp-server/tests/api.rs` on the branch — the existing test file to extend.

## Scope

- `crates/chirp-server/tests/api.rs` — add `public_timeline` stub to `UnhealthyStore` and add `mod public_timeline` with four `#[tokio::test]` functions as specified in `CHILD_tests/_GLOBAL.md`.

## Declared outputs

- `crates/chirp-server/tests/api.rs` modified with UnhealthyStore stub and four test cases, committed on `work/chirp-logged-out`
- `COMPLETE.md` in this workspace

## Success criteria

- Four `#[tokio::test]` functions present in a `mod public_timeline` block in `tests/api.rs`:
  1. `public_timeline_empty_store_returns_200_with_empty_page`
  2. `public_timeline_includes_all_users_newest_first`
  3. `public_timeline_paginates_with_cursor`
  4. `public_timeline_requires_no_auth`
- `UnhealthyStore` has a `public_timeline` method stub so the file compiles
- Commit exists on `work/chirp-logged-out`
- Nothing committed contains host paths, internal addresses, SSH key paths, or taskflow references
- Existing test helpers (`TestApp`, `build_app`, etc.) are unchanged

## Constraints

- Build server: `mattm@100.90.75.93`, codebase at `~/nswe-demo`
- Use `bash -lc` to load server PATH
- Tests are infrastructure-free (use the existing `TestApp::new()` / `build_app()` in-process harness, no database, no network)
- Do NOT modify the existing tests or any other file beyond `tests/api.rs`
- Commit message: `test(chirp-server): add integration tests for public_timeline endpoint`

## Suggested Methodology Files

Domain mapping: **Writing tests** → primary `testing`, supporting `core`

- `testing/Testing_Integration_Testing_Methodology.md` — in-process integration test patterns
- `testing/Testing_Unit_Testing_Methodology.md` — test structure conventions

These are parent-flagged suggestions; the agent is the final judge.

## Inherited Constraints

- Follow the existing test harness pattern exactly (see `CHILD_tests/_GLOBAL.md` for the `TestApp` / `build_app` conventions)
- Tests call `GET /api/public/timeline` — the route is unauthenticated
