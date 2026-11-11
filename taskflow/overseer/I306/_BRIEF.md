# _BRIEF.md — NSWE overseer step I306 (persona swe-lead) — ACT: watch chirp-logged-out-r3 (4th check — stall confirmation threshold)

**Depends on**: I305
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I305

chirp-logged-out-r3 3rd check: only _BRIEF.md and _FORK.md, no child tasks. STALL CONCERN recorded (3rd check = concern threshold).
ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift only. #35 still In Progress;
no PR on work/chirp-logged-out yet.

STATE at: `taskflow/overseer/I305/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r3 DAG (4th check — stall confirmation threshold)

Check if `taskflow/dags/chirp-logged-out-r3/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r3/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r4 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**Stall detection**: r3 was dispatched in I302; this is the 4th check.
- 1st check (I303): no child tasks — no concern.
- 2nd check (I304): no child tasks — no concern.
- 3rd check (I305): no child tasks — STALL CONCERN recorded.
- 4th check (this iteration): still no child tasks → **STALL CONFIRMED** → re-fork as chirp-logged-out-r4.
  - If child tasks appeared → DAG progressing, re-suspend for I307 (+20 min).
  - If SYNTHESIS.md appeared → act on verdict (above).

**On stall confirmation (4th check, still no child tasks)**:
  - Move chirp-logged-out-r3 to dags_stalled in STATE.
  - Re-fork as chirp-logged-out-r4 (swe-coder), carrying the same goal and brief from r3.
  - Post a comment on issue #35 noting the re-fork.
  - Read `taskflow/dags/chirp-logged-out-r3/_BRIEF.md` to carry the full goal/brief forward to r4.

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

Write updated STATE at `taskflow/overseer/I306/project_state.json`.

### 6. Proceed

- If SYNTHESIS.md found and PASS: dispatch review DAG (swe-reviewer) and schedule I307 watching the review.
- If SYNTHESIS.md found and FAIL: dispatch chirp-logged-out-r4 remediation DAG and schedule I307 watching it.
- If child tasks appeared (DAG now in progress, 4th check): re-suspend for I307 (+20 min).
- If no child tasks (4th check — STALL CONFIRMED): re-fork as chirp-logged-out-r4, schedule I307 watching it.

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r3 was dispatched I302. Check cycle counts: 1st=I303, 2nd=I304, 3rd=I305 (concern),
  4th=I306 (this — stall confirmation threshold → re-fork as r4 if still no child tasks).
- stall concern threshold: 3rd check (I305, DONE); stall confirmation: 4th check (I306, this iteration).
- Previous r3 _BRIEF.md is at `taskflow/dags/chirp-logged-out-r3/_BRIEF.md` — read it to carry goal forward to r4.
- Previous stalls: chirp-logged-out (stalled I298, 6 checks), chirp-logged-out-r2 (stalled I302, 4 checks),
  chirp-logged-out-r3 (concern I305, confirmation threshold I306 = this).
