# COMPLETE — pin-image-digest-r1

## Task
Replace the placeholder image digest in `deploy/chirp/10-deployment.yaml` with the
actual digest published by the post-merge CI run for commit `0d5917dc`.

## Outcome
**COMPLETED** — commit `a255baf` pushed to `origin/main`.

## Change
| Field | Value |
|---|---|
| File | `deploy/chirp/10-deployment.yaml` |
| Before | `ghcr.io/nousix-llc/chirp-server@sha256:0000000000000000000000000000000000000000000000000000000000000000` |
| After | `ghcr.io/nousix-llc/chirp-server@sha256:adaa4c26c94d2bffab0342d3dc279eb2d8b42e835494c59385c4b731e246fd41` |
| Commit | `a255baf` |
| Commit message | `deploy(chirp): pin durable image digest for commit 0d5917dc (#180)` |

## Verification
- Digest `sha256:adaa4c26c94d2bffab0342d3dc279eb2d8b42e835494c59385c4b731e246fd41` sourced from:
  - CI run `41687555341` on `Nousix-LLC/nswe-demo`, job `image` (ID 126098384047)
  - Log entry: `pushing manifest for ghcr.io/nousix-llc/chirp-server:sha-0d5917dc6b10d25b15e47a867f41a450239007f6@sha256:adaa4c26c94d2bffab0342d3dc279eb2d8b42e835494c59385c4b731e246fd41`
  - `containerimage.digest: sha256:adaa4c26c94d2bffab0342d3dc279eb2d8b42e835494c59385c4b731e246fd41`
- Comment block updated: placeholder text replaced with provenance note referencing commit + CI run
- ArgoCD (`chirp` Application) will detect the manifest change and reconcile the cluster roll

## Issues
- Closes #180 (pin the durable image digest)
- Unblocks #64 closure (durable PostgreSQL persistence deployment)
