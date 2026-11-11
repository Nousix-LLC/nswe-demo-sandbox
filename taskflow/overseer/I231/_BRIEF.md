# _BRIEF.md — NSWE overseer step I231 (persona swe-lead) — EVALUATE: board check / next code goal #132 HTTP Client

**Depends on**: I230
**Task Kind**: evaluate — load `appfiles/WORK_SESSION.md` + `appfiles/BOARD.md`. Check board state and decide next code goal.

## Context from I230 (ACT: chirp-server digest update — reconstructed)

- **Deployment**: LIVE_AND_CURRENT. PR #209 merged at 2026-11-04T09:52:49Z (merge commit f481a5ee).
  - chirp-server pod running sha256:f845ca8c (d8230fea build — includes PRs #182/#183/#188/#203)
  - ArgoCD operation Succeeded at f481a5ee. Endpoint HTTP 200. 
  - Issues #206/#208 closed and Done on board.
- **Escalation**: ferric-async-forms (#193) budget exhausted — STILL ACTIVE. No user response as of I230 reconstruction. Do NOT launch ferric-async-forms-r3.
- **Free DAG slots**: 4 (all slots open)
- **main_sha**: f481a5eebddb1322d60d18b349c5190aa7318493
- **STATE**: `taskflow/overseer/I230/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I230/project_state.json`.

### 2. Board check
Check GitHub project board, open issues, and open PRs for:
- Any new issues or comments since I230 (especially on PR #193 escalation — has the user responded?)
- Board hygiene: issues #206/#208 should be Done ✓, issue #209 board item (if present) should be Done ✓
- Any new issues that need intake

### 3. Decide next code goal
Per WORK_SESSION.md priority order: finish before starting, then delivery (deployment just verified), then new work.

**Deployment**: Just verified LIVE_AND_CURRENT in I230 — no deployment action needed.

**Next code epic**: #132 (HTTP Client — Ferric 1.0 http client, usable_early)
- Depends on #131 (LANDED ✓ — PR #203, d8230fea) and #129 (LANDED ✓ — PR #188, aa24687)
- Both dependencies met. Epic #132 is ready.
- Sub-issues to cover: check board for open sub-issues under epic #132 (expected from design: REQ-HTTP-* requirements from the ferric 1.0 design)

**Check issue #179** (open: "Chore: note cross-epic dependency on issue #159 in epic issue #132") — this is a type:chore board item. Determine if it should be incorporated into the #132 goal brief or closed as covered.

**Escalation check**: Has the user responded to the ferric-async-forms escalation on PR #193? Check the PR comments.
- If YES: determine action per their response (extend budget → launch ferric-async-forms-r3, or defer → close PR #193 and move #130 to later milestone)
- If NO: escalation remains ACTIVE, do NOT launch ferric-async-forms-r3

### 4. Schedule action
If #132 is ready and no higher priority items block it:
- Schedule I232 ACT: launch code DAG for #132 (HTTP Client, swe-coder)
- The brief for I232 should include:
  - Goal: Ferric 1.0 — HTTP Client (epic #132, usable_early): fetch/JSON HTTP client, async integration, request lifecycle
  - Issues: #132 and all open sub-issues (check board for the REQ-HTTP-* sub-issues filed under #132)
  - Branch: work/ferric-http-r1
  - Inputs: ferric 1.0 design (design/ferric/ on main, especially the HTTP client spec), crates/ferric on main (foundation #129 and router #131 landed), crates/chirp-server and crates/chirp-frontend for integration context
  - Acceptance criteria per issue #132 and its sub-issues

## Notes
- Config: delegated/auto_land/headless
- Do NOT launch ferric-async-forms-r3 — escalation ACTIVE unless user responds
- Issue #179 (cross-epic dependency note) is a type:chore — assess whether it should be closed or included in the #132 goal
- After deciding next goal, schedule I232 ACT launch, then resume the loop with a bounded wake (5–10 min)
