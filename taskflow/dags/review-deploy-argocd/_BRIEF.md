# _BRIEF.md — review-deploy-argocd (NSWE #13 review DAG, persona swe-coder)

You are a **code-review DAG** (`swe-coder`) for the `Nousix-LLC/nswe-demo` engagement. Review **PR #28**
(`work/deploy-argocd` → `main`, head `63a299a0`, `Closes #13`) — the Kubernetes manifests + ArgoCD Application
that deploy `chirp-server` onto the live k3d-hosted k3s cluster via GitOps. You **read and report; you do not
fix and you do not land.** Evaluate your own scope (Atomic vs decompose), select and load your own methodology
(the code-review methodology is your spine; do not carry any prior DAG's selection forward), and fold to a root
`SYNTHESIS.md` carrying an **APPROVE** or **REQUEST-CHANGES** verdict with findings.

## Objective
Judge whether PR #28 is fit to land against #13's acceptance criteria and the concerns below, and make the
review **visible on GitHub** per the standing directive (#26).

## The change under review
- **PR**: #28, `work/deploy-argocd` → `main`, head `63a299a0`, `Closes #13`. CI green (run 37818968143, 6/6
  SUCCESS), MERGEABLE/CLEAN at fork time. No attribution trailers (the engagement forbids them — #27/HYG-1).
- **Issue #13** (acceptance): `deploy/` k8s manifests (Namespace/Deployment/Service/Ingress) + an ArgoCD
  Application (GitOps) tracking this repo's `deploy/` path, syncing `chirp-server`
  (`ghcr.io/nousix-llc/chirp-server`, digest-pinned) onto the live k3d-hosted k3s cluster, with **demonstrated
  reachability**, resource limits + liveness/readiness probes; PR into `main`; root `SYNTHESIS.md`.
- **Machine verdict (do not re-run)**: the code DAG's root `SYNTHESIS.md` at
  `/home/user/nousix-runtime/nswe-demo/taskflow/dags/deploy-argocd/SYNTHESIS.md` — gate=PASS, round 1, 8/8
  parent-contract identities PASS (6 clean + 2 evidenced env/ordering qualifiers: **Q1** pinned private-GHCR
  digest unpullable in-sandbox → reachability proven with a node-imported functionally-identical build, pin
  intact; **Q2** ArgoCD `Sync=Unknown` only because `deploy/chirp` is not on `main` until #28 merges — wiring +
  `Healthy` proven live). App reachable: HTTP 200 captured through Traefik ingress; negative-control 404 proves
  the host rule routes.

## Inputs (read first)
- PR #28 diff of `work/deploy-argocd` against its merge base (read-only; `git`/`gh`).
- The code DAG's `SYNTHESIS.md` and its subtask evidence (static_gate report, reachability_evidence) under
  `/home/user/nousix-runtime/nswe-demo/taskflow/dags/deploy-argocd/`.
- Issue #13 and the follow-up #24 (ArgoCD RBAC least-privilege + supply-chain) it folds in; #23 (native/systemd
  durability) is explicitly out of scope for #13 — note, do not block on it.

## What to evaluate — distinct concerns (decide depth per what the diff touches; do not reduce to idiom)
1. **Manifest / ArgoCD Application correctness** — the six objects form one connected, routable graph; the
   Application references `deploy/chirp` + the AppProject and lives outside its own synced path (no self-reconcile);
   sync/prune/self-heal options are sane.
2. **Reachability** — the ingress/host-rule/Service/targetPort wiring actually routes to the server; the live
   HTTP 200 evidence is sound and reproducible (not a fabricated green); negative control is meaningful.
3. **#24 RBAC least-privilege + supply-chain** — AppProject scoped off `*/*/*` to the enumerated
   namespaces/resources with `Secret` excluded; image digest-pinned (`@sha256:…`); `--force-conflicts` / server-side
   apply survival; no baked secrets; `imagePullSecrets` handled without leaking credentials.
4. **Probes / resource limits** — liveness/readiness/startup probes on the real health endpoint and port;
   requests+limits present and reasonable; PodSecurity (restricted) posture.
5. **Security / trust boundary** — namespace isolation, no secrets in manifests, least-privilege ServiceAccount,
   supply-chain trust (digest pin, pull secret handling), ingress exposure surface.
6. **k3s / GitOps idiom** — Traefik ingress idiom on k3s, ArgoCD Application/AppProject conventions, digest-pin
   and sync-wave/ordering conventions.
7. **Testing / evidence depth** — how reachability and health are evidenced; whether the proof survives the
   Q1/Q2 qualifiers honestly; whether a reviewer can reproduce it.

Add architecture/contract-stability review if the diff touches a shared contract or public surface.

## Declared output (ALL required)
- A root **`SYNTHESIS.md`** at this workspace root with: the verdict (**APPROVE** | **REQUEST-CHANGES**), the
  findings classified **blockers** vs **non-blockers** each with **severity + location**, and the acceptance-criteria
  pass/fail. Read the body, not only the verdict line — an approve that lists a blocker is not an approval.
- **Review visible on GitHub (#26 standing directive — MANDATORY):**
  (a) PR #28 **added to the NSWE Delivery board** next to #13;
  (b) a **PR comment on #28 carrying the verdict + reason** (because `gh pr review --approve` is blocked when the
      PR author == the authenticated account, the comment is the authoritative visible record; the `SYNTHESIS.md`
      body remains the authoritative verdict);
  (c) **findings posted** with severity + location — **inline on the diff where a finding anchors to a line**,
      otherwise in the PR comment.
- **Non-blocking findings filed as backlog issues** on the board, linked to PR #28 and #13 (group related
  findings; do not duplicate issues the board already holds — #23/#24/#25/#26/#27 exist).

## Constraints
- Repo scope: `Nousix-LLC/nswe-demo` only (+ its k3d k3s cluster / ArgoCD for read-only verification). **Review
  only — do NOT modify the tree, do NOT push to `work/deploy-argocd`, do NOT merge, do NOT force-push, do NOT edit
  manifests.** If you believe a change is needed, that is a **blocker finding** for a remediation DAG, not an edit.
- Add no attribution trailers to anything you post (#27/HYG-1).
- You select and load your own methodology bundles for the concerns above through the methodology loader.
