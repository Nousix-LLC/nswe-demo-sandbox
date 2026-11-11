# Task: Review PR #20 through the security / secrets / least-privilege lens

## Task Specification

**Slug**: SUBTASK_review_security_rbac
**Task Kind**: standard
**Status**: Pending

### Objective

Review PR #20 (infra-bootstrap, `deploy/bootstrap/`) through the **"is it secure and least-privilege"** lens,
producing a concern-scoped findings document. You review only; you do NOT edit, stage, push, or fix anything.

### Context

Part of the review-infra-bootstrap review DAG (see `../_GLOBAL.md` and the read-only `../contracts/`). You own
**two distinct review concerns** — treat each as its own concern with its own assessment:

1. **Security & secrets posture** — no committed kubeconfig / token / password / key anywhere in the diff;
   secrets are **retrieved at runtime** (ArgoCD admin password, kubeconfig), never staged into the repo. Judge
   the "least surprise" of what the scripts fetch and execute: provenance and pinning of any piped installer
   (`curl … | sh`, `kubectl apply -f <remote-url>`) — is the source trusted and version-pinned, or an
   unpinned/opaque remote execution? No over-broad fetch-and-run.
2. **Least-privilege RBAC / cluster posture** — ArgoCD's install namespace isolation and any RBAC it applies;
   whether anything is granted `cluster-admin` (or equivalently broad ClusterRole) without cause; whether the
   overall cluster / GitOps footprint matches the stated infra-only scope (ArgoCD's own install workloads are in
   scope; broad or surprising cluster-wide grants are a finding).

**Dependencies**: none. **Dependents**: `SUBTASK_synthesis_gate`.

## Input Specification

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Shared context, scope |
| Review contract | `../contracts/_MANIFEST.yaml`, `../contracts/finding_schema.md` | Finding schema, severity vocabulary, AC enumeration |
| Reviewed scripts (live tree) | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/checkout/deploy/bootstrap/` | The scripts + READMEs to read (esp. `gitops/` and `cluster/`) |
| PR diff + body | `gh pr diff 20 -R Nousix-LLC/nswe-demo`, `gh pr view 20 -R Nousix-LLC/nswe-demo` | Exact landed change; confirm nothing secret in the diff |
| Code DAG machine verdict (INPUT) | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/SYNTHESIS.md` | Its I2 (no committed secret) + I6 scope scan as a starting point to corroborate, not to trust blindly |

## Approach (not a runbook — your judgment governs depth)

Read the scripts and the diff with a secrets/least-privilege eye; independently corroborate the code DAG's I2
"no committed secret" claim (do your own scan for hard-value kubeconfig/token/password/key patterns vs. runtime
retrieval commands), judge piped-installer provenance/pinning, and assess ArgoCD's namespace isolation and any
RBAC/ClusterRole breadth against least-privilege. Classify defects by severity per the contract with concrete
remediation for block/major. Record clean concerns with the evidence that justifies "clean".

## Output Specification

**Primary output**: `review_security.md` in this workspace — per the contract's "Per-lens output document shape"
(lens summary; concern-by-concern assessment for both owned concerns; findings in schema; AC bearing). AC most in
your scope: AC2 (gitops — runtime-retrieved kubeconfig/ArgoCD access, never staged; namespace isolation) and the
AC4 "commit no secrets" clause — map each finding to the criteria it genuinely bears on.

## Success Criteria

- [ ] Both owned concerns assessed individually with evidence.
- [ ] Independent secrets scan performed (not merely citing the code DAG's I2) and its result recorded.
- [ ] Explicit judgment on piped-installer provenance/pinning and on ArgoCD RBAC/namespace least-privilege.
- [ ] Every finding well-formed per `finding_schema.md`; `review_security.md` written; no repo modification performed.

## Suggested Methodology Files

Domain Mapping rows matched: **"Security review" → Security (primary); Code Review (supporting)** and
**"Kubernetes RBAC & service-account least-privilege" → Kubernetes Security**. Load via
`engine_load_methodology { name: "<bundle_id>" }`, then reference:
- `security` — `Security_Secure_Coding_Methodology.md`, `BestPractices_Configuration_Management_Methodology.md` (secrets handling, no-committed-secrets, config/secret separation).
- `kubernetes-security` — `K8sSecurity_RBAC_And_Service_Accounts_Methodology.md` (least-privilege RBAC/ClusterRole breadth), `K8sSecurity_Secrets_Protection_Methodology.md` (runtime secret handling), `K8sSecurity_Supply_Chain_Security_Methodology.md` (piped-installer / remote-manifest provenance & pinning).
- `gitops` — `GitOps_Secrets_Management_Methodology.md` (how GitOps installs ought to handle the admin secret / kubeconfig).
- `code-review` — `CodeReview_Checklist_Methodology.md` (security review checklist, structuring findings).

Parent's flagged starting points for this task type; load as a starting point and use your own judgment — load
fewer if inapplicable, more if the scripts reveal additional surface.

## Inherited Constraints

- Review-only: never edit/stage/commit/push/merge; never touch `main`/branch/checkout.
- Subject is shell / infra / GitOps install scripts (not Rust app code).
- Do NOT reproduce the full cold install; review by reading. Corroborate the code DAG's security claims
  independently rather than assuming them.
- Emit findings strictly in the contract schema and severity vocabulary.

## Out-of-Scope Methodologies

- Script correctness / reproducibility / shell idiom — owned by `SUBTASK_review_correctness_repro` (note a
  security-relevant shell bug for the gate, but functional-correctness findings are that lens's).
- Honest-blocker (k3d substitution) adjudication, scope conformance, operability — owned by
  `SUBTASK_review_honesty_scope_ops`. (You may flag a *security* consequence of the k3d substitution; judging
  whether the substitution is an acceptable environment is not your call.)
