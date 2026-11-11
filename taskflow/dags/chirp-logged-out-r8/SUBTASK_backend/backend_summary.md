# Backend Public API Endpoints — Summary

## Status

Implementation was **already complete** on `work/chirp-logged-out` prior to this task
executing. The branch commit `eaf96cf` ("feat(chirp-server): add public GET /api/chirps
and GET /api/users/:username/chirps") carries the full backend deliverable. This task
verified correctness, ran CI, and documents the as-built contract.

---

## Routes Added

| Method | Path | Auth Required | Handler | Notes |
|--------|------|:---:|---------|-------|
| `GET` | `/api/chirps` | No | `public_chirps` | Public timeline, embedded author, paginated |
| `GET` | `/api/users/{username}/chirps` | No | `user_chirps` | Public user profile + chirps, 404 on missing user |

The `GET /api/chirps` route is registered on the same path as `POST /api/chirps` (which
remains auth-required). The router registers them as `get(handlers::public_chirps).post(handlers::create_chirp)`,
so the authenticated `POST` route is not affected.

Authentication bypass pattern: neither handler takes an `AuthUser` extractor parameter.
No middleware layering change was required — the `AuthUser` extractor is opt-in at the
handler signature level.

---

## Response Shapes (Rust types)

All types in `crates/chirp-types/src/api.rs`, serialized as camelCase JSON.

### `GET /api/chirps` — Public Timeline

**Query parameters** (`PublicTimelineQuery`):
```
before: Option<i64>   // ms-since-epoch of last seen chirp (pagination cursor); omit for first page
limit:  Option<u32>   // 1–50, default 20
```

**Response** (`PublicTimelineResponse`):
```rust
PublicTimelineResponse {
    chirps:   Vec<PublicChirp>,  // reverse-chronological
    has_more: bool,              // true when more pages exist
}

PublicChirp {
    id:         ChirpId,       // server-assigned integer
    content:    String,        // chirp body text
    author:     PublicAuthor,  // embedded author info
    created_at: i64,           // ms since Unix epoch
    like_count: u64,
}

PublicAuthor {
    username:     String,         // unique handle
    display_name: Option<String>, // null when unset
}
```

**Example JSON**:
```json
{
  "chirps": [
    {
      "id": 42,
      "content": "Hello world",
      "author": { "username": "alice", "displayName": "Alice" },
      "createdAt": 1700000000000,
      "likeCount": 3
    }
  ],
  "hasMore": false
}
```

---

### `GET /api/users/{username}/chirps` — Public User Profile

**Path parameter**: `username` (case-insensitive lookup)

**Query parameters**: same `PublicTimelineQuery` as above

**Response** (`PublicUserResponse`):
```rust
PublicUserResponse {
    user:     PublicUserProfile,   // user's public profile
    chirps:   Vec<PublicUserChirp>, // reverse-chronological
    has_more: bool,
}

PublicUserProfile {
    username:     String,         // unique handle
    display_name: Option<String>, // null when unset
    bio:          Option<String>, // null when unset
    chirp_count:  u64,            // total chirp count (all pages)
}

PublicUserChirp {
    id:         ChirpId,  // server-assigned integer
    content:    String,
    created_at: i64,      // ms since Unix epoch
    like_count: u64,
}
```

**404 response**: returns HTTP 404 when no user has the given username.

**Example JSON**:
```json
{
  "user": {
    "username": "alice",
    "displayName": "Alice",
    "bio": "Just chirping",
    "chirpCount": 7
  },
  "chirps": [
    { "id": 42, "content": "Hello world", "createdAt": 1700000000000, "likeCount": 3 }
  ],
  "hasMore": false
}
```

---

## Test Coverage

All tests are in-process unit tests within `crates/chirp-server/src/api/handlers.rs`
using `InMemoryRepository` (no network socket required). They call the handler functions
directly via `State`/`Query`/`Path` extractors.

### `public_chirps` tests

| Test name | Scenario |
|-----------|----------|
| `public_chirps_returns_200_without_auth_and_empty_timeline` | Empty store → 200, empty `chirps` list, `hasMore: false` |
| `public_chirps_returns_chirp_with_embedded_author` | Store with one chirp + user → embedded author fields present and correct |

### `user_chirps` tests

| Test name | Scenario |
|-----------|----------|
| `user_chirps_returns_200_for_existing_user_with_no_chirps` | User exists but has no chirps → 200, `chirps: []`, `chirpCount: 0` |
| `user_chirps_returns_404_for_missing_user` | Unknown username → `ServerError::NotFound` |
| `user_chirps_returns_chirp_count_and_page` | User with chirps → `chirpCount` matches total, `chirps` present |
| `user_chirps_case_insensitive_lookup` | `"ALICE"` resolves same user as `"alice"` |

**CI results** (run on `work/chirp-logged-out` HEAD `617f253`):

| Check | Result |
|-------|--------|
| `cargo fmt --check -p chirp-server` | ✓ pass |
| `cargo clippy -p chirp-server -- -D warnings` | ✓ pass (no warnings) |
| `cargo test -p chirp-server` | ✓ pass — 26 unit + 1 integration + 3 doc-tests, 0 failures |

---

## Deviations from Analysis Document

| # | Deviation | Explanation |
|---|-----------|-------------|
| 1 | `created_at` serializes as `i64` (ms since epoch), not ISO 8601 string | The existing domain `Timestamp` type stores milliseconds; the `analysis.md` spec mentions ISO 8601 as the external notation, but the implementation uses ms-epoch for consistency with all other timestamps in the codebase. This deviation is documented in the handler docstring and in the `PublicChirp` struct docstring. |
| 2 | `display_name` is `Option<String>` (null when empty), not unconditional `String` | The domain `User.display_name` is an empty string when unset; the handler coerces empty → `None` so the wire format is `null` rather than `""`. This aligns frontend expectations. |
| 3 | Branch HEAD at task start was `617f253`, not `21dca55` as recorded in `analysis.md` | A frontend empty-state fix landed after the analysis was written. No backend files were affected. |
