# Task: Review PR #20 through the correctness / reproducibility / idiom lens

## Task Specification

**Slug**: SUBTASK_review_correctness_repro
**Task Kind**: standard
**Status**: Pending

### Objective

Review PR #20 (infra-bootstrap, `deploy/bootstrap/`) through the **"does it work, re-runnably, idiomatically"**
lens, producing a concern-scoped findings document. You review only; you do NOT edit, stage, push, or fix anything.

### Context

Part of the review-infra-bootstrap review DAG (see `../_GLOBAL.md` and the read-only `../contracts/`). You own
**three distinct review concerns** — treat each as its own concern with its own assessment, not as one blurred pass:

1. **Script correctness** — do the k3s/ArgoCD/wasm install + verify scripts actually do what they claim? Is the
   verification **genuine** (a real `kubectl get nodes` / rollout wait / ArgoCD health check; a real wasm build
   that produces `pkg/*.wasm`) rather than a fabricated or trivially-true green? Does each verify script fail
   when the thing it checks is actually broken?
2. **Reproducibility & idempotency** — safe re-run from a clean host and from a partial state (create-if-missing,
   server-side-apply converge, no-op when already satisfied); pinned/deterministic versions; correct shell
   discipline (`set -euo pipefail`, quoting, failure propagation, no swallowed errors).
3. **Code quality & the shell / k8s / GitOps idiom** — are the scripts idiomatic and maintainable for their
   domain (shell + kubectl + ArgoCD), readable at 2am during an incident, free of needless complexity?

**Dependencies**: none. **Dependents**: `SUBTASK_synthesis_gate`.

## Input Specification

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Shared context, scope, concern→lens map |
| Review contract | `../contracts/_MANIFEST.yaml`, `../contracts/finding_schema.md` | Finding schema, severity vocabulary, AC enumeration — emit findings in this exact shape |
| Reviewed scripts (live tree) | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/checkout/deploy/bootstrap/` | The six scripts + READMEs + `versions.txt` to read |
| PR diff + body | `gh pr diff 20 -R Nousix-LLC/nswe-demo`, `gh pr view 20 -R Nousix-LLC/nswe-demo` | Exact landed change |
| Code DAG machine verdict (INPUT) | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/SYNTHESIS.md` | What the cold gate already verified (lean on it for the build it ran; do NOT re-run the full install) |

## Approach (not a runbook — your judgment governs depth)

Read the six scripts and the code DAG's recorded evidence; judge the three concerns above against what the code
actually does. Rely on the code DAG's cold gate for the build/verification it already executed — your job is to
judge correctness, re-runnability, and idiom by reading, not to reproduce the install. Classify every defect by
severity (`block`/`major`/`minor`/`nit`) per the contract, with concrete actionable remediation for block/major.
Where a concern is clean, say so with the evidence that justifies it (absence of findings is an evidenced
conclusion, never silence).

## Output Specification

**Primary output**: `review_correctness.md` in this workspace — per the contract's "Per-lens output document
shape" (lens summary; concern-by-concern assessment for all three owned concerns; findings in schema; which of
AC1..AC4 your findings touch). AC most in your scope: AC1 (cluster script mechanics), AC3 (genuine wasm build),
AC4 (idempotency/pinning clause) — but map each finding to the criteria it genuinely bears on.

## Success Criteria

- [ ] All three owned concerns assessed individually with evidence.
- [ ] Every finding well-formed per `finding_schema.md` (severity in vocabulary; block/major carry actionable remediation).
- [ ] Explicit judgment on whether verification is genuine vs. trivially-true green for each of the three subsystems.
- [ ] `review_correctness.md` written; no repo/branch/checkout modification performed.

## Suggested Methodology Files

Domain Mapping row matched: **"Code review" → Code Review (primary); Core, Testing (supporting)**, extended for
the shell/infra/GitOps subject matter. Load via `engine_load_methodology { name: "<bundle_id>" }`, then reference
the specific members:
- `code-review` — `CodeReview_Checklist_Methodology.md`, `CodeReview_Process_Methodology.md` (the review rubric + how to structure findings).
- `core` — `BestPractices_Error_Handling_Methodology.md`, `BestPractices_Coding_Standards_Methodology.md` (failure propagation, shell discipline baseline).
- `operations` — `DevTools_CICD_Methodology.md`, `DevTools_Build_Systems_Methodology.md` (reproducible/pinned build + install-script idiom).
- `containerization` — `Containerization_Runtime_Methodology.md` (k3d/Docker runtime semantics the k3s install relies on).
- `kubernetes` — `K8s_Networking_And_Service_Connectivity_Methodology.md` (what a genuine node-Ready / rollout check looks like).
- `gitops` — `GitOps_Reconciliation_And_Drift_Control_Methodology.md` (server-side-apply converge / idempotent reconcile idiom for the ArgoCD install).
- `code-quality` — `Framework_Clean_Code_Methodology.md` (readability / needless-complexity bar).

These are the parent's flagged starting points based on the task type. You SHOULD load them as a starting point
but are the final judge of what your work requires — load fewer if some are clearly inapplicable, load more if
your reading of the scripts reveals additional methodology surface.

## Inherited Constraints

- Review-only: do not edit/stage/commit/push/merge/relock/rebase; never touch `main` or the PR branch or the checkout.
- Subject is shell / infra / GitOps, not Rust app code — review against the shell/k8s/GitOps idiom.
- Do NOT reproduce the full cold install to re-derive PASS; the code DAG already ran it. Review by reading.
- Emit findings strictly in the contract schema and severity vocabulary.

## Out-of-Scope Methodologies

- Security & secrets posture and RBAC/cluster posture — owned by `SUBTASK_review_security_rbac`. If you notice a
  security issue, note it briefly for the gate but do not make it your finding; it is the security lens's to own.
- Honest-blocker (k3d substitution) adjudication, scope conformance, and operability/runbook-walkthrough — owned
  by `SUBTASK_review_honesty_scope_ops`. (You may observe that a verify step is genuine; judging whether the k3d
  substitution is an acceptable environment is not your call.)
- Rust app-code methodologies (`rust/`, TDD app testing) — this diff contains no app code.
