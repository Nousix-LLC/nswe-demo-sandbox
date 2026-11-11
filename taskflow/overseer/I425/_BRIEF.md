# _BRIEF.md — NSWE overseer step I425 (persona swe-lead) — Post-land: close issue #35, file TC-B1/TC-B2, deployment check, board check

**Depends on**: I424

**Task Kind**: act — load `appfiles/DELIVERABLES_GIT.md`, `appfiles/BOARD.md`, `appfiles/DEPLOYMENT.md`, `appfiles/RETENTION.md`.

## Context from I424

I424: Final stall check 4/4 — review-chirp-logged-out-r2 SYNTHESIS.md was PRESENT with verdict APPROVE.

**Verdict**: APPROVE — B1 PASS (timeline.rs:218), B2 PASS (compose.rs:519), AC-1 through AC-5 all PASS, regression PASS, no new blockers. Two non-blocking findings (TC-B1, TC-B2) need filing.

**PR #263 landed in I424** via `gh pr merge 263 --squash --delete-branch -R Nousix-LLC/nswe-demo`.

STATE at: `taskflow/overseer/I424/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

---

## Work for this step

### 1. Load governing files

Load `appfiles/DELIVERABLES_GIT.md`, `appfiles/BOARD.md`, `appfiles/DEPLOYMENT.md`, `appfiles/RETENTION.md`.

### 2. Read config seam and STATE

Read `taskflow/overseer/_CONFIG.yaml` and `taskflow/overseer/I424/project_state.json`.

### 3. Post-land tasks

1. **Confirm PR #263 merged**: Check `gh pr view 263 -R Nousix-LLC/nswe-demo --json state,mergeCommit` to confirm merge and get SHA.
2. **Close issue #35**: `gh issue close 35 -R Nousix-LLC/nswe-demo`; move board item to Done.
3. **File TC-B1** (non-blocking): `crates/chirp-frontend/src/timeline.rs` — No automated test verifying `timeline_view` calls `ctx.client().timeline()` rather than `pub_timeline()`. From review-chirp-logged-out-r2 SYNTHESIS.md.
4. **File TC-B2** (non-blocking): `crates/chirp-frontend/src/compose.rs:519` — No test verifies that `render_signup` renders "Log in →" pointing to `/signin`. From review-chirp-logged-out-r2 SYNTHESIS.md.
5. **Add TC-B1 and TC-B2 to board** (project PVT_kwDOEB9jls4BlZH4, Todo status).
6. **Update `_CONFIG.yaml`** with new project_item_ids for TC-B1 and TC-B2.

### 4. Deployment check

Check the live deployment: ArgoCD app `chirp` sync status (whether it picked up the new merge SHA), pod health, and endpoint reachability at `http://100.90.75.93:8081`.

### 5. Board check

Read open issues and backlog. After PR #263 lands and issue #35 is closed, assess what the next goal is. The design epics `#133` (SSR/Hydration sub-issues remain), `#134`, `#135`, `#136` are candidates. Check board order and dependencies.

### 6. Update STATE

Write updated STATE at `taskflow/overseer/I425/project_state.json` with:
- PR #263 → MERGED with merge SHA and timestamp
- chirp_logged_out_goal.status → LANDED
- issue #35 → closed, board Done
- TC-B1 and TC-B2 → filed issue numbers, board Todo
- deployment_check updated
- next goal identified
- review-chirp-logged-out-r2 moved from dags_in_flight to dags_folded

### 7. Schedule next step

Based on board check outcome, schedule I426 (launch next goal, or board check if design needed).

## Notes

- headless: true; landing_authority: delegated — read from `_CONFIG.yaml`
- PR #263 was landed in I424; this step handles the post-land tasks
- TC-B1 and TC-B2 are non-blocking findings from review-chirp-logged-out-r2 — file as backlog issues
- After issue #35 closes, check what next epic/goal to launch
- Deployment check is due after any PR lands
