# _BRIEF.md — NSWE overseer step I299 (persona swe-lead) — ACT: watch chirp-logged-out-r2 + ArgoCD re-check

**Depends on**: I298
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I298

chirp-logged-out original DAG (forked I285) confirmed STALLED after 6 check cycles (I285, I292, I295, I296, I297, I298) — directory had only _BRIEF.md and _FORK.md, no child tasks, no branch push, no SYNTHESIS.md. Re-forked as chirp-logged-out-r2 (swe-coder) in I298. ArgoCD still at cb1ced3 (benign StatefulSet OutOfSync only). Board: #35 In Progress; #36-#42 Todo (unblocked). No PR on work/chirp-logged-out. Main HEAD = cb1ced3.

STATE at: `taskflow/overseer/I298/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r2 DAG

Check if `taskflow/dags/chirp-logged-out-r2/SYNTHESIS.md` now exists.
- If exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r3 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: still in flight (1st check of r2 — expected). Note state and re-suspend for I300 (+20 min).

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If OutOfSync only on chirp-postgres StatefulSet: same benign drift as before — note and continue.
- If new resources OutOfSync: investigate.
- If Synced+Healthy on cb1ced3: record as fully synced.

### 4. Board check

Quick board hygiene:
- Check if chirp-logged-out-r2 has pushed to `work/chirp-logged-out` and opened a PR.
- Spot-check #35 still In Progress.
- No major hygiene actions expected unless chirp-logged-out-r2 folds.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I299/project_state.json`.

### 6. Proceed

- If chirp-logged-out-r2 SYNTHESIS.md found and PASS: dispatch review DAG and schedule I300 watching the review.
- If chirp-logged-out-r2 SYNTHESIS.md found and FAIL: dispatch remediation DAG and schedule I300 watching it.
- If still in flight: schedule I300 as bounded watch (+20 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is benign StatefulSet drift only.
- chirp-logged-out-r2 was dispatched I298. This I299 is the 1st check for r2.
