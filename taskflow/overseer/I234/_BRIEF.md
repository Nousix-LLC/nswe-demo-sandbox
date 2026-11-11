# _BRIEF.md — NSWE overseer step I234 (persona swe-lead) — EVALUATE: fold review-update-chirp-server-digest-r1 for PR #209

**Depends on**: I233  
**Task Kind**: evaluate — load `appfiles/REVIEW_GATE.md`, `appfiles/WORK_SESSION.md`, `appfiles/DELIVERABLES_GIT.md`.

## Context from I233 (ACT: review DAG forked, board updated)

- **review-update-chirp-server-digest-r1** forked (swe-reviewer) for PR #209
  - Review brief: `taskflow/dags/review-update-chirp-server-digest-r1/_BRIEF.md`
  - Synthesis to read: `taskflow/dags/review-update-chirp-server-digest-r1/SYNTHESIS.md`
- **PR #209**: `deploy/update-chirp-server-digest-d8230fea` → `main`, machine gate PASS, CI all 6 PASS (run 41806003677), MERGEABLE
- **Issue #206**: chirp-server image digest update — board item `PVTI_lADOEB9jls4BlZH4zhF7WNw` (In Progress)
- **STATE**: `taskflow/overseer/I233/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`
- Escalation ferric-async-forms STILL ACTIVE — do NOT launch ferric-async-forms-r3

## Work for this step

### 1. Load governing files

Load `appfiles/REVIEW_GATE.md`, `appfiles/WORK_SESSION.md`, `appfiles/DELIVERABLES_GIT.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I233/project_state.json`.

### 2. Check review DAG status

Check `taskflow/dags/review-update-chirp-server-digest-r1/SYNTHESIS.md`.

- **If SYNTHESIS.md exists** (review DAG folded): proceed to step 3.
- **If SYNTHESIS.md does not exist** (review DAG still running): re-suspend on forked-thread-completion (review-update-chirp-server-digest-r1) + 20-minute timer. Schedule I235 to re-check.

### 3. Evaluate review verdict

Read `review-update-chirp-server-digest-r1/SYNTHESIS.md` for the verdict.

**If APPROVE**:
1. Land PR #209: `gh pr merge 209 --squash --repo Nousix-LLC/nswe-demo`
2. Update board item `PVTI_lADOEB9jls4BlZH4zhF7WNw` → Done (`98236657`)
3. Record work_item in STATE (issue_closed: #206, pr: 209, verdict: LANDED)
4. Check deployment: SSH kubectl -n chirp get pods to confirm ArgoCD syncs and pod restarts on new image (sha256:f845ca8c). Check `http://100.90.75.93:8081` returns HTTP 200.
5. Assess next code goal: **#132 HTTP Client (Ferric 1.0)** — depends on #131 (LANDED ✓) and #129 (LANDED ✓). Brief a code DAG `ferric-http-r1` for issue #132.

**If REQUEST_CHANGES**:
1. Read blockers from SYNTHESIS.md
2. Assess whether remediation is feasible within budget (attempt 1 of 2)
3. If remediable: schedule I235 ACT to launch remediation DAG `update-chirp-server-digest-r2`
4. If not: escalate to user with specific blockers

### 4. Update STATE

Write `taskflow/overseer/I234/project_state.json` with updated review status and board.

### 5. Schedule I235

Based on the outcome above:
- If PR landed: I235 EVALUATE — assess deployment, then assess next code goal #132 HTTP Client
- If review pending: I235 EVALUATE — re-check review DAG (re-suspend)

## Notes

- Config: `landing_authority: delegated`, `auto_land: true`, `headless: true` → land on APPROVE without human gate
- Do NOT launch ferric-async-forms-r3 (escalation ACTIVE)
- Next code goal after #206 Done: **#132 HTTP Client (Ferric 1.0)** — depends on #131 (LANDED ✓) and #129 (LANDED ✓)
- issue_206 board item: `PVTI_lADOEB9jls4BlZH4zhF7WNw`
- PR #209: https://github.com/Nousix-LLC/nswe-demo/pull/209
