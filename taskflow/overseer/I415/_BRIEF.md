# _BRIEF.md — NSWE overseer step I415 (persona swe-lead) — EVALUATE: stall check 1/4 for review-chirp-logged-out-r1

**Depends on**: I414

**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

## Context from I414

I414: review DAG `review-chirp-logged-out-r1` launched. PR #263 is under review.

- **Review DAG**: `review-chirp-logged-out-r1` — FORKED in I414
- **Review DAG workspace**: `taskflow/dags/review-chirp-logged-out-r1/`
- **PR #263**: OPEN/MERGEABLE, head `decb6196c2c1e6ed421d393a642f0c844cc333ba`
- **Branch**: `work/chirp-logged-out`
- **Issue**: #35 ("Logged-out reading and a useful landing with accurate states")
- **Free DAG slots**: 3

STATE at: `taskflow/overseer/I414/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

---

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`.

### 2. Read config seam and STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I414/project_state.json`.

### 3. Check review-chirp-logged-out-r1 progress

Check the review DAG's progress:
- Look for `taskflow/dags/review-chirp-logged-out-r1/SYNTHESIS.md` (terminal: folded)
- Look for child task activity (subtasks under the DAG workspace)
- Check PR #263 for a posted review (`gh pr view 263 --repo Nousix-LLC/nswe-demo`)

### 4. Decide

- **SYNTHESIS.md found with verdict**: DAG has folded. Read it. Evaluate the verdict (APPROVE → land path; REQUEST-CHANGES → remediation path). Schedule the appropriate next step (landing or remediation). This is stall check 1/4 — if folded, proceed.
- **No SYNTHESIS.md**: DAG still in-flight. Record stall check 1/4 observation. Schedule stall check 2/4 (I416).

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I415/project_state.json` recording the check outcome.

### 6. Schedule next step

- If folded APPROVE: schedule I416 as a landing step.
- If folded REQUEST-CHANGES: schedule I416 as a remediation-launch step.
- If still in-flight: schedule I416 as stall check 2/4 for review-chirp-logged-out-r1. Suspend I415 on a bounded wake: `+15 min from now OR review-chirp-logged-out-r1 forked-thread-completion`.

## Notes

- headless: true; landing_authority: delegated — read from `_CONFIG.yaml`.
- DAG slots: 3 free.
- This is stall check 1/4. If the DAG has not folded by check 4/4, classify as stalled and re-fork.
