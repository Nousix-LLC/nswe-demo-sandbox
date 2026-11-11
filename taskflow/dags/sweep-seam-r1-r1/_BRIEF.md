# _BRIEF.md — sweep-seam-r1-r1 (swe-coder remediation DAG)

## Goal
Remediate PR #183 (`work/sweep-seam-r1`): fix the CI fmt failure and rebase onto main (commit `c3f9f558`) so PR #183 is clean and all CI checks pass.

**GitHub issue**: #117 — Sweep CronJob second source of truth: eliminate duplicate raw SQL, invoke Rust seam for CronJob.

## Why remediation
The prior code DAG `sweep-seam-r1` met all 6 functional acceptance criteria (see `taskflow/dags/sweep-seam-r1/SYNTHESIS.md`). The code changes are functionally correct. Two defects remain:
1. **CI fmt failure**: the CI `cargo fmt --check` gate failed on PR #183 (conclusion `FAILURE` at 2026-11-03T18:58:55Z). The DAG ran `cargo clippy` and `cargo test` but did not run `cargo fmt --workspace` before committing.
2. **Branch conflict**: `work/sweep-seam-r1` is CONFLICTING with main after PR #182 (`security-persist-r1`, commit `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`) was merged.

## Prior work
All 6 functional ACs were met by `sweep-seam-r1`. The changes are:
- `crates/chirp-server/src/main.rs`: dispatch on `sweep` CLI argument → `run_sweep()` → `ChirpRepository::sweep_expired_transient_state()`
- `deploy/chirp/50-transient-sweep-cronjob.yaml`: rewritten to use chirp-server image, invoke `sweep` subcommand, use `CHIRP_DATABASE_URL`
- New test: `login_always_stamps_a_bounded_session_expiry`

See `taskflow/dags/sweep-seam-r1/SYNTHESIS.md` for the full verdict.

## Acceptance criteria (all must be met)
1. Sweep CronJob no longer duplicates DELETE predicates as raw SQL — invoke `ChirpRepository::sweep_expired_transient_state()` instead.
2. CronJob will succeed in the cluster after merge (new image with sweep subcommand deployed).
3. Root cause of prior CronJob failures diagnosed and fixed.
4. `sessions.expires_at` nullability invariant documented and tested.
5. All existing tests pass; new tests added as appropriate.
6. PR #183 passes CI (fmt, clippy, test, wasm, doc) on the branch — this is the specific defect to remediate.

## Lesson from prior attempt
The `sweep-seam-r1` DAG ran `cargo clippy` and `cargo test` locally but did not run `cargo fmt --check` or `cargo fmt` before committing. The fmt gate catches formatting differences that the editor or clippy do not. **Run `cargo fmt --workspace` and commit the result before pushing.**

## Required actions
1. Rebase `work/sweep-seam-r1` onto `main` (commit `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`) to resolve the CONFLICTING status.
2. Run `cargo fmt --workspace` and commit any formatting changes.
3. Run `cargo clippy --workspace --all-targets --locked -- -D warnings` to confirm no regressions.
4. Run `cargo test --workspace --locked` to confirm tests still pass.
5. Force-push the rebased, fmt-clean branch to origin (`work/sweep-seam-r1`).
6. Confirm CI re-runs on PR #183 and all checks pass.

## Branch and PR
- **Branch**: `work/sweep-seam-r1` (existing branch — remediate in place, do not create a new branch)
- **PR**: #183 (already open — do not open a new PR; push to the existing branch so PR #183 updates)

## Inputs
- Repository: `Nousix-LLC/nswe-demo`
- Prior synthesis: `taskflow/dags/sweep-seam-r1/SYNTHESIS.md`
- Main at: `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`

## Declared output
- Commits on `work/sweep-seam-r1` (rebased, fmt-clean)
- PR #183 updated (pushed to the existing branch) with all CI checks passing
- Root `SYNTHESIS.md` at `taskflow/dags/sweep-seam-r1-r1/SYNTHESIS.md` accounting for each AC (met or not met, and why)

## Constraints
- Do NOT force-push to `main`
- Do NOT open a new PR; push fixes to `work/sweep-seam-r1` so PR #183 tracks them
- Repo scope: `Nousix-LLC/nswe-demo` only
