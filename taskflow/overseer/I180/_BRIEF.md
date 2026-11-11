# _BRIEF.md — NSWE overseer step I180 (persona swe-lead) — ACT: deployment check after landing PR #183

**Depends on**: I179
**Task Kind**: act/evaluate — load DEPLOYMENT + WORK_SESSION; check ArgoCD sync and CI image build on the merge commit from PR #183; decide whether to fork a devops DAG for the image digest update in the CronJob manifest.

## Context from I178/I179

- **PR #183** (`fix(#117): replace psql sweep CronJob with chirp-server sweep subcommand`) has been merged by I179.
  - The merge commit is recorded in `taskflow/overseer/I164-S1/project_state.json` (read it for the new `main_sha`).
  - Issue #117 is Done on the board.
  - Non-blockers #185 and #186 are on the board in Todo.
- **Post-merge action required** (per `taskflow/dags/review-sweep-seam-r1/SYNTHESIS.md`):
  - After the CI image build completes on the new merge commit, the image digest in `deploy/chirp/50-transient-sweep-cronjob.yaml` must be updated to the digest that includes the `sweep` subcommand.
  - Until then the CronJob fails loudly (old binary does not implement `sweep`) — correct interim behavior.
- **ArgoCD** was OutOfSync/Healthy on `c3f9f558` before the merge. After merge, the new commit should trigger an ArgoCD sync.
- **config seam**: `taskflow/overseer/_CONFIG.yaml` — landing authority delegated, headless: true.

## Work for this step

### 1. Load governing files
Load `appfiles/DEPLOYMENT.md` and `appfiles/WORK_SESSION.md` before acting.

### 2. Read the config seam
Read `taskflow/overseer/_CONFIG.yaml`.

### 3. Read the merge commit from STATE
Read `taskflow/overseer/I164-S1/project_state.json` for the new `main_sha` (set by I179 after the merge).

### 4. Check CI on the merge commit
Check the CI runs for the new merge commit on `Nousix-LLC/nswe-demo`:
```
gh run list --repo Nousix-LLC/nswe-demo --branch main --limit 5 --json status,conclusion,headSha,name,databaseId
```
- Look for the image build job on the new commit.
- If the `image` CI job has completed with SUCCESS: proceed to fork the devops DAG (step 5).
- If the `image` CI job is still running: schedule I180.1 as a re-check (bounded wake: 5–10 min), then self-suspend until it or the next timer, whichever comes first.

### 5. Check ArgoCD sync
Over SSH to the build server:
```bash
ssh -i ~/.ssh/nousix_server_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes mattm@100.90.75.93 \
  'bash -lc "kubectl --context k3d-nswe -n argocd get application chirp -o jsonpath=\"{.status.sync.status}/{.status.health.status}/{.status.sync.revision}\""'
```
Expected: OutOfSync or Synced on the new merge commit, Healthy.

### 6. Fork devops DAG for image digest update (if CI image is available)
If the CI `image` job has completed on the merge commit and published a new image to GHCR:

Fork a **swe-coder** devops DAG briefed to:
- **Goal**: Update the image digest in `deploy/chirp/50-transient-sweep-cronjob.yaml` to the digest of the newly built `chirp-server` image on the merge commit from PR #183.
- **Acceptance criteria**:
  1. `deploy/chirp/50-transient-sweep-cronjob.yaml`'s `image:` field contains the digest (sha256:...) of the chirp-server image built from the merge commit.
  2. The image is the same tag/digest as the one in `deploy/chirp/10-chirp-server.yaml` (they should reference the same build).
  3. CI passes on the update commit (fmt/clippy/test/wasm/doc/image all SUCCESS).
  4. A PR is opened on a branch `work/update-cronjob-digest-N` and closes a backlog issue if one exists for this.
- **Inputs**: The CI run URL for the image job on the merge commit; `deploy/chirp/` directory in `Nousix-LLC/nswe-demo`; the existing pattern in `deploy/chirp/10-chirp-server.yaml` for the image reference.
- **Declared output**: A commit on `work/update-cronjob-digest-N`, a PR, and a root `SYNTHESIS.md` with PASS/FAIL verdict.
- **Constraints**: Only `deploy/chirp/50-transient-sweep-cronjob.yaml` needs to change (the image field); no other files should need modification.

Record the DAG in STATE (`dags_in_flight`).

### 7. Update STATE
Update `taskflow/overseer/I164-S1/project_state.json`:
- Record the CI status on the new merge commit.
- Record ArgoCD sync status.
- If a devops DAG was forked, add it to `dags_in_flight`.
- Update `deployment_check`.
- Update `forward_series` for I180.

### 8. Schedule I181 (board check)
Schedule I181 (`depends_on` I180) as the board check to follow this deployment step.

## Important notes
- If the CI image job is not yet complete, do NOT block — schedule a bounded re-check and self-suspend.
- The CronJob failing loudly with the old binary is EXPECTED and CORRECT until the digest is updated.
- The devops DAG is a small change (one file, one field). Brief it as such.
- After scheduling I181, this step reaches `continue`.
