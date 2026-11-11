# SUBTASK_code_quality — Suspended (NeedsDecompose)

## Status

Suspended pending subtree completion.

## Decomposition Summary

This node decomposed its five concern areas into three parallel analysis spokes and one synthesis task:

| Child | Concerns | Output |
|-------|----------|--------|
| `SUBTASK_format_check` | 1 (structural coherence), 4 (formatting consistency) | `SUBTASK_format_check/format_review_partial.md` |
| `SUBTASK_placement_check` | 2 (placement correctness), 3 (duplication) | `SUBTASK_placement_check/placement_review_partial.md` |
| `SUBTASK_completeness_check` | 5 (documentation completeness as API contract) | `SUBTASK_completeness_check/completeness_review_partial.md` |
| `SUBTASK_synthesis` | Merge partials → final findings | `code_quality_findings.md` (this workspace root) |

## Resumption Condition

This node resumes when all four child tasks reach terminal states and `code_quality_findings.md` is present at this workspace root.

## Named-State Authored

- `_GLOBAL.md` — subtree hub
- `contracts/_MANIFEST.yaml` — ownership manifest and identities
- `contracts/spoke_partial_schema.yaml` — intermediate findings format for spoke tasks
- `SUBTASK_format_check/_BRIEF.md`
- `SUBTASK_placement_check/_BRIEF.md`
- `SUBTASK_completeness_check/_BRIEF.md`
- `SUBTASK_synthesis/_BRIEF.md`
