# SUSPENSION — SUBTASK_explore-codebase

**Status**: SUSPENDED — NeedsDecompose  
**Suspended at**: 2026-11-05  
**Task**: SUBTASK_explore-codebase  
**Resumption**: This task resumes when the synthesis child (SUBTASK_explore-synthesis) folds it via `engine_resume_suspended`. The fold fires after all five children reach their terminal states and SUBTASK_explore-synthesis writes `analysis.md` and `SYNTHESIS.md` at this workspace root.

---

## Decomposition Record

This task was evaluated as `NeedsDecompose`. The evaluation fired on the **Enumerated-Concerns Rule**: the brief explicitly names four distinct analysis areas (API endpoint survey, frontend route survey, Ferric primitives survey, design docs / per-AC gap analysis), each spanning a different input corpus with no shared source. These are genuinely distinct concerns that cannot be collapsed without violating single-responsibility; they also enable full parallelism.

**Cut selected**: Candidate A — by source/component (parallel spokes by codebase). Each survey child reads a disjoint corpus. The synthesis child reads the four survey outputs and folds the parent.

---

## Children Materialized

| Slug | Depends On | Output |
|------|-----------|--------|
| SUBTASK_explore-survey-design | none | `SUBTASK_explore-survey-design/design-survey.md` |
| SUBTASK_explore-survey-backend | none | `SUBTASK_explore-survey-backend/backend-survey.md` |
| SUBTASK_explore-survey-frontend | none | `SUBTASK_explore-survey-frontend/frontend-survey.md` |
| SUBTASK_explore-survey-ferric | none | `SUBTASK_explore-survey-ferric/ferric-survey.md` |
| SUBTASK_explore-synthesis | all 4 above | `analysis.md`, `SYNTHESIS.md` (at this workspace root) |

The four survey children run concurrently (no inter-dependencies). SUBTASK_explore-synthesis depends on all four.

---

## Resumption Condition

This task un-suspends when SUBTASK_explore-synthesis calls:
```
engine_resume_suspended {
  target_task_id: SUBTASK_explore-codebase,
  synthesized_task_id: SUBTASK_explore-synthesis,
  seam_path: <absolute path to SYNTHESIS.md at this workspace root>
}
```
after successfully writing `analysis.md` and `SYNTHESIS.md` at this workspace root (`SUBTASK_explore-codebase/`).

---

## Declared Output Location

`analysis.md` — at this workspace root (`SUBTASK_explore-codebase/analysis.md`).  
This is the input consumed by SUBTASK_backend-api.
