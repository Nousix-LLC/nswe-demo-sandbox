# _BRIEF.md — deploy-argocd (NSWE work-item #13, code DAG, persona swe-coder)

You are a `swe-coder` code DAG for the NSWE engagement on `Nousix-LLC/nswe-demo`. This brief is your whole task
spec. Evaluate your own scope and choose your own decomposition and methodology; this brief describes **what** to
deliver and **what to get right**, not how to build it.

## Objective
Close issue **#13 — deploy-argocd: k8s manifests + ArgoCD Application (GitOps on k3s)** (EPIC #3 DevOps; depends
on the already-landed #10 infra-bootstrap, #11 CI, #12 containerize). Deliver the Kubernetes deployment manifests
for the `chirp` application and an ArgoCD `Application` that tracks this repo so the app auto-syncs onto the k3s
cluster via GitOps, **and the deployed app is actually reachable.**

## Acceptance criteria (testable)
1. `deploy/` carries k8s manifests for the chirp app: at minimum a **Namespace**, a **Deployment** of
   `chirp-server` (the containerized app from #12, image `ghcr.io/nousix-llc/chirp-server`), a **Service**, and
   an **Ingress** (or an equivalent, justified reachability mechanism for k3s/k3d). Resolve and reference the
   **actual published image** from the #11 CI pipeline; pin it by immutable **digest (`@sha256:`)**, not a movable
   tag (see concern: supply-chain).
2. The Deployment declares **resource requests/limits** and **liveness + readiness probes** (a healthcheck exists
   at `deploy/docker/healthcheck.rs`; use the app's real health surface).
3. An **ArgoCD `Application`** manifest tracks this repository's `deploy/` path and syncs the app into its
   namespace on the in-cluster ArgoCD. Scope it through an **AppProject** with least-privilege destinations
   (see concern: RBAC/#24), not the stock cluster-admin posture.
4. **Reachability is demonstrated**, not just asserted: the app is reachable on the live k3d-hosted k3s cluster
   (the k3d serverlb maps host `localhost:8081 -> 80` and `8444 -> 443` via the k3s Traefik ingress; a NodePort
   or port-forward is an acceptable alternative if justified). Show the evidence in your synthesis (e.g. an HTTP
   request against the ingress/service returning the SPA or an API health response). If a private GHCR package
   requires an `imagePullSecret`, handle it (or document making the package pullable) so the pod does not wedge in
   `ImagePullBackOff`.
5. A **PR into `main`** that `Closes #13`, commits on branch **`work/deploy-argocd`**, CI green, and a root
   **`SYNTHESIS.md`** carrying your machine-gate verdict (PASS/FAIL), the decision record, and the reachability
   evidence.

## Inputs (what you build on)
- `origin/main @ ada3aa9` — the integration branch. Landed and merged: the app layer (ferric #4-6, chirp #7-9),
  #10 infra-bootstrap (`deploy/bootstrap/{cluster,gitops,wasm}` scripts that stood up the cluster + ArgoCD),
  #11 CI (`.github/workflows/ci.yml`, which builds and on `main` publishes `ghcr.io/nousix-llc/chirp-server`),
  and #12 containerize (root `Dockerfile` multi-stage build bundling the wasm frontend; `deploy/docker/healthcheck.rs`).
- The **live cluster**: k3d cluster `nswe`, k3s v1.35.5+k3s1, ArgoCD running in ns `argocd`. Inspect it read-only
  to ground your manifests (ingress class, storage, the ArgoCD version/AppProject surface).
- Issue **#24** (ArgoCD RBAC least-privilege + supply-chain hardening) and issue **#23** (native-install-path /
  durability caveats) — read both; their concerns are folded in below.

## Declared output
- Commits on `work/deploy-argocd`; a PR into `main` that closes #13; a root `SYNTHESIS.md` verdict at the DAG
  workspace root. A DAG never merges its own PR and never pushes to `main`.

## What to evaluate / concerns to cover (named; you select & load the methodology)
- **Correctness of the k8s/GitOps deploy** — valid, minimal manifests; ArgoCD Application + AppProject that
  actually syncs on this cluster; declarative, idempotent, reconcilable.
- **Reachability** — the app is reachable from outside the cluster through the k3d/k3s ingress path (or a
  justified NodePort/port-forward); image pull works (no ImagePullBackOff); probes reflect real readiness.
- **RBAC least-privilege (#24 SEC-2)** — do NOT rely on the stock `application-controller` `*/*/*`
  cluster-admin-equivalent ClusterRole; constrain the Application's permissions via an AppProject with explicit
  allowed destinations/resources. Express any hardening as GitOps-managed config.
- **Supply-chain hardening (#24 SEC-3)** — reference the app image by immutable `@sha256:` digest; pin any other
  referenced manifests/charts by SHA; note (do not necessarily implement) a cosign/admission follow-up.
- **`--force-conflicts` survival (#24 SEC-4)** — ensure RBAC narrowing is GitOps-managed so it is not silently
  reverted by a re-run of the infra install path.
- **Durability caveat (#23 HSO-1)** — the deploy targets the proven **k3d-hosted k3s** cluster (the engagement's
  cluster). The native/systemd production install path is a separate, unproven follow-up (#23) — do NOT take it
  on here; just do not assume it, and note any manifest choice that would differ on a native cluster.
- **Resource limits & health** — requests/limits, liveness/readiness, graceful shutdown.
- **Security / trust boundary** — namespace isolation, no secrets in the tree, minimal RBAC, ingress TLS posture
  appropriate to k3d.
- **k8s / k3s idiom** — conventions a k3s/ArgoCD reviewer expects.

## Constraints
- Repo scope: `Nousix-LLC/nswe-demo` only. Branch `work/deploy-argocd`; PR into `main`.
- Never force-push `main`; never rewrite merged history. **Add NO attribution trailers** to commits or the PR
  body (the engagement forbids them — see #27/HYG-1). Keep the PR body accurate to what shipped.
- Only this project's k3s (k3d-hosted) cluster/namespaces and its ArgoCD. Do not touch sibling apps/clusters.
- You are the only writer of your branch; do not merge your own PR.
