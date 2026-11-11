# _BRIEF.md — NSWE overseer step I222 (persona swe-lead) — ACT: launch ferric-router-r3

**Depends on**: I221
**Task Kind**: act — load `WORK_SESSION` + `DELIVERABLES_GIT`. Write brief and fork ferric-router-r3.

## Context from I221 (board check / ferric-router-r2 fold-read, 2026-11-03)

- **ferric-router-r2 HAS FOLDED** — SYNTHESIS.md confirmed.
  - Deliverables verdict: PASS. PR #202 (work/ferric-router-r2) clean router-only 3 cherry-pick commits (c03818f, 9c9fdd8, 3404dea). Macros scope NIL DIFF (already on main via PR #188).
  - **Machine gate: FAIL** — CI run 41786452070: clippy FAILURE. Error: `unused import: VNode` in `crates/ferric-router` test code (`-D unused-imports` implied by `-D warnings`). fmt/test/wasm/doc SUCCESS. image SKIPPED.
  - Remediation budget: attempt 1 of 2 used → ferric-router-r3 is attempt **2/2** (last attempt).
  - PR #202: OPEN/MERGEABLE. Issues: #131, #146, #147.
  - PR #192: OPEN (superseded by PR #202; to be closed when PR #203 merges).
- **ferric-async-forms escalation**: ACTIVE, no user response yet. Hold.
- **Free DAG slots**: 3.
- **Config**: delegated/auto_land/headless.
- **STATE**: `taskflow/overseer/I221/project_state.json`.
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/DELIVERABLES_GIT.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I221/project_state.json`.

### 2. Confirm slot availability
Free DAG slots = 3 → one slot available for ferric-router-r3. Proceed.

### 3. Write ferric-router-r3 brief
Write `taskflow/dags/ferric-router-r3/_BRIEF.md`.

**Goal**: Fix the clippy `unused import: VNode` error in `crates/ferric-router` test code. Build on the work from ferric-router-r2 (the clean 3-commit router-only branch), producing a fresh branch `work/ferric-router-r3` and a new PR that supersedes PR #202. All 6 CI checks must PASS.

**Key lesson to carry forward**:
- ferric-router-r2 (PR #202, branch work/ferric-router-r2) had its CI fail at clippy: `unused import: VNode` in `crates/ferric-router` test code. The error is in the ferric-router crate's test section — `VNode` is imported but not used in a test. The fix is minimal: remove the unused import. All other CI checks (fmt, test, wasm, doc) pass.
- Branch `work/ferric-router-r2` has the 3 clean cherry-pick commits: c03818f, 9c9fdd8, 3404dea. These are the same router commits cherry-picked onto the current main (aa24687). Macros scope is NIL DIFF (already on main via PR #188).
- Do NOT re-introduce macros/context scope. Router-only: `crates/ferric-router/` only.

**Inputs**:
- Repository: Nousix-LLC/nswe-demo
- Branch to build on: `work/ferric-router-r2` (3 cherry-pick commits: c03818f, 9c9fdd8, 3404dea — router-only scope, `crates/ferric-router/` files only)
- Failing CI run: 41786452070, clippy job: `unused import: VNode` in `crates/ferric-router` test code
- PR #202 (open, to be superseded)
- Issues: #131 (navigate_replace — REQ-RT-003), #146 (active-route awareness — REQ-RT-005/006), #147 (nested routes — REQ-RT-004)
- Design: `design/ferric/router-and-http.md` Part 1 (REQ-RT-001..008) — the same design as ferric-router-r1/r2

**Declared output**:
- Branch `work/ferric-router-r3` on Nousix-LLC/nswe-demo with the same 3 router commits plus the clippy fix
- PR #203 (new PR) closing #131, #146, #147 — supersedes PR #202
- All 6 CI checks PASS (fmt, clippy, test, wasm, doc, image or image SKIPPED on non-image branch)
- Root `SYNTHESIS.md` accounting for all 3 issues and the CI result

**Concerns to evaluate**:
1. **CI fix completeness**: The clippy error `unused import: VNode` is removed and all 6 CI checks pass. No new clippy warnings introduced.
2. **Scope integrity**: Branch diff remains router-only (`crates/ferric-router/` only). Zero ferric-macros or other crate files in the diff vs main.
3. **Issue coverage**: All 3 issues (#131, #146, #147) covered. PR body closes them correctly.
4. **Correctness of the router code**: The underlying router implementation (REQ-RT-001..008) is functionally correct. The fix is minimal and does not regress any test.

**Constraints**:
- Branch must be `work/ferric-router-r3`; do NOT force-push to `work/ferric-router-r2`.
- Do NOT close PR #202 manually; it will be superseded by PR #203.
- Router-only scope: no changes outside `crates/ferric-router/`.
- No force-push to any existing branch.
- Remediation budget: this is attempt 2 of 2 (the final attempt). If CI cannot be made green, report clearly in SYNTHESIS.md what blocks remain.

### 4. Fork ferric-router-r3

Write `taskflow/dags/ferric-router-r3/_FORK.md` and fork with `launch_agent: swe-coder`.

### 5. Update project STATE

Write `taskflow/overseer/I222/project_state.json`:
- `current_pointer`: overseer/I222
- Add ferric-router-r3 to `dags_in_flight`
- Update PR #202: add `superseded_by_pr: TBD (PR #203 when opened)`
- Update PR #202 remediation note: `remediation_dag_r3: ferric-router-r3`
- `free_dag_slots`: 3 → 2
- Carry all other state from I221

### 6. Record forward_series entry for I222

Summarize in `forward_series.I222`.

## Notes

- Config: delegated/auto_land/headless.
- This is remediation attempt 2/2 for ferric-router. If this fails, escalate to user with both attempt details.
- The escalation for ferric-async-forms (#130) is still active; do not launch ferric-async-forms-r3 without user decision.
- After forking ferric-router-r3, schedule I223 (EVALUATE: board check / watch ferric-router-r3 fold).
