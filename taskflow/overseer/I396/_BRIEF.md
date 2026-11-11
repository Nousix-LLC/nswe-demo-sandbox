# _BRIEF.md — NSWE overseer step I396 (persona swe-lead) — ACT: board check / stall check 4/4 for r22

**Depends on**: I395

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I395

I395: board check / stall check 3/4 for chirp-logged-out-r22. HEAD UNCHANGED at `617f25395eebe9475f19a90e0b1dac5921215ea3`, no SYNTHESIS.md at I395 check.
- **r22 DAG**: stall_check_count = 3/4 (HEAD UNCHANGED at `617f2539`, no SYNTHESIS.md, only `_BRIEF.md` and `_FORK.md` in workspace — no child tasks started).
- **PR #263**: OPEN/MERGEABLE/CLEAN (head `617f2539`). CI run 42183715802: completed/success (all 6 checks green: fmt, clippy, test, wasm, doc, image).
- **Issue #35**: OPEN/In Progress/assigned (mattsmcknight). No new user comments since I392.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 — benign StatefulSet drift (unchanged since I303).
- **Board hygiene**: issues #254–#262 on board as Todo (confirmed I392). No new issues since I394, no new PRs.
- **Free DAG slots**: 3 (only chirp-logged-out-r22 in flight).

STATE at: `taskflow/overseer/I395/project_state.json`
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
- Any new issues filed, comments, or reviews since I395?
- Any new PRs or PR status changes?
- Is issue #35 still correctly assigned and In Progress?
- Deployment: ArgoCD still benign StatefulSet drift?

### 4. Evaluate r22 progress

**stall_check_count starts at 4/4 for r22** (this is the fourth and final check after dispatch).

**If SYNTHESIS.md exists**: Read it and act on the verdict:
- PASS → schedule review launch task (load `appfiles/REVIEW_GATE.md`; fork review DAG as swe-reviewer for PR #263).
- FAIL → schedule remediation (fork chirp-logged-out-r23 as swe-coder, carrying blockers from SYNTHESIS.md).

**If no SYNTHESIS.md and head ADVANCED** from `617f2539`: Record new head. stall_check_count = 1/4 against new head. Schedule I397 (+15 min) as stall check 1/4 against new head (reset).

**If no SYNTHESIS.md and head UNCHANGED** at `617f2539`: **stall confirmed (4/4)**. r22 is stalled.
- Post a comment to issue #35 announcing the r22 stall and r23 dispatch (summarizing the stall evidence: 4 checks, head unchanged at 617f2539, no SYNTHESIS.md).
- Fork chirp-logged-out-r23 as swe-coder. The r23 brief must carry:
  - Full stall history (r13–r22 all stalled at or after `21dca556`; r13–r17 at `21dca556`; r18–r22 at `617f2539`)
  - Full acceptance criteria for issue #35 (AC-1 through AC-5)
  - Current branch state: head `617f2539`, CI run 42183715802 (all 6 checks green)
  - PR #263: OPEN/MERGEABLE/CLEAN
  - Explicit SYNTHESIS.md requirement as declared mandatory output
  - Constraint: do NOT force-push `work/chirp-logged-out`
- Schedule I397 (+15 min or r23 completion) as stall check 1/4 for r23.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I396/project_state.json`.

### 6. Schedule next step

Schedule the appropriate follow-up based on evaluation (I397).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r22 DAG path: `taskflow/dags/chirp-logged-out-r22/`.
- stall pattern: r13–r21 all stalled without synthesizing; r13–r17 stalled at 21dca556; r18 advanced to 617f2539 then stalled; r19–r22 stalled at 617f2539.
- PR #263: OPEN/MERGEABLE/CLEAN on `work/chirp-logged-out`. Head: `617f2539`. CI run 42183715802: completed/success.
- Issues #254–#262 on board as Todo items (added I392).
