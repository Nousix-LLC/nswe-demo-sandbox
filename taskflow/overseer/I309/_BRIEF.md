# _BRIEF.md — NSWE overseer step I309 (persona swe-lead) — ACT: watch chirp-logged-out-r4 (3rd check — stall concern threshold)

**Depends on**: I308
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I308

chirp-logged-out-r4 2nd check (I308): still only _FORK.md — no child tasks, no SYNTHESIS.md. 2nd check — no concern.
ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift only. #35 still In Progress.
No PR on work/chirp-logged-out (expected — r4 hasn't pushed yet).

STATE at: `taskflow/overseer/I308/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Stall schedule for chirp-logged-out-r4

- DAG process: proc-770f650d-3782-4eff-b33e-d8ca8b09f602
- 1st check (I307): only _FORK.md — no concern.
- 2nd check (I308): only _FORK.md — no concern.
- **3rd check (I309): stall concern threshold** — if still no child tasks, note stall concern.
- 4th check (I310): stall confirmation threshold → re-fork as r5 if still no child tasks.
- Previous stalls: chirp-logged-out (I298, 6 checks), r2 (I302, 4 checks), r3 (I306, 4 checks).

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r4 DAG (3rd check — stall concern)

Check if `taskflow/dags/chirp-logged-out-r4/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r4/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r5 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**Stall detection (3rd check — concern threshold)**:
  - If child tasks appeared → DAG progressing, re-suspend for I310 (+20 min), clear stall concern.
  - If SYNTHESIS.md appeared → act on verdict (above).
  - If no child tasks → **note stall concern** (3rd check threshold reached), re-suspend for I310 (+20 min).
    - Set `stall_concern: true` in STATE.
    - 4th check (I310) is confirmation threshold → re-fork as r5.

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If OutOfSync only on chirp-postgres StatefulSet: same benign drift as before — note and continue.
- If new resources OutOfSync: investigate.
- If Synced+Healthy on cb1ced3: record as fully synced.

### 4. Board spot-check

- Confirm #35 still In Progress.
- Check if any new PR appeared on `work/chirp-logged-out`: `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I309/project_state.json`.

### 6. Proceed

- If SYNTHESIS.md found and PASS: dispatch review DAG (swe-reviewer) and schedule I310 watching the review.
- If SYNTHESIS.md found and FAIL: dispatch chirp-logged-out-r5 remediation DAG and schedule I310 watching it.
- If child tasks appeared (DAG in progress, 3rd check): clear stall concern, re-suspend for I310 (+20 min).
- If no child tasks (3rd check — stall concern): note concern in STATE, re-suspend for I310 (+20 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r4 was dispatched I306. 3rd check in I309 (1st: I307 no concern, 2nd: I308 no concern).
- Stall schedule: concern at 3rd check (I309 — this iteration); confirmation at 4th check (I310) → re-fork as r5 if still no child tasks.
- Previous stalls: chirp-logged-out (I298, 6 checks), r2 (I302, 4 checks), r3 (I306, 4 checks).
- r4 DAG process ID: proc-770f650d-3782-4eff-b33e-d8ca8b09f602
