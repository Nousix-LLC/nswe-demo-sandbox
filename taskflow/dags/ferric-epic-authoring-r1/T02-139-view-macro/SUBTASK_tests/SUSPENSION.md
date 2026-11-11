# SUSPENSION.md — SUBTASK_tests

## Suspension Reason

NeedsDecompose: The brief explicitly enumerated two distinct concerns (native conformance
tests AND trybuild diagnostic fixtures), firing the Scope-Based trigger and the Distinct
Concerns Test. The work was split into two independent spokes plus a synthesis/commit gate.

## Decomposition

**Cut chosen:** 3 children — 2 independent spokes (conformance, trybuild) + 1 synthesis gate

| Child | Task ID | Depends on | Concern |
|-------|---------|------------|---------|
| SUBTASK_conformance | ferric-tests-conformance | none | Write tests/lowering.rs — native conformance tests for all §2.12 rows |
| SUBTASK_trybuild | ferric-tests-trybuild | none | Write trybuild runner + 7 fixtures + generate .stderr via SSH |
| SUBTASK_synthesis | ferric-tests-synthesis | conformance + trybuild | Verification gate + commit on work/ferric-epic-authoring-r1 |

## Resumption Condition

Resumes when all three child tasks (ferric-tests-conformance, ferric-tests-trybuild,
ferric-tests-synthesis) reach terminal lifecycle states. The fold is performed by
SUBTASK_synthesis writing SYNTHESIS.md at this workspace and calling engine_resume_suspended.

## Authored Named State

- `_GLOBAL.md` — subtree hub with context, task structure, contract declaration
- `contracts/_MANIFEST.yaml` — behavioral spec contract: ownership + identity assertions
- `SUBTASK_conformance/_BRIEF.md` — conformance spoke brief
- `SUBTASK_trybuild/_BRIEF.md` — trybuild spoke brief
- `SUBTASK_synthesis/_BRIEF.md` — synthesis/verification gate brief (task kind: synthesis)
