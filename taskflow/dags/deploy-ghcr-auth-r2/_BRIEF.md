# _BRIEF.md — deploy-ghcr-auth-r2 (devops DAG, persona swe-coder)

## Objective
Verify and, where reachable, **complete** the live reachability of Chirp running on its **committed image**
for `Nousix-LLC/nswe-demo`, and reconcile the running cluster with the committed GitOps desired state. This is
the **F1 deploy attempt #2 of 2** (the first attempt folded blocked on a missing registry credential; the
situation has since changed — see "What changed"). The board item is **issue #32**; hold the result to its
acceptance criteria. Produce one PR for any repository change the fix needs, and a root `SYNTHESIS.md` that
records what is deployed, at which commit, how it was verified live, the AC results, and any external input
still required.

## What changed since attempt #1 (re-evaluate on a fresh clock; do not assume the old wall)
- The owner acted directly on `main`: commit **`c805525`** adds a **host-less ingress rule** to
  `deploy/chirp/30-ingress.yaml` so Chirp is reachable by the cluster's external (tailnet) address for any
  Host, alongside the existing `chirp.localhost` host rule. `main` HEAD is now `c805525`. This addresses
  north-south **reachability**; it does **not** by itself resolve the image pull.
- The prior escalation issue was closed; the credential was **never supplied through the prior ask**. The
  owner may have resolved the pull **out of band** (created a `ghcr-pull` Secret, or flipped the GHCR package
  public) without saying so — **test the live world first**, do not assume it is still blocked.
- Because the world changed, this attempt is **released to verify/complete live reachability**, NOT to repeat a
  blind credential retry against the identical wall. Begin by reading the live cluster state fresh.

## Inputs
- Repo `Nousix-LLC/nswe-demo` @ `main` (`c805525`). Working checkout per the repo's `CLAUDE.md`.
- **Host/cluster access is in the repo's `CLAUDE.md`** (root of the checkout): `kubectl`/`helm`/`k3d` run over
  SSH to the build server; k3d cluster `nswe`, context `k3d-nswe`, namespace `chirp`; ArgoCD in namespace
  `argocd`, Application `chirp`; the app is served by the server's k3d load balancer. Read and follow it.
- Committed GitOps state: `deploy/chirp/{00-namespace,10-deployment,20-service,30-ingress}.yaml` + `README.md`.
  `10-deployment.yaml` pins the `chirp-server` image **by digest** (`@sha256:054af27…`) and references
  `imagePullSecrets: [ghcr-pull]`; the GHCR package is private. The ArgoCD `AppProject` whitelist does **not**
  include `Secret`, so an out-of-band `ghcr-pull` Secret survives selfHeal/prune.
- **Prior verdict + ruled-out hypotheses — read these, do NOT re-tread them**:
  `taskflow/dags/deploy-ghcr-auth/SYNTHESIS.md` and `.../FAILURE.md`. They establish: the committed digest pod
  was in `ImagePullBackOff` (no `ghcr-pull` Secret, no `read:packages` on the only available token); a stale
  `chirp:local` pod masked the outage as the sole Service endpoint; ArgoCD was Synced@`22d2df6` but
  Health=Degraded. Ruled out (do not retry blindly): the local `gh`/docker token cannot pull GHCR (403) and
  cannot flip package visibility via API (no `read:packages`); anonymous pull is 403 (private); non-interactive
  `gh auth refresh` is a device flow (not viable headless); a local `docker pull` + `k3d image import` is
  non-durable and fails the operability bar. The pull-auth runbook is in `deploy/chirp/README.md` (landed by
  PR #30).

## Acceptance criteria (issue #32)
1. The `chirp-server` pod runs the **committed digest**, `1/1 Ready`; the stale local-image ReplicaSet is
   scaled to `0`.
2. ArgoCD `Application chirp` is **Synced and Healthy** at the integration-branch head.
3. `GET /healthz` returns `200` served by the **committed-digest** pod (not the stale local-image pod),
   reachable through the ingress.
4. The fix **survives ArgoCD selfHeal/prune**.
5. Supply-chain / least-privilege posture preserved: digest pinning unchanged, no registry secret committed to
   the repo, no broad RBAC, ArgoCD project scope unchanged.

## Concerns to cover (each is its own concern with its own bar)
- **Reachability** — Is the app actually answering through the ingress, at both the owner's host-less route and
  the existing host route? Confirm the owner's `c805525` rule behaves as intended and nothing else blocks
  north-south reachability. Bar: the endpoint answers live over the ingress.
- **Image-pull / supply chain** — Is the committed-digest pod Running? If not, determine whether a pull
  credential is now reachable (the owner may have created the Secret or made the package public out of band);
  if a credential is reachable and the Secret is still missing, create the least-privilege `ghcr-pull` Secret
  so the digest pulls. If **no** credential is reachable, do not burn effort on a blind retry — report cleanly
  what is still needed and exactly where the system expects it. Bar: the digest pod pulls and runs, with no
  secret material committed to git and the digest unchanged.
- **GitOps drift / selfHeal survival** — Reconcile the running cluster with the committed desired state; the
  fix survives selfHeal/prune; the Application is Synced and Healthy at head. Bar: desired == running, durably.
- **Ops** — The stale local-image pod is scaled to 0, the rollout is clean, and no posture regressions are
  introduced. Bar: a clean single-endpoint deployment on the committed image.

## Declared output
- Any repository change the fix needs as a PR on `work/deploy-ghcr-auth-r2` into `main`, linking issue #32 with
  a `Closes #32` line in the PR body (plain text) if and only if the live reachability is actually achieved and
  verified; otherwise leave #32 open and say why.
- A root `SYNTHESIS.md` stating what is deployed at which commit, the AC1–5 results, **how it was verified
  live** (synced, healthy, the endpoint answering, a smoke test — not merely that manifests applied), and any
  external input still required (what it is and where the system expects to find it). If reachability cannot be
  completed because no credential is reachable, report `failed` cleanly (not an open-ended wait) with that
  external input named precisely.

## Constraints
- Scope: `Nousix-LLC/nswe-demo` plus this project's own k3s cluster/namespaces (`chirp*`) and its own ArgoCD
  Application `chirp`. Do **not** touch other namespaces or other ArgoCD applications on the cluster.
- The overseer reads the live system; **you** change it (apply manifests, create the Secret, reconcile) — but
  through the repo where GitOps owns the desired state, and as reviewed PRs where a repository change is needed.
- Never force-push `main`; never rewrite merged history; **no attribution trailers** on commits or PR bodies.
- Never commit a secret or registry credential to the repo.
- **Whatever posts to GitHub (issues, PRs, comments) carries no host/system details** — no server address, no
  SSH key path, no user name, no host paths, no taskflow internals. Translate host facts to repository
  identities before anything goes on GitHub. Host facts stay in the working environment only.
- Select and load your own methodology for these concerns; decide your own decomposition. This brief describes
  the work; it does not prescribe how to divide or execute it.
