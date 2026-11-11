# _BRIEF.md — NSWE overseer step I239 (persona swe-lead) — EVALUATE: fold review-ferric-http-r1 and land

**Depends on**: I238
**Task Kind**: evaluate — load `appfiles/REVIEW_GATE.md`, `appfiles/DELIVERABLES_GIT.md`, `appfiles/BOARD.md`.

## Context from I238 (ACT: review-ferric-http-r1 DAG forked)

- **review-ferric-http-r1** DAG forked (swe-reviewer) in I238
- PR **#210** OPEN: `work/ferric-http-r1` → `main`, closes #132 and #148
  - URL: https://github.com/Nousix-LLC/nswe-demo/pull/210
  - Single additive commit `d6a9b6e`: `crates/ferric-http/CHANGELOG.md` (142 lines)
  - CI all 6 PASS (run 41812754296)
- **Board**: #132 (`PVTI_lADOEB9jls4BlZH4zhFl_MI`) → In Progress; #148 (`PVTI_lADOEB9jls4BlZH4zhFl_pM`) → In Progress
- **STATE**: `taskflow/overseer/I238/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`
- Escalation ferric-async-forms STILL ACTIVE — do NOT launch ferric-async-forms-r3
- Free DAG slots: 1 (review-ferric-http-r1 in flight)

## Work for this step

### 1. Load governing files

Load `appfiles/REVIEW_GATE.md`, `appfiles/DELIVERABLES_GIT.md`, and `appfiles/BOARD.md`. Read `_CONFIG.yaml`.

### 2. Check review-ferric-http-r1 fold status

Check whether `taskflow/dags/review-ferric-http-r1/SYNTHESIS.md` exists and is a terminal record.

**If the DAG has not yet folded**: re-evaluate whether it is progressing or stalled. If still in flight,
re-suspend on forked-thread-completion + 20-min timer and schedule I240 to re-check.

**If the DAG has folded**:

### 3. Read the review SYNTHESIS.md

Read `taskflow/dags/review-ferric-http-r1/SYNTHESIS.md`. Evaluate:
- Verdict: APPROVE / REQUEST_CHANGES / REJECT
- Blockers (if any): what must change before PR #210 can land
- Non-blockers: file as backlog issues if the review DAG did not (per REVIEW_GATE.md)

### 4. Act on the verdict

**On APPROVE** (config: `landing_authority: delegated`, `auto_land: true`, `headless: true`):
- PR #210 is machine-PASS + review APPROVE → land it
- Squash-merge PR #210 under delegated authority (`appfiles/DELIVERABLES_GIT.md`)
- Move board items #132 and #148 to Done
- Record landing in STATE

**On REQUEST_CHANGES / REJECT**:
- Record blockers in STATE
- Launch a remediation DAG (swe-coder) carrying the blockers + original acceptance criteria
- Move board items to appropriate status
- Do NOT launch ferric-async-forms-r3 (escalation ACTIVE)

### 5. Update STATE

Write `taskflow/overseer/I239/project_state.json` with:
- review-ferric-http-r1 moved to `dags_folded` with verdict
- If landed: PR #210 → MERGED, issues #132 and #148 → Done
- If remediation: new remediation DAG in `dags_in_flight`

### 6. Schedule I240

Schedule I240 as the next iteration (EVALUATE board health + deployment check, or re-check if DAG not folded).

## Notes

- Config: `landing_authority: delegated`, `auto_land: true`, `headless: true`
- Do NOT launch ferric-async-forms-r3 (escalation ACTIVE)
- issue_132 board item: `PVTI_lADOEB9jls4BlZH4zhFl_MI`
- issue_148 board item: `PVTI_lADOEB9jls4BlZH4zhFl_pM`
- PR #210: https://github.com/Nousix-LLC/nswe-demo/pull/210
- review-ferric-http-r1 DAG workspace: `taskflow/dags/review-ferric-http-r1/`
- Firing condition for I239: forked-thread-completion (review-ferric-http-r1) OR 20-min timer
