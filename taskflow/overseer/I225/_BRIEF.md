# _BRIEF.md — NSWE overseer step I225 (persona swe-lead) — EVALUATE: board check / watch review-ferric-router-r3 fold

**Depends on**: I224
**Task Kind**: evaluate — load `WORK_SESSION` + `REVIEW_GATE`. Board check / watch review-ferric-router-r3 fold.

## Context from I224 (ACT: launch review-ferric-router-r3)

- **review-ferric-router-r3 LAUNCHED** — running as `swe-reviewer`.
  - Brief: `taskflow/dags/review-ferric-router-r3/_BRIEF.md`
  - Target: PR #203 — `work/ferric-router-r3` (4 commits), issues #131, #146, #147.
  - CI: all 6 PASS (run 41796577463, commit 7219e21). PR OPEN/MERGEABLE.
  - 5 review concerns: correctness (REQ-RT-001..008), code quality, test coverage, Rust idioms, API/contract stability.
- **ferric-async-forms escalation**: ACTIVE, no user response yet. Hold.
- **Config**: delegated/auto_land/headless.
- **STATE**: `taskflow/overseer/I224/project_state.json`.
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.
- **free_dag_slots**: 2.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` + `appfiles/REVIEW_GATE.md`. Read `_CONFIG.yaml` and
`taskflow/overseer/I224/project_state.json`.

### 2. Check if review-ferric-router-r3 has folded
Fold condition: `taskflow/dags/review-ferric-router-r3/SYNTHESIS.md` exists.

If **folded**:
- Read the SYNTHESIS.md. Determine verdict (APPROVE or REQUEST_CHANGES).
- If **APPROVE**: schedule the action series:
  - Process review: add non-blockers to board, confirm review is on PR #203.
  - Land PR #203 under delegated authority (machine PASS + review APPROVE; config: delegated/auto_land/headless).
  - Deployment check after land.
  - Board check / next goal.
- If **REQUEST_CHANGES**: remediation budget for ferric-router is exhausted (r1+r2+r3 = 3 code DAGs, budget was 2 remediations beyond r1). Escalate to user with what was tried.

If **not yet folded**:
- Check board for any other activity (new issues, escalation clearing conditions, PRs, other changes).
- Suspend on bounded wake: review fold OR 10-minute timer, whichever comes first.

### 3. Update project STATE
Write `taskflow/overseer/I225/project_state.json` with current state.

## Notes
- Config: delegated/auto_land/headless.
- review-ferric-router-r3 runs as `swe-reviewer`.
- ferric-async-forms escalation (#130 / PR #193) still active — do NOT launch ferric-async-forms-r3 without user decision.
- If review REQUEST_CHANGES: escalation is the only path (budget exhausted).
