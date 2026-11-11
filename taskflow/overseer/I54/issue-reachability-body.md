## Verify & complete live reachability of Chirp on the committed image

The workspace is build-complete (ferric + chirp, #4–#13 merged, CI green) and the GitOps desired state is in
the repo: `deploy/chirp/10-deployment.yaml` pins the `chirp-server` image **by digest** and references
`imagePullSecrets: [ghcr-pull]`, with the GHCR package private. ArgoCD `Application chirp` tracks the repo.

What remains before the deploy is "delivered" is to confirm the app is actually **running and reachable on the
committed digest**, live — not on a leftover locally-built image. A prior investigation found the committed
digest pod unable to authenticate to the registry (the out-of-band `ghcr-pull` Secret had not been created),
with a stale local-image pod masking the outage; the pull-auth runbook landed in `deploy/chirp/README.md`
(PR #30).

Since then the reachability approach was changed directly on `main`: commit `c805525` adds a **host-less
ingress rule** to `deploy/chirp/30-ingress.yaml` so Chirp is reachable by the cluster's external address for
any Host, alongside the existing `chirp.localhost` host rule. This addresses north-south reachability; it does
**not** by itself resolve the image pull.

### Acceptance criteria
1. The `chirp-server` pod runs the **committed digest**, `1/1 Ready`, and the stale local-image ReplicaSet is
   scaled to `0`.
2. ArgoCD `Application chirp` is **Synced and Healthy** at the integration branch head.
3. `GET /healthz` returns `200` served by the **committed-digest** pod (not the stale local-image pod),
   reachable through the ingress.
4. The fix **survives ArgoCD selfHeal/prune**.

### Scope
- If the digest pod still cannot pull, establish **least-privilege GHCR pull auth** (create the `ghcr-pull`
  Secret in namespace `chirp` from a `read:packages`-only credential for the package) so the committed digest
  pulls; reconcile the GitOps desired state with what is actually running.
- Keep the supply-chain posture: digest pinning unchanged, no registry secret committed to the repo, no broad
  RBAC, ArgoCD project scope unchanged.
- Verify **live** (synced, healthy, endpoint answering, a smoke test), not merely that manifests apply.

### Non-goals
- No change to application code, image contents, or the pinned digest.
- Does not supersede the longer-term GitOps-managed-secret work tracked under the DevOps epic.

Follows through on the F1 deploy reachability item previously tracked under the now-closed #29. Part of
epic #3 (DevOps — CI and CD on k3s).
