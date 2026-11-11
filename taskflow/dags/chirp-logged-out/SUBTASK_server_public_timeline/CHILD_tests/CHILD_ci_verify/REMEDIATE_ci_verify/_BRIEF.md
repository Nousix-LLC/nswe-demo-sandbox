# _BRIEF.md — REMEDIATE_ci_verify

**Parent task:** CHILD_ci_verify (failed — this task is remediation synthesis)
**Parent hub:** `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/_GLOBAL.md`

## Task Specification

**Slug:** REMEDIATE_ci_verify
**Task Kind:** synthesis
**Depends on:** REMEDIATE_write_tests
**Status:** Pending

## Objective

This task is a **verification gate**. After REMEDIATE_write_tests commits the test code, run all three CI checks (`cargo fmt --check`, `cargo clippy`, `cargo test`) against `crates/chirp-server/` on branch `work/chirp-logged-out`. Fix any formatting or clippy warnings. Author the two declared COMPLETE.md records. Author `CHILD_tests/SYNTHESIS.md` as the fold record and fold the `CHILD_tests` parent SUSPENDED → COMPLETED via `engine_resume_suspended`.

## Context

REMEDIATE_implementation and REMEDIATE_write_tests will have committed the full implementation and tests. This gate verifies the branch is clean and the tests pass, then synthesizes the CHILD_tests subtree.

## Inputs

- Branch `work/chirp-logged-out` with all implementation and test commits from REMEDIATE_implementation and REMEDIATE_write_tests
- `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/contracts/_MANIFEST.yaml` — four identities to assert: fmt, clippy, test, no leaked secrets
- `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/_GLOBAL.md` — gate context

## Gate checks (all four must pass)

- `cargo fmt --check -p chirp-server` → exit 0
- `cargo clippy -p chirp-server --all-targets -- -D warnings` → exit 0
- `cargo test -p chirp-server` → exit 0 (all tests pass, including the four new `public_timeline` tests)
- No host paths, internal addresses, SSH key paths, or taskflow references in committed code

## Declared outputs

- `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/COMPLETE.md` — records that all four CI checks passed, lists commits on the branch, confirms the public_timeline endpoint is fully implemented and tested
- `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/SYNTHESIS.md` — fold record (verification gate result)
- Any fmt/clippy fix commits on `work/chirp-logged-out` (if needed)
- `COMPLETE.md` in this workspace
- `CHILD_tests` SUSPENDED → COMPLETED (via `engine_resume_suspended`)

## Success criteria

- All four gate identities hold
- `SUBTASK_server_public_timeline/COMPLETE.md` authored
- `CHILD_tests/SYNTHESIS.md` authored at the fold location
- `engine_resume_suspended` called with CHILD_tests as target, this task as synthesized, and `CHILD_tests/SYNTHESIS.md` as seam_path
- `CHILD_tests` lifecycle state observable as COMPLETED after the fold

## Constraints

- Build server: `mattm@100.90.75.93`, codebase at `~/nswe-demo`
- Run cargo without `--features postgres` (in-memory harness tests only)
- Branch: `work/chirp-logged-out`
- Nothing committed contains host paths, internal addresses, SSH key paths, or taskflow references
- If any gate identity fails and cannot be fixed, report FAILED with structured description — do NOT silently plug

## Suggested Methodology Files

Domain mapping: **Verifying a build (synthesis gate)** → primary `synthesis`, supporting `operations`

- `synthesis/Synthesis_Overview_Methodology.md` — verification gate model: four-check model, go/no-go decision (ALWAYS load this first)
- `synthesis/Synthesis_Contract_Verification_Methodology.md` — asserting identities from `contracts/_MANIFEST.yaml`
- `operations/DevTools_CICD_Methodology.md` — CI check patterns

These are parent-flagged suggestions; the agent is the final judge.

## Gate posture (MANDATORY — this is a verification gate, not a prose summary)

This task MUST assert all four identities from `contracts/_MANIFEST.yaml`. If a formatting or clippy issue is fixable: fix it, commit, re-run. If not fixable within this invocation: report FAILED with a structured description of which check failed, what was observed, and what was attempted. Do NOT author SYNTHESIS.md with a failed gate.

## Inherited Constraints

- Run CI commands without `--features postgres`
- The fold target is CHILD_tests (the SUSPENDED NeedsDecompose parent). The seam path is `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/SYNTHESIS.md`.
