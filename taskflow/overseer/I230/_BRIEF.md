# _BRIEF.md — NSWE overseer step I230 (persona swe-lead) — ACT: launch devops DAG for chirp-server digest update

**Depends on**: I229
**Task Kind**: act — load `appfiles/WORK_SESSION.md`. Fork devops coder DAG (swe-coder) to update chirp-server image digest. Issue #206.

## Context from I229 (EVALUATE: board check / next goal after PR #203 land)

- **Escalation**: ferric-async-forms budget exhausted (PR #193) — STILL ACTIVE, no user response. Do NOT launch ferric-async-forms-r3.
- **Issue #206 filed**: `deploy(chirp): update chirp-server image digest to d8230fea build` (board Todo, high priority)
  - Board item: `PVTI_lADOEB9jls4BlZH4zhF7WNw`
  - Chirp-server running sha256:adaa4c26 (predates PRs #182/#183/#188/#203 — security code not live)
  - Issue #207 was a duplicate; closed in I229.
- **Issues #204/#205**: confirmed on board (Todo) ✓
- **Decision**: I230 launches devops DAG (swe-coder) to pin `deploy/10-deployment.yaml` chirp-server image to d8230fea CI build (run 41803200262). After DAG folds and lands: I231 evaluates board and schedules next code goal (#132 HTTP Client).
- **STATE**: `taskflow/overseer/I229/project_state.json`
- **Config seam**: `taskflow/overseer/_CONFIG.yaml`

## Work for this step

### 1. Load governing files
Load `appfiles/WORK_SESSION.md`. Read `_CONFIG.yaml` and `taskflow/overseer/I229/project_state.json`.

### 2. Fork devops DAG (swe-coder): chirp-server image digest update

**Goal**: Update `deploy/10-deployment.yaml` to pin the chirp-server image to the digest built from commit `d8230fea` (CI run 41803200262).

**Brief to author** at `taskflow/dags/update-chirp-server-digest-r1/_BRIEF.md`:

```
# _BRIEF.md — update-chirp-server-digest-r1 (swe-coder)

## Objective
Update deploy/10-deployment.yaml to pin the chirp-server container image to the digest from
the CI "image" job on commit d8230fea (GitHub Actions run 41803200262, repo Nousix-LLC/nswe-demo).

## Background
The deployed chirp-server pod is running sha256:adaa4c26... which predates PRs #182/#183/#188/#203.
PRs that contain argon2id credential hashing, sweep subcommand, Ferric 1.0 authoring model, and 
router are merged but NOT running in the deployed image. Issue #206 tracks this gap.

## Acceptance criteria
- deploy/10-deployment.yaml: chirp-server container image updated to the digest from CI run 41803200262
  (the image job built from commit d8230fea). Find the exact SHA256 digest from the CI run artifacts
  or from the GitHub Container Registry (ghcr.io/nousix-llc/nswe-demo, tag d8230fea or the run's output).
- CI: all 6 jobs PASS (fmt, clippy, test, wasm, doc, image) on a branch work/update-chirp-server-digest-r1
- PR open against main on Nousix-LLC/nswe-demo, titled: "deploy(chirp): pin chirp-server image to d8230fea build (CI run 41803200262)"
- PR body references issue #206

## Declared output
- Branch: work/update-chirp-server-digest-r1
- PR on Nousix-LLC/nswe-demo targeting main
- deploy/10-deployment.yaml updated with correct chirp-server image digest
- All 6 CI jobs green

## Scope
devops only — this is a one-line manifest change (the image digest in 10-deployment.yaml).
No Rust code changes. No test changes. No other files unless the image tag/digest format requires
updating a companion file.

## Notes
- This is a devops digest update analogous to PR #187 (which pinned the sweep CronJob digest)
- The CI image job builds and pushes a ghcr.io image on every main push; find the d8230fea digest
  from run 41803200262 output or from the registry
- Repo: Nousix-LLC/nswe-demo, default branch: main
```

**Fork**: `launch_agent = swe-coder`, workspace = `taskflow/dags/update-chirp-server-digest-r1/`

### 3. Record the fork in STATE and suspend on forked-thread-completion

After forking:
- Write `taskflow/overseer/I230/project_state.json` with:
  - `dags_in_flight`: `update-chirp-server-digest-r1` (goal: chirp-server digest update, issues: [206], kind: devops)
  - Forward series: I230 suspended waiting on update-chirp-server-digest-r1 fold; I231 to fold result and decide next code goal
- Self-suspend on firing conditions: `forked-thread-completion` (update-chirp-server-digest-r1) + schedule wake (bounded: 20 minutes from fork)

### 4. I231 ACT: fold devops DAG result + decide next code goal

When I230 wakes (DAG terminal or timer):
- Read `taskflow/dags/update-chirp-server-digest-r1/SYNTHESIS.md` (or COMPLETE.md)
- If machine gate PASS: launch review DAG (swe-reviewer)
- If review APPROVE: land PR under delegated authority; update board; file I232 for next code goal (#132 HTTP Client)

## Notes
- Config: delegated/auto_land/headless
- Do NOT launch ferric-async-forms-r3 — escalation still ACTIVE
- Next code epic after digest update lands: #132 (HTTP Client — Ferric 1.0 http client, usable_early). Depends on #131 (LANDED ✓) and #129 (LANDED ✓).
- The devops DAG (swe-coder) finds the actual image digest from CI run 41803200262 output or the registry — do not guess the digest in the brief
