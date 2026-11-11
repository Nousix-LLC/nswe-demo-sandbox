# _BRIEF.md — NSWE overseer step I388 (persona swe-lead) — ACT: watch chirp-logged-out-r20 (stall check 4/4)

**Depends on**: I387

**Task Kind**: act — load `appfiles/WORK_SESSION.md`.

## Context from I387

I387: stall check 3/4 for chirp-logged-out-r20 — head UNCHANGED at `617f2539`, no SYNTHESIS.md. r20 stall check 3/4 recorded.
- **Action taken**: I388 scheduled (+15 min from I387) as stall check 4/4.
- **r20 DAG**: `taskflow/dags/chirp-logged-out-r20/` (dispatched I384).
- **Branch HEAD at I387**: `617f25395eebe9475f19a90e0b1dac5921215ea3` (unchanged through 3/4 stall checks).
- **PR #263**: OPEN/MERGEABLE/CLEAN (head `617f2539`).
- **CI run 42183715802**: completed/success (all green) on head `617f2539`.
- **Issue #35**: OPEN/In Progress.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 (benign StatefulSet drift — unchanged since I303).

STATE at: `taskflow/overseer/I387/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md`.

### 2. Read r20 branch HEAD and check for SYNTHESIS.md

Record the current branch HEAD of `work/chirp-logged-out`:
```
gh api repos/Nousix-LLC/nswe-demo/git/refs/heads/work/chirp-logged-out --jq '.object.sha'
```

Check if `taskflow/dags/chirp-logged-out-r20/SYNTHESIS.md` exists.

### 3. Evaluate

**If SYNTHESIS.md exists**: Read it and act on the verdict:
- PASS → schedule review launch task (load `appfiles/REVIEW_GATE.md`; fork review DAG as swe-reviewer for PR #263).
- FAIL → schedule remediation (fork chirp-logged-out-r21 as swe-coder, carrying blockers from SYNTHESIS.md).

**If no SYNTHESIS.md and head ADVANCED** from `617f2539`: Record new head. stall_check_count = 1/4 against new head. Schedule I389 (+15 min) as stall check 1/4 against new head.

**If no SYNTHESIS.md and head UNCHANGED** at `617f2539`: stall_check_count = 4/4 — **r20 CONFIRMED STALLED**.
- Post stall comment on issue #35 (GitHub).
- Fork chirp-logged-out-r21 as swe-coder with brief carrying: prior diff/head, the stall history (r13–r20 all stalled without synthesizing), and the original acceptance criteria from issue #35.
- Record r20 as STALLED in STATE.
- Schedule I389 as board check (+15 min) after r21 is dispatched.

### 4. Update STATE

Write updated STATE at `taskflow/overseer/I388/project_state.json`:
- Record current branch HEAD.
- If SYNTHESIS.md exists: record verdict and next step.
- If no SYNTHESIS.md and head UNCHANGED (4/4 stall confirmed): record r20 as STALLED, record r21 dispatch, record stall comment.
- If no SYNTHESIS.md and head advanced: record stall_check_count = 1/4, record head, schedule I389.

### 5. Schedule next step

If SYNTHESIS.md found: schedule the appropriate follow-up (review launch or remediation DAG dispatch).
If stall confirmed (4/4): fork r21, post stall comment, schedule I389 as board check (+15 min).
If head advanced: schedule I389 as stall check 1/4 against new head (+15 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r20 DAG path: `taskflow/dags/chirp-logged-out-r20/`. Process id: chirp-logged-out-r20.
- Prior stalls: r1–r19 all stalled. r19 stall comment: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6680541037
- stall_check_count so far: 3/4 (r20 stall check 1/4 at I385: head UNCHANGED; r20 stall check 2/4 at I386: head UNCHANGED, no SYNTHESIS.md; r20 stall check 3/4 at I387: head UNCHANGED, no SYNTHESIS.md).
- If 4/4 stall confirmed at I388: post stall comment on issue #35, fork r21 as swe-coder.
- r21 brief should include: the stall pattern (r13–r20 all stall without synthesizing on 617f2539), the full issue #35 acceptance criteria, CI is green (42183715802), PR #263 is CLEAN/MERGEABLE, explicit requirement to write root SYNTHESIS.md at `taskflow/dags/chirp-logged-out-r21/SYNTHESIS.md`.
- PR #263: OPEN/MERGEABLE/CLEAN on `work/chirp-logged-out`. Head: `617f2539`. CI run 42183715802: completed/success.
