# _BRIEF.md — NSWE overseer step I173 (persona swe-lead) — ACTION: launch remediation DAG sweep-seam-r1-r1

**Depends on**: I172
**Task Kind**: act — load WORK_SESSION + DELIVERABLES_GIT; fork sweep-seam-r1-r1 remediation DAG.

## Context from I172

- **sweep-seam-r1** (swe-coder): FOLDED — SYNTHESIS.md present. Verdict: PASS on all 6 functional ACs.
  - CI machine gate: **FAIL** — fmt check failed (conclusion: FAILURE at 2026-11-03T18:58:55Z). clippy/test/wasm/doc all SUCCESS. image SKIPPED.
  - Branch status: **CONFLICTING** (mergeStateStatus: DIRTY) — branch `work/sweep-seam-r1` has conflicts with main after PR #182 (security-persist-r1, commit c3f9f558) was merged.
  - PR #183: open, CONFLICTING, fmt CI FAIL.
- **ArgoCD**: OutOfSync/Healthy — revision c3f9f558 (still awaiting CI image build from security-persist-r1 merge). Non-blocking.
- **CronJob**: `chirp-transient-sweep-29895540` succeeded (0 failed, 1 succeeded). No second failure. Issue #117 still open.
- **free_dag_slots**: 1
- **main_sha**: `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`
- **project_state.json**: `taskflow/overseer/I164-S1/project_state.json`
- **_CONFIG.yaml**: `taskflow/overseer/_CONFIG.yaml`
- **Remediation budget**: 1st of 2 allowed automatic remediation attempts.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md` before acting.

### 2. Read the config seam
Read `taskflow/overseer/_CONFIG.yaml`.

### 3. Check DAG slots
Confirm free_dag_slots ≥ 1. (As of I172: 1 free slot, no DAGs in flight.)

### 4. Write the remediation DAG brief
Create `taskflow/dags/sweep-seam-r1-r1/_BRIEF.md` for a `swe-coder` remediation DAG.

The remediation brief must carry:
- **Goal**: Issue #117 — Sweep CronJob second source of truth: eliminate duplicate raw SQL, invoke Rust seam for CronJob.
- **Why remediation**: CI fmt check fails on branch `work/sweep-seam-r1` (PR #183). Branch also has conflicts with main after c3f9f558 merge. Remediation must fix fmt and rebase.
- **Prior work**: All 6 functional ACs were met by sweep-seam-r1 (see `taskflow/dags/sweep-seam-r1/SYNTHESIS.md`). The code changes are functionally correct. The only defect is unformatted Rust code.
- **Original ACs** (from issue #117 and the original brief):
  1. Sweep CronJob no longer duplicates DELETE predicates as raw SQL — invoke `ChirpRepository::sweep_expired_transient_state()` instead.
  2. CronJob must succeed in the cluster after merge (new image with sweep subcommand deployed).
  3. Root cause of prior CronJob failures diagnosed and fixed.
  4. `sessions.expires_at` nullability invariant documented and tested.
  5. All existing tests pass; new tests added as appropriate.
  6. PR passes CI (fmt, clippy, test, wasm, doc) on the branch.
- **Lesson from prior attempt**: The sweep-seam-r1 DAG ran `cargo clippy` and `cargo test` locally but did not run `cargo fmt --check` or `cargo fmt` before committing. The fmt gate catches formatting differences the editor or clippy do not. Run `cargo fmt --workspace` and commit the result before pushing.
- **Branch**: `work/sweep-seam-r1` (existing branch — remediate in place).
- **PR**: #183 (already open — do not open a new PR; update the existing one by pushing to the branch).
- **Required actions**:
  1. Rebase `work/sweep-seam-r1` onto `main` (commit c3f9f558) to resolve the CONFLICTING status.
  2. Run `cargo fmt --workspace` and commit any formatting changes.
  3. Run `cargo clippy --workspace --all-targets --locked -- -D warnings` to confirm no regressions.
  4. Run `cargo test --workspace --locked` to confirm tests still pass.
  5. Force-push the rebased, fmt-clean branch to origin.
  6. Confirm CI re-runs on PR #183 and all checks pass.
- **Declared output**: Commits on `work/sweep-seam-r1`; PR #183 updated and CI-green; root `SYNTHESIS.md` at `taskflow/dags/sweep-seam-r1-r1/SYNTHESIS.md` accounting for each AC (met or not and why).
- **Repo**: `Nousix-LLC/nswe-demo`
- **Constraint**: No force-push to main. Do not open a new PR; push to the existing branch so PR #183 updates.

### 5. Write _FORK.md and fork the DAG
Write `taskflow/dags/sweep-seam-r1-r1/_FORK.md` (launch_agent: swe-coder, disposition: reap-whole-after-land, launch_context: application: software).

Fork the DAG at `taskflow/dags/sweep-seam-r1-r1/`.

### 6. Update board and STATE
- Mark issue #117 as still In Progress (already is — no board change needed unless status changed).
- Update `taskflow/overseer/I164-S1/project_state.json`:
  - Move sweep-seam-r1 from dags_folded to a remediation entry noting sweep-seam-r1-r1 dispatched.
  - Add sweep-seam-r1-r1 to dags_in_flight.
  - Update free_dag_slots to 0.
  - Update current_pointer to overseer/I174.

### 7. Write CONTINUE.md and report terminal
Write `I173/CONTINUE.md` with:
- sweep-seam-r1-r1 DAG forked (or if slots unexpectedly full, explain the skip).
- Next iteration I174: board check — observe remediation fold, ArgoCD image update, GitHub activity.

Report terminal `status: completed, thread_evaluation: Continue`.

## Important notes

- landing_authority: delegated, auto_land: true, headless: true (from _CONFIG.yaml).
- Budget: this is attempt 1 of 2 for sweep-seam-r1. If sweep-seam-r1-r1 also fails, attempt 2 (sweep-seam-r1-r2) is the last automatic remediation before user escalation.
- After sweep-seam-r1-r1 folds PASS: launch review DAG (swe-reviewer, review-sweep-seam-r1-r1) per REVIEW_GATE.
- Do not re-open a second PR. Push fixes to work/sweep-seam-r1 so PR #183 tracks them.
