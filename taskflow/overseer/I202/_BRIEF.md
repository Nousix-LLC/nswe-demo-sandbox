# _BRIEF.md — NSWE overseer step I202 (persona swe-lead) — EVALUATE: board check / watch review fold (review-ferric-epic-authoring-r1)

**Depends on**: I201
**Task Kind**: evaluate — load `WORK_SESSION`, `REVIEW_GATE`; check whether `review-ferric-epic-authoring-r1` has folded; act on what is found.

## Context from I201

- Review DAG `review-ferric-epic-authoring-r1` launched (swe-reviewer) for PR #188.
- PR #188: `feat(ferric): Ferric 1.0 Authoring Model — view!, components, context (#129)`, OPEN, MERGEABLE.
  Branch: `work/ferric-epic-authoring-r1`, tip `e29e2f4`. Closes: #129, #137–#142.
- **STATE**: `taskflow/overseer/I201/project_state.json` (current_pointer: I201, review-ferric-epic-authoring-r1
  in dags_in_flight, free_dag_slots: 1).
- **Config seam**: `taskflow/overseer/_CONFIG.yaml` (landing_authority: delegated, auto_land: true, headless: true).
- IA6 follow-up: issue #189 filed and on board Todo.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/REVIEW_GATE.md`.

### 2. Check review DAG fold
Check `taskflow/dags/review-ferric-epic-authoring-r1/SYNTHESIS.md`:
- If **present** (folded): read it, apply the verdict, and schedule what it calls for:
  - APPROVE → schedule: process review (file non-blockers on board), then land PR #188 (merge under
    delegated authority), then deployment check, then board check.
  - REQUEST-CHANGES → schedule: process review (sort findings, file non-blockers), then remediation DAG.
- If **absent** (not yet folded): check for other board activity; self-suspend on a bounded wake
  (10 min or DAG fold, whichever first) and schedule I203 for the next check.

### 3. Check board for other activity
While the review runs: check for new GitHub issues, comments, or PRs since I201. If there is nothing
actionable other than the review fold, record that and pass on.

### 4. Update STATE and schedule what follows
- Update `current_pointer` to I202.
- Update `checked_at`.
- Schedule the next task based on what was found.
