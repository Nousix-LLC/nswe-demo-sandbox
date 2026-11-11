# _BRIEF.md — NSWE overseer step I297 (persona swe-lead) — ACT: watch chirp-logged-out + ArgoCD re-check

**Depends on**: I296
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I296

chirp-logged-out DAG still in flight (4th check: I285, I292, I295, I296). ArgoCD auto-synced to cb1ced3 (PR #193 merge) since I295; OutOfSync only on chirp-postgres StatefulSet (benign k8s spec drift). Board clean: #130, #143, #144, #145 confirmed Done; #35 In Progress; #36-#42 Todo (unblocked from #130 dependency).

STATE at: `taskflow/overseer/I296/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out DAG

Check if `taskflow/dags/chirp-logged-out/SYNTHESIS.md` now exists.
- If exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r2 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: still in flight (5th check: I285, I292, I295, I296, I297); note extended duration; re-suspend for I298 (+20 min).

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If OutOfSync: check which resources are out of sync. At I296, only chirp-postgres StatefulSet was OutOfSync (benign drift). Note if still the same or if new resources became OutOfSync.
- If Synced+Healthy on cb1ced3: record as fully synced and current. No new commits to main are expected unless chirp-logged-out lands.
- If unhealthy: investigate pods and log.

### 4. Board check

Quick board hygiene:
- Check if chirp-logged-out has opened a PR on `work/chirp-logged-out` (may have opened since last check).
- Spot-check #35 still In Progress.
- No major hygiene actions expected unless chirp-logged-out folds.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I297/project_state.json`.

### 6. Proceed

- If chirp-logged-out SYNTHESIS.md found and PASS: dispatch review DAG and schedule I298 watching the review.
- If chirp-logged-out SYNTHESIS.md found and FAIL: dispatch remediation DAG and schedule I298 watching it.
- If still in flight: schedule I298 as bounded watch (+20 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status at I296 was benign StatefulSet drift only.
- chirp-logged-out DAG has been in flight since I285. At I297 this will be the 5th check cycle. Still do not force-fail — the DAG is running complex work. Note the extended duration.
