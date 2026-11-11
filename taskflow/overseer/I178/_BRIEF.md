# _BRIEF.md — NSWE overseer step I178 (persona swe-lead) — EVALUATE: board check / watch review-sweep-seam-r1

**Depends on**: I177
**Task Kind**: evaluate — load WORK_SESSION + REVIEW_GATE + BOARD; check whether review-sweep-seam-r1 has folded; decide what follows.

## Context from I177

- **review-sweep-seam-r1** (review DAG, swe-reviewer): still running as of I177 check.
  - DAG workspace: `taskflow/dags/review-sweep-seam-r1/`
  - Target: PR #183 (`work/sweep-seam-r1`), issue #117. Head commit `5dcb72f` on `Nousix-LLC/nswe-demo`.
  - Machine gate: PASS (all CI SUCCESS, MERGEABLE/CLEAN).
  - No SYNTHESIS.md present at I177 check. No reviews posted on PR #183 yet.
  - DAG scheduler shows: Running since 2026-11-03T19:48:44Z.
- **Landing authority**: delegated, auto_land: true, headless: true (from `taskflow/overseer/_CONFIG.yaml`).
- **project_state.json**: `taskflow/overseer/I164-S1/project_state.json`
- **_CONFIG.yaml**: `taskflow/overseer/_CONFIG.yaml`
- **main_sha**: `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`
- **Remediation budget**: 2 total; 1 used; 1 remaining.
- **ArgoCD**: OutOfSync/Healthy on `c3f9f558` (cosmetic postgres StatefulSet drift, non-blocking).
- **free_dag_slots**: 0 (review-sweep-seam-r1 is in flight).
- **New GitHub activity at I177**: None requiring intake (no new issues or PR comments).

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md`, `appfiles/REVIEW_GATE.md`, and `appfiles/BOARD.md` before acting.

### 2. Read the config seam
Read `taskflow/overseer/_CONFIG.yaml`.

### 3. Check whether review-sweep-seam-r1 has folded
Check for `taskflow/dags/review-sweep-seam-r1/SYNTHESIS.md`.

**If the review DAG has folded:**
- Read `SYNTHESIS.md` verdict (APPROVE or REQUEST-CHANGES).
- If **APPROVE**: machine PASS + review APPROVE → delegated authority applies. Schedule:
  1. A "process review + land" step (load REVIEW_GATE + BOARD): sort findings into blockers / non-blockers, file non-blockers as grouped backlog issues, make sure the review is on PR #183, then land PR #183 (merge), move issue #117 to Done, append to STATE.
  2. A deployment check step after landing (ArgoCD sync, new image digest update for CronJob per SYNTHESIS follow-up).
  3. A board check to follow.
- If **REQUEST-CHANGES**: schedule remediation (swe-coder, budget: 1 remaining) carrying blockers + prior diff.
- Either way, file all non-blockers as backlog issues (REVIEW_GATE + BOARD).

**If the review DAG is still running** (no SYNTHESIS.md yet):
- Schedule I179 as a bounded re-check (5–10 min or DAG fold, whichever comes first).
- Self-suspend on that bounded wake.

### 4. Check GitHub for new activity
While reviewing, check for any new issues, comments, or PR activity on `Nousix-LLC/nswe-demo` that require intake.

### 5. Update STATE
Update project_state.json with the review DAG status (or fold result).

## Important notes

- landing_authority: delegated, auto_land: true, headless: true. On APPROVE: land without human gate.
- After merge: CI will publish a new chirp-server image with the `sweep` subcommand. The image digest in
  `deploy/chirp/50-transient-sweep-cronjob.yaml` must be updated (a devops step or separate DAG). Plan for it after the land.
- Remediation budget remaining: 1. If review is REQUEST-CHANGES, one remediation DAG may be launched.
- After landing PR #183, the deployment check is the next step (ArgoCD sync + image digest update for CronJob).
