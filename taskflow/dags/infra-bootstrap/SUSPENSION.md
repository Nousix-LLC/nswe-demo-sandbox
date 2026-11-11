# SUSPENSION.md — infra-bootstrap (#10) root: NeedsDecompose

**Task**: `infra-bootstrap` (DAG root for work-item #10, EPIC #3 devops)
**Status**: SUSPENDED — `decompose_evaluation = NeedsDecompose`
**When**: 2026-10-07

## Why decomposed
The #10 brief enumerates six concerns and spans three distinct system components
(k3s cluster / ArgoCD control plane / wasm build toolchain), each binding a different methodology.
The Scope-Based trigger (enumerated distinct concerns + multiple components + multiple
methodologies), the Single-Responsibility conjunction test (provision-cluster *and* install-control-
plane *and* enable+prove-toolchain *and* deliver-PR), and the Output-Size trigger all fire. Per
trigger precedence these win over any "one cohesive deliverable" instinct → NeedsDecompose.

## Cut chosen
By component + a single synthesis gate (candidate B): disjoint path ownership under
`deploy/bootstrap/`, minimal edges (only the runtime argocd→k3s serialize), each child independently
reviewable. Layer-cut (A) and merged-cluster+gitops (C) were rejected (ownership-overlap / single-
responsibility violation). Rationale recorded in `_GLOBAL.md §Chosen Cut`.

## Children materialized (via engine_amend_plan add_task)
| Task id | Group | Depends on | Kind |
|---------|-------|------------|------|
| `SUBTASK_cluster_k3s` | 0 | none | standard |
| `SUBTASK_wasm_toolchain` | 0 | none | standard |
| `SUBTASK_gitops_argocd` | 1 | `SUBTASK_cluster_k3s` | standard |
| `SUBTASK_synthesis_gate` | 2 | all three spokes | synthesis |

## Contract (frozen seam)
`contracts/_MANIFEST.yaml` (kind `yaml_schema`): path-ownership partition + identities I1–I6
(criteria coverage, no committed secrets, reproducibility, versions recorded, honest blockers,
infra-only scope) + seam classification (argocd→k3s = SERIALIZE; spokes→gate = FREEZE).
`contracts/result_record.schema.md`: the per-spoke `RESULT.md` evidence record the gate enumerates.

## Resumption
Implicit: resolve when the entire subtree reaches terminal states. The `SUBTASK_synthesis_gate` fold
produces the root `SYNTHESIS.md` verdict + the PR into `main` that Closes #10 (PR not merged; `main`
not pushed — the overseer lands). Honest PASS-with-documented-blocker is an acceptable terminal
outcome if the host/sandbox forbids the k3s/ArgoCD install.
