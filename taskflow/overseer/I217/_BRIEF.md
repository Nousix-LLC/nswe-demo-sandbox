# _BRIEF.md — NSWE overseer step I217 (persona swe-lead) — ACT: process both review folds

**Depends on**: I216
**Task Kind**: act — load `REVIEW_GATE` + `BOARD`. Record outcomes for both review folds; add non-blocking findings to the board project.

## Context from I216

Both review DAGs have folded with REQUEST CHANGES:
- **review-ferric-router-r1** (PR #192): REQUEST CHANGES — B1: PR bundles ~3,290 lines of undescribed scope (ferric-macros crate + context-API, commits for issues #137-#142) alongside the router work. Router work PASSES all 6 concerns in its own scope. Non-blockers filed by reviewer: #194 (navigate/navigate_replace input validation, aria-current), #195 (commit description narrower than #146 scope). Both #194 and #195 already have project item IDs in _CONFIG.yaml.
- **review-ferric-async-forms-r2** (PR #193): REQUEST CHANGES — 3 blockers: B1 (Resource fire-once, no reactive re-fetch; REQ-ASYNC-001/003/005), B2 (no prevent_default/stop_propagation callable from handlers; REQ-ASYNC-023), B3 (Bind DOM→signal direction broken in WASM runtime; REQ-ASYNC-042). Non-blockers #196-#201 filed by review DAG but NOT yet on board project.

STATE: `taskflow/overseer/I215/project_state.json`.
Config seam: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/REVIEW_GATE.md` and `appfiles/BOARD.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I215/project_state.json`.

### 2. Process review-ferric-router-r1
- Verify non-blockers #194 and #195 are on the board project (they have project item IDs in _CONFIG.yaml already).
- If #178 (pre-existing, referenced as NB2) is not already on board, verify its status.
- Record the review outcome in STATE: REQUEST CHANGES, B1 (scope bundling), non-blockers #194/#195/#178.
- Update PR #192 record: review_verdict = REQUEST_CHANGES, review_dag_status = FOLDED.
- review-ferric-router-r1 moves from dags_in_flight to dags_folded in STATE.

### 3. Process review-ferric-async-forms-r2
- Add issues #196, #197, #198, #199, #200, #201 to the board project (gh project item add), record their project item IDs in `_CONFIG.yaml`.
- Record the review outcome in STATE: REQUEST CHANGES, 3 blockers (B1 reactive re-fetch, B2 prevent_default, B3 Bind DOM→signal), non-blockers #196-#201.
- Update PR #193 record: review_verdict = REQUEST_CHANGES, review_dag_status = FOLDED.
- review-ferric-async-forms-r2 moves from dags_in_flight to dags_folded in STATE.

### 4. Write project_state.json
Write `taskflow/overseer/I217/project_state.json` with:
- Both review DAGs moved from dags_in_flight to dags_folded
- PR #192 and PR #193 records updated with verdicts
- free_dag_slots updated to 3 (both reviews freed their slots)
- board total updated with new items
- forward_series entry for I217

### 5. Schedule what follows
I218 follows (launch router remediation).

## Notes

- Config: delegated/auto_land/headless.
- Both remediations are within budget: router is first attempt at remediation; async-forms-r3 would be attempt 2 of 2 on the codebase (async-forms-r1 was a machine-gate FAIL on wrong repo; async-forms-r2 is first real attempt), review REQUEST CHANGES = new remediation budget.
- Do not launch any DAGs in this step — I218 handles router remediation, I219 handles async-forms remediation.
