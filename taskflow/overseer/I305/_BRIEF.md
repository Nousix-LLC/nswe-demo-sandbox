# _BRIEF.md — NSWE overseer step I305 (persona swe-lead) — ACT: watch chirp-logged-out-r3 (3rd check)

**Depends on**: I304
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I304

chirp-logged-out-r3 2nd check: only _BRIEF.md and _FORK.md, no child tasks. 2nd check — no concern yet.
ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift only. #35 still In Progress;
no PR on work/chirp-logged-out yet.

STATE at: `taskflow/overseer/I304/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r3 DAG (3rd check)

Check if `taskflow/dags/chirp-logged-out-r3/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r3/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r4 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**Stall detection**: r3 was dispatched in I302; this is the 3rd check.
- 1st check (I303): no child tasks — no concern.
- 2nd check (I304): no child tasks — no concern.
- 3rd check (this iteration): still no child tasks → **STALL CONCERN**. Note in STATE.
- If child tasks appeared → DAG progressing, re-suspend for I306 (+20 min).
- Concern threshold reached → note stall concern; 4th check (I306) confirms stall → re-fork as r4.

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

Write updated STATE at `taskflow/overseer/I305/project_state.json`.

### 6. Proceed

- If chirp-logged-out-r3 SYNTHESIS.md found and PASS: dispatch review DAG (swe-reviewer) and schedule
  I306 watching the review.
- If chirp-logged-out-r3 SYNTHESIS.md found and FAIL: dispatch chirp-logged-out-r4 remediation DAG and
  schedule I306 watching it.
- If child tasks appeared (DAG now in progress, 3rd check): re-suspend for I306 (+20 min).
- If no child tasks (3rd check — STALL CONCERN): note concern, re-suspend for I306 (+20 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r3 was dispatched I302. Check cycle counts: 1st=I303, 2nd=I304, 3rd=I305 (concern),
  4th=I306 (confirm stall threshold → re-fork as r4).
- stall concern threshold: 3rd check (this iteration); stall confirmation: 4th check (I306).
