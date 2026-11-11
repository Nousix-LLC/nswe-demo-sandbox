# _BRIEF.md — NSWE overseer step I389 (persona swe-lead) — ACT: board check after r21 dispatch

**Depends on**: I388

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I388

I388: stall check 4/4 for chirp-logged-out-r20 — head UNCHANGED at `617f25395eebe9475f19a90e0b1dac5921215ea3`, no SYNTHESIS.md. r20 CONFIRMED STALLED (4/4).
- **Action taken**: Stall comment posted on issue #35. chirp-logged-out-r21 forked as swe-coder. I389 scheduled as board check (+15 min).
- **r21 DAG**: `taskflow/dags/chirp-logged-out-r21/` (dispatched I388).
- **Branch HEAD at I388**: `617f25395eebe9475f19a90e0b1dac5921215ea3` (unchanged through r20's 4/4 stall checks).
- **PR #263**: OPEN/MERGEABLE/CLEAN (head `617f2539`).
- **CI run 42183715802**: completed/success (all green) on head `617f2539`.
- **Issue #35**: OPEN/In Progress.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 (benign StatefulSet drift — unchanged since I303).

STATE at: `taskflow/overseer/I388/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Read r21 branch HEAD and check for SYNTHESIS.md

Record the current branch HEAD of `work/chirp-logged-out`:
```
gh api repos/Nousix-LLC/nswe-demo/git/refs/heads/work/chirp-logged-out --jq '.object.sha'
```

Check if `taskflow/dags/chirp-logged-out-r21/SYNTHESIS.md` exists.

### 3. Board check

Check the full board state:
- Any new issues filed, comments, or reviews since I388?
- Any new PRs or PR status changes?
- Any other DAGs in flight that have folded?
- Is issue #35 still correctly assigned and In Progress?
- Deployment: ArgoCD still benign StatefulSet drift (unchanged from I303)?

### 4. Evaluate r21 progress

**If SYNTHESIS.md exists**: Read it and act on the verdict:
- PASS → schedule review launch task (load `appfiles/REVIEW_GATE.md`; fork review DAG as swe-reviewer for PR #263).
- FAIL → schedule remediation (fork chirp-logged-out-r22 as swe-coder, carrying blockers from SYNTHESIS.md).

**If no SYNTHESIS.md and head ADVANCED** from `617f2539`: Record new head. stall_check_count = 1/4 against new head. Schedule I390 (+15 min) as stall check 1/4 against new head.

**If no SYNTHESIS.md and head UNCHANGED** at `617f2539`: stall_check_count = 1/4 for r21. Schedule I390 (+15 min) as stall check 2/4.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I389/project_state.json`.

### 6. Schedule next step

Schedule the appropriate follow-up based on evaluation.

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r21 DAG path: `taskflow/dags/chirp-logged-out-r21/`.
- stall pattern: r13–r20 all stalled without synthesizing; r13–r17 stalled at 21dca556; r18 advanced to 617f2539 then stalled; r19–r20 stalled at 617f2539.
- r21 brief carries the full stall history, full acceptance criteria, and explicit SYNTHESIS.md requirement.
- PR #263: OPEN/MERGEABLE/CLEAN on `work/chirp-logged-out`. Head: `617f2539`. CI run 42183715802: completed/success.
