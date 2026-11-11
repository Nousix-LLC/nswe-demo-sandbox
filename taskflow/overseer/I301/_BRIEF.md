# _BRIEF.md — NSWE overseer step I301 (persona swe-lead) — ACT: watch chirp-logged-out-r2 + ArgoCD re-check

**Depends on**: I300
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I300

chirp-logged-out-r2 (swe-coder, forked I298): 2nd check in I300 — only _BRIEF.md and _FORK.md present, no child tasks, no SYNTHESIS.md. This is the 2nd check for r2. No PR on work/chirp-logged-out. ArgoCD: OutOfSync/Healthy/cb1ced3ffe6efc678d96a26ae16a63cb948d4237 — same benign StatefulSet drift only. Board: #35 In Progress; #36-#42 Todo (unblocked). Main HEAD = cb1ced3.

STATE at: `taskflow/overseer/I300/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r2 DAG

Check if `taskflow/dags/chirp-logged-out-r2/SYNTHESIS.md` now exists. Also count the files in `taskflow/dags/chirp-logged-out-r2/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r3 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**Stall detection**: chirp-logged-out-r2 is on its 3rd check cycle (1st was I299, 2nd was I300, 3rd is I301). The original stall pattern was no child tasks after 6 cycles.
- If by 3rd check still no child tasks (only _BRIEF.md and _FORK.md): BEGIN CONCERN. Note in STATE. Re-suspend for I302 (+20 min).
- If by 4th check still no child tasks: CONFIRM STALL. Re-fork as chirp-logged-out-r3.

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If OutOfSync only on chirp-postgres StatefulSet: same benign drift as before — note and continue.
- If new resources OutOfSync: investigate.
- If Synced+Healthy on cb1ced3: record as fully synced.

### 4. Board spot-check

- Confirm #35 still In Progress.
- No major hygiene actions expected unless chirp-logged-out-r2 folds.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I301/project_state.json`.

### 6. Proceed

- If chirp-logged-out-r2 SYNTHESIS.md found and PASS: dispatch review DAG and schedule I302 watching the review.
- If chirp-logged-out-r2 SYNTHESIS.md found and FAIL: dispatch remediation DAG and schedule I302 watching it.
- If still in flight (3rd check, no child tasks): note concern, schedule I302 as bounded watch (+20 min).
- If still in flight (4th check+, no child tasks): confirm stall and re-fork as r3.

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is benign StatefulSet drift only.
- chirp-logged-out-r2 was dispatched I298. I299 was the 1st check, I300 was the 2nd check, I301 is the 3rd check.
- Stall threshold: begin concern at 3rd check with no child tasks (this iteration — I301). Confirm stall and re-fork at 4th check.
