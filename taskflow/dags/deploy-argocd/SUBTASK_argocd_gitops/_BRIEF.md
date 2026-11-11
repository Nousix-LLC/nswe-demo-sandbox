# Task: Author the ArgoCD Application + least-privilege AppProject (GitOps)

## Task Specification

**Slug**: SUBTASK_argocd_gitops
**Task Kind**: standard
**Status**: Pending

### Objective

Author the GitOps config under `deploy/argocd/`: an ArgoCD `Application` that tracks this repo's
`deploy/chirp` path and syncs the chirp app into namespace `chirp`, scoped through a least-privilege
`AppProject` (explicit allowed destinations/resources — NOT the stock cluster-admin posture).

### Context

Part of the deploy-argocd subtree (NSWE #13) — see `../_GLOBAL.md` and `../contracts/`. You own the
`deploy/argocd/` directory exclusively; the app workload manifests are a disjoint sibling
(`SUBTASK_app_manifests`, owns `deploy/chirp/`). Compose against the frozen identities in
`../contracts/deploy_contract.yaml` (Application name, project name, source path, destination).

**Dependencies**: `SUBTASK_discovery`.
**Dependents**: `SUBTASK_synthesis`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Scope, constraints |
| Contract | `../contracts/deploy_contract.yaml`, `../contracts/_MANIFEST.yaml` | Frozen ArgoCD names/paths/destination + identities you must satisfy |
| Ground-truth facts | `../SUBTASK_discovery/outputs/ground_truth.md` | ArgoCD/AppProject `apiVersion`, repo checkout path, cluster destination server |

### Input Verification
- [ ] Contract and `ground_truth.md` readable; ArgoCD `apiVersion` surface present.

---

## Process Specification

This task has two tightly related security-sensitive facets; get both right and decide for yourself
whether they warrant further decomposition:

- **ArgoCD `Application`**: tracks `repoURL` = the nswe-demo repo, `source.path = deploy/chirp`,
  `destination.namespace = chirp`, `destination.server` = the in-cluster API; `spec.project` = the
  `chirp` AppProject (NOT `default`). Set a sensible sync policy (automated sync/prune/self-heal is
  the GitOps idiom — justify your choice). Pin any referenced external manifests/charts by SHA
  (#24 SEC-3). The Application + AppProject live in `deploy/argocd/`, OUTSIDE the synced `deploy/chirp`
  path, so ArgoCD does not manage its own definition.
- **Least-privilege `AppProject` (#24 SEC-2 / SEC-4)**: restrict `destinations` to the chirp
  namespace on the in-cluster server (+ `argocd` only if genuinely required); constrain the
  `clusterResourceWhitelist` / `namespaceResourceWhitelist` to what chirp actually needs — do NOT
  leave a `*/*/*` cluster-admin-equivalent posture. Ensure this narrowing is itself GitOps-managed
  (committed, reconcilable) so a re-run of the #10 infra install path with `--force-conflicts` cannot
  silently revert it. Note (do not necessarily implement) a cosign/admission-verification follow-up.

Declarative, idempotent, reconcilable manifests a k3s/ArgoCD reviewer expects. Note any choice that
would differ on a native cluster (#23 HSO-1) — but target only k3d-hosted k3s.

### Methodology
Apply the suggested bundles below. Compose against `../contracts/` literally — do not paraphrase it.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Location | `deploy/argocd/` (in the repo checkout from `ground_truth.md`) |
| Files | `Application` manifest + `AppProject` manifest (YAML); optional short `README.md` you own |

Declare the concrete file paths you produce as your task outputs.

---

## Success Criteria

- [ ] `deploy/argocd/` contains an ArgoCD `Application` (tracking `deploy/chirp` into ns `chirp`) and
      an `AppProject` the Application references via `spec.project`.
- [ ] The `AppProject` is least-privilege: explicit scoped destinations/resources, NO `*/*/*`
      cluster-admin-equivalent grant; the narrowing is GitOps-managed/committed (survives
      `--force-conflicts`).
- [ ] Any referenced external manifests/charts pinned by SHA; a cosign/admission follow-up noted.
- [ ] Manifests satisfy the contract identities `argocd-application-wired` and
      `appproject-least-privilege`. No secrets committed.

---

## Suggested Methodology Files

SUGGESTIONS — load as a starting point; you are the final judge.

- Task-type rows: *"GitOps repository topology & app composition (Argo CD / Flux)"* (primary
  `gitops`); *"Kubernetes RBAC & service-account least-privilege"* (`kubernetes-security`);
  *"GitOps reconciliation / drift & self-heal control"* (`gitops`); *"GitOps secrets management"*
  if any secret surface arises (`gitops` + `security`).
- Bundle IDs: `gitops` (`GitOps_Repository_Topology_And_App_Composition_Methodology.md`,
  `GitOps_Reconciliation_And_Drift_Control_Methodology.md`), `kubernetes-security`
  (`K8sSecurity_RBAC_And_Service_Accounts_Methodology.md`,
  `K8sSecurity_Supply_Chain_Security_Methodology.md`), `security` (config hygiene),
  `kubernetes` (Application/AppProject as CRDs).
- Rationale: GitOps topology covers the Application+AppProject composition and sync policy;
  k8s-security RBAC covers the least-privilege AppProject scoping (#24 SEC-2/4); supply-chain covers
  SHA-pinning referenced manifests (#24 SEC-3).
- These are the parent's flagged methodologies based on task type; load more/fewer per your reading.

## Inherited Constraints

- ArgoCD Application name `chirp`, AppProject name `chirp`, source path `deploy/chirp`, destination
  namespace `chirp` are FROZEN in `../contracts/deploy_contract.yaml` — compose against them; request
  an additive amendment if one is genuinely wrong (do not edit the read-only contract).
- Do NOT rely on the stock application-controller cluster-admin posture; least-privilege is mandatory.
- Hardening MUST be GitOps-managed (#24 SEC-4). No secrets committed.
- You own ONLY `deploy/argocd/`. Do NOT write `deploy/chirp/` (sibling) or any workload manifest.
- Target k3d-hosted k3s only (#23 HSO-1): assume nothing about a native cluster; note divergences.

## Out-of-Scope Methodologies

- Workload manifest authoring (Deployment/Service/Ingress/probes/resources) belongs to
  `SUBTASK_app_manifests` — do not author those here.
- Applying to the cluster, proving reachability, and opening the PR belong to the synthesis gate — do
  not `kubectl apply`/`argocd app sync` or run git/gh here; produce manifests only.
