# _GLOBAL.md — review-update-chirp-server-digest-r1

**DAG**: review-update-chirp-server-digest-r1  
**Reviewer node**: swe-reviewer  
**Decomposition decision**: NeedsDecompose

---

## Context

PR #209 (`Nousix-LLC/nswe-demo`) pins the `chirp-server` container image digest to the build
produced by CI run 41803200262 for commit `d8230fea917dc1228fbb5ccd72bcb7ea79d0bed3`. It changes
one file, `deploy/chirp/10-deployment.yaml`, updating a three-line block (comment + image reference).

The brief enumerates four distinct concerns — Correctness, Deployment Safety, Ops Hygiene, Security —
each drawing on a different primary evidence source. The Distinct Concerns Test fires: different
specialists could verify each concern in parallel. This node decomposes into four parallel concern
spokes and one synthesis hub.

---

## Decomposition

### Concern spokes (run in parallel, no mutual dependencies)

| Child slug | Concern | Primary evidence |
|---|---|---|
| `review-correctness` | Digest matches CI output | GitHub Actions run 41803200262 image job log |
| `review-safety` | Manifest change is deployment-safe | PR diff, full deployment YAML, migration history |
| `review-hygiene` | Ops conventions followed | PR title/description, commit message, YAML comment |
| `review-security` | No forbidden content in diff | PR diff, all changed files |

### Synthesis hub (depends on all four spokes)

| Child slug | Responsibility | Inputs |
|---|---|---|
| `review-synthesis` | Aggregate findings → SYNTHESIS.md + PR comment | FINDINGS.md from each of the four spokes |

---

## Seam Contract

Each concern spoke writes its result to `{child-workspace}/FINDINGS.md`. The format is declared
in `contracts/_MANIFEST.yaml`. The synthesis child reads those four files and produces:

1. `taskflow/dags/review-update-chirp-server-digest-r1/SYNTHESIS.md` (the observation seam)
2. A review comment on PR #209 (`Nousix-LLC/nswe-demo`) carrying the verdict and per-concern findings

---

## Constant Facts

The following facts are confirmed from the Code DAG SYNTHESIS
(`taskflow/dags/update-chirp-server-digest-r1/SYNTHESIS.md`) and the CI record. All concern children
may use them as authoritative inputs — there is no need to re-derive them from scratch; each child
verifies the evidence directly for the concern it owns.

- **PR**: https://github.com/Nousix-LLC/nswe-demo/pull/209
- **PR title**: "deploy(chirp): pin chirp-server image digest to d8230fea build"
- **Issue closed**: #206
- **Changed file**: `deploy/chirp/10-deployment.yaml` (image comment + image reference only)
- **Digest in PR**: `sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f`
- **CI run to verify against**: 41803200262 (commit `d8230fea917dc1228fbb5ccd72bcb7ea79d0bed3`, branch `main`)
- **PR CI run**: 41806003677 (all 6 jobs pass: fmt, clippy, test, wasm, doc, image)
- **Previous digest**: `sha256:adaa4c26c94d2bffab0342d3dc279eb2d8b42e835494c59385c4b731e246fd41`
