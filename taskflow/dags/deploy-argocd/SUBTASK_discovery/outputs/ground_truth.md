# ground_truth.md — resolved facts for the chirp deploy (NSWE #13, deploy-argocd)

**Task**: `SUBTASK_discovery` (Group 0, serialized precursor). **Produced by**: swe-coder discovery agent.
**Resolved**: 2026-10-08. **Cluster inspection was strictly read-only** (no mutations).

This file is the single source of truth both authoring spokes (`SUBTASK_app_manifests`,
`SUBTASK_argocd_gitops`) and the `SUBTASK_synthesis` gate consume. Field names match
`../contracts/_MANIFEST.yaml` `derived_facts` so downstream tasks can read them unambiguously. Every
fact carries its provenance (the command or file it came from).

---

## derived_facts (contract-aligned)

| Field | Value |
|---|---|
| `repo_checkout_path` | `/home/user/nswe-demo` |
| `image_digest` | `ghcr.io/nousix-llc/chirp-server@sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3` |
| `container_listen_port` | `8080` |
| `health_path` | `/healthz` (API health endpoint; SPA is served at `/`) |
| `ingress_class` | `traefik` |
| `argocd_application_apiversion` | `argoproj.io/v1alpha1` |
| `appproject_apiversion` | `argoproj.io/v1alpha1` |
| `ghcr_package_private` | `true` (→ an imagePullSecret is required, unless the package is made public) |
| `storage_notes` | None required — chirp-server is stateless (in-memory repository default). Cluster default StorageClass is `local-path` if a PVC is ever introduced. |

All fields are RESOLVED. None is left unresolved.

---

## 1. `repo_checkout_path` — and a REQUIRED base-checkout caveat ⚠

**Value**: `/home/user/nswe-demo`

- Remote: `https://github.com/Nousix-LLC/nswe-demo.git` (correct repo); working tree clean.
  - Provenance: `git -C /home/user/nswe-demo remote get-url origin`; `git status --short` (empty).
- The declared base **`ada3aa9` is the current `origin/main` HEAD** on GitHub — it is the live base, not a detached historical commit.
  - Provenance: `gh api repos/Nousix-LLC/nswe-demo/commits/main --jq .sha` → `ada3aa97eb2…`; full SHA `ada3aa97eb2d580b7b5b9cb1b0ca898f2ad6fbf2`. Message: `CI: GitHub Actions for the Rust/WASM workspace (#11)`.

### ⚠ The checkout's working tree is STALE — the authoring spokes MUST re-base before writing

- The checkout's local `main` is checked out at **`25e90c0`** ("ferric-http … (#15)"), which git reports as **`[origin/main: behind 5]`** — i.e. **5 commits BEHIND `ada3aa9`**, and `ada3aa9` is NOT reachable from `25e90c0`.
  - Provenance: `git -C /home/user/nswe-demo branch -vv` → `* main 25e90c0 [origin/main: behind 5]`; `git merge-base --is-ancestor ada3aa9 25e90c0` → non-zero (NO).
- **Consequence**: the **root `Dockerfile` and the entire `deploy/` tree were added in #11 (`ada3aa9`) and are NOT present in the currently checked-out tree** (`ls Dockerfile` / `ls deploy/docker/healthcheck.rs` both fail at the current HEAD). They DO exist at `ada3aa9` (verified read-only via `git ls-tree -r ada3aa9` and `git show ada3aa9:<path>`).
- **Action the authoring spokes MUST take** (discovery did NOT mutate the checkout): create the work branch from the real base before authoring, e.g.
  ```
  git -C /home/user/nswe-demo fetch origin
  git -C /home/user/nswe-demo checkout -B work/deploy-argocd ada3aa9   # == origin/main
  ```
  Do NOT branch off the current local `main`/`HEAD` (`25e90c0`) — it predates #11 and lacks the Dockerfile and `deploy/` path. The spokes write `deploy/chirp/` and `deploy/argocd/` onto this `work/deploy-argocd` branch based at `ada3aa9`.
- The `work/deploy-argocd` branch does not exist yet (local or remote): `git branch -a --list '*deploy-argocd*'` → empty.

