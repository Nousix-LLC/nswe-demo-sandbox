# SUSPENSION — review-chirp-logged-out-r2

**Status**: Suspended / NeedsDecompose  
**Suspended at**: 2026-11-06

## Decomposition

Three child tasks registered via `amend_plan`. The parent suspends here awaiting their completion.

| Task id | Depends on | Output |
|---------|------------|--------|
| `SUBTASK_verify-fixes` | none | `SUBTASK_verify-fixes/findings-fixes.md` |
| `SUBTASK_verify-acs` | none | `SUBTASK_verify-acs/findings-acs.md` |
| `SUBTASK_synthesis` | `SUBTASK_verify-fixes`, `SUBTASK_verify-acs` | `SYNTHESIS.md` (observation seam) |

## Resumption condition

This task resumes when the child subtree reaches terminal states — specifically when `SUBTASK_synthesis` completes and writes the root `SYNTHESIS.md` at `taskflow/dags/review-chirp-logged-out-r2/SYNTHESIS.md`. The synthesis task calls `engine_resume_suspended` to fold this parent at that point.

## Authored artifacts

- `_GLOBAL.md` — hub document with PR metadata, ACs, task structure, constraints
- `contracts/_MANIFEST.yaml` — taxonomy contract with required verdict fields and identity assertions
- `SUBTASK_verify-fixes/_BRIEF.md` — fix correctness, quality, tests, security, regression
- `SUBTASK_verify-acs/_BRIEF.md` — AC-1 through AC-5 re-verification
- `SUBTASK_synthesis/_BRIEF.md` — verification gate, verdict, GitHub post, SYNTHESIS.md
