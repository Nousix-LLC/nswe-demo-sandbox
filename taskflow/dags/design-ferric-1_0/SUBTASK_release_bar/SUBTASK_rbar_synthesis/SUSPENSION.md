# SUSPENSION.md — SUBTASK_rbar_synthesis

**Status**: SUSPENDED / NeedsDecompose

## Why this task decomposed

The brief for SUBTASK_rbar_synthesis explicitly names three distinct concerns under the heading "Distinct concerns":
1. Framework surface gap review
2. BAR-FERRIC-* criteria and staging
3. Assembly and verification

By the TDF enumerated-concerns rule, the Scope-Based trigger fires when a brief enumerates two or more distinct
concerns, themes, or analyses. The scope trigger fires here; per trigger precedence ("if ANY trigger fires, the
task is not atomic"), the task is NeedsDecompose.

## Subtree materialized

### Actual DAG structure (two concurrent tasks)

| Task | Depends on | Output |
|------|-----------|--------|
| `SUBTASK_rbar_gap` | none (spokes already complete) | `gap-analysis-internal.md` |
| `SUBTASK_rbar_assembly` (synthesis) | none (concurrent with rbar_gap; reads sibling's gap analysis) | `../../release-bar.md`, `../../SYNTHESIS.md`, `../SYNTHESIS.md` |

### Why not three sequential tasks

The original design was a three-task serial pipeline: rbar_gap → rbar_criteria → rbar_assembly. The engine
rejected a dependency from rbar_criteria onto rbar_gap as "cycle detected in recompute_execution_groups."
This is the same constraint the parent SUBTASK_release_bar documented when deciding to collapse the chain
into a single SUBTASK_rbar_synthesis node: a sequential chain under a group-1 node pushes the synthesis
task into a group that conflicts with the parent's group assignment.

Resolution: rbar_gap and rbar_assembly run concurrently. rbar_assembly uses the sibling
`SUBTASK_rbar_gap_review/gap-analysis.md` (already COMPLETE) as primary input, reads
`SUBTASK_rbar_gap/gap-analysis-internal.md` as a cross-check if available, and incorporates the
BAR-FERRIC-* criteria work originally scoped to SUBTASK_rbar_criteria. `SUBTASK_rbar_criteria/_BRIEF.md`
is retained on disk as a design artifact documenting format and staging; it is not a DAG node.

## Resumption condition

Both SUBTASK_rbar_gap and SUBTASK_rbar_assembly reach terminal states. SUBTASK_rbar_assembly writes the
fold records and calls `engine_resume_suspended` for both SUBTASK_release_bar and SUBTASK_rbar_synthesis.

## Files authored in this invocation

- `_GLOBAL.md` — subtree hub
- `contracts/_MANIFEST.yaml` — seam contract
- `SUBTASK_rbar_gap/_BRIEF.md`
- `SUBTASK_rbar_criteria/_BRIEF.md` — design reference, not a DAG node
- `SUBTASK_rbar_assembly/_BRIEF.md`
- `SUSPENSION.md` (this file)
