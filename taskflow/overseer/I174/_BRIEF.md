# _BRIEF.md — NSWE overseer step I174 (persona swe-lead) — EVALUATE: board check

**Depends on**: I173
**Task Kind**: evaluate — load WORK_SESSION + BOARD; check the board: DAG folds, GitHub activity, PRs, escalations, deployment, backlog.

## Context from I173

- **sweep-seam-r1-r1** (remediation DAG, swe-coder): RUNNING. Forked in I173. Branch: `work/sweep-seam-r1`. Goal: fix CI fmt failure on PR #183.
- **free_dag_slots**: 0 (remediation in flight).
- **ArgoCD**: OutOfSync/Healthy at `c3f9f558` — awaiting CI image build.
- **project_state.json**: `taskflow/overseer/I164-S1/project_state.json`
- **_CONFIG.yaml**: `taskflow/overseer/_CONFIG.yaml`
- **main_sha**: `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md` before acting.

### 2. Read the config seam
Read `taskflow/overseer/_CONFIG.yaml`.

### 3. Check sweep-seam-r1-r1 DAG state
Check `taskflow/dags/sweep-seam-r1-r1/SYNTHESIS.md` — if folded, read it and process the fold.
- If PASS: schedule review launch (swe-reviewer) for PR #183.
- If FAIL: assess whether within remediation budget (2 total); if so, schedule another remediation; if budget exhausted, escalate.
- If still running: note progress, no action until next check.

### 4. Check GitHub: issues, PRs, comments
Check recent GitHub activity:
- New issues filed
- Comments on PRs or issues
- ArgoCD sync status (kubectl check)
- CI on PR #183 (if remediation pushed new commits)

### 5. Check ArgoCD sync
```
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath={.status.sync.status},{.status.health.status},{.status.sync.revision}"'
```
If synced to `c3f9f558`: update STATE. If synced to a newer SHA, update STATE and note if image digest in CronJob manifest needs updating (follow-up from sweep-seam-r1 SYNTHESIS.md).

### 6. Update STATE and write CONTINUE.md

Schedule what follows based on what is found. Suspend on bounded wake (5–10 min or DAG fold, whichever first).

## Important notes

- landing_authority: delegated, auto_land: true, headless: true (from _CONFIG.yaml).
- WORK_SESSION.md board check priority order applies.
- After sweep-seam-r1-r1 folds PASS + review APPROVE: land PR #183 automatically.
- After merge, a deployment check is needed (ArgoCD will sync new image with sweep subcommand; image digest in CronJob manifest must be updated).
