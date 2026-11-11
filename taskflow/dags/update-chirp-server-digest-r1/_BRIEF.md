# _BRIEF.md — update-chirp-server-digest-r1 (swe-coder)

## Objective
Update `deploy/10-deployment.yaml` to pin the chirp-server container image to the digest from
the CI "image" job on commit `d8230fea` (GitHub Actions run 41803200262, repo Nousix-LLC/nswe-demo).

## Background
The deployed chirp-server pod is running sha256:adaa4c26... which predates PRs #182/#183/#188/#203.
PRs that contain argon2id credential hashing, sweep subcommand, Ferric 1.0 authoring model, and
router are merged but NOT running in the deployed image. Issue #208 tracks this gap.

## Acceptance criteria
- `deploy/10-deployment.yaml`: chirp-server container image updated to the digest from CI run 41803200262
  (the "image" job built from commit d8230fea). Find the exact SHA256 digest from the CI run artifacts
  or from the GitHub Container Registry (ghcr.io/nousix-llc/nswe-demo, tag d8230fea or the run's output).
- CI: all 6 jobs PASS (fmt, clippy, test, wasm, doc, image) on a branch `work/update-chirp-server-digest-r1`
- PR open against main on Nousix-LLC/nswe-demo, titled: `deploy(chirp): pin chirp-server image to d8230fea build (CI run 41803200262)`
- PR body references issue #208

## Declared output
- Branch: `work/update-chirp-server-digest-r1`
- PR on Nousix-LLC/nswe-demo targeting main, title as above, body references #208
- `deploy/10-deployment.yaml` updated with correct chirp-server image digest
- All 6 CI jobs green
- Root `SYNTHESIS.md` accounting for all acceptance criteria (met or not met and why)

## Scope
Devops only — this is a one-line manifest change (the image digest in `deploy/10-deployment.yaml`).
No Rust code changes. No test changes. No other files unless the image tag/digest format requires
updating a companion file.

## Inputs
- Repo: Nousix-LLC/nswe-demo, default branch: main
- Current main HEAD: d8230fea917dc1228fbb5ccd72bcb7ea79d0bed3
- CI run: 41803200262 (GitHub Actions run on commit d8230fea) — image job built the chirp-server image
- Registry: ghcr.io/nousix-llc/nswe-demo
- Reference PR: #187 (pinned the sweep CronJob digest in a similar devops update — `deploy/50-transient-sweep-cronjob.yaml`)
- Current `deploy/10-deployment.yaml` chirp-server image: sha256:adaa4c26...

## Notes
- This is a devops digest update analogous to PR #187 (which pinned the sweep CronJob digest)
- The CI image job builds and pushes a ghcr.io image on every main push; find the d8230fea digest
  from run 41803200262 output or from the registry (tag d8230fea or the digest on the ghcr.io package page)
- Do not guess the digest — find the actual SHA256 from CI run 41803200262 or the registry
- Constraints: no force-push; PR must be clean and mergeable against main
