# _BRIEF.md — NSWE overseer step I391 (persona swe-lead) — ACT: stall check 3/4 for r21

**Depends on**: I390

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I390

I390: stall check 2/4 for chirp-logged-out-r21 — head UNCHANGED at `617f25395eebe9475f19a90e0b1dac5921215ea3`, no SYNTHESIS.md. stall_check_count = 2/4 for r21.
- **r21 DAG**: `taskflow/dags/chirp-logged-out-r21/` — only `_BRIEF.md` and `_FORK.md` present at I390 check.
- **Branch HEAD at I390**: `617f25395eebe9475f19a90e0b1dac5921215ea3` (unchanged through I389 and I390).
- **PR #263**: OPEN/MERGEABLE/CLEAN (head `617f2539`).
- **CI run 42183715802**: completed/success (all green) on head `617f2539`.
- **Issue #35**: OPEN/In Progress.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 (benign StatefulSet drift — unchanged since I303).
- **Free DAG slots**: 3 (only chirp-logged-out-r21 in flight).

STATE at: `taskflow/overseer/I390/project_state.json`
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
- Any new issues filed, comments, or reviews since I390?
- Any new PRs or PR status changes?
- Is issue #35 still correctly assigned and In Progress?
- Deployment: ArgoCD still benign StatefulSet drift (unchanged from I303)?

### 4. Evaluate r21 progress

**If SYNTHESIS.md exists**: Read it and act on the verdict:
- PASS → schedule review launch task (load `appfiles/REVIEW_GATE.md`; fork review DAG as swe-reviewer for PR #263).
- FAIL → schedule remediation (fork chirp-logged-out-r22 as swe-coder, carrying blockers from SYNTHESIS.md).

**If no SYNTHESIS.md and head ADVANCED** from `617f2539`: Record new head. stall_check_count = 1/4 against new head. Schedule I392 (+15 min) as stall check 1/4 against new head (reset).

**If no SYNTHESIS.md and head UNCHANGED** at `617f2539`: stall_check_count = 3/4 for r21. Schedule I392 (+15 min) as stall check 4/4.

**If no SYNTHESIS.md and head UNCHANGED** at `617f2539` for 4 consecutive checks (4/4 reached at I392):
Confirm stall, post stall comment on issue #35, fork chirp-logged-out-r22 as swe-coder.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I391/project_state.json`.

### 6. Schedule next step

Schedule the appropriate follow-up based on evaluation.

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r21 DAG path: `taskflow/dags/chirp-logged-out-r21/`.
- stall pattern: r13–r20 all stalled without synthesizing; r13–r17 stalled at 21dca556; r18 advanced to 617f2539 then stalled; r19–r20 stalled at 617f2539. r21 is 2/4 at I390.
- r21 brief carries the full stall history, full acceptance criteria, and explicit SYNTHESIS.md requirement.
- PR #263: OPEN/MERGEABLE/CLEAN on `work/chirp-logged-out`. Head: `617f2539`. CI run 42183715802: completed/success.
