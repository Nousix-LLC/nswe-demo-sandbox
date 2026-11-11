# _BRIEF.md — SUBTASK_remediate (deploy-ghcr-auth-r2)

## Task Specification
**Slug**: SUBTASK_remediate
**Task Kind**: standard
**Status**: Pending

### Objective
Make **the change, and only the change**, that brings the live Chirp deployment to the committed GitOps desired
state — along the decision branch the diagnosis selected — so the committed digest pulls and runs; or, if the pull
is not reachable, record precisely and cleanly what external input is still required. This task performs the change;
it does **not** render the AC1–5 verdict (that is the verification gate's job — the change/verify split).

### Context
Part of `deploy-ghcr-auth-r2` (see `../_GLOBAL.md`). This is the **transform** stage: consume `diagnosis.md`, act on
the chosen branch, produce a record of what changed. The overseer lands/merges; you change the cluster and open the
PR (if a repo change is needed), through the repo where GitOps owns desired state.

**Dependencies**: `SUBTASK_diagnose`. **Dependents**: `SUBTASK_verify_synthesis`.

## Input Specification
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree context | `../_GLOBAL.md` | Scope, constraints, success criteria |
| Deployment identity + ownership + identities | `../contracts/_MANIFEST.yaml` (read-only) | Constants to preserve; what you own; the invariants your change must not break |
| **Diagnosis** | `../SUBTASK_diagnose/diagnosis.md` | The fresh live state and the chosen `decision_branch` — act on this, do not re-diagnose from scratch |
| Host/cluster access | the repo checkout's `CLAUDE.md` | How to reach/change the cluster and apply through GitOps |
| Committed GitOps state + runbook | `deploy/chirp/*` + `README.md` @ `main` | Desired state; the pull-auth runbook (PR #30) |

## Process (approach — not a runbook)
Act strictly on `diagnosis.md`'s `decision_branch`:
- **already-working** — no cluster change and no PR are needed; confirm the convergence you were handed and record
  that the desired state is already met. Do not manufacture a change.
- **create-secret** — create the **least-privilege** out-of-band `ghcr-pull` docker-registry Secret in ns `chirp`
  from the reachable `read:packages`-only credential for the one package, per the runbook in `deploy/chirp/README.md`.
  Let ArgoCD selfHeal roll the committed digest to Ready and the stale RS to 0; reconcile any drift so desired ==
  running. Preserve posture: no secret material in git, digest pin unchanged, AppProject scope unchanged, no broad RBAC.
- **blocked** — no reachable credential: do **not** burn effort on a blind retry of the ruled-out paths. Record
  cleanly and precisely what is still needed and exactly where the system expects it (the one-step unblock).

Open a PR on `work/deploy-ghcr-auth-r2` into `main` **only if a repository change is actually needed** (per
`diagnosis.md`'s `repo_change_needed`; the out-of-band Secret is **not** a repo change). If you open a PR, author its
body **without** a `Closes #32` line — the issue-closing decision is verdict-gated and belongs to the verification
gate. Keep any PR small and reviewable; host facts never appear in the PR.

## Output Specification
**Primary output**: `remediation.md` in this workspace — what was changed (the Secret created, drift reconciled, RS
scaled) **or** why no change was needed (already-working) **or** why blocked and the precise external input required;
plus the PR link and branch/commit if a PR was opened. Record which `../contracts/_MANIFEST.yaml` identities your
action touched. Do **not** declare an AC pass/fail verdict here (watching a rollout converge while you work is fine as
process; it is not a declared verdict).

## Success Criteria
- [ ] Acted on exactly the `decision_branch` from `diagnosis.md`; no re-diagnosis, no action off-branch.
- [ ] On create-secret: the Secret is least-privilege, out-of-band (uncommitted), and the digest pod is rolling/rolled
      to the committed image with the stale RS heading to 0; posture invariants (I5) preserved.
- [ ] On blocked: a clean, precise statement of the external input and where it is expected — not an open-ended wait,
      not a blind retry.
- [ ] A PR exists **iff** a repository change was genuinely needed; its body omits `Closes #32`; no host facts in it.
- [ ] No secret committed to the repo; no `main` force-push/history rewrite; no attribution trailers.
- [ ] `remediation.md` is self-contained for the verification gate.

## Suggested Methodology Files
Parent's Domain-Mapping reading: *"GitOps secrets management"* → **GitOps** (primary) + **Security**;
*"Kubernetes RBAC & service-account least-privilege"* / *"secrets protection"* → **Kubernetes Security**;
*"GitOps reconciliation / drift & self-heal"* → **GitOps**; *"PR creation and management via gh CLI"* → **Operations**.
- `gitops/GitOps_Secrets_Management_Methodology.md` — how an out-of-band / unmanaged Secret sits correctly alongside GitOps desired state.
- `gitops/GitOps_Reconciliation_And_Drift_Control_Methodology.md` — drive reconcile/selfHeal to converge desired == running.
- `kubernetes-security/K8sSecurity_Secrets_Protection_Methodology.md` — least-privilege registry Secret, no secret sprawl, nothing in git.
- `kubernetes-security/K8sSecurity_RBAC_And_Service_Accounts_Methodology.md` — keep the blast radius minimal; no broad RBAC.
- `operations/GitWorkflow_PR_Lifecycle_Methodology.md` — open a tidy PR on the integration branch if a repo change is needed.
- `security/BestPractices_Configuration_Management_Methodology.md` — handle credential material safely during Secret creation.

*Parent's flagged starting points for this task type. Load fewer if a branch makes some inapplicable (e.g. the
already-working branch needs almost none); load more if your reading reveals additional surface.*

## Inherited Constraints
- **Change through the repo where GitOps owns desired state; repository changes land as reviewed PRs** — the overseer
  merges, you open.
- Never commit a secret/registry credential; never force-push `main` or rewrite merged history; no attribution trailers.
- Scope limited to `chirp*` namespaces and ArgoCD Application `chirp`.
- Preserve supply-chain posture: digest pin unchanged, AppProject scope unchanged, least-privilege only.
- `Closes #32` is NOT yours to add — it is verdict-gated to `SUBTASK_verify_synthesis`.
- Host facts stay out of anything bound for GitHub.

## Out-of-Scope Methodologies
- `synthesis/*` — you do not run the verification gate or render the AC verdict.
- `decomposition/*` — decomposer-side only.
