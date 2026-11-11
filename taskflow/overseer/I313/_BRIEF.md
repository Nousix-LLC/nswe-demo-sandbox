# _BRIEF.md — NSWE overseer step I313 (persona swe-lead) — ACT: watch chirp-logged-out-r5 (3rd check — STALL CONCERN THRESHOLD)

**Depends on**: I312
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I312

chirp-logged-out-r5 2nd check (I312): only _FORK.md — no child tasks, no SYNTHESIS.md. 2nd check — **no concern** (expected).
- ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift only. No change.
- #35 confirmed OPEN/In Progress.
- No PR on work/chirp-logged-out (expected — r5 still starting).

STATE at: `taskflow/overseer/I312/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Stall schedule for chirp-logged-out-r5

- DAG process: chirp-logged-out-r5 (dag_process_id in STATE)
- 1st check (I311): no concern — only _FORK.md, expected.
- 2nd check (I312): no concern — only _FORK.md, expected.
- **3rd check (I313 — this iteration): STALL CONCERN THRESHOLD.**
- 4th check: I314 — stall CONFIRMATION threshold → re-fork as r6 if still no child tasks.

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r5 DAG (3rd check — stall concern threshold)

Check if `taskflow/dags/chirp-logged-out-r5/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r5/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r6 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**3rd check — STALL CONCERN THRESHOLD**: If still only _FORK.md (no child tasks, no SYNTHESIS.md), this is now
a stall concern. Record it as `stall_concern: true` in STATE. Still schedule I314 for stall CONFIRMATION (+20 min).
If child tasks DID appear (DAG has decomposed and is working), no concern — just note and re-suspend for I314.

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

Write updated STATE at `taskflow/overseer/I313/project_state.json`.

### 6. Proceed

- If SYNTHESIS.md found and PASS: dispatch review DAG (swe-reviewer) and schedule I314 watching the review.
- If SYNTHESIS.md found and FAIL: dispatch chirp-logged-out-r6 remediation DAG and schedule I314 watching it.
- If child tasks appeared: re-suspend for I314 (+20 min), note stall_concern: false (DAG is progressing).
- If still only _FORK.md (3rd check — stall concern): set stall_concern: true, re-suspend for I314 (+20 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r5 was dispatched I310. 1st check I311 (no concern). 2nd check I312 (no concern). 3rd check in I313 (this — stall concern threshold).
- Stall schedule: concern at 3rd check (I313 — this); CONFIRMATION at 4th check (I314) → re-fork as r6 if still no child tasks.
- Previous stalls: chirp-logged-out (I298, 6 checks), r2 (I302, 4 checks), r3 (I306, 4 checks), r4 (I310, 4 checks).
- r5 DAG process ID: chirp-logged-out-r5 (read from STATE)
- If re-forking as r6: read the goal from r5's brief at `taskflow/dags/chirp-logged-out-r5/_FORK.md`
  to carry the acceptance criteria forward. Issue #35 is the target. Branch: work/chirp-logged-out.
