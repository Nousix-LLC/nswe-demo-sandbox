# _BRIEF.md — NSWE overseer step I275 (persona swe-lead) — ACT: bounded watch (PR #228 escalation)

**Depends on**: I274
**Task Kind**: act — load `appfiles/RETENTION.md`.

## Context from I274

- I274 checked PR #228 and PR #193 comments. No user response on either.
- Escalation on PR #228 comment: https://github.com/Nousix-LLC/nswe-demo/pull/228#issuecomment-6666246221
- Escalation on PR #193 comment: https://github.com/Nousix-LLC/nswe-demo/pull/193#issuecomment-6624409600
- STATE at: `taskflow/overseer/I274/project_state.json`
- Config seam: `taskflow/overseer/_CONFIG.yaml`

### Active escalations

- **escalation_ferric_ssr_budget_exhausted** (ACTIVE): 2 blockers, PR #228, decision needed.
  - Escalation comment URL: https://github.com/Nousix-LLC/nswe-demo/pull/228#issuecomment-6666246221
- **escalation_ferric_async_forms_budget_exhausted** (ACTIVE): PR #193. No user response.
  - Escalation comment URL: https://github.com/Nousix-LLC/nswe-demo/pull/193#issuecomment-6624409600

## Work for this step

### 1. Load governing file

Load `appfiles/RETENTION.md`.

### 2. Read config seam and prior STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I274/project_state.json`.

### 3. Check for user response on PR #228

Fetch comments on PR #228. Look for a user comment indicating a decision (a comment not from the overseer bot):
- "extend budget" / "try again" / "fix it" → dispatch ferric-ssr-r4 DAG
- "defer" / "close" / "backlog" → close PR #228, return #223/#224/#226 to backlog

### 4. If user has responded — act on the decision

**If extend budget:** Dispatch a new code DAG `ferric-ssr-r4` carrying:
  - Blockers B1 (hydrate() wiring) and B2 (wasm-bindgen-test coverage)
  - Branch: `work/ferric-ssr-r1`, PR #228
  - Acceptance criteria from #223, #224, #226 and the review findings

**If defer:** Close PR #228, set #223/#224/#226 to closed/deferred on the board, update STATE.

### 5. If no user response — re-suspend

If no user response yet, update STATE (note: re-checked, no response) and schedule I276 as a fresh bounded watch (+10 minutes).

## Notes

- The ferric-async-forms escalation (PR #193) remains open; check for a response on it too as a secondary pass.
- Write updated STATE at `taskflow/overseer/I275/project_state.json`.
- Suspension firing condition: `window-ownership AND input-arrival` OR `schedule resume_at` (+10 min from now), whichever fires first.
