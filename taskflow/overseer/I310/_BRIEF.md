# _BRIEF.md — NSWE overseer step I310 (persona swe-lead) — ACT: watch chirp-logged-out-r4 (4th check — stall CONFIRMATION threshold)

**Depends on**: I309
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I309

chirp-logged-out-r4 3rd check (I309): still only _FORK.md — no child tasks, no SYNTHESIS.md. 3rd check — STALL CONCERN noted. `stall_concern: true` set in STATE.
ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift only. #35 still In Progress.
No PR on work/chirp-logged-out (expected — r4 hasn't pushed yet).

STATE at: `taskflow/overseer/I309/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Stall schedule for chirp-logged-out-r4

- DAG process: proc-770f650d-3782-4eff-b33e-d8ca8b09f602
- 1st check (I307): only _FORK.md — no concern.
- 2nd check (I308): only _FORK.md — no concern.
- 3rd check (I309): only _FORK.md — **stall concern noted** (`stall_concern: true`).
- **4th check (I310 — this iteration): stall CONFIRMATION threshold** → re-fork as r5 if still no child tasks.
- Previous stalls: chirp-logged-out (I298, 6 checks), r2 (I302, 4 checks), r3 (I306, 4 checks).

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r4 DAG (4th check — stall CONFIRMATION)

Check if `taskflow/dags/chirp-logged-out-r4/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r4/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r5 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**Stall detection (4th check — CONFIRMATION threshold)**:
  - If child tasks appeared → DAG progressing, clear stall concern, re-suspend for I311 (+20 min).
  - If SYNTHESIS.md appeared → act on verdict (above).
  - If no child tasks → **stall CONFIRMED** (4th check threshold reached):
    - Move r4 from `dags_in_flight` to `dags_stalled` in STATE.
    - **Re-fork as chirp-logged-out-r5** (swe-coder), carrying the same goal and acceptance criteria
      from the r4 brief (`taskflow/dags/chirp-logged-out-r4/_BRIEF.md`). Do NOT carry child state from r4
      (there is none). The r5 brief is a fresh brief with the same goal.
    - Post a comment on issue #35 noting the stall and the r5 re-fork attempt.
    - Schedule I311 to watch chirp-logged-out-r5 (1st check — no concern).

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If OutOfSync only on chirp-postgres StatefulSet: same benign drift as before — note and continue.
- If new resources OutOfSync: investigate.
- If Synced+Healthy on cb1ced3: record as fully synced.

### 4. Board spot-check

- Confirm #35 still In Progress.
- Check if any new PR appeared on `work/chirp-logged-out`: `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`
- If re-forking as r5, update #35 board comment with the stall note.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I310/project_state.json`.

### 6. Proceed

- If SYNTHESIS.md found and PASS: dispatch review DAG (swe-reviewer) and schedule I311 watching the review.
- If SYNTHESIS.md found and FAIL: dispatch chirp-logged-out-r5 remediation DAG and schedule I311 watching it.
- If child tasks appeared (DAG in progress, 4th check): clear stall concern, re-suspend for I311 (+20 min).
- If no child tasks (4th check — stall CONFIRMED): re-fork as chirp-logged-out-r5, post comment on #35, schedule I311 watching r5 (1st check — no concern, +20 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r4 was dispatched I306. 4th check in I310 (1st: I307 no concern, 2nd: I308 no concern,
  3rd: I309 stall concern noted).
- Stall schedule: concern at 3rd check (I309 — DONE); CONFIRMATION at 4th check (I310 — this iteration) → re-fork as r5 if still no child tasks.
- Previous stalls: chirp-logged-out (I298, 6 checks), r2 (I302, 4 checks), r3 (I306, 4 checks).
- r4 DAG process ID: proc-770f650d-3782-4eff-b33e-d8ca8b09f602
- If re-forking as r5: read the goal from r4's brief at `taskflow/dags/chirp-logged-out-r4/_BRIEF.md`
  to carry the acceptance criteria forward. Issue #35 is the target. Branch: work/chirp-logged-out.
