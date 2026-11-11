## ⛔ Blocked on you (@mattsmcknight) — F1 needs a `read:packages` credential to finish live

**Status:** the engagement is **build-complete** (all of #4–#13 merged on `main @ 22d2df6`, CI green) but the
deploy is **not yet reachable on the committed digest**, and finishing it is **blocked on input only you can
provide**. The automated recovery DAG (`deploy-ghcr-auth`, attempt 1 of 2) investigated this to the end and
confirmed the blocker is an **environment credential gap**, not a defect — so I am **not** burning the second
automatic attempt on a blind retry (it would hit the identical wall). I need one of the two choices below.

### What's wrong (confirmed live by the DAG)
The committed GitOps state is correct: `deploy/chirp/10-deployment.yaml` pins the **private** GHCR image by
digest `@sha256:054af27…` and references `imagePullSecrets: [ghcr-pull]`. But the out-of-band `ghcr-pull` Secret
was **never created** in namespace `chirp`, and **no GitHub token in this environment has `read:packages`**
(the only identity present, `mattsmcknight`'s `gh`/docker token, is scoped `repo, read:org, workflow, …` — a
direct `docker pull` of the digest returns **403**, and the packages API returns `403 "need at least
read:packages scope"`; non-interactive scope escalation isn't viable headless). Result: the digest pod is in
**ImagePullBackOff**; the app answers `/healthz` 200 **only** via a stale `chirp:local` pod that the committed
state no longer describes; ArgoCD `Application chirp` is **Synced@22d2df6 but Health=Degraded**.

### What I need from you (either one unblocks it)
1. **Preferred (least-privilege):** provide a **`read:packages`-ONLY** token for `nousix-llc/chirp-server` (a
   dedicated bot/deploy identity is ideal). I'll create the `ghcr-pull` Secret and ArgoCD selfHeal rolls the
   digest pod to `1/1 Ready` (the Secret survives selfHeal/prune because `Secret` is intentionally **not** in
   the AppProject whitelist). One step:
   ```sh
   kubectl -n chirp create secret docker-registry ghcr-pull \
     --docker-server=ghcr.io \
     --docker-username='<bot-or-user>' \
     --docker-password='<token with read:packages ONLY for nousix-llc/chirp-server>'
   ```
2. **Alternative (recorded supply-chain trade-off):** make the `chirp-server` GHCR package **public** — simplest,
   but the image becomes world-readable (integrity/digest-pin is unchanged). Say the word and I'll proceed on
   this basis instead.

### What's already in flight for you
- **PR #30** (`work/deploy-ghcr-auth`, docs-only) strengthens the `deploy/chirp/README.md` pull-auth runbook
  (least-privilege requirement, selfHeal-survival rationale, a live verification runbook, the public-package
  trade-off). It is **MERGEABLE** and does **not** close this issue. It's now in **review**; I'll land it on
  its own merit (it's a strictly-better runbook independent of the live fix) and keep #29 open for the live fix.
- Full live evidence, the AC1–4 verification runbook, and every ruled-out credential path are in
  `taskflow/dags/deploy-ghcr-auth/SYNTHESIS.md` (and `FAILURE.md`).

**Until you act, the project is held open as `blocked-on-user`.** As soon as you supply a `read:packages` token
(or flip the package public), I'll fork a fresh devops DAG (**attempt 2/2**) to run the one-step fix and verify
AC1–4 reachability live, then drive to Done. No action is needed from you anywhere else — a reply here (or a
comment on the board) is enough; I pick it up on my next board check.
