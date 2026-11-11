# _BRIEF.md — NSWE overseer step I406 (persona swe-lead) — ACT: board check / stall check 4/4 for r24

**Depends on**: I405

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I405

I405: board check / stall check 3/4 for r24. Branch `work/chirp-logged-out` HEAD was UNCHANGED at `decb6196c2c1e6ed421d393a642f0c844cc333ba`. No SYNTHESIS.md in `taskflow/dags/chirp-logged-out-r24/` (only `_BRIEF.md` and `_FORK.md` — DAG dispatched I402 but not yet running). stall_check_count for r24 = 3/4 against `decb6196`.

**Key facts from I405**:
- **r24 DAG**: IN FLIGHT (dispatched I402, stall check 3/4 at I405). Workspace: `taskflow/dags/chirp-logged-out-r24/`. No SYNTHESIS.md yet. Only `_BRIEF.md` and `_FORK.md`. Forked thread ID: `proc-4c401512-8481-40f2-b91b-e64c06f05e4e`.
- **PR #263**: OPEN/MERGEABLE (head `decb6196`). CI run 42194072348: ALL 6 PASS (confirmed I400/I402/I403/I404/I405). Ready for review once SYNTHESIS.md appears.
- **Issue #35**: OPEN/In Progress/assigned (mattsmcknight). No new user comments since I402.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 — benign StatefulSet drift (unchanged since I303). Re-confirmed I405.
- **Board hygiene**: issues #254–#262 on board as Todo. No new issues since I402.
- **Free DAG slots**: 3 (only chirp-logged-out-r24 in flight).
- **No new GitHub activity** since I402.

STATE at: `taskflow/overseer/I405/project_state.json`
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
- Any new issues filed, comments, or reviews since I405?
- Any new PRs or PR status changes?
- CI run 42194072348: still ALL 6 PASS? Any re-run triggered?
- Is issue #35 still correctly assigned and In Progress?
- Deployment: ArgoCD still benign StatefulSet drift?

### 4. Evaluate r24 progress

**stall_check_count is now 3/4 against decb6196 for r24** — this is the fourth and final check after r24 was forked in I402.

**If SYNTHESIS.md exists**: Read it and act on the verdict:
- PASS → schedule review launch task (load `appfiles/REVIEW_GATE.md`; fork review DAG as swe-reviewer for PR #263). PR is CLEAN/MERGEABLE/CI-green (all 6 PASS).
- FAIL → schedule remediation (fork chirp-logged-out-r25 as swe-coder, carrying blockers from SYNTHESIS.md).

**If no SYNTHESIS.md and head ADVANCED** from `decb6196`: Record new head. stall_check_count = 1/4 against new head. Schedule I407 (+15 min) as stall check 1/4 against new head.

**If no SYNTHESIS.md and head UNCHANGED** at `decb6196`: This is the **4/4 stall confirmation** for r24.
- Post stall comment on issue #35 announcing r24 stall and r25 dispatch.
- Schedule I407 as a DAG-launch task to re-fork as chirp-logged-out-r25 (load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`; fork swe-coder with brief carrying the full stall history and all prior context).
- Brief for r25 must carry: full stall history (r1–r24, all stalled at 21dca556/617f2539/decb6196), explicit first priority (assess the current state at decb6196, write SYNTHESIS.md), CI ALL 6 PASS on decb6196 (PR #263 CI-green), and all acceptance criteria from issue #35.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I406/project_state.json`.

### 6. Schedule next step

Schedule the appropriate follow-up based on evaluation:
- Stall 4/4: I407 as DAG-launch (re-fork as chirp-logged-out-r25) + stall comment on #35.
- SYNTHESIS.md PASS: I407 as review-launch task.
- SYNTHESIS.md FAIL: I407 as remediation-launch task.
- Head advanced: I407 (+15 min) as stall check 1/4 against new head.

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r24 DAG path: `taskflow/dags/chirp-logged-out-r24/`. Forked thread ID: `proc-4c401512-8481-40f2-b91b-e64c06f05e4e`.
- Full stall history: r13–r23 all stalled without synthesizing; r13–r17 at 21dca556; r18–r22 at 617f2539; r23 advanced to decb6196 but stalled (4/4, I402). r24 dispatched I402. r24 stall check 1/4 at I403 (UNCHANGED at decb6196). r24 stall check 2/4 at I404 (UNCHANGED at decb6196). r24 stall check 3/4 at I405 (UNCHANGED at decb6196).
- PR #263: OPEN/MERGEABLE on `work/chirp-logged-out`. Head: `decb6196c2c1e6ed421d393a642f0c844cc333ba`. CI run 42194072348: ALL 6 PASS (confirmed I400/I402/I403/I404/I405) — PR is CI-green and ready for review once SYNTHESIS.md appears.
- Issues #254–#262 on board as Todo items (added I392).
- If 4/4 stall confirmed: post comment on https://github.com/Nousix-LLC/nswe-demo/issues/35 and re-fork as chirp-logged-out-r25.
