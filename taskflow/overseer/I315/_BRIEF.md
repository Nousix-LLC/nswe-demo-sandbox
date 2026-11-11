# _BRIEF.md — NSWE overseer step I315 (persona swe-lead) — ACT: watch chirp-logged-out-r6 (1st check)

**Depends on**: I314
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I314

chirp-logged-out-r5 4th check (I314): **STALL CONFIRMED** — only _FORK.md, no child tasks, no SYNTHESIS.md.
- ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift only. Unchanged.
- #35 confirmed OPEN/In Progress.
- No PR on work/chirp-logged-out (expected — r5 stalled, never produced code).
- **Action taken**: Re-forked as chirp-logged-out-r6 (swe-coder, forked I314).
  - Comment posted: https://github.com/Nousix-LLC/nswe-demo/issues/35#issuecomment-6676485084
  - r5 moved to dags_stalled in STATE.
  - r6 added to dags_in_flight in STATE.

STATE at: `taskflow/overseer/I314/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Stall schedule for chirp-logged-out-r6

- DAG process: chirp-logged-out-r6
- **1st check (I315 — this iteration)**: allow up to 20 min — no concern yet.
- 2nd check (I316): no concern yet.
- 3rd check (I317): stall_concern: true if still no child tasks.
- 4th check (I318): STALL CONFIRMATION — re-fork as r7 if still no child tasks.

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r6 DAG (1st check)

Check if `taskflow/dags/chirp-logged-out-r6/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r6/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r7 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**1st check — no concern threshold**. If still only _FORK.md (no child tasks, no SYNTHESIS.md): note, no
stall concern yet. Schedule I316 (+20 min).

If child tasks DID appear (DAG has decomposed and is working): record stall_concern: false, note DAG is
progressing, and schedule I316 (+20 min) to continue watching.

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

Write updated STATE at `taskflow/overseer/I315/project_state.json`.

### 6. Schedule next step

Schedule I316 (+20 min) to continue watching chirp-logged-out-r6 (2nd check).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r6 was dispatched I314. 1st check I315 (this — no concern). 2nd check I316. 3rd check I317
  (stall concern). 4th check I318 (confirmation → re-fork as r7 if still no child tasks).
- Previous stalls: chirp-logged-out (I298, 6 checks), r2 (I302, 4 checks), r3 (I306, 4 checks), r4 (I310,
  4 checks), r5 (I314, 4 checks).
- r6 DAG process ID: chirp-logged-out-r6
- When re-forking as r7: read the goal from r6's brief at `taskflow/dags/chirp-logged-out-r6/_FORK.md`
  to carry the acceptance criteria forward. Issue #35 is the target. Branch: work/chirp-logged-out.
