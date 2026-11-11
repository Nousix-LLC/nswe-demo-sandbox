# _BRIEF.md — NSWE overseer step I295 (persona swe-lead) — ACT: post-land hygiene

**Depends on**: I294
**Task Kind**: act — load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

## Context from I294

PR #193 merged (branch `work/ferric-async-forms-r2`, epic #130 — async resources, expanded events, form binding).
- Merge SHA: recorded in I294/project_state.json
- Issue #130: closed (confirmed or closed manually), board Done
- ferric_async_forms_goal: status LANDED

chirp-logged-out code DAG still in flight (dispatched I285, synthesis_path: taskflow/dags/chirp-logged-out/SYNTHESIS.md).

STATE at: `taskflow/overseer/I294/project_state.json`
Config seam: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files

Load `appfiles/BOARD.md` and `appfiles/DEPLOYMENT.md`.

### 2. Post-land board hygiene

After PR #193 merged:
- Confirm issue #130 board status is Done (project item `PVTI_lADOEB9jls4BlZH4zhFl_I0`).
- Check whether any sub-issues of #130 (the async-forms epic) need closing as well:
  `gh issue list --repo Nousix-LLC/nswe-demo --state open --label "" | grep -i "async\|form\|event\|resource\|bind"`
  Or simply: check sub-issues referenced in the epic body via `gh issue view 130 --repo Nousix-LLC/nswe-demo`.
  Close any sub-issues that #193 delivered and that are still open.
- Sweep sibling PRs for conflicts: check if any other open PRs now have merge conflicts due to main advancing.
  `gh pr list --repo Nousix-LLC/nswe-demo --state open --json number,title,mergeable,mergeStateStatus`

### 3. Deployment check

The main branch advanced with the ferric-async-forms merge. Check whether ArgoCD has synced and the new
image is running:
- ArgoCD sync status (via SSH kubectl in `argocd` ns, Application `chirp`)
- If Synced+Healthy: record as current.
- If not Synced: note the lag and check again in I296.

### 4. Check chirp-logged-out DAG

Check if `taskflow/dags/chirp-logged-out/SYNTHESIS.md` now exists (the DAG may have completed).
- If exists: read it, record verdict, plan next step (review dispatch or remediation).
- If not: still in flight, record last_check_result.

### 5. Update STATE

Write updated STATE at `taskflow/overseer/I295/project_state.json`:
- Post-land board state
- Deployment check result
- chirp-logged-out status update

### 6. Proceed

Schedule I296 as next step (bounded watch on chirp-logged-out if still in flight, or review dispatch if done).

## Notes

- Landing authority: delegated (`auto_land: true`, `headless: true`).
- After landing, sibling PRs may have conflicts; check but do not fix inline — a rebase/relock DAG when next to land.
- Sub-issues of #130: check if any were specifically targeted by PR #193 and need closing.
