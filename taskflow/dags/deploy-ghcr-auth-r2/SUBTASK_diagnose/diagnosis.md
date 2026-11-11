# diagnosis.md — SUBTASK_diagnose (deploy-ghcr-auth-r2)

Fresh, read-only live diagnosis of Chirp against the committed GitOps desired state at `main` HEAD
(`c805525`). **No cluster mutation, no PR, no committed-file change was performed by this task.**

## Decision

**`decision_branch = already-working`.**

The world changed out of band since attempt #1. The owner created the `ghcr-pull` Secret (~31h ago);
the private digest is now pullable; the committed-digest pod is `1/1 Ready` and is the sole Service
endpoint; the stale `chirp:local` ReplicaSet is scaled to `0`; ArgoCD is **Synced + Healthy** at
`c805525`; and both ingress routes answer `/healthz` → `200` from the digest pod. Every issue-#32
acceptance identity (I1–I7) is observed satisfied on a fresh read. **No remediation is required** and
**no committed manifest change is needed** — but AC4 (selfHeal/prune survival) and the per-route AC3
correlation are left for the verification gate to *execute* as rehearsed checks, since this stage is
read-only and does not trigger a reconcile.

## diagnosis_schema fields (per `../contracts/_MANIFEST.yaml`)

| Field | Observed value |
|-------|----------------|
| `observed_at` | **2026-10-10T02:03Z – 02:05Z** (fresh clock; cluster reads 02:03–02:05Z, ingress curls 02:04:48Z) |
| `main_head_live` | ArgoCD app `chirp` is synced to **`c805525`** (`.status.sync.revision`), `targetRevision: main`. **Equals** the contract's `main_head: c805525`. |
| `digest_pod` | **`chirp-server-bbff68f5b-22spd` — Running, 1/1 Ready, 0 restarts, age ~31h.** Image **and** Image ID both `ghcr.io/nousix-llc/chirp-server@sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3` = committed digest in `deploy/chirp/10-deployment.yaml@c805525`. Clean pull (no `ImagePullBackOff`). |
| `stale_pod` | **Absent as a running pod.** The stale local-image ReplicaSet `chirp-server-f6476ccff` (image `docker.io/library/chirp:local`) is `DESIRED=0 CURRENT=0 READY=0`. It is **not** a Service endpoint. |
| `ghcr_pull_secret_present` | **true.** Secret `ghcr-pull` (type `kubernetes.io/dockerconfigjson`, 1 data key) exists in ns `chirp`, age ~31h. It is the only Secret in the namespace. |
| `ghcr_pullable` | **true.** The Secret is present and valid: the private digest resolved and the pod has been Running ~31h with 0 restarts and a matching Image ID — a successful authenticated pull. (Owner resolved the pull out of band, as anticipated.) |
| `argocd_sync_status` | **Synced**, target revision **`c805525`** (`targetRevision: main`, path `deploy/chirp`, repo `github.com/Nousix-LLC/nswe-demo.git`). |
| `argocd_health` | **Healthy.** SyncPolicy `automated{prune:true, selfHeal:true, allowEmpty:false}`, `ServerSideApply=true`, `PrunePropagationPolicy=foreground`. |
| `ingress_healthz.hostless_route` | **200** — `curl http://<tailnet-LB>:8081/healthz` (any-host rule, added by `c805525`) → `{"service":"chirp-server","status":"ok","version":"0.1.0"}`. Served by the digest pod (see correlation note). |
| `ingress_healthz.host_route` | **200** — `curl -H 'Host: chirp.localhost' .../healthz` → same `{"status":"ok",...}` body. Served by the digest pod. SPA root `/` also returns 200 `text/html` on both routes. |
| `appproject_whitelist_intact` | **true.** AppProject `chirp` `namespaceResourceWhitelist = [Service, ServiceAccount, ConfigMap, apps/Deployment, networking.k8s.io/Ingress]`. **Secret is NOT whitelisted** (matches contract `appproject_secret_whitelisted: false`) → the out-of-band `ghcr-pull` Secret is unmanaged by ArgoCD and survives selfHeal/prune. `sourceRepos` = the repo; `destinations` = ns `chirp` on the in-cluster API only. Scope unchanged. |
| `decision_branch` | **already-working** |
| `credential_reachability` | A valid `read:packages` credential **is reachable**: it lives in the cluster as Secret **`ghcr-pull`** in ns `chirp`, referenced by `10-deployment.yaml` `imagePullSecrets`. It authenticated the pull of the private package `ghcr.io/nousix-llc/chirp-server`. No further external credential input is required. |
| `repo_change_needed` | **false — none.** The `ghcr-pull` Secret is out-of-band and must never be committed; `c805525` already added the host-less ingress rule; the committed digest pin is current and matches the running pod. There is no committed manifest change for the remediation stage to make. |

