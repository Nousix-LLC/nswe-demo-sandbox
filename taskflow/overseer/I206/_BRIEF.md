# _BRIEF.md — NSWE overseer step I206 (persona swe-lead) — EVALUATE: board check / next-goal planning

**Depends on**: I205
**Task Kind**: evaluate — load `WORK_SESSION`, `BOARD`; sweep open issues; decide next goal.

## Context from I205

- PR #188 squash-merged at 2026-11-04T03:26:50Z. Merge commit: `aa2468771eccd9e2ee79c12c79b8943fca18e07a`.
- Issues #129, #137–#142: CLOSED and Done on board.
- main_sha: `aa2468771eccd9e2ee79c12c79b8943fca18e07a`.
- **STATE**: `taskflow/overseer/I205/project_state.json` (current_pointer: I205, free_dag_slots: 2).
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.
- Deployment check (I205): ArgoCD OutOfSync/Healthy — CI on aa24687 in_progress (run 41767186758, image build); auto-sync expected when complete. Endpoint HTTP 200. Non-blocking.
- Board: 173 items total, ~27 open issues. Last board update: 2026-11-04T03:26:50Z.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Read live board state
Check open issues on the GitHub project (Nousix-LLC/nswe-demo). Focus on:
- What is currently Todo / In Progress on the board
- Ferric 1.0 epics: status of #130 (Router), #131 (HTTP), #132 (Forms), #133 (must-have), #134–#136 (one_oh)
- Known follow-up issues: #184 (credential helper polish), #185 (sslmode=require validation), #186 (CLI smoke tests), #189 (IA6 trybuild fixtures), #190 (conditional render test), #191 (macro refactor nits)
- Any issues not yet on the board project (sweep: compare repo issues to board items)

### 3. Assess product gap vs release bar
Per `appfiles/PRODUCT_DESIGN.md` and `appfiles/DEPLOYMENT.md`: the engagement is not done when the board empties; it is done when the product meets the release bar set by the design DAG (BAR-FERRIC-* criteria). Determine:
- What Ferric 1.0 epics remain unimplemented?
- Is a gap review (design DAG) warranted at this stage given what has landed?
- What is the highest-priority next goal?

### 4. Decide next goal and schedule work
Options (in rough priority order):
- Implement next Ferric 1.0 epic (epic #130 Router, #131 HTTP, etc.) — code DAG
- File/schedule IA6 trybuild fixtures fix (issue #189) — code DAG
- Schedule a gap review (design DAG) if enough has landed to warrant it
- Schedule improvement review if the board is thin

Write I207 brief with the decided action and report terminal.

### 5. Write CONTINUE.md and schedule I207
I207: perform the decided next action (fork code DAG, fork design DAG, or other).
Write CONTINUE.md and report terminal.

## Notes
- free_dag_slots: 2 — room to launch a code DAG and potentially a parallel item.
- Deployment auto-sync is non-blocking: do not wait for it before starting next goal.
- The board check governs what comes next; finish it, then act.
