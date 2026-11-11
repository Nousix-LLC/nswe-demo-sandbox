# _BRIEF.md — SUBTASK_server_public_timeline

**Parent:** chirp-logged-out  
**Global hub:** `taskflow/dags/chirp-logged-out/_GLOBAL.md`

## Objective

Extend `chirp-server` with an unauthenticated public timeline endpoint so that logged-out visitors can read the global timeline without a bearer token. The endpoint returns a paginated list of all recent chirps across all authors, newest-first, using the same cursor-based `Page<Chirp>` shape already used by the authenticated home-timeline endpoint.

## Background

`GET /api/timeline` today requires the `AuthUser` extractor and returns HTTP 401 for unauthenticated callers. The `ChirpRepository::timeline` method signature also requires a `viewer: UserId`. Neither the handler nor the trait method can serve a logged-out visitor today.

`GET /api/users/{id}` is already unauthenticated — that path requires no change.

The existing `InMemoryRepository` and `PostgresRepository` both implement `ChirpRepository`. Any new trait method must be implemented in both.

## Scope

Add a `public_timeline` capability to the server:

1. **`ChirpRepository` trait** (`crates/chirp-server/src/repository/mod.rs`): add a new `async fn public_timeline(&self, query: TimelineQuery) -> Result<Page<Chirp>, ServerError>` method. No viewer argument. Returns all chirps globally, newest-first, with cursor-based pagination. Document its contract in the same style as the existing `timeline` method.

2. **`InMemoryRepository`** (`crates/chirp-server/src/repository/in_memory.rs`): implement `public_timeline`. All chirps from all users, sorted newest-first, with the same `limit`/`cursor` semantics as the existing `timeline` implementation.

3. **`PostgresRepository`** (`crates/chirp-server/src/repository/postgres.rs`, feature-gated): implement `public_timeline`. Same contract, executed against the PostgreSQL schema. Match the query style already used for `timeline`.

4. **Handler** (`crates/chirp-server/src/api/handlers.rs`): add `pub async fn public_timeline(State(state): State<AppState>, Query(query): Query<TimelineQuery>) -> Result<Json<Page<Chirp>>, ServerError>`. No auth extractor. Delegate to `state.repo.public_timeline(query)`. Document it in the module doc table.

5. **Router** (`crates/chirp-server/src/api/router.rs`): mount `GET /public/timeline` → `public_timeline` handler. This sits at `GET /api/public/timeline` from the client's perspective.

6. **Tests**: integration tests covering the new endpoint:
   - Empty store → 200 with empty page.
   - Posts from multiple users → 200, all chirps returned newest-first.
   - Cursor pagination → second page returns remainder.
   - No `Authorization` header → 200 (not 401).

## Declared outputs

- Commits on branch `work/chirp-logged-out` (create from `main` at commit `62febf5faf6023b3492365d246c7ac39c9f659a3` if the branch does not yet exist).
- `crates/chirp-server/src/repository/mod.rs` — `public_timeline` trait method.
- `crates/chirp-server/src/repository/in_memory.rs` — `InMemoryRepository` impl.
- `crates/chirp-server/src/repository/postgres.rs` — `PostgresRepository` impl (feature-gated).
- `crates/chirp-server/src/api/handlers.rs` — `public_timeline` handler.
- `crates/chirp-server/src/api/router.rs` — route wired.
- Tests passing under `cargo test` (no `--features postgres` needed in CI for in-memory tests).
- `COMPLETE.md` in this workspace on completion.

## Success criteria

- `GET /api/public/timeline` returns HTTP 200 with a valid `Page<Chirp>` body when called without any `Authorization` header.
- The existing authenticated `GET /api/timeline` is unmodified — no regression.
- `cargo fmt --check`, `cargo clippy`, and `cargo test` all pass on the branch.

## Constraints

- Repository: `Nousix-LLC/nswe-demo`
- Branch: `work/chirp-logged-out`
- Written for the repository's readers: no host paths, no internal addresses, no taskflow references in anything committed or posted to GitHub.
- Do not change `GET /api/timeline` or any existing authenticated endpoint.
- Do not remove authentication from any endpoint that currently has it.
