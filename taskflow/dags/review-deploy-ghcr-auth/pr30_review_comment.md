## Review verdict: ✅ APPROVE

Authoritative review of PR #30 (`docs(chirp): least-privilege GHCR pull-auth runbook`, commit `18ab880`, base `main @ 22d2df6`) by the `review-deploy-ghcr-auth` review DAG. `gh pr review --approve` is blocked here (PR author == authenticated account), so this comment carries the authoritative verdict; full detail is in the review DAG's root `SYNTHESIS.md`.

**Docs-only** change to `deploy/chirp/README.md` (`gh pr diff 30` touches exactly that one file; manifests, `imagePullSecrets: [ghcr-pull]`, and the pinned digest `@sha256:054af27…` are unchanged). **No blockers.**

### Acceptance criteria
- **AC1 — technically accurate vs committed state — ✅.** README digest / `imagePullSecrets: [ghcr-pull]` / ns `chirp` match `10-deployment.yaml`; the quoted AppProject `namespaceResourceWhitelist` `{Service, ServiceAccount, ConfigMap, apps/Deployment, networking/Ingress}` matches `deploy/argocd/appproject.yaml` exactly, and `Secret` is deliberately excluded there — so the out-of-band `ghcr-pull` Secret genuinely survives selfHeal/prune.
- **AC2 — one-step unblock + live verify runbook runnable — ✅.** The `kubectl create secret docker-registry ghcr-pull …` command and the AC1–4 checks (deployment `chirp-server`, Application `chirp`/ns `argocd`, ingress `chirp.localhost` via `localhost:8081`, `/healthz` 200) all resolve against the real manifests and match the devops `SYNTHESIS.md` verbatim.
- **AC3 — least-privilege guidance sound; public-package trade-off honest — ✅.** `read:packages`-ONLY token (bot/deploy identity preferred), explicitly not a broad `repo`/`workflow`/write/admin-packages token; the public-package option is framed as a deliberate supply-chain confidentiality trade-off with option 1 preferred.
- **AC4 — no smuggled changes / no secrets / no trailers — ✅.** Diff is README-only, snippets use placeholders, commit `18ab880` has no attribution trailers, and the PR correctly does **not** carry `Closes #29`.

### Stands on its own? — YES
The runbook is a strictly-better `deploy/chirp/README.md` independent of whether the live F1 fix has happened: the least-privilege guidance and trade-off are credential advice; the selfHeal-survival section documents a property that is **already true** of the committed AppProject; the verify runbook is runnable whenever a deploy occurs and never asserts the fix is applied. **This PR can land now on its own merit** (or be batched with the live fix — either is safe).

### Non-blocking nits (recorded, not filed — the substantive rollout-prereq is already tracked as #29 F1)
- **NB-1 [editorial, out-of-diff]** — the pre-existing "Handoff to the synthesis gate (git state)" section (`deploy/chirp/README.md:119-136`) is now historically stale (references local `main 25e90c0` / checkout `work/deploy-argocd` from `ada3aa9`, obsolete post-#28). It is **not** touched by this PR, so it is not a finding against #30 — optional future cleanup only.
- **NB-2 [nit]** — the selfHeal-survival step patches `sync.revision: HEAD` while the Application tracks `targetRevision: main`; both work, `main` matches the tracked revision exactly.
- **NB-3 [nit]** — "classic PAT or fine-grained PAT": a fine-grained PAT additionally needs the org GHCR package to grant it read access; a one-clause caveat would help.

No new backlog issues filed: #29 F1 already holds the substantive non-blocker this PR documents, and NB-1…NB-3 are below the bar for a tracked issue (reference-don't-duplicate, per #25/#27/#29).

_Posted by the `review-deploy-ghcr-auth` review DAG (NSWE, reviews PR #30 / #29). No attribution trailers (#27/HYG-1)._
