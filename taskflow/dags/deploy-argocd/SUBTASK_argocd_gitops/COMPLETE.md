# COMPLETE — SUBTASK_argocd_gitops

**Task**: Author the Argo CD `Application` + least-privilege `AppProject` (GitOps) under `deploy/argocd/`.
**Status**: COMPLETED (Atomic). **Date**: 2026-10-08.

## What was produced

Three files in the repo checkout `/home/user/nswe-demo/deploy/argocd/` (I own this directory
exclusively; `deploy/chirp/` is the disjoint sibling `SUBTASK_app_manifests`'s and was NOT touched
or read):

| File | Kind | Summary |
|------|------|---------|
| `deploy/argocd/application.yaml` | `argoproj.io/v1alpha1` `Application` (`chirp`, ns `argocd`) | Tracks `repoURL=https://github.com/Nousix-LLC/nswe-demo.git`, `path=deploy/chirp`, `targetRevision=main`; `destination` `{server: https://kubernetes.default.svc, namespace: chirp}`; `spec.project=chirp`; automated prune+selfHeal, `allowEmpty:false`, SSA, foreground prune, bounded retry; cascade finalizer. |
| `deploy/argocd/appproject.yaml` | `argoproj.io/v1alpha1` `AppProject` (`chirp`, ns `argocd`) | `sourceRepos`=nswe-demo only; `destinations`=chirp ns on in-cluster server only; explicit `clusterResourceWhitelist` (Namespace) + `namespaceResourceWhitelist` (Service, ServiceAccount, ConfigMap, Deployment, Ingress); `orphanedResources.warn`. No `*/*/*`. |
| `deploy/argocd/README.md` | docs | Decisions, divergences, coordination notes, and tracked follow-ups. |

## How it composes with the contract (identities satisfied)

- **`argocd-application-wired`** ✔ — `source.path==deploy/chirp`, `repoURL==nswe-demo`,
  `destination.namespace==chirp`, `spec.project==chirp` (not `default`). (Asserted programmatically.)
- **`appproject-least-privilege`** ✔ — destinations scoped to `{chirp, in-cluster server}`;
  explicit, non-wildcard resource whitelists; **no cluster-admin-equivalent `*/*/*`**; narrowing is
  committed/GitOps-managed. `Secret` deliberately excluded (defense-in-depth; no secrets in Git).
  (Asserted programmatically: no wildcard group/kind; every destination ns == `chirp`.)

Frozen contract values from `../contracts/deploy_contract.yaml` used verbatim (not paraphrased):
app/project name `chirp`, source path `deploy/chirp`, destination ns `chirp`. API versions and the
in-cluster server from `../SUBTASK_discovery/outputs/ground_truth.md` (`argoproj.io/v1alpha1`).

## Key decisions (full rationale in README.md)

1. Least-privilege AppProject is the Application's authorization boundary (does not rely on the stock
   controller cluster-admin posture); explicit allow-lists, not `*/*/*` (#24 SEC-2/SEC-4).
2. `Secret` excluded from the whitelist — GHCR pull secret (ground_truth §6, private package) is
   applied out-of-band, no secrets committed (#24).
3. Automated prune + selfHeal + `allowEmpty:false` (+ retry) — the GitOps idiom, chosen deliberately.
4. No `CreateNamespace`; rely on the committed `Namespace` manifest (contract
   `namespace-isolation-no-secrets`). Recommended the sibling annotate it `sync-wave: "-1"`.
5. `targetRevision: main` (steady-state GitOps truth), not the ephemeral feature branch.

## SHA-pinning (#24 SEC-3)

The Application references only in-repo plain manifests — no external Helm charts/remote manifests —
so there is nothing external to SHA-pin at the GitOps layer (satisfied vacuously). The image digest
pin lives in `deploy/chirp` (sibling). A cosign/admission-verification follow-up is **noted** (not
implemented) in README.md.

## Verification performed (no cluster mutation; no git/gh/kubectl)

- Both manifests parse as well-formed YAML (`yaml.safe_load`).
- Programmatic assertions confirm the two contract identities' fields and the no-wildcard /
  dest-scoped-to-chirp / Secret-excluded least-privilege properties.

## Handoffs / coordination for the synthesis gate (`SUBTASK_synthesis`)

- Apply `deploy/argocd/` via `kubectl apply` (gate owns apply/reachability/PR — I did none).
- **Branch base caveat (ground_truth §1):** create `work/deploy-argocd` from `ada3aa9` (real
  `origin/main`), not the stale local `main`. These additive files survive that branch creation.
- Provision the GHCR imagePullSecret out-of-band (or make the package public) so `image-pull-works`
  holds; it is intentionally not a committed Secret.
- Follow-ups flagged in README: cosign/admission verification; apply-layer sync impersonation
  (`destinationServiceAccounts` + `argocd-cm` feature flag, tied to install path #10); optional
  bootstrap Application to continuously reconcile `deploy/argocd` itself.

## Outputs
- `/home/user/nswe-demo/deploy/argocd/application.yaml`
- `/home/user/nswe-demo/deploy/argocd/appproject.yaml`
- `/home/user/nswe-demo/deploy/argocd/README.md`
