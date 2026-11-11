# SYNTHESIS — review-deploy-argocd (NSWE #13) — code-review verdict for PR #28

**Review DAG**: `review-deploy-argocd` (persona `swe-coder`), forked by overseer I49. **Role**: independent
code-review gate for **PR #28** (`work/deploy-argocd` → `main`, head `63a299a0`, `Closes #13`) — the k8s
manifests + ArgoCD Application/AppProject that deploy `chirp-server` onto the live k3d `nswe` k3s cluster via
GitOps. **Mode**: read-and-report only — no tree edit, no push, no merge, no manifest change. **Date**: 2026-10-08.
**Methodology spine**: `code-review` (process + checklist); applied with k8s/GitOps/security domain judgement.

This `SYNTHESIS.md` body is the **authoritative verdict**. The GitHub-visible record (PR comment, inline
findings, board item, backlog issue) is the #26 projection of it; because the PR author (`mattsmcknight`) ==
the authenticated account, `gh pr review --approve` is blocked, so the **PR comment** — not a `gh` review
state — carries the visible verdict.

---

## Verdict

```
APPROVE   (fit to land against #13's acceptance criteria)
blockers: 0
non-blockers: 6  (1 operational / merge-readiness; 2 informational/ordering; 3 polish nits)
```

PR #28 is a small (8 files, +568/-0 — 6 manifests + 2 READMEs), cohesive, well-engineered change. Every #13
acceptance criterion is met; the security/least-privilege posture is strong and preemptively satisfies the
intent of #24; reachability is genuinely demonstrated and I **reproduced it independently** on the live cluster.
No finding rises to a blocker. The one finding worth real attention is operational, not a manifest defect: the
private-GHCR `imagePullSecret` is a rollout precondition that was never exercised end-to-end in the authoring
sandbox — it must be provisioned (or the package made public) before/at merge, else ArgoCD auto-sync will
`ImagePullBackOff` post-merge. That is a deploy-readiness gate, not a reason to withhold approval of the code.

**An approve that lists a blocker would not be an approval. This one lists none** — all six findings below are
non-blocking.

---

## Acceptance criteria (#13) — pass/fail

| # | #13 / #24 criterion | Result | Evidence (file:line / live check) |
|---|---------------------|--------|-----------------------------------|
| A1 | `deploy/` k8s manifests: Namespace, Deployment, Service, Ingress | **PASS** | `deploy/chirp/{00-namespace,10-deployment,20-service,30-ingress}.yaml` — all four present, one `kind:` each |
| A2 | ArgoCD `Application` (GitOps) tracking this repo's deploy path, syncing `chirp-server` | **PASS** | `deploy/argocd/application.yaml` — `source.path: deploy/chirp`, `repoURL` nswe-demo, `dest.namespace: chirp`, `spec.project: chirp` (not `default`); lives in ns `argocd`, outside its synced path → no self-reconcile |
| A3 | Image digest-pinned (`@sha256:…`, never a movable tag) | **PASS** | `10-deployment.yaml:59` → `…chirp-server@sha256:054af27f…`; `imagePullPolicy: IfNotPresent`; no `:tag` form anywhere |
| A4 | Demonstrated reachability | **PASS (independently reproduced)** | My own live GET through Traefik: `GET /healthz` → `200` `{"service":"chirp-server","status":"ok","version":"0.1.0"}`; `GET /` → `200`; no-Host negative control → `404`. Full path `serverlb:8081 → Traefik → Ingress(host=chirp.localhost) → Svc:80 → targetPort 8080 → pod`. See qualifier Q1 on the *image used*. |
| A5 | Resource limits + liveness/readiness probes | **PASS** | `requests` cpu `50m`/mem `64Mi`, `limits` cpu `500m`/mem `256Mi` (`10-deployment.yaml:66–71`); startup+liveness+readiness all `httpGet /healthz:8080` — the real API health surface, not the SPA `/` |
| A6 | PR into `main` | **PASS** | PR #28, base `main`, head `63a299a0`, OPEN / MERGEABLE / CLEAN, CI green (run 37818968143, 6/6); `Closes #13`; no attribution trailers (#27/HYG-1 honored) |
| A7 | Root `SYNTHESIS.md` | **PASS** | code DAG's `SYNTHESIS.md` (gate=PASS, round 1) present; this review's `SYNTHESIS.md` is the review gate |
| A8 | #24 least-privilege RBAC + supply-chain (folded into #13) | **PASS** | AppProject `chirp` scoped off `*/*/*`: `clusterResourceWhitelist`=`{"",Namespace}` only, enumerated `namespaceResourceWhitelist`, `Secret` excluded, one `{server,ns}` destination, `sourceRepos`=nswe-demo only. Verified live. |

