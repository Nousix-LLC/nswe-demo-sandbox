# COMPLETE — SUBTASK_server_analysis

**Task**: chirp-server API Surface Analysis  
**Status**: completed  
**Output**: `server_findings.md`

## Summary

Read the full chirp-server source (`crates/chirp-server/src/`) and `contracts/public_api_spec.md`.
Produced `server_findings.md` with all required sections.

### Key findings

**Router registration file**: `crates/chirp-server/src/api/router.rs` — `build_router(state: AppState) -> Router`

**Auth extractor type name**: `AuthUser` (defined in `crates/chirp-server/src/api/auth.rs`).  
No optional auth extractor (`OptionalAuthUser`) exists — public endpoints simply omit the `AuthUser` parameter.

**API spec verdict**:
- `GET /api/chirps` (public timeline) → **CONFLICT**: existing public timeline is at `GET /api/public/timeline`
  with a different response shape (`items`/`nextCursor` vs spec's `chirps`/`has_more`, author as `authorId`
  integer vs embedded `{username, display_name}`, `cursor` vs `before` pagination param).
- `GET /api/users/:username/chirps` (user profile) → **ABSENT**: nothing similar exists; the existing
  `GET /api/users/{id}` is by integer id and returns a user profile only (no chirps, no pagination).
- Pagination `before`/`has_more` → **INCONSISTENT**: existing uses opaque `cursor`/`nextCursor`.

Recommendation: add both spec endpoints as new routes (keeping existing routes unchanged); add new
response DTOs to `chirp-types`; add a new repository trait method for username-based user chirp lookup.
