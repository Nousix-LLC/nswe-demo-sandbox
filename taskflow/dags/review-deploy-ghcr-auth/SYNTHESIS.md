# SYNTHESIS.md — review-deploy-ghcr-auth (code review of PR #30)

**Verdict: APPROVE.**
PR #30 (`docs(chirp): least-privilege GHCR pull-auth runbook`, branch `work/deploy-ghcr-auth`, commit
`18ab880`, base `main @ 22d2df6`) is a **docs-only** change to `deploy/chirp/README.md` that is
technically accurate against the committed state, operationally runnable, sound on least-privilege, and
clean of smuggled changes/secrets/trailers. **No blockers.** The non-blocking items are minor editorial
nits, all out of the PR's own diff; none is backlog-worthy beyond what the board already holds (the
substantive rollout-prereq non-blocker is already tracked as **#29 F1**, which this PR documents).

This verdict (my root `SYNTHESIS.md` body) is the authoritative gate per the brief. The overseer may
**land PR #30 now on its own merit** — see the "stands on its own?" judgement below.

- Review task: `swe-coder` review DAG `review-deploy-ghcr-auth`, forked by `overseer/I52` for
  `Nousix-LLC/nswe-demo`. Reviews **PR #30**; related **issue #29** (F1).
- Evaluation: **Atomic** — one review responsibility over one small docs artifact; the four named
  concerns (doc correctness, operability, least-privilege, clarity) are lenses on one indivisible
  review, not separable subtasks.
- Read-only review: no code/manifest change, no merge, no push. `gh pr review --approve` is blocked
  (PR author == authenticated account `mattsmcknight`), so this `SYNTHESIS.md` is the authoritative
  verdict and is posted to PR #30 as a comment.

---

## Scope of the change (what was actually reviewed)

`gh pr diff 30` (authoritative, computed against the real base `main @ 22d2df6`) touches **exactly one
file**: `deploy/chirp/README.md`. The committed manifests, the `imagePullSecrets: [ghcr-pull]`
reference, and the pinned digest `@sha256:054af27…` are **unchanged**. (A `git diff main...` against the
local checkout shows extra files only because the local `main` ref is stale/behind the #28 merge; the
PR's real merge-base diff is README-only.)

The diff adds, to the existing runbook: (1) a least-privilege requirement on the pull credential;
(2) a new "Why the out-of-band Secret survives ArgoCD selfHeal/prune" section; (3) a live verification
runbook (AC1–4); (4) an honest supply-chain framing of the "make the package public" alternative.

## Acceptance-criteria results (from `_BRIEF.md`)

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| AC1 | Runbook is **technically accurate** vs the committed state (digest, `imagePullSecrets: [ghcr-pull]`, ns `chirp`, and the AppProject whitelist **not** including `Secret`) | ✅ PASS | README digest line matches `10-deployment.yaml:59`; `imagePullSecrets: [ghcr-pull]` matches `10-deployment.yaml:52-56`; ns `chirp` matches `00-namespace.yaml`; README's whitelist `{Service, ServiceAccount, ConfigMap, apps/Deployment, networking/Ingress}` matches `deploy/argocd/appproject.yaml:65-75` **exactly**, and `Secret` is **deliberately excluded** there (`appproject.yaml:60-64` says so verbatim). |
| AC2 | **One-step unblock** + **live verification runbook** are correct and runnable (pod on committed digest `1/1 Ready`, Application Synced+Healthy, `/healthz` 200 through ingress, selfHeal-survival re-check) | ✅ PASS | `kubectl create secret docker-registry ghcr-pull …` is the correct dockerconfigjson form and matches the devops `SYNTHESIS.md` unblock verbatim. Verify steps resolve: deployment `chirp-server` (✓ `10-deployment.yaml:11`), Application `chirp` in ns `argocd` (✓ `application.yaml:21-22`), ingress host `chirp.localhost` + serverlb `localhost:8081→80` (✓ `30-ingress.yaml:3-7,32`), `/healthz` health surface (✓ probes `10-deployment.yaml:72-93`). jsonpath expressions are valid. |
| AC3 | **Least-privilege guidance** sound (`read:packages`-ONLY, not broad `repo`/`workflow`/write/admin-packages) and **public-package alternative** framed honestly as a confidentiality trade-off | ✅ PASS | Option 1 requires a `read:packages`-ONLY token for `nousix-llc/chirp-server`, bot/deploy identity preferred, blast radius bounded — correct minimal scope for a GHCR pull. Option 2 is framed as a "deliberate supply-chain trade-off" (integrity/digest pin unchanged, confidentiality dropped), option 1 explicitly preferred. Honest and correct. |
| AC4 | No manifest/digest/code changes smuggled into a docs-only PR; no secret material committed; no attribution trailers on commit/PR (#27/HYG-1) | ✅ PASS | Diff is README-only. Added shell snippets use placeholders (`<token with read:packages ONLY>`), no real secret material. Commit `18ab880` has **no trailers** (`git show -s --format='%(trailers)'` empty); PR body carries no `Co-Authored-By`/`Generated with…`. PR body correctly does **not** carry `Closes #29`. |

## The four concerns evaluated

1. **Documentation correctness / accuracy — PASS.** Every claim, path, digest, namespace, command, and
   ordering in the runbook matches the real committed state (manifests above) and the authoritative
   devops verdict (`taskflow/dags/deploy-ghcr-auth/SYNTHESIS.md` / `FAILURE.md`): the live root cause
   (digest pod `ImagePullBackOff`, `ghcr-pull` absent, stale `chirp:local` pod masking), the whitelist
   fact, and the one-step unblock all agree. The selfHeal/prune reasoning is sound — an out-of-band
   `kubectl`-created Secret is untracked by ArgoCD **and** its kind is not in the AppProject whitelist,
   so `prune`/`selfHeal` (both `true` in `application.yaml:58-59`) will not delete it.
2. **Operability / completeness — PASS.** A competent operator can follow the runbook end-to-end:
   create the least-privilege Secret, let selfHeal roll the digest pod, then run the four verify steps.
   AC1–4 verification is present and correct; no missing precondition.
3. **Security & least-privilege guidance — PASS.** The credential advice is minimal-scope and correct;
   it actively steers away from over-broad tokens and from committing secrets, and keeps the AppProject
   un-widened (explicitly "do **not** add `Secret` to the whitelist just to commit a secret"). The
   public-package option is represented honestly as a confidentiality trade-off, not glossed.
4. **Clarity / editorial quality — PASS (with minor nits).** Well-structured, unambiguous, consistent
   with the repo's docs idiom (fenced command blocks, resolved-facts framing). See non-blockers.

## Findings

### Blockers — NONE.

### Non-blocking (minor; recorded, not filed — see rationale)

- **NB-1 [editorial · low] — stale pre-existing "Handoff to the synthesis gate (git state)" section.**
  `deploy/chirp/README.md:119-136` still describes the pre-#28 authoring handoff (local `main 25e90c0`
  "5 commits behind `origin/main @ ada3aa9`", instructions to checkout `work/deploy-argocd` from
  `ada3aa9` and commit the untracked `deploy/` tree). That is now historical — `deploy/` is on
  `main @ 22d2df6` and #28 has landed. **This section is OUTSIDE PR #30's diff** (the PR did not
  introduce or touch it); per the brief I do not invent concerns the diff does not raise, so it is **not
  a finding against #30**. Noted only as optional future cleanup for whoever next edits this README.
