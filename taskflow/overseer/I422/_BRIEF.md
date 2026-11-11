# _BRIEF.md — NSWE overseer step I422 (persona swe-lead) — Stall check 2/4: review-chirp-logged-out-r2

**Depends on**: I421

**Task Kind**: act — load `appfiles/WORK_SESSION.md`.

## Context from I421

I421: stall check 1/4 — DAG in-flight and progressing. No root SYNTHESIS.md yet.

**Progress observed in I421:**
- `SUBTASK_verify-fixes`: COMPLETE — B1 (`timeline.rs:218`) and B2 (`compose.rs:519`) both PASS, diff clean (single commit, two lines, no collateral changes)
- `SUBTASK_verify-acs`: 3/4 children COMPLETE (`ac1-verify`, `ac4-verify`, `ac235-confirm`); `acs-gate` READY (not yet dispatched)
- `SUBTASK_synthesis`: PENDING (depends on verify-fixes + verify-acs)
- Root `SYNTHESIS.md`: not present

DAG tree is progressing; `acs-gate` → `findings-acs.md` → `SUBTASK_synthesis` → root `SYNTHESIS.md` is the remaining path.

- **review-chirp-logged-out-r2**: still IN-FLIGHT — workspace `taskflow/dags/review-chirp-logged-out-r2/`, thread_id `review-chirp-logged-out-r2`
- **Synthesis path**: `taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md`
- **PR #263**: OPEN/MERGEABLE, HEAD `7f4b684`, CI ALL 6 PASS

STATE at: `taskflow/overseer/I421/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

---

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md`.

### 2. Read config seam and STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I421/project_state.json`.

### 3. Stall check 2/4: review-chirp-logged-out-r2

Check if `taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md` exists and has a verdict.

**If SYNTHESIS.md present with verdict**:
- Read it and determine verdict (APPROVE or REQUEST-CHANGES)
- If APPROVE: land PR #263 (`gh pr merge 263 --squash --delete-branch -R Nousix-LLC/nswe-demo`), close issue #35, do deployment check, check board for next goal
- If REQUEST-CHANGES: read blockers, record them, fork remediation DAG for PR #263 carrying the new blockers

**If SYNTHESIS.md not present / DAG still in flight**:
- Check DAG progress (look for completed files in `taskflow/dags/review-chirp-logged-out-r2/`)
- Assess current state: `acs-gate` READY → `findings-acs.md` → `SUBTASK_synthesis` → root `SYNTHESIS.md`
- If progressing: schedule I423 as stall check 3/4 and suspend (+15 min or DAG completion)
- If frozen / no progress since I421: assess whether to re-fork

### 4. Update STATE

Write updated STATE at `taskflow/overseer/I422/project_state.json` recording review outcome or continued in-flight status.

### 5. Schedule next step

Schedule I423 based on outcome (next stall check, or the step after landing).

## Notes

- headless: true; landing_authority: delegated — read from `_CONFIG.yaml`
- On APPROVE: land immediately with `gh pr merge 263 --squash --delete-branch -R Nousix-LLC/nswe-demo`
- After landing: close issue #35, deployment check, board check for next goal
- After landing PR #263, check the board for the next highest-priority open issue
