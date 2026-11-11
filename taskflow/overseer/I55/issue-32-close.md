## Resolved — Chirp is live-reachable on the committed image, verified live

Live reachability on the committed container image is achieved and verified against the running cluster. All acceptance criteria (AC1–AC5) are satisfied:

- **AC1 — committed image is what runs, no stale masking.** The `chirp-server` pod is `1/1 Ready` running `ghcr.io/nousix-llc/chirp-server@sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3` — identical to the digest pinned in `deploy/chirp/10-deployment.yaml` at `c805525`. The Service has exactly one endpoint, that pod; the earlier stale local-image ReplicaSet is scaled to 0 and no longer masks it.
- **AC2 — GitOps reconciled.** The ArgoCD `chirp` Application is **Synced + Healthy at `c805525`** (`main` HEAD), tracking `deploy/chirp`.
- **AC3 — endpoint answers.** `GET /healthz` returns `200` `{"service":"chirp-server","status":"ok","version":"0.1.0"}` on both ingress routes (the host-less rule added in `c805525` and the `chirp.localhost` host rule); the SPA root `/` returns `200 text/html`.
- **AC4 — survives reconciliation.** A deliberate managed-field drift was injected and ArgoCD's self-heal reverted it to the committed desired state; across the reconcile the committed-image pod stayed Running `1/1` and the private-registry pull credential persisted. Self-heal + prune are proven, not merely argued.
- **AC5 — supply-chain / least-privilege posture preserved.** The digest pin is unchanged, no secret material is committed under `deploy/chirp/*` (the pull credential is referenced by name only), the namespace carries no broad RBAC, and the ArgoCD AppProject scope is unchanged (the Secret kind is excluded from its resource whitelist).

**How it was fixed:** out of band. The private-registry pull credential now exists in the `chirp` namespace and authenticates the pull, and the host-less ingress rule committed in `c805525` makes the service reachable at the deployment's address. **No repository change was required, so there is no PR** — hence this issue is closed directly against the live evidence rather than by a `Closes #32` merge.

No further input is needed to reach or sustain the deployed state. Closing as done.
