# SUSPENSION.md — SUBTASK_verify_deliver

**Task**: SUBTASK_verify_deliver  
**Decompose evaluation**: NeedsDecompose  
**Suspension kind**: Decomposition — awaiting child subtree to reach terminal states

## Decomposition Rationale

The brief names 3 distinct concerns under a "Distinct concerns" header (scope trigger fires) and
the task name "verify_deliver" joins two different-in-kind operations with "and" (single-
responsibility test fires). Per TDF trigger precedence, either firing trigger mandates decomposition.

The two fired triggers:
1. **Scope / enumeration**: brief enumerates "Blocker verification", "Non-regression
   verification", "Delivery" as distinct concerns → scope trigger fires
2. **Single-responsibility test / conjunction**: verify ≠ deliver in kind (observe CI state vs.
   write PR description); the task name is the conjunction itself → single-responsibility test fires

## Children Materialized

| Child ID | Workspace | Depends on | Output |
|----------|-----------|------------|--------|
| `SUBTASK_ci_verify` | `SUBTASK_verify_deliver/SUBTASK_ci_verify/` | none | `CI_EVIDENCE.md` |
| `SUBTASK_pr_update` | `SUBTASK_verify_deliver/SUBTASK_pr_update/` | `SUBTASK_ci_verify` | `PR_UPDATE.md` |
| `SUBTASK_synthesis` | `SUBTASK_verify_deliver/SUBTASK_synthesis/` | `SUBTASK_ci_verify`, `SUBTASK_pr_update` | `../VERIFICATION.md` |

## Resumption Condition

Implicit: all child tasks (`SUBTASK_ci_verify`, `SUBTASK_pr_update`, `SUBTASK_synthesis`) reach
terminal lifecycle states. The synthesis child folds this parent from SUSPENDED to COMPLETED by
calling `engine_resume_suspended { target_task_id: "SUBTASK_verify_deliver", ... }` after writing
`VERIFICATION.md` at this workspace.
