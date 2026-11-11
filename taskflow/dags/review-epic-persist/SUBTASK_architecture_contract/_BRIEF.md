# Task: Architecture / contract stability — PR #113

## Task Specification

**Slug**: SUBTASK_architecture_contract
**Task Kind**: standard
**Status**: Pending

### Objective

Judge whether the change keeps the shared seam's contract and the public/operational surface stable and
coherent, and whether the additive deployment changes are correct and minimal.

### Context

Part of the PR #113 review DAG (see `../_GLOBAL.md`). This concern owns the *contract shape* of the
`ChirpRepository` seam and the *deployment contract*; behavioral correctness of the seam is the correctness
concern's. Read-only; write a findings document only.

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Pinned commit, target, constraints |
| Contract | `../contracts/finding_schema.md`, `../contracts/_MANIFEST.yaml` | Findings format + rubric |
| PR #113 diff @ `09fa453` | `gh pr diff 113` / `git` (read-only) | Seam definition, manifests, AppProject |
| Issue #66 | `gh issue view 66` | The `ChirpRepository` seam criterion |
| Design | `design/domain-application-design.md`, `design/operational-readiness.md` | Seam + deployment contract of record |

## The bar

A finding when the seam's contract or the public/operational surface drifts or becomes incoherent, or when
the deployment changes are incorrect or non-minimal. Examine at least:

- `ChirpRepository` seam contract: does the durable backend sit behind the *existing* seam without widening,
  weakening, or forking it? Is the capability set complete at the contract level?
- Deployment contract: manifests, the ArgoCD AppProject, probes moving to `/readyz`.
- The additive AppProject changes — `StatefulSet`, `PersistentVolumeClaim`, `CronJob` — are they correct and
  **minimal** (nothing added beyond what the durable store requires)?

## Output

`SUBTASK_architecture_contract/outputs/findings.md`, conforming to `../contracts/finding_schema.md` (prefix
`ARC`).

## Success criteria

- [ ] Seam-contract stability and deployment-contract coherence assessed; AppProject additions judged for
  correctness and minimality.
- [ ] "What I checked" / "what I found clean" both specific.
- [ ] Findings pinned, severities + `blocks_landing` honest, each with "what would satisfy me"; sub-verdict.

## Constraints

Read-only on the repo; no GitHub writes. No host/cluster/SSH/credential details or DAG internals. Plain voice.
