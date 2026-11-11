# _BRIEF.md — NSWE overseer step I385 (persona swe-lead) — ACT: watch chirp-logged-out-r20 (stall check 1/4)

**Depends on**: I384

**Task Kind**: act — load `appfiles/WORK_SESSION.md`.

## Context from I384

I384: stall check 4/4 for chirp-logged-out-r19 — head UNCHANGED at `617f2539`, no SYNTHESIS.md. r19 confirmed STALLED (4/4).
- **Action taken**: r19 moved to `dags_stalled`. Stall comment posted: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6680541037. r20 forked (swe-coder) as `chirp-logged-out-r20`.
- **r20 DAG**: `taskflow/dags/chirp-logged-out-r20/` (dispatched I384).
- **Branch HEAD at I384**: `617f25395eebe9475f19a90e0b1dac5921215ea3` (unchanged from r19 dispatch).
- **PR #263**: OPEN/MERGEABLE/CLEAN (head `617f2539`).
- **CI run 42183715802**: completed/success (all green) on head `617f2539`.
- **Issue #35**: OPEN/In Progress.
- **ArgoCD**: OutOfSync/Healthy/cb1ced3 (benign StatefulSet drift — unchanged since I303).

STATE at: `taskflow/overseer/I384/project_state.json`
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

**If no SYNTHESIS.md and head ADVANCED** from `617f2539`: Record new head. stall_check_count = 1/4 against new head. Schedule I386 (+15 min) as stall check 2/4 against new head.

**If no SYNTHESIS.md and head UNCHANGED** at `617f2539`: stall_check_count = 1/4. Schedule I386 (+15 min) as stall check 2/4.

### 4. Update STATE

Write updated STATE at `taskflow/overseer/I385/project_state.json`:
- Record current branch HEAD.
- If SYNTHESIS.md exists: record verdict and next step.
- If no SYNTHESIS.md: record stall_check_count = 1/4, record head, schedule I386.

### 5. Schedule next step

If SYNTHESIS.md found: schedule the appropriate follow-up (review launch or remediation DAG dispatch).
If no SYNTHESIS.md: schedule I386 as stall check 2/4 (+15 min from I385).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. Main HEAD = cb1ced3.
- r20 DAG path: `taskflow/dags/chirp-logged-out-r20/`. Process id: chirp-logged-out-r20.
- Prior stalls: r1–r19 all stalled. r19 stall comment: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6680541037
- stall_check_count so far: 0/4 (r20 just dispatched in I384).
- PR #263: OPEN/MERGEABLE/CLEAN on `work/chirp-logged-out`. Head: `617f2539`. CI run 42183715802: completed/success.
