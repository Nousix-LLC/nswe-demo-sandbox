# _BRIEF.md — update-cronjob-digest-r1 (swe-coder)

## Objective

Update the image digest in `deploy/chirp/50-transient-sweep-cronjob.yaml` to the digest of the
newly built `chirp-server` image from the merge commit of PR #183 (`febeb151`).

## Background

PR #183 (`fix(#117): replace psql sweep CronJob with chirp-server sweep subcommand`) merged to main
at commit `febeb151ba50f6c2635d922b5c3da6e01371c617` on 2026-11-03T20:11:06Z. The CI image build
(run 41710206505) completed successfully and published a new `chirp-server` image to GHCR:

```
ghcr.io/nousix-llc/chirp-server@sha256:2c5eafbe4e4009652ec0f0bc3d6aeac594904debcd3776b9dacb6b78ed98e06c
```

The CronJob manifest (`deploy/chirp/50-transient-sweep-cronjob.yaml`) still carries the old image
digest from the prior CI build:

```
ghcr.io/nousix-llc/chirp-server@sha256:adaa4c26c94d2bffab0342d3dc279eb2d8b42e835494c59385c4b731e246fd41
```

The old binary does not implement the `chirp-server sweep` subcommand, so the CronJob fails loudly.
ArgoCD is currently `OutOfSync/Degraded` on `febeb151`. This is the expected interim behavior —
the manifest comment says "update this digest after the post-merge CI run" — and this task is that update.

## Acceptance criteria

1. `deploy/chirp/50-transient-sweep-cronjob.yaml`: the `image:` field reads exactly:
   `ghcr.io/nousix-llc/chirp-server@sha256:2c5eafbe4e4009652ec0f0bc3d6aeac594904debcd3776b9dacb6b78ed98e06c`
2. The image digest in `50-transient-sweep-cronjob.yaml` matches the one in `10-deployment.yaml`
   (both should reference `sha256:2c5eafbe4e4009652ec0f0bc3d6aeac594904debcd3776b9dacb6b78ed98e06c`).
3. All CI checks pass on the branch (fmt/clippy/test/wasm/doc/image — all SUCCESS).
4. A PR is opened on branch `work/update-cronjob-digest-r1` against `main`, titled:
   `fix(ops): update CronJob image digest to febeb151 build (post-merge #183)`

## Scope

- One file to change: `deploy/chirp/50-transient-sweep-cronjob.yaml`
- One line to change: the `image:` field under the `sweep` container spec
- No other files, no Rust code, no logic changes

## Declared output

- A pull request against main with the corrected image digest
- PR URL in SYNTHESIS.md

## Concerns

1. **Correctness**: The digest must be exactly `sha256:2c5eafbe4e4009652ec0f0bc3d6aeac594904debcd3776b9dacb6b78ed98e06c`
   from CI run 41710206505. No typos.
2. **CI gate**: All CI checks must be green before declaring success.
3. **Minimal diff**: Only the image line changes; no other modifications.

## Branch

Use `work/update-cronjob-digest-r1` as the branch name.

## Notes

- No attribution trailers on anything posted to GitHub.
- Do not close issues; the overseer will close them after landing.
- Repo: `Nousix-LLC/nswe-demo`
- Reference: `deploy/chirp/10-deployment.yaml` shows the image reference pattern.
