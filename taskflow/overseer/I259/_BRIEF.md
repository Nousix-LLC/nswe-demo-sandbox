# _BRIEF.md — NSWE overseer step I259 (persona swe-lead) — ACT: tidy board

**Depends on**: I258
**Task Kind**: act — load `appfiles/BOARD.md`, `appfiles/DELIVERABLES_GIT.md`.

## Context from I258 (board check)

- ferric-ssr-r2: RUNNING (no SYNTHESIS.md); 1 DAG in flight (3 slots free)
- ferric-async-forms escalation: ACTIVE (no user response); PR #193 open with 3 blockers
  - Last activity on PR #193: 2026-11-04T06:38:30Z (escalation comment)
- Board hygiene issue confirmed: issues #130, #143, #144 are CLOSED (GitHub) and Done (board) but PR #193
  is still OPEN with blockers — these were closed 2026-11-04T05:43:07–12Z before the escalation was filed.
  "Done means merged" per BOARD.md. These must be re-opened and set to Blocked.
- Main SHA: 945fade38abd6b053268501f3801734756f02502 (unchanged, no recheck needed)
- STATE at: `taskflow/overseer/I256/project_state.json`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DELIVERABLES_GIT.md`.

### 2. Read the config seam

Read `taskflow/overseer/_CONFIG.yaml`.

### 3. Fix board state for issues #130, #143, #144

These issues are CLOSED on GitHub and Done on the board. PR #193 has NOT merged — it is OPEN with 3
review blockers. The escalation is ACTIVE waiting for the user's decision (extend budget or defer epic).
Per BOARD.md: "Done means merged." These should not be Done.

Correct state:
- Re-open GitHub issues #130, #143, #144 (`gh issue reopen`)
- Set their board status to **Blocked** (the escalation on PR #193 names what is waiting):
  - Project item IDs (from _CONFIG.yaml):
    - issue_130: `PVTI_lADOEB9jls4BlZH4zhFl_I0`
    - issue_143: `PVTI_lADOEB9jls4BlZH4zhFl_h4`
    - issue_144: `PVTI_lADOEB9jls4BlZH4zhFl_jk`
  - Status field ID: `PVTSSF_lADOEB9jls4BlZH4zhkGLsc`
  - Project ID: `PVT_kwDOEB9jls4BlZH4`
  - Note: The board only has Todo / In Progress / Done status options in `_CONFIG.yaml`. Use "Todo"
    if Blocked is not an available option — check the actual board status options first with
    `gh project field-list` before setting. If a Blocked option exists, use it; otherwise use Todo
    (backlog), which correctly signals "not done, awaiting decision."

Also check issue #145 (Ferric 1.0: Forms and two-way binding) — the escalation comment mentions it as
one of the issues that would move to backlog under deferral, but it was also closed 2026-11-04T05:43:12Z.
Check its GitHub state and board status; if closed/Done, re-open and set Todo (it may have been
legitimately addressed in PR #193's merged portions — verify before reopening).

### 4. Write CONTINUE.md

Document actions taken (what was re-opened, what board status was set), and confirm the hygiene fix.

## Notes

- Tidy the board only for the confirmed hygiene issue. Do not make other board changes in this step.
- The user has not yet responded to the escalation on PR #193; do not interpret the status change as a
  decision — it is a correction to the board's factual state.
- After this step: I260 board check → suspend on bounded wake (ferric-ssr-r2 fold OR 10 minutes).
