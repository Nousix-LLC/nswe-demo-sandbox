# _BRIEF.md — deploy-ghcr-auth (swe-coder DAG)

You are a `swe-coder` DAG for `Nousix-LLC/nswe-demo`. Evaluate your own scope (Atomic vs NeedsDecompose),
select and load your own methodology, and produce the declared output with a root `SYNTHESIS.md` verdict.
This is a **devops remediation work-item**, forked by the project overseer (`overseer/I51`) to resolve review
finding **F1 of issue #29** on the just-merged `#13` (deploy-argocd). It is **not** a feature.

## Objective

After the `#13` merge (`main @ 22d2df6`), the ArgoCD `chirp` Application now syncs the **committed** manifests
and applies the **digest-pinned private image**
`ghcr.io/nousix-llc/chirp-server@sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3`.
The new ReplicaSet is in **ImagePullBackOff** (`401 Unauthorized` — the GHCR package is **private** and there is
**no pull credential** in namespace `chirp`). The deployment currently answers only via a **stale `chirp:local`
pod** from the pre-merge in-sandbox override, which the committed GitOps state no longer describes and which
ArgoCD selfHeal will eventually replace. **Make the committed GitOps desired state actually run and stay
reachable**: the pod must pull the committed digest and run `1/1 Ready`, the Application must reach
**Healthy + Synced**, and `GET /healthz` must return **200** from a pod running the committed digest (not from the
stale override pod).

## Acceptance criteria (testable, verify live on the running cluster)

1. The `chirp-server` pod backing the Service runs the **committed digest** `@sha256:054af27…` and is `1/1 Ready`
   (no ImagePullBackOff / ErrImagePull), with the stale `chirp:local` ReplicaSet scaled to 0 / pruned.
2. The ArgoCD Application `chirp` (ns `argocd`) is **Synced** to the committed revision **and Health = Healthy**.
3. `GET /healthz` via the k3s Traefik ingress (`Host: chirp.localhost` → `http://localhost:8081/healthz`) returns
   **200**, served by the pod running the committed digest.
4. The fix **survives ArgoCD selfHeal/prune**: after ArgoCD re-syncs (or a hard refresh), the pod still pulls the
   digest and stays Ready — i.e. the resolution is not an out-of-band patch that selfHeal reverts.
5. Least-privilege and supply-chain posture from `#24`/`#13` is preserved: the image stays **digest-pinned**, the
   AppProject stays scoped (see inputs), and no broad RBAC or `*/*/*` whitelist is introduced. If the resolution
   adds any Secret/manifest, it is scoped to ns `chirp` and the minimum needed to pull.

## Scope / non-goals

- In scope: namespace `chirp` on the live k3d-hosted k3s cluster (context `k3d-nswe`), its ArgoCD `chirp`
  Application/AppProject in ns `argocd`, the `deploy/chirp` manifests in the repo, and the GHCR package
  `nousix-llc/chirp-server` visibility/credentials — only as far as needed to make the committed digest pullable
  and the app reachable.
- Non-goals: do **not** change the application code, the image contents, or the digest; do **not** re-architect the
  deploy; do **not** take on `#23` (native k3s path), `#24` (deeper RBAC/supply-chain hardening beyond preserving
  what exists), or `#29` F3–F5 (manifest polish) — those remain separate backlog items. Do not force-push `main`,
  rewrite merged history, or add attribution trailers to any commit or PR body (the engagement forbids them).

## Inputs / evidence (observed by the overseer at 2026-10-08T18:34Z, read-only)

