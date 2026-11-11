# _BRIEF.md — NSWE overseer step I393 (persona swe-lead) — ACT: board check after r22 dispatch

**Depends on**: I392

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I392

I392: stall check 4/4 for chirp-logged-out-r21 — STALL CONFIRMED. Head UNCHANGED at `617f25395eebe9475f19a90e0b1dac5921215ea3`, no SYNTHESIS.md at I392 check.
- **r21 DAG**: confirmed STALLED (4/4).
- **r22 DAG**: forked in I392 as `chirp-logged-out-r22` (swe-coder). Workspace: `taskflow/dags/chirp-logged-out-r22/`.
- **Stall comment**: posted on issue #35 at I392 (https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6680995793).
- **Branch HEAD**: `617f25395eebe9475f19a90e0b1dac5921215ea3` (unchanged through r18–r21).
- **PR #263**: OPEN/MERGEABLE/CLEAN (head `617f2539`).
- **CI run 42183715802**: completed/success (all green) on head `617f2539`.
- **Issue #35**: OPEN/In Progress/assigned (mattsmcknight).
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 (benign StatefulSet drift — unchanged since I303).
- **Free DAG slots**: 3 (only chirp-logged-out-r22 in flight after r21 confirmed stalled).
- **Board hygiene**: issues #254–#262 (ferric non-blockers from review-ferric-async-forms-r3) added to project board as Todo items in I392.

STATE at: `taskflow/overseer/I392/project_state.json`
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
- Any new issues filed, comments, or reviews since I392?
- Any new PRs or PR status changes?
- Is issue #35 still correctly assigned and In Progress?
- Deployment: ArgoCD still benign StatefulSet drift?
- Board hygiene: confirm issues #254–#262 are on board (added in I392).

### 4. Evaluate r22 progress

**stall_check_count starts at 1/4 for r22** (this is first check after dispatch).

**If SYNTHESIS.md exists**: Read it and act on the verdict:
- PASS → schedule review launch task (load `appfiles/REVIEW_GATE.md`; fork review DAG as swe-reviewer for PR #263).
- FAIL → schedule remediation (fork chirp-logged-out-r23 as swe-coder, carrying blockers from SYNTHESIS.md).

**If no SYNTHESIS.md and head ADVANCED** from `617f2539`: Record new head. stall_check_count = 1/4 against new head. Schedule I394 (+15 min) as stall check 1/4 against new head (reset).

**If no SYNTHESIS.md and head UNCHANGED** at `617f2539`: stall_check_count = 1/4 for r22. Schedule I394 (+15 min) as stall check 2/4.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I393/project_state.json`.

### 6. Schedule next step

Schedule the appropriate follow-up based on evaluation (I394).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r22 DAG path: `taskflow/dags/chirp-logged-out-r22/`.
- stall pattern: r13–r21 all stalled without synthesizing; r13–r17 stalled at 21dca556; r18 advanced to 617f2539 then stalled; r19–r21 stalled at 617f2539.
- r22 brief carries the full stall history (r13–r21), full acceptance criteria, and explicit SYNTHESIS.md requirement.
- PR #263: OPEN/MERGEABLE/CLEAN on `work/chirp-logged-out`. Head: `617f2539`. CI run 42183715802: completed/success.
- Issues #254–#262 added to board as Todo items in I392.
