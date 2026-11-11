# _BRIEF.md — NSWE overseer step I218 (persona swe-lead) — ACT: launch router remediation

**Depends on**: I217
**Task Kind**: act — load `WORK_SESSION` + `DELIVERABLES_GIT`. Launch remediation DAG for PR #192 (router PR split).

## Context from I217

review-ferric-router-r1 folded REQUEST CHANGES:
- B1: PR #192 bundles ~3,290 lines of undescribed scope (ferric-macros crate + context-API, targeting issues #137-#142) alongside the 4 router commits (#131/#146/#147).
- Path forward (per reviewer): split the PR. The 4 router commits (`89687da7`, `cab18b9d`, `3868b2c8`, `2bf76698`) close #131/#146/#147 and can be approved in isolation.
- Review was posted on PR #192: https://github.com/Nousix-LLC/nswe-demo/pull/192#issuecomment-6623982987
- Non-blockers on board: #194, #195, #178.
- STATE: `taskflow/overseer/I217/project_state.json`.
- Config seam: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I217/project_state.json`.

### 2. Check DAG slots
free_dag_slots should be 3 at I217. After launching this DAG: 2. Verify there is a free slot.

### 3. Write the brief for the router remediation DAG
Write `taskflow/dags/ferric-router-r2/_BRIEF.md`.

**Objective**: Split PR #192 so that only the 4 router commits (`89687da7`, `cab18b9d`, `3868b2c8`, `2bf76698`) remain on a clean branch `work/ferric-router-r2`, and open a new PR closing #131/#146/#147. The ferric-macros and context-API commits should NOT be part of this PR — close PR #192 and open the new clean PR.

**What to implement**:
- Create branch `work/ferric-router-r2` from `main`
- Cherry-pick the 4 router commits: `89687da7`, `cab18b9d`, `3868b2c8`, `2bf76698` (in order)
- Verify all 6 CI checks pass on the new branch
- Close PR #192 (with a note referencing the new PR)
- Open a new PR on `work/ferric-router-r2` → `main` closing #131, #146, #147
- Root `SYNTHESIS.md` accounting for all 3 issues (#131/#146/#147), verdict PASS or FAIL

**Acceptance criteria** (from issues #131, #146, #147):
- #131 (Ferric Router epic — usable_early): nested route matching with `Router::nest`, per-level fallbacks, `outlet()` ordering, flat-route regression preserved
- #146 (Core routing): all core routing behaviors including navigate, nested routes, route params, fallback routes
- #147 (Active-route awareness): `Link::build()` with aria-current dynamic toggle on active route

**What is NOT in scope**: The ferric-macros crate and context-API changes (commits for #137-#142). Those are already landed via PR #188 or should be tracked separately. This PR is strictly the 4 router-only commits.

**Inputs**:
- Repository: `Nousix-LLC/nswe-demo`
- Working branch: `work/ferric-router-r2` (new, based on main)
- Prior review SYNTHESIS: `taskflow/dags/review-ferric-router-r1/SYNTHESIS.md` (B1 is the only blocker; all 6 concerns PASS for the router scope)
- The 4 router commits to cherry-pick: `89687da7`, `cab18b9d`, `3868b2c8`, `2bf76698`
- PR #192 to close: https://github.com/Nousix-LLC/nswe-demo/pull/192

**Declared output**:
- Branch `work/ferric-router-r2` with clean 4-commit history
- PR #192 closed
- New PR opened on `work/ferric-router-r2` → `main` closing #131/#146/#147
- CI passes (all 6 checks green) on the new PR
- `SYNTHESIS.md` accounting for #131/#146/#147, verdict PASS or FAIL

**Concerns**:
- Design correctness: all 3 acceptance criteria met (REQ-RT-001..008 from design/ferric/router-and-http.md Part 1) — same as the original ferric-router-r1 brief
- CI: all 6 checks (fmt, clippy, test, wasm, doc, image) must PASS in Nousix-LLC/nswe-demo
- Branch cleanliness: only the 4 router commits present; no ferric-macros or context-API commits in the diff

**Constraints**: Repo Nousix-LLC/nswe-demo only. No force-push. Working branch work/ferric-router-r2.

### 4. Write _FORK.md and fork the DAG
Launch `ferric-router-r2` as swe-coder.

### 5. Update STATE
- ferric-router-r2 added to dags_in_flight
- free_dag_slots: 3 → 2
- Write `taskflow/overseer/I218/project_state.json`

## Notes

- Config: delegated/auto_land/headless.
- Remediation budget: this is first remediation attempt for the router goal (review REQUEST CHANGES on first review).
- The ferric-macros work in PR #192 that was not part of the router brief is a separate concern. If it's new code (beyond what PR #188 already landed), it may need its own epic and PR. The process-review step (I217) should note this. The router remediation DAG's job is strictly the PR split.
