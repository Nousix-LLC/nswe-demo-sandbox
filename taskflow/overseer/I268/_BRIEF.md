# _BRIEF.md — NSWE overseer step I268 (persona swe-lead) — ACT: bounded watch (PR #228 escalation)

**Depends on**: I267
**Task Kind**: act — load `appfiles/RETENTION.md`.

## Context from I267

- Escalation comment posted on PR #228 explaining the two blockers (B1: hydrate() not wired; B2: zero wasm-bindgen-test), exhausted remediation budget (2/2), and decision options (extend budget or defer).
- Escalation recorded in STATE at `taskflow/overseer/I267/project_state.json`.
- Board status for #223, #224, #226 set to Blocked.
- STATE at: `taskflow/overseer/I267/project_state.json`
- Config seam: `taskflow/overseer/_CONFIG.yaml`

### Active escalations

- **escalation_ferric_ssr_budget_exhausted** (ACTIVE): 2 blockers, PR #228, decision needed.
  - Escalation comment URL: recorded in project_state.json.
- **escalation_ferric_async_forms_budget_exhausted** (ACTIVE): PR #193. No user response.

## Work for this step

### 1. Load governing file

Load `appfiles/RETENTION.md`.

### 2. Read config seam and prior STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I267/project_state.json`.

### 3. Check for user response on PR #228

Fetch comments on PR #228 since the escalation comment (comment 6647644348). Look for a user comment indicating a decision:
- "extend budget" / "try again" / "fix it" → dispatch ferric-ssr-r4 DAG
- "defer" / "close" / "backlog" → close PR #228, return #223/#224/#226 to backlog

### 4. If user has responded — act on the decision

**If extend budget:** Dispatch a new code DAG `ferric-ssr-r4` carrying:
  - Blockers B1 (hydrate() wiring) and B2 (wasm-bindgen-test coverage)
  - Branch: `work/ferric-ssr-r1`, PR #228
  - Acceptance criteria from #223, #224, #226 and the review findings

**If defer:** Close PR #228, set #223/#224/#226 to closed/deferred on the board, update STATE.

### 5. If no user response — re-suspend

If no user response yet, update STATE (note: re-checked, no response) and schedule I269 as a fresh bounded watch (+10 minutes).

## Notes

- The ferric-async-forms escalation (PR #193) remains open; check for a response on it too as a secondary pass.
- Write updated STATE at `taskflow/overseer/I268/project_state.json`.
- Suspension firing condition: `window-ownership AND input-arrival` OR `schedule resume_at` (+10 min from now), whichever fires first.
