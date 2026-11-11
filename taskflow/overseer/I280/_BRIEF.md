# _BRIEF.md — NSWE overseer step I280 (persona swe-lead) — ACT: bounded watch (ferric-ssr-r4 + ferric-async-forms-r3)

**Depends on**: I279
**Task Kind**: act — load `appfiles/BOARD.md`.

## Context from I279

I279 reclassified both escalations (ferric-ssr + ferric-async-forms) as ordinary remediation per corrected app policy (REQUEST-CHANGES from a review is not a budget-exhausted escalation), and dispatched two code DAGs:

- **ferric-ssr-r4** (`forked_thread_id: ferric-ssr-r4`): Remediating PR #228 B1 (hydrate() wiring from WASM entry point) and B2 (wasm-bindgen-test coverage in hydrate.rs). Synthesis at: `taskflow/dags/ferric-ssr-r4/SYNTHESIS.md`
- **ferric-async-forms-r3** (`forked_thread_id: ferric-async-forms-r3`): Remediating PR #193 B1 (reactive Resource/create_resource), B2 (prevent_default/stop_propagation), B3 (DOM→signal binding). Synthesis at: `taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md`

STATE at: `taskflow/overseer/I279/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing file

Load `appfiles/BOARD.md`.

### 2. Read config seam and prior STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I279/project_state.json`.

### 3. Check DAG progress

For each in-flight DAG, check whether SYNTHESIS.md exists and what the verdict is:

**ferric-ssr-r4** (`taskflow/dags/ferric-ssr-r4/SYNTHESIS.md`):
- PASS → dispatch `review-ferric-ssr-r2` review DAG for PR #228
- FAIL → evaluate: dispatch ferric-ssr-r5 (if the fail is recoverable) or escalate (if not)
- Not yet present → DAG still in flight; continue watching

**ferric-async-forms-r3** (`taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md`):
- PASS → dispatch `review-ferric-async-forms-r3` review DAG for PR #193
- FAIL → evaluate: dispatch ferric-async-forms-r4 (if recoverable) or escalate (if not)
- Not yet present → DAG still in flight; continue watching

### 4. Act on completed DAGs

For each DAG that has completed:
- **Code PASS**: dispatch a review DAG (`swe-reviewer`) with the PR details, branch, review synthesis from code DAG, and acceptance criteria.
- **Code FAIL**: dispatch a fresh code remediation DAG carrying the failure synthesis and original blockers as the brief. Record the attempt.

### 5. If neither DAG has completed — re-suspend

If both DAGs are still in flight, update STATE (note: re-checked, both still running) and schedule I281 as a fresh bounded watch (+15 minutes).

## Suspension firing condition

```
resumption_condition:
  any_of:
    - { member: schedule, resume_at: "<+15 minutes from dispatch>" }
    - { member: forked-thread-completion, forked_thread: "ferric-ssr-r4" }
    - { member: forked-thread-completion, forked_thread: "ferric-async-forms-r3" }
  deadline: null
```

## Notes

- Write updated STATE at `taskflow/overseer/I280/project_state.json`.
- ferric-ssr-r4 is on branch `work/ferric-ssr-r1`, PR #228, issues #223/#224/#226.
- ferric-async-forms-r3 is on branch `work/ferric-async-forms-r2`, PR #193, epic #130.
- The escalation comments on PR #228 and PR #193 may be noted as resolved (closed or obsoleted) once the new code DAGs land — do not post additional escalation comments unless a new true user-only gate arises.
