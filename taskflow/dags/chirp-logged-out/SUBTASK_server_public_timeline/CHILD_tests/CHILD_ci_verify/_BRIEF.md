# _BRIEF.md — CHILD_ci_verify

**Parent task:** CHILD_tests (decomposed)  
**Parent hub:** `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/_GLOBAL.md`

## Task Specification

**Slug:** CHILD_ci_verify  
**Task Kind:** synthesis  
**Depends on:** CHILD_write_tests  
**Status:** Pending

## Objective

This task is a **verification gate**. After CHILD_write_tests commits the test code, run all three CI checks (`cargo fmt --check`, `cargo clippy`, `cargo test`) against `crates/chirp-server/` on branch `work/chirp-logged-out`. Fix any formatting or clippy warnings introduced by any of the CHILD_skeleton / CHILD_in_memory / CHILD_postgres / CHILD_write_tests commits. Make a fix commit if changes are needed. Author the two declared `COMPLETE.md` records. Author `SYNTHESIS.md` as the fold record and fold the CHILD_tests parent SUSPENDED → COMPLETED.

## Context

CHILD_write_tests will have committed the four test cases and the `UnhealthyStore::public_timeline` stub. All prior implementation commits (skeleton, in_memory, postgres) are also on the branch. This task verifies the branch is clean (no formatting or lint issues) and the full test suite passes.

## Inputs

- Codebase on `work/chirp-logged-out` with CHILD_write_tests committed
- `contracts/_MANIFEST.yaml` — identities to assert (all four must pass: fmt, clippy, test, no leaked secrets)
- Parent hub: `_GLOBAL.md` — context and what COMPLETE.md should record

## Work to perform

### Step 1: Run CI checks

Run against `crates/chirp-server/` (without `--features postgres`):

```bash
cd /home/user/nswe-demo
cargo fmt --check -p chirp-server
cargo clippy -p chirp-server --all-targets -- -D warnings
cargo test -p chirp-server
```

If the commands are unavailable directly, check `/home/user/.cargo/bin/` for `cargo`.

### Step 2: Fix any issues

**Formatting failures** (`fmt --check` exits non-zero): run `cargo fmt -p chirp-server` to auto-format, then commit the formatting fixes with message `"style(chirp-server): apply cargo fmt to work/chirp-logged-out"`.

**Clippy warnings treated as errors**: fix each warning in the relevant source file, then commit with message `"fix(chirp-server): resolve clippy warnings on work/chirp-logged-out"`.

**Test failures**: diagnose the failure, fix the root cause (likely in the test code from CHILD_write_tests or in the implementation), commit the fix.

If no issues are found, no additional commit is needed.

### Step 3: Verify all four CI checks pass (gate assertion)

Assert against the identities in `contracts/_MANIFEST.yaml`:
- [ ] `cargo fmt --check` exits 0
- [ ] `cargo clippy -p chirp-server --all-targets -- -D warnings` exits 0
- [ ] `cargo test -p chirp-server` exits 0 (all tests pass, including the four new ones)
- [ ] No host paths, internal addresses, SSH key paths, or taskflow references in committed code

If any identity fails and cannot be fixed, report FAILED with a structured description of which check failed, what was observed, and what was attempted.

### Step 4: Author declared outputs and fold

**Author `SUBTASK_server_public_timeline/COMPLETE.md`:**
Path: `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/COMPLETE.md`

Content: record that all four CI checks passed, list the commits on the branch, and state that the public_timeline endpoint is fully implemented and tested.

**Author `CHILD_tests/SYNTHESIS.md` (fold record):**
Path: `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/SYNTHESIS.md`

Content: verification gate result — which CI checks ran, what was observed (exit codes, test counts), whether any fixes were applied, identities asserted from `contracts/_MANIFEST.yaml`.

**Fold CHILD_tests SUSPENDED → COMPLETED:**
Call `engine_resume_suspended` with:
- `target_task_id`: the task id of CHILD_tests (the parent that is SUSPENDED/NeedsDecompose)
- `synthesized_task_id`: this task's id (CHILD_ci_verify)
- `seam_path`: absolute path to `CHILD_tests/SYNTHESIS.md`

## Declared outputs

- `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/COMPLETE.md` — parent task completion record
- `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/SYNTHESIS.md` — fold record
- Any fmt/clippy fix commits on `work/chirp-logged-out` (if needed)
- All CI checks pass: `cargo fmt --check`, `cargo clippy`, `cargo test` exit 0
- `COMPLETE.md` in this workspace

## Success criteria

- `cargo fmt --check -p chirp-server` exits 0
- `cargo clippy -p chirp-server --all-targets -- -D warnings` exits 0
- `cargo test -p chirp-server` exits 0 — all tests pass, including the four new `public_timeline` tests
- `SUBTASK_server_public_timeline/COMPLETE.md` authored
- `CHILD_tests/SYNTHESIS.md` authored and fold called
- No host paths, internal addresses, SSH key paths, or taskflow references in any committed file

## Constraints

- Run cargo without `--features postgres` (in-memory harness tests only)
- Branch: `work/chirp-logged-out`
- Nothing committed contains host paths, internal addresses, SSH key paths, or taskflow references

## Suggested Methodology Files

Domain mapping row: **CI/CD setup + verifying a build** → primary `operations`, supporting `testing` and `synthesis`

Specific files:
- `operations/DevTools_CICD_Methodology.md` — CI check patterns, what constitutes a passing CI gate
- `operations/DevTools_Build_Systems_Methodology.md` — cargo build and test toolchain
- `synthesis/Synthesis_Overview_Methodology.md` — verification gate model: four-check model, go/no-go decision, remediation-as-decomposition if failures cannot be fixed
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — asserting the identities declared in `contracts/_MANIFEST.yaml`

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires.

## Inherited Constraints

- CI commands: `cargo fmt --check`, `cargo clippy`, `cargo test` (no `--features postgres`)
- Rust toolchain is available on the build machine
- Branch: `work/chirp-logged-out`

## Gate posture (MANDATORY — this is a verification gate, not a prose summary)

This task MUST run all three CI checks and assert all four identities from `contracts/_MANIFEST.yaml`. If any identity fails:
- If fixable (formatting, clippy lint): fix and re-run, commit the fix.
- If not fixable within this invocation: report FAILED with structured description.

A PASS result means all identities hold. A FAIL result means at least one identity does not hold and could not be remediated. Do NOT silently plug a failure.
