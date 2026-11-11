# _BRIEF.md — NSWE overseer step I307 (persona swe-lead) — ACT: watch chirp-logged-out-r4 (1st check)

**Depends on**: I306
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I306

chirp-logged-out-r3 stall CONFIRMED at 4th check (I306): only _BRIEF.md and _FORK.md, no child tasks.
Re-forked as chirp-logged-out-r4 (swe-coder) in I306. Comment posted on issue #35.
ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift only. #35 still In Progress.

STATE at: `taskflow/overseer/I306/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r4 DAG (1st check)

Check if `taskflow/dags/chirp-logged-out-r4/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r4/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r5 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**Stall detection**: r4 was dispatched in I306; this is the 1st check.
- 1st check (I307): note state; no concern.
- Stall concern threshold: 3rd check (I309).
- Stall confirmation threshold: 4th check (I310) → re-fork as r5 if still no child tasks.

**On stall detection (1st check)**:
  - If child tasks appeared → DAG progressing, re-suspend for I308 (+20 min).
  - If SYNTHESIS.md appeared → act on verdict (above).
  - If no child tasks → note state (1st check: no concern), re-suspend for I308 (+20 min).

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

Write updated STATE at `taskflow/overseer/I307/project_state.json`.

### 6. Proceed

- If SYNTHESIS.md found and PASS: dispatch review DAG (swe-reviewer) and schedule I308 watching the review.
- If SYNTHESIS.md found and FAIL: dispatch chirp-logged-out-r5 remediation DAG and schedule I308 watching it.
- If child tasks appeared (DAG in progress, 1st check): re-suspend for I308 (+20 min).
- If no child tasks (1st check — no concern yet): note state, re-suspend for I308 (+20 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r4 was dispatched I306. 1st check in I307.
- Stall schedule: concern at 3rd check (I309); confirmation at 4th check (I310) → re-fork as r5 if still no child tasks.
- Previous stalls: chirp-logged-out (I298, 6 checks), r2 (I302, 4 checks), r3 (I306, 4 checks).
