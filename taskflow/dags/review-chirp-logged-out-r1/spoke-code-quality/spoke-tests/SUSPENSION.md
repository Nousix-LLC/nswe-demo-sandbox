# Suspension Record — spoke-tests

## Reason

`spoke-tests` decomposed into 4 child tasks (3 analysis spokes + 1 synthesis gate) because
the brief enumerates 3 distinct concerns across 3 different test files and test layers, firing
the scope/enumerated-concerns trigger. Each concern is an independent analysis that could be
done by a different specialist in parallel.

## Children Materialized

| Task id | Concerns | Depends on |
|---------|----------|------------|
| `SUBTASK_handler-unit-tests` | 1 (handler unit tests) | none |
| `SUBTASK_integration-tests` | 2 (integration test depth) | none |
| `SUBTASK_frontend-test-validity` | 5 (frontend test validity) | none |
| `SUBTASK_synthesis` | 1, 2, 5 (gate + assembly) | all 3 above |

## Resumption Condition

All 4 child tasks reach terminal lifecycle states, with `SUBTASK_synthesis` having produced
`FINDINGS.md` at `spoke-tests/FINDINGS.md` per `../contracts/findings_schema.md`.

## Named State Authored

- `_GLOBAL.md` — subtree hub document
- `contracts/_MANIFEST.yaml` — ownership and identities for this decomposition level
- `contracts/analysis_schema.md` — intermediate analysis output schema for child tasks
- `SUBTASK_handler-unit-tests/_BRIEF.md` — concern 1 analysis brief
- `SUBTASK_integration-tests/_BRIEF.md` — concern 2 analysis brief
- `SUBTASK_frontend-test-validity/_BRIEF.md` — concern 5 analysis brief
- `SUBTASK_synthesis/_BRIEF.md` — synthesis gate brief
