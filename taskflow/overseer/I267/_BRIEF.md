# _BRIEF.md — NSWE overseer step I267 (persona swe-lead) — ACT: escalate to user (PR #228 blockers)

**Depends on**: I266
**Task Kind**: act — load `appfiles/RETENTION.md` and `appfiles/BOARD.md`.

## Context from I266

- review-ferric-ssr-r1 folded with REQUEST-CHANGES.
- Review comment confirmed on PR #228: https://github.com/Nousix-LLC/nswe-demo/pull/228#issuecomment-6647644348
- Non-blockers #229–#242 added to board (Todo status). Project item IDs recorded in `taskflow/overseer/_CONFIG.yaml`.
- Two blockers remain unresolved; remediation budget exhausted (2/2).
- STATE at: `taskflow/overseer/I266/project_state.json`
- Config seam: `taskflow/overseer/_CONFIG.yaml`

### Blockers

- **B1 (REQ-HYD-003)**: `hydrate()` never called from WASM entry point. `crates/chirp-frontend/src/app.rs::start()` calls `ferric::dom::mount` not `ferric::hydrate`. SSR+hydration is not functional end-to-end.
- **B2 (REQ-SSR-006 / Area E)**: Zero `wasm-bindgen-test` in `hydrate.rs`. Issues #224 and #226 require headless wasm-bindgen-test coverage (adopt walk, event wiring, mismatch detection).

### Context

- ferric-ssr goal: issues #223, #224, #226 (branch `work/ferric-ssr-r1`, PR #228).
- Remediation attempts: 2/2 (ferric-ssr-r2 FAIL CI; ferric-ssr-r3 PASS machine gate).
- Review verdict: REQUEST-CHANGES (2 blockers).
- Budget policy: 2 remediation attempts per goal without escalation.

## Work for this step

### 1. Load governing files

Load `appfiles/RETENTION.md` and `appfiles/BOARD.md`.

### 2. Read the config seam

Read `taskflow/overseer/_CONFIG.yaml`.

### 3. Post escalation comment on PR #228

Post a comment on PR #228 explaining:
- The review returned REQUEST-CHANGES with 2 blockers (B1 and B2 above).
- The remediation budget (2 attempts) is exhausted.
- The user must decide: extend the budget (dispatch a 3rd code DAG to fix B1 and B2) OR defer issues #223/#224/#226 to a later milestone (close PR #228, return to backlog).
- Do NOT name host paths, taskflow internals, or agent/node IDs. Write for the repository's readers.
- Do NOT repeat the full 14 non-blocker list (they're already on the board as issues).

### 4. Record escalation in STATE

Write updated project state at `taskflow/overseer/I267/project_state.json`:
- Add escalation_ferric_ssr_budget_exhausted to escalations (ACTIVE)
- Record escalation comment URL
- Update ferric_ssr_goal board_status to "Blocked (escalation active)"
- Update forward_plan for I268 (bounded watch)

### 5. Update board status for #223, #224, #226

Set issues #223, #224, and #226 on the board to "Blocked" (or leave as Todo with a note — use whatever the board offers that most clearly signals "waiting on owner decision").

### 6. Schedule I268

Schedule I268: bounded watch — suspend until user responds on PR #228 (new comment) OR +10 minutes.

## Notes

- The active ferric-async-forms escalation (PR #193) remains open; do not close or touch it.
- The escalation comment goes on PR #228 (the ferric-ssr PR), not PR #193.
- Write the escalation comment for GitHub readers (no internal paths or node IDs).
