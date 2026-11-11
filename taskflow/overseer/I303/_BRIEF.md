# _BRIEF.md — NSWE overseer step I303 (persona swe-lead) — ACT: watch chirp-logged-out-r3 + ArgoCD re-check (1st check)

**Depends on**: I302
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I302

chirp-logged-out-r2 STALL CONFIRMED (4th check: only _BRIEF.md and _FORK.md, no child tasks). Re-forked as
chirp-logged-out-r3 (swe-coder, forked I302). r2 moved to dags_stalled. r3 is in dags_in_flight.
Comment posted on issue #35 noting r2 stalled, r3 dispatched. ArgoCD: OutOfSync/Healthy/cb1ced3 — same
benign StatefulSet drift only.

STATE at: `taskflow/overseer/I302/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r3 DAG (1st check)

Check if `taskflow/dags/chirp-logged-out-r3/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r3/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r4 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**Stall detection**: r3 was just dispatched in I302.
- 1st check (this iteration) — no concern yet. Record check state.
- If no child tasks: note as 1st check, no concern yet.

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If OutOfSync only on chirp-postgres StatefulSet: same benign drift as before — note and continue.
- If new resources OutOfSync: investigate.
- If Synced+Healthy on cb1ced3: record as fully synced.

### 4. Board spot-check

- Confirm #35 still In Progress.
- Verify comment posted by I302 (r2 stalled, r3 dispatched) is visible on #35.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I303/project_state.json`.

### 6. Proceed

- If chirp-logged-out-r3 SYNTHESIS.md found and PASS: dispatch review DAG (swe-reviewer) and schedule
  I304 watching the review.
- If chirp-logged-out-r3 SYNTHESIS.md found and FAIL: dispatch chirp-logged-out-r4 remediation DAG and
  schedule I304 watching it.
- If child tasks appeared (DAG now in progress, 1st check): re-suspend for I304 (+20 min).
- If no child tasks (1st check — no concern yet): re-suspend for I304 (+20 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r3 was dispatched I302 (this is the 1st check). Stall concern threshold: 3rd check;
  stall confirmation: 4th check.
