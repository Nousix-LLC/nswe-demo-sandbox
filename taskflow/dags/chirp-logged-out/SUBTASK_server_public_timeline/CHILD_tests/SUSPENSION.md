# SUSPENSION — CHILD_tests

## Status

SUSPENDED (NeedsDecompose)

## Decomposition

CHILD_tests decomposed into two serial children:

| Child | Slug | Depends on | Purpose |
|-------|------|------------|---------|
| Write tests | `CHILD_write_tests` | none | Add `public_timeline` stub to `UnhealthyStore` + write 4 integration test cases; commit |
| CI verify | `CHILD_ci_verify` | `CHILD_write_tests` | Run cargo fmt/clippy/test; fix any issues; author COMPLETE.md records; fold SUSPENDED parent |

## Decomposition rationale

The brief enumerated two distinct concerns:
1. Integration tests (writing test code — creative/domain work)
2. CI verification (running tools, potentially fixing formatting/lint from prior commits — mechanical/quality work)

The scope-based trigger fired by explicit enumeration. These are distinct areas of work with a natural sequential dependency (CI verification can only run after tests are written).

## Resumption condition

CHILD_tests resumes (and becomes COMPLETED via synthesis fold) when CHILD_ci_verify completes and calls `engine_resume_suspended` with `seam_path: .../CHILD_tests/SYNTHESIS.md`.

## Children materialized

- `CHILD_write_tests` workspace: `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/CHILD_write_tests/`
- `CHILD_ci_verify` workspace: `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/CHILD_tests/CHILD_ci_verify/`
