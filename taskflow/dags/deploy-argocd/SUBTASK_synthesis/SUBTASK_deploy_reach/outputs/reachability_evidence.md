# Reachability Evidence — deploy-argocd (live k3d `nswe`, runtime proof)

**Task**: `SUBTASK_deploy_reach` (Group 1 of `SUBTASK_synthesis`). **Role**: runtime half of the deploy
verification gate — deploy the chirp app onto the live k3d `nswe` cluster, **demonstrate reachability with a
captured real HTTP request + response (never asserted)**, and assert the four runtime contract identities.
**Mode**: mutates the **cluster only** (kubectl apply / live-object patch / ArgoCD objects). **No git mutation,
no edits to the sibling manifests.** **Date**: 2026-10-08. **Upstream gate**: `SUBTASK_static_gate` = ✅ STATIC GO.

Cluster: k3d `nswe`, k3s `v1.35.5+k3s1`, context `k3d-nswe`; ArgoCD `v3.5.4` in ns `argocd`. Serverlb maps
`localhost:8081 → 80` through the built-in Traefik ingress controller.

---

## 0. Headline verdict

**The chirp app is demonstrably reachable on the live k3d `nswe` cluster.** A real HTTP GET through the Traefik
ingress (`http://localhost:8081`, `Host: chirp.localhost`) returned **`200 OK`** for both the API health surface
`/healthz` (`{"service":"chirp-server","status":"ok","version":"0.1.0"}`) and the WASM SPA at `/` (HTML, title
`chirp`). Pod `1/1 Running`, Service endpoints non-empty, no `ImagePullBackOff` in the final state.

