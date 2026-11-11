# SUSPENSION — review-infra-bootstrap (root, NeedsDecompose)

**Status**: SUSPENDED (decompose_evaluation = NeedsDecompose)
**Resumption**: all child tasks reach terminal lifecycle state; the synthesis gate folds its `SYNTHESIS.md`
into this parent via `engine_resume_suspended` (SUSPENDED → COMPLETED).

## Why decomposed

The brief enumerates eight distinct review concerns and directs `decompose → review → synthesize`. The
Scope-Based trigger and Distinct Concerns Test fired by that enumeration (Trigger Precedence: the single
`SYNTHESIS.md` output does not override a fired scope trigger). Verdict: NeedsDecompose.

## Cut (parallel review fan-out by review lens — 3 spokes + 1 synthesis gate)

| Task id | Role | Depends on | Output |
|---|---|---|---|
| `SUBTASK_review_correctness_repro` | Lens: correctness + reproducibility/idempotency + shell/k8s/GitOps idiom (concerns 1–3) | none | `review_correctness.md` |
| `SUBTASK_review_security_rbac` | Lens: security & secrets posture + least-privilege RBAC/cluster posture (concerns 4–5) | none | `review_security.md` |
| `SUBTASK_review_honesty_scope_ops` | Lens: honest-blocker/k3d verdict + scope conformance + operability (concerns 6–8); F1 recommendation | none | `review_honesty_scope_ops.md` |
| `SUBTASK_synthesis_gate` | Verification gate: fold → authoritative verdict; assert R1–R7; AC1–AC4 checklist; k3d + F1 calls; post gh review; fold | all three spokes | `SYNTHESIS.md` (at this parent/fold location — the observation seam) |

Cut rationale (recorded in `_GLOBAL.md §Chosen Cut`): cut by review lens (not by subsystem) for disjoint artifact
ownership (one findings doc per lens, no shared writers — ownership-disjointness hard gate satisfied), zero
cross-spoke dependency edges, each spoke an independently-reviewable specialist pass.

## Contract (frozen seam — `contracts/`)

`kind: taxonomy`. Finding schema + severity vocabulary (block/major/minor/nit) + verdict rule + AC1–AC4
enumeration + per-lens concern/artifact ownership + identities R1–R7 the gate asserts (concern coverage, AC
verdict coverage, finding well-formedness, single k3d verdict, single F1 disposition, verdict consistency,
review-only). No derived artifacts (review taxonomy).

## Authored before this suspension
- `_GLOBAL.md` (subtree hub)
- `contracts/_MANIFEST.yaml`, `contracts/finding_schema.md`
- `SUBTASK_review_correctness_repro/_BRIEF.md`
- `SUBTASK_review_security_rbac/_BRIEF.md`
- `SUBTASK_review_honesty_scope_ops/_BRIEF.md`
- `SUBTASK_synthesis_gate/_BRIEF.md`
- four `engine_amend_plan { add_task }` calls (one per child), applied.

The authoritative APPROVE / REQUEST-CHANGES landing verdict is produced by the synthesis gate's fold into this
parent's `SYNTHESIS.md`; the overseer gates PR #20's land on that folded record.
