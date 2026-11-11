# _GLOBAL.md — SUBTASK_server_public_timeline subtree

**Task:** SUBTASK_server_public_timeline  
**Parent hub:** `taskflow/dags/chirp-logged-out/_GLOBAL.md`

## Goal

Extend `chirp-server` with an unauthenticated public timeline endpoint (`GET /api/public/timeline`) so logged-out visitors can read the global timeline without a bearer token. Delivers all required changes on branch `work/chirp-logged-out`: the `ChirpRepository` trait method, both implementor overrides, the axum handler and route mount, and integration tests with CI passing.

## Shared context

- **Repository:** `Nousix-LLC/nswe-demo`
- **Branch:** `work/chirp-logged-out` — created from `main` at `62febf5faf6023b3492365d246c7ac39c9f659a3` by CHILD_skeleton; subsequent children commit on top.
- **Codebase root:** `/home/user/nswe-demo/crates/chirp-server/`
- **Key files:**
  - `src/repository/mod.rs` — `ChirpRepository` trait (`async_trait`, object-safe, `Arc<dyn ChirpRepository>`)
  - `src/repository/in_memory.rs` — `InMemoryRepository` (default no-infra backing; `Mutex<Store>`, `store.chirps: HashMap<ChirpId, Chirp>`, `store.removed: HashSet<ChirpId>`)
  - `src/repository/postgres.rs` — `PostgresRepository` (feature-gated `#[cfg(feature = "postgres")]`)
  - `src/api/handlers.rs` — axum handler functions
  - `src/api/router.rs` — composition root, mounts all routes under `/api/…`
  - `tests/api.rs` — end-to-end integration tests (in-process, no network)

## New capability contract

**Trait method:**
```rust
/// Returns a page of all public chirps across all authors, newest-first.
///
/// No viewer argument — the feed is global and unauthenticated. Soft-removed chirps
/// are excluded. Pagination uses the same opaque cursor scheme as `timeline`: a present
/// cursor is the last-seen chirp id; a malformed cursor fails safe to the first page.
async fn public_timeline(&self, query: TimelineQuery) -> Result<Page<Chirp>, ServerError>;
```

**Handler:**
```rust
pub async fn public_timeline(
    State(state): State<AppState>,
    Query(query): Query<TimelineQuery>,
) -> Result<Json<Page<Chirp>>, ServerError> {
    let page = state.repo.public_timeline(query).await?;
    Ok(Json(page))
}
```

**Route:** `GET /public/timeline` → `public_timeline` handler (mounts as `GET /api/public/timeline` from the client's perspective).

## Existing pattern — `timeline` in `in_memory.rs` (lines 351–405)

Locks the store; resolves `limit` from `query.limit.unwrap_or(DEFAULT_TIMELINE_LIMIT).clamp(1, MAX_TIMELINE_LIMIT)`; decodes `cursor_id: Option<u64>` from `query.cursor` (malformed = `None` = first page). Collects from `store.chirps.values()` filtered by `!store.removed.contains(&chirp.id)` and by visibility (viewer's own + followees'). Sorts by `Reverse(chirp.id.get())`. Takes `limit+1` to detect a next page. Uses the last item's id as `Cursor`. `public_timeline` omits the viewer/followee filter — collects all non-removed chirps.

## Existing pattern — `timeline` in `postgres.rs` (line 532)

Uses helpers: `clamp_limit(query.limit)`, `decode_cursor(query.cursor.as_ref())`, `fetch_limit(limit)`, `paginate(chirps, limit, |chirp| chirp.id.get())`. SQL:
```sql
SELECT id, author_id, text, created_at, like_count, reply_to, removed, removed_at
FROM chirps
WHERE removed = FALSE
  AND (author_id = $1 OR author_id IN (SELECT followee_id FROM follows WHERE follower_id = $1))
  AND ($2::BIGINT IS NULL OR id < $2)
ORDER BY id DESC LIMIT $3
```
`public_timeline` removes the `author_id` filter entirely, keeping only `removed = FALSE` and the cursor clause.

## Sub-task map

| ID | Name | Depends on | Key deliverable |
|----|------|------------|-----------------|
| `CHILD_skeleton` | Seam and stubs | — | Trait method + `todo!()` stubs in both impls + handler + route mount; `cargo build` passes; branch created; committed |
| `CHILD_in_memory` | In-memory implementation | `CHILD_skeleton` | Real `InMemoryRepository::public_timeline` impl; committed |
| `CHILD_postgres` | Postgres implementation | `CHILD_in_memory` | Real `PostgresRepository::public_timeline` impl; committed |
| `CHILD_tests` | Tests and CI verify | `CHILD_postgres` | Integration tests; `cargo fmt --check`, `cargo clippy`, `cargo test` pass; committed; `COMPLETE.md` |

## Security constraint

Nothing committed to the repository may contain host paths, internal addresses, SSH key paths, or taskflow references. Code and tests only reference `chirp-server` internals and public `chirp-types` DTOs.
