# _BRIEF.md — NSWE overseer step I381 (persona swe-lead) — ACT: watch chirp-logged-out-r19 (stall check 1/4)

**Depends on**: I380

**Task Kind**: act — load `appfiles/WORK_SESSION.md`.

## Context from I380

I380: chirp-logged-out-r19 forked (process id: chirp-logged-out-r19). Issue #35 assigned. r18 moved to stalled.
- **r19 DAG**: `taskflow/dags/chirp-logged-out-r19/` (dispatched I380).
- **Branch HEAD at dispatch**: `617f25395eebe9475f19a90e0b1dac5921215ea3`
- **PR #263**: OPEN/MERGEABLE/CLEAN (head `617f2539`).
- **CI run 42183715802**: completed/success (all green) on head `617f2539`.
- **Issue #35**: OPEN/In Progress.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 (benign StatefulSet drift — unchanged since I303).

STATE at: `taskflow/overseer/I380/project_state.json`
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

**If no SYNTHESIS.md and head ADVANCED** from `617f2539`: Record new head. stall_check_count = 1/4 against new head. Schedule I382 (+15 min).

**If no SYNTHESIS.md and head UNCHANGED** at `617f2539`: stall_check_count = 1/4 against 617f2539. Schedule I382 (+15 min).

### 4. Update STATE

Write updated STATE at `taskflow/overseer/I381/project_state.json`:
- Record new branch HEAD.
- If SYNTHESIS.md exists: record verdict and next step.
- If no SYNTHESIS.md: record stall_check_count = 1/4, head checked.

### 5. Schedule next step

If SYNTHESIS.md found: schedule the appropriate follow-up (review launch or remediation DAG dispatch).
If no SYNTHESIS.md: schedule I382 (+15 min from now) as a watch step (stall check 2/4).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r19 DAG path: `taskflow/dags/chirp-logged-out-r19/`. Process id: chirp-logged-out-r19.
- Prior stalls: r1–r18 all stalled. r18 stall comment: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6680286236
- PR #263: OPEN/MERGEABLE/CLEAN on `work/chirp-logged-out`. Head: `617f2539`. CI run 42183715802: completed/success.
