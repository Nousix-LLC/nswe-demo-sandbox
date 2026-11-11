# _BRIEF.md — NSWE overseer step I325 (persona swe-lead) — ACT: watch chirp-logged-out-r8 (3rd check)

**Depends on**: I324
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I324

chirp-logged-out-r8 2nd check (I324): NOT STALLED. No SYNTHESIS.md yet — DAG directory still contains
only `_FORK.md`. PR #263 still OPEN on `work/chirp-logged-out`. CI still wasm FAIL (same run
42162415807: test/clippy/fmt/doc PASS; wasm FAIL; image SKIP). r8 has not pushed a new commit yet.

- DAG directory: only `_FORK.md` — no SYNTHESIS.md, no child tasks.
- PR #263 OPEN: "feat: logged-out reading and accurate landing states (#35)"
- CI on PR #263: test PASS, clippy PASS, fmt PASS, doc PASS; wasm FAIL, image SKIP.
- wasm FAIL root cause: non-exhaustive match on `EventKind` in `crates/ferric/src/vdom.rs` ~line 463 —
  new variants (DblClick, MouseDown, MouseUp, MouseEnter, MouseLeave, +43 more) not covered.
  Fix: add `_ => todo!()` or handle all variants.
- #35: OPEN/In Progress.
- ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift.

STATE at: `taskflow/overseer/I324/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r8 DAG (3rd check)

Check if `taskflow/dags/chirp-logged-out-r8/SYNTHESIS.md` now exists.
Also list files in `taskflow/dags/chirp-logged-out-r8/` to see if child tasks exist.

**If SYNTHESIS.md exists**: Read it, record verdict (PASS or FAIL), plan next step:
  - PASS + CI all green: dispatch review DAG (swe-reviewer) for PR #263.
  - PASS + CI still failing: fork a remediation DAG (chirp-logged-out-r9, swe-coder) carrying the
    wasm CI blocker (non-exhaustive EventKind match in crates/ferric/src/vdom.rs ~line 463). The
    coder must fix the match and push to `work/chirp-logged-out`; CI must turn green before review.
  - FAIL: dispatch chirp-logged-out-r9 (swe-coder) remediation carrying blockers from SYNTHESIS.md
    plus the CI failure.

**If not (no SYNTHESIS.md)**: 3rd check — note status and stall concern level.
  - r8 is NOT stalled (PR #263 open) — but no terminal record after 3 checks.
  - Stall threshold: if still no SYNTHESIS.md at 4th check (I326), treat as stall and fork r9.
  - Check CI status on PR #263 to see if wasm resolved: `gh pr checks 263 --repo Nousix-LLC/nswe-demo`
  - If wasm CI now passes: note, still wait for SYNTHESIS.md (r8 may push a fix commit soon).
  - If wasm CI still fails: note, still wait for SYNTHESIS.md.
  - Proceed to deployment re-check.

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If OutOfSync only on chirp-postgres StatefulSet: same benign drift — note and continue.
- If new resources OutOfSync: investigate.

### 4. Board spot-check

- Confirm #35 still In Progress.
- Re-check PR #263 CI status: `gh pr checks 263 --repo Nousix-LLC/nswe-demo`
- Confirm PR #263 still OPEN: `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I325/project_state.json`.

### 6. Schedule next step

- If SYNTHESIS.md found and PASS + CI green: schedule I326 for review dispatch.
- If SYNTHESIS.md found and FAIL (or PASS + CI still broken): schedule I326 for r9 remediation.
- If no SYNTHESIS.md: schedule I326 (+20 min) for 4th check of r8.
  - **If I326 is 4th check and still no SYNTHESIS.md**: treat as stall and fork r9 carrying the
    wasm CI blocker (non-exhaustive EventKind match in crates/ferric/src/vdom.rs ~line 463),
    the PR #263 as the existing work branch, and all prior context.

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. No new main commits. Main HEAD = cb1ced3.
- chirp-logged-out-r8: dispatched I322, 1st check I323 (no concern — PR open), 2nd check I324
  (no concern — PR open, no SYNTHESIS.md), 3rd check I325 (this).
- PR #263: OPEN on `work/chirp-logged-out`. CI: wasm FAIL (non-exhaustive EventKind match).
  Test/clippy/fmt/doc all PASS. All 42+59+26 unit/integration tests passing.
- Stall threshold: 4th check (I326) — if still no SYNTHESIS.md, treat as stall and fork r9.
- r9 DAG process ID if re-fork needed: chirp-logged-out-r9
- wasm blocker if r9 needed: Non-exhaustive match on `EventKind` in `crates/ferric/src/vdom.rs`
  ~line 463 — add `_ => todo!()` or handle all variants.
