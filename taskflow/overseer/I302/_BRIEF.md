# _BRIEF.md — NSWE overseer step I302 (persona swe-lead) — ACT: watch chirp-logged-out-r2 + ArgoCD re-check (4th check)

**Depends on**: I301
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I301

chirp-logged-out-r2 (swe-coder, forked I298): 3rd check in I301 — only _BRIEF.md and _FORK.md present, no child tasks, no SYNTHESIS.md. This is the 3rd check for r2 → CONCERN NOTED. No PR on work/chirp-logged-out. ArgoCD: OutOfSync/Healthy/cb1ced3ffe6efc678d96a26ae16a63cb948d4237 — same benign StatefulSet drift only. Board: #35 In Progress; #36-#42 Todo (unblocked). Main HEAD = cb1ced3.

STATE at: `taskflow/overseer/I301/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r2 DAG (4th check)

Check if `taskflow/dags/chirp-logged-out-r2/SYNTHESIS.md` now exists. Also count the files in `taskflow/dags/chirp-logged-out-r2/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r3 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**Stall detection**: chirp-logged-out-r2 is on its 4th check cycle (1st was I299, 2nd was I300, 3rd was I301 — CONCERN noted, 4th is I302).
- If by 4th check still no child tasks (only _BRIEF.md and _FORK.md): CONFIRM STALL. Re-fork as chirp-logged-out-r3.
  - Read the original r2 _BRIEF.md for the goal/scope/acceptance criteria.
  - Fork chirp-logged-out-r3 (swe-coder) carrying those criteria plus the stall context.
  - Update STATE: move chirp-logged-out-r2 to dags_stalled; record chirp-logged-out-r3 in dags_in_flight.
  - Update board: add note on issue #35 that r2 stalled and r3 was dispatched.
- If child tasks have appeared since I301: DAG is now in flight. Record progress and re-suspend for I303 (+20 min).

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If OutOfSync only on chirp-postgres StatefulSet: same benign drift as before — note and continue.
- If new resources OutOfSync: investigate.
- If Synced+Healthy on cb1ced3: record as fully synced.

### 4. Board spot-check

- Confirm #35 still In Progress.
- No major hygiene actions expected unless chirp-logged-out-r2 folds or stall is confirmed.
- If stall confirmed: add comment on #35 noting r2 stalled, r3 dispatched.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I302/project_state.json`.

### 6. Proceed

- If chirp-logged-out-r2 SYNTHESIS.md found and PASS: dispatch review DAG (swe-reviewer) and schedule I303 watching the review.
- If chirp-logged-out-r2 SYNTHESIS.md found and FAIL: dispatch chirp-logged-out-r3 remediation DAG and schedule I303 watching it.
- If stall confirmed (4th check, still no child tasks): re-fork as chirp-logged-out-r3 and schedule I303 watching r3.
- If child tasks appeared (DAG now in progress, 4th check): re-suspend for I303 (+20 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is benign StatefulSet drift only.
- chirp-logged-out-r2 was dispatched I298. I299 was 1st check, I300 was 2nd check, I301 was 3rd check (CONCERN noted), I302 is 4th check.
- Stall threshold: CONFIRM STALL and re-fork at 4th check (this iteration — I302).
