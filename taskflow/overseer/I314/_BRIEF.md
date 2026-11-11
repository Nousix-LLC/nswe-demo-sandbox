# _BRIEF.md — NSWE overseer step I314 (persona swe-lead) — ACT: watch chirp-logged-out-r5 (4th check — STALL CONFIRMATION THRESHOLD)

**Depends on**: I313
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I313

chirp-logged-out-r5 3rd check (I313): only _FORK.md — no child tasks, no SYNTHESIS.md. **STALL CONCERN THRESHOLD reached. stall_concern: true.**
- ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift only. No change.
- #35 confirmed OPEN/In Progress.
- No PR on work/chirp-logged-out (expected — r5 stalled).

STATE at: `taskflow/overseer/I313/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Stall schedule for chirp-logged-out-r5

- DAG process: chirp-logged-out-r5 (dag_process_id in STATE)
- 1st check (I311): no concern — only _FORK.md, expected.
- 2nd check (I312): no concern — only _FORK.md, expected.
- 3rd check (I313): **STALL CONCERN** — only _FORK.md. stall_concern: true.
- **4th check (I314 — this iteration): STALL CONFIRMATION THRESHOLD → re-fork as r6 if still no child tasks.**

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r5 DAG (4th check — stall CONFIRMATION threshold)

Check if `taskflow/dags/chirp-logged-out-r5/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r5/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r6 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**4th check — STALL CONFIRMATION THRESHOLD**: If still only _FORK.md (no child tasks, no SYNTHESIS.md), this
is now a **confirmed stall**. Re-fork as chirp-logged-out-r6:
  1. Read `taskflow/dags/chirp-logged-out-r5/_FORK.md` for the goal and acceptance criteria.
  2. Create `taskflow/dags/chirp-logged-out-r6/` directory.
  3. Write `taskflow/dags/chirp-logged-out-r6/_FORK.md` as a fresh swe-coder brief carrying the goal
     from r5 (issue #35, branch work/chirp-logged-out) with the stall context added.
  4. Fork chirp-logged-out-r6 via `mcp__hal__fork` as swe-coder.
  5. Post a comment on issue #35 noting the re-fork (r5 confirmed stalled, launching r6).
  6. Move chirp-logged-out-r5 from dags_in_flight to dags_stalled in STATE.
  7. Add chirp-logged-out-r6 to dags_in_flight in STATE.
  8. Schedule I315 to watch chirp-logged-out-r6 (1st check, +20 min).

If child tasks DID appear (DAG has decomposed and is working): no stall confirmed — just record
stall_concern: false, note DAG is progressing, and schedule I315 (+20 min) to continue watching.

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If OutOfSync only on chirp-postgres StatefulSet: same benign drift as before — note and continue.
- If new resources OutOfSync: investigate.
- If Synced+Healthy on cb1ced3: record as fully synced.

### 4. Board spot-check

- Confirm #35 still In Progress.
- Check if any PR appeared on `work/chirp-logged-out`: `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I314/project_state.json`.

### 6. Proceed

- If SYNTHESIS.md found and PASS: dispatch review DAG (swe-reviewer) and schedule I315 watching the review.
- If SYNTHESIS.md found and FAIL: dispatch chirp-logged-out-r6 remediation DAG and schedule I315 watching it.
- If child tasks appeared (DAG progressing): schedule I315 (+20 min), note stall_concern: false.
- If confirmed stall (4th check, still only _FORK.md): re-fork as chirp-logged-out-r6 (see step 2 above),
  schedule I315 (+20 min) watching r6 (1st check).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r5 was dispatched I310. 1st check I311 (no concern). 2nd check I312 (no concern). 3rd check I313 (stall concern). 4th check I314 (this — STALL CONFIRMATION).
- Stall schedule: concern at 3rd check (I313); **CONFIRMATION at 4th check (I314 — this) → re-fork as r6 if still no child tasks.**
- Previous stalls: chirp-logged-out (I298, 6 checks), r2 (I302, 4 checks), r3 (I306, 4 checks), r4 (I310, 4 checks).
- r5 DAG process ID: chirp-logged-out-r5 (read from STATE)
- When re-forking as r6: read the goal from r5's brief at `taskflow/dags/chirp-logged-out-r5/_FORK.md`
  to carry the acceptance criteria forward. Issue #35 is the target. Branch: work/chirp-logged-out.
