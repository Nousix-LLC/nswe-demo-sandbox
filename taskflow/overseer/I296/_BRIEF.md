# _BRIEF.md — NSWE overseer step I296 (persona swe-lead) — ACT: watch chirp-logged-out + ArgoCD re-check

**Depends on**: I295
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I295

Post-land hygiene for PR #193 completed:
- Issue #130 confirmed CLOSED; sub-issues #143 (Async resources/suspense), #144 (DOM event handling), #145 (Forms/binding) closed and added to board as Done.
- No open PRs (PR list empty at I295 check).
- ArgoCD: OutOfSync (synced to 62febf5 = PR #228; PR #193 merge cb1ced3 not yet picked up). App Healthy. Auto-sync enabled (selfHeal: true). Will re-check.
- chirp-logged-out DAG: SYNTHESIS.md not yet present at taskflow/dags/chirp-logged-out/SYNTHESIS.md — still in flight (3rd check: I285, I292, I295).

STATE at: `taskflow/overseer/I295/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out DAG

Check if `taskflow/dags/chirp-logged-out/SYNTHESIS.md` now exists.
- If exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out`; if yes, dispatch review DAG (swe-reviewer). If no PR yet, check for the branch and PR via `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`.
  - FAIL: dispatch chirp-logged-out-r2 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: still in flight; record last_check_result, re-suspend for I297 (bounded watch, +20 min).

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If Synced+Healthy on cb1ced3: record as deployed and current.
- If still OutOfSync on 62febf5 but Healthy: still auto-syncing; note lag.
- If unhealthy: investigate pods and log.

### 4. Board check

After any state changes, do a quick board hygiene sweep:
- Confirm #130 and sub-issues #143/#144/#145 show Done on board (spot-check via `gh project item-list 1 --owner Nousix-LLC --format json`).
- Check if any items newly unblocked now that #130 is landed (issues #36–#42 depended on #130; also check #83 identity/sessions).

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I296/project_state.json`.

### 6. Proceed

- If chirp-logged-out SYNTHESIS.md found and PASS: dispatch review DAG and schedule I297 watching the review.
- If chirp-logged-out SYNTHESIS.md found and FAIL: dispatch remediation DAG and schedule I297 watching it.
- If still in flight: schedule I297 as bounded watch (+20 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). OutOfSync with one newer commit — expect auto-sync to have fired by now or soon.
- chirp-logged-out DAG has been in flight since I285. If SYNTHESIS.md still absent at I296, it has been running for multiple check cycles; note the extended duration but do not force-fail — DAGs can take longer for complex work.
