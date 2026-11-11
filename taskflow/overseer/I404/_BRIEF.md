# _BRIEF.md — NSWE overseer step I404 (persona swe-lead) — ACT: board check / stall check 2/4 for r24

**Depends on**: I403

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I403

I403: board check / stall check 1/4 for r24. Branch `work/chirp-logged-out` HEAD was UNCHANGED at `decb6196c2c1e6ed421d393a642f0c844cc333ba`. No SYNTHESIS.md in `taskflow/dags/chirp-logged-out-r24/` (only `_BRIEF.md` and `_FORK.md` — DAG dispatched I402 but not yet running). stall_check_count for r24 = 1/4 against `decb6196`.

**Key facts from I403**:
- **r24 DAG**: IN FLIGHT (dispatched I402, stall check 1/4 at I403). Workspace: `taskflow/dags/chirp-logged-out-r24/`. No SYNTHESIS.md yet. Only `_BRIEF.md` and `_FORK.md`.
- **PR #263**: OPEN/MERGEABLE (head `decb6196`). CI run 42194072348: ALL 6 PASS (confirmed I403). Ready for review once SYNTHESIS.md appears.
- **Issue #35**: OPEN/In Progress/assigned (mattsmcknight). No new user comments.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 — benign StatefulSet drift (unchanged since I303).
- **Board hygiene**: issues #254–#262 on board as Todo. No new issues since I402.
- **Free DAG slots**: 3 (only chirp-logged-out-r24 in flight).
- **No new GitHub activity** since I402.

STATE at: `taskflow/overseer/I403/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Read r24 branch HEAD and check for SYNTHESIS.md

Record the current branch HEAD of `work/chirp-logged-out`:
```
gh api repos/Nousix-LLC/nswe-demo/git/refs/heads/work/chirp-logged-out --jq '.object.sha'
```

Check if `taskflow/dags/chirp-logged-out-r24/SYNTHESIS.md` exists.

### 3. Board check

Check the full board state:
- Any new issues filed, comments, or reviews since I403?
- Any new PRs or PR status changes?
- CI run 42194072348: still ALL 6 PASS? Any re-run triggered?
- Is issue #35 still correctly assigned and In Progress?
- Deployment: ArgoCD still benign StatefulSet drift?

### 4. Evaluate r24 progress

**stall_check_count is now 1/4 against decb6196 for r24** — this is the second check after r24 was forked in I402.

**If SYNTHESIS.md exists**: Read it and act on the verdict:
- PASS → schedule review launch task (load `appfiles/REVIEW_GATE.md`; fork review DAG as swe-reviewer for PR #263). PR is CLEAN/MERGEABLE/CI-green (all 6 PASS).
- FAIL → schedule remediation (fork chirp-logged-out-r25 as swe-coder, carrying blockers from SYNTHESIS.md).

**If no SYNTHESIS.md and head ADVANCED** from `decb6196`: Record new head. stall_check_count = 1/4 against new head. Schedule I405 (+15 min) as stall check 1/4 against new head.

**If no SYNTHESIS.md and head UNCHANGED** at `decb6196`: stall_check_count = 2/4 against `decb6196` for r24. Schedule I405 (+15 min) as stall check 3/4.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I404/project_state.json`.

### 6. Schedule next step

Schedule the appropriate follow-up based on evaluation (I405 for another stall check, or review/remediation launch).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r24 DAG path: `taskflow/dags/chirp-logged-out-r24/`.
- Full stall history: r13–r23 all stalled without synthesizing; r13–r17 at 21dca556; r18–r22 at 617f2539; r23 advanced to decb6196 but stalled (4/4, I402). r24 dispatched I402. r24 stall check 1/4 at I403 (head UNCHANGED at decb6196, no SYNTHESIS.md).
- PR #263: OPEN/MERGEABLE on `work/chirp-logged-out`. Head: `decb6196c2c1e6ed421d393a642f0c844cc333ba`. CI run 42194072348: ALL 6 PASS (confirmed I403) — PR is CI-green and ready for review once SYNTHESIS.md appears.
- Issues #254–#262 on board as Todo items (added I392).
