# _BRIEF.md — SUBTASK_diagnose (deploy-ghcr-auth-r2)

## Task Specification
**Slug**: SUBTASK_diagnose
**Task Kind**: standard
**Status**: Pending

### Objective
Read the **fresh** live cluster and repo state and diagnose the current gap between the running cluster and the
committed GitOps desired state for Chirp, concluding with an explicit decision branch — **already-working**,
**create-secret**, or **blocked** — that downstream remediation and verification depend on.

### Context
Part of `deploy-ghcr-auth-r2` (see `../_GLOBAL.md`). This is the **observe** stage of a diagnose → remediate →
verify pipeline: you establish the ground truth; you do **not** change anything. Attempt #1 found the committed-digest
pod in `ImagePullBackOff` with no `ghcr-pull` Secret and a stale `chirp:local` pod masking the outage — but the world
may have changed (the owner may have created the Secret or made the GHCR package public out of band, and `c805525`
added a host-less ingress rule). **Test the live world fresh; do not assume the prior blocked state still holds.**

**Dependencies**: none. **Dependents**: `SUBTASK_remediate`, `SUBTASK_verify_synthesis`.

## Input Specification
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Scope, constraints, success criteria |
| Deployment identity + diagnosis schema | `../contracts/_MANIFEST.yaml` (read-only) | The constants to assert against and the exact fields your output MUST carry |
| Host/cluster access | the **repo checkout's `CLAUDE.md`** | How to reach the cluster (SSH to build server for `kubectl`; context `k3d-nswe`, ns `chirp`; ArgoCD ns `argocd`; the k3d LB serving port) |
| Committed GitOps state | `deploy/chirp/{00-namespace,10-deployment,20-service,30-ingress}.yaml` + `README.md` @ `main` (`c805525`) | The desired state and the pull-auth runbook |
| Prior verdict | `../../deploy-ghcr-auth/SYNTHESIS.md` + `FAILURE.md` | Ruled-out hypotheses — read so you do not re-tread them |

### Required Inputs verification
- [ ] `../_GLOBAL.md` and `../contracts/_MANIFEST.yaml` read.
- [ ] Repo checkout established per `CLAUDE.md`; cluster reachable read-only.

## Process (approach — not a runbook)
Establish, on a fresh clock, the complete decision-relevant live picture and compare it to the committed desired
state and the prior ruled-out hypotheses. Read the live cluster (digest pod vs stale pod, endpoints, whether the
`ghcr-pull` Secret exists, whether the committed digest is pullable now, ArgoCD sync/health at head, the ingress
behaviour at both routes, AppProject whitelist intact) and the committed manifests. **This is a read-only
investigation** — make no cluster changes and open no PR. Decide and record the branch:
- **already-working** — the digest pod is `1/1 Ready`, the stale RS is at 0, both ingress routes answer 200 from the
  digest pod, ArgoCD Synced+Healthy. (Owner likely resolved the pull out of band.)
- **create-secret** — the pull is now reachable (a `read:packages` credential exists, or the package is public) but
  the `ghcr-pull` Secret is still missing / the cluster has not converged; name precisely what credential is reachable
  and where the system expects it.
- **blocked** — no credential is reachable and the package is still private; name precisely the external input still
  required and where the system expects to find it. Do **not** prescribe a blind retry of the ruled-out paths.

Determine whether any **committed manifest change** is actually needed (default expectation: none — the `ghcr-pull`
Secret is out-of-band and never committed; `c805525` already added the host-less ingress). Record it either way.

## Output Specification
**Primary output**: `diagnosis.md` in this workspace, carrying **every required field of
`diagnosis_schema` in `../contracts/_MANIFEST.yaml`** (observed_at, live/desired comparison, the branch,
credential reachability, repo_change_needed, and the per-route ingress/healthz observations). Self-contained: the
remediation and verification stages read this instead of re-deriving the live world.

## Success Criteria
- [ ] Fresh live read performed (not assumed from attempt #1); `observed_at` recorded.
- [ ] Every `diagnosis_schema` required field present and evidenced.
- [ ] Exactly one `decision_branch` chosen, with the reasoning and (for create-secret/blocked) the precise
      credential/external-input location.
- [ ] No cluster mutation, no PR, no committed-file change performed by this task.
- [ ] `repo_change_needed` stated explicitly (what, or "none").

## Suggested Methodology Files
Parent's Domain-Mapping reading (closest rows): *"GitOps reconciliation / drift & self-heal control"* →
**GitOps** (primary) + **IaC Practices**; *"Kubernetes networking & service connectivity"* / *"workloads"* →
**Kubernetes**; *"Incident response / observability"* → **Operations**.
- `gitops/GitOps_Reconciliation_And_Drift_Control_Methodology.md` — read live sync/health/drift correctly; what Synced-vs-Healthy means.
- `kubernetes/K8s_Workloads_And_API_Objects_Methodology.md` — reason about ReplicaSets/pods/rollout state (digest vs stale pod).
- `kubernetes/K8s_Networking_And_Service_Connectivity_Methodology.md` — Service endpoints and Ingress behaviour at the two routes.
- `operations/Observability_Incident_Management_Methodology.md` — disciplined live-state capture / evidence gathering for a degraded service.

*These are the parent's flagged starting points based on the task type. You are the final judge of what your work
requires — load fewer if some are clearly inapplicable; load more if your reading of the brief reveals additional
surface.*

## Inherited Constraints
- Read-only on the cluster; change nothing in this stage.
- Scope limited to `chirp*` namespaces and ArgoCD Application `chirp`; never touch other namespaces/apps.
- Host facts (server address, SSH key path, user, host paths) stay in the working environment; they never enter any
  file destined for GitHub. (`diagnosis.md` is a taskflow-internal file and may carry working facts.)
- Do not re-run the prior attempt's ruled-out credential paths as live experiments; consult them as settled findings.

## Out-of-Scope Methodologies
- `synthesis/*` — the verification gate is a different sibling; do not run gate checks here.
- `decomposition/*` — decomposer-side only; irrelevant to this leaf.
