# SUSPENSION — SUBTASK_hydration

**Status**: Suspended (NeedsDecompose)
**Suspended at**: 2026-11-05

## Decomposition Summary

SUBTASK_hydration was decomposed into five children because the brief enumerates four distinct
acceptance criteria (REQ-HYD-001–004) covering different behavioral properties of hydrate():

- **REQ-HYD-001**: DOM walking strategy (querySelector vs appendChild)
- **REQ-HYD-002**: Signal propagation post-hydration
- **REQ-HYD-003**: WASM entry point and integration test coverage
- **REQ-HYD-004**: Marker schema consistency (critical cross-check for synthesis)

These four criteria are distinct enough for the Scope/Distinct-Concerns triggers to fire under the
Task Decomposition Framework; a reviewer examining DOM manipulation strategy (001) is doing
different analysis from one examining marker schema format (004), and both could proceed in parallel.

## Children Materialized

| Task id | Responsibility | Output |
|---------|----------------|--------|
| SUBTASK_hyd001 | REQ-HYD-001: DOM walk | criterion_001.md |
| SUBTASK_hyd002 | REQ-HYD-002: Signal propagation | criterion_002.md |
| SUBTASK_hyd003 | REQ-HYD-003: WASM entry point | criterion_003.md |
| SUBTASK_hyd004 | REQ-HYD-004: Marker schema | criterion_004.md |
| SUBTASK_hyd_synthesis | Verification gate + fold | ../hydration_findings.md, ../SYNTHESIS.md |

## Resumption Condition

This task resumes (SUSPENDED → COMPLETED via fold) when SUBTASK_hyd_synthesis completes and
calls `engine_resume_suspended` with `seam_path = ../SYNTHESIS.md`.

## Named State Authored

- `_GLOBAL.md` — subtree hub (this workspace)
- `SUBTASK_hyd001/_BRIEF.md`
- `SUBTASK_hyd002/_BRIEF.md`
- `SUBTASK_hyd003/_BRIEF.md`
- `SUBTASK_hyd004/_BRIEF.md`
- `SUBTASK_hyd_synthesis/_BRIEF.md`
- `SUSPENSION.md` (this file)
