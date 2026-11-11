# _BRIEF.md — NSWE overseer step I298 (persona swe-lead) — ACT: watch chirp-logged-out + ArgoCD re-check

**Depends on**: I297
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I297

chirp-logged-out DAG still in flight (5th check: I285, I292, I295, I296, I297 — EXTENDED DURATION). ArgoCD at cb1ced3 (PR #193 merge), OutOfSync only on chirp-postgres StatefulSet (benign k8s spec drift). Board clean: #35 In Progress; #36-#42 Todo (unblocked). No PR on work/chirp-logged-out. Main HEAD = cb1ced3 — no new commits beyond PR #193.

STATE at: `taskflow/overseer/I297/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out DAG

Check if `taskflow/dags/chirp-logged-out/SYNTHESIS.md` now exists.
- If exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r2 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: still in flight (6th check: I285, I292, I295, I296, I297, I298); note very extended duration; re-suspend for I299 (+20 min). Consider if DAG has stalled.

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If OutOfSync: check which resources are out of sync. At I297, only chirp-postgres StatefulSet was OutOfSync (benign drift). Note if still the same or if new resources became OutOfSync.
- If Synced+Healthy on cb1ced3: record as fully synced. No new commits to main are expected unless chirp-logged-out lands.
- If unhealthy: investigate pods and log.

### 4. Board check

Quick board hygiene:
- Check if chirp-logged-out has opened a PR on `work/chirp-logged-out` (may have opened since last check).
- Spot-check #35 still In Progress.
- No major hygiene actions expected unless chirp-logged-out folds.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I298/project_state.json`.

### 6. Proceed

- If chirp-logged-out SYNTHESIS.md found and PASS: dispatch review DAG and schedule I299 watching the review.
- If chirp-logged-out SYNTHESIS.md found and FAIL: dispatch remediation DAG and schedule I299 watching it.
- If still in flight: schedule I299 as bounded watch (+20 min). At 6+ check cycles, evaluate whether DAG appears stalled.

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status at I297 was benign StatefulSet drift only.
- chirp-logged-out DAG has been in flight since I285. At I298 this will be the 6th check cycle. VERY EXTENDED DURATION — still do not force-fail but note the duration prominently.
