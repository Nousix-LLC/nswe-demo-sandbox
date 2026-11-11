# _BRIEF.md — NSWE overseer step I392 (persona swe-lead) — ACT: stall check 4/4 for r21

**Depends on**: I391

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I391

I391: stall check 3/4 for chirp-logged-out-r21 — head UNCHANGED at `617f25395eebe9475f19a90e0b1dac5921215ea3`, no SYNTHESIS.md. stall_check_count = 3/4 for r21.
- **r21 DAG**: `taskflow/dags/chirp-logged-out-r21/` — only `_BRIEF.md` and `_FORK.md` present at I391 check.
- **Branch HEAD at I391**: `617f25395eebe9475f19a90e0b1dac5921215ea3` (unchanged through I389, I390, I391).
- **PR #263**: OPEN/MERGEABLE/CLEAN (head `617f2539`).
- **CI run 42183715802**: completed/success (all green) on head `617f2539`.
- **Issue #35**: OPEN/In Progress/assigned (mattsmcknight).
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 (benign StatefulSet drift — unchanged since I303).
- **Free DAG slots**: 3 (only chirp-logged-out-r21 in flight).
- **Board hygiene note**: issues #254–#262 (ferric non-blockers filed ~03:02Z) exist in repo but not yet tracked as project board items — add in this or next full board check.

STATE at: `taskflow/overseer/I391/project_state.json`
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
- Any new issues filed, comments, or reviews since I391?
- Any new PRs or PR status changes?
- Is issue #35 still correctly assigned and In Progress?
- Deployment: ArgoCD still benign StatefulSet drift (unchanged from I303)?
- Board hygiene: add issues #254–#262 (open ferric non-blockers not yet on project board) as project items with appropriate status/labels/epic grouping.

### 4. Evaluate r21 progress — THIS IS CHECK 4/4 (THE FINAL CHECK)

**If SYNTHESIS.md exists**: Read it and act on the verdict:
- PASS → schedule review launch task (load `appfiles/REVIEW_GATE.md`; fork review DAG as swe-reviewer for PR #263).
- FAIL → schedule remediation (fork chirp-logged-out-r22 as swe-coder, carrying blockers from SYNTHESIS.md).

**If no SYNTHESIS.md and head ADVANCED** from `617f2539`: Record new head. stall_check_count = 1/4 against new head. Schedule I393 (+15 min) as stall check 1/4 against new head (reset).

**If no SYNTHESIS.md and head UNCHANGED** at `617f2539` for 4 consecutive checks (4/4 reached):
**Confirm stall for r21.** Take the following actions:
1. Post a stall comment on issue #35 (similar to previous stall comments at the URLs in STATE).
2. Fork chirp-logged-out-r22 as swe-coder. Write `taskflow/dags/chirp-logged-out-r22/_BRIEF.md` with:
   - Full stall history: r13–r21 all stalled without synthesizing; r13–r17 at 21dca556; r18 advanced to 617f2539 then stalled; r19–r21 stalled at 617f2539.
   - Current branch HEAD: `617f25395eebe9475f19a90e0b1dac5921215ea3` (PR #263 open, CI green, MERGEABLE/CLEAN).
   - Full acceptance criteria from issue #35.
   - Explicit requirement: produce a root `SYNTHESIS.md` at `taskflow/dags/chirp-logged-out-r22/SYNTHESIS.md`.
   - Explicit requirement: do NOT stall without synthesizing; if work is complete, write SYNTHESIS.md and mark PASS or FAIL.
3. Schedule I393 as a board check (+15 min or forked-thread-completion for r22).

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I392/project_state.json`.

### 6. Schedule next step

Schedule the appropriate follow-up based on evaluation:
- If SYNTHESIS.md found: schedule review launch or remediation task.
- If head advanced (new stall cycle): schedule I393 as stall check 1/4 (+15 min).
- If stall confirmed (4/4 at 617f2539): fork r22 and schedule I393 as board check (+15 min or fork completion).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r21 DAG path: `taskflow/dags/chirp-logged-out-r21/`.
- stall pattern: r13–r20 all stalled without synthesizing; r13–r17 stalled at 21dca556; r18 advanced to 617f2539 then stalled; r19–r21 stalled at 617f2539. r21 is 3/4 at I391.
- r21 brief carries the full stall history, full acceptance criteria, and explicit SYNTHESIS.md requirement.
- PR #263: OPEN/MERGEABLE/CLEAN on `work/chirp-logged-out`. Head: `617f2539`. CI run 42183715802: completed/success.
- If stall confirmed at 4/4: post stall comment + fork r22 immediately. Do not wait further.
- Board hygiene: issues #254–#262 need project board items. These are ferric framework non-blockers from review-ferric-async-forms-r3 (filed ~03:02Z, not yet added as project items). Add them with Todo status under the ferric non-blockers epic/group.
