# COMPLETE — CHILD_ci_verify Failure Handler

## Summary

This node is the failure handler for `CHILD_ci_verify`. It diagnosed the root cause of the failure, authored the full remediation plan as three `_BRIEF.md` files, and attempted to inject them into the scheduler. The scheduler was in `Failed` phase and could not accept `add_task` amendments.

The remediation plan is fully authored and available on disk.

---

## Root Cause

Branch `work/chirp-logged-out` and all commits cited by predecessor tasks (`1d8edab`, `7160514`, `ec70b78`, `d57335d`) do not exist in any git repository. The predecessor tasks (CHILD_skeleton, CHILD_in_memory, CHILD_postgres, CHILD_write_tests) each authored `COMPLETE.md` records claiming specific commits, but those git operations did not persist. The commits do not exist in git object storage.

As a result, `CHILD_ci_verify` could not run any CI checks — there was nothing to verify.

Full diagnosis: `FAILURE.md` in this directory.

---

## Remediation Plan (Authored — Not Injected)

Three `_BRIEF.md` files were authored in this directory. Each is a fully specified task. They must be executed in dependency order:

### 1. REMEDIATE_implementation
**Path:** `REMEDIATE_implementation/_BRIEF.md`  
**Depends on:** none  
**Scope:** Create branch `work/chirp-logged-out` from `main` at `62febf5faf6023b3492365d246c7ac39c9f659a3`. Implement the full `public_timeline` feature:
- `crates/chirp-server/src/repository/mod.rs` — `public_timeline` trait method
- `crates/chirp-server/src/repository/in_memory.rs` — `InMemoryRepository::public_timeline`
- `crates/chirp-server/src/repository/postgres.rs` — `PostgresRepository::public_timeline` (feature-gated)
- `crates/chirp-server/src/api/handlers.rs` — axum handler
- `crates/chirp-server/src/api/router.rs` — `GET /public/timeline` route mount
- Gate: `cargo build -p chirp-server` → exit 0
- Commit on the branch

### 2. REMEDIATE_write_tests
**Path:** `REMEDIATE_write_tests/_BRIEF.md`  
**Depends on:** REMEDIATE_implementation  
**Scope:** Add `public_timeline` stub to `UnhealthyStore` and four `#[tokio::test]` functions to `crates/chirp-server/tests/api.rs`:
1. `public_timeline_empty_store_returns_200_with_empty_page`
2. `public_timeline_includes_all_users_newest_first`
3. `public_timeline_paginates_with_cursor`
4. `public_timeline_requires_no_auth`

Commit on the branch.

### 3. REMEDIATE_ci_verify
**Path:** `REMEDIATE_ci_verify/_BRIEF.md`  
**Depends on:** REMEDIATE_write_tests  
**Task Kind:** synthesis  
**Scope:** Run all three CI checks (`cargo fmt --check -p chirp-server`, `cargo clippy -p chirp-server --all-targets -- -D warnings`, `cargo test -p chirp-server`) on `work/chirp-logged-out`. Fix any fmt/clippy issues. Author `SUBTASK_server_public_timeline/COMPLETE.md` and `CHILD_tests/SYNTHESIS.md`. Call `engine_resume_suspended` to fold `CHILD_tests` SUSPENDED → COMPLETED.

---

## Plan Amendment Status

**Attempted:** Yes — `mcp__hal__amend_plan { operation: "add_task" }` called for `REMEDIATE_implementation`  
**Result:** `amendment failed: scheduler apply failed: pause_for_amendment: amendment not allowed: scheduler is in Failed phase, expected Running`  

The scheduler had already transitioned to `Failed` phase when this handler executed. New tasks cannot be injected into a Failed-phase DAG via `add_task`.

**Action required:** A human operator or the orchestrating session must restart or re-dispatch the `chirp-logged-out` DAG, supplying the three `_BRIEF.md` files authored here as the remediation specification.

---

## Outputs

| Artifact | Path | Status |
|----------|------|--------|
| Root cause diagnosis | `FAILURE.md` (pre-existing, authored by CHILD_ci_verify) | ✓ |
| REMEDIATE_implementation brief | `REMEDIATE_implementation/_BRIEF.md` | ✓ Authored |
| REMEDIATE_write_tests brief | `REMEDIATE_write_tests/_BRIEF.md` | ✓ Authored |
| REMEDIATE_ci_verify brief | `REMEDIATE_ci_verify/_BRIEF.md` | ✓ Authored |
| Scheduler injection | n/a | ✗ Blocked (scheduler in Failed phase) |
