# Task: GitOps control-plane install (ArgoCD)

## Task Specification
**Slug**: SUBTASK_gitops_argocd
**Task Kind**: standard
**Status**: Pending

### Objective
Install **ArgoCD** into its own namespace on the k3s cluster, prove its core workloads reach Ready,
and document how to reach the API/UI and RETRIEVE the initial admin credential (without committing any
secret) — delivered as a reproducible declarative install + an honest evidence record, with a
least-privilege RBAC posture noted. Make the control plane **ready for** a later `Application` (#13)
**without** authoring that Application here.

### Context
Part of infra-bootstrap (#10) — see `../_GLOBAL.md` and `../contracts/`. This is the GitOps
control-plane concern only. It installs INTO the cluster that `SUBTASK_cluster_k3s` stood up, so it
**depends on** that task. It does NOT create any ArgoCD `Application`, app manifests, or containers
(those are #13/#12).

**Dependencies**: `SUBTASK_cluster_k3s`. **Dependents**: `SUBTASK_synthesis_gate`.

## Inputs
- `../_GLOBAL.md` — objective, constraints, environment facts.
- `../contracts/_MANIFEST.yaml` + `../contracts/result_record.schema.md` — owned paths + `RESULT.md`
  schema (read-only).
- The running k3s cluster from `SUBTASK_cluster_k3s` (declared dependency — assume its kubeconfig
  access, per that spoke's documented retrieval path, is available when you run; do not re-provision
  the cluster). If the cluster criterion was BLOCKED upstream, your install will likewise be
  BLOCKED — report it honestly against the real environment fact.

## Scope / what to deliver
- A reproducible, idempotent-where-feasible **ArgoCD install** (prefer a declarative manifest install
  pinned to a specific ArgoCD version, into a dedicated namespace e.g. `argocd`), a **readiness-
  verification script** (core ArgoCD workloads Ready), and an **access runbook fragment**: how to
  reach the API/UI (e.g. port-forward) and how to RETRIEVE the initial admin credential at runtime —
  plus a short **RBAC/least-privilege posture** note. Record the **ArgoCD version**.
- Stage repo-destined files under `staged/deploy/bootstrap/gitops/`. Write `RESULT.md` per schema. No
  git; the synthesis gate owns it.
- Own and record the **argocd** criterion in `RESULT.md` (`owns-criteria: [argocd]`).

### Honest-outcome rule
If the cluster is unavailable or the install is blocked (no cluster, no egress to pull ArgoCD images,
etc.): deliver the reproducible install manifest/script and mark the argocd criterion **BLOCKED** with
the exact blocker + remediation. Never claim ArgoCD pods Ready without a real check.

### Security (sharpened for this spoke)
Document credential RETRIEVAL only (e.g. the command to read the bootstrap admin secret at runtime);
never stage or commit the credential value. Note the least-privilege/RBAC posture (service-account
scope ArgoCD runs under) without over-provisioning. No kubeconfig with live credentials in any file.

## Success Criteria
- [ ] Staged ArgoCD install + verification scripts/manifests exist, each with prereqs/re-run headers; install pinned to a specific ArgoCD version in a dedicated namespace.
- [ ] `RESULT.md`: `argocd` criterion PASS (evidence: the readiness command + observed Ready workloads) OR BLOCKED (blocker + remediation); ArgoCD version recorded; `confirmed-no-secrets: true`; access + credential-retrieval documented; RBAC posture noted.
- [ ] No ArgoCD `Application`, no app deploy manifests, no container builds (that is #13/#12).

## Suggested Methodology Files
Parent's Domain-Mapping reading (**GitOps control plane (Argo CD)**; primary **GitOps**, supporting
**Kubernetes**, **Kubernetes Security**, **Security**). Load on-demand:
- `gitops` — primary. `gitops/GitOps_Repository_Topology_And_App_Composition_Methodology.md`
  (ArgoCD install posture + readiness for a later Application) and
  `gitops/GitOps_Reconciliation_And_Drift_Control_Methodology.md`. Rationale: install the control
  plane healthy and ready, without building the Application.
- `kubernetes` — `kubernetes/K8s_Configuration_Management_Methodology.md`,
  `kubernetes/K8s_Networking_And_Service_Connectivity_Methodology.md`. Rationale: namespace install +
  reaching the API/UI (port-forward/service).
- `kubernetes-security` — `kubernetes-security/K8sSecurity_RBAC_And_Service_Accounts_Methodology.md`,
  `kubernetes-security/K8sSecurity_Secrets_Protection_Methodology.md`. Rationale: least-privilege RBAC
  posture + safe handling of the initial admin credential.
- `security` — `security/Confidential_Data_Custody_Multi_Tenant_Methodology.md`. Rationale: runtime
  credential retrieval rather than committed secrets.

*Parent's flags, not exclusive — you are the final judge of what you load.*

## Inherited Constraints
All of `../_GLOBAL.md §Subtree-Wide Constraints` bind you (infra-only; no secrets; reproducible;
honest reporting; repo scope; stage-only, no git). Compose against `../contracts/` literally; request
an additive amendment rather than deviating.

## Out-of-Scope Methodologies
`rust/*` / `frontend/*` (the wasm spoke), `synthesis/*` (the gate), containerization/* and any app
`Application`/Deployment-manifest methodology (#12/#13). Install the control plane; do not deploy the app.
