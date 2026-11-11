# Backend Verification — AC-5

## Summary

Overall verdict: PASS

Both `GET /api/chirps` and `GET /api/users/:username/chirps` are registered in the router,
implemented without any authentication guard, and return the correct response shapes. CI passes
(all 6/6 checks) on branch HEAD `617f2539`. No code fixes were required.

---

## AC-5: Backend routes serve public chirps without auth

verdict: PASS

evidence:
- `crates/chirp-server/src/api/router.rs` — both routes registered:
  - `.route("/api/chirps", get(handlers::public_chirps).post(handlers::create_chirp))` (line ~85)
  - `.route("/api/users/{username}/chirps", get(handlers::user_chirps))` (line ~84)
- `crates/chirp-server/src/api/handlers.rs` — `public_chirps` handler signature:
  ```rust
  pub async fn public_chirps(
      State(state): State<AppState>,
      Query(query): Query<PublicTimelineQuery>,
  ) -> Result<Json<PublicTimelineResponse>, ServerError>
  ```
  No `AuthUser` extractor → no auth required. Returns `PublicTimelineResponse` with embedded
  author info (username, display_name, created_at, like_count) per chirp.
- `crates/chirp-server/src/api/handlers.rs` — `user_chirps` handler signature:
  ```rust
  pub async fn user_chirps(
      State(state): State<AppState>,
      Path(username): Path<String>,
      Query(query): Query<PublicTimelineQuery>,
  ) -> Result<Json<PublicUserResponse>, ServerError>
  ```
  No `AuthUser` extractor → no auth required. Returns `PublicUserResponse` with user profile
  and reverse-chronological chirp list.
- `crates/chirp-server/src/api/auth.rs` — confirms `AuthUser` is the sole auth enforcement
  mechanism (FromRequestParts extractor; rejects with 401 when absent/invalid). Handlers
  omitting `AuthUser` from their argument list receive no auth enforcement.
- Handler unit tests (`handlers.rs` #[cfg(test)]):
  - `public_chirps_returns_200_without_auth_and_empty_timeline` — calls `public_chirps`
    without `AuthUser`, asserts success
  - `user_chirps_returns_200_for_existing_user_with_no_chirps` — calls `user_chirps`
    without `AuthUser`, asserts 200 with correct profile
  - `user_chirps_returns_404_for_missing_user` — confirms 404 (not 401) for unknown user
- CI run on `617f25395eebe9475f19a90e0b1dac5921215ea3` (branch HEAD): all 6/6 checks pass
  (clippy, doc, fmt, image, test, wasm).
- Live smoke test note: `GET /api/chirps` returns 405 against the live cluster because the
  cluster (ArgoCD `targetRevision: main`) runs the `main` branch image (`cb1ced3`), which
  predates the logged-out feature. This is expected for an open, unmerged PR — not a code gap.

blockers: none

## Commits

None — no changes were needed. The branch code fully satisfies AC-5.
