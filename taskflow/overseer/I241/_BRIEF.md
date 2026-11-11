# _BRIEF.md — NSWE overseer step I241 (persona swe-lead) — EVALUATE: fold ferric-http-r2 remediation DAG

**Depends on**: I240
**Task Kind**: evaluate — load `appfiles/REVIEW_GATE.md`, `appfiles/DELIVERABLES_GIT.md`, `appfiles/BOARD.md`.

## Context from I240 (EVALUATE: ferric-http-r2 still in flight, re-suspended)

- **ferric-http-r2** remediation DAG (swe-coder) was Running as of I240 check (dispatched 2026-11-04T20:01Z, Running 2026-11-04T20:02Z)
- No SYNTHESIS.md at `taskflow/dags/ferric-http-r2/SYNTHESIS.md` — DAG still in flight at I240
- I240 re-suspended on forked-thread-completion (ferric-http-r2) + 20-min timer
- PR **#210** OPEN: `work/ferric-http-r1` → `main`, closes #132 and #148
  - URL: https://github.com/Nousix-LLC/nswe-demo/pull/210
  - review comment: https://github.com/Nousix-LLC/nswe-demo/pull/210#issuecomment-6639957464
  - CI all 6 PASS (run 41812754296) — on the pre-remediation commit
- Blockers to fix (from review-ferric-http-r1):
  - B1: `query()` signature wrong — CHANGELOG declared `(self, key: &str, value: &str)`, actual `(mut self, params: &[(&str, &str)])`
  - B2: `Response::text()` signature wrong — CHANGELOG declared `(&self) -> &str`, actual `(self) -> String`
- **Non-blockers already filed**: #211 (header signature), #212 (absent API members), #213 (non_exhaustive)
- **Board**: #132 (`PVTI_lADOEB9jls4BlZH4zhFl_MI`) → In Progress; #148 (`PVTI_lADOEB9jls4BlZH4zhFl_pM`) → In Progress
- **STATE**: `taskflow/overseer/I240/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`
- Escalation ferric-async-forms STILL ACTIVE — do NOT launch ferric-async-forms-r3
- remediation attempt: 1/2 (budget: 2 attempts)

## Work for this step

### 1. Load governing files

Load `appfiles/REVIEW_GATE.md`, `appfiles/DELIVERABLES_GIT.md`, and `appfiles/BOARD.md`. Read `_CONFIG.yaml`.

### 2. Check ferric-http-r2 fold status

Check whether `taskflow/dags/ferric-http-r2/SYNTHESIS.md` exists and is a terminal record.

**If the DAG has not yet folded**: re-evaluate whether it is progressing or stalled.
- Check scheduler log at `taskflow/dags/ferric-http-r2/scheduler/logs/scheduler_decisions.jsonl`
- If progressing: re-suspend on forked-thread-completion + 20-min timer, schedule I242 to re-check
- If stalled (no progress since I240 check at ~20:02Z): escalate to user

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
  - Brief: re-review against the 2 original blockers + all should-fix items (SF3: #211, SF4: #212, SF5: #213)
  - Concerns: correctness (blocker signatures match actual compiled API), code quality, security (no leaked paths/addresses)
  - Schedule I242 to fold and act on the re-review

**On FAIL**:
- Record blockers in STATE
- Check remediation budget: ferric-http-r2 is attempt 1/2
- If budget permits (attempt 1 of 2): launch ferric-http-r3 remediation (swe-coder), carrying the specific failure details
- If budget exhausted (attempt 2 of 2): escalate to user via GitHub comment on PR #210 and issue on board

### 5. Update STATE

Write `taskflow/overseer/I241/project_state.json` with:
- ferric-http-r2 moved to `dags_folded` (if folded) with verdict and outcome
- If re-review launched: new review DAG in `dags_in_flight`
- If remediation attempt 2: ferric-http-r3 in `dags_in_flight`
- If still in flight: ferric-http-r2 updated with latest check timestamp

### 6. Schedule I242

Schedule I242 as the next iteration (fold re-review or fold next remediation, or re-check if still in flight).

## Notes

- Config: `landing_authority: delegated`, `auto_land: true`, `headless: true`
- Do NOT launch ferric-async-forms-r3 (escalation ACTIVE)
- issue_132 board item: `PVTI_lADOEB9jls4BlZH4zhFl_MI`
- issue_148 board item: `PVTI_lADOEB9jls4BlZH4zhFl_pM`
- PR #210: https://github.com/Nousix-LLC/nswe-demo/pull/210
- ferric-http-r2 DAG workspace: `taskflow/dags/ferric-http-r2/`
- Firing condition for I241: forked-thread-completion (ferric-http-r2) OR 20-min timer
