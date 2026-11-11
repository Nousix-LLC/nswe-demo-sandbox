# _BRIEF.md — NSWE overseer step I421 (persona swe-lead) — Stall check 1/4: review-chirp-logged-out-r2

**Depends on**: I420

**Task Kind**: act — load `appfiles/WORK_SESSION.md`.

## Context from I420

I420: launched review-chirp-logged-out-r2 — forked as `swe-reviewer` DAG. PR #263 (`work/chirp-logged-out`, HEAD `7f4b684671cab7eb778f5ad7f54dfdc82d57b3c4`) OPEN/MERGEABLE. CI 6/6 green. Both blockers (B1 + B2) fixed. All 5 ACs confirmed by chirp-logged-out-r27.

- **review-chirp-logged-out-r2**: FORKED as `swe-reviewer` — workspace `taskflow/dags/review-chirp-logged-out-r2/`, thread_id `review-chirp-logged-out-r2`
- **Synthesis path**: `taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md`
- **PR #263**: OPEN/MERGEABLE, HEAD `7f4b684`, CI ALL 6 PASS

STATE at: `taskflow/overseer/I420/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

---

## Work for this step

### 1. Load governing files

Load `appfiles/WORK_SESSION.md`.

### 2. Read config seam and STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I420/project_state.json`.

### 3. Stall check 1/4: review-chirp-logged-out-r2

Check if `taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md` exists and has a verdict.

**If SYNTHESIS.md present with verdict**:
- Read it and determine verdict (APPROVE or REQUEST-CHANGES)
- If APPROVE: land PR #263 (`gh pr merge 263 --squash --delete-branch -R Nousix-LLC/nswe-demo`), close issue #35, do deployment check, check board for next goal
- If REQUEST-CHANGES: read blockers, record them, fork remediation DAG for PR #263 carrying the new blockers

**If SYNTHESIS.md not present / DAG still in flight**:
- Check DAG progress (look for any completed sub-task files in `taskflow/dags/review-chirp-logged-out-r2/`)
- If progressing: schedule I422 as stall check 2/4 and suspend (+15 min or DAG completion)
- If frozen / no progress: assess whether to re-fork

### 4. Update STATE

Write updated STATE at `taskflow/overseer/I421/project_state.json` recording review outcome or continued in-flight status.

### 5. Schedule next step

Schedule I422 based on outcome (next stall check, or the step after landing).

## Notes

- headless: true; landing_authority: delegated — read from `_CONFIG.yaml`
- On APPROVE: land immediately with `gh pr merge 263 --squash --delete-branch -R Nousix-LLC/nswe-demo`
- After landing: close issue #35, deployment check, board check for next goal
- After landing PR #263, check the board for the next highest-priority open issue
