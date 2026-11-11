# SUSPENSION — SUBTASK_regression

**Status**: Suspended (NeedsDecompose)  
**Task**: SUBTASK_regression  
**Reason**: Scope trigger and enumerated-concerns rule fired during the decompose-evaluation.

## Decomposition Rationale

The brief explicitly enumerates three distinct Review Focus sections:
1. **Regression checks** — verify 9 previously-clean criteria against ferric-ssr-r4 commits
2. **Security** — HTML injection in SSR path, DOM spoofing in hydrate dispatch
3. **Code quality** — new code in `app.rs` and `hydrate_wasm.rs`

Per TASK_DECOMPOSITION_FRAMEWORK.md §Trigger Precedence (enumerated-concerns rule): "when the brief enumerates two or more distinct analyses, areas, themes, questions, sources, perspectives, components, or methodologies, the Scope-Based trigger and the Distinct Concerns Test fire by that enumeration alone — the agent MUST decompose."

The Single-Responsibility Test also fails: the task joins "verify regression" AND "check security" AND "assess quality" — three distinct verb families.

## Children Materialized

| Child | Workspace | Depends on | Output |
|-------|-----------|------------|--------|
| `SUBTASK_reg_criteria` | `SUBTASK_reg_criteria/` | none | `SUBTASK_reg_criteria/criteria_findings.md` |
| `SUBTASK_sec_quality` | `SUBTASK_sec_quality/` | none | `SUBTASK_sec_quality/sec_quality_findings.md` |
| `SUBTASK_verdict_synthesis` | `SUBTASK_verdict_synthesis/` | SUBTASK_reg_criteria, SUBTASK_sec_quality | `regression_verdict.md` |

## Resumption Condition

All three child tasks reach terminal lifecycle state (COMPLETED or FAILED). The synthesis child (`SUBTASK_verdict_synthesis`) writes `regression_verdict.md` to this workspace when complete.
