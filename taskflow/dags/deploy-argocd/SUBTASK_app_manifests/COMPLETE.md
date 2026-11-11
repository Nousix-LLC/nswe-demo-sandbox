# COMPLETE — SUBTASK_app_manifests

**Task**: Author the chirp app Kubernetes workload manifests (`deploy/chirp/`).
**Status**: completed (Atomic).
**Owner scope respected**: wrote ONLY `deploy/chirp/`. Did not touch `deploy/argocd/` (sibling),
did not `kubectl apply`, did not run git/gh (synthesis-gate scope).

## What was produced

Repo working tree (primary artifact location, per the ownership contract):
`/home/user/nswe-demo/deploy/chirp/`

- `00-namespace.yaml` — `Namespace chirp` (+ Pod Security Admission `restricted`).
- `10-deployment.yaml` — `Deployment chirp-server` (digest-pinned image, startup/liveness/readiness
  probes on `/healthz:8080`, requests+limits, graceful shutdown, `restricted`-compliant
  securityContext, `imagePullSecrets: [ghcr-pull]`, `replicas: 1`).
- `20-service.yaml` — `Service chirp-server` ClusterIP `80` → targetPort `8080`.
- `30-ingress.yaml` — `Ingress chirp-server` class `traefik`, host `chirp.localhost`, path `/`.
- `README.md` — reachability contract, pull-secret handling, design notes, native-cluster
  divergences (#23 HSO-1), and the git-state handoff to the synthesis gate.

A verbatim mirror is kept under this workspace at
`outputs/deploy/chirp/` as a stable source independent of any repo git operation.

## Composition against `../contracts/` (all identities self-verified: ALL PASS)

- Image `ghcr.io/nousix-llc/chirp-server@sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3` — immutable digest, never a tag (#24 SEC-3).
- Service `.spec.selector` (`name`+`part-of`) is a subset of the Deployment pod-template labels; `targetPort 8080` == `container_listen_port`; Service `port 80`.
- Ingress backend → Service `chirp-server:80`; `ingressClassName: traefik` == `ground_truth.ingress_class`; host `chirp.localhost` recorded for the Host-header reachability test via `http://localhost:8081`.
- Deployment declares resource **requests AND limits** and **liveness + readiness** (+ startup) probes on the real health surface `/healthz:8080`; `terminationGracePeriodSeconds: 30`.
- All resources in namespace `chirp`; a `Namespace` manifest exists; **no secrets committed** to the tree.
- Private GHCR package handled: `imagePullSecrets: [ghcr-pull]` referenced; the Secret is created out-of-band by the deploy step (documented in README), NOT committed. Alternative (make package public) documented.

## Reachability the synthesis gate should demonstrate

```sh
curl -H 'Host: chirp.localhost' http://localhost:8081/healthz   # expect HTTP 200 {"status":"ok",...}
curl -H 'Host: chirp.localhost' http://localhost:8081/          # expect HTTP 200 (SPA)
```

## Handoff notes for the synthesis gate (git state)

The checkout was on `main @ 25e90c0`, 5 behind `origin/main @ ada3aa9` (where `deploy/` + the
`Dockerfile` live). These manifests were written as **untracked** files. The gate must:
`git fetch origin` → `git checkout -B work/deploy-argocd ada3aa9` (untracked `deploy/chirp/`
survives; it doesn't exist at `ada3aa9`) → stage/commit `deploy/chirp/`. Do NOT `git clean`/`reset
--hard` before staging. Also create the `ghcr-pull` Secret in ns `chirp` (or make the package
public) so the image pulls.

## Decision record (load-bearing choices)

- **`replicas: 1`** — in-memory repository (no DB/PVC); >1 would split state. Scale-out needs a shared store first.
- **Ingress (not Gateway API)** — k3s ships Traefik as an Ingress controller; contract + ground_truth specify an Ingress with class `traefik`. Correct, idiomatic for this target; Gateway-API migration is a cluster-platform decision, not this app's.
- **PSA `restricted` enforced at the namespace** — pod is fully compliant, so enforcement is safe defense-in-depth.
- **TLS omitted** — plain HTTP via the k3d serverlb for the demo; native deploy would terminate TLS at Traefik (documented divergence).