- `main @ 22d2df6`; CI green; `#13` merged (PR #28 squash `22d2df6`), `#13` and `#26` closed.
- Pod `chirp-server-bbff68f5b-s5tns`: `0/1 ImagePullBackOff`, pulling `@sha256:054af27…`, error
  `failed to authorize: ... 401 Unauthorized` on `ghcr.io/token?scope=repository:nousix-llc/chirp-server:pull`,
  and event `FailedToRetrieveImagePullSecret ... ghcr-pull`. Anonymous GHCR manifest fetch of the digest → **401**
  (package is private).
- Pod `chirp-server-f6476ccff-bcksd`: `1/1 Running` (age ~57m), the **only** endpoint behind Service
  `chirp-server` (ClusterIP :80 → :8080); this is the stale `chirp:local` override from the DAG's in-sandbox demo.
- Secret `ghcr-pull` is **NotFound** in ns `chirp`; the Deployment template references `imagePullSecrets: [ghcr-pull]`.
- ArgoCD `chirp`: `syncPolicy.automated{prune:true, selfHeal:true}`, `ServerSideApply=true`; source
  `repoURL=https://github.com/Nousix-LLC/nswe-demo.git path=deploy/chirp targetRevision=main`.
- AppProject `chirp`: `destinations=[{ns:chirp, in-cluster}]`, `sourceRepos=[the repo]`,
  `clusterResourceWhitelist=[Namespace]`,
  `namespaceResourceWhitelist=[Service, ServiceAccount, ConfigMap, apps/Deployment, networking/Ingress]`.
  **Secret is NOT in the whitelist** — so a Secret created directly in ns `chirp` is outside ArgoCD's managed set
  and is not pruned by selfHeal (useful if the resolution is a cluster-side pull credential rather than a
  package-visibility change). Verify this yourself before relying on it.
- `deploy/chirp/` = `00-namespace.yaml`, `10-deployment.yaml`, `20-service.yaml`, `30-ingress.yaml`, `README.md`.
- GitHub auth available via `gh` (account `mattsmcknight`, token in env). The k8s context is `k3d-nswe` (admin).
- Prior verdicts for context: `taskflow/dags/deploy-argocd/SYNTHESIS.md` (machine PASS, Q1 image-pull qualifier),
  `taskflow/dags/review-deploy-argocd/SYNTHESIS.md` (APPROVE; F1 is this item).

## What to evaluate / concerns to cover (named; select & load your own methodology)

- **Correctness of the rollout**: the committed digest actually pulls and runs; the stale override pod is gone; the
  Service routes to the digest-running pod; reachability is real and stable, not transient.
- **GitOps convergence**: ArgoCD reaches Synced + Healthy and stays there through selfHeal/prune; the resolution is
  convergent, not a manual patch the controller fights.
- **Supply-chain & least-privilege security**: digest-pinning preserved; any credential is least-privilege
  (`read:packages`-only scope if a token-backed pull secret) and scoped to ns `chirp`; no secret material is
  committed to git in plaintext; package-visibility changes (if chosen) are a deliberate, recorded trade-off.
- **Durability/operability**: the fix is reproducible and documented (how the credential/visibility is
  established), so the deploy is not dependent on undocumented cluster state.

Decide the resolution yourself (e.g. provisioning a least-privilege `ghcr-pull` dockerconfigjson pull secret in ns
`chirp`, or making the `chirp-server` GHCR package public, or an equivalent) and justify the trade-off in
`SYNTHESIS.md`. Do not treat either candidate as prescribed.

## Declared output

- Whatever repo change the resolution needs (e.g. a committed pull-secret manifest/overlay, a README/runbook
  update documenting how GHCR pull auth is established, or a manifest tweak) delivered as commits on
  `work/deploy-ghcr-auth` and a **PR into `main`** whose description says `Closes #29` **as plain text** (not inside
  code formatting) — OR, if the resolution is purely a cluster/GitHub-side action with no durable repo change, a
  documented runbook note in the PR/SYNTHESIS explaining why no code change was needed and how to reproduce the
  auth. Either way the deploy must end verified-reachable on the committed digest.
- A root **`SYNTHESIS.md`** at this workspace root with a PASS/FAIL verdict, the live verification evidence
  (pod image + Ready, Application Synced+Healthy, `/healthz` 200 from the digest pod, selfHeal-survival check),
  the resolution chosen and its security/trade-off rationale, and the acceptance-criteria results.
- Do not merge your own PR and do not push to `main`; the overseer gates and lands.

## Constraints

- Repo scope: `Nousix-LLC/nswe-demo` + its k3d-hosted k3s cluster/namespaces + its ArgoCD only. Never force-push
  `main`, never rewrite merged history, add no attribution trailers. Keep the image digest-pinned.
