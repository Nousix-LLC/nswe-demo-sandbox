# COMPLETE — FIXTASK_frontend_contract

## Status: completed

## What was done

Fixed the wire-format mismatch between the backend's public API serialization and the
frontend's deserialization structs in `crates/chirp-frontend`.

### `crates/chirp-frontend/src/api.rs`
- Added `#[serde(rename_all = "camelCase")]` to all 6 public API structs:
  `PublicAuthor`, `PublicChirp`, `PublicTimelineResponse`, `PublicUserInfo`,
  `PublicUserChirp`, `PublicUserResponse`
- Changed `PublicChirp.id: String` → `pub id: u64`
- Changed `PublicChirp.created_at: String` → `pub created_at: i64` (ms epoch)
- Changed `PublicUserChirp.id: String` → `pub id: u64`
- Changed `PublicUserChirp.created_at: String` → `pub created_at: i64`

### `crates/chirp-frontend/src/landing.rs`
- `LandingModel.before_cursor: Option<String>` → `Option<i64>`
- `apply_initial` / `apply_more`: removed `.clone()` (i64 is Copy)
- `request_load`: added `let before_str = before.map(|ts| ts.to_string());` for query param conversion
- `chirp_item`: `.key(chirp.id.to_string())` and `.child(text(chirp.created_at.to_string()))`
- Updated `sample_chirp` test helper and all 71 test call sites to numeric types
- Updated cursor assertions: `assert_eq!(m.before_cursor, Some(1700000000000i64))`

### `crates/chirp-frontend/src/public_profile.rs`
- Same `before_cursor` type update and query-param conversion as landing.rs
- Updated `sample_chirp` test helper and all call sites to numeric types
- Updated cursor assertions

## Verification

- `cargo fmt --check -p chirp-frontend` ✅
- `cargo clippy -p chirp-frontend -- -D warnings` ✅
- `cargo test -p chirp-frontend` ✅ (71 passed, 0 failed)
- Commit `fed1fc8` on `work/chirp-logged-out`
- PR #263 remains open and updated

## Outputs

- `crates/chirp-frontend/src/api.rs`
- `crates/chirp-frontend/src/landing.rs`
- `crates/chirp-frontend/src/public_profile.rs`
