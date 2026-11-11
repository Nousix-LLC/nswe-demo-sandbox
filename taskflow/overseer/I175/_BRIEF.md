# _BRIEF.md — NSWE overseer step I175 (persona swe-lead) — EVALUATE: board check

**Depends on**: I174
**Task Kind**: evaluate — load WORK_SESSION + BOARD; check the board: DAG folds, GitHub activity, PRs, CI, ArgoCD.

## Context from I174

- **sweep-seam-r1-r1** (remediation DAG, swe-coder): RUNNING. Forked in I173 (dispatched 2026-11-03T19:31Z). Branch: `work/sweep-seam-r1`. Goal: fix CI fmt failure + rebase conflict on PR #183.
  - CI run 41705065393 on work/sweep-seam-r1: fmt/clippy/test/wasm/doc all PASS. image: PENDING.
  - Branch: MERGEABLE (conflict resolved by remediation DAG's rebase).
- **free_dag_slots**: 0 (remediation in flight).
- **ArgoCD**: OutOfSync/Healthy at `c3f9f558` — only cosmetic postgres StatefulSet drift, no functional impact.
- **project_state.json**: `taskflow/overseer/I164-S1/project_state.json`
- **_CONFIG.yaml**: `taskflow/overseer/_CONFIG.yaml`
- **main_sha**: `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`
- **landing_authority**: delegated, auto_land: true, headless: true

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md` and `appfiles/BOARD.md` before acting.

### 2. Read the config seam
Read `taskflow/overseer/_CONFIG.yaml`.

### 3. Check sweep-seam-r1-r1 DAG state
Check `taskflow/dags/sweep-seam-r1-r1/SYNTHESIS.md` — if folded, read it and process the fold.
- If PASS: schedule review launch (swe-reviewer) for PR #183 (load `REVIEW_GATE.md`).
- If FAIL: assess whether within remediation budget (1 attempt remaining); if so, schedule another remediation; if budget exhausted, escalate.
- If still running: note progress; check CI status on PR #183 (image job completion).

### 4. Check GitHub: issues, PRs, CI on PR #183
- New issues filed since I174
- Comments on PR #183 or other open PRs
- CI status on PR #183: has the `image` job completed?
  - If image: SUCCESS and all other checks pass: PR #183 is machine-PASS.

### 5. Check ArgoCD sync
```
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath={.status.sync.status},{.status.health.status},{.status.sync.revision}"'
```
If synced to a newer SHA than `c3f9f558`: update STATE. If still on c3f9f558: note cosmetic postgres StatefulSet OutOfSync (non-blocking).

### 6. Update STATE and write CONTINUE.md

Dispatch logic:
- If sweep-seam-r1-r1 folded PASS + CI all green: schedule "launch review" task (read `REVIEW_GATE.md`).
- If sweep-seam-r1-r1 folded FAIL and budget remaining (1 attempt left): schedule remediation-r2 launch.
- If sweep-seam-r1-r1 folded FAIL and budget exhausted: schedule "escalate to user" task.
- If sweep-seam-r1-r1 still running: note progress, schedule next board check on bounded wake (5–10 min or DAG fold).

## Important notes

- landing_authority: delegated, auto_land: true, headless: true (from _CONFIG.yaml).
- After sweep-seam-r1-r1 folds PASS + all CI green + review APPROVE: land PR #183 automatically.
- After merge, a deployment check is needed (ArgoCD will sync new image; CronJob manifest image digest may need updating after next land if new image SHA differs).
- Remediation budget: 2 total attempts; 1 used (sweep-seam-r1-r1 is attempt 1). Budget remaining: 1.
