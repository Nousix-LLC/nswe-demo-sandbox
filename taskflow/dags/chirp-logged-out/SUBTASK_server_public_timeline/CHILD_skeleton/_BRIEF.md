# _BRIEF.md — CHILD_skeleton

**Parent task:** SUBTASK_server_public_timeline  
**Parent hub:** `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/_GLOBAL.md`

## Objective

Establish the `public_timeline` capability seam in `chirp-server`: add the new `ChirpRepository` trait method, placeholder `todo!()` overrides in both implementing structs, the axum handler, and the route mount. After this child completes, `cargo build` passes and the route exists end-to-end, even though the implementations are not yet functional.

Branch `work/chirp-logged-out` must be created from `main` at commit `62febf5faf6023b3492365d246c7ac39c9f659a3` if it does not yet exist.

## Scope

Three distinct concerns:

1. **Trait extension** — `crates/chirp-server/src/repository/mod.rs`: add `async fn public_timeline(&self, query: TimelineQuery) -> Result<Page<Chirp>, ServerError>` to the `ChirpRepository` trait. Document its contract (no viewer arg, global unfiltered feed, newest-first, same cursor-based pagination as `timeline`) in the same style as the adjacent `timeline` method. Update the module-level capability table in the doc comment to include `public_timeline`.

2. **Stub overrides** — `crates/chirp-server/src/repository/in_memory.rs` and `crates/chirp-server/src/repository/postgres.rs`: add `async fn public_timeline(&self, query: TimelineQuery) -> Result<Page<Chirp>, ServerError> { todo!("public_timeline not yet implemented") }` overrides in `impl ChirpRepository for InMemoryRepository` and `impl ChirpRepository for PostgresRepository`. The postgres override is inside the `#[cfg(feature = "postgres")]` block. These stubs exist only to satisfy the compiler; they will be replaced by CHILD_in_memory and CHILD_postgres.

3. **Handler and route** — `crates/chirp-server/src/api/handlers.rs`: add `pub async fn public_timeline(State(state): State<AppState>, Query(query): Query<TimelineQuery>) -> Result<Json<Page<Chirp>>, ServerError>` with no `AuthUser` extractor; it delegates to `state.repo.public_timeline(query).await` and wraps the result in `Json`. Update the module doc table to include this handler. `crates/chirp-server/src/api/router.rs`: mount `.route("/api/public/timeline", get(handlers::public_timeline))` in `build_router`.

## Inputs

- Codebase: `/home/user/nswe-demo/crates/chirp-server/` on `main` at `62febf5faf6023b3492365d246c7ac39c9f659a3`
- Parent hub: `taskflow/dags/chirp-logged-out/SUBTASK_server_public_timeline/_GLOBAL.md` (contains trait method contract, handler signature, and route path)

## Declared outputs

- `work/chirp-logged-out` branch created (if not existing) from `62febf5faf6023b3492365d246c7ac39c9f659a3`
- `crates/chirp-server/src/repository/mod.rs` — trait method added
- `crates/chirp-server/src/repository/in_memory.rs` — stub override added
- `crates/chirp-server/src/repository/postgres.rs` — stub override added (feature-gated)
- `crates/chirp-server/src/api/handlers.rs` — handler added
- `crates/chirp-server/src/api/router.rs` — route mounted
- `cargo build` and `cargo build --features postgres` both pass
- Changes committed on `work/chirp-logged-out`
- `COMPLETE.md` in this workspace

## Success criteria

- `cargo build` (and `cargo build --features postgres`) exits 0.
- `GET /api/public/timeline` route exists (the handler panics at runtime until CHILD_in_memory fills in the impl — that is acceptable for this gate).
- No existing authenticated endpoint is modified; `GET /api/timeline` is untouched.
- Nothing committed contains host paths, internal addresses, SSH key paths, or taskflow references.

## Constraints

- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out`
- Do not change `GET /api/timeline` or any existing handler.
- Do not remove authentication from any endpoint that currently has it.
