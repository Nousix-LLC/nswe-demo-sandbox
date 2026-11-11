# _BRIEF.md — NSWE overseer step I227 (persona swe-lead) — ACT: land PR #203

**Depends on**: I226
**Task Kind**: act — load `DELIVERABLES_GIT` + `RETENTION`. Land PR #203 (ferric-router-r3); close superseded PRs #192/#202; move issues #131/#146/#147 to Done on board; append work_items entry; update main_sha.

## Context from I226 (ACT: process review-ferric-router-r3)

- **review-ferric-router-r3** APPROVE processed:
  - Non-blockers #204 and #205 added to board (Todo): `PVTI_lADOEB9jls4BlZH4zhF7IB8` / `PVTI_lADOEB9jls4BlZH4zhF7IEk`
  - Review confirmed on PR #203 as comment (self-approval block, APPROVE verdict stated, protocol-correct)
- **Config**: delegated/auto_land/headless. All landing conditions met.
- **PR #203**: OPEN/MERGEABLE, CI all 6 PASS (run 41796577463, commit 7219e21), issues #131/#146/#147
- **STATE**: `taskflow/overseer/I226/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files
Load `appfiles/DELIVERABLES_GIT.md` + `appfiles/RETENTION.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I226/project_state.json`.

### 2. Verify landing conditions live
- Confirm PR #203 is still OPEN and MERGEABLE
- Confirm CI all 6 PASS on head SHA 7219e21 (run 41796577463)
- Confirm review APPROVE (comment posted by review DAG)
- Config: landing_authority=delegated, auto_land=true, headless=true ✓

### 3. Land PR #203
- Squash-merge PR #203 under delegated authority
- Record merge commit SHA
- Note: Issues #131/#146/#147 should auto-close via closing keywords in PR description

### 4. Close superseded PRs #192 and #202
- Close PR #192 (ferric-router-r1) with note it was superseded by PR #203
- Close PR #202 (ferric-router-r2) with note it was superseded by PR #203

### 5. Move issues #131/#146/#147 to Done on board
- If not auto-closed by merge, close them
- Move board status to Done for #131, #146, #147

### 6. Update project STATE
Write `taskflow/overseer/I227/project_state.json` with:
- PR #203 status=MERGED, merge_commit=<sha>
- PR #192 status=CLOSED (superseded by #203)
- PR #202 status=CLOSED (superseded by #203)
- Issues #131/#146/#147 moved to Done
- work_items entry for ferric-router (PRs #192→#202→#203)
- main_sha updated to new merge commit
- free_dag_slots: 3 (unchanged)
- I228 follows (deployment check after PR #203 land)

## Notes
- Config: delegated/auto_land/headless. No human approval step.
- ferric-async-forms escalation (#130 / PR #193) still active — do NOT launch ferric-async-forms-r3 without user decision.
- After landing, I228 does deployment check (CI on merge commit, ArgoCD, pods, endpoint).
- I229 will do board check / next goal (likely #132 HTTP Client if escalation still active).
