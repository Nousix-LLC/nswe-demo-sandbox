# Backend Public API Implementation

## Summary

Both required public endpoints already existed on branch `work/chirp-logged-out` in
`crates/chirp-server/src/api/handlers.rs` and satisfied every constraint in
`contracts/public_api_contract.md`. No new handlers, routes, or auth changes were
required. This document confirms their shapes for SUBTASK_frontend-ui.

---

## 1. Endpoints Implemented

### Public Timeline

| Attribute | Value |
|-----------|-------|
| URL pattern | `GET /api/chirps` |
| Handler | `public_chirps` — `crates/chirp-server/src/api/handlers.rs` |
| Router mount | `crates/chirp-server/src/api/router.rs` |
| Origin | Pre-existing endpoint; no changes made |

### Public User Profile

| Attribute | Value |
|-----------|-------|
| URL pattern | `GET /api/users/{username}/chirps` |
| Handler | `user_chirps` — `crates/chirp-server/src/api/handlers.rs` |
| Router mount | `crates/chirp-server/src/api/router.rs` |
| Path parameter | `{username}` — case-insensitive string lookup |
| Origin | Pre-existing endpoint; no changes made |

---

## 2. Auth Behavior

**Neither endpoint requires authentication.**

The server uses no global auth middleware (`build_router` applies only
`TraceLayer::new_for_http()`). Auth is opt-in per handler via an `AuthUser`
extractor argument. Neither `public_chirps` nor `user_chirps` include `AuthUser`
in their parameter lists, so:

- Requests with no `Authorization` header succeed.
- Requests with no session cookie succeed.
- Bearer tokens, if present, are silently ignored.

---

## 3. Response Shapes

### `GET /api/chirps` → `PublicTimelineResponse`

```json
{
  "chirps": [
    {
      "id": 1,
      "content": "Hello chirp!",
      "author": {
        "username": "alice",
        "display_name": "Alice"
      },
      "created_at": 1700000000000,
      "like_count": 3
    }
  ],
  "has_more": false
}
```

Rust types:

```rust
pub struct PublicTimelineResponse {
    pub chirps: Vec<PublicChirp>,
    pub has_more: bool,
}

pub struct PublicChirp {
    pub id: ChirpId,          // u64 — serialises as a JSON number
    pub content: String,
    pub author: PublicAuthor,
    pub created_at: i64,      // Unix milliseconds (epoch ms)
    pub like_count: u64,
}

pub struct PublicAuthor {
    pub username: String,
    pub display_name: Option<String>,
}
```

Empty timeline (no chirps in the store):

```json
{ "chirps": [], "has_more": false }
```

This is a 200 response, not an error. `has_more: false` signals end-of-list.

---

### `GET /api/users/{username}/chirps` → `PublicUserResponse`

```json
{
  "user": {
    "username": "alice",
    "display_name": "Alice",
    "bio": "Just a person.",
    "chirp_count": 42
  },
  "chirps": [
    {
      "id": 7,
      "content": "My latest thought",
      "created_at": 1700000050000,
      "like_count": 1
    }
  ],
  "has_more": false
}
```

Rust types:

```rust
pub struct PublicUserResponse {
    pub user: PublicUserProfile,
    pub chirps: Vec<PublicUserChirp>,
    pub has_more: bool,
}

pub struct PublicUserProfile {
    pub username: String,
    pub display_name: Option<String>,
    pub bio: Option<String>,
    pub chirp_count: u64,
}

pub struct PublicUserChirp {
    pub id: ChirpId,          // u64
    pub content: String,
    pub created_at: i64,      // Unix milliseconds
    pub like_count: u64,
}
```

Unknown username returns HTTP 404 (`ServerError::NotFound`).

---

## 4. Pagination Contract

Both endpoints accept the same query parameters, defined by `PublicTimelineQuery`:

```rust
pub struct PublicTimelineQuery {
    pub before: Option<i64>,  // cursor: exclusive upper bound (created_at ms)
    pub limit: Option<u32>,   // page size; clamped to [1, 50]; default 20
}
```

**Cursor behaviour**

- Results are ordered newest-first (descending `created_at`).
- `before` is an exclusive upper bound on `created_at` in Unix milliseconds.
- To fetch the next page, pass the `created_at` of the last item in the current
  page as `before`.
- Omit `before` (or pass `null`) to start from the most recent chirp.

**`has_more` flag**

- `true` → at least one more chirp exists beyond this page; fetch the next page.
- `false` → this is the last page (end-of-list state).

**Examples**

```
GET /api/chirps                        → first 20 chirps, newest first
GET /api/chirps?limit=10               → first 10 chirps
GET /api/chirps?before=1700000000000   → chirps older than epoch 1700000000000
GET /api/chirps?before=1700000000000&limit=5

GET /api/users/alice/chirps            → first 20 of alice's chirps
GET /api/users/ALICE/chirps            → same (case-insensitive)
GET /api/users/alice/chirps?limit=5&before=1700000000000
```

---

## 5. Test Coverage

All tests are pre-existing (none were added by this task; none were needed).

### Unit tests — `crates/chirp-server/src/api/handlers.rs`

| Test name | What it verifies |
|-----------|-----------------|
| `public_chirps_returns_200_without_auth_and_empty_timeline` | Handler returns `Ok` with `{ chirps: [], has_more: false }` on an empty store with no auth headers |
| `public_chirps_returns_chirp_with_embedded_author` | Chirp items embed the author's `username` and `display_name` in the response |
| `user_chirps_returns_200_for_existing_user_with_no_chirps` | Returns `Ok` with empty `chirps` and `chirp_count: 0` for a known user with no chirps |
| `user_chirps_returns_404_for_missing_user` | Returns `Err(ServerError::NotFound)` for an unknown username |
| `user_chirps_returns_chirp_count_and_page` | `chirp_count` reflects total count; `has_more` is correct after pagination |
| `user_chirps_case_insensitive_lookup` | Username lookup is case-insensitive (`"Alice"` matches user `"alice"`) |

### Integration tests — `crates/chirp-server/tests/api.rs`

| Test name | What it verifies |
|-----------|-----------------|
| `public_timeline::public_timeline_requires_no_auth` | HTTP request with no `Authorization` header returns 200 |
| `public_timeline::public_timeline_empty_store_returns_200_with_empty_page` | Empty store returns `200 { chirps: [], has_more: false }`, not 404 or 500 |
| `public_timeline::public_timeline_includes_all_users_newest_first` | Multiple users' chirps appear in the response, ordered newest-first |
| `public_timeline::public_timeline_paginates_with_cursor` | `before` cursor + `limit` correctly partitions results across pages |

**All 95 tests pass** (65 unit, 26 integration, 1 concurrency, 3 doc).
`cargo clippy -p chirp-server -- -D warnings` produces no warnings.

---

## 6. Contract Compliance

| Contract constraint | Status |
|--------------------|--------|
| No auth required | ✓ Neither handler includes `AuthUser` |
| Returns chirps with id, content, author username, created_at | ✓ All present in `PublicChirp` and `PublicUserChirp` |
| Supports pagination | ✓ `before` cursor + `limit`; `has_more` flag |
| Empty list is distinguishable from error | ✓ Empty → `200 { chirps: [], has_more: false }`; not a 4xx/5xx |
| Returns user profile with username, display_name, bio | ✓ All present in `PublicUserProfile` (display_name and bio are `Option`) |
| Returns the user's chirps | ✓ `chirps: Vec<PublicUserChirp>` in `PublicUserResponse` |
| 404 for unknown usernames | ✓ `ServerError::NotFound` → HTTP 404 |
