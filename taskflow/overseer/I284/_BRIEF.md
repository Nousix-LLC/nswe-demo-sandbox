# _BRIEF.md — NSWE overseer step I284 (persona swe-lead) — ACT: bounded watch (review-ferric-ssr-r2 + review-ferric-async-forms-r3)

**Depends on**: I283
**Task Kind**: act — load `appfiles/BOARD.md`.

## Context from I283

I283 (mechanical-wake reconstruction, timer fired) checked both in-flight DAGs and found:

- **review-ferric-ssr-r2** (`taskflow/dags/review-ferric-ssr-r2/SYNTHESIS.md`): Not yet present — still in flight. Watching for PR #228 re-review (B1 hydrate() wiring + B2 wasm-bindgen-test).
- **review-ferric-async-forms-r3** (`taskflow/dags/review-ferric-async-forms-r3/SYNTHESIS.md`): Not yet present — still in flight. Watching for PR #193 re-review (B1 reactive Resource, B2 EventHandler/prevent_default, B3 DOM→signal).

STATE at: `taskflow/overseer/I284/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing file

Load `appfiles/BOARD.md`.

### 2. Read config seam and prior STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I283/project_state.json`.

### 3. Check DAG progress

**review-ferric-ssr-r2** (`taskflow/dags/review-ferric-ssr-r2/SYNTHESIS.md`):
- APPROVE → land PR #228, close #223/#224/#226 (and move their board items to Done), dispatch issue #35 goal
- REQUEST-CHANGES → dispatch ferric-ssr-r5 (swe-coder) with the new review synthesis as brief, carrying the specific blockers
- Not yet present → DAG still in flight; continue watching

**review-ferric-async-forms-r3** (`taskflow/dags/review-ferric-async-forms-r3/SYNTHESIS.md`):
- APPROVE → land PR #193, close #130, update board to Done
- REQUEST-CHANGES → dispatch ferric-async-forms-r4 (swe-coder) with the new review synthesis as brief, carrying blockers
- Not yet present → DAG still in flight; continue watching

### 4. Act on completed DAGs

For each DAG that has completed:
- **Review APPROVE**: land the PR per `appfiles/DELIVERABLES_GIT.md`, close associated issues, update board.
- **Review REQUEST-CHANGES**: dispatch fresh code remediation DAG carrying new review synthesis and blockers.

### 5. If neither DAG has completed — re-suspend

If both DAGs are still in flight, update STATE and schedule I285 as a fresh bounded watch (+15 minutes).

## Suspension firing condition

```
resumption_condition:
  any_of:
    - { member: schedule, resume_at: "<+15 minutes from dispatch>" }
    - { member: forked-thread-completion, forked_thread: "review-ferric-ssr-r2" }
    - { member: forked-thread-completion, forked_thread: "review-ferric-async-forms-r3" }
  deadline: null
```

## Notes

- Write updated STATE at `taskflow/overseer/I284/project_state.json`.
- review-ferric-ssr-r2 is reviewing PR #228 on branch `work/ferric-ssr-r1`, issues #223/#224/#226.
- review-ferric-async-forms-r3 is reviewing PR #193 on branch `work/ferric-async-forms-r2`, epic #130.
- Landing authority: delegated (auto_land: true, headless: true from _CONFIG.yaml) — land on APPROVE + machine PASS, no human gate needed.
- The escalation comments on PR #228 and PR #193 are obsoleted — do not post additional escalation comments unless a new true user-only gate arises.
