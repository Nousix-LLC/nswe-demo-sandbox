# ESCALATION — failure handler for `deploy-ghcr-auth` (F1 of #29)

**Disposition: ESCALATE (not autonomously recoverable). No remediation task scheduled — by design.**

The engine dispatched this callback to handle the `TaskFailed` of DAG `deploy-ghcr-auth` (forked by
`overseer/I51` to resolve review finding **F1 of issue #29** on `Nousix-LLC/nswe-demo`). After reading the
failed node's recorded state (`FAILURE.md`, `_BRIEF.md`, `SYNTHESIS.md`, `_FORK.md`, `SUSPENSION.md`), the
handling verdict is: **this failure cannot be fixed by any task that can be scheduled into this
environment.** It requires one out-of-band human/overseer action. It is escalated, not amended.

The failed node stays TERMINAL and IMMUTABLE (never revived).

---

## Diagnosis (from the failed node's own records — confirmed, not re-derived)

- **What was required:** make the committed GitOps desired state run — the `chirp-server` pod must pull the
  committed **private** GHCR digest `ghcr.io/nousix-llc/chirp-server@sha256:054af27…` and reach `1/1 Ready`,
  ArgoCD `chirp` Application → Synced **and** Healthy, `/healthz` → 200 from the digest pod, surviving
  selfHeal/prune (AC1–4), with least-privilege posture preserved (AC5).
- **Root cause:** purely an **operational credential gap**. The committed manifests are correct and already
  reference `imagePullSecrets: [ghcr-pull]`; the `ghcr-pull` Secret was never created in ns `chirp`, so the
  digest pod cannot authenticate to GHCR (`401`/`ImagePullBackOff`). A stale `chirp:local` pod masks the
  outage as the sole Service endpoint.
- **Why it blocked (verified live, not assumed):** the only GitHub identity in the sandbox is `mattsmcknight`
  via `gh`, scoped `gist, project, read:org, repo, workflow` — **no `read:packages`, no admin:packages**.
  - `docker pull …@sha256:054af27…` → **403**; token-exchange manifest fetch → **404**.
  - Anonymous GHCR fetch → **403** (package private).
  - `GET /orgs/nousix-llc/packages/container/chirp-server` → **403 "need at least read:packages scope"**
    (cannot flip visibility via API with this token either).
  - `gh auth refresh -s read:packages` is an interactive device-flow → not viable headless.
  - `mattsmcknight` **is** an org admin of `nousix-llc` by identity, so the *authority* exists — but the
    *sandbox token* lacks package scope.

## Why no remediation task is scheduled (the recoverability test)

A remediation task is only worth scheduling if, when the scheduler later dispatches it, it can actually fix
the problem. Here it cannot:

1. **The critical-path step is not schedulable.** The enabling action is "provision a `read:packages`
   credential for `nousix-llc/chirp-server`" **or** "an org admin makes the package public." Neither can be
   performed by an autonomous task in this sandbox (both need interactive GitHub auth or package-admin
   rights the environment does not hold). A task can *consume* such a credential but cannot *produce* it.
2. **A credential-less retry re-treads documented dead ends.** `FAILURE.md` enumerates every ruled-out path
   precisely so the next attempt does not repeat them. A re-dispatched in-sandbox deploy task hits the same
   `403`/`404`/`401` and re-fails identically — wasted dispatch, no progress.
3. **The only in-sandbox alternative is explicitly out of scope.** A GitOps-managed pull secret
   (sealed-secret / External Secrets Operator) is the durable long-term path but is deferred to **#24**
   (installing a controller); the F1 brief's non-goals forbid taking on #24. So there is no in-scope,
   unblocked, autonomous work to schedule.
4. **The system is already designed to recover via the overseer, not via this DAG.** `_FORK.md` sets
   `disposition: reap-whole-after-land` and has the overseer gate only on the root `SYNTHESIS.md` seam;
   `FAILURE.md` states the node reported `failed` *specifically* "so the overseer can re-fork with a
   packages-scoped credential," carrying the lesson forward into the next DAG's brief. Grafting a child task
   onto this reap-whole DAG would fight that design and (per the kernel's forward-only / no-sideways-reach
   amendment rules) cannot legally depend on `overseer/I51` to supply the credential anyway.

Because the sole blocker is a non-schedulable external action, this is the kernel's "genuinely
unrecoverable → escalate" branch, not the "amend-with-remediation" branch.

## The one action that unblocks it (for the overseer / human)

Provide a least-privilege credential and create the Secret on the live cluster (context `k3d-nswe`):

```sh
kubectl -n chirp create secret docker-registry ghcr-pull \
  --docker-server=ghcr.io \
  --docker-username='<bot-or-user>' \
  --docker-password='<token with read:packages ONLY for nousix-llc/chirp-server>'
```

ArgoCD selfHeal then rolls the committed digest to `1/1 Ready` and scales the stale `chirp:local`
ReplicaSet to 0. (The `ghcr-pull` Secret survives selfHeal/prune because `Secret` is not in the AppProject
`namespaceResourceWhitelist` — verified in the failed node's evidence.) **Alternative** (recorded
supply-chain trade-off, not preferred): an org admin makes the `chirp-server` GHCR package public, after
which the digest pulls anonymously.

## Recommended recovery path

1. **Overseer/human supplies the capability:** inject a `read:packages`-ONLY credential into the deploy
   environment (preferred), or flip the package public.
2. **Re-fork a fresh `deploy-ghcr-auth` DAG** (per `_FORK.md` design — this failed DAG is reaped whole; the
   lesson is already captured here and in the failed node's `FAILURE.md`/`SYNTHESIS.md`). The fresh DAG runs
   the one-step fix above and verifies AC1–4 live using the runbook landed in **PR #30**
   (`deploy/chirp/README.md`).
3. **Land PR #30** (docs-only runbook strengthening; branch `work/deploy-ghcr-auth`, commit `18ab880`). It
   is the durable, already-complete half of the fix. It intentionally does **not** carry `Closes #29`; **#29
   stays open** until the live deploy is verified-reachable on the committed digest.

## Constraints to preserve on recovery

Keep the image digest-pinned; keep the AppProject scoped (no broad RBAC, no `*/*/*` whitelist); any Secret
stays in ns `chirp` and `read:packages`-only; no secret material committed to git; no `main` force-push, no
history rewrite, no attribution trailers. Do not take on #23, #24, or #29 F3–F5.

---

**Handler outcome:** failure diagnosed; disposition = escalate to `overseer/I51` / human for an external
`read:packages` credential (or package-public flip). No new task injected (none could fix the problem). The
failed node remains terminal; recovery proceeds via overseer re-fork once the credential is available.
