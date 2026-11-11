# _BRIEF.md — NSWE overseer step I320 (persona swe-lead) — ACT: watch chirp-logged-out-r7 (2nd check — no concern)

**Depends on**: I319
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I319

chirp-logged-out-r7 1st check (I319): **NO CONCERN** — only _FORK.md, no child tasks, no SYNTHESIS.md.
- 1st check — no concern as expected.
- #35 confirmed OPEN/In Progress.
- No PR on work/chirp-logged-out (expected — r7 not yet decomposed).
- ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift only. Unchanged.

STATE at: `taskflow/overseer/I319/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Stall schedule for chirp-logged-out-r7

- DAG process: chirp-logged-out-r7 (forked I318)
- 1st check (I319 — done): no concern.
- **2nd check (I320 — this iteration): no concern.** Simply verify if the DAG has started (look for child tasks
  or SYNTHESIS.md). Note state. No concern at 2nd check regardless of state.

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r7 DAG (2nd check — no concern)

Check if `taskflow/dags/chirp-logged-out-r7/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r7/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r8 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: note state (2nd check — no concern regardless).

### 3. ArgoCD deployment re-check

Re-check ArgoCD sync status:
  `kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath="{.status.sync.status},{.status.health.status},{.status.sync.revision}"`
- If OutOfSync only on chirp-postgres StatefulSet: same benign drift as before — note and continue.
- If new resources OutOfSync: investigate.
- If Synced+Healthy on cb1ced3: record as fully synced.

### 4. Board spot-check

- Confirm #35 still In Progress.
- Check if any PR appeared on `work/chirp-logged-out`: `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I320/project_state.json`.

### 6. Schedule next step

Schedule I321 (+20 min) to continue watching r7 (3rd check — stall_concern: true if still no child tasks).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r7 was dispatched I318. 1st check I319 (no concern). 2nd check I320 (this — no concern).
- Previous stalls: chirp-logged-out (I298, 6 checks), r2 (I302, 4 checks), r3 (I306, 4 checks), r4 (I310,
  4 checks), r5 (I314, 4 checks), r6 (I318, 4 checks).
- r7 DAG process ID: chirp-logged-out-r7
- r8 DAG process ID to use if re-fork needed: chirp-logged-out-r8
- Stall schedule for r7: 1st check I319 (no concern — DONE), 2nd check I320 (no concern — this), 3rd check I321 (concern
  if still no child tasks), 4th check I322 (CONFIRMATION → re-fork as r8).
