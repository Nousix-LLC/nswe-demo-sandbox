# SUSPENSION.md — remediate-epic-persist-r1 (NeedsDecompose)

## Disposition

`status: suspended`, `decompose_evaluation: NeedsDecompose`. This root task decomposed the PR #113 doc-blocker
remediation into a four-node serial pipeline with a synthesis gate, materialized every child, and now suspends
pending the subtree's resolution. The root resumes (folds `SUSPENDED → COMPLETED`) when the synthesis task writes
the root `SYNTHESIS.md` and folds it.

## Why decompose (evaluation summary)

The brief enumerates four distinct concerns with distinct bars (documentation-link correctness; documentation
accuracy; feature-gating hygiene; non-regression of durability) and declares outputs of two kinds (a committed code
change **and** an assessment verdict). The Scope trigger fires by the enumeration alone, and the Single-Responsibility
Test fires on the diagnose → edit → verify-and-deliver → judge pipeline. Per Trigger Precedence the small output size
does not override those fired signals; verdict: NeedsDecompose.

## Subtree materialized

| Task id | Depends on | Owns (output) |
|---------|------------|---------------|
| `SUBTASK_assess` | none | `SUBTASK_assess/INVENTORY.md` — complete doc-hazard correction inventory (contract schema) |
| `SUBTASK_apply_fixes` | `SUBTASK_assess` | docs-only edits committed to `work/epic-persist` + `SUBTASK_apply_fixes/CHANGESET.md` |
| `SUBTASK_verify_deliver` | `SUBTASK_apply_fixes` | `SUBTASK_verify_deliver/VERIFICATION.md` + PR #113 update in place |
| `SUBTASK_synthesis` (synthesis) | all three | `SYNTHESIS.md` at this root (the fold location / overseer observation seam) |

## Contract

`contracts/_MANIFEST.yaml` (ownership + identities: coverage, scope_docs_only, blocker_cleared, no_regression,
output_hygiene) and `contracts/inventory.schema.yaml` (the correction-record seam). Read-only for all descendants.

## Resumption condition

All child tasks reach terminal lifecycle state; the synthesis fold writes `SYNTHESIS.md` and flips this root to
COMPLETED.