> An alternate clean checkout at `/tmp/rcia-clone` exists but is on branch `work/ci-actions` and does **not** contain `ada3aa9` — do not use it. `/home/user/nswe-demo` is the correct checkout.

---

## 2. `image_digest` — the ACTUAL published digest (immutable), not a tag

**Value**: `ghcr.io/nousix-llc/chirp-server@sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3`

- This is the **published manifest-list (multi-arch index) digest** — the correct, immutable thing to pin.
- The `#11` CI `image` job publishes to GHCR **only on push to `main`**, tagging `type=sha,format=long` (→ `sha-<full-commit-sha>`) and `latest`. Both tags for the `ada3aa9` main build resolve to the digest above.
- **Provenance** (GitHub Actions run `37805862710`, the single successful `ci.yml` push run on `main` @ `ada3aa97eb2…`), three corroborating log lines:
  - `Summarize published image` step: `digest: sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3` (the `docker/build-push-action` `outputs.digest`).
  - `exporting manifest list sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3 done`.
  - `pushing manifest for ghcr.io/nousix-llc/chirp-server:latest@sha256:054af27…` AND `…:sha-ada3aa97eb2d580b7b5b9cb1b0ca898f2ad6fbf2@sha256:054af27…`.
  - Obtained with: `gh run list --repo Nousix-LLC/nswe-demo --workflow ci.yml --branch main --event push` then `gh run view 37805862710 --log`.
- The single-platform child manifest digest (for reference only, do NOT pin this) is `sha256:f341329f7d4cb585ba5c6b428ff47c3d38a9825fd2c12cc93d39559dcc3216a8`. **Pin the manifest-list digest `054af27…`.**
- Direct registry inspection (`docker buildx imagetools inspect`, registry `/v2/.../tags/list`) was **blocked** in this environment — see §8 (the available `gh` token lacks `read:packages`). The Actions publish log is the authoritative source used here and is unambiguous.

Full digest line to paste into the Deployment:
```
image: ghcr.io/nousix-llc/chirp-server@sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3
```

---

## 3. `container_listen_port` = `8080`

- Provenance: root `Dockerfile` @ `ada3aa9` (`git show ada3aa9:Dockerfile`):
  - `ENV CHIRP_BIND_ADDR=0.0.0.0:8080` (binds `0.0.0.0`, not the `127.0.0.1` dev default, so the port is reachable from outside the container).
  - `EXPOSE 8080`.
  - `8080` is unprivileged, so the non-root user (uid/gid **65532**, `USER 65532:65532`) can bind it.
- Corroborated by `deploy/docker/healthcheck.rs` (`git show ada3aa9:deploy/docker/healthcheck.rs`): the probe derives its port from `CHIRP_BIND_ADDR`, default `8080`.

**For the Service**: `targetPort: 8080` (== `container_listen_port`); contract `service.port` stays `80`.

---

## 4. `health_path` = `/healthz` (API health endpoint — NOT the SPA root)

- Provenance: `Dockerfile` header doc + `HEALTHCHECK` + `healthcheck.rs` @ `ada3aa9`:
  - Dockerfile verify note: `curl -fsS http://127.0.0.1:8080/healthz   # -> {"status":"ok",...}` and `open http://127.0.0.1:8080/   # -> the SPA`.
  - `healthcheck.rs` issues exactly one `GET /healthz HTTP/1.0` over loopback and maps **HTTP 200 → healthy (exit 0)**, else unhealthy.
  - Container `HEALTHCHECK` runs the standalone `/usr/local/bin/healthcheck` binary (distroless has no shell/curl/wget) every 30s, timeout 5s, start-period 5s, 3 retries.
- **Distinction (SPA root vs API health)**: `/` serves the WASM SPA (HTML); `/healthz` is the JSON API health endpoint returning `{"status":"ok",...}` with status 200. **k8s liveness/readiness probes MUST target `/healthz` on port 8080**, not `/`.