**Two disclosed qualifiers (carried from the code DAG, independently re-verified — both environment/ordering, not defects):**
- **Q1 — image pull (env limitation).** The pinned *private* GHCR digest is unpullable in the authoring sandbox
  (403, the available `gh` token lacks `read:packages`). Reachability was proven with a node-imported,
  functionally-identical `chirp:local` via a **live-object image patch**; the committed manifest is byte-unchanged
  (digest pin intact). I confirmed this live: `deploy/chirp` Deployment's live image = `docker.io/library/chirp:local`
  with annotation `nswe.deploy-reach/image-override` explaining why. Honest, disclosed, pre-authorized (#23 HSO-1 /
  ground_truth §8). **Consequence → non-blocker F1 below.**
- **Q2 — ArgoCD Sync deferred pre-merge.** Live Application `health=Healthy` but `sync=Unknown`
  (`ComparisonError: deploy/chirp: app path does not exist`, 3 orphaned resources) — purely because
  `targetRevision: main` and `deploy/chirp` is not on `main` until #28 merges. Resolves on merge. Not a defect.
  **Consequence → non-blocker F2 below.**

---

## Independent verification I performed (not merely trusting the code DAG's evidence)

Read-only over the live k3d `nswe` cluster (context `k3d-nswe`) + the PR diff; no mutation:

- **Reachability reproduced** (GET is read-only): `/healthz` → `200` + correct JSON body; `/` → `200`; no-Host → `404`.
  The green is real and reproducible, not a fabricated artifact.
- **Live cluster state** matches the evidence exactly: Deployment `1/1` Available, pod `Running` 0 restarts,
  Service `ClusterIP …:80`, Endpoints `10.42.1.9:8080` (non-empty), Ingress `traefik`/`chirp.localhost`,
  Application `chirp` `Healthy`/`Unknown`, AppProject `chirp` present.
- **Live image override** confirmed (`chirp:local` + override annotation) → Q1 is a genuine, honestly-handled env limit.
- **Live pod securityContext** confirmed fully `restricted`-compliant: `allowPrivilegeEscalation:false`,
  `capabilities.drop:[ALL]`, `readOnlyRootFilesystem:true`, `runAsNonRoot`, uid/gid `65532`, `seccompProfile:RuntimeDefault`.
- **Live least-privilege** confirmed: `kubectl get appproject chirp` → `sourceRepos`=nswe-demo only, one
  `{chirp, in-cluster}` destination, `clusterResourceWhitelist`=`Namespace` only, enumerated `namespaceResourceWhitelist`,
  **no `*/*/*`**.
- **No secrets** in ns `chirp` (`kubectl get secrets` → none) — nothing committed or created.

---

## Findings — classified (severity + location)

### Blockers
**None.** The manifests are correct, connected, routable, hardened, least-privilege, and digest-pinned. Nothing
must change before this lands.

### Non-blockers

**F1 — [operational / merge-readiness] `ghcr-pull` imagePullSecret is an un-provisioned rollout precondition.**
Location: `deploy/chirp/10-deployment.yaml:52–56` (`imagePullSecrets: [ghcr-pull]`) + the committed GHCR digest pin
(`:59`). The committed manifest pulls a **private** image and depends on a `ghcr-pull` `dockerconfigjson` Secret in
ns `chirp` that is deliberately (correctly) not committed. In-sandbox reachability used a substituted local image via
a live-object patch, so the committed image's *pull path was never exercised end-to-end here*. Post-merge, ArgoCD
`automated` sync (`prune`+`selfHeal`) will apply the committed digest; **absent the secret (or a public package) the
pod will `ImagePullBackOff`.** Action before/at merge: create `ghcr-pull` from a token with `read:packages` (or make
the package public), then confirm the pod pulls `@sha256:054af27…` directly and the Application reaches `Synced`.
Not a manifest defect — a deploy-time prerequisite.

**F2 — [informational / ordering] ArgoCD `sync=Unknown` until #28 merges.**
Location: `deploy/argocd/application.yaml:42` (`targetRevision: main`). Expected pre-merge (`deploy/chirp` not on
`main` yet); `health=Healthy`, wiring proven. Recommend a post-merge check that the Application flips to `Synced`
and adopts the 3 currently-orphaned directly-applied objects. No change required.

**F3 — [polish / nit] Namespace has no `argocd.argoproj.io/sync-wave` and `CreateNamespace` is unset.**
Location: `deploy/chirp/00-namespace.yaml`; `deploy/argocd/application.yaml` `syncOptions`. Deliberate (avoids an
unlabeled imperatively-created ns), and the bounded `retry` (limit 5) converges the namespace-before-namespaced
ordering on first auto-sync. Adding `sync-wave: "-1"` to the Namespace makes ordering deterministic rather than
retry-dependent. The author already recommends this in `deploy/argocd/README.md`. Optional robustness.

