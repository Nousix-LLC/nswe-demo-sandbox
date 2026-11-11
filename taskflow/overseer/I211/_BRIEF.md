# _BRIEF.md — NSWE overseer step I211 (persona swe-lead) — EVALUATE: board check / watch folds

**Depends on**: I210
**Task Kind**: evaluate — load `WORK_SESSION`, `BOARD`. Board check: watch for ferric-async-forms-r2 and ferric-router-r1 folds; check board hygiene and GitHub activity.

## Context from I210

- ferric-async-forms-r2 launched (remediation attempt 2 of 2, forked as `ferric-async-forms-r2`).
  Brief at `taskflow/dags/ferric-async-forms-r2/_BRIEF.md`. Board: #130/#143/#144/#145 remain In Progress.
  Lesson carried: wrong repo + no CI from r1; this DAG must deliver branch + PR in Nousix-LLC/nswe-demo with all 6 CI PASS.
- ferric-router-r1 still RUNNING. No fold confirmed yet.
- free_dag_slots: 2 (ferric-router-r1 + ferric-async-forms-r2).
- STATE: `taskflow/overseer/I210/project_state.json`.
- Config seam: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`. Read `_CONFIG.yaml` and
`taskflow/overseer/I210/project_state.json`.

### 2. Board check

Check the live GitHub state:

1. **DAG folds**: Check if either `ferric-async-forms-r2` or `ferric-router-r1` has folded:
   - `taskflow/dags/ferric-async-forms-r2/SYNTHESIS.md` — present → folded (read verdict, schedule fold-read)
   - `taskflow/dags/ferric-router-r1/SYNTHESIS.md` — present → folded (read verdict, schedule fold-read)
   
2. **GitHub activity**: New or changed issues, comments, PRs, or reviews since I210.

3. **Board hygiene**: Any items that have drifted off the board, any open PRs without board links,
   any review findings that never reached the board.

4. **Backlog**: Whether any new goals are ready (blocked on ferric-router landing for some epics).
   free_dag_slots=2, so at most 0 more launches until a slot frees.

### 3. Decide and schedule

If a DAG has folded, schedule a fold-read task. If neither has folded and nothing else needs the
thread, suspend on the bounded wake (DAG-fold-or-timer, 5–10 min floor) until one folds or the
next routine check is due.

## Notes

- ferric-async-forms-r2 is remediation attempt 2 of 2 (the final attempt). If it also fails
  machine gate, escalate to the user with both attempts' findings.
- I212 follows (the fold-read or the next board check, as decided here).
