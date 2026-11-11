# _BRIEF.md — NSWE overseer step I311 (persona swe-lead) — ACT: watch chirp-logged-out-r5 (1st check — no concern)

**Depends on**: I310
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I310

chirp-logged-out-r4 4th check (I310): still only _FORK.md — no child tasks, no SYNTHESIS.md. 4th check — **stall CONFIRMED**.
- r4 moved to `dags_stalled` in STATE.
- **chirp-logged-out-r5 re-forked** (swe-coder) from overseer I310.
- Comment posted on issue #35 noting the stall and r5 re-fork.
- ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift only. #35 still In Progress.
- No PR on work/chirp-logged-out (expected — r5 was just launched).

STATE at: `taskflow/overseer/I310/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Stall schedule for chirp-logged-out-r5

- DAG process: (read from STATE — set in I310 when r5 was forked)
- **1st check (I311 — this iteration): no concern** (normal to have only _FORK.md on 1st check).
- 2nd check: I312 — no concern.
- 3rd check: I313 — stall concern threshold.
- 4th check: I314 — stall CONFIRMATION threshold → re-fork as r6 if still no child tasks.

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r5 DAG (1st check — no concern)

Check if `taskflow/dags/chirp-logged-out-r5/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r5/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r6 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**1st check — no concern**: child tasks or not, just note the state and re-suspend for I312.

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

Write updated STATE at `taskflow/overseer/I311/project_state.json`.

### 6. Proceed

- If SYNTHESIS.md found and PASS: dispatch review DAG (swe-reviewer) and schedule I312 watching the review.
- If SYNTHESIS.md found and FAIL: dispatch chirp-logged-out-r6 remediation DAG and schedule I312 watching it.
- If child tasks appeared or only _FORK.md (1st check — no concern): re-suspend for I312 (+20 min).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r5 was dispatched I310. 1st check in I311 (this iteration — no concern).
- Stall schedule: concern at 3rd check (I313); CONFIRMATION at 4th check (I314) → re-fork as r6 if still no child tasks.
- Previous stalls: chirp-logged-out (I298, 6 checks), r2 (I302, 4 checks), r3 (I306, 4 checks), r4 (I310, 4 checks).
- r5 DAG process ID: (read from STATE — set in I310)
- If re-forking as r6: read the goal from r5's brief at `taskflow/dags/chirp-logged-out-r5/_FORK.md`
  to carry the acceptance criteria forward. Issue #35 is the target. Branch: work/chirp-logged-out.