**F4 — [polish / nit] `resources-finalizer.argocd.argoproj.io` on the AppProject.**
Location: `deploy/argocd/appproject.yaml:23–24`. The resources-finalizer's cascade-delete semantics apply to
*Applications* (it is correct on `application.yaml`); on an AppProject it is effectively inert (a Project is guarded
by Application references, not by this finalizer). Harmless; removing it from the AppProject would reduce confusion.

**F5 — [polish / nit] AppProject `namespaceResourceWhitelist` includes kinds no committed manifest uses.**
Location: `deploy/argocd/appproject.yaml` (`ServiceAccount`, `ConfigMap`). These are allow-list headroom, not synced
objects; mild over-grant vs strict least-privilege. Defensible as minimal workload-identity/config headroom; could be
tightened to exactly `{Namespace, Deployment, Service, Ingress}` until a dedicated SA/ConfigMap actually lands (ties
to the "no dedicated `serviceAccountName`" observation — the pod runs under the `default` SA with token mount disabled,
which is fine for a workload that makes no API calls).

**F6 — [informational] TLS deliberately omitted (k3d HTTP demo).**
Location: `deploy/chirp/30-ingress.yaml`. Correct and documented for the k3d demo (plain HTTP via serverlb). A
production/native deploy must terminate TLS at Traefik — this belongs to the native-path hardening already tracked by
**#23** (HSO-1), out of scope for #13. No action here.

**Mapping to existing board issues (no duplicates filed):** the deeper supply-chain hardening the PR itself flags —
cosign/Sigstore image signing + admission-time verification, and Argo CD sync-impersonation with
`destinationServiceAccounts` — belongs to **#24** (least-privilege RBAC + supply-chain); the native-cluster TLS/install
path belongs to **#23**. F1–F5 (deploy rollout prereq + manifest polish) are filed as one grouped backlog issue linked
to #28 and #13, following the engagement's established "review non-blockers" convention (cf. #25, #27).

---

## Review depth rationale (per concern in the brief)

1. **Manifest/ArgoCD correctness** — six objects form one connected, routable graph; Application references
   `deploy/chirp`+`project:chirp` and lives outside its synced path; sync policy sane. **Clean.**
2. **Reachability** — wiring routes end-to-end; live `200` + negative-control `404` reproduced by me. **Sound, reproducible.**
3. **#24 RBAC + supply-chain** — AppProject genuine least-privilege (no `*/*/*`, `Secret` excluded), digest pin,
   SSA (`ServerSideApply=true` → survives `--force-conflicts`), no baked secrets. **Strong** (F1 operational, F5 nit).
4. **Probes / limits** — probes on the real `/healthz:8080`, sane requests+limits, startup grace, PSA `restricted`. **Clean.**
5. **Security / trust boundary** — ns isolation, no secrets, token mount off, hardened pod, digest pin. **Strong** (F4/F5/F6 nits).
6. **k3s / GitOps idiom** — Traefik Ingress correct for k3s; ArgoCD Application/AppProject conventions correct. **Strong** (F3 nit).
7. **Testing / evidence depth** — reachability captured + reproducible; Q1/Q2 qualifiers disclosed honestly, not plugged. **Sound.**

No shared contract or public code surface is touched by this diff (it is additive deploy manifests), so no
architecture/contract-stability escalation is warranted.

---

## GitHub-visible record (#26 standing directive)

- (a) PR #28 added to the **NSWE Delivery** board (status `In Progress`, next to #13).
- (b) PR comment on #28 carrying the **APPROVE** verdict + reason (authoritative visible record; `gh pr review
  --approve` blocked for same-account author).
- (c) Findings posted: inline on the diff where they anchor to a line (F1, F3, F4), and in the PR comment otherwise.
- (d) Non-blockers F1–F5 filed as one grouped backlog issue, linked to #28 and #13; #24/#23 referenced for items
  that belong to them (no duplicate issues).

## Scope / side-effect attestation

Read-only throughout: PR diff via `gh`, read-only `kubectl get` + `curl` GET against the live cluster, read of the
code DAG's evidence. **No tree edit, no push to `work/deploy-argocd`, no merge, no force-push, no manifest change, no
cluster mutation, no secret read into this record.** The only writes this review performs are: this `SYNTHESIS.md`,
the PR comment + inline review comments on #28, the board item for #28, and one grouped backlog issue. Landing (merge)
remains the human's / fold's decision — a review never lands its own subject.
