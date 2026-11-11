## Verdict

PASS

## Evidence

**CI run 41803200262 (head: `d8230fea917dc1228fbb5ccd72bcb7ea79d0bed3`, branch: `main`)**

The image job (job ID 126484056562, step "Build chirp-server image (push on `main`, build-only on PR)") completed with:

- `##[group]Digest`: `sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f`
- `containerimage.digest` (from build-push-action metadata): `sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f`
- Manifest pushed as: `ghcr.io/nousix-llc/chirp-server:latest@sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f`
- Manifest pushed as: `ghcr.io/nousix-llc/chirp-server:sha-d8230fea917dc1228fbb5ccd72bcb7ea79d0bed3@sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f`

The "Summarize published image" step wrote: `- digest: sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f`

**Deployment manifest** (`deploy/chirp/10-deployment.yaml` on branch `deploy/update-chirp-server-digest-d8230fea`):

```
image: ghcr.io/nousix-llc/chirp-server@sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f
```

**Comparison**

| Source | Digest |
|--------|--------|
| CI image job (published) | `sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f` |
| Manifest (PR branch) | `sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f` |

Byte-for-byte match.

**Additional checks**

- Image reference format: `registry/name@sha256:<64-hex-chars>` — well-formed; no movable tag.
- CI run head SHA: `d8230fea917dc1228fbb5ccd72bcb7ea79d0bed3` — matches the claimed commit.
- CI run branch: `main` — matches the claim.

## Findings

None.
