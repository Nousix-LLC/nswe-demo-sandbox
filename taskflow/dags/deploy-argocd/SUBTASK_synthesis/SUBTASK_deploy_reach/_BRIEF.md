# Task: Deploy onto the live k3d cluster and demonstrate reachability (with evidence)

## Task Specification

**Slug**: SUBTASK_deploy_reach
**Task Kind**: deployment / reachability proof (cluster-only)
**Status**: Pending

### Objective

Deploy the chirp app onto the live k3d `nswe` cluster and **demonstrate it is actually reachable**, then
assert the runtime contract identities with captured evidence. Reachability MUST be shown with a real
HTTP request + response, never asserted. This task mutates the **cluster only** — no git, no PR.

### Context

Second stage of the `SUBTASK_synthesis` sub-subtree (hub `../_GLOBAL.md`, contract `../contracts/`).
The static gate (`SUBTASK_static_gate`, your declared dependency) has produced its go/no-go report at
`../SUBTASK_static_gate/outputs/static_gate_report.md` — read it; if it is NO-GO, surface the blocking
violation and route a remediation fix-task rather than forcing a broken deploy. The manifests to deploy are
`/home/user/nswe-demo/deploy/chirp/*` and `/home/user/nswe-demo/deploy/argocd/*`. Ground truth (digest,
port 8080, health `/healthz`, ingress `traefik`, **private GHCR → imagePullSecret required**) is in
`../../SUBTASK_discovery/outputs/ground_truth.md`.

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Static gate report | `../SUBTASK_static_gate/outputs/static_gate_report.md` | Go/no-go + any flagged issues to resolve before/at deploy |
| App + GitOps manifests | `/home/user/nswe-demo/deploy/chirp/*`, `/home/user/nswe-demo/deploy/argocd/*` | What to deploy/sync |
| Ground-truth facts | `../../SUBTASK_discovery/outputs/ground_truth.md` | Digest, listen port, health path, ingress class, pull-secret need, serverlb mapping |
| Parent identities | `../../contracts/_MANIFEST.yaml` | The runtime identities to assert |
| Sub-subtree contract | `../contracts/_MANIFEST.yaml`, `../contracts/synthesis_gate_contract.yaml` | Your identity-coverage assignment + the required evidence shape |

## Scope (what this task covers — you decide the method)

- Bring the app up on the live k3d `nswe` cluster: apply the AppProject + Application and/or let ArgoCD
  sync (direct `kubectl apply` of the manifests is an acceptable way to demonstrate reachability; a
  justified NodePort/port-forward is an acceptable fallback if the Traefik path is obstructed).
- Handle the **private-GHCR imagePullSecret** out-of-band (create a `dockerconfigjson` Secret in ns
  `chirp`, or document the package being made public) — **never commit a secret to the tree**.
- Watch the rollout to Synced/Healthy; resolve `ImagePullBackOff` / probe failures. If the root cause is a
  wrong manifest value, that is a gate FAIL → inject a remediation fix-task (`engine_amend_plan { add_task }`)
  and re-verify; do not silently edit the sibling manifests in place.
- Issue a **real HTTP request** through the k3d ingress path (`http://localhost:8081`, with the recorded
  Host header if host-based routing) and capture the response proving the SPA (`/`) or API health
  (`/healthz`) surface is served.
- Assert the runtime identities assigned to you in `../contracts/_MANIFEST.yaml` `identity_coverage`
  (`service-selector-matches-pods` via non-empty endpoints; `ingress-wires-service` via the live GET;
  `argocd-application-wired` via Synced/Healthy; `image-pull-works` via a clean rollout).

Constraint on cluster scope: only the project's k3d `nswe` cluster/namespaces and its ArgoCD — do not
touch sibling apps/clusters. Out of scope: any git branch/commit/PR (that is `SUBTASK_land_pr`) and the
static-only assertions (already done by `SUBTASK_static_gate`).

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `outputs/reachability_evidence.md` (under this task's workspace) |
| Content | Per the `reachability_evidence` schema in `../contracts/synthesis_gate_contract.yaml`: deploy mechanism, rollout/endpoints/no-ImagePullBackOff evidence, pull-secret handling, the HTTP request issued + response captured, and the runtime per-identity PASS/FAIL |

## Success Criteria

- [ ] The app is demonstrably reachable: a captured HTTP request+response through the ingress path (or justified fallback).
- [ ] Rollout reached Synced/Healthy; Service endpoints non-empty; pod NOT in ImagePullBackOff; probes reflect real readiness.
- [ ] Private-GHCR pull handled without committing any secret; the mechanism is documented in the evidence.
- [ ] Each assigned runtime identity recorded PASS/FAIL with evidence; any FAIL routed to a remediation fix-task + re-verification.
- [ ] No git side effects; sibling manifests not edited in place.

## Suggested Methodology Files

Task-type rows: *"Kubernetes networking & service connectivity"* (`kubernetes`); *"GitOps reconciliation
/ drift"* and *"Set up GitOps with Argo CD"* (`gitops`); *"Kubernetes secrets protection"* +
*"Verify signed container images at admission"* adjacency (`kubernetes-security`, for the pull-secret and
supply-chain posture). SUGGESTIONS — you judge coverage depth.

- `kubernetes` (`K8s_Networking_And_Service_Connectivity_Methodology.md` for the Service/Ingress/Traefik path;
  `K8s_Workloads_And_API_Objects_Methodology.md` + `K8s_Configuration_Management_Methodology.md` for rollout/probes/secrets).
- `gitops` (`GitOps_Reconciliation_And_Drift_Control_Methodology.md` for ArgoCD sync-to-Healthy; `GitOps_Secrets_Management_Methodology.md` for the pull-secret path).
- `kubernetes-security` (`K8sSecurity_Secrets_Protection_Methodology.md`) — keep the pull secret out of git.
- `synthesis/Synthesis_Remediation_Methodology.md` — if a runtime check FAILs, inject fix-tasks rather than plug.
- `core` — baseline error-handling discipline for the operational steps.

Parent-flagged for this task type; load as a starting point, you are the final judge. Synthesis never loads
`decomposition/` content.

## Inherited Constraints

- Target the k3d `nswe` cluster + its ArgoCD only; read/modify only the `chirp`/`argocd` namespaces this task needs; do not touch sibling apps/clusters.
- Reachability must be demonstrated with evidence, not asserted.
- No secrets committed to the tree; the imagePullSecret is applied out-of-band and documented.
- No git mutation here (no branch/commit/PR). Image is digest-pinned and the AppProject is least-privilege already — honor them, do not loosen.
- Target k3d-hosted k3s only (#23 HSO-1); note, but do not act on, any native-cluster divergence.

## Out-of-Scope Methodologies

- `operations`/git-workflow methodologies — landing the PR is `SUBTASK_land_pr`.
- `decomposition/` content — remediation here is injected fix-tasks (gate-driven correction), not re-cutting the subtree.