- **NB-2 [nit · trivial] — selfHeal-survival sync revision.** The verify step patches
  `{"operation":{"sync":{"revision":"HEAD"}}}` while the Application tracks `targetRevision: main`
  (`application.yaml:42`). `HEAD` resolves correctly, so this works; `main` would match the tracked
  revision exactly. Pure polish.
- **NB-3 [nit · trivial] — fine-grained PAT caveat.** Option 1 says "classic PAT or fine-grained PAT."
  A fine-grained PAT additionally needs the org-owned GHCR package to grant it read access; a one-clause
  caveat would spare an operator a surprise. Pure polish.

**No new backlog issues filed.** The one substantive, non-blocking rollout-prereq that this PR exists to
document is already tracked as **#29 F1** (and referenced by the devops `SYNTHESIS.md`); filing again
would duplicate the board. NB-1…NB-3 are trivial editorial nits below the bar for a tracked issue and
are recorded here (and surfaced in the PR comment) rather than turned into board noise, consistent with
the engagement's "reference, don't duplicate" convention (#25/#27/#29).

## Does the runbook stand on its own? — YES.

The new `deploy/chirp/README.md` is a **strictly-better** document independent of whether the live F1
fix has happened. Every added block is accurate and useful **now**:

- The least-privilege requirement and the public-package trade-off are credential *guidance* — correct
  regardless of cluster state.
- The "Why the out-of-band Secret survives selfHeal/prune" section documents a property that is
  **already true** of the committed manifests (the AppProject already excludes `Secret`); it records
  existing reality, not a future change.
- The verify runbook is correct against the committed state and is runnable whenever a deploy/unblock
  occurs; it does not assert the fix has been applied.

Nothing in the diff claims F1 is resolved live; the options are consistently framed as "before/at
deploy" preconditions, and the PR body + commit correctly withhold `Closes #29`. **Recommendation: the
overseer can land PR #30 now on its own merit**; it does not need to be held to land together with the
live fix. (It equally may be batched with the live fix — nothing in the PR precludes either; "stands on
its own" means landing-now carries no documentation-accuracy risk.)

## GitHub visibility (declared outputs, standing directive #26)

- **(a) Board:** PR #30 added to the **NSWE Delivery** project (`PVT_kwDOEB9jls4BlZH4`), next to #29.
- **(b) PR comment:** the verdict (APPROVE) + reason posted as a comment on PR #30 (authoritative gate,
  because `gh pr review --approve` is blocked when author == authenticated account).
- **(c) Inline findings:** none applicable — no finding anchors to a line **within the PR diff** (the
  diff is clean; NB-1 anchors to unchanged lines 119-136 outside the diff hunk, so GitHub cannot place
  an inline review comment there). The non-blocking nits are surfaced in the PR comment with their
  file/line locations instead.
- **Backlog issues:** none filed (see Findings rationale — #29 F1 already holds the substantive item).

## Inputs consulted

- PR #30 diff + metadata (`gh pr diff 30`, `gh pr view 30`).
- Committed state on the branch (== `main` for the manifests): `deploy/chirp/{README.md,00-namespace,
  10-deployment,20-service,30-ingress}.yaml`, `deploy/argocd/{appproject,application}.yaml`.
- Devops verdict this PR documents: `taskflow/dags/deploy-ghcr-auth/SYNTHESIS.md` and `FAILURE.md`.
- Issue #29 (F1 context) and PR #30's body/commit `18ab880`.
- Methodology spine: `code-review` bundle (Process, Checklist, Feedback Guidelines).
