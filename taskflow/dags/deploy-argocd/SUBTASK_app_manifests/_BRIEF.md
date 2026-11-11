# Task: Author the chirp app Kubernetes workload manifests

## Task Specification

**Slug**: SUBTASK_app_manifests
**Task Kind**: standard
**Status**: Pending

### Objective

Author the Kubernetes manifests under `deploy/chirp/` that run the `chirp-server` app on the k3s
cluster and make it reachable from outside: a Namespace, a Deployment, a Service, and an Ingress (or
a justified equivalent k3s/k3d reachability mechanism).

### Context

Part of the deploy-argocd subtree (NSWE #13) — see `../_GLOBAL.md` and `../contracts/`. You own the
`deploy/chirp/` directory exclusively; the GitOps/ArgoCD config is a disjoint sibling
(`SUBTASK_argocd_gitops`, owns `deploy/argocd/`). Compose against the frozen identities in
`../contracts/deploy_contract.yaml`; do not invent divergent names/ports/labels.

**Dependencies**: `SUBTASK_discovery`.
**Dependents**: `SUBTASK_synthesis`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Scope, constraints |
| Contract | `../contracts/deploy_contract.yaml`, `../contracts/_MANIFEST.yaml` | Frozen names/ports/labels/paths + the identities you must satisfy |
| Ground-truth facts | `../SUBTASK_discovery/outputs/ground_truth.md` | Image digest, container listen port, health path, ingress class, repo checkout path, pull-secret need |

### Input Verification
- [ ] Contract and `ground_truth.md` readable; image digest and container port present.

---

## Process Specification

This task covers several facets of ONE workload definition; treat them as the aspects to get right,
and evaluate for yourself whether they warrant further decomposition:

- **Namespace + Deployment**: `chirp-server` Deployment in namespace `chirp`, image pinned by the
  `@sha256:` digest from `ground_truth.md`; resource **requests AND limits**; **liveness + readiness**
  probes targeting the real health surface; graceful-shutdown posture (termination grace, preStop if
  warranted). Handle the imagePullSecret if `ground_truth.md` says the package is private (or document
  the package being made pullable) so the pod does not wedge in ImagePullBackOff.
- **Service**: ClusterIP selecting the Deployment pods; port/targetPort per the contract + real port.
- **Ingress (reachability)**: route external traffic through the k3s Traefik ingress using the
  cluster's ingress class from `ground_truth.md`, reachable via the k3d serverlb
  (`localhost:8081 -> 80`). If you choose a host-based rule, record the exact host so the synthesis
  gate can reach it (Host header); if path-based, record the path. A NodePort/port-forward is an
  acceptable alternative ONLY with a recorded justification.

Idiomatic, minimal, declarative, reconcilable manifests a k3s/ArgoCD reviewer expects. Note (in a
comment or a short README you own under `deploy/chirp/`) any manifest choice that would differ on a
native/systemd cluster (#23 HSO-1) — but target only k3d-hosted k3s.

### Methodology
Apply the suggested bundles below. Compose against `../contracts/` literally — do not paraphrase it.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Location | `deploy/chirp/` (in the repo checkout from `ground_truth.md`) |
| Files | Namespace, Deployment, Service, Ingress manifests (YAML); optional short `README.md` you own |

Declare the concrete file paths you produce as your task outputs.

---

## Success Criteria

- [ ] `deploy/chirp/` contains a Namespace, a Deployment (`chirp-server`), a Service, and an Ingress
      (or justified equivalent).
- [ ] Image pinned by the `@sha256:` digest from `ground_truth.md` (no movable tag).
- [ ] Deployment declares requests + limits and liveness + readiness probes on the real health surface.
- [ ] Service selector matches pod labels; Ingress references the Service by name+port with the
      correct ingress class; the external reachability path (and host/path to test) is recorded.
- [ ] imagePullSecret handled or package documented pullable; no secrets committed to the tree.
- [ ] Manifests satisfy the contract identities relevant to the workload (see `_MANIFEST.yaml`).

---

## Suggested Methodology Files

SUGGESTIONS — load as a starting point; you are the final judge.

- Task-type rows: *"Kubernetes workload & API-object design"* (primary `kubernetes`; supporting
  `architecture`); *"Kubernetes Service / Ingress vs Gateway API"* (`kubernetes` networking);
  *"Kubernetes requests/limits & QoS"* (`kubernetes` scheduling).
- Bundle IDs: `kubernetes` (`K8s_Workloads_And_API_Objects_Methodology.md`,
  `K8s_Networking_And_Service_Connectivity_Methodology.md`,
  `K8s_Scheduling_And_Resource_Model_Methodology.md`,
  `K8s_Configuration_Management_Methodology.md`), `kubernetes-security`
  (`K8sSecurity_Supply_Chain_Security_Methodology.md` for digest pinning; secrets hygiene),
  `containerization` (reading the image's runtime/health), `core` (standards).
- Rationale: workload/API-object + networking + resource-model cover Deployment/Service/Ingress and
  probes; supply-chain covers digest pinning; secrets hygiene keeps the tree clean.
- These are the parent's flagged methodologies based on task type; load more/fewer per your reading.

## Inherited Constraints

- Namespace is `chirp`; app/label/Service names and the `deploy/chirp` path are FROZEN in
  `../contracts/deploy_contract.yaml` — compose against them; request an additive amendment if one is
  genuinely wrong (do not edit the read-only contract).
- Image pinned by immutable `@sha256:` digest (#24 SEC-3). No secrets committed.
- You own ONLY `deploy/chirp/`. Do NOT write `deploy/argocd/` (sibling) or any ArgoCD manifest.
- Target k3d-hosted k3s only (#23 HSO-1): assume nothing about a native cluster; note divergences.

## Out-of-Scope Methodologies

- ArgoCD `Application`/`AppProject` authoring and RBAC least-privilege design belong to
  `SUBTASK_argocd_gitops` — do not author GitOps/RBAC config here.
- Deploying to the cluster and opening the PR belong to the synthesis gate — do not `kubectl apply`
  or run git/gh here; produce manifests only.
