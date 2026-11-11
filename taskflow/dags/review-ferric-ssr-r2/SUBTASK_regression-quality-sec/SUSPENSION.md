# Suspension Record: SUBTASK_regression-quality-sec

**Status**: SUSPENDED — NeedsDecompose
**Suspended at**: 2026-11-06

## Decomposition Summary

This task was too broad for a single node (four distinct concerns: regression check,
code quality, security, and synthesis). The scope triggers fired; NeedsDecompose declared.

The task has been decomposed into four child tasks:

| Child task | Depends on | Output |
|---|---|---|
| `SUBTASK_regression-check` | none | `regression-check.md` |
| `SUBTASK_code-quality` | none | `code-quality.md` |
| `SUBTASK_security` | none | `security.md` |
| `SUBTASK_synthesis` | regression-check, code-quality, security | `verdict-regression-quality-sec.md`, `SYNTHESIS.md` |

## Resumption Condition

This task resumes when `SUBTASK_synthesis` completes and calls `engine_resume_suspended`
with the fold record at `SYNTHESIS.md` (this workspace).

The synthesis child is responsible for:
- Writing `verdict-regression-quality-sec.md` (the declared output of this task)
- Writing `SYNTHESIS.md` (the fold record at this workspace)
- Calling `engine_resume_suspended` to fold this task SUSPENDED→COMPLETED

## Authored Artifacts

- `_GLOBAL.md` — subtree hub
- `contracts/_MANIFEST.yaml` — ownership manifest
- `SUBTASK_regression-check/_BRIEF.md`
- `SUBTASK_code-quality/_BRIEF.md`
- `SUBTASK_security/_BRIEF.md`
- `SUBTASK_synthesis/_BRIEF.md`