Recommended k8s probe shape (both spokes should align on this):
```yaml
livenessProbe:  { httpGet: { path: /healthz, port: 8080 }, periodSeconds: 30, timeoutSeconds: 5, failureThreshold: 3 }
readinessProbe: { httpGet: { path: /healthz, port: 8080 }, periodSeconds: 10, timeoutSeconds: 3, failureThreshold: 3 }
```
- **Graceful shutdown**: `ENTRYPOINT ["/usr/local/bin/chirp-server"]` (exec form) → chirp-server is PID 1 and receives `SIGTERM` directly; it drains in-flight requests via tokio graceful shutdown. No special `preStop` hook required; a modest `terminationGracePeriodSeconds` (e.g. 30) is appropriate.
- **Runtime user / security context**: runs as non-root uid/gid `65532`, distroless/cc base. The Deployment can safely set `runAsNonRoot: true`, `runAsUser: 65532`, `readOnlyRootFilesystem: true` (SPA is read at `/srv/chirp`; config via env only).

---

## 5. Cluster facts (live k3d `nswe` / k3s v1.35.5+k3s1, read-only)

- **Cluster**: k3d cluster `nswe`, k3s **v1.35.5+k3s1**, 1 server + 1 agent, both `Ready`.
  - Provenance: `k3d cluster list`; `kubectl get nodes -o wide` (versions `v1.35.5+k3s1`, runtime `containerd://2.2.3-k3s1`). Context `k3d-nswe`.
- **`ingress_class` = `traefik`**: the k3s built-in Traefik ingress controller.
  - Provenance: `kubectl get ingressclass` → `traefik  traefik.io/ingress-controller`; `kubectl -n kube-system get deploy` → `traefik 1/1`, plus `svclb-traefik-*` DaemonSet (the serverlb path).
  - The Ingress should set `spec.ingressClassName: traefik`. The k3d serverlb maps host `localhost:8081 -> 80` and `8444 -> 443` through Traefik; reachability tests hit `http://localhost:8081` (with the chosen Host header if host-based routing is used).
- **ArgoCD**: installed in namespace `argocd`, version **v3.5.4** (`quay.io/argoproj/argocd:v3.5.4`); all core workloads `1/1` (server, repo-server, application/notifications/applicationset controllers, dex, redis).
  - Provenance: `kubectl -n argocd get deploy -o wide`; `kubectl -n argocd get deploy argocd-server -o jsonpath='{…image}'`.
- **`argocd_application_apiversion` = `argoproj.io/v1alpha1`** and **`appproject_apiversion` = `argoproj.io/v1alpha1`**.
  - Provenance: `kubectl get crd applications.argoproj.io` and `appprojects.argoproj.io` → group `argoproj.io`, kind `Application`/`AppProject`, version `v1alpha1` (served=true, storage=true). (`applicationsets.argoproj.io` v1alpha1 is also present but not needed for this task.)
- **Namespaces**: `argocd` is `Active`. **`chirp` does NOT exist yet** — the `SUBTASK_app_manifests` spoke authors a `Namespace` manifest for `chirp` (and/or the ArgoCD Application uses `syncOptions: CreateNamespace=true`). Both spokes must keep every resource in namespace `chirp`.
  - Provenance: `kubectl get ns` (no `chirp`).
- **`storage_notes`**: single StorageClass `local-path` (default; `rancher.io/local-path`, `WaitForFirstConsumer`, no volume expansion). chirp-server uses the in-memory repository default (no DB, no persistent volume) per the Dockerfile — **no PVC/StorageClass is needed** for this deploy.
  - Provenance: `kubectl get storageclass`.

---

## 6. `ghcr_package_private` = `true` → imagePullSecret required

- **Signal (authoritative available signal)**: the GHCR anonymous token endpoint **denies** anonymous pull for this package:
  - `curl -s -o /dev/null -w '%{http_code}' "https://ghcr.io/token?scope=repository:nousix-llc/chirp-server:pull&service=ghcr.io"` → **`401`**. For a PUBLIC GHCR package this endpoint returns `200` with an anonymous pull token; a `401` means anonymous pull is not permitted → **the package is private**.
  - `docker buildx imagetools inspect ghcr.io/nousix-llc/chirp-server:latest` (no auth) → `401 Unauthorized` (anonymous), and `403 Forbidden` after login with the environment token (that token lacks `read:packages`).
