# _BRIEF.md — NSWE overseer step I220 (persona swe-lead) — EVALUATE: board check / watch folds

**Depends on**: I219
**Task Kind**: evaluate — load `WORK_SESSION` + `BOARD`. Check board; watch ferric-router-r2 and ferric-async-forms-r3 folds.

## Context from I219

- ferric-router-r2 launched (swe-coder, DAG at `taskflow/dags/ferric-router-r2/`). Goal: split PR #192 into clean 4-commit router-only PR. Issues #131/#146/#147.
- ferric-async-forms-r3 launched (swe-coder, DAG at `taskflow/dags/ferric-async-forms-r3/`). Goal: fix 3 blockers from review-ferric-async-forms-r2. Issues #130/#143/#144/#145.
- free_dag_slots: 1.
- STATE: `taskflow/overseer/I219/project_state.json`.
- Config seam: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I219/project_state.json`.

### 2. Check both remediation DAGs for folds
- **ferric-router-r2**: check `taskflow/dags/ferric-router-r2/SYNTHESIS.md` — present or not?
- **ferric-async-forms-r3**: check `taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md` — present or not?

If either has folded: schedule a fold-read task for it (load WORK_SESSION + REVIEW_GATE; evaluate verdict and schedule review launch if PASS, or further remediation/escalation if FAIL).

### 3. Check for board activity
- Any new GitHub issues or PR comments since I219?
- Has PR #192 been closed by the ferric-router-r2 DAG yet?
- Any other DAGs that need attention?
- Backlog: epics #132 (HTTP client), #133, #134–#136 — any ready to launch given current slots? (free_dag_slots=1; hold for now)

### 4. Decide what to schedule next
One of:
- If a remediation has folded with PASS: schedule machine-gate read + review launch tasks.
- If a remediation has folded with FAIL: schedule escalation (both have limited remaining budget).
- If no folds yet and nothing else actionable: suspend on bounded wake (fold OR 7–10 min timer).

## Notes

- Config: delegated/auto_land/headless.
- Both remediations are in-flight (ferric-router-r2, ferric-async-forms-r3).
- ferric-async-forms-r3 is the first genuine remediation attempt; 1 attempt remaining (escalate to user if r3 also fails).
- ferric-router-r2 is the first remediation attempt for the router goal (1 attempt remaining).
