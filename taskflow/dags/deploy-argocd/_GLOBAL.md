# _GLOBAL.md — deploy-argocd subtree hub (NSWE #13, swe-coder DAG)

## Project Context

**Status**: Active

### Objective

Close issue **#13 — deploy-argocd**: author the Kubernetes deployment manifests for the `chirp`
application plus an ArgoCD `Application`/`AppProject` so the app auto-syncs onto the live
k3d-hosted k3s cluster via GitOps, **demonstrate the deployed app is actually reachable**, and open
a PR into `main` on branch `work/deploy-argocd` that `Closes #13`. A root `SYNTHESIS.md` carries the
machine-gate PASS/FAIL verdict, the decision record, and the reachability evidence.

The authoritative whole-task spec is this subtree's `_BRIEF.md` (sibling of this file). This hub
records the chosen decomposition, the shared seam (`contracts/`), and the subtree methodology posture.

### Scope

**In scope:**
- `deploy/chirp/` k8s manifests: Namespace, Deployment (`chirp-server`), Service, Ingress (or a
  justified equivalent reachability mechanism for k3s/k3d).
- `deploy/argocd/` ArgoCD `Application` (tracks `deploy/chirp`) + least-privilege `AppProject`.
- Image pinned by immutable `@sha256:` digest resolved from the #11 CI-published package.
- Resource requests/limits, liveness + readiness probes on the app's real health surface, graceful shutdown.
- Demonstrated reachability on the live cluster (evidence captured), imagePullSecret handling if needed.
- Commits on `work/deploy-argocd`, a PR into `main` closing #13, CI green, root `SYNTHESIS.md`.

