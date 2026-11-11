# _GLOBAL.md — review-infra-bootstrap (review DAG hub)

## Project Context

**Status**: Active

### Objective

Render the **authoritative human-landing review verdict** (APPROVE / REQUEST-CHANGES) for **PR #20**
(`Nousix-LLC/nswe-demo`, `work/infra-bootstrap` → `main`, Closes #10, head `016bd44`, base `main @ fcfc7a2`) —
the infra-bootstrap deliverable: reproducible scripts + a unified runbook under `deploy/bootstrap/` that stand
up and PROVE a k3s cluster, the ArgoCD GitOps control plane, and the WASM build toolchain. The verdict is folded
into this subtree's **root `SYNTHESIS.md`** (this workspace), which is the record the overseer gates the land on.

This DAG **reviews**; it does NOT re-implement, edit, stage, push, relock, rebase, force-push, touch `main`, or
merge. Blocking defects ⇒ verdict REQUEST-CHANGES with precise actionable findings; remediation is a separate
forked DAG the overseer dispatches, never an edit from inside this DAG.

### Scope

**In scope:** reviewing the PR #20 diff (+912/-0 across 11 files, all under `deploy/bootstrap/`: six `bash`
scripts + four READMEs + `versions.txt`) against the #10 acceptance criteria and the eight named review concerns;
reading the code DAG's folded machine verdict as INPUT; producing a single authoritative verdict; posting a
`gh pr review 20` (expected to post as COMMENTED due to the self-review platform block — authoritative verdict
lives in `SYNTHESIS.md`, not the gh review state).

