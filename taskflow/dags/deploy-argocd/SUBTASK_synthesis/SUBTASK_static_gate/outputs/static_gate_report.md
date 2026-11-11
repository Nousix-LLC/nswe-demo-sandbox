# Static Verification Gate Report — deploy-argocd (pre-cluster GO/NO-GO)

**Task**: `SUBTASK_static_gate` (first stage of `SUBTASK_synthesis`). **Role**: static half of the deploy
verification gate — assert every statically-checkable parent-contract identity against the real manifest
text, confirm wiring + duplication, record the static halves of the runtime identities, give a focused
k3s/Traefik + ArgoCD + security review, and emit an unambiguous **static GO / NO-GO**.
**Mode**: strictly read-only over the sibling manifests. **No cluster access, no git mutation, no edits.**
**Date**: 2026-10-08.

## Inputs asserted (provenance)

| Input | Resolved location | Role |
|-------|-------------------|------|
| App workload manifests | `/home/user/nswe-demo/deploy/chirp/{00-namespace,10-deployment,20-service,30-ingress}.yaml` | objects asserted |
| GitOps config | `/home/user/nswe-demo/deploy/argocd/{application,appproject}.yaml` | Application + AppProject asserted |
| Parent identities | `../../contracts/_MANIFEST.yaml` `identities`; `../../contracts/deploy_contract.yaml` | assertion set + frozen values |
| Ground-truth facts | `../../SUBTASK_discovery/outputs/ground_truth.md` | digest / port / health-path / ingress-class to compare against |
| Coverage assignment + report shape | `../contracts/_MANIFEST.yaml` `identity_coverage`; `../contracts/synthesis_gate_contract.yaml` | which identities I own + required report content |

The canonical `deploy/chirp/*` is **byte-identical** to the `SUBTASK_app_manifests/outputs/deploy/chirp/`
mirror (verified `diff` on all four files) — the assertions below hold at both locations.

---

## 1. Assigned static identities — PASS/FAIL with evidence

Coverage set (from `../contracts/_MANIFEST.yaml` `identity_coverage`): `image-pinned-by-digest`,
`resources-and-probes`, `appproject-least-privilege`, `namespace-isolation-no-secrets`. All four are fully
statically decidable; each is asserted against the real manifest text with concrete evidence. **No silent plug.**

| Identity | Verdict | Evidence (file:line / value compared) |
|---|---|---|
| **image-pinned-by-digest** | **PASS** | `10-deployment.yaml:59` → `image: ghcr.io/nousix-llc/chirp-server@sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3`. Byte-equal to `ground_truth.md` `image_digest` (the published manifest-list digest `054af27…`). Reference is `@sha256:` form; **no `:<tag>`** form anywhere in the Deployment. `imagePullPolicy: IfNotPresent` (`:60`) is consistent with an immutable digest. |
| **resources-and-probes** | **PASS** | `requests` cpu `50m` / memory `64Mi` (`10-deployment.yaml:66–68`) **and** `limits` cpu `500m` / memory `256Mi` (`:69–71`) both present. `livenessProbe` httpGet `/healthz:8080` (`:80–86`) **and** `readinessProbe` httpGet `/healthz:8080` (`:87–93`) both present, targeting the real API health surface (`ground_truth.md §4`: `/healthz` on `8080`, not the SPA `/`). Bonus `startupProbe /healthz:8080` (`:73–79`) gives cold-start grace. |
| **appproject-least-privilege** | **PASS** | `appproject.yaml` `clusterResourceWhitelist` = **only** `{group: "", kind: Namespace}` (`:51–53`) — **no `*/*/*`**, no `group: '*', kind: '*'`. `destinations` = exactly `{server: https://kubernetes.default.svc, namespace: chirp}` (`:43–45`). `sourceRepos` = only the nswe-demo repo (`:37–38`), not `*`. `namespaceResourceWhitelist` is an explicit enumerated set — Service / ServiceAccount / ConfigMap / Deployment / Ingress (`:65–75`), **Secret deliberately excluded** (`:60–64`). `application.yaml:32` binds `spec.project: chirp` (not `default`), so the Application is scoped by this project. |
| **namespace-isolation-no-secrets** | **PASS** | Namespace manifest exists: `00-namespace.yaml` `kind: Namespace`, `name: chirp` (`:7,:9`). Every chirp **workload** object carries `namespace: chirp` — Deployment (`10-deployment.yaml:12`), Service (`20-service.yaml:10`), Ingress (`30-ingress.yaml:24`). The Application/AppProject correctly live in `namespace: argocd` (`application.yaml:22`, `appproject.yaml:21`) — ArgoCD control-plane objects belong in the control-plane namespace, not the workload namespace; this is correct, not a leak. Tree grep for committed secret material (`kind: Secret`, `stringData`, `.dockerconfigjson` data, PEM blocks, `password:`/`token:` values) → **none**. The only two hits are benign: a hardening flag `automountServiceAccountToken: false` (`10-deployment.yaml:41`) and a README *description* of the out-of-band pull-secret pattern (`argocd/README.md:40`) — neither is committed secret data. |

