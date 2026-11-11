# SUSPENSION — spoke-correctness

**Status**: Suspended / NeedsDecompose
**Suspended at**: 2026-11-06

## Why suspended

The two concerns assigned to this node (concern 3: SQL correctness; concern 4: spec
deviation) span distinct source files and analysis types. The enumerated-concerns
decomposition trigger fired: NeedsDecompose.

## Subtree materialized

Three children registered via `amend_plan { add_task }`:

| Child id | Depends on | Description | Output |
|----------|------------|-------------|--------|
| `SUBTASK_sql-correctness` | none | SQL semantic correctness — concern 3 | `SUBTASK_sql-correctness/FINDINGS.md` |
| `SUBTASK_spec-deviation` | none | Spec deviation — concern 4 | `SUBTASK_spec-deviation/FINDINGS.md` |
| `SUBTASK_synthesis` | both above | Merge into final FINDINGS.md | `FINDINGS.md` |

Hub document: `_GLOBAL.md`
Contract manifest: `contracts/_MANIFEST.yaml`

## Resumption

This node resumes when `SUBTASK_synthesis` reaches COMPLETED and has written
`FINDINGS.md` at the spoke-correctness workspace level.
