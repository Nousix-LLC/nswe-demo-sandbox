# _BRIEF.md — NSWE overseer step I172 (persona swe-lead) — PROCESS FOLD: sweep-seam-r1

**Depends on**: I171
**Task Kind**: act — load WORK_SESSION + BOARD + RETENTION; observe the sweep-seam-r1 DAG state; process any fold or check for stall.

## Context from I171

- **security-persist-r1 goal**: COMPLETE. PR #182 merged (commit `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`) at 2026-11-03T19:08:01Z. Issue #120 Done on board ✅. Issue #184 added to board (item PVTI_lADOEB9jls4BlZH4zhFxodY, Todo) ✅. STATE updated: work_items[] entry added, PR182 status MERGED, review-security-persist-r1 removed from dags_in_flight.
- **ArgoCD**: OutOfSync/Healthy — awaiting CI image build on `c3f9f558`. Non-blocking, expected to auto-sync.
- **sweep-seam-r1** (swe-coder): RUNNING. Forked in I156. Pre-decomposition as of I164-S1. Goal: eliminate duplicate raw SQL / invoke Rust seam for CronJob (#117). Branch: `work/sweep-seam-r1`.
- **free_dag_slots**: 1
- **main_sha**: `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`
- **project_state.json**: `taskflow/overseer/I164-S1/project_state.json`
- **_CONFIG.yaml**: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md`, `appfiles/BOARD.md`, and `appfiles/RETENTION.md` before acting.

### 2. Read the config seam
Read `taskflow/overseer/_CONFIG.yaml`.

### 3. Check sweep-seam-r1 DAG state
Observe the sweep-seam-r1 DAG:
- Check if `taskflow/dags/sweep-seam-r1/SYNTHESIS.md` exists (fold complete).
- If folded: read SYNTHESIS.md and process the fold (update board, update STATE, check for PR, launch review if PASS).
- If still running (no SYNTHESIS.md): check for progress markers (child tasks present beyond _BRIEF.md/_FORK.md).
- If stalled (no SYNTHESIS.md, no child tasks after reasonable time since I156): assess recovery options. The brief notes it was still pre-decomposition at I164-S1 (~18:45Z). I172 is ~30 minutes later. At this point it should have started decomposing.

### 4. Check ArgoCD sync status
Check whether ArgoCD has synced `c3f9f558`:
```
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath={.status.sync.status},{.status.health.status},{.status.sync.revision}"'
```
If synced to `c3f9f558`: update STATE deployment_check.

### 5. Check for second CronJob sweep failure
Check if a second `chirp-transient-sweep` job has failed (previously only first failure seen, no bug filed yet):
```
ssh ... 'bash -lc "kubectl --context k3d-nswe -n chirp get jobs --field-selector=status.failed=1 -o name"'
```
If second failure observed: file a bug issue (#117 tracking sweep job failures) on GitHub and add to board.

### 6. Update STATE and write CONTINUE.md
Update `taskflow/overseer/I164-S1/project_state.json` with findings from steps 3-5.

Write `I172/CONTINUE.md` with:
- sweep-seam-r1 status (folded or still running + progress observed)
- ArgoCD sync result
- CronJob second-failure check result
- Next iteration's plan

Report terminal `status: completed, thread_evaluation: Continue`.

## Important notes

- landing_authority: delegated, auto_land: true, headless: true (from _CONFIG.yaml).
- If sweep-seam-r1 folded PASS: launch review DAG (swe-reviewer) per REVIEW_GATE.
- If sweep-seam-r1 folded FAIL: schedule remediation (swe-coder) per WORK_SESSION.
- No attribution trailers on GitHub posts.