**Out of scope:** any modification to the repo, branch, or checkout; re-running the full cold install to
re-derive the machine PASS (rely on the code DAG's gate for the build it already ran); reviewing Rust app code
(this diff is shell/infra/GitOps only); containerization (#12) or app manifests / ArgoCD `Application` (#13).

### Success Criteria

- [ ] All eight review concerns covered, each by exactly one review lens, classified by severity (block / major / minor / nit).
- [ ] Every #10 acceptance criterion (AC1 cluster, AC2 gitops, AC3 wasm, AC4 runbook) carries an explicit pass/fail verdict.
- [ ] Explicit, reasoned line on the **k3d-vs-native substitution** (acceptable / blocking weakening).
- [ ] Explicit disposition of the code DAG's **F1** minor finding (carry-as-tracked-issue / drop).
- [ ] A single `verdict: APPROVE | REQUEST-CHANGES` in root `SYNTHESIS.md`, consistent with the finding set, plus a posted `gh pr review`.

## Inputs (shared, read-only for every task in this subtree)

| Input | Location | Purpose |
|---|---|---|
| This hub | `_GLOBAL.md` (this file) | Shared context, scope, concern→lens map |
| Review contract | `contracts/_MANIFEST.yaml` + `contracts/finding_schema.md` | Finding schema, severity vocabulary, AC enumeration, ownership, identities the gate asserts |
| The reviewed code (live working tree) | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/checkout/deploy/bootstrap/` (on `work/infra-bootstrap` @ `016bd44`) | The six scripts + four READMEs + `versions.txt` under review |
| The PR diff | `gh pr diff 20 -R Nousix-LLC/nswe-demo` (and `gh pr view 20`) | The exact landed change + PR body (k3d caveat lives here) |
| Code DAG machine verdict (INPUT, not authority) | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/SYNTHESIS.md` | gate=PASS round 1; identities I1–I6 PASS; minor finding **F1** (contract-wording tension, recorded-not-plugged) |
| Code DAG contract (context for F1) | `/home/user/nousix-runtime/nswe-demo/taskflow/dags/infra-bootstrap/contracts/` | Grounds the F1 disposition decision |

## Chosen Cut (rationale — recorded per decomposition discipline)

The brief enumerates eight distinct review concerns; the Scope/Distinct-Concerns triggers fired on that
enumeration, so this task decomposed. **Cut by review lens**, not by subsystem:

- Candidate "by subsystem" (cluster / gitops / wasm, mirroring the code DAG) was **rejected**: it forces every
  spoke to re-bundle all eight concerns, and the brief's decomposition axis is explicitly the *concerns*.
- Candidate "by review lens" was **chosen**: disjoint artifact ownership (one findings doc per lens — no shared
  writers, ownership-disjointness hard gate satisfied), zero cross-spoke dependency edges, each spoke an
  independently-reviewable specialist pass in the S/M band.

Cross-cutting assembly (the AC N/N checklist and the final verdict) is **not** a spoke concern — it is owned by
the synthesis **verification gate**, which folds the three lens outputs. Each acceptance criterion's final
pass/fail is a gate identity computed from the union of findings touching it (see `contracts/`).

### Concern → lens ownership map (each concern owned once)

| # | Review concern (from `_BRIEF.md`) | Owning lens spoke |
|---|---|---|
| 1 | Script correctness (genuine verification, no fabricated green) | `SUBTASK_review_correctness_repro` |
| 2 | Reproducibility & idempotency (clean + partial re-run, pins, shell discipline) | `SUBTASK_review_correctness_repro` |
| 3 | Code quality & shell/k8s/GitOps idiom | `SUBTASK_review_correctness_repro` |
| 4 | Security & secrets posture (no committed secrets, runtime-retrieval, piped-installer provenance) | `SUBTASK_review_security_rbac` |
| 5 | Least-privilege RBAC / cluster posture (ArgoCD namespace isolation, no needless cluster-admin, footprint vs scope) | `SUBTASK_review_security_rbac` |
| 6 | Honest-blocker handling (k3d-vs-native substitution: genuine k3s vs weakening; caveat honesty/completeness; escalation/tracked-issue) | `SUBTASK_review_honesty_scope_ops` |
| 7 | Scope conformance (infra-only; zero app Dockerfile / `kind: Deployment` / `kind: Application`) | `SUBTASK_review_honesty_scope_ops` |
| 8 | Operability (run order, per-track verification, kubeconfig/ArgoCD access docs, stdout logging, newcomer-follows-runbook) | `SUBTASK_review_honesty_scope_ops` |

## Task Structure

```
review-infra-bootstrap/
├── _GLOBAL.md                              (this hub)
├── contracts/
│   ├── _MANIFEST.yaml                      (kind=taxonomy; ownership, identities R1–R7, AC enumeration)
│   └── finding_schema.md                   (finding record schema + severity vocabulary + verdict rule)
├── SUBTASK_review_correctness_repro/_BRIEF.md     (lens: does it work, re-runnably, idiomatically → review_correctness.md)
├── SUBTASK_review_security_rbac/_BRIEF.md         (lens: secure & least-privilege → review_security.md)
├── SUBTASK_review_honesty_scope_ops/_BRIEF.md     (lens: honest, in-scope, operable → review_honesty_scope_ops.md)
└── SUBTASK_synthesis_gate/_BRIEF.md               (synthesis gate: fold → root SYNTHESIS.md + gh pr review + fold)
```

### Task Summary (authoritative DAG table)

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_review_correctness_repro` | none | Correctness + reproducibility/idempotency + shell/k8s/GitOps idiom review of all six scripts + versions file | `SUBTASK_review_correctness_repro/review_correctness.md` |
| `SUBTASK_review_security_rbac` | none | Security & secrets posture + least-privilege RBAC / cluster posture review | `SUBTASK_review_security_rbac/review_security.md` |
| `SUBTASK_review_honesty_scope_ops` | none | Honest-blocker (k3d substitution) + scope conformance + operability review | `SUBTASK_review_honesty_scope_ops/review_honesty_scope_ops.md` |
| `SUBTASK_synthesis_gate` | `SUBTASK_review_correctness_repro`, `SUBTASK_review_security_rbac`, `SUBTASK_review_honesty_scope_ops` | Verification gate: fold three lens outputs into the authoritative verdict; assert identities R1–R7; post gh review | `SYNTHESIS.md` (at this parent workspace — the fold/observation seam) |

### Dependency Graph

```
SUBTASK_review_correctness_repro ──┐
SUBTASK_review_security_rbac      ──├── SUBTASK_synthesis_gate ── (fold → parent SYNTHESIS.md)
SUBTASK_review_honesty_scope_ops  ──┘
```

## Subtree Methodology Posture

**Dominant task type:** Code review (software domain). Every leaf is a review lens; the hub is a verification gate.
**Primary bundles in scope across the subtree:** `code-review`, `core`. Lens-specific supporting bundles are
propagated per child `_BRIEF.md` (security / kubernetes-security / gitops for the security lens; operations /
containerization / code-quality / kubernetes / gitops for the correctness lens; gitops / kubernetes / operations
for the honesty-scope-ops lens; `synthesis` for the gate).
**Subtree-wide binding conventions:** (1) review-only — no task modifies the repo/branch/checkout/`main`;
(2) findings use the contract's severity vocabulary and schema verbatim; (3) the code DAG `SYNTHESIS.md` is INPUT
context, never the authority — this DAG's folded `SYNTHESIS.md` is the authoritative landing record;
(4) suggestion-not-prescription — each child loads the suggested methodology IDs plus whatever its own reading
reveals it needs, and is the final judge.

## Subtree-Wide Constraints

- Engagement scope is **only** `Nousix-LLC/nswe-demo`.
- The diff is shell / infra / GitOps (not Rust app code); review against shell/k8s/GitOps idiom, not app-code idiom.
- Rely on the code DAG's cold machine gate for the build/verification it already executed; do NOT reproduce the
  full install to re-derive PASS. Review for correctness, design, security, reproducibility, and honesty.
- Infra-only boundary: containerization (#12) and app manifests / ArgoCD `Application` (#13) are out of scope; a
  staged artifact of those kinds would itself be an in-scope *scope-conformance* finding.