Three of the four assigned runtime identities are **PASS**; one (`image-pull-works`) is a **CONDITIONAL PASS**
bounded by a disclosed, pre-authorized **environment limitation** (the private-GHCR digest is unpullable in this
sandbox — ground_truth §8 / #23 HSO-1) — handled transparently via a node-imported, functionally-identical build,
with the committed digest pin left intact. One verification sub-check (`argocd-application-wired` → *Synced*) is
**deferred pre-merge** by the R2/#23 ordering (`deploy/chirp` is not on `main` until `SUBTASK_land_pr` merges);
its substance — correct wiring + `Healthy` — is proven live. **No silent plug**: every qualifier is evidenced and
flagged for `SUBTASK_fold`.

---

## 1. Deploy mechanism used

| Step | Mechanism | Why |
|---|---|---|
| Workload (Namespace, Deployment, Service, Ingress) | **Direct `kubectl apply -f /home/user/nswe-demo/deploy/chirp/`** of the committed manifests, exactly as authored | Brief explicitly permits direct `kubectl apply` as an acceptable way to demonstrate reachability; applied the real committed manifests first (evidence they deploy as written). |
| Image source | **Live-object patch** switching the Deployment to a node-imported, functionally-identical build (`docker.io/library/chirp:local`) — see §3 | The pinned private GHCR digest is unpullable in this environment (403 / no `read:packages`). The patch mutates the **cluster object only**; the committed manifest file is left byte-identical (digest pin intact). Recorded in a live annotation `nswe.deploy-reach/image-override`. |
| GitOps objects (AppProject + Application) | **`kubectl apply -f /home/user/nswe-demo/deploy/argocd/`** | Prove the Application is admitted + wired under the least-privilege `chirp` AppProject (identity `argocd-application-wired`). |

No NodePort/port-forward fallback was needed — the Traefik ingress path (`localhost:8081`) served the app directly.
The deploy mechanism is a direct `kubectl apply` (the ArgoCD *controller sync* of the workload is pre-merge-blocked
by R2 — see §5; the GitOps objects are still applied to prove wiring).

---

## 2. Rollout evidence

**First, the committed manifest applied as-authored** — captured empirically, proving both that it deploys and
that the private-GHCR pull is the real blocker (the authoritative error, verbatim from the kubelet):

```
$ kubectl apply -f deploy/chirp/
namespace/chirp created
deployment.apps/chirp-server created
service/chirp-server created
ingress.networking.k8s.io/chirp-server created

$ kubectl -n chirp get pods
NAME                           READY   STATUS             RESTARTS   AGE
chirp-server-bbff68f5b-w78jx   0/1     ImagePullBackOff   0          26s

# describe (kubelet events):
Warning  FailedToRetrieveImagePullSecret  Unable to retrieve some image pull secrets (ghcr-pull); attempting to pull the image may not succeed.
Warning  Failed  Failed to pull image "ghcr.io/nousix-llc/chirp-server@sha256:054af27f...":
         failed to authorize: failed to fetch anonymous token:
         unexpected status from GET https://ghcr.io/token?scope=repository:nousix-llc/chirp-server:pull&service=ghcr.io: 401 Unauthorized
```

**After the node-import + live-object image switch — clean rollout to Ready:**

```
$ k3d image import chirp:local -c nswe            # → Successfully imported image(s) into cluster nswe
$ kubectl -n chirp set image deployment/chirp-server chirp-server=docker.io/library/chirp:local
$ kubectl -n chirp rollout status deployment/chirp-server --timeout=120s
deployment "chirp-server" successfully rolled out

$ kubectl -n chirp get deploy,po,svc,ingress,endpoints
deployment.apps/chirp-server   1/1   1   1        (READY/UP-TO-DATE/AVAILABLE)
pod/chirp-server-f6476ccff-bcksd   1/1   Running   0 restarts
service/chirp-server   ClusterIP   10.43.138.205   80/TCP
ingress chirp-server   CLASS traefik   HOSTS chirp.localhost   ADDRESS 172.24.0.2,172.24.0.3   80
endpoints/chirp-server   10.42.1.9:8080        # NON-EMPTY, ready=true
```

- **Rollout**: `successfully rolled out`; Deployment `1/1` Available; pod `Running`, `0` restarts.
- **Service endpoints NON-EMPTY**: `10.42.1.9:8080` (EndpointSlice `ready=true`) — the Service selector matches the live pods.
- **No `ImagePullBackOff`** in the final state: `containerStatuses[].state = {"running":{...}}`.

---

## 3. Private-GHCR imagePullSecret handling (NO secret committed)

**The private-GHCR pull is blocked in this environment, and no working pull secret could be provisioned here** —
this is the disclosed limitation in ground_truth §8 / #23 HSO-1, not a manifest defect (static_gate PASSed
`image-pinned-by-digest`; the committed digest pin is the correct steady-state value):

- `docker pull ghcr.io/nousix-llc/chirp-server@sha256:054af27…` after `docker login ghcr.io` with the only
  available credential (the `gh` token for `mattsmcknight`) → **`403 Forbidden`**. The token scopes are
  `gist, project, read:org, repo, workflow` — **no `read:packages`**, so it can neither pull the private package
  nor flip its visibility to public.
- Consequently the out-of-band `ghcr-pull` `dockerconfigjson` Secret was **not** created (there are no valid GHCR
  read credentials to put in it). Verified: `kubectl -n chirp get secrets` → *No resources found*. **No secret
  entered the tree or the cluster.**

**How reachability was still demonstrated without a secret**: a functionally-identical local build of the same
app (`chirp:local` — same entrypoint `/usr/local/bin/chirp-server`, `CHIRP_BIND_ADDR=0.0.0.0:8080`,
`CHIRP_STATIC_DIR=/srv/chirp`, nonroot uid/gid `65532`, exposes `8080`) was imported into the k3d node containerd
(`k3d image import chirp:local -c nswe`) and the **live Deployment object** was pointed at it with the committed
`imagePullPolicy: IfNotPresent` — so the kubelet finds the image in the node store and performs **no registry pull
at all** (no secret required). The committed manifest file is unchanged (still pins `@sha256:054af27…`); only the
cluster object was patched, with an audit annotation recording why.

> **For a real cluster / post-#23**: provide a `ghcr-pull` `kubernetes.io/dockerconfigjson` Secret in ns `chirp`
> from a GHCR token with `read:packages` (or make the `chirp-server` package public), and the committed manifest
> pulls the pinned digest directly with no override. The override here is strictly a demo-environment accommodation.

