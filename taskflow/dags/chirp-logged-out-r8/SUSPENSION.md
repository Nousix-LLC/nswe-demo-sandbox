# SUSPENSION.md — chirp-logged-out-r8

**Status**: Suspended (NeedsDecompose)  
**Reason**: Decomposed into four child tasks forming a linear pipeline.  
**Resumption**: All child tasks must reach terminal state.

## Decomposition Summary

This root task was decomposed into the following pipeline:

```
SUBTASK_explore → SUBTASK_backend → SUBTASK_frontend → SUBTASK_synthesis
```

### SUBTASK_explore (Group 0, no dependencies)
Reads the existing codebase and design documents, designs the API and frontend structure, creates the git branch `work/chirp-logged-out`, and produces `analysis.md` for downstream tasks.

### SUBTASK_backend (Group 1, depends on SUBTASK_explore)
Implements public (unauthenticated) timeline and user profile API endpoints in chirp-server with integration tests. Commits to `work/chirp-logged-out`. Produces `backend_summary.md`.

### SUBTASK_frontend (Group 2, depends on SUBTASK_backend)
Implements the home/landing route (with loading/empty/error/end-of-list states), public user profile view, and sign-up/sign-in navigation in chirp-frontend using Ferric. Includes wasm-bindgen tests per state. Commits to `work/chirp-logged-out`. Produces `frontend_summary.md`.

### SUBTASK_synthesis (Group 3, depends on SUBTASK_frontend)
Verification gate: checks all five acceptance criteria against the combined implementation, verifies backend/frontend wiring, runs CI checks, creates the GitHub PR closing issue #35, and authors `SYNTHESIS.md` at this workspace root.

## Cut Rationale

Linear phase pipeline selected over parallel fan-out because:
- Backend and frontend committing to the same branch in parallel would create git merge conflicts
- Frontend builds against the actually-implemented backend (not just a contract document), making the sequential dependency correct
- Each child owns disjoint files: explore (no production files), backend (crates/chirp-server/), frontend (crates/chirp-frontend/), synthesis (GitHub PR + SYNTHESIS.md)

## Acceptance Criteria Traceability

Each AC maps to child tasks:

| AC | Addressed by |
|----|-------------|
| AC-1 (public access to timeline + profiles) | SUBTASK_backend (routes) + SUBTASK_frontend (routes without auth guard) |
| AC-2 (empty-state landing) | SUBTASK_frontend (empty state component) |
| AC-3 (error state) | SUBTASK_frontend (error state component) |
| AC-4 (sign-up navigation) | SUBTASK_frontend (navigation links) |
| AC-5 (four distinct states) | SUBTASK_frontend (loading/empty/error/end-of-list) |

Verification is owned by SUBTASK_synthesis (the gate).
