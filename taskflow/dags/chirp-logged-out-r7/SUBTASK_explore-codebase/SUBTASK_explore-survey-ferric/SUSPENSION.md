# Suspension Record — SUBTASK_explore-survey-ferric

**Task**: SUBTASK_explore-survey-ferric (Ferric Framework Primitives Survey)
**Status**: SUSPENDED (NeedsDecompose)
**Decompose Evaluation**: NeedsDecompose

## Decomposition Decision

The task brief explicitly enumerates 6 distinct areas from 3 separate PRs:
1. Crate Structure
2. Async Resource Primitives (PR #193)
3. Router API (PR #203)
4. SSR and Hydration (PR #228)
5. Component Pattern
6. Gaps or Limitations

The enumerated-concerns rule fires by enumeration alone. PRs #193, #203, and #228 introduced distinct API surfaces that different specialists could survey in parallel. Output size is expected to exceed 400 lines. The asymmetric decomposition bias applies.

## Children Materialized

| Task | Slug | Depends on |
|------|------|-----------|
| Ferric Async Survey | `SUBTASK_ferric-async-survey` | none |
| Ferric Router Survey | `SUBTASK_ferric-router-survey` | none |
| Ferric SSR Survey | `SUBTASK_ferric-ssr-survey` | none |
| Ferric Survey Synthesis | `SUBTASK_ferric-survey-synthesis` | SUBTASK_ferric-async-survey, SUBTASK_ferric-router-survey, SUBTASK_ferric-ssr-survey |

## Resumption Condition

All four child tasks must reach terminal lifecycle state. The synthesis task (`SUBTASK_ferric-survey-synthesis`) folds this task SUSPENDED → COMPLETED by writing `SYNTHESIS.md` and calling `engine_resume_suspended`.

## Authored Subtree Files

- `_GLOBAL.md` — subtree hub
- `contracts/_MANIFEST.yaml` — contract ownership manifest
- `contracts/notes-schema.yaml` — schema for spoke notes output format
- `SUBTASK_ferric-async-survey/_BRIEF.md`
- `SUBTASK_ferric-router-survey/_BRIEF.md`
- `SUBTASK_ferric-ssr-survey/_BRIEF.md`
- `SUBTASK_ferric-survey-synthesis/_BRIEF.md`
