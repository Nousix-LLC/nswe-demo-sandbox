# _BRIEF.md — review-deploy-ghcr-auth (code review of PR #30)

You are a `swe-coder` review DAG for the NSWE engagement on `Nousix-LLC/nswe-demo`. Review **PR #30** and
produce an authoritative verdict. You review and report; you do **not** fix, edit, or land anything.

## Objective
Review **PR #30** — `docs(chirp): least-privilege GHCR pull-auth runbook` (branch `work/deploy-ghcr-auth`, base
`main`, commit `18ab880`) — and decide **APPROVE** or **REQUEST-CHANGES** with findings. It is a **docs-only**
change to `deploy/chirp/README.md` (the GHCR pull-authentication runbook); the manifests, the
`imagePullSecrets: [ghcr-pull]` reference, and the committed digest `@sha256:054af27…` are unchanged. The PR
addresses the **documentation/durability half of F1 of #29** and explicitly does **not** close #29 (the live
fix is blocked on an external `read:packages` credential).

## Acceptance criteria the PR is held to
- The runbook is **technically accurate** against the actual committed state: it must agree with what
  `deploy/chirp/10-deployment.yaml` pins (digest, `imagePullSecrets: [ghcr-pull]`), with ns `chirp`, and with the
  fact that the AppProject `namespaceResourceWhitelist` in `deploy/argocd/appproject.yaml` does **not** include
  `Secret` (which is why an out-of-band `ghcr-pull` Secret survives selfHeal/prune).
- The documented **one-step unblock** (`kubectl -n chirp create secret docker-registry ghcr-pull …`) and the
  **live verification runbook** (pod on the committed digest `1/1 Ready`, Application Synced+Healthy, `/healthz`
  200 through the ingress, selfHeal-survival re-check) are correct and actually runnable.
- The **least-privilege guidance** is sound (a `read:packages`-ONLY token, not a broad `repo`/`workflow` or
  write/admin-packages token) and the **"make the package public" alternative** is framed honestly as a
  supply-chain confidentiality trade-off.
- No manifest/digest/code changes smuggled into a "docs-only" PR; no secret material committed; no attribution
  trailers in the commit or PR body (engagement forbids them — #27/HYG-1).

## A specific judgement the overseer needs
State explicitly in your `SYNTHESIS.md` whether the runbook **stands on its own** — i.e. whether it is a
strictly-better `deploy/chirp/README.md` independent of whether the live F1 fix has happened yet. The overseer
uses this to decide whether to land PR #30 now or hold it to land together with the live fix.

## Inputs (what to build on)
- PR #30 diff (`gh pr diff 30` / the `work/deploy-ghcr-auth` branch vs `main @ 22d2df6`, read-only).
- The committed deploy state on `main`: `deploy/chirp/` (manifests + current `README.md`) and
  `deploy/argocd/appproject.yaml` (the whitelist fact).
- The devops verdict this PR documents: `taskflow/dags/deploy-ghcr-auth/SYNTHESIS.md` and `FAILURE.md`.
- Issue #29 (F1 context) and PR #30's own body.

## What to evaluate — cover these as distinct concerns
- **Documentation correctness / accuracy** — every claim, path, digest, namespace, command, and ordering in the
  runbook matches the real committed state and the real cluster behavior.
- **Operability / completeness** — a competent operator could follow the runbook end-to-end and actually unblock
  the deploy and verify it; the AC1–4 verification steps are present and correct; no missing precondition.
- **Security & least-privilege guidance** — the credential advice is minimal-scope and correct; the
  public-package trade-off is represented honestly; nothing encourages over-broad tokens or committing secrets.
- **Clarity / editorial quality** — unambiguous, well-structured, consistent with the repo's docs idiom.

Decide the concerns and depth from what the diff touches; select and load whatever methodology serves them
yourself (the code-review methodology is your spine). This is a docs PR — weight documentation correctness and
operability accordingly; do not invent code-level concerns the diff does not raise.

## Declared output
- A root **`SYNTHESIS.md`** at this DAG's workspace root with the verdict (**APPROVE** / **REQUEST-CHANGES**),
  the findings (blockers vs non-blockers, each with severity + file/line location), the acceptance-criteria
  results, and the explicit "stands on its own?" judgement above.
- **Review visibility on GitHub (standing directive from #26)** — declared output includes: **(a)** PR #30 added
  to the NSWE Delivery board next to #29; **(b)** a **PR comment** on #30 carrying the verdict + reason (because
  `gh pr review --approve` is blocked when the PR author == the authenticated account, the `SYNTHESIS.md` verdict
  is authoritative and is posted as a comment); **(c)** the findings posted with severity + location, inline on
  the diff where a finding anchors to a line.
- Any **non-blocking** findings filed as **backlog issues** on the board, linked to PR #30 / #29. Do not file a
  duplicate of anything the board already holds.

## Constraints
- Repo scope: `Nousix-LLC/nswe-demo` only. Read-only on the tree — a review never modifies code or manifests and
  never merges or pushes. No force-push, no history rewrite, no attribution trailers.
- Gate strictly on your own root `SYNTHESIS.md` body as the authoritative verdict.