**Out of scope:**
- The native/systemd production install path (#23 HSO-1) — do NOT take it on; note any manifest
  choice that would differ on a native cluster, but target only the proven k3d-hosted k3s cluster.
- Merging the PR, pushing to `main`, or force-pushing/rewriting merged history.
- Sibling apps/clusters/namespaces or any ArgoCD other than this project's.

### Success Criteria

- [ ] All five `_BRIEF.md` acceptance criteria satisfied and demonstrated.
- [ ] Reachability shown with concrete evidence (HTTP response via the k3d ingress path or a
      justified NodePort/port-forward), not merely asserted.
- [ ] Image referenced by `@sha256:` digest; AppProject is least-privilege (not stock cluster-admin);
      RBAC narrowing is GitOps-managed (survives a `--force-conflicts` infra re-run, #24 SEC-4).
- [ ] PR into `main` opened on `work/deploy-argocd`, `Closes #13`, CI green, **no attribution trailers**.
- [ ] Root `SYNTHESIS.md` present with PASS/FAIL verdict + decision record + reachability evidence.

---

## Constraints and Requirements

### Technical / process constraints (inherited — bind the whole subtree)

- **Repo scope**: `Nousix-LLC/nswe-demo` only. Base is `origin/main @ ada3aa9`. Branch
  `work/deploy-argocd`; PR into `main`. Never force-push `main`; never rewrite merged history.
- **NO attribution trailers** on any commit or the PR body (#27/HYG-1). Keep the PR body accurate
  to what shipped. (This overrides any default "Generated with / Co-Authored-By" footer.)
- **Target cluster only**: k3d cluster `nswe`, k3s v1.35.5+k3s1, ArgoCD in ns `argocd`. The k3d
  serverlb maps host `localhost:8081 -> 80` and `8444 -> 443` through the k3s Traefik ingress.
  Inspect the cluster **read-only** to ground manifests; do not touch sibling apps/clusters.
- **Supply-chain (#24 SEC-3)**: app image pinned by immutable `@sha256:` digest, not a movable tag;
  pin any referenced external manifests/charts by SHA; a cosign/admission follow-up is noted, not
  necessarily implemented.
- **RBAC least-privilege (#24 SEC-2)**: do NOT rely on the stock `application-controller` `*/*/*`
  cluster-admin-equivalent posture; constrain the Application via an AppProject with explicit allowed
  destinations/resources. Express all hardening as GitOps-managed config (#24 SEC-4).
- **Durability caveat (#23 HSO-1)**: assume nothing about a native/systemd cluster; note divergences.
- **No secrets committed** to the tree; namespace isolation; ingress TLS posture appropriate to k3d.
- A DAG never merges its own PR and never pushes to `main`; this subtree is the only writer of its branch.

---

## Methodology

### Subtree Methodology Posture

- **Dominant task types**: this subtree is a k8s/GitOps deploy build. Leaves fall under
  *"Kubernetes workload & API-object design"*, *"GitOps repository topology & app composition
  (Argo CD / Flux)"*, *"Kubernetes RBAC & service-account least-privilege"* /
  *"Image signing & admission-time verification"* (supply chain), and a *"Synthesizing / verifying a
  hub-and-spoke decomposition"* gate that also does *"PR creation and management via gh CLI"*.
- **Primary bundles the subtree draws on** (children SHOULD assume these in scope): `kubernetes`,
  `gitops`, `kubernetes-security`. Supporting: `containerization`, `operations`, `security`,
  `synthesis`, `architecture`, `core`.
- **Cross-cutting bindings** (bind every leaf): supply-chain digest-pinning (`kubernetes-security`
  supply-chain), least-privilege RBAC as GitOps-managed config (`kubernetes-security` RBAC +
  `gitops` reconciliation/drift), and k3s/k3d ingress idiom (`kubernetes` networking). These are
  inherited constraints, not per-leaf choices.
- **Suggestion, not prescription**: each child loads the bundle IDs its brief names plus whatever its
  own reading reveals; it is the final judge of what it loads.

### Analysis Approach — chosen decomposition (contract-first fan-out + serialized discovery precursor)

Candidate cuts considered: (A) single atomic task — rejected at the kernel evaluation (multiple
distinct concerns + tool-call envelope). (B) cut by k8s-object type (one child per manifest) —
rejected: maximizes cross-sibling edges and forces shared-file writers (every child edits the same
app's labels/namespace). (C) **chosen** — a serialized **discovery** precursor that resolves
ground-truth facts, then **two disjoint parallel authoring spokes** (app workload manifests vs.
ArgoCD/GitOps+RBAC), then a **synthesis verification gate** that deploys, proves reachability, and
opens the PR. Cut C has disjoint child ownership (hard gate satisfied), minimal cross-sibling edges,
and independently revertible, reviewable children.

The concrete digest, ingress class, and ArgoCD/AppProject API surface are **discovery-dependent**, so
that seam is **serialized** (discovery → authors). The naming/path/identity seam shared by the two
authoring spokes is **forced/stable**, so it is **frozen** in `contracts/` (read-only to descendants).

---

## Task Structure

### Overview

```
deploy-argocd/
├── _GLOBAL.md                         (this hub)
├── contracts/
│   ├── _MANIFEST.yaml                 (kind, per-child ownership, identities, derived facts)
│   └── deploy_contract.yaml           (frozen shared identities: names, labels, ports, paths)
├── SUBTASK_discovery/_BRIEF.md        (Group 0 — serialized precursor; writes ground_truth.md)
├── SUBTASK_app_manifests/_BRIEF.md    (Group 1 — deps discovery; owns deploy/chirp/*)
├── SUBTASK_argocd_gitops/_BRIEF.md    (Group 1 — deps discovery; owns deploy/argocd/*)
└── SUBTASK_synthesis/_BRIEF.md        (Group 2 — deps all; verification gate, deploy+reachability+PR)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_discovery` | none | Resolve ground-truth facts: repo checkout location; the actual published `ghcr.io/nousix-llc/chirp-server` image `@sha256:` digest from the #11 CI package; the app's real health surface (listen port + health path) from the root `Dockerfile` + `deploy/docker/healthcheck.rs`; live-cluster facts (ingress class/Traefik, ArgoCD version + `AppProject`/`Application` apiVersion, storage, whether the GHCR package is private → imagePullSecret need). Read-only against the cluster. | `outputs/ground_truth.md` |
| `SUBTASK_app_manifests` | `SUBTASK_discovery` | Author `deploy/chirp/` workload manifests: Namespace, Deployment (`chirp-server`, image pinned by the discovered digest, resource requests/limits, liveness+readiness probes on the real health surface, graceful shutdown), Service, Ingress on the k3s Traefik path. Handle imagePullSecret if the package is private. Compose against `contracts/`. | `deploy/chirp/*.yaml` |
| `SUBTASK_argocd_gitops` | `SUBTASK_discovery` | Author `deploy/argocd/` GitOps config: an ArgoCD `Application` tracking repo path `deploy/chirp` into namespace `chirp`, and a least-privilege `AppProject` (explicit allowed destinations/resources, NOT cluster-admin) that the Application references. Keep RBAC narrowing GitOps-managed so a `--force-conflicts` infra re-run cannot silently revert it (#24 SEC-2/SEC-4); pin any referenced external manifests by SHA. Compose against `contracts/`. | `deploy/argocd/*.yaml` |
| `SUBTASK_synthesis` | `SUBTASK_discovery`, `SUBTASK_app_manifests`, `SUBTASK_argocd_gitops` | Verification gate: run the four-check model over the combined manifests + contract identities; deploy/sync onto the live k3d cluster and **demonstrate reachability** (capture the HTTP evidence); resolve any ImagePullBackOff/probe failures (remediation-as-decomposition if needed); commit on `work/deploy-argocd`, open the PR into `main` that `Closes #13` (no attribution trailers), confirm CI; author the root `SYNTHESIS.md` fold record with PASS/FAIL + decision record + reachability evidence. | `SYNTHESIS.md` (at this subtree root) |

### Dependency Graph

```
SUBTASK_discovery ──┬── SUBTASK_app_manifests ──┐
                    └── SUBTASK_argocd_gitops  ──┼── SUBTASK_synthesis
                                                 ┘
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (a shared-identity manifest of agreed names/ports/paths) + identities.

### Inherited Contracts

None — this is the root decomposition of the deploy-argocd DAG.

### Structural Declarations

`contracts/deploy_contract.yaml` fixes the identities both authoring spokes must agree on so the
manifests mechanically compose (namespace, app name + labels, Service name/port/targetPort, Ingress
host/path + class source, container listen port source, ArgoCD Application + AppProject names,
destination namespace, and the repo path layout `deploy/chirp` vs `deploy/argocd`). See
`contracts/_MANIFEST.yaml` for ownership + identities; both are read-only to descendants.

### Ownership

| Artifact (repo-relative) | Owning subtask |
|---|---|
| `outputs/ground_truth.md` (resolved facts incl. image digest) | `SUBTASK_discovery` |
| `deploy/chirp/*.yaml` (Namespace, Deployment, Service, Ingress) | `SUBTASK_app_manifests` |
| `deploy/argocd/*.yaml` (Application, AppProject) | `SUBTASK_argocd_gitops` |
| `SYNTHESIS.md` + the PR + deploy/reachability evidence | `SUBTASK_synthesis` |

The two authoring spokes write to **disjoint** directories (`deploy/chirp/` vs `deploy/argocd/`); no
two children write the same file. The ArgoCD `Application` tracks `deploy/chirp` only, so it does not
manage its own manifests (which live in `deploy/argocd/`, outside the synced path).

### Identities (the synthesis gate asserts these; no silent plug)

- [ ] Deployment container image is `ghcr.io/nousix-llc/chirp-server@sha256:<digest>` where `<digest>`
      equals the digest recorded in `outputs/ground_truth.md` — an immutable digest, never a movable tag.
- [ ] Service `.spec.selector` matches the Deployment pod-template labels; Service `targetPort` equals
      the container listen port recorded in `ground_truth.md`.
- [ ] Ingress backend references the Service by name + port; Ingress class matches the cluster's
      (from `ground_truth.md`); the path is reachable via the k3d serverlb (`localhost:8081`).
- [ ] Deployment declares resource **requests AND limits** and **liveness + readiness** probes on the
      app's real health surface (from `ground_truth.md`); graceful-shutdown posture set.
- [ ] ArgoCD `Application.spec.source.path == deploy/chirp`, `repoURL` is the nswe-demo repo, and
      `destination.namespace == chirp`; the Application references the project `AppProject` (NOT `default`).
- [ ] `AppProject` restricts `destinations` to the chirp namespace (+ `argocd` only if required) and
      does not grant a cluster-admin-equivalent `*/*/*` posture; narrowing is GitOps-managed.
- [ ] All chirp resources live in namespace `chirp`; a Namespace manifest exists; no secrets are
      committed to the tree; if the GHCR package is private, an imagePullSecret path is handled (no
      ImagePullBackOff) or the package is documented as made pullable.

### Derived Facts (serialized, not mocked)

`outputs/ground_truth.md` (image digest, container port, health path, ingress class, ArgoCD/AppProject
apiVersion, pull-secret need, repo checkout path) is the serialized precursor both authoring spokes
read. There are no runtime mocks — the seam is a naming/identity agreement, and the real join is
verified by the synthesis gate via actual deploy + reachability.

### Thin-Seam Note

The seam is deliberately small (shared identities + path layout). It is frozen, not absent: without it
the two spokes would diverge on namespace/labels/ports/paths and the Application would point at the
wrong path. The discovery-dependent facts are serialized rather than frozen, per the stability heuristic.

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| Ground-truth facts | Markdown | `outputs/ground_truth.md` | Pinned digest + cluster/app facts |
| App workload manifests | YAML | `deploy/chirp/` | Namespace, Deployment, Service, Ingress |
| GitOps config | YAML | `deploy/argocd/` | ArgoCD Application + least-privilege AppProject |
| Fold record | Markdown | `SYNTHESIS.md` (subtree root) | PASS/FAIL verdict, decision record, reachability evidence, PR link |
