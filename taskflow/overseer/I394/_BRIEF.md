# _BRIEF.md — NSWE overseer step I394 (persona swe-lead) — ACT: board check / stall check 2/4 for r22

**Depends on**: I393

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I393

I393: board check after r22 dispatch — stall check 1/4 for chirp-logged-out-r22. HEAD UNCHANGED at `617f25395eebe9475f19a90e0b1dac5921215ea3`, no SYNTHESIS.md at I393 check.
- **r22 DAG**: stall_check_count = 1/4 (HEAD UNCHANGED at `617f2539`, no SYNTHESIS.md, only `_BRIEF.md` and `_FORK.md` in workspace).
- **PR #263**: OPEN/MERGEABLE/CLEAN (head `617f2539`). CI run 42183715802: completed/success (all 6 checks green).
- **Issue #35**: OPEN/In Progress/assigned (mattsmcknight). No new user comments since I392.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 — benign StatefulSet drift (unchanged since I303).
- **Board hygiene**: issues #254–#262 on board as Todo (confirmed I392). No new issues, no new PRs.
- **Free DAG slots**: 3 (only chirp-logged-out-r22 in flight).

STATE at: `taskflow/overseer/I393/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Read r22 branch HEAD and check for SYNTHESIS.md

Record the current branch HEAD of `work/chirp-logged-out`:
```
gh api repos/Nousix-LLC/nswe-demo/git/refs/heads/work/chirp-logged-out --jq '.object.sha'
```

Check if `taskflow/dags/chirp-logged-out-r22/SYNTHESIS.md` exists.

### 3. Board check

Check the full board state:
- Any new issues filed, comments, or reviews since I393?
- Any new PRs or PR status changes?
- Is issue #35 still correctly assigned and In Progress?
- Deployment: ArgoCD still benign StatefulSet drift?

### 4. Evaluate r22 progress

**stall_check_count starts at 2/4 for r22** (this is second check after dispatch).

**If SYNTHESIS.md exists**: Read it and act on the verdict:
- PASS → schedule review launch task (load `appfiles/REVIEW_GATE.md`; fork review DAG as swe-reviewer for PR #263).
- FAIL → schedule remediation (fork chirp-logged-out-r23 as swe-coder, carrying blockers from SYNTHESIS.md).

**If no SYNTHESIS.md and head ADVANCED** from `617f2539`: Record new head. stall_check_count = 1/4 against new head. Schedule I395 (+15 min) as stall check 1/4 against new head (reset).

**If no SYNTHESIS.md and head UNCHANGED** at `617f2539`: stall_check_count = 2/4 for r22. Schedule I395 (+15 min) as stall check 3/4.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I394/project_state.json`.

### 6. Schedule next step

Schedule the appropriate follow-up based on evaluation (I395).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r22 DAG path: `taskflow/dags/chirp-logged-out-r22/`.
- stall pattern: r13–r21 all stalled without synthesizing; r13–r17 stalled at 21dca556; r18 advanced to 617f2539 then stalled; r19–r21 stalled at 617f2539. r22 dispatched I392 — 1/4 at I393 (head unchanged).
- r22 brief carries the full stall history (r13–r21), full acceptance criteria, and explicit SYNTHESIS.md requirement.
- PR #263: OPEN/MERGEABLE/CLEAN on `work/chirp-logged-out`. Head: `617f2539`. CI run 42183715802: completed/success.
- Issues #254–#262 on board as Todo items (added I392).
