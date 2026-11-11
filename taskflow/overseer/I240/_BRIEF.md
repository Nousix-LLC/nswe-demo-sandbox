# _BRIEF.md — NSWE overseer step I240 (persona swe-lead) — EVALUATE: fold ferric-http-r2 remediation DAG

**Depends on**: I239
**Task Kind**: evaluate — load `appfiles/REVIEW_GATE.md`, `appfiles/DELIVERABLES_GIT.md`, `appfiles/BOARD.md`.

## Context from I239 (ACT: REQUEST_CHANGES — remediation launched)

- **review-ferric-http-r1** DAG folded with verdict: **REQUEST CHANGES** (2 blockers)
- PR **#210** OPEN: `work/ferric-http-r1` → `main`, closes #132 and #148 (unchanged, still open)
  - URL: https://github.com/Nousix-LLC/nswe-demo/pull/210
  - review comment: https://github.com/Nousix-LLC/nswe-demo/pull/210#issuecomment-6639957464
  - CI all 6 PASS (run 41812754296)
- **ferric-http-r2** remediation DAG forked (swe-coder) in I239
  - Goal: fix CHANGELOG.md — 2 blockers from review-ferric-http-r1
  - Workspace: `taskflow/dags/ferric-http-r2/`
- **Non-blocker issues filed in I239**: see STATE for issue numbers
- **Board**: #132 (`PVTI_lADOEB9jls4BlZH4zhFl_MI`) → In Progress; #148 (`PVTI_lADOEB9jls4BlZH4zhFl_pM`) → In Progress
- **STATE**: `taskflow/overseer/I239/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`
- Escalation ferric-async-forms STILL ACTIVE — do NOT launch ferric-async-forms-r3
- Free DAG slots: 1 (ferric-http-r2 remediation in flight)

## Work for this step

### 1. Load governing files

Load `appfiles/REVIEW_GATE.md`, `appfiles/DELIVERABLES_GIT.md`, and `appfiles/BOARD.md`. Read `_CONFIG.yaml`.

### 2. Check ferric-http-r2 fold status

Check whether `taskflow/dags/ferric-http-r2/SYNTHESIS.md` exists and is a terminal record.

**If the DAG has not yet folded**: re-evaluate whether it is progressing or stalled. If still in flight,
re-suspend on forked-thread-completion + 20-min timer and schedule I241 to re-check.

**If the DAG has folded**:

### 3. Read the remediation SYNTHESIS.md

Read `taskflow/dags/ferric-http-r2/SYNTHESIS.md`. Evaluate:
- Verdict: PASS / FAIL
- Did it fix the 2 blockers?
  - B1: `query()` signature wrong (CHANGELOG declared `(self, key: &str, value: &str)`, actual `(mut self, params: &[(&str, &str)])`)
  - B2: `Response::text()` signature wrong (CHANGELOG declared `(&self) -> &str`, actual `(self) -> String`)
- CI status on the new commits

### 4. Act on the verdict

**On PASS** (CI passing, blockers addressed):
- Launch review DAG (swe-reviewer) for PR #210 re-review
  - Brief: re-review against the 2 original blockers + all should-fix items (3, 4, 5)
  - Schedule I241 to fold and act on the re-review

**On FAIL**:
- Record blockers in STATE
- Check remediation budget: ferric-http-r2 is attempt 1/2
- If budget permits: launch ferric-http-r3 remediation (swe-coder)
- If budget exhausted: escalate to user

### 5. Update STATE

Write `taskflow/overseer/I240/project_state.json` with:
- ferric-http-r2 moved to `dags_folded` with verdict
- If re-review launched: new review DAG in `dags_in_flight`
- If remediation attempt 2: ferric-http-r3 in `dags_in_flight`

### 6. Schedule I241

Schedule I241 as the next iteration (fold re-review or fold next remediation).

## Notes

- Config: `landing_authority: delegated`, `auto_land: true`, `headless: true`
- Do NOT launch ferric-async-forms-r3 (escalation ACTIVE)
- issue_132 board item: `PVTI_lADOEB9jls4BlZH4zhFl_MI`
- issue_148 board item: `PVTI_lADOEB9jls4BlZH4zhFl_pM`
- PR #210: https://github.com/Nousix-LLC/nswe-demo/pull/210
- ferric-http-r2 DAG workspace: `taskflow/dags/ferric-http-r2/`
- Firing condition for I240: forked-thread-completion (ferric-http-r2) OR 20-min timer
