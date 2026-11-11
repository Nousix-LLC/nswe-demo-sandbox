# Task: Review PR #20 through the honesty / scope / operability lens

## Task Specification

**Slug**: SUBTASK_review_honesty_scope_ops
**Task Kind**: standard
**Status**: Pending

### Objective

Review PR #20 (infra-bootstrap, `deploy/bootstrap/`) through the **"is it honest, in-scope, and operable"** lens,
producing a concern-scoped findings document that also renders the explicit k3d-substitution verdict the gate
requires. You review only; you do NOT edit, stage, push, or fix anything.

### Context

Part of the review-infra-bootstrap review DAG (see `../_GLOBAL.md` and the read-only `../contracts/`). You own
**three distinct review concerns** — treat each as its own concern with its own assessment:

1. **Honest-blocker handling (the k3d-vs-native substitution)** — the code DAG reports that the native systemd
   k3s install cannot run on the rootless sandbox host (uid 1001, no non-interactive sudo, protected paths) and
   auto-selected **k3d** (k3s-in-Docker, proven Ready), carrying the native path unchanged for a privileged host.
   Judge: (a) is this a **genuine k3s environment** (so downstream #12 image build + #13 deploy can legitimately
   target it) or a weakening/substitution that misrepresents the deliverable? (b) is the caveat surfaced
   **honestly and completely** in the PR body AND `cluster/README.md` — not hidden, not overstated? (c) should
   anything become a **tracked follow-up issue or escalation** (e.g. if the eventual #13 deploy needs a cluster
   the sandbox cannot host)? Render a single explicit verdict `acceptable | blocking-weakening` with reasoning
   (contract identity R4).
2. **Scope conformance** — confirm infra-only: **zero** app `Dockerfile`, `kind: Deployment`, or
   `kind: Application` staged (those are #12 / #13). ArgoCD's own install workloads are in scope; an app-level
   manifest or Dockerfile would be an out-of-scope finding.
3. **Operability** — run-order clarity, a per-track verification step, kubeconfig / ArgoCD access documentation,
   logging to stdout; can a newcomer follow the unified `deploy/bootstrap/README.md` end to end?

You are also the lens that forms a recommendation on the code DAG's **F1** finding (carry-as-tracked-issue vs.
drop) for the gate to adjudicate — F1 is a contract-wording tension (see `../_GLOBAL.md` inputs), so weigh it as
a documentation/honesty follow-up candidate.

**Dependencies**: none. **Dependents**: `SUBTASK_synthesis_gate`.

## Input Specification

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Shared context, scope |
| Review contract | `../contracts/_MANIFEST.yaml`, `../contracts/finding_schema.md` | Finding schema, severity vocabulary, AC enumeration; R4/R5 context |
| Reviewed tree (live) | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/checkout/deploy/bootstrap/` | Unified `README.md`, `cluster/README.md` (caveat), all scripts/READMEs |
| PR body + diff | `gh pr view 20 -R Nousix-LLC/nswe-demo`, `gh pr diff 20 -R Nousix-LLC/nswe-demo` | Where the k3d caveat must be surfaced honestly; scope scan |
| Code DAG machine verdict (INPUT) | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/SYNTHESIS.md` | Its native-install sub-blocker note, I6 scope scan, and finding F1 (for your disposition recommendation) |

## Approach (not a runbook — your judgment governs depth)

Read the PR body and the two runbook-level READMEs to judge caveat honesty/completeness; independently scope-scan
the staged tree for app Dockerfile/Deployment/Application artifacts; walk the unified runbook as a newcomer would
and judge operability. Form the single k3d-substitution verdict and the F1 disposition recommendation. Classify
defects by severity per the contract with concrete remediation for block/major; record clean concerns with
evidence.

## Output Specification

**Primary output**: `review_honesty_scope_ops.md` in this workspace — per the contract's "Per-lens output
document shape" (lens summary; concern-by-concern assessment for all three owned concerns; findings in schema; AC
bearing), PLUS an explicit `k3d-substitution verdict:` line (`acceptable | blocking-weakening` + reasoning on
downstream #12/#13 targetability and caveat honesty) and an explicit `F1 recommendation:` line
(`carry-as-tracked-issue | drop` + rationale). AC most in your scope: AC2 (ArgoCD access docs), AC4 (runbook run
order + per-track verification), and the honesty of AC1's "Ready" claim given k3d.

## Success Criteria

- [ ] All three owned concerns assessed individually with evidence.
- [ ] A single explicit k3d-substitution verdict rendered with reasoning (satisfies the gate's R4 input).
- [ ] An explicit F1 disposition recommendation with rationale (feeds the gate's R5).
- [ ] Independent scope scan performed; result recorded. `review_honesty_scope_ops.md` written; no repo modification.

## Suggested Methodology Files

Domain Mapping rows matched: **"Code review" → Code Review; Core** extended with GitOps/Kubernetes/Operations for
the subject. Load via `engine_load_methodology { name: "<bundle_id>" }`, then reference:
- `code-review` — `CodeReview_Process_Methodology.md`, `CodeReview_Feedback_Guidelines_Methodology.md` (honest, actionable review posture).
- `operations` — `BestPractices_Documentation_Methodology.md` (runbook completeness / newcomer-follows-it bar), `Observability_Incident_Management_Methodology.md` (whether the sandbox-vs-privileged-host caveat warrants a tracked issue/escalation).
- `gitops` — `GitOps_Repository_Topology_And_App_Composition_Methodology.md` (what belongs to infra bootstrap vs. an app `Application` — the #13 scope line).
- `kubernetes` — `K8s_Day2_Operations_And_Multitenancy_Methodology.md` (whether a k3d-hosted k3s is a legitimate target env for downstream deploys).
- `core` — `CodeManagement_Commit_Practices_Methodology.md` (honest PR body / caveat surfacing).

Parent's flagged starting points; load as a starting point and use your judgment — fewer if inapplicable, more if
the runbook/caveat reveals additional surface.

## Inherited Constraints

- Review-only: never edit/stage/commit/push/merge; never touch `main`/branch/checkout.
- Subject is shell / infra / GitOps (not Rust app code).
- Infra-only boundary (#12 containerization and #13 app manifests/ArgoCD `Application` are out of scope — a
  staged artifact of those kinds is itself a scope-conformance finding).
- Emit findings strictly in the contract schema and severity vocabulary.

## Out-of-Scope Methodologies

- Script functional correctness / reproducibility / shell idiom — owned by `SUBTASK_review_correctness_repro`.
- Security & secrets posture and RBAC breadth — owned by `SUBTASK_review_security_rbac` (you may note that the
  k3d caveat has a security dimension, but the secrets/RBAC findings are that lens's).
