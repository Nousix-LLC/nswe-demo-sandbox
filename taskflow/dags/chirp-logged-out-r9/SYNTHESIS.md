# Synthesis — chirp-logged-out-r9

**Status: PASS**

## Summary

All acceptance criteria for issue #35 (logged-out visitor experience) are fully implemented and CI is clean on branch `work/chirp-logged-out` (PR #263). No new code was required in this r9 attempt — r8 commits had already resolved both the CI wasm blocker and all feature work. This synthesis confirms the implementation is complete and green.

## What Was Implemented (by prior r8 commits)

### AC-1: Public timeline at root URL (`/`)
- `crates/chirp-frontend/src/app.rs`: Route `/` maps to `landing_view` with no authentication guard.
- `crates/chirp-frontend/src/landing.rs`: Full public timeline implementation loading `GET /api/chirps`. Uses `LandingModel` state machine (loading, loaded, paginating, error). Pagination via ISO 8601 `before` cursor. No login redirect at any state.

### AC-2: Public user profile pages (`/@:username`)
- `app.rs` route `/@:handle` maps to `public_profile_view`. Served without authentication.

### AC-3: Accurate landing states
- Authenticated users routing to `/` get the public timeline (or redirect to `/timeline` based on `AppContext.session`).
- Unauthenticated visitors land on the public timeline directly.

### AC-4: Sign-in / sign-up links visible for logged-out visitors
- `landing.rs` renders sign-in and sign-up nav links in all states (loaded, loading_more, error), satisfying the requirement that unauthenticated visitors always see the auth entry points.

### AC-5: No regression in authenticated flows
- Authenticated routes (`/compose`, `/user/:id`, `/timeline`) remain intact in the route table with their existing guards.

### CI Wasm Blocker (resolved by r8)
- Commit `2615ba1` ("fix(ferric): update hydrate.rs for new EventHandler enum and full EventKind set") resolved the previously-cited non-exhaustive `EventKind` match. The `EventKind` enum in `crates/ferric/src/vdom.rs` has 48 variants; `dom.rs` and `hydrate.rs` both carry exhaustive `event_name()` / `stash_key()` coverage. Local builds confirmed clean.

### Server-side public API
- `GET /api/chirps` and `GET /api/public/timeline` — both unauthenticated — implemented in `crates/chirp-server/src/api/handlers.rs` with backing queries in both `postgres.rs` and `in_memory.rs`.

### Test coverage
- 76 unit tests in `chirp-frontend` (landing state machine + view tree).
- 65 + 26 + 1 + 5 tests in `chirp-server`.

## CI Result

All 6 required checks on PR #263 — **SUCCESS** as of 2026-11-06T07:55:48Z.

| Check   | Status  |
|---------|---------|
| fmt     | ✅ SUCCESS |
| clippy  | ✅ SUCCESS |
| test    | ✅ SUCCESS |
| wasm    | ✅ SUCCESS |
| doc     | ✅ SUCCESS |
| image   | ✅ SUCCESS |

## Remaining Blockers

None. The branch is ready for merge.
