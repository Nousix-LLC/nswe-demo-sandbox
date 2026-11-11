# Suspension Record — SUBTASK_validate-crossrefs

**Status**: Suspended (NeedsDecompose)  
**Reason**: The brief named two distinct analyses — REQ register cross-reference reconciliation
and GitHub issue traceability — that satisfy the Scope-Based trigger's enumerated-concerns rule.
The task was decomposed into three children.

## Children Materialized

| Task id | Kind | Depends on | Output |
|---|---|---|---|
| `SUBTASK_req-reconciliation` | standard | none | `req-reconciliation.md` |
| `SUBTASK_issue-traceability` | standard | none | `issue-traceability.md` |
| `SUBTASK_synthesis-crossrefs` | synthesis | both above | `crossrefs-findings.md`, `SYNTHESIS.md` |

## Resumption Condition

All three child tasks reach terminal lifecycle states. The synthesis child
(`SUBTASK_synthesis-crossrefs`) will fold this parent `SUSPENDED → COMPLETED` via
`engine_resume_suspended` using `SYNTHESIS.md` at this workspace as the seam.

## Authored Artifacts

- `_GLOBAL.md` — subtree hub describing the two-spoke decomposition
- `contracts/_MANIFEST.yaml` — intermediate artifact schemas and ownership manifest
- `SUBTASK_req-reconciliation/_BRIEF.md` — REQ reconciliation spoke brief
- `SUBTASK_issue-traceability/_BRIEF.md` — issue traceability spoke brief
- `SUBTASK_synthesis-crossrefs/_BRIEF.md` — synthesis gate brief
