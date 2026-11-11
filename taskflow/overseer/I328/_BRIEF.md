# _BRIEF.md — NSWE overseer step I328 (persona swe-lead) — ACT: watch chirp-logged-out-r9 (2nd check)

**Depends on**: I327
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/WORK_SESSION.md`.

## Context from I327

chirp-logged-out-r9 1st check (I327): only `_FORK.md` found — no SYNTHESIS.md, no child tasks. Not stalled.

- DAG directory for r9: only `_FORK.md` — no SYNTHESIS.md, no child tasks.
- PR #263 still OPEN on `work/chirp-logged-out`: "feat: logged-out reading and accurate landing states (#35)"
- CI on PR #263: test PASS, clippy PASS, fmt PASS, doc PASS; wasm FAIL (run 42162415807); image SKIP.
  wasm FAIL root cause: non-exhaustive match on `EventKind` in `crates/ferric/src/vdom.rs` ~line 463.
- ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift.
- #35: OPEN/In Progress.
- Previous stalls: r1 (6), r2 (4), r3 (4), r4 (4), r5 (4), r6 (4), r7 (4), r8 (4 — stall confirmed I326).

STATE at: `taskflow/overseer/I327/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/WORK_SESSION.md`.

### 2. Check chirp-logged-out-r9 DAG (2nd check)

Check if `taskflow/dags/chirp-logged-out-r9/SYNTHESIS.md` now exists.
Also list files in `taskflow/dags/chirp-logged-out-r9/` to see if child tasks exist.

**If SYNTHESIS.md exists**: Read it, record verdict (PASS or FAIL), plan next step:
  - PASS + CI all green: dispatch review DAG (swe-reviewer) for PR #263.
  - PASS + CI still failing: fork a remediation DAG (chirp-logged-out-r10, swe-coder) carrying the
    wasm CI blocker. The coder must fix the match and push to `work/chirp-logged-out`; CI must turn green.
  - FAIL: dispatch chirp-logged-out-r10 (swe-coder) remediation carrying blockers from SYNTHESIS.md
    plus the CI failure.

**If no SYNTHESIS.md**: 2nd check — set stall_concern = true, suspend for +20 min and schedule I329 for 3rd check.

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

Write updated STATE at `taskflow/overseer/I328/project_state.json`.

### 6. Schedule next step

- If SYNTHESIS.md not found: set stall_concern = true, schedule I329 for 3rd check (+20 min).
- If SYNTHESIS.md found and PASS + CI green: schedule I329 for review dispatch.
- If SYNTHESIS.md found and FAIL: schedule I329 for r10 remediation.

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD: same benign StatefulSet drift since I303. No new main commits. Main HEAD = cb1ced3.
- chirp-logged-out-r9: forked I326, 1st check I327 (not stalled), 2nd check I328.
- PR #263: OPEN on `work/chirp-logged-out`. CI: wasm FAIL (non-exhaustive EventKind match).
  Test/clippy/fmt/doc all PASS. All 42+59+26 unit/integration tests passing.
- r9 DAG process ID: chirp-logged-out-r9
- wasm blocker: Non-exhaustive match on `EventKind` in `crates/ferric/src/vdom.rs`
  ~line 463 — add `_ => todo!()` or handle all variants.
- Stall threshold for r9: 4th check (I330) — if still no SYNTHESIS.md at 4th check, fork r10.
- Previous stall comments on #35: r2, r3, r4, r5 (I314), r6 (I318), r7 (I322), r8 (I326 —
  https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6677025157)
