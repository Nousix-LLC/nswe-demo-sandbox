# SUSPENSION.md — chirp-logged-out

**Status:** Suspended — NeedsDecompose  
**Suspended at:** 2026-11-06

## What was done

Explored the codebase to identify the gap between the logged-out visitor requirements (issue #35) and the current server and frontend code:

- `GET /api/timeline` requires `AuthUser` → HTTP 401 for unauthenticated callers.
- `ChirpRepository::timeline` requires a `viewer: UserId`.
- The frontend `ApiClient` calls `GET /api/timeline` unconditionally.
- `GET /api/users/{id}` is already unauthenticated — no change needed there.
- The `TimelineModel` state machine already models all four states; the render path may not make all four visually distinct.

## Decomposition

Three child tasks have been materialized:

1. **SUBTASK_server_public_timeline** — Add `GET /api/public/timeline` unauthenticated endpoint, `public_timeline` trait method, both repository implementations, handler, router wiring, and integration tests.

2. **SUBTASK_frontend_logged_out** — Add `ApiClient::public_timeline`, update timeline view to call it for logged-out sessions, make all four states visually distinct, add sign-up/sign-in navigation. Depends on `SUBTASK_server_public_timeline`.

3. **SUBTASK_synthesis** — Verify CI on `work/chirp-logged-out`, confirm all five acceptance criteria, open the PR closing issue #35, write `SYNTHESIS.md`. Depends on `SUBTASK_frontend_logged_out`.

## Resumption

This task resumes when all three child tasks have reached terminal COMPLETED state and the observation seam `taskflow/dags/chirp-logged-out/SYNTHESIS.md` has been authored by `SUBTASK_synthesis`.