## Live-vs-desired comparison

| Aspect | Committed desired (`@c805525`) | Live (fresh read) | Gap |
|--------|-------------------------------|-------------------|-----|
| Image | `@sha256:054af27f…` pinned | pod Image ID `@sha256:054af27f…` | none |
| imagePullSecrets | `ghcr-pull` | `ghcr-pull` present & valid | none |
| replicas | 1 (deliberate, in-memory repo) | Deploy 1/1, RS=1 | none |
| Service | ClusterIP, selector name+part-of, 80→8080 | ClusterIP `10.43.138.205`, 80/TCP, matching selector | none |
| Endpoints | single digest pod | `10.42.1.10:8080` only (digest pod); EndpointSlice `chirp-server-bd9hq` → `10.42.1.10` | none (no stale masking) |
| Ingress | `chirp.localhost` + host-less rule, class `traefik` | both rules live, class `traefik`, address present | none |
| ArgoCD | Synced+Healthy at head | Synced+Healthy @ `c805525` | none |

## Notes for the downstream stages (remediate / verify_synthesis)

- **Integration-branch head == `main` head.** AC2 asks for Synced+Healthy "at the integration-branch
  head." No repo change is needed, so branch `work/deploy-ghcr-auth-r2` has nothing to carry beyond
  `c805525`; its head would be identical to `main@c805525`, to which ArgoCD is already Synced+Healthy.
  Treat "integration head" and `main@c805525` as the same desired state — there is no drift to close.
- **Remediate is expected to be a no-op change.** On the already-working branch there is no Secret to
  create (it exists), no drift to reconcile, no stale RS to scale (already 0), and no committed-file
  change — therefore **no PR is required**. `SUBTASK_remediate` should record "no change needed /
  already converged" rather than inventing one.
- **AC3 serving-pod correlation.** The Service has exactly one endpoint (the digest pod `10.42.1.10`),
  so every `200` through either ingress route is necessarily served by the digest pod. The gate may
  additionally correlate by executing its own per-route check if it wants independent evidence.
- **AC4 selfHeal survival is unexecuted here (read-only).** selfHeal is `true` and the `ghcr-pull`
  Secret's kind is excluded from the AppProject whitelist, so the Secret is structurally safe from
  prune; the digest Deployment is the ArgoCD-managed desired state and persists. The gate should
  *execute* the reconcile/await rehearsal to confirm it fires, per the identity `I4` check.
- **Prior ruled-out paths were NOT re-run.** Per the brief, the attempt-#1 credential dead-ends
  (local token lacks `read:packages`, anonymous pull 403, device-flow refresh, `k3d image import`
  non-durable) were consulted as settled findings, not retried as live experiments.

## Methodology applied
- `gitops/GitOps_Reconciliation_And_Drift_Control_Methodology.md` — Argo CD `Synced` (live==desired
  diff) vs `Healthy` (resource-health roll-up) read as distinct; `automated.selfHeal`/`prune`
  semantics; a resource kind absent from the project whitelist is unmanaged and not pruned.
- `kubernetes/*` (workloads, networking) and `operations/*` (incident evidence capture) applied from
  expertise: ReplicaSet/rollout state, Service→EndpointSlice correlation, Ingress route behavior.

## Evidence (commands run, read-only)
- Repo: `git fetch origin`; `origin/main` = `c805525`; `git show origin/main:deploy/chirp/{00,10,20,30}-*.yaml`.
- Cluster (via SSH to the build server, context `k3d-nswe`, ns `chirp`/`argocd`): `get pods/rs/deploy -o wide`,
  `get secret ghcr-pull`, `get secrets`, `get endpoints`, `get endpointslices`, `get svc`, `get ingress`,
  ArgoCD `get application chirp` (sync/health/revision/targetRevision/syncPolicy/history), `get appproject chirp`
  (namespaceResourceWhitelist/sourceRepos/destinations), `describe pod` (Image/Image ID/State/Ready/restarts).
- Ingress: `curl` `/healthz` and `/` on both the host (`Host: chirp.localhost`) and host-less routes via the
  k3d LB serving port 8081.
