# _BRIEF.md — NSWE overseer step I281 (persona swe-lead) — ACT: bounded watch (review-ferric-ssr-r2 + ferric-async-forms-r3)

**Depends on**: I280
**Task Kind**: act — load `appfiles/BOARD.md`.

## Context from I280

I280 (mechanical-wake reconstruction, timer fired at 2026-11-05T22:45Z) checked both in-flight code DAGs and found:

- **ferric-ssr-r4** (`taskflow/dags/ferric-ssr-r4/SYNTHESIS.md`): **PASS** — 7 CI checks green on commit `75c1eef`. B1 (hydrate() wiring from WASM entry point) and B2 (wasm-bindgen-test coverage in hydrate.rs) both resolved. `review-ferric-ssr-r2` dispatched for PR #228.
- **ferric-async-forms-r3** (`taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md`): Still in flight. Remediating PR #193 B1 (reactive Resource/create_resource), B2 (prevent_default/stop_propagation), B3 (DOM→signal binding).

STATE at: `taskflow/overseer/I281/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing file

Load `appfiles/BOARD.md`.

### 2. Read config seam and prior STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I281/project_state.json`.

### 3. Check DAG progress

**review-ferric-ssr-r2** (`taskflow/dags/review-ferric-ssr-r2/SYNTHESIS.md`):
- APPROVE → land PR #228, close #223/#224/#226 (and move their board items to Done), dispatch issue #35 goal
- REQUEST-CHANGES → dispatch ferric-ssr-r5 (swe-coder) with the new review synthesis as brief, carrying the specific blockers
- Not yet present → DAG still in flight; continue watching

**ferric-async-forms-r3** (`taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md`):
- PASS → dispatch `review-ferric-async-forms-r3` review DAG for PR #193
- FAIL → evaluate: dispatch ferric-async-forms-r4 (if recoverable) or escalate (if not)
- Not yet present → DAG still in flight; continue watching

### 4. Act on completed DAGs

For each DAG that has completed:
- **Code PASS**: dispatch a review DAG (`swe-reviewer`) with PR details, branch, review synthesis from code DAG, and acceptance criteria.
- **Code FAIL**: dispatch a fresh code remediation DAG carrying the failure synthesis and original blockers.
- **Review APPROVE**: land the PR per `appfiles/DELIVERABLES_GIT.md`, close associated issues, update board.
- **Review REQUEST-CHANGES**: dispatch fresh code remediation DAG carrying new review synthesis and blockers.

### 5. If neither DAG has completed — re-suspend

If both DAGs are still in flight, update STATE and schedule I282 as a fresh bounded watch (+15 minutes).

## Suspension firing condition

```
resumption_condition:
  any_of:
    - { member: schedule, resume_at: "<+15 minutes from dispatch>" }
    - { member: forked-thread-completion, forked_thread: "review-ferric-ssr-r2" }
    - { member: forked-thread-completion, forked_thread: "ferric-async-forms-r3" }
  deadline: null
```

## Notes

- Write updated STATE at `taskflow/overseer/I281/project_state.json`.
- review-ferric-ssr-r2 is reviewing PR #228 on branch `work/ferric-ssr-r1`, issues #223/#224/#226.
- ferric-async-forms-r3 is on branch `work/ferric-async-forms-r2`, PR #193, epic #130.
- The escalation comments on PR #228 and PR #193 are obsoleted — do not post additional escalation comments unless a new true user-only gate arises.
- Landing authority: delegated (auto_land: true, headless: true from _CONFIG.yaml) — land on APPROVE + machine PASS, no human gate needed.