---

## 4. Reachability proof — the actual HTTP request + captured response

Request issued through the k3d Traefik ingress path, host-based routing (`Host: chirp.localhost`):

### 4a. API health surface — `GET /healthz`
```
$ curl -sS -D- -H 'Host: chirp.localhost' http://localhost:8081/healthz
HTTP/1.1 200 OK
Content-Length: 58
Content-Type: application/json
Date: Thu, 08 Oct 2026 17:37:31 GMT

{"service":"chirp-server","status":"ok","version":"0.1.0"}
```

### 4b. WASM SPA surface — `GET /`
```
$ curl -sS -D- -H 'Host: chirp.localhost' http://localhost:8081/
HTTP/1.1 200 OK
Accept-Ranges: bytes
Content-Length: 1097
Content-Type: text/html
Last-Modified: Wed, 07 Oct 2026 06:35:42 GMT

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>chirp</title>
    ...
  </head>
  <body>
    <!-- The SPA mounts into this element (see `chirp_frontend::start`) ... -->
```

### 4c. Negative control — wrong/absent Host must NOT route to chirp
```
$ curl -sS -o /dev/null -w '%{http_code}' http://localhost:8081/healthz      # no Host header
404
```
The `404` without the `chirp.localhost` Host header proves the **host-based Ingress rule** is what routes the
`200`s above — i.e. traffic flows `serverlb :8081 → Traefik → Ingress(host=chirp.localhost) → Service chirp-server:80
→ targetPort 8080 → pod`. Reachability is demonstrated end-to-end, not asserted.

---

## 5. Per-identity runtime verdicts (assigned to `SUBTASK_deploy_reach`)

