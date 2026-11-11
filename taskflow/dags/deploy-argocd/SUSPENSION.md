# SUSPENSION.md — deploy-argocd (NSWE #13) — NeedsDecompose

## Disposition

`status: suspended`, `decompose_evaluation: NeedsDecompose`. This root task decomposed into a
hub-and-spoke subtree and now suspends pending its subtree's resolution. It performed NO substantive
deploy work itself.

## Why decompose (triggers that fired)

Evaluated against the actual #13 brief at the decompose-evaluation point:
- **Tool-call envelope**: read-only cluster inspection + image-digest resolution + authoring multiple
  manifests + ArgoCD sync/rollout debugging + HTTP reachability proof + PR authoring far exceeds the
  5–15-call atomic floor. Fired.
- **Scope / Distinct Concerns**: separable specialists — k8s workload authoring vs. ArgoCD/GitOps+RBAC
  authoring vs. deploy-and-verify vs. PR/synthesis. Fired.
- **Single-Responsibility**: faithful description joins distinct verbs (discover → author × 2 → verify
  → integrate) — a serial precursor→author→verify pipeline. Fired.
- Trigger precedence: scope/responsibility win over output-size; `Atomic` was not available.

## Chosen cut (contract-first fan-out + serialized discovery precursor)

Candidate cuts: (A) atomic — rejected by the evaluation; (B) by k8s-object type — rejected
(cross-sibling edges + shared-file writers); (C) **chosen** — discovery precursor → two disjoint
parallel authoring spokes → synthesis gate. Disjoint ownership (hard gate satisfied), minimal
cross-sibling edges, independently revertible/reviewable children.

- Stable seam (names/labels/ports/paths/ArgoCD identities) → FROZEN in `contracts/`.
- Discovery-dependent facts (digest, ingress class, apiVersions, ports) → SERIALIZED via
  `SUBTASK_discovery/outputs/ground_truth.md`.

## Children materialized (via engine_amend_plan add_task)

| Task id | Depends on | Group | Owns |
|---------|------------|-------|------|
| `SUBTASK_discovery` | none | 0 | `outputs/ground_truth.md` |
| `SUBTASK_app_manifests` | `SUBTASK_discovery` | 1 | `deploy/chirp/*` |
| `SUBTASK_argocd_gitops` | `SUBTASK_discovery` | 1 | `deploy/argocd/*` |
| `SUBTASK_synthesis` (synthesis gate) | all three | 2 | `SYNTHESIS.md` + PR + reachability evidence |

## Named state authored

- `_GLOBAL.md` (subtree hub), `contracts/_MANIFEST.yaml`, `contracts/deploy_contract.yaml`
- `SUBTASK_discovery/_BRIEF.md`, `SUBTASK_app_manifests/_BRIEF.md`,
  `SUBTASK_argocd_gitops/_BRIEF.md`, `SUBTASK_synthesis/_BRIEF.md`

## Resumption

Implicit: all child tasks reach a terminal lifecycle state. The synthesis gate folds its
`SYNTHESIS.md` into this parent (`SUSPENDED → COMPLETED`); the owner (`overseer/I49`) gates on that
folded root `SYNTHESIS.md` at the observation seam — never on a side-effect or a force-complete.
