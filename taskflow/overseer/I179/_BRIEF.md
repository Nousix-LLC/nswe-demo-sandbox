# _BRIEF.md — NSWE overseer step I179 (persona swe-lead) — ACT: process review + land PR #183

**Depends on**: I178
**Task Kind**: act — load REVIEW_GATE + BOARD + DELIVERABLES_GIT + RETENTION; sort review findings, file non-blockers, land PR #183 under delegated authority, move issue #117 to Done, update STATE, then schedule the deployment check series.

## Context from I177/I178 (timer-wake evaluation)

- **review-sweep-seam-r1** has **FOLDED** with verdict: **APPROVE**.
  - SYNTHESIS.md: `taskflow/dags/review-sweep-seam-r1/SYNTHESIS.md`
  - 7 concerns checked; all PASS. No blockers. 2 non-blocking findings.
  - Non-blocking findings:
    - **#1 (Low)**: CLI dispatch in `main()` has no automated test (`crates/chirp-server/src/main.rs:42–61`) → filed as issue **#186**
    - **#2 (Low)**: `sslmode=require` relies on operator convention; no startup validation (`deploy/chirp/50-transient-sweep-cronjob.yaml`) → filed as issue **#185**
  - Review was posted on PR #183 as a COMMENT (same-account review; COMMENTED state, not APPROVED — the SYNTHESIS.md verdict is authoritative per REVIEW_GATE).
- **PR #183**: `work/sweep-seam-r1 → main`, issue #117, all CI SUCCESS (fmt/clippy/test/wasm/doc/image), MERGEABLE/CLEAN, head commit `5dcb72f`.
- **Landing authority**: delegated, auto_land: true, headless: true (from `taskflow/overseer/_CONFIG.yaml`). Machine PASS + review APPROVE → land now. No human gate step.
- **project_state.json**: `taskflow/overseer/I164-S1/project_state.json`
- **_CONFIG.yaml**: `taskflow/overseer/_CONFIG.yaml`
- **main_sha** (at I177): `c3f9f558fc7b254c2b0d431c31a7fc9a095fe0d5`
- **Remediation budget**: 2 total; 1 used; 1 remaining (not needed — APPROVE).
- **ArgoCD**: OutOfSync/Healthy on `c3f9f558` (cosmetic postgres StatefulSet drift).
- **free_dag_slots**: will be 1 once review-sweep-seam-r1 is counted as folded.

## Work for this step

### 1. Load governing files
Load `appfiles/REVIEW_GATE.md`, `appfiles/BOARD.md`, `appfiles/DELIVERABLES_GIT.md`, `appfiles/RETENTION.md` before acting.

### 2. Read the config seam
Read `taskflow/overseer/_CONFIG.yaml` to confirm landing authority (delegated, auto_land: true, headless: true).

### 3. Sort review findings from SYNTHESIS.md

Read `taskflow/dags/review-sweep-seam-r1/SYNTHESIS.md`.

- **Blockers**: none — APPROVE, land proceeds.
- **Non-blockers** (filed by review DAG):
  - Issue **#185** (`feat: validate sslmode=require at startup`) — Low severity, source: PR #183 finding #2.
  - Issue **#186** (`test: add process-level smoke tests for chirp-server CLI dispatch`) — Low severity, source: PR #183 finding #1.

### 4. Verify non-blockers are on the board as project items

Both #185 and #186 exist as GitHub issues (filed by review DAG at 2026-11-03T19:55). Check whether they are project board items (have a status on the GitHub Project PVT_kwDOEB9jls4BlZH4). If not, add them to the board in Todo status and record their project_item_ids in `_CONFIG.yaml`. Link them to their source PR #183 and to issue #117.

Use `gh project item-add` to add them to the board if missing.

### 5. Confirm review is on PR #183

The review DAG posted its review on PR #183 as a COMMENT (same-account author/reviewer — platform posted it as COMMENTED). Verify the review comment is present. The SYNTHESIS.md verdict (APPROVE) is authoritative per REVIEW_GATE. No additional action needed unless the review is missing entirely.

### 6. Land PR #183

Delegated authority: land now. Steps per `appfiles/DELIVERABLES_GIT.md`:

1. Confirm PR #183 is MERGEABLE and all CI checks are SUCCESS (re-verify at merge time).
2. Squash-merge PR #183: `gh pr merge 183 --repo Nousix-LLC/nswe-demo --squash --delete-branch`
   - The PR title will become the squash commit message. Ensure it closes #117.
3. Record the merge commit SHA.
4. Update `main_sha` in `taskflow/overseer/I164-S1/project_state.json`.

### 7. Move issue #117 to Done on the board

After merge:
1. Mark issue #117 as Done on the GitHub Project board.
2. The issue should auto-close from the PR closing keyword; confirm it is closed.

### 8. Append goal to STATE

Update `taskflow/overseer/I164-S1/project_state.json`:
- Move PR183 from OPEN → MERGED with merge commit, merge time.
- Move `review-sweep-seam-r1` from `dags_in_flight` to `dags_folded` with APPROVE verdict.
- Add to `work_items`: the sweep-seam-r1 goal entry (issues_closed: [117], pr: 183, verdict: APPROVE, etc.).
- Update `main_sha` to the new merge commit.
- Update `dags_in_flight` (review-sweep-seam-r1 leaves; free_dag_slots becomes 1).
- Note the post-merge action required: image digest update for `deploy/chirp/50-transient-sweep-cronjob.yaml`.

### 9. Schedule the deployment check series

Schedule I180 as the deployment check step, and I181 as the board check to follow:

- **I180** (`depends_on` I179): ACT/EVALUATE — deployment check after landing PR #183. Loads DEPLOYMENT + WORK_SESSION.
  - Check ArgoCD sync for the new merge commit.
  - The post-merge CI build will produce a new image with the `sweep` subcommand.
  - Until the image digest is updated in `deploy/chirp/50-transient-sweep-cronjob.yaml`, the CronJob will fail loudly (old binary, non-zero exit on `sweep`). This is by design per SYNTHESIS.
  - Fork a devops DAG (swe-coder) to update the image digest once CI publishes the new digest. This is the first item when the deployment check runs.
  
- **I181** (`depends_on` I180): EVALUATE — board check. Loads WORK_SESSION + BOARD.

## Important notes

- **landing_authority: delegated, auto_land: true, headless: true**. Land on APPROVE without human gate.
- **No blockers**: APPROVE with 0 blocking findings. Land directly.
- **Non-blockers already filed**: #185 and #186 exist as GitHub issues. Only board placement may be needed.
- **Post-merge devops**: After merge, CI builds a new image on the new commit. The CronJob manifest needs its image digest updated to the new image. This is a small devops DAG (swe-coder) that the I180 deployment check will plan. The CronJob failing loudly with the old binary is the correct interim behavior per SYNTHESIS.
- **ArgoCD**: After merge, ArgoCD will pick up the new commit. The postgres StatefulSet OutOfSync is cosmetic and does not need a remediation DAG for now (documented in STATE).
