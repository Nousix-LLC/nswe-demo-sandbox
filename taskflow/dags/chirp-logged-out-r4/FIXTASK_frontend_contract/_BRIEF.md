# Task: Fix — Frontend Public API Struct Wire Format Mismatch

## Task Specification

**Slug**: FIXTASK_frontend_contract  
**Task Kind**: fix  
**Injected By**: SUBTASK_synthesis (Check 2 contract violation)  
**Depends on**: SUBTASK_synthesis (this fix-task is unblocked once synthesis completes)  
**Branch**: `work/chirp-logged-out`  
**Repository**: `Nousix-LLC/nswe-demo`

---

## Problem Statement

The synthesis gate (Check 2 — Contract Verification) identified a wire-format mismatch between
the backend's public API serialization and the frontend's deserialization structs in
`crates/chirp-frontend/src/api.rs`.

### Root Cause

The backend DTOs in `crates/chirp-types/src/api.rs` are annotated with
`#[serde(rename_all = "camelCase")]` and use integer types for opaque IDs and timestamps
(consistent with all other chirp-types DTOs). The frontend was written against the frozen
API spec (`contracts/public_api_spec.md`), which described `id` as "string (UUID)" and
`created_at` as "string (ISO 8601)". The backend deviations from the spec were documented
in `SUBTASK_backend/COMPLETE.md` but were not propagated to the frontend.

### Specific Mismatches

| JSON field sent by backend | Backend Rust type | Frontend expects | Issue |
|---------------------------|-------------------|-----------------|-------|
| `id` (number) | `u64` (`ChirpId`) | `String` | Type mismatch — serde cannot coerce JSON number to String |
| `createdAt` (number) | `i64` (ms epoch) | field `created_at: String` | Key name + type both wrong |
| `likeCount` (number) | `u64` | field `like_count: u64` | Key name mismatch |
| `hasMore` (bool) | `bool` | field `has_more: bool` | Key name mismatch |
| `displayName` (string/null) | `Option<String>` | field `display_name` | Key name mismatch |
| `chirpCount` (number) | `u64` | field `chirp_count: u64` | Key name mismatch |

The frontend would receive a serde deserialization error for every API response, causing the
error state to render immediately on every page load — the feature does not work at runtime.

---

## Objective

Update `crates/chirp-frontend/src/api.rs` (and dependent view modules) so the frontend's
public API structs correctly deserialize the backend's actual JSON wire format.

---

## Required Changes

### 1. `crates/chirp-frontend/src/api.rs`

For the five public-API structs (`PublicAuthor`, `PublicChirp`, `PublicTimelineResponse`,
`PublicUserInfo`, `PublicUserChirp`, `PublicUserResponse`):

- Add `#[serde(rename_all = "camelCase")]` to each struct
- Change `PublicChirp.id: String` → `id: u64`
- Change `PublicChirp.created_at: String` → `created_at: i64` (ms since Unix epoch)
- Change `PublicUserChirp.id: String` → `id: u64`
- Change `PublicUserChirp.created_at: String` → `created_at: i64`

### 2. `crates/chirp-frontend/src/landing.rs`

- Update `LandingModel.before_cursor: Option<String>` → `Option<i64>`
- Update any display formatting of `created_at` timestamps (format i64 ms as a display string;
  use JavaScript's `Date` API in the WASM context, or format as a plain number if no display
  format exists yet)
- Update tests that construct `PublicChirp` or `PublicTimelineResponse` with hardcoded values

### 3. `crates/chirp-frontend/src/public_profile.rs`

- Same `before_cursor` type update as landing.rs if used
- Update tests that construct `PublicUserChirp` or `PublicUserResponse` with hardcoded values

### 4. Update existing tests

All existing tests in `landing::tests` and `public_profile::tests` that construct
`PublicChirp`, `PublicUserChirp`, `PublicTimelineResponse`, or `PublicUserResponse` with
`id: "some-uuid".to_string()` or `created_at: "2024-...".to_string()` must be updated to
use `id: 1u64` (or similar numeric value) and `created_at: 1700000000000i64`.

---

## Success Criteria

- [ ] `cargo fmt --check -p chirp-frontend` passes
- [ ] `cargo clippy -p chirp-frontend -- -D warnings` passes  
- [ ] `cargo test -p chirp-frontend` passes (all existing + updated tests)
- [ ] The frontend can deserialize a `PublicTimelineResponse` JSON produced by the backend's
  `public_chirps` handler without serde errors (can be verified by a round-trip test)
- [ ] `before_cursor` correctly stores the `created_at` i64 value and passes it as a numeric
  string in the `?before=<ms>` query parameter

## Output

- Modified `crates/chirp-frontend/src/api.rs`
- Modified `crates/chirp-frontend/src/landing.rs`
- Modified `crates/chirp-frontend/src/public_profile.rs`
- Commit on `work/chirp-logged-out`
- PR #263 (already open) is updated/still open

## Inherited Constraints

- Branch: `work/chirp-logged-out`
- No host paths, internal addresses, or taskflow references in git commits or GitHub posts
- No force-push to main
- If the fix introduces additional issues, document them and do not block

## Reference Files

- `crates/chirp-frontend/src/api.rs` — structs to fix
- `crates/chirp-frontend/src/landing.rs` — dependent view + tests
- `crates/chirp-frontend/src/public_profile.rs` — dependent view + tests
- `crates/chirp-types/src/api.rs` — backend DTOs (ground truth for wire format)
- `taskflow/dags/chirp-logged-out-r4/SUBTASK_backend/COMPLETE.md` — documents backend deviations
