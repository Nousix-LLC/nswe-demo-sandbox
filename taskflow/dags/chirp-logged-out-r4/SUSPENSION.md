# SUSPENSION — chirp-logged-out-r4

## Status: Suspended — NeedsDecompose

This task has decomposed its work into four child tasks and is suspended pending their
completion.

## Decomposition Shape

Contract-first fan-out: exploration gates parallel backend+frontend spokes, synthesis gate
verifies and commits.

| Task ID | Slug | Depends On | Workspace |
|---------|------|-----------|-----------|
| chirp-logged-out-r4-explore | SUBTASK_explore_and_setup | none | taskflow/dags/chirp-logged-out-r4/SUBTASK_explore_and_setup |
| chirp-logged-out-r4-backend | SUBTASK_backend | chirp-logged-out-r4-explore | taskflow/dags/chirp-logged-out-r4/SUBTASK_backend |
| chirp-logged-out-r4-frontend | SUBTASK_frontend | chirp-logged-out-r4-explore | taskflow/dags/chirp-logged-out-r4/SUBTASK_frontend |
| chirp-logged-out-r4-synthesis | SUBTASK_synthesis | chirp-logged-out-r4-backend, chirp-logged-out-r4-frontend | taskflow/dags/chirp-logged-out-r4/SUBTASK_synthesis |

## Contracts authored

- `taskflow/dags/chirp-logged-out-r4/_GLOBAL.md` — hub document
- `taskflow/dags/chirp-logged-out-r4/contracts/public_api_spec.md` — frozen JSON API spec
- `taskflow/dags/chirp-logged-out-r4/contracts/_MANIFEST.yaml` — ownership manifest

## Resumption condition

This task resumes when the synthesis child (`chirp-logged-out-r4-synthesis`) completes and
calls `engine_resume_suspended` with:
- `target_task_id: proc-770f650d-3782-4eff-b33e-d8ca8b09f602`
- `seam_path: taskflow/dags/chirp-logged-out-r4/SYNTHESIS.md`

The fold record is `taskflow/dags/chirp-logged-out-r4/SYNTHESIS.md`.
