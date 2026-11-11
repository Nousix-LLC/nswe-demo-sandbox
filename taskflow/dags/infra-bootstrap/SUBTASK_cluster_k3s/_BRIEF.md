# Task: Cluster provisioning & verification (k3s)

## Task Specification
**Slug**: SUBTASK_cluster_k3s
**Task Kind**: standard
**Status**: Pending

### Objective
Produce a reproducible **k3s** install and a **real** readiness proof for the engagement's
deployment cluster, and document kubeconfig access — delivering the reproducible script set plus an
honest evidence record of what actually happened on this host.

### Context
Part of infra-bootstrap (#10) — see `../_GLOBAL.md` (hub) and `../contracts/` (frozen seam). This is
the cluster concern only: ArgoCD (a separate spoke) installs INTO the cluster you stand up, and
depends on this task. You do NOT install ArgoCD or any app here.

**Dependencies**: none. **Dependents**: `SUBTASK_gitops_argocd`, `SUBTASK_synthesis_gate`.

## Inputs
- `../_GLOBAL.md` — objective, subtree-wide constraints, environment facts.
- `../contracts/_MANIFEST.yaml` and `../contracts/result_record.schema.md` — your owned paths and the
  `RESULT.md` evidence schema you MUST follow (read-only; import literally).
- The host environment itself (the subject under test): verify, do not assume, whether a k3s install
  is possible here (root/systemd/cgroups/egress to the k3s install endpoint).

## Scope / what to deliver
- A reproducible, idempotent-where-feasible **k3s install script** and a **readiness-verification
  script** (a real check: node Ready via `kubectl get nodes`, core system pods healthy), plus a short
  **cluster runbook fragment** (prereqs, run order, how to obtain kubeconfig access — the exact
  command/path, e.g. the k3s-written kubeconfig location and how a client consumes it) and recorded
  **k3s version**.
- Stage all repo-destined files under `staged/deploy/bootstrap/cluster/` (mirroring the intended repo
  path). Write your evidence record at `RESULT.md` per the schema. Do NOT run git; do NOT touch a repo
  checkout — the synthesis gate owns git.
- Own and record the **cluster** criterion in `RESULT.md` (`owns-criteria: [cluster]`), and contribute
  to the shared **reproducible** and **honest** criteria for your own scripts.

### Honest-outcome rule
If the host forbids the install (no root/systemd, no egress, cgroup v2 unavailable, etc.): still
deliver the reproducible script set, and mark the cluster criterion **BLOCKED** with the exact
`blocker{command,error,env_fact}` and a concrete `remediation`. Never fabricate a Ready node.

## Success Criteria
- [ ] Staged install + verification scripts exist, each with a prereqs/re-run header (idempotent where feasible).
- [ ] `RESULT.md` follows `result_record.schema.md`: `cluster` criterion with verdict PASS (evidence: the readiness command + observed Ready node) OR BLOCKED (blocker + remediation); k3s version recorded; `confirmed-no-secrets: true`.
- [ ] Kubeconfig-access is documented as a RETRIEVAL command/path — no kubeconfig with live credentials is staged or committed.
- [ ] No ArgoCD, no app workloads, no container images (that is other items / other spokes).

## Suggested Methodology Files
Parent's Domain-Mapping reading for this child's task type (**Kubernetes cluster lifecycle / day-2**;
primary **Kubernetes**, supporting **Operations**, **IaC Practices**, **Security**). Load the bundle
IDs on-demand; these are the parent's flags, not an exclusive list:
- `kubernetes` — primary. `kubernetes/K8s_Day2_Operations_And_Multitenancy_Methodology.md` (cluster
  lifecycle/readiness posture), `kubernetes/K8s_Workloads_And_API_Objects_Methodology.md` (what
  "Ready" means for core objects). Rationale: a correct, verified single-node k3s stand-up.
- `operations` — `operations/DevTools_Build_Systems_Methodology.md` and
  `operations/BestPractices_Documentation_Methodology.md`. Rationale: reproducible script + runbook fragment.
- `iac-practices` — `iac-practices/CloudOps_Environment_State_And_Drift_Methodology.md`. Rationale:
  idempotent, re-runnable bootstrap.
- `security` — `security/BestPractices_Configuration_Management_Methodology.md`. Rationale: no-secrets
  posture for kubeconfig handling.

*These are the parent's flagged methodologies based on task type. You SHOULD load them as a starting
point but are the final judge of what your work requires — load fewer if clearly inapplicable, more if
your own reading reveals additional surface.*

## Inherited Constraints
All of `../_GLOBAL.md §Subtree-Wide Constraints` bind you: infra-only; no secrets committed; scripts
reproducible/idempotent with documented verification; honest blocker reporting; repo scope
`Nousix-LLC/nswe-demo` only; you stage files only (no git). Compose against `../contracts/` literally;
request an additive amendment if the contract is inadequate — do not deviate silently.

## Out-of-Scope Methodologies
`gitops/*` (ArgoCD is the next spoke), `rust/*` / `frontend/*` (the wasm spoke), `synthesis/*`
(the gate), containerization/* and any app-deploy-manifest methodology (#12/#13, not #10).
