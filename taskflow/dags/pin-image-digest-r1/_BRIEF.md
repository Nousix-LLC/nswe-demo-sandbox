# _BRIEF.md — pin-image-digest-r1 (swe-coder)

## Objective

Pin the chirp-server production image digest in `deploy/chirp/10-deployment.yaml` so ArgoCD can deploy the postgres-enabled binary to the cluster.

## Background

PR #113 (EPIC-PERSIST durable store) merged to main at commit `0d5917dc` with a placeholder image digest `sha256:0000000000000000000000000000000000000000000000000000000000000000` in the deployment manifest. The post-merge CI run (41687555341) built and published the correct postgres-enabled image:

```
ghcr.io/nousix-llc/chirp-server@sha256:adaa4c26c94d2bffab0342d3dc279eb2d8b42e835494c59385c4b731e246fd41
```

The cluster is currently running the old in-memory-backed image (`sha256:054af27f...`); the new deployment pods fail with `ImagePullBackOff` because they reference the placeholder. Postgres is running (`chirp-postgres-0 1/1 Running`) and `chirp-db-credentials` Secret is in place.

## Acceptance criteria

- `deploy/chirp/10-deployment.yaml`: the `image:` field for the `chirp-server` container reads exactly:
  `ghcr.io/nousix-llc/chirp-server@sha256:adaa4c26c94d2bffab0342d3dc279eb2d8b42e835494c59385c4b731e246fd41`
- All CI checks pass on the branch
- PR is created against main, titled: `deploy: pin chirp-server image digest (durable-store build)`
- PR body references issue #180 and issue #64

## Scope

- One file to change: `deploy/chirp/10-deployment.yaml`
- One line to change: the `image:` field under the `chirp-server` container spec
- No other files, no Rust code, no logic changes

## Declared output

- A pull request against main with the corrected image digest
- PR URL in SYNTHESIS.md

## Concerns

1. **Correctness**: Verify the digest is the exact value from CI run 41687555341 (confirmed above). No typos.
2. **CI gate**: All CI checks must be green before declaring success.
3. **Minimal diff**: Only the image line changes; no other modifications.

## Branch

Use `work/pin-image-digest` as the branch name.

## Notes

- No attribution trailers on anything posted to GitHub.
- Do not close issues; the overseer will close them after landing.
