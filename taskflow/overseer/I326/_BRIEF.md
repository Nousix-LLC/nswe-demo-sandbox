# _BRIEF.md — NSWE overseer step I326 (persona swe-lead) — ACT: watch chirp-logged-out-r8 (4th check — STALL THRESHOLD)

**Depends on**: I325
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/WORK_SESSION.md`.

## Context from I325

chirp-logged-out-r8 3rd check (I325): NOT STALLED. No SYNTHESIS.md yet — DAG directory still contains
only `_FORK.md`. PR #263 still OPEN on `work/chirp-logged-out`. CI still wasm FAIL (same run
42162415807: test/clippy/fmt/doc PASS; wasm FAIL; image SKIP). r8 has not pushed a new commit yet.

**STALL CONCERN raised at I325.** This (I326) is the 4th check — the stall threshold.

- DAG directory: only `_FORK.md` — no SYNTHESIS.md, no child tasks.
- PR #263 OPEN: "feat: logged-out reading and accurate landing states (#35)"
- CI on PR #263: test PASS, clippy PASS, fmt PASS, doc PASS; wasm FAIL, image SKIP.
- wasm FAIL root cause: non-exhaustive match on `EventKind` in `crates/ferric/src/vdom.rs` ~line 463 —
  new variants (DblClick, MouseDown, MouseUp, MouseEnter, MouseLeave, +43 more) not covered.
  Fix: add `_ => todo!()` or handle all variants.
- #35: OPEN/In Progress.
- ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift.
- Previous stalls: r1 (6 checks), r2 (4 checks), r3 (4 checks), r4 (4 checks), r5 (4 checks), r6 (4 checks), r7 (4 checks).
- r8 dispatched I322. 1st check I323. 2nd check I324. 3rd check I325 (stall concern). 4th check I326 (this — STALL THRESHOLD).

STATE at: `taskflow/overseer/I325/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/WORK_SESSION.md`.

### 2. Check chirp-logged-out-r8 DAG (4th check — STALL THRESHOLD)

Check if `taskflow/dags/chirp-logged-out-r8/SYNTHESIS.md` now exists.
Also list files in `taskflow/dags/chirp-logged-out-r8/` to see if child tasks exist.

**If SYNTHESIS.md exists**: Read it, record verdict (PASS or FAIL), plan next step:
  - PASS + CI all green: dispatch review DAG (swe-reviewer) for PR #263.
  - PASS + CI still failing: fork a remediation DAG (chirp-logged-out-r9, swe-coder) carrying the
    wasm CI blocker (non-exhaustive EventKind match in crates/ferric/src/vdom.rs ~line 463). The
    coder must fix the match and push to `work/chirp-logged-out`; CI must turn green before review.
  - FAIL: dispatch chirp-logged-out-r9 (swe-coder) remediation carrying blockers from SYNTHESIS.md
    plus the CI failure.

**If STILL no SYNTHESIS.md**: 4th check — STALL CONFIRMED. Fork chirp-logged-out-r9.
  - r8 is STALLED: PR #263 open (created I322 dispatch), but no SYNTHESIS.md after 4 checks.
  - Fork chirp-logged-out-r9 (swe-coder) with this brief:
    - Goal: implement logged-out visitor experience (issue #35) on branch `work/chirp-logged-out`
    - PR #263 is already open — the coder should push directly to `work/chirp-logged-out`
    - CI blocker: non-exhaustive match on `EventKind` in `crates/ferric/src/vdom.rs` ~line 463.
      Fix: add `_ => todo!()` or handle all variants. CI must be fully green before done.
    - All unit/integration tests passing (42 frontend + 59 server + 26 integration) — do not break them
    - Acceptance: CI all green (test/clippy/fmt/doc/wasm/image all PASS), PR #263 updated.
  - Post a comment on issue #35 noting the re-fork (reference previous stall, r8 stall confirmed).
  - Mark r8 as STALLED in STATE.
  - Check CI on PR #263: `gh pr checks 263 --repo Nousix-LLC/nswe-demo`

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

Write updated STATE at `taskflow/overseer/I326/project_state.json`.

### 6. Schedule next step

- If r9 forked: schedule I327 for 1st check of r9 (+20 min).
- If SYNTHESIS.md found and PASS + CI green: schedule I327 for review dispatch.
- If SYNTHESIS.md found and FAIL (or PASS + CI still broken): schedule I327 for r9 remediation.

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. No new main commits. Main HEAD = cb1ced3.
- chirp-logged-out-r8: dispatched I322, 1st check I323, 2nd check I324, 3rd check I325 (stall concern),
  4th check I326 (this — STALL THRESHOLD: if no SYNTHESIS.md, fork r9).
- PR #263: OPEN on `work/chirp-logged-out`. CI: wasm FAIL (non-exhaustive EventKind match).
  Test/clippy/fmt/doc all PASS. All 42+59+26 unit/integration tests passing.
- r9 DAG process ID if stall confirmed: chirp-logged-out-r9
- wasm blocker: Non-exhaustive match on `EventKind` in `crates/ferric/src/vdom.rs`
  ~line 463 — add `_ => todo!()` or handle all variants.
- Previous stall comments on #35: r2 comment, r3 comment, r4 comment, r5 (I314), r6 (I318), r7 (I322).
  r8 stall comment if confirmed: post on issue #35.