---

## 2. Static halves of the three runtime identities

The runtime proof of these belongs to `SUBTASK_deploy_reach`; recorded here are the **statically-checkable
halves** (label/port, backend/class, path/project diffs) — all consistent.

| Runtime identity | Static half | Verdict | Evidence |
|---|---|---|---|
| **service-selector-matches-pods** | selector ⊆ pod labels; `targetPort == container_listen_port` | **PASS (static half)** | Service `selector` = `{name: chirp-server, part-of: chirp}` (`20-service.yaml:17–19`) is a subset of the Deployment pod-template labels `{name: chirp-server, part-of: chirp, managed-by: argocd}` (`10-deployment.yaml:35–38`) → selector matches these pods. Service `targetPort: 8080` (`20-service.yaml:23`) == container `containerPort: 8080` (`10-deployment.yaml:63`) == `ground_truth` `container_listen_port 8080`. Also consistent with the Deployment `selector.matchLabels` (`:30–32`). *Runtime half (non-empty `endpoints` after rollout) → deploy_reach.* |
| **ingress-wires-service** | backend refs Service name+port; class == ground_truth | **PASS (static half)** | Ingress backend `service.name: chirp-server`, `port.number: 80` (`30-ingress.yaml:38–41`) == Service `name: chirp-server` (`20-service.yaml:9`), `port: 80` (`:22`). `ingressClassName: traefik` (`30-ingress.yaml:30`) == `ground_truth` `ingress_class: traefik`. Host-based routing `host: chirp.localhost`, `path: / (Prefix)` (`:32–36`) — reachability test MUST send `Host: chirp.localhost` via `localhost:8081`. *Runtime half (live HTTP 200) → deploy_reach.* |
| **argocd-application-wired** | source.path / repoURL / dest.ns / project | **PASS (static half)** | `source.path: deploy/chirp` (`application.yaml:44`) == contract `source_path`. `repoURL: https://github.com/Nousix-LLC/nswe-demo.git` (`:35`) == the nswe-demo repo. `destination.namespace: chirp` (`:50`). `spec.project: chirp` (`:32`), **not `default`**. `targetRevision: main` (`:42`) is the correct committed steady-state value (see Review note R2). *Runtime half (app Synced/Healthy) → deploy_reach.* |

---

## 3. Wiring — every object referenced/mounted; no dead manifest

**PASS.** The six objects form one connected graph with no orphan:

- **Namespace `chirp`** ← every namespaced workload object targets it (Deployment/Service/Ingress `namespace: chirp`); it is also the AppProject's sole destination namespace. Referenced.
- **Deployment** ← selected by the Service selector; synced by the Application (`path: deploy/chirp`). Referenced.
- **Service** → selects the Deployment pods; ← referenced by the Ingress backend (`name: chirp-server`, `port 80`). Referenced on both sides.
- **Ingress** → references the Service; routed by Traefik (serverlb `localhost:8081 → 80`). Referenced.
- **Application** → references `path: deploy/chirp` + `project: chirp`; lives OUTSIDE its own synced path (`deploy/argocd` ≠ `deploy/chirp`), so no self-reconciliation recursion (`application.yaml:16–17`). Referenced.
- **AppProject** ← referenced by `Application.spec.project: chirp`. Its whitelists **cover exactly the kinds that are synced**: Namespace (cluster-scoped) + Deployment/Service/Ingress (namespaced). ServiceAccount/ConfigMap are allow-list headroom, not manifests, so they are not dead objects. Referenced.

No manifest is detached, unreferenced, or unroutable.

## 4. Duplication — exactly one producer per owned path

**PASS.** Producers are disjoint by directory: `deploy/chirp/*` (4 files) owned by `SUBTASK_app_manifests`;
`deploy/argocd/*` (2 files) owned by `SUBTASK_argocd_gitops`. No path is produced by both; no object `kind`
is defined twice. The `SUBTASK_app_manifests/outputs/` mirror is byte-identical to the canonical tree (no
divergent second copy). Exactly one `kind:` per file across the six manifests (enumerated by grep).

