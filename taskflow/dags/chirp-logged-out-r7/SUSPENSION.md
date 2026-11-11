# SUSPENSION — Chirp Logged-Out Visitor Experience r7

**Task**: chirp-logged-out-r7  
**Decompose evaluation**: NeedsDecompose  
**Suspended at**: decomposition complete, children materialized  

## Children Materialized

This task has been decomposed into four atomic child tasks:

| Child task id | Depends on | Description |
|---|---|---|
| `SUBTASK_explore-codebase` | none | Explore codebase, read design docs, create branch, produce analysis.md |
| `SUBTASK_backend-api` | SUBTASK_explore-codebase | Implement public API endpoints in chirp-server |
| `SUBTASK_frontend-ui` | SUBTASK_backend-api | Implement frontend UI with 4 states, profile, navigation |
| `SUBTASK_synthesis` | SUBTASK_frontend-ui | Verify ACs, create PR closing #35, produce SYNTHESIS.md |

## Resumption Condition

This parent task resumes (transitions SUSPENDED → COMPLETED) when its entire subtree resolves to terminal states — specifically when SUBTASK_synthesis completes and produces `SYNTHESIS.md` at this workspace root.

## Workspace Structure

```
chirp-logged-out-r7/
├── _GLOBAL.md                                  (subtree hub)
├── contracts/
│   ├── _MANIFEST.yaml                          (ownership, identities)
│   └── public_api_contract.md                  (API surface declaration)
├── SUBTASK_explore-codebase/_BRIEF.md          (child brief)
├── SUBTASK_backend-api/_BRIEF.md               (child brief)
├── SUBTASK_frontend-ui/_BRIEF.md               (child brief)
├── SUBTASK_synthesis/_BRIEF.md                 (synthesis gate brief)
└── SUSPENSION.md                               (this file)
```

## Declared Output Location

The root `SYNTHESIS.md` (declared output per the task prompt) will be produced at:
`taskflow/dags/chirp-logged-out-r7/SYNTHESIS.md`

This is the fold record that the synthesis child will author and use to call `engine_resume_suspended` to flip this parent `SUSPENDED → COMPLETED`.
