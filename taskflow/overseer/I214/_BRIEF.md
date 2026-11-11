# _BRIEF.md — NSWE overseer step I214 (persona swe-lead) — EVALUATE: fold-read ferric-async-forms-r2 + machine gate

**Depends on**: I213
**Task Kind**: evaluate — load `WORK_SESSION` + `REVIEW_GATE`. Fold-read ferric-async-forms-r2 and confirm machine gate.

## Context from I213

- review-ferric-router-r1 launched (swe-reviewer, forked in I213). Now in dags_in_flight.
- free_dag_slots: 3 (was 4; review-ferric-router-r1 now in flight).
- ferric-async-forms-r2 folded (COMPLETE.md at `taskflow/dags/ferric-async-forms-r2/COMPLETE.md`).
  PR #193: OPEN/MERGEABLE, `work/ferric-async-forms-r2` → `main`.
  Issues: #130 (async resources + suspense), #143 (DOM events), #144 (form bindings), #145 (further async concerns).
  CI run 41780600207 — all 6 SUCCESS.
- review-ferric-router-r1 is now in dags_in_flight.
- STATE: `taskflow/overseer/I213/project_state.json`.
- Config seam: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/REVIEW_GATE.md`. Read `_CONFIG.yaml` and
`taskflow/overseer/I213/project_state.json`.

### 2. Fold-read ferric-async-forms-r2

Read `taskflow/dags/ferric-async-forms-r2/COMPLETE.md` (the DAG's terminal record).
Confirm:
- All 6 CI checks PASS on the head commit.
- PR #193 OPEN and MERGEABLE.
- Issues #130, #143, #144, #145: each acceptance criterion met per COMPLETE.md.
- Machine gate: PASS (confirmed from COMPLETE.md review — all CI green, correct repo nswe-demo, ACs met).

### 3. Decide what follows

If machine gate PASS:
- Schedule I215 (ACT: launch review for PR #193).
- Schedule I216 (EVALUATE: board check / watch review folds: review-ferric-router-r1 and review-ferric-async-forms-r2).

If machine gate FAIL:
- Assess remediation budget (remediation_attempt=2, remediation_budget=2 — EXHAUSTED).
- Escalate to user with both attempt summaries.

### 4. Update STATE

Write `taskflow/overseer/I214/project_state.json`:
- Record ferric-async-forms-r2 machine gate result.
- Update forward_series with I214 entry.

## Notes

- I215 follows: ACT — launch review for PR #193 (loads REVIEW_GATE + WORK_SESSION).
- Design reference for ferric-async-forms-r2: `design/ferric/async-forms-events.md` (REQ-ASYNC-001..024, REQ-ASYNC-040..043).
