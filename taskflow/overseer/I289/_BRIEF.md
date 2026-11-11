# _BRIEF.md — NSWE overseer step I289 (persona swe-lead) — ACT: bounded watch (review-ferric-async-forms-r3 + chirp-logged-out)

**Depends on**: I288
**Task Kind**: act — load `appfiles/WORK_SESSION.md`.

## Context from I288

I288 checked both DAGs — neither had completed:
- review-ferric-async-forms-r3: SYNTHESIS.md not present — still in flight
- chirp-logged-out: SYNTHESIS.md not present — still in flight

Re-suspended for +15 minutes.

STATE at: `taskflow/overseer/I288/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing file

Load `appfiles/WORK_SESSION.md`.

### 2. Read config seam and prior STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I288/project_state.json`.

### 3. Check DAG progress

**review-ferric-async-forms-r3** (`taskflow/dags/review-ferric-async-forms-r3/SYNTHESIS.md`):
- APPROVE → land PR #193, close #130, update board to Done, groom board after landing
- REQUEST-CHANGES → dispatch ferric-async-forms-r4 (swe-coder) with the new review synthesis as brief, carrying the specific blockers
- Not yet present → DAG still in flight; continue watching

**chirp-logged-out** (`taskflow/dags/chirp-logged-out/SYNTHESIS.md`):
- PASS → dispatch review DAG (swe-reviewer) for PR that the DAG opened
- FAIL → dispatch chirp-logged-out-r2 (swe-coder) remediation carrying the blockers
- Not yet present → DAG still in flight; continue watching

### 4. Act on completed DAGs

For each DAG that has completed, act per the above rules.

### 5. If neither DAG has completed — re-suspend

If both DAGs are still in flight, update STATE and schedule I290 as a fresh bounded watch (+15 minutes).

## Suspension firing condition

```
resumption_condition:
  any_of:
    - { member: schedule, resume_at: "<+15 minutes from dispatch>" }
    - { member: forked-thread-completion, forked_thread: "review-ferric-async-forms-r3" }
    - { member: forked-thread-completion, forked_thread: "chirp-logged-out" }
  deadline: null
```

## Notes

- Write updated STATE at `taskflow/overseer/I289/project_state.json`.
- review-ferric-async-forms-r3 is reviewing PR #193 on branch `work/ferric-async-forms-r2`, epic #130.
- chirp-logged-out is implementing issue #35 on branch `work/chirp-logged-out`.
- Landing authority: delegated (auto_land: true, headless: true from _CONFIG.yaml) — land on APPROVE + machine PASS, no human gate needed.
- Non-blockers #245, #246, #247 are in backlog (Todo) and can be taken into a goal when a DAG slot is free.
