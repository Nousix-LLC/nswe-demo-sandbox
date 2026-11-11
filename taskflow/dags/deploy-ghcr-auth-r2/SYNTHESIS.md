# SYNTHESIS.md — deploy-ghcr-auth-r2 (verification gate + fold record)

**Verdict: PASS — Chirp is live-reachable on the committed image digest and reconciled with the committed
GitOps desired state. All issue-#32 acceptance criteria (AC1–5) are satisfied, each confirmed by an
executed check against the fresh live world (verification clock below), not asserted from upstream prose.**

This is the subtree's single required deliverable, authored at the fold location (the subtree root) — the
overseer's observation seam. It is both this gate task's terminal record and the fold record; no separate
duplicate is written.

- Subtree: DAG `deploy-ghcr-auth-r2` (issue #32, F1 deploy **attempt #2 of 2**), `Nousix-LLC/nswe-demo`.
- Stages: diagnose → remediate → **verify/synthesize (this gate)**. The gate owns the AC1–5 verdict and the
  `Closes #32` decision (the change/verify split keeps the verdict out of the remediate stage).
- Gate evaluation: **Atomic** (one synthesis/verification responsibility: enumerate the frozen identities,
  execute each against the live world, render one verdict + this one fold record).
- **Resumed, reconstructed node.** Prior invocations of this gate authored PASS records but never reached
  their terminal fold, so the parent stayed SUSPENDED and the node was re-dispatched. The gate posture forbids
  folding on stale prose: **this invocation re-executed every identity check against the live world as it
  stands now, re-confirms PASS, and reaches the terminal fold.**
- **Live verification clock: 2026-10-22T16:08–16:47Z** (gate-executed this invocation: fresh cluster reads of
  pods/RS/deploy/endpoints/secret/appproject/RBAC, both ingress-route `/healthz` curls with clean JSON-body
  re-capture, an **executed** selfHeal reconcile rehearsal — `replicas 1→2` reverted to `1` in ~2s — and
  repo/supply-chain inspection against `origin/main@276138f`).

---

## What is deployed, at which commit

| Aspect | Value (verified live this invocation) |
|---|---|
| Repo / branch | `Nousix-LLC/nswe-demo`, `main` HEAD **`276138f`** (`276138f…d5a54`, "docs: add the language-cleanup directive (#109)"). No integration branch `work/deploy-ghcr-auth-r2` on the remote (`git ls-remote --heads` → empty) and no PR open — no repo change was needed. |
| Running image | `ghcr.io/nousix-llc/chirp-server@sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3` — the deploy/RS image **equals** the committed pin in `deploy/chirp/10-deployment.yaml@276138f`. |
| Pod | `chirp-server-bbff68f5b-22spd` — Running, **1/1 Ready**, 0 restarts, ~13d. Sole running chirp pod. |
| Pull auth | out-of-band least-privilege Secret `ghcr-pull` (`kubernetes.io/dockerconfigjson`, 1 data key) in ns `chirp`; the private digest pulled cleanly (no `ImagePullBackOff`). Secret material is deliberately NOT reproduced in this record. |
| ArgoCD | Application `chirp` **Synced + Healthy** at `276138f` (`targetRevision: main`, path `deploy/chirp`), `automated{selfHeal:true, prune:true, allowEmpty:false}`, `ServerSideApply=true`, `PrunePropagationPolicy=foreground`. |
| Ingress | both routes answer — the host-less (any-Host) rule and the `chirp.localhost` host rule, class `traefik`. |

**Relationship to attempt #1 (which FAILed, blocked on a `read:packages` credential):** the credential
dead-ends ruled out in attempt #1 were **not** re-tried. The owner resolved the pull out of band — the
`ghcr-pull` Secret exists in-cluster — and the host-less ingress rule is committed (`c805525`). The gate
tested the fresh live world rather than assuming the prior block held; the block is gone.

### Revision note (since the integration was planned at `c805525`)

`main` advanced to **`276138f`** via `76eeba9` (chore: scrub host-specific paths/address from tracked files —
comment-only, ingress rules unchanged), `ab824a5`, `8fa347e`, `276138f` (all docs/design). The committed image
pin is unchanged across the advance; `imagePullSecrets` still references `ghcr-pull` by name only. AC2's
"integration-branch head" resolves to `main@276138f`: no repo change was needed, so the committed desired state
and the integration head are the same revision, to which ArgoCD is Synced + Healthy — no drift to close.

---

## Checks (every `contracts/_MANIFEST.yaml` identity enumerated and EXECUTED; no silent plugs)

| Identity (AC) | Result | Executed check + evidence (this invocation, 2026-10-22) |
|---|---|---|
| **I1** digest running / stale RS at 0 (AC1) | **PASS** | `kubectl -n chirp get pod/rs/deploy -o wide`: digest pod `…-22spd` 1/1 Running, 0 restarts; its RS `chirp-server-bbff68f5b` (image `@sha256:054af27f…`) `DESIRED=1 CURRENT=1 READY=1`; deploy `1/1`. Stale local-image RS `chirp-server-f6476ccff` (`docker.io/library/chirp:local`) at `DESIRED=0 CURRENT=0 READY=0`. Deploy/RS image == committed pin @276138f. |
| **I2** ArgoCD Synced + Healthy at head (AC2) | **PASS** | `kubectl -n argocd get application chirp -o jsonpath`: `Synced Healthy rev=276138fb049… target=main path=deploy/chirp`. Integration head == `main@276138f` (no repo change ⇒ no drift). |
| **I3** `/healthz` 200 from the digest pod, both routes (AC3) | **PASS** | `curl` host-less (any-Host) route → `200` `{"service":"chirp-server","status":"ok","version":"0.1.0"}`; `curl -H 'Host: chirp.localhost'` → identical `200` body; SPA root `/` → `200 text/html` on both routes. The Service has exactly one endpoint (`10.42.1.10:8080` = the digest pod, via I6), so every `200` is necessarily served by the committed-digest pod. |
| **I4** survives selfHeal/prune (AC4) | **PASS** | **Executed reconcile rehearsal:** injected a managed-field drift (`kubectl -n chirp scale deploy chirp-server --replicas=2`); ArgoCD **selfHeal reverted `spec.replicas` to the committed `1` within ~2s**. Across the reconcile the digest pod stayed Running 1/1 (same pod `…-22spd`) and the **out-of-band `ghcr-pull` Secret persisted** (its kind is excluded from the AppProject whitelist, so prune cannot reach it). App returned to Synced + Healthy @276138f; cluster left at desired state (replicas=1, no residual drift). |
| **I5** supply-chain / least-privilege posture (AC5) | **PASS** | Digest pin unchanged (`10-deployment.yaml@276138f` digest == running image). **No secret material committed** — `git grep` of `origin/main -- deploy/` for `dockerconfigjson` / `kind: Secret` / private-key headers / `gh[pos]_` token literals matched only a documentation reference in `deploy/argocd/README.md` (runbook prose), no real credential; `imagePullSecrets` references `ghcr-pull` by name only. **No broad RBAC** — ns `chirp` has zero Roles/RoleBindings and only the `default` ServiceAccount. **AppProject scope unchanged** — `namespaceResourceWhitelist` = Service/ServiceAccount/ConfigMap/apps·Deployment/networking·Ingress (Secret excluded), cluster whitelist = Namespace only, `sourceRepos` = the repo only, `destinations` = ns `chirp` on the in-cluster API only. |
| **I6** single endpoint, no stale masking (AC1) | **PASS** | `kubectl -n chirp get endpoints chirp-server` → only `10.42.1.10:8080` (the digest pod). The attempt-#1 masking (stale `chirp:local` pod as sole endpoint) is gone. |
| **I7** no host facts on GitHub | **PASS (preserved + vacuous)** | This subtree opened no PR, pushed no branch, posted no commit/comment (`git ls-remote --heads origin work/deploy-ghcr-auth-r2` → empty; `gh pr list` → `[]`) — no GitHub surface carries host/system facts. Independently, committed `deploy/` files scan clean of node address / host paths / key paths (the `76eeba9` scrub). This record is a taskflow state file (not GitHub-bound) and references routes/secrets by cluster/repository identity only; it embeds no raw host facts and no credential material. |

**AC1–5 roll-up:** AC1 = I1+I6 ✅ · AC2 = I2 ✅ · AC3 = I3 ✅ · AC4 = I4 ✅ · AC5 = I5 (+I7 hygiene) ✅.

---

## How it was verified live (not "manifests applied")

Verification was executed against the real cluster (context `k3d-nswe`, namespaces `chirp`/`argocd`) and the
real remote repo, not inferred from the upstream diagnosis/remediation prose:

1. **Reachability actually answered** — `/healthz` returned `200` with the chirp-server JSON body through
   **both** ingress routes, and the SPA root returned `200 text/html`. Serving pod correlated to the
   committed-digest pod via the single Service endpoint.
2. **Synced + Healthy confirmed** — ArgoCD reports both at `276138f`, not merely "applied"; the current `main`
   HEAD was re-derived from `origin` (`git fetch` + `git rev-parse origin/main`) rather than trusting the prior
   record's revision.
3. **selfHeal proven by execution** — a deliberate managed drift (`replicas=2`) was injected and ArgoCD reverted
   it to the committed desired state in ~2s, while the unmanaged pull Secret and the digest pod survived the
   reconcile. AC4 is demonstrated, not argued by construction.
4. **Supply-chain posture inspected** — committed manifests, the digest pin, AppProject scope, and in-namespace
   RBAC were read directly and show no regression; the image pin is unchanged across the `main` advance.

The rehearsal left the cluster at desired state (replicas back to 1). No persistent change was introduced by
this gate.

---

## Issue-#32 disposition

**#32 is satisfied AND already CLOSED.** Live reachability on the committed image digest is achieved and
verified. The fix was fully out-of-band (the owner's `ghcr-pull` Secret) plus the already-committed host-less
ingress rule, so **no repository change was required and no PR exists**; there is therefore no PR body to carry
a `Closes #32` line, and none was fabricated (the manifest's ownership gates `Closes #32` on a PR existing — it
does not).

**Issue state confirmed this invocation:** `gh issue view 32` → **CLOSED** (labels `devops`, `type:deploy`,
`priority:high`). The overseer has already closed #32; the live-reconcile evidence above corroborates the close —
the committed-digest pod is `1/1 Ready` as the sole Service endpoint, ArgoCD is Synced + Healthy at `276138f`,
`/healthz` serves `200` from the digest pod on both ingress routes, and the fix survives selfHeal/prune. No
code or manifest merge is pending and **no further overseer action is required**.

## External input still required

**None.** A valid `read:packages` credential — the attempt-#1 blocker — is present in-cluster as Secret
`ghcr-pull` in ns `chirp` and authenticated the pull. No further external input, credential, or merge is needed
to reach or sustain the deployed state.

---

## Coverage assertion (gate PASS)

- Ownership coverage: every `contracts/_MANIFEST.yaml` identity (I1–I7) enumerated and executed against the
  live world this invocation — ✅
- Wiring: the fix is live-wired — the single Service endpoint serves from the committed-digest pod, not a
  detached/stale pod — ✅
- Identities: every identity evaluated live; **none silently plugged** (a failing identity would have been
  reported FAIL with the precise missing input, or scheduled as a remediation fix-task) — ✅
- Posture / review: supply-chain + least-privilege posture preserved; no host facts on any GitHub surface; no
  credential material in this record — ✅

**No remediation fix-task was injected: the gate passed cleanly on live re-verification at `main@276138f`.**
