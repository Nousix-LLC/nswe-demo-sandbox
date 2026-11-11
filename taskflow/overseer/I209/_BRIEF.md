# _BRIEF.md — NSWE overseer step I209 (persona swe-lead) — EVALUATE: board check / watch DAG folds

**Depends on**: I208
**Task Kind**: evaluate — load `WORK_SESSION`, `BOARD`.

## Context from I208

- ferric-router-r1 DAG forked (epic #131, issues #131/#146/#147). Board: #131/#146/#147 moved to In Progress, all assigned to mattsmcknight.
- 2 free DAG slots (was 3, used 1 for ferric-router-r1).
- Two DAGs in flight: ferric-async-forms-r1 (epic #130) and ferric-router-r1 (epic #131).
- **STATE**: `taskflow/overseer/I208/project_state.json` (updated by I208).
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Board check / watch DAG folds

Check the board and both DAGs in flight:
- `ferric-async-forms-r1`: check if `taskflow/dags/ferric-async-forms-r1/SYNTHESIS.md` exists (fold complete).
- `ferric-router-r1`: check if `taskflow/dags/ferric-router-r1/SYNTHESIS.md` exists (fold complete).

For any folded DAG: read its `SYNTHESIS.md` verdict and schedule the appropriate follow-up
(machine-gate read → review launch if PASS; remediation if FAIL).

### 3. Decide and schedule

Based on what the board check finds, follow the WORK_SESSION priority order:
1. Any cleared escalations — resolve them.
2. Any folded machine-PASS DAG with no review yet — schedule review launch.
3. Any review not yet processed — schedule processing.
4. Any machine FAIL — schedule remediation.
5. If no DAG has folded: suspend on bounded wake (DAG fold OR 10 minutes, whichever first).

## Notes

- Both code DAGs are running in parallel on non-overlapping crates (ferric vs. ferric-router). No
  conflict expected. Watch for either folding first.
- If board has new issues (non-blockers from prior reviews, etc.) and time permits, groom lightly.
- 2 free DAG slots available for reviews or remediations once one of the code DAGs folds.
- main_sha: aa2468771eccd9e2ee79c12c79b8943fca18e07a (unchanged since I204 land).
