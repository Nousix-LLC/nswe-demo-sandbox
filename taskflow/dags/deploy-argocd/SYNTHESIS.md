# SYNTHESIS.md — deploy-argocd verification gate (fold record, NSWE #13)

**Task**: `SUBTASK_fold` (final stage of `SUBTASK_synthesis`). **Role**: the deploy-argocd subtree's final
verification gate and fold point. This record consolidates the three upstream outputs into a single machine-gate
verdict over the **entire** parent contract-identity set (static + runtime, no silent plug), carries the
reachability evidence and the decision record, and is the seam that folds the deploy-argocd subtree to COMPLETED.
**Date**: 2026-10-22. **Mode**: read-only over the three upstream outputs + the contracts; authors this one record
and performs the kernel fold. No manifest edits, no cluster mutation, no git mutation.

## Upstream inputs consolidated (all COMPLETED)

| Source | Output read | Contributes |
|--------|-------------|-------------|
| `SUBTASK_static_gate` | `SUBTASK_static_gate/outputs/static_gate_report.md` | Static per-identity results, wiring, duplication, review; **STATIC GO** |
| `SUBTASK_deploy_reach` | `SUBTASK_deploy_reach/outputs/reachability_evidence.md` | Runtime per-identity results + captured HTTP request/response |
| `SUBTASK_land_pr` | `SUBTASK_land_pr/outputs/pr_record.md` | PR #28, commit SHA, CI green, no-trailers / no-merge / no-main-push |
| `SUBTASK_discovery` | `../SUBTASK_discovery/outputs/ground_truth.md` | Decision-record facts (digest, ports, ingress, pull-secret, #23 divergences) |

---

## 1. Machine-gate verdict

### ✅ PASS — GATE GO (PR open, awaiting human merge)

Every one of the **8 parent contract identities** (`../contracts/_MANIFEST.yaml` `identities`) has a recorded
PASS traceable to an upstream evidence line — no identity is unresolved, none is silently plugged. The four-check
posture holds: **contract identities** (§2), **wiring** (§3), **duplication** (§3), and **combined-output review**
(§3) all reflect in the verdict. **No check FAILed**, therefore no remediation fix-task was injected
(`engine_amend_plan` remediation is reserved for a *wrong manifest*; the manifests are correct).

Two qualifiers are carried transparently (§4), and **both are disclosed, pre-authorized environment/ordering
conditions (#23 HSO-1 / R2) — "note, do not act on" — not manifest defects**:
1. `image-pull-works` is an **environment-bounded CONDITIONAL PASS** — the pinned *private* GHCR digest is
   unpullable in this sandbox (no `read:packages`); runnability was proven with a node-imported,
   functionally-identical build while the committed digest pin was left intact.
2. ArgoCD **`Synced`** is **deferred pre-merge** — `targetRevision: main` lacks `deploy/chirp` until PR #28 merges;
   wiring + `Healthy` are proven live.

Neither qualifier licenses a manifest edit; both resolve on a real cluster / post-merge with the committed
manifests unchanged.

---

## 2. Per-identity results (static half + runtime half)

| # | Identity | Static half | Runtime half | Verdict | Source |
|---|----------|-------------|--------------|---------|--------|
| 1 | **image-pinned-by-digest** | PASS — `10-deployment.yaml:59` pins `@sha256:054af27f…`, byte-equal to `ground_truth` `image_digest`; no `:<tag>` form | n/a (static identity) | **PASS** | static_gate §1 |
| 2 | **resources-and-probes** | PASS — `requests`+`limits` both present (`:66–71`); `liveness`+`readiness` httpGet `/healthz:8080` (`:80–93`); +startupProbe | n/a | **PASS** | static_gate §1 |
| 3 | **appproject-least-privilege** | PASS — `clusterResourceWhitelist` only `{"",Namespace}`, destinations scoped `{chirp, in-cluster}`, no `*/*/*`, `Secret` excluded; Application bound `project: chirp` | PASS — live Application admitted + bound by the live scoped `chirp` AppProject | **PASS** | static_gate §1 · deploy_reach §5 |
| 4 | **namespace-isolation-no-secrets** | PASS — `Namespace chirp` manifest exists; every workload object `namespace: chirp`; tree grep → no committed Secret data | n/a | **PASS** | static_gate §1 |
| 5 | **service-selector-matches-pods** | PASS — selector `{name,part-of}` ⊆ pod labels; `targetPort 8080 == container_listen_port` | PASS — `kubectl get endpoints` → `10.42.1.9:8080` **non-empty**, EndpointSlice `ready=true` after rollout | **PASS** | static_gate §2 · deploy_reach §5 |
| 6 | **ingress-wires-service** | PASS — backend `chirp-server:80`, `ingressClassName: traefik` == `ground_truth`; host `chirp.localhost`, path `/` | PASS — live `GET /healthz` & `/` via `localhost:8081` + `Host: chirp.localhost` → **200 OK**; negative control (no Host → 404) proves the host rule routes | **PASS** | static_gate §2 · deploy_reach §4,§5 |
| 7 | **argocd-application-wired** | PASS — `source.path: deploy/chirp`, `repoURL` = nswe-demo, `dest.namespace: chirp`, `project: chirp` (not `default`) | PASS (wiring + `Healthy`); **`Synced` deferred pre-merge** — `ComparisonError: deploy/chirp app path does not exist` because `targetRevision: main` lacks the path until PR #28 merges (R2/#23) | **PASS** (Sync post-merge) | static_gate §2 · deploy_reach §5 |
| 8 | **image-pull-works** | (pull-secret is a runtime precondition; manifest references `imagePullSecrets: [ghcr-pull]`, correctly uncommitted) | **CONDITIONAL PASS (env-limited)** — no `ImagePullBackOff` in final state, `rollout status` = successfully rolled out, pod `1/1 Running`; pinned *private* digest unpullable here (403, no `read:packages`), proven with node-imported functionally-identical build; committed digest pin intact | **PASS (conditional)** | deploy_reach §2,§3,§5 |

**Coverage check (`../contracts/_MANIFEST.yaml` `identity_coverage`)**: identities 1,2,3,4 owned by `SUBTASK_static_gate`;
5,6,7,8 proven at runtime by `SUBTASK_deploy_reach` (with static halves of 5,6,7 also asserted by static_gate). All
8 covered by exactly one assigned child; both halves recorded where applicable. **No silent plug; no unresolved identity.**

---

## 3. Four-check posture (wiring · duplication · review)

- **Wiring** — PASS (static_gate §3): the six objects form one connected graph; Namespace ← all workload objects;
  Service → selects Deployment, ← Ingress backend; Application → `path: deploy/chirp` + `project: chirp`, lives
  outside its own synced path (no self-reconcile); AppProject ← bound by the Application. No dead/orphan manifest.
- **Duplication** — PASS (static_gate §4): disjoint producers by directory — `deploy/chirp/*` (`SUBTASK_app_manifests`)
  vs `deploy/argocd/*` (`SUBTASK_argocd_gitops`); one `kind:` per file; the outputs mirror is byte-identical.
- **Combined-output review** — strong (static_gate §5): k3s/Traefik idiom correct (`ingressClassName: traefik`,
  serverlb `8081→80`, host `chirp.localhost`); ArgoCD idiom correct (Application in `argocd` ns, outside its synced
  path, `automated {prune,selfHeal}`, SSA, finalizer); security posture strong (PSA `restricted`, non-root 65532,
  `readOnlyRootFilesystem`, caps dropped, digest pin, `Secret` excluded from the AppProject whitelist, no committed
  secrets). PR #28 body is accurate to what shipped and discloses the two #23/R2 conditions as non-defects.

---

## 4. Reachability evidence (request issued + response captured)

Issued through the k3d Traefik ingress (`http://localhost:8081`, host-based `Host: chirp.localhost`) — deploy_reach §4:

```
# API health surface
$ curl -sS -D- -H 'Host: chirp.localhost' http://localhost:8081/healthz
HTTP/1.1 200 OK
Content-Type: application/json
{"service":"chirp-server","status":"ok","version":"0.1.0"}

# WASM SPA surface
$ curl -sS -D- -H 'Host: chirp.localhost' http://localhost:8081/
HTTP/1.1 200 OK
Content-Type: text/html      (<title>chirp</title>, Content-Length 1097)

# Negative control — wrong/absent Host must NOT route to chirp
$ curl -sS -o /dev/null -w '%{http_code}' http://localhost:8081/healthz    # no Host header
404
```

Rollout state at proof time (deploy_reach §2): Deployment `1/1` Available; pod `Running`, 0 restarts; Service
endpoints `10.42.1.9:8080` non-empty (`ready=true`); no `ImagePullBackOff` in the final state. The `404` negative
control proves the host-based Ingress rule is what routes the `200`s — end-to-end
`serverlb:8081 → Traefik → Ingress(host=chirp.localhost) → Service chirp-server:80 → targetPort 8080 → pod`.
Reachability is **demonstrated, not asserted.**

---

## 5. Decision record

- **Ingress mechanism** — k3s built-in **Traefik as Ingress** (`ingressClassName: traefik`); k3d serverlb maps
  `localhost:8081 → 80`; host-based routing on `chirp.localhost`, path `/` (Prefix). TLS omitted deliberately for
  the HTTP demo. Idiomatic for k3d/k3s.
- **AppProject scoping** — least-privilege confirmed both statically and live: `destinations` scoped to
  `{namespace: chirp, server: https://kubernetes.default.svc}`, `clusterResourceWhitelist` only `{"",Namespace}`,
  `sourceRepos` only the nswe-demo repo, `Secret` excluded from the namespace whitelist. **No `*/*/*`.** The
  Application is bound by `spec.project: chirp` (not `default`). Honored, not loosened.
- **imagePullSecret handling** — GHCR `chirp-server` package is **private** (`ground_truth §6`). The Deployment
  references `imagePullSecrets: [ghcr-pull]`, correctly applied **out-of-band** (not committed, not in the AppProject
  whitelist). In this sandbox no valid GHCR read credential exists (the `gh` token lacks `read:packages`), so the
  `ghcr-pull` Secret could not be provisioned and **no secret entered the tree or the cluster**
  (`kubectl -n chirp get secrets` → none). Reachability was instead demonstrated with a node-imported,
  functionally-identical `chirp:local` build via a **live-object patch** (committed manifest unchanged, digest pin
  intact, audit annotation `nswe.deploy-reach/image-override`). **Real-cluster / post-#23 path**: provide a
  `kubernetes.io/dockerconfigjson` `ghcr-pull` Secret in ns `chirp` from a `read:packages` token (or make the
  package public), and the committed manifest pulls the pinned digest directly with no override.
- **Native-cluster divergences noted for #23 (HSO-1)** — scope is k3d-hosted k3s only; these are noted, **not acted on**:
  1. *Image source* — pinned private GHCR digest unpullable in-sandbox; node-imported identical build used (above).
  2. *ArgoCD `Sync` deferred pre-merge (R2)* — `targetRevision: main` lacks `deploy/chirp` until PR #28 merges;
     `ComparisonError` + 3 orphaned (directly-applied) resources are the expected pre-merge state; wiring + `Healthy`
     proven; full `Synced` resolves post-merge. `targetRevision: main` is the correct steady-state value (tracking
     the feature branch would be an anti-pattern) — left unchanged.
  3. *imagePullSecret* — not creatable here; no secret committed or created anywhere.

---

## 6. PR link

- **PR**: https://github.com/Nousix-LLC/nswe-demo/pull/28 (**#28**) — `deploy-argocd: k8s manifests + ArgoCD Application (Closes #13)`
- **Base** `main` (`ada3aa97eb2d580b7b5b9cb1b0ca898f2ad6fbf2`); **Head** `work/deploy-argocd` (based at `ada3aa9`).
- **Commit** `63a299a0eef1ccb638fb112a47888f272f514690` — 8 files, +568/-0, confined to `deploy/chirp/*` + `deploy/argocd/*`.
- **Closes #13** (confirmed via `closingIssuesReferences → [13]`). **No attribution trailers** on the commit or PR body (#27/HYG-1).
- **CI green** — run `37818968143`, `completed/success` (fmt, clippy, test, wasm, doc, image all pass).
- **State OPEN / not merged**; `origin/main` still `ada3aa9` (**not pushed, not force-pushed**). Merge is the human's / out of this subtree's scope.

---

## 7. Fold

Per `../contracts/synthesis_gate_contract.yaml` `fold_output` and `../contracts/_MANIFEST.yaml` `fold_obligation`,
this record is authored at the deploy-argocd subtree root (`SYNTHESIS.md`) and is the seam that folds the subtree:

- `SUBTASK_synthesis` (sub-subtree root) — SUSPENDED/NeedsDecompose → resumed **COMPLETED** via `engine_resume_suspended` (seam = this `SYNTHESIS.md`, synthesized = `SUBTASK_fold`).
- `deploy-argocd` (subtree root) — SUSPENDED/NeedsDecompose → resumed **COMPLETED** via `engine_resume_suspended` (seam = this `SYNTHESIS.md`, synthesized = `SUBTASK_fold`).

Neither ancestor is left dangling SUSPENDED.

---

## 8. Success-criteria self-check

- [x] Every parent contract identity has a recorded PASS/FAIL sourced from an upstream output — 8/8 covered, no silent plug, no unresolved identity (§2).
- [x] Four-check posture honored — contract identities + wiring + duplication + review all reflected; no FAIL, so no injected remediation (§1,§3).
- [x] `SYNTHESIS.md` present at the deploy-argocd subtree root with verdict, per-identity results (static+runtime), reachability evidence, decision record, PR link (§1–§6).
- [x] Fold performed — both `SUBTASK_synthesis` and `deploy-argocd` resumed to COMPLETED with this `SYNTHESIS.md` as the seam; neither left SUSPENDED (§7).
