# _BRIEF.md — NSWE overseer step I384 (persona swe-lead) — ACT: watch chirp-logged-out-r19 (stall check 4/4)

**Depends on**: I383

**Task Kind**: act — load `appfiles/WORK_SESSION.md`.

## Context from I383

I383: stall check 3/4 for chirp-logged-out-r19 — head UNCHANGED at `617f2539`, no SYNTHESIS.md.
- **r19 DAG**: `taskflow/dags/chirp-logged-out-r19/` (dispatched I380).
- **Branch HEAD at I383**: `617f25395eebe9475f19a90e0b1dac5921215ea3` (unchanged from dispatch).
- **PR #263**: OPEN/MERGEABLE/CLEAN (head `617f2539`).
- **CI run 42183715802**: completed/success (all green) on head `617f2539`.
- **Issue #35**: OPEN/In Progress.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 (benign StatefulSet drift — unchanged since I303).
- **Stall check 3/4 verdict**: No SYNTHESIS.md, head unchanged. stall_check_count = 3/4.

STATE at: `taskflow/overseer/I383/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md`.

### 2. Read r19 branch HEAD and check for SYNTHESIS.md

Record the current branch HEAD of `work/chirp-logged-out`:
```
gh api repos/Nousix-LLC/nswe-demo/git/refs/heads/work/chirp-logged-out --jq '.object.sha'
```

Check if `taskflow/dags/chirp-logged-out-r19/SYNTHESIS.md` exists.

### 3. Evaluate

**If SYNTHESIS.md exists**: Read it and act on the verdict:
- PASS → schedule review launch task (load `appfiles/REVIEW_GATE.md`; fork review DAG as swe-reviewer for PR #263).
- FAIL → schedule remediation (fork chirp-logged-out-r20 as swe-coder, carrying blockers from SYNTHESIS.md).

**If no SYNTHESIS.md and head ADVANCED** from `617f2539`: Record new head. stall_check_count = 4/4 against new head. This resets the cycle — treat as a fresh dispatch, schedule I385 (+15 min) as stall check 1/4 against the new head.

**If no SYNTHESIS.md and head UNCHANGED** at `617f2539`: This is 4/4 — r19 is confirmed stalled. Take stall action:
1. Confirm r19 stalled: move slug from `dags_in_flight` to `dags_stalled` in STATE.
2. Post stall comment on issue #35 (the 19th stall comment, format per prior stall comments on https://github.com/Nousix-LLC/nswe-demo/issues/35).
3. Fork chirp-logged-out-r20 as swe-coder with brief at `taskflow/dags/chirp-logged-out-r20/_BRIEF.md`. The brief carries:
   - Current branch HEAD `617f2539` and what it contains (the r10–r18 work: backend APIs, frontend routes, sign-up form AC-4).
   - The fact that r13–r19 all stalled without producing SYNTHESIS.md — the DAG must produce a SYNTHESIS.md as its declared output.
   - PR #263 is open, MERGEABLE/CLEAN, CI green.
   - Acceptance criteria from issue #35.
4. Schedule I385 (board check, +15 min fire condition, waiting on SYNTHESIS.md or DAG fold).

### 4. Update STATE

Write updated STATE at `taskflow/overseer/I384/project_state.json`:
- Record new branch HEAD.
- If SYNTHESIS.md exists: record verdict and next step.
- If no SYNTHESIS.md and head advanced: record new head, reset stall cycle.
- If no SYNTHESIS.md and head unchanged (4/4): record r19 as STALLED, record r20 dispatch, record stall comment URL.

### 5. Schedule next step

If SYNTHESIS.md found: schedule the appropriate follow-up (review launch or remediation DAG dispatch).
If head advanced: schedule I385 as stall check 1/4 against new head (+15 min).
If 4/4 stall confirmed: re-fork as chirp-logged-out-r20 and schedule I385 as a watch step (+15 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r19 DAG path: `taskflow/dags/chirp-logged-out-r19/`. Process id: chirp-logged-out-r19.
- Prior stalls: r1–r18 all stalled. r18 stall comment: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6680286236
- stall_check_count so far: 3/4 (I383 — head unchanged, no synthesis).
- If 4/4 stall checks all show head UNCHANGED and no SYNTHESIS.md: confirm r19 stalled, re-fork as chirp-logged-out-r20, post stall comment on issue #35.
- PR #263: OPEN/MERGEABLE/CLEAN on `work/chirp-logged-out`. Head: `617f2539`. CI run 42183715802: completed/success.