- **Caveat on directness**: the direct visibility flag (`gh api /orgs/nousix-llc/packages/container/chirp-server --jq .visibility`) could NOT be read here — it returns `403: You need at least read:packages scope`. The `private=true` conclusion is therefore inferred from the anonymous-`401` denial, which is a reliable public/private discriminator. (Note the parent repo `Nousix-LLC/nswe-demo` is itself **public** — `gh api repos/… --jq .private` → `false` — but GHCR **package** visibility is independent of repo visibility and defaults to private.)
- **Implications for the spokes/gate** (either path is acceptable; the gate's `image-pull-works` identity must hold → no `ImagePullBackOff`):
  1. **imagePullSecret path** — create a `kubernetes.io/dockerconfigjson` Secret in namespace `chirp` with GHCR read credentials and reference it via the Deployment `imagePullSecrets` (and/or the ServiceAccount). **Do NOT commit the secret to the tree** (constraint: no secrets in git); apply it out-of-band or via a sealed/external-secret mechanism, and document that in `SYNTHESIS.md`. OR
  2. **Make the package public** — set the `chirp-server` GHCR package visibility to public, after which no pull secret is needed; document the choice.
- This is the one fact with an environmental limitation on direct confirmation; it is flagged so the authoring spokes handle the pull-secret path deliberately rather than discovering an `ImagePullBackOff` at deploy time.

---

## 7. Cross-reference to contract identities (for the authoring spokes)

Values the spokes must wire consistently (from `../contracts/deploy_contract.yaml` + these facts):

- Deployment image → `ghcr.io/nousix-llc/chirp-server@sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3` (digest, never a tag).
- Service `targetPort: 8080` (== `container_listen_port`); `port: 80`; `type: ClusterIP`; name `chirp-server`.
- Ingress `ingressClassName: traefik`; backend → Service `chirp-server` port `80`; path `/` (Prefix); reachable via `http://localhost:8081`.
- Probes (liveness + readiness) → `httpGet /healthz:8080`; resources requests AND limits present; `terminationGracePeriodSeconds` ~30; non-root 65532.
- ArgoCD `Application` (`argoproj.io/v1alpha1`) → `spec.source.path: deploy/chirp`, `repoURL` = the nswe-demo repo, `destination.namespace: chirp`, `spec.project: chirp` (the AppProject, NOT `default`); consider `syncOptions: CreateNamespace=true` since `chirp` ns is absent.
- `AppProject` (`argoproj.io/v1alpha1`) `chirp` → `destinations` scoped to `{namespace: chirp, server: https://kubernetes.default.svc}` (+ `argocd` only if strictly required), NO `*/*/*` clusterResourceWhitelist; narrowing GitOps-managed.
- All resources in namespace `chirp`; a `Namespace` manifest exists; no secrets committed; pull-secret path handled per §6.

---

## 8. Environmental limitations encountered (full disclosure)

- The `gh` token present in this environment has scopes `gist, project, read:org, repo, workflow` — **no `read:packages`**. This blocked (a) the GHCR Packages REST API (`.../packages/container/chirp-server`), and (b) authenticated registry `tags/list` / `imagetools inspect` (`403 permission_denied: token … scopes`). It did NOT block the image-digest resolution, which was taken authoritatively from the `#11` Actions publish-run log (§2). It left the GHCR private/public flag resolvable only by the anonymous-`401` inference (§6), not by the direct visibility field.
- The repo checkout was inspected **read-only**; its working tree was NOT modified (branch creation / rebase is left to the authoring spokes per §1). The Dockerfile and `deploy/docker/healthcheck.rs` were read from the `ada3aa9` git objects via `git show ada3aa9:<path>`, not from a checked-out tree.
- The k3d cluster was inspected **read-only** (`get`/`jsonpath` only); no `apply`/`create`/`delete`/`patch` was issued.

---

## Self-check against success criteria

- [x] Every `derived_facts` field resolved and recorded with provenance (none left unresolved).
- [x] Image digest is a real published `@sha256:` manifest-list digest (`054af27…`), not a placeholder/tag.
- [x] Cluster inspection was read-only (no mutations).
- [x] `outputs/ground_truth.md` exists and is self-contained.
- [x] Field names match `../contracts/_MANIFEST.yaml` `derived_facts`.
- [x] No secrets written to the tree or this file.