---

## 5. Focused review note (k3s/Traefik + ArgoCD idiom + security posture)

**Idiom — strong.**
- **k3s/Traefik**: `ingressClassName: traefik` is the correct shipped controller for k3d/k3s; the serverlb
  `8081→80` path and host-based `chirp.localhost` routing are documented inline, and the Ingress-vs-Gateway-API
  choice is justified (the cluster's supported controller is Traefik-as-Ingress). TLS omission is deliberate
  and justified for the k3d demo. Correct and idiomatic.
- **ArgoCD**: Application in the `argocd` namespace and outside its own synced path (no self-reconcile loop);
  `resources-finalizer` for clean cascade; `automated: {prune, selfHeal, allowEmpty:false}`; `ServerSideApply`;
  `PrunePropagationPolicy=foreground`; bounded `revisionHistoryLimit`. `CreateNamespace` deliberately NOT set
  because the Namespace is a committed, labeled manifest (avoids a diff against an imperatively-created
  unlabeled ns) — correct reasoning. AppProject `orphanedResources.warn: true` surfaces sprawl.

**Security posture — strong.** PSA `restricted` enforced at the namespace (`00-namespace.yaml:14–20`); the pod
is fully restricted-compliant: `runAsNonRoot`, uid/gid `65532`, `allowPrivilegeEscalation: false`,
`capabilities.drop: [ALL]`, `seccompProfile: RuntimeDefault`, `readOnlyRootFilesystem: true` (+ `emptyDir`
scratch), `automountServiceAccountToken: false`. Image pinned by immutable digest. Least-privilege AppProject
with `Secret` excluded from the whitelist (defense-in-depth). No secrets in the tree.

**Non-blocking observations (all static-PASS; carried forward to `SUBTASK_deploy_reach`, none gates static GO):**
- **R1 — pull Secret is a runtime precondition.** The Deployment references `imagePullSecrets: [ghcr-pull]`
  (`10-deployment.yaml:52–56`) because the GHCR package is private (`ground_truth §6`). That Secret is applied
  **out-of-band** (correctly not committed, and correctly not in the AppProject whitelist). It MUST exist in
  namespace `chirp` at rollout or `image-pull-works` fails with `ImagePullBackOff`. **Runtime concern** →
  `deploy_reach` must handle it (or make the package public). Static posture is correct.
- **R2 — `targetRevision: main` vs pre-merge test.** The committed Application tracks `main` (the correct
  steady-state value; tracking the ephemeral feature branch would be an anti-pattern). Consequently a
  reachability test run **before** the PR merges must either temporarily point `targetRevision` at
  `work/deploy-argocd` or sync after merge (the #23 HSO-1 divergence, already noted in `application.yaml:38–41`).
  **Runtime/ordering concern** → `deploy_reach` / fold; not a static defect.
- **R3 — no explicit `serviceAccountName`.** The pod runs under the namespace `default` SA with its token
  mount disabled — acceptable for a workload that makes no API calls; `ServiceAccount` is whitelisted for a
  future dedicated SA. Non-blocking.

No static check FAILed, so no remediation fix-task (`engine_amend_plan { add_task }`) is injected. Had one
FAILed, it would be routed to a remediation task — never fixed by editing the siblings' COMPLETED manifests.

---

## 6. Overall static verdict

### ✅ STATIC GO

All four assigned static identities **PASS** with recorded evidence; the static halves of the three runtime
identities are **consistent (PASS)**; **wiring** is complete (no dead/orphan manifest) and **duplication** is
clean (one producer per owned path, disjoint `deploy/chirp` vs `deploy/argocd`, mirror identical). The k3s/Traefik
and ArgoCD idiom is correct and the security posture is strong. The three non-blocking observations (R1 pull-Secret,
R2 targetRevision/merge ordering, R3 default SA) are **runtime concerns** carried forward to `SUBTASK_deploy_reach`
and the fold — none blocks the static gate.

**Downstream proceeds**: `SUBTASK_deploy_reach` may apply/sync against the live k3d `nswe` cluster and prove the
runtime halves (`service-selector-matches-pods`, `ingress-wires-service`, `argocd-application-wired`,
`image-pull-works`). This report is the static input to `SUBTASK_fold`'s combined verdict.

### Side-effect attestation
No cluster mutation, no git mutation, sibling manifests unmodified (read-only throughout). No secrets read into
or written to this report.
