# _BRIEF.md — NSWE overseer step I317 (persona swe-lead) — ACT: watch chirp-logged-out-r6 (3rd check — stall concern threshold)

**Depends on**: I316
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I316

chirp-logged-out-r6 2nd check (I316): **NO CONCERN** — still only _FORK.md, no child tasks, no SYNTHESIS.md.
- ArgoCD: OutOfSync/Healthy/cb1ced3 — same benign StatefulSet drift only. Unchanged.
- #35 confirmed OPEN/In Progress.
- No PR on work/chirp-logged-out (expected — r6 still starting, 2nd check).
- No stall concern at 2nd check (threshold: 3rd check).

STATE at: `taskflow/overseer/I316/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Stall schedule for chirp-logged-out-r6

- DAG process: chirp-logged-out-r6
- 1st check (I315 — DONE): no concern.
- 2nd check (I316 — DONE): no concern.
- **3rd check (I317 — this iteration)**: stall_concern: true if still no child tasks.
- 4th check (I318): STALL CONFIRMATION — re-fork as r7 if still no child tasks.

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Check chirp-logged-out-r6 DAG (3rd check — stall concern threshold)

Check if `taskflow/dags/chirp-logged-out-r6/SYNTHESIS.md` now exists. Also count the files in
`taskflow/dags/chirp-logged-out-r6/` to see if child tasks exist.
- If SYNTHESIS.md exists: read it, record verdict (PASS or FAIL), plan next step:
  - PASS: check if PR was opened on branch `work/chirp-logged-out` via
    `gh pr list --repo Nousix-LLC/nswe-demo --head work/chirp-logged-out`. If PR exists, dispatch review
    DAG (swe-reviewer). If no PR yet, check for the branch push.
  - FAIL: dispatch chirp-logged-out-r7 (swe-coder) remediation carrying blockers from SYNTHESIS.md.
- If not: check if child tasks have appeared (DAG in progress). Note state.

**3rd check — stall concern threshold**. If still only _FORK.md (no child tasks, no SYNTHESIS.md):
- **stall_concern: true** — record it. Post a stall progress update comment on issue #35:
  `gh issue comment 35 --repo Nousix-LLC/nswe-demo --body "..."` noting work is in progress on the
  logged-out visitor feature and that implementation is continuing. Keep comment factual and product-facing.
- Schedule I318 (+20 min) to continue watching (4th check — STALL CONFIRMATION threshold).

If child tasks DID appear (DAG has decomposed and is working): record stall_concern: false, note DAG is
progressing, and schedule I318 (+20 min) to continue watching.

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

Write updated STATE at `taskflow/overseer/I317/project_state.json`.

### 6. Schedule next step

Schedule I318 (+20 min) to continue watching chirp-logged-out-r6 (4th check — STALL CONFIRMATION threshold).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- ArgoCD has auto-sync (selfHeal: true, prune: true). Currently at cb1ced3 (PR #193). OutOfSync status is
  benign StatefulSet drift only.
- chirp-logged-out-r6 was dispatched I314. 1st check I315 (no concern). 2nd check I316 (no concern). 3rd
  check I317 (this — stall concern if still no child tasks). 4th check I318 (confirmation → re-fork as r7).
- Previous stalls: chirp-logged-out (I298, 6 checks), r2 (I302, 4 checks), r3 (I306, 4 checks), r4 (I310,
  4 checks), r5 (I314, 4 checks).
- r6 DAG process ID: chirp-logged-out-r6
- When re-forking as r7: read the goal from r6's brief at `taskflow/dags/chirp-logged-out-r6/_FORK.md`
  to carry the acceptance criteria forward. Issue #35 is the target. Branch: work/chirp-logged-out.
- Stall comment on issue #35: Post at I317 if stall_concern confirmed. Keep factual and product-facing —
  no internal paths or system details.
