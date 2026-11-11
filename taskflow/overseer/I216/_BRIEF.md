# _BRIEF.md — NSWE overseer step I216 (persona swe-lead) — EVALUATE: board check / watch review folds

**Depends on**: I215
**Task Kind**: evaluate — load `WORK_SESSION` + `REVIEW_GATE`. Check board; watch review-ferric-router-r1 and review-ferric-async-forms-r2 folds.

## Context from I215

- review-ferric-async-forms-r2 launched (swe-reviewer, DAG at `taskflow/dags/review-ferric-async-forms-r2/`). PR #193.
- review-ferric-router-r1 still IN_FLIGHT (forked I213). PR #192.
- free_dag_slots: 1 (both reviews in flight).
- STATE: `taskflow/overseer/I215/project_state.json`.
- Config seam: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/REVIEW_GATE.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I215/project_state.json`.

### 2. Check both review DAGs for folds
- **review-ferric-router-r1**: check `taskflow/dags/review-ferric-router-r1/SYNTHESIS.md` — present or not?
- **review-ferric-async-forms-r2**: check `taskflow/dags/review-ferric-async-forms-r2/SYNTHESIS.md` — present or not?

If either has folded: schedule a fold-read task for it (load WORK_SESSION + REVIEW_GATE; evaluate verdict and schedule processing + landing if APPROVE, or remediation if REQUEST-CHANGES).

### 3. Check for other board activity
- Any new GitHub issues or PR comments since I215?
- Any other DAGs that need attention?
- Backlog: epics #132 (HTTP client), #133, #134–#136 — any ready to launch given current slots?

### 4. Decide what to schedule next
One of:
- If a review has folded with APPROVE + machine PASS: schedule process-review + land tasks.
- If a review has folded with REQUEST-CHANGES: schedule remediation.
- If no folds yet and nothing else actionable: suspend on bounded wake (review-fold OR 7–10 min timer).

## Notes

- Config: delegated/auto_land/headless. On APPROVE for either PR, land without human gate.
- Both review DAGs (review-ferric-router-r1 and review-ferric-async-forms-r2) run as swe-reviewer.
- free_dag_slots=1 as of I215 (both reviews in flight). A fold frees one slot.
