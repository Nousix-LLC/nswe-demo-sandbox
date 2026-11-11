# _BRIEF.md — CHILD_postgres

**Parent task:** SUBTASK_server_public_timeline  
**Parent hub:** `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/_GLOBAL.md`

## Objective

Replace the `todo!()` stub in `PostgresRepository::public_timeline` with a real implementation that queries the database for all non-removed chirps, ordered by id descending, with cursor-based pagination — matching the contract of `InMemoryRepository::public_timeline` and the existing `timeline` method's SQL and helper style.

## Scope

A single implementation concern: `crates/chirp-server/src/repository/postgres.rs` (feature-gated `#[cfg(feature = "postgres")]`).

The existing `timeline` method (around line 532 in the same file) is the reference implementation. It uses `clamp_limit`, `decode_cursor`, `fetch_limit`, and `paginate` helpers and wraps the SQL query in `self.with_transaction`. `public_timeline` uses the same helpers and the same `with_transaction` pattern, but the SQL query is simpler — it removes the `author_id` filter entirely, keeping only `removed = FALSE` and the optional cursor clause:

```sql
SELECT id, author_id, text, created_at, like_count, reply_to, removed, removed_at
FROM chirps
WHERE removed = FALSE
  AND ($1::BIGINT IS NULL OR id < $1)
ORDER BY id DESC LIMIT $2
```

The rows are decoded via `mapping::ChirpRow::into_chirp` and paginated with `paginate(chirps, limit, |chirp| chirp.id.get())`, exactly as in `timeline`.

## Inputs

- `crates/chirp-server/src/repository/postgres.rs` on branch `work/chirp-logged-out` (CHILD_in_memory has committed; the postgres stub is still from CHILD_skeleton)
- Parent hub: `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/_GLOBAL.md`

## Declared outputs

- `crates/chirp-server/src/repository/postgres.rs` — real `public_timeline` implementation replacing the stub (inside `#[cfg(feature = "postgres")]`)
- `cargo build --features postgres` passes
- Changes committed on `work/chirp-logged-out`
- `COMPLETE.md` in this workspace

## Success criteria

- `PostgresRepository::public_timeline` issues a SQL query that selects all non-removed chirps ordered by `id DESC` with an optional cursor clause, using `fetch_limit(limit)`.
- Uses `clamp_limit`, `decode_cursor`, `fetch_limit`, and `paginate` consistent with the existing `timeline` implementation.
- `cargo build --features postgres` exits 0.
- No other method in `postgres.rs` is changed.

## Constraints

- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out`
- Feature-gated: the impl is inside the `#[cfg(feature = "postgres")]` block.
- Do not modify the `timeline` method or any other existing method.
- Nothing committed contains host paths, internal addresses, SSH key paths, or taskflow references.
