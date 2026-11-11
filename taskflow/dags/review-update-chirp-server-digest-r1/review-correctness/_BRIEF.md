# _BRIEF.md — review-digest-r1-correctness

**Kind**: review concern (atomic)  
**Concern**: Digest Correctness  
**Parent DAG**: review-update-chirp-server-digest-r1

---

## Objective

Verify that the container image digest in PR #209's `deploy/chirp/10-deployment.yaml` matches
the image published by CI run 41803200262 for commit `d8230fea917dc1228fbb5ccd72bcb7ea79d0bed3`.

---

## Scope

**Digest under review**: `sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f`  
**Image reference in PR**: `ghcr.io/nousix-llc/chirp-server@sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f`  
**CI run to check**: 41803200262 (`Nousix-LLC/nswe-demo`, head commit `d8230fea917dc1228fbb5ccd72bcb7ea79d0bed3`, branch `main`)

What to establish:
- The image job in CI run 41803200262 published the digest that appears in the PR manifest
- The image reference format is well-formed: `registry/name@sha256:<64-hex-chars>`
- The CI run's head SHA and branch are what the comment claims (`d8230fea`, `main`)

Evidence sources:
- GitHub Actions run 41803200262: use `gh run view 41803200262 --repo Nousix-LLC/nswe-demo --log` or
  the GitHub API to read the image job log and extract the published digest
- PR #209 manifest: `deploy/chirp/10-deployment.yaml` on branch `deploy/update-chirp-server-digest-d8230fea`

---

## Declared Output

`taskflow/dags/review-update-chirp-server-digest-r1/review-correctness/FINDINGS.md`

Format: per `taskflow/dags/review-update-chirp-server-digest-r1/contracts/_MANIFEST.yaml`
- `## Verdict` — PASS or FAIL
- `## Evidence` — the log lines or API response that show the digest; the image reference as it
  appears in the manifest; the comparison result
- `## Findings` — None, or a list of discrepancies (blocker if digest does not match)

---

## Success Criteria

The concern is satisfied (PASS) when: the digest in the manifest byte-for-byte matches the digest
published in the image job log for CI run 41803200262; the image reference format is correct; and
the CI run's head SHA matches `d8230fea917dc1228fbb5ccd72bcb7ea79d0bed3`.

A mismatch on the digest is a blocking finding.
