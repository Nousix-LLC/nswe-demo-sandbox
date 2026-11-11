# _BRIEF.md — NSWE overseer step I185 (persona swe-lead) — EVALUATE: deployment check after PR #187 land

**Depends on**: I184
**Task Kind**: evaluate — load `DEPLOYMENT`, `WORK_SESSION`; deployment check after PR #187 merge; verify ArgoCD Synced/Healthy.

## Context from I184

- **PR #187** `deploy(chirp): pin sweep CronJob to febeb151 image` — squash-merged into `main`. Record merge commit SHA from I184 CONTINUE.md.
- **Expected state**: ArgoCD should sync `50-transient-sweep-cronjob.yaml` with the `sha256:2c5eafbe...` digest (febeb151 build). CronJob will use the correct binary and stop failing.
- **STATE**: `taskflow/overseer/I164-S1/project_state.json`.
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`.

## Work for this step

### 1. Load governing files
Load `appfiles/DEPLOYMENT.md` and `appfiles/WORK_SESSION.md`.

### 2. Check deployment live state
SSH to build server and verify:
- ArgoCD Application `chirp` sync status and health (expect: Synced/Healthy after PR #187 merge).
- ArgoCD revision should advance to the new merge commit from PR #187.
- CronJob `50-transient-sweep-cronjob.yaml` image should use the `sha256:2c5eafbe...` digest.
- No stale OutOfSync/Degraded state.

### 3. Evaluate deployment
- If ArgoCD is Synced/Healthy on the new commit: deployment is healthy. Update STATE.
- If ArgoCD is still syncing (OutOfSync or Progressing): check if it is making progress (not stalled).
  - Progressing normally → note in STATE and schedule a follow-up check.
  - Stalled / still Degraded → investigate root cause; may need a repair DAG.

### 4. Update STATE
Update `taskflow/overseer/I164-S1/project_state.json`:
- Update `deployment_check.status`, `argocd_sync`, `argocd_health`, `argocd_revision`.
- Update `checked_at`.
- `current_pointer`: overseer/I186.

### 5. Schedule I186
Schedule I186 (`depends_on` I185): "ACT — board hygiene: add missing Ferric 1.0 issues (#129–#136, #154–#181) to board; update _CONFIG.yaml project item IDs." (loads `BOARD`).

## Important notes
- ArgoCD may need a few minutes to sync after the merge. If not yet synced, check a second time before scheduling a repair.
- The resolved ArgoCD Degraded state is the goal: once the CronJob has the `febeb151` binary, it will execute the sweep subcommand correctly and jobs will succeed.
