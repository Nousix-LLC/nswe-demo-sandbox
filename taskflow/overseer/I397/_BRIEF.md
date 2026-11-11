# _BRIEF.md — NSWE overseer step I397 (persona swe-lead) — ACT: board check / stall check 1/4 for r23

**Depends on**: I396

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I396

I396: board check / stall check 4/4 for chirp-logged-out-r22. HEAD UNCHANGED at `617f2539`, no SYNTHESIS.md.
**r22 stall confirmed (4/4).** Comment posted to issue #35. chirp-logged-out-r23 dispatched as swe-coder.

- **r22 DAG**: STALLED (4/4 — head unchanged, no SYNTHESIS.md, only `_BRIEF.md` and `_FORK.md` in workspace)
- **r23 DAG**: DISPATCHED in I396 (swe-coder, `taskflow/dags/chirp-logged-out-r23/`).
- **PR #263**: OPEN/MERGEABLE/CLEAN (head `617f2539`). CI run 42183715802: completed/success (all 6 checks green).
- **Issue #35**: OPEN/In Progress/assigned (mattsmcknight). Stall comment posted by I396.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 — benign StatefulSet drift (unchanged since I303).
- **Board hygiene**: issues #254–#262 on board as Todo. No new issues. No new PRs.
- **Free DAG slots**: 3 (only chirp-logged-out-r23 in flight after r22 stall confirmed).

STATE at: `taskflow/overseer/I396/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Read r23 branch HEAD and check for SYNTHESIS.md

Record the current branch HEAD of `work/chirp-logged-out`:
```
gh api repos/Nousix-LLC/nswe-demo/git/refs/heads/work/chirp-logged-out --jq '.object.sha'
```

Check if `taskflow/dags/chirp-logged-out-r23/SYNTHESIS.md` exists.

### 3. Board check

Check the full board state:
- Any new issues filed, comments, or reviews since I396?
- Any new PRs or PR status changes?
- Is issue #35 still correctly assigned and In Progress?
- Deployment: ArgoCD still benign StatefulSet drift?

### 4. Evaluate r23 progress

**stall_check_count starts at 1/4 for r23** (this is the first check after dispatch).

**If SYNTHESIS.md exists**: Read it and act on the verdict:
- PASS → schedule review launch task (load `appfiles/REVIEW_GATE.md`; fork review DAG as swe-reviewer for PR #263).
- FAIL → schedule remediation (fork chirp-logged-out-r24 as swe-coder, carrying blockers from SYNTHESIS.md).

**If no SYNTHESIS.md and head ADVANCED** from `617f2539`: Record new head. stall_check_count = 1/4 against new head. Schedule I398 (+15 min) as stall check 1/4 against new head (reset).

**If no SYNTHESIS.md and head UNCHANGED** at `617f2539`: stall_check_count = 1/4. Schedule I398 (+15 min or r23 completion) as stall check 2/4.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I397/project_state.json`.

### 6. Schedule next step

Schedule the appropriate follow-up based on evaluation (I398).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r23 DAG path: `taskflow/dags/chirp-logged-out-r23/`.
- Full stall history: r13–r21 all stalled without synthesizing; r13–r17 at 21dca556; r18–r22 at 617f2539.
- PR #263: OPEN/MERGEABLE/CLEAN on `work/chirp-logged-out`. Head: `617f2539`. CI run 42183715802: completed/success.
- Issues #254–#262 on board as Todo items (added I392).
