# _BRIEF.md — NSWE overseer step I232 (persona swe-lead) — EVALUATE: fold devops DAG result + decide next code goal

**Depends on**: I231
**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md`, `appfiles/REVIEW_GATE.md`. Read the devops DAG result; if PASS, launch review DAG; decide next code goal.

## Context from I231 (EVALUATE: check devops DAG — still running)

- **Escalation**: ferric-async-forms budget exhausted (PR #193) — STILL ACTIVE, no user response. Do NOT launch ferric-async-forms-r3.
- **Devops DAG**: `taskflow/dags/update-chirp-server-digest-r1/` (swe-coder)
  - Goal: update `deploy/10-deployment.yaml` chirp-server image digest to d8230fea build (CI run 41803200262)
  - Tracking issue: #208 (board item PVTI_lADOEB9jls4BlZH4zhF7Wkk) — NOTE: check if #208 or #206 is the correct issue number; the STATE records it as #206 (PVTI_lADOEB9jls4BlZH4zhF7WNw)
  - I231 check: DAG not folded yet (no SYNTHESIS.md). Re-suspended with 20-min timer + forked-thread-completion.
- **STATE**: `taskflow/overseer/I231/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/REVIEW_GATE.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I231/project_state.json`.

### 2. Check devops DAG status

Read `taskflow/dags/update-chirp-server-digest-r1/SYNTHESIS.md` (or COMPLETE.md if present).

**If DAG has NOT folded yet** (no SYNTHESIS.md):
- Record the check in STATE
- Schedule I233 as a board check / DAG fold check; self-suspend on forked-thread-completion + 20-minute timer

**If DAG folded — machine gate PASS**:
- Read SYNTHESIS.md verdict
- Confirm PR exists, CI all 6 jobs PASS, branch work/update-chirp-server-digest-r1 clean
- Launch review DAG (swe-reviewer) for PR: write `taskflow/dags/review-update-chirp-server-digest-r1/_BRIEF.md` and fork
- Record review DAG in STATE (dags_in_flight)
- Update board: issue #206 (chirp-server image digest update) → In Progress
- Schedule I233 to fold review result + land + decide next code goal (#132 HTTP Client)

**If DAG folded — machine gate FAIL**:
- Read SYNTHESIS.md failure details
- Determine if remediation budget allows (attempt 1 of 2: re-drive as update-chirp-server-digest-r2)
- Launch remediation DAG if budget allows; escalate to user if exhausted
- Schedule I233 for next check

### 3. Post-review path (if reviewing)

When review folds (handled in I233 or later):
- If review APPROVE: land PR under delegated authority (`landing_authority: delegated`, `auto_land: true`)
  - Squash-merge PR to main
  - Move issue #206 to Done on board
  - Append work_item to STATE
  - After land: check deployment (chirp-server image should update)
- If review REQUEST_CHANGES: remediate within budget

### 4. Next code goal: #132 HTTP Client (Ferric 1.0)

After digest update lands:
- Next code epic: #132 (HTTP Client — Ferric 1.0 http client, usable_early)
  - Depends on #131 (LANDED ✓) and #129 (LANDED ✓)
  - Both prerequisites are on main
- Schedule I233 or I234 as the launch task for #132 (after board check confirms it is next priority)

## Notes

- Config: delegated/auto_land/headless
- Do NOT launch ferric-async-forms-r3 — escalation ACTIVE
- Review DAG brief should reference: PR, CI run, issue #206, deploy/10-deployment.yaml change
- The devops DAG (swe-coder) finds the actual image digest from CI run 41803200262 output or the registry
- issue #206 board item ID: PVTI_lADOEB9jls4BlZH4zhF7WNw
