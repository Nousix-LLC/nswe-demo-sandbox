# Task: Land the work — branch, commit, and open the PR into main (Closes #13)

## Task Specification

**Slug**: SUBTASK_land_pr
**Task Kind**: git / release operations (git-only)
**Status**: Pending

### Objective

Land the verified deploy manifests: put them on branch `work/deploy-argocd` based at `ada3aa9`, commit
(no attribution trailers), push, and open a PR into `main` that `Closes #13` with an accurate body and no
trailers; confirm CI is green. Do **NOT** merge the PR and do **NOT** push `main`. This task mutates
**git only** — no cluster.

### Context

Third stage of the `SUBTASK_synthesis` sub-subtree (hub `../_GLOBAL.md`, contract `../contracts/`). Your
declared dependencies — `SUBTASK_static_gate` (static GO) and `SUBTASK_deploy_reach` (reachability proven)
— are COMPLETED; read their outputs so the PR body is accurate to what actually shipped and was proven.
The manifests live in the working tree at `/home/user/nswe-demo/deploy/chirp/*` and
`/home/user/nswe-demo/deploy/argocd/*`.

⚠ Repo-state caveat (from `../../SUBTASK_discovery/outputs/ground_truth.md` §1): the checkout's local
`main` is **stale at `25e90c0`** (5 commits behind, and `ada3aa9` is NOT reachable from it); the #11
`Dockerfile`/`deploy/` baseline exists only at `ada3aa9`; the manifests are currently sitting in the
working tree. The branch `work/deploy-argocd` does not exist yet. Landing MUST base the branch at
`ada3aa9` (= `origin/main` HEAD) and bring the `deploy/chirp` + `deploy/argocd` files onto it cleanly, not
off the stale local `main`.

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Static gate report | `../SUBTASK_static_gate/outputs/static_gate_report.md` | Confirm GO; summarize verified posture in the PR body |
| Reachability evidence | `../SUBTASK_deploy_reach/outputs/reachability_evidence.md` | Confirm reachability proven; reference it in the PR body |
| Manifests to commit | `/home/user/nswe-demo/deploy/chirp/*`, `/home/user/nswe-demo/deploy/argocd/*` | The change set to land |
| Base/branch facts | `../../SUBTASK_discovery/outputs/ground_truth.md` §1, `../../contracts/deploy_contract.yaml` (layout) | Base `ada3aa9`, branch `work/deploy-argocd`, repo `Nousix-LLC/nswe-demo` |
| Sub-subtree contract | `../contracts/synthesis_gate_contract.yaml` | The required `pr_record.md` shape |

## Scope (what this task covers — you decide the method)

- Create `work/deploy-argocd` from `ada3aa9` and bring `deploy/chirp/` + `deploy/argocd/` onto it as a
  clean change set (so the branch contains the #11 baseline + the new deploy manifests, not the stale-`main` state).
- Commit with an accurate message and **no attribution trailers** (no "Generated with", no "Co-Authored-By").
- Push the branch and open a PR into `main` via the `gh` CLI; the PR body `Closes #13`, is accurate to what
  shipped and was proven reachable, and carries **no attribution trailers**.
- Confirm CI is green on the PR (reference the run). Do NOT merge the PR; do NOT push or force-push `main`.

Out of scope: any cluster mutation; re-running the deploy or reachability proof (done by
`SUBTASK_deploy_reach`); authoring `SYNTHESIS.md` (that is `SUBTASK_fold`).

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `outputs/pr_record.md` (under this task's workspace) |
| Side effect | Branch `work/deploy-argocd` pushed; PR opened into `main` (not merged) |
| Content | Per the `pr_record` schema in `../contracts/synthesis_gate_contract.yaml`: PR URL/number, base/head, commit SHA(s), Closes-#13 + no-trailers confirmation, CI-green reference, not-merged / main-not-pushed confirmation |

## Success Criteria

- [ ] Branch `work/deploy-argocd` based at `ada3aa9` carries the deploy manifests; commits have NO attribution trailers.
- [ ] A PR into `main` `Closes #13` with an accurate body and NO attribution trailers; CI green.
- [ ] The PR is NOT merged and `main` is NOT pushed/force-pushed; merged history not rewritten.
- [ ] `outputs/pr_record.md` records the PR URL, commit SHA(s), CI status, and the no-merge/no-main confirmations.

## Suggested Methodology Files

Task-type rows: *"PR creation and management via gh CLI"* (`operations`); *"Create PRs from taskflow
tasks"* (`operations` GitWorkflow); supporting `code-review` for PR authoring. SUGGESTIONS — you judge depth.

- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — the branch→commit→push→PR lifecycle via `gh`.
- `operations/CodeManagement_Branching_Strategy_Methodology.md` + `CodeManagement_Commit_Practices_Methodology.md` (core) — clean branch off the correct base, commit hygiene.
- `code-review/CodeReview_PR_Authoring_Methodology.md` — an accurate, reviewable PR body.
- `fast-delivery/FastDelivery_PR_Practices_For_AI_Authors_Methodology.md` — small-PR discipline; AI-author PR practices (optional, if useful).

Parent-flagged for this task type; load as a starting point, you are the final judge.

## Inherited Constraints

- **NO attribution trailers** on any commit or the PR body (#27/HYG-1) — overrides any default footer.
- Base at `ada3aa9`; branch `work/deploy-argocd`; PR into `main`. A DAG never merges its own PR and never pushes `main`; never force-push `main` or rewrite merged history.
- Repo `Nousix-LLC/nswe-demo` only; this subtree is the only writer of its branch.
- Do not commit secrets (the imagePullSecret is out-of-band, handled by `SUBTASK_deploy_reach`).

## Out-of-Scope Methodologies

- Kubernetes/GitOps deploy methodologies — the deploy + reachability proof is `SUBTASK_deploy_reach`.
- `synthesis/` gate + `decomposition/` content — the verdict and fold are `SUBTASK_fold`'s; you land what was verified.
