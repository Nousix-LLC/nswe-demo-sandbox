# SYNTHESIS.md — deploy-ghcr-auth (F1 of #29)

**Verdict: FAIL — BLOCKED on an external `read:packages` credential.**
The resolution is fully determined and the durable documentation is delivered (PR #30), but the
live fix cannot be completed in this environment: no credential present can pull the private GHCR
digest or change the package's visibility. The deploy is **not** verified-reachable on the committed
digest. Disposition: **FAILED** — reported cleanly (not an open-ended wait) so the overseer can supply
a `read:packages` credential (or flip the package public) and re-fork a fresh attempt; the one-step fix
and verification runbook are in *Unblock* below. (Terminal record: `FAILURE.md`.)

- Task: `swe-coder` DAG `deploy-ghcr-auth`, forked by `overseer/I51` for `Nousix-LLC/nswe-demo`.
- Repo: `origin/main @ 22d2df6`; checkout `/home/user/nswe-demo`.
- Cluster: context `k3d-nswe` (k3s v1.35.5, nodes Ready). Verified live at ~2026-10-08 (dispatch).
- Evaluation: **Atomic** (one remediation responsibility — establish GHCR pull auth for the committed
  digest and verify convergence; the four named concerns are lenses on one indivisible change).

---

## Root cause (confirmed live)

The committed GitOps desired state is correct and already designed for this: `10-deployment.yaml`
pins the digest `@sha256:054af27…` and references `imagePullSecrets: [ghcr-pull]`, with the package
being **private**. F1 is the **operational gap**: the out-of-band `ghcr-pull` Secret (the "synthesis
gate's deploy step" from #13, documented in `deploy/chirp/README.md`) was **never created** in the
running cluster, so the digest pod cannot authenticate to GHCR. A stale `chirp:local` pod from the
pre-merge in-sandbox override is masking the outage as the sole Service endpoint.

The committed state's **documentation** was essentially complete already; the missing piece is purely
the cluster-side credential — which requires a GitHub token scope this environment does not have.

## Why it is blocked (verified, not assumed)

The only GitHub identity available is `mattsmcknight` via `gh` (token also stored in `~/.docker/config.json`
for `ghcr.io`). Its OAuth scopes are `gist, project, read:org, repo, workflow` — **no `read:packages`,
no write/admin-packages**. Evidence:

- `docker pull ghcr.io/nousix-llc/chirp-server@sha256:054af27…` → **403 Forbidden**.
- GHCR token exchange with the stored cred → manifest fetch **404** (recognized but not authorized to read).
- Anonymous GHCR manifest fetch → **403** (package private).
- `GET /orgs/nousix-llc/packages/container/chirp-server` → **403 "need at least read:packages scope"**
  (so visibility cannot be changed via API with this token either).
- `mattsmcknight` **is an org admin** of `nousix-llc` by identity — so the *authority* exists, but the
  *token* lacks package scope, and non-interactive scope escalation (`gh auth refresh -s read:packages`,
  a device-flow) is not viable in a headless dispatch.

Neither candidate resolution (create the pull Secret / make the package public) is therefore executable
in this sandbox.

## Live evidence observed

| Item | Observation |
|---|---|
| Digest ReplicaSet `chirp-server-bbff68f5b` | pod `…-s5tns` **0/1 ImagePullBackOff**, pulling `@sha256:054af27…` |
| Pod event | `FailedToRetrieveImagePullSecret (ghcr-pull)` → anonymous fallback → `401 Unauthorized` on `ghcr.io/token?...:pull` |
| Stale ReplicaSet `chirp-server-f6476ccff` | pod `…-bcksd` **1/1 Running**, image `docker.io/library/chirp:local`; the **only** Service endpoint (`10.42.1.9:8080`) |
| `Secret ghcr-pull` (ns `chirp`) | **NotFound**; namespace has zero secrets |
| Deployment | image = committed digest; `imagePullSecrets=[ghcr-pull]`; `imagePullPolicy=IfNotPresent`; strategy `maxSurge=1,maxUnavailable=0` (explains the surviving stale pod) |
| ArgoCD `Application chirp` | **Synced** to `22d2df6`, **Health = Degraded** (Deployment cannot go Available) |
| AppProject `chirp` | `namespaceResourceWhitelist` = `{Service, ServiceAccount, ConfigMap, apps/Deployment, networking/Ingress}` — **`Secret` not whitelisted** (so an out-of-band `ghcr-pull` Secret would survive selfHeal/prune) |
| `GET /healthz` via ingress | **200**, but served by the **stale `chirp:local` pod**, not the committed digest |

## Acceptance-criteria results

| # | Criterion | Result |
|---|---|---|
| 1 | Pod runs committed digest `1/1 Ready`, stale RS scaled to 0 | ❌ digest pod ImagePullBackOff; stale `chirp:local` pod still the sole endpoint |
| 2 | Application `Synced` **and** `Healthy` | ⚠️ Synced to `22d2df6` but **Degraded** |
| 3 | `/healthz` 200 from the **digest** pod | ❌ 200 comes from the stale pod, not the digest pod |
| 4 | Survives selfHeal/prune | ⏳ not reachable to test (blocked at #1). Mechanism documented + confirmed: an out-of-band `ghcr-pull` Secret survives because `Secret` is not in the AppProject whitelist |
| 5 | Least-privilege / supply-chain posture preserved | ✅ no posture regressions introduced — digest still pinned, AppProject unchanged, no broad RBAC/`*/*/*`, no secret committed to git; PR #30 strengthens least-privilege guidance |

## Resolution (chosen) + trade-off

**Chosen: out-of-band least-privilege `ghcr-pull` dockerconfigjson Secret in ns `chirp`**, created from
a `read:packages`-ONLY credential for `nousix-llc/chirp-server`. Rationale:
- Preserves digest-pinning and keeps the AppProject scoped (the `Secret` is unmanaged by ArgoCD because
  its kind is not whitelisted → selfHeal/prune cannot revert it, satisfying AC4 by construction).
- No secret material in git; blast radius bounded to "read this one package."
- Completes the committed desired state's existing intent (`imagePullSecrets: [ghcr-pull]`) without
  modifying any manifest or the digest.

**Rejected: make the GHCR package public.** Viable and simplest, but a supply-chain confidentiality
trade-off (image becomes world-readable); integrity (digest pin) is unchanged. Recorded as the
documented alternative, not chosen, to preserve least-privilege. (A sealed-secret / ESO GitOps-managed
equivalent is the durable long-term path but is deferred — installing a controller is #24 scope.)

## Unblock (one step, then re-verify)

Provide a least-privilege credential and create the Secret on the live cluster:

```sh
kubectl -n chirp create secret docker-registry ghcr-pull \
  --docker-server=ghcr.io \
  --docker-username='<bot-or-user>' \
  --docker-password='<token with read:packages ONLY for nousix-llc/chirp-server>'
```

ArgoCD selfHeal then rolls the digest pod to `1/1 Ready` and the stale `chirp:local` RS to 0; verify
AC1–4 with the runbook added to `deploy/chirp/README.md` in PR #30. Alternatively an org admin makes the
package public (recorded trade-off), after which the digest pulls anonymously.

## Durable artifact delivered

- **PR #30** → `main` (branch `work/deploy-ghcr-auth`, commit `18ab880`): docs-only strengthening of the
  `deploy/chirp/README.md` pull-auth runbook — least-privilege requirement, the selfHeal-survival
  rationale, a live verification runbook, and the public-package trade-off. Manifests/digest unchanged.
  The PR **does not** carry `Closes #29` (F1 is not resolved live); #29 stays open pending the credential.
- Not merged / `main` not pushed — the overseer gates and lands.

## Notes / constraints honored

- No change to app code, image contents, or digest; no deploy re-architecture; no `main` force-push or
  history rewrite; no attribution trailers on the commit or PR. #23/#24/#29-F3–F5 untouched.
- A GitHub token value was transiently echoed by a shell typo during investigation; it was **not** written
  to any file, manifest, runbook, or this record.