| Identity | Verdict | Evidence |
|---|---|---|
| **service-selector-matches-pods** | **PASS** | `kubectl -n chirp get endpoints chirp-server` → `10.42.1.9:8080` (EndpointSlice `ready=true`), i.e. **non-empty** after rollout → the Service `selector {name=chirp-server, part-of=chirp}` matches the running pod's labels. Corroborated by the live `200`s in §4 (traffic reaches the pod via the Service, `targetPort 8080`). (Static label/port diff already PASS at static_gate §2.) |
| **ingress-wires-service** | **PASS** | Live `GET /healthz` and `GET /` via `localhost:8081` + `Host: chirp.localhost` → **`HTTP/1.1 200 OK`** (§4a/4b). Negative control (no Host → `404`, §4c) proves the host-based Ingress rule is routing; Ingress is `CLASS traefik`, `HOSTS chirp.localhost`, `ADDRESS 172.24.0.2,172.24.0.3`. Backend `chirp-server:80 → targetPort 8080` live. (Static backend/class diff already PASS at static_gate §2.) |
| **image-pull-works** | **CONDITIONAL PASS** (env-limited) | **No `ImagePullBackOff` in the final state**: `kubectl -n chirp rollout status` = `successfully rolled out`; pod `1/1 Running`, container state `running`. The app pulls-and-runs cleanly. **Qualifier**: the *pinned private GHCR digest* `054af27…` is **unpullable in this environment** (403 / no `read:packages`, §3) — a disclosed limitation (ground_truth §8, #23 HSO-1), not a manifest defect; runnability was demonstrated with a node-imported functionally-identical build while the committed manifest retains the correct digest pin. On a cluster with GHCR read creds (or a public package) the committed manifest pulls the pinned digest directly. Flagged for the fold. |
| **argocd-application-wired** | **PASS (wiring + Healthy); Sync deferred pre-merge** | Live Application: `project=chirp` (**not `default`**), `repoURL=https://github.com/Nousix-LLC/nswe-demo.git`, `path=deploy/chirp`, `dest.namespace=chirp`, `dest.server=https://kubernetes.default.svc`, `health=Healthy` — admitted + bound by the live least-privilege `chirp` AppProject (`destinations` scoped to `{chirp, in-cluster}`, `clusterResourceWhitelist=[{"",Namespace}]`, **no `*/*/*`**). `sync=Unknown` with the literal `ComparisonError: deploy/chirp: app path does not exist` — because `targetRevision: main` and `deploy/chirp` is not on `main` **until `SUBTASK_land_pr` merges the PR** (R2 / #23 HSO-1 ordering, the correct steady-state value per `application.yaml:38-41`). The identity's substance (correct wiring, admitted by the scoped project, `Healthy`) is proven live; the *Synced* sub-check is a pre-merge ordering artifact, resolved post-merge. Flagged for the fold. |

**No gate FAIL requiring a remediation fix-task.** Both qualifiers above are *environment/ordering* conditions
explicitly pre-authorized as "note, do not act on" (#23 HSO-1; R2). The sibling manifests are **correct** — editing
them or injecting a manifest-changing fix-task would corrupt a correct steady-state (`engine_amend_plan { add_task }`
remediation is reserved for a *wrong manifest*, which is not the case here).

---

## 6. Decision record / divergences carried to `SUBTASK_fold` (#23 HSO-1)

1. **Image source override (env-limited)**: pinned private GHCR digest `054af27…` unpullable here (403, no
   `read:packages`); reachability proven with the node-imported functionally-identical `chirp:local` via a
   **live-object patch** (committed manifest unchanged, digest pin intact; audit annotation
   `nswe.deploy-reach/image-override` on the live Deployment). Real-cluster path: GHCR read-cred pull secret or
   public package.
2. **ArgoCD Sync deferred pre-merge (R2)**: `targetRevision: main` lacks `deploy/chirp` until the PR merges;
   `ComparisonError` observed. Wiring + `Healthy` proven; full `Synced` is post-merge. The Application reports 3
   orphaned resources (the directly-`kubectl apply`'d workload objects, unmanaged until the Application can sync) —
   expected pre-merge state.
3. **imagePullSecret**: not creatable here (no GHCR read creds); **no secret committed or created** anywhere.
4. **Ingress mechanism**: k3s built-in Traefik as Ingress (`ingressClassName: traefik`), serverlb `:8081 → 80`,
   host-based `chirp.localhost` — correct/idiomatic for k3d; TLS omitted deliberately for the HTTP demo.
5. **AppProject scoping**: least-privilege confirmed live (scoped destinations, `Namespace`-only cluster
   whitelist, no `*/*/*`) — honored, not loosened.

---

## 7. Side-effect attestation

- **Cluster-only mutations** (as scoped): created ns `chirp` + Deployment/Service/Ingress (direct apply of the
  committed manifests); patched the **live** Deployment image to the node-imported build + an audit annotation;
  applied AppProject `chirp` + Application `chirp` into ns `argocd`. Confined to the k3d `nswe` cluster and the
  `chirp`/`argocd` namespaces; no sibling app/cluster/namespace touched.
- **No git mutation**: checkout still on `main` (`25e90c0`); no `work/deploy-argocd` branch (local or remote); the
  PR/landing is `SUBTASK_land_pr`'s job.
- **Sibling manifests not edited in place**: `/home/user/nswe-demo/deploy/chirp/*` and `deploy/argocd/*` are
  byte-unchanged (the Deployment file still pins `@sha256:054af27…`); the image swap lives only on the cluster object.
- **No secrets** written to the tree, the cluster, or this report.

---

## 8. Self-check against success criteria

- [x] App demonstrably reachable: captured HTTP request+response (`200` on `/healthz` and `/`) through the Traefik ingress; negative-control `404` proves the route (§4).
- [x] Rollout Ready; Service endpoints non-empty; pod not in `ImagePullBackOff`; probes reflect real readiness (§2).
- [x] Private-GHCR pull handled without committing any secret; mechanism documented (§3), with the real cluster path noted.
- [x] Each assigned runtime identity recorded PASS / CONDITIONAL with evidence; the two qualifiers are env/ordering (#23/R2), not manifest FAILs → no remediation fix-task warranted; nothing silently plugged (§5).
- [x] No git side effects; sibling manifests not edited in place (§7).
