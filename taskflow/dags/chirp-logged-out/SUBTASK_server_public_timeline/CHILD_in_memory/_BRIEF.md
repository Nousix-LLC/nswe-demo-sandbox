# _BRIEF.md — CHILD_in_memory

**Parent task:** SUBTASK_server_public_timeline  
**Parent hub:** `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/_GLOBAL.md`

## Objective

Replace the `todo!()` stub in `InMemoryRepository::public_timeline` with a real implementation that returns all non-removed chirps from all users, sorted newest-first, with the same cursor-based pagination mechanics as the existing `timeline` method.

## Scope

A single implementation concern: `crates/chirp-server/src/repository/in_memory.rs`.

The existing `timeline` method in the same `impl ChirpRepository for InMemoryRepository` block is the reference implementation. `public_timeline` has the same pagination mechanics but omits the viewer/followee visibility filter — it collects all chirps from `store.chirps.values()` that are not in `store.removed`, regardless of author.

The parent hub (`_GLOBAL.md` → "Existing pattern — `timeline` in `in_memory.rs`") contains the full implementation pattern. The key difference is that `public_timeline` removes these two lines from the filter chain:
```rust
let followees: HashSet<UserId> = ...;
let is_visible = |author: UserId| author == viewer || followees.contains(&author);
// and the .filter(|chirp| is_visible(chirp.author_id)) step
```
Everything else — lock, limit/cursor resolution, sort, limit+1 trick, next_cursor — is identical.

## Inputs

- `crates/chirp-server/src/repository/in_memory.rs` on branch `work/chirp-logged-out` (CHILD_skeleton has committed the stub)
- Parent hub: `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/_GLOBAL.md`

## Declared outputs

- `crates/chirp-server/src/repository/in_memory.rs` — real `public_timeline` implementation replacing the stub
- `cargo build` passes
- Changes committed on `work/chirp-logged-out`
- `COMPLETE.md` in this workspace

## Success criteria

- `InMemoryRepository::public_timeline` returns all non-removed chirps, newest-first, respecting `limit` and `cursor` from `TimelineQuery`.
- Pagination contract matches `timeline`: cursor is the last returned chirp's id; `next_cursor` is `Some` iff more items remain beyond this page.
- A malformed cursor fails safe to the first page (same as `timeline`).
- `cargo build` exits 0.
- No other method in `in_memory.rs` is changed.

## Constraints

- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out`
- Do not modify the `timeline` method or any other existing method.
- Nothing committed contains host paths, internal addresses, SSH key paths, or taskflow references.
