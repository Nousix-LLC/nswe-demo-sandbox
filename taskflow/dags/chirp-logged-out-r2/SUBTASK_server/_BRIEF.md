# _BRIEF.md — SUBTASK_server

## Objective

Create the branch `work/chirp-logged-out` from `main` at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`
and implement the unauthenticated public timeline endpoint on `chirp-server` so that
`GET /api/public/timeline` returns all chirps without requiring an Authorization header.

This is the server-side half of GitHub issue #35.

## Context

**Repository:** `Nousix-LLC/nswe-demo`  
**Branch:** `work/chirp-logged-out` (create from `main` at `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`)  
**Codebase root:** `crates/chirp-server/`

**Current state of `chirp-server`:**
- `GET /api/timeline` exists but requires `AuthUser` Axum extractor (HTTP 401 for unauthenticated requests). This is the personalized home timeline (self + followees). Do not change it.
- `GET /api/users/{id}` is already unauthenticated.
- `ChirpRepository` trait lives in `crates/chirp-server/src/repository/mod.rs`.
- `timeline(&self, viewer: UserId, query: TimelineQuery)` on the trait filters to viewer + followees.
- `InMemoryRepository` in `repository/in_memory.rs`, `PostgresRepository` in `repository/postgres.rs`.
- Handlers in `api/handlers.rs`, routes in `api/router.rs`.

**Types (from `chirp-types`):** `TimelineQuery { limit: Option<u32>, cursor: Option<Cursor> }`, `Page<T>`, `Chirp`, `ApiError`. All already exist — no new shared types are needed.

## Declared outputs

- Commits on branch `work/chirp-logged-out` containing all server changes
- The endpoint `GET /api/public/timeline` returns `Page<Chirp>` without authentication
- Integration tests verifying the new endpoint

## Scope (this task only)

**In scope:**
1. Create branch `work/chirp-logged-out` from `main` at `cb1ced3`
2. Add `pub_timeline(&self, query: TimelineQuery) -> Result<Page<Chirp>, ServerError>` to the `ChirpRepository` trait in `repository/mod.rs`
3. Implement `pub_timeline` in `InMemoryRepository`: return all chirps (no viewer/followee filter), same pagination logic as `timeline` (reverse-chron by id, `limit+1` probe, opaque cursor = last item's id as string)
4. Implement `pub_timeline` in `PostgresRepository`: SQL query without the viewer/followee join — `SELECT` all chirps ordered reverse-chronologically with cursor-based pagination
5. Add `pub async fn public_timeline_handler` in `api/handlers.rs`: uses `State<AppState>` and `Query<TimelineQuery>` extractors — NO `AuthUser` — calls `state.repo.pub_timeline(query)` and returns JSON
6. Register `GET /api/public/timeline` route in `api/router.rs` pointing to `public_timeline_handler`
7. Write integration tests: at minimum, one test that GETs `/api/public/timeline` without an Authorization header and asserts HTTP 200 with a `Page<Chirp>` response body

**Out of scope:** Any frontend changes; any changes to existing authenticated endpoints; SSR integration.

## Success criteria

- `GET /api/public/timeline` returns HTTP 200 with a `Page<Chirp>` body when called without an Authorization header
- `GET /api/timeline` (existing) is unchanged and still requires auth
- `cargo test` passes for `chirp-server`
- `cargo fmt --check` passes
- `cargo clippy -- -D warnings` passes
- All changes committed on `work/chirp-logged-out` with commit message attribution

## Constraints (inherited from parent hub)

- **Security**: Do not put any host address, SSH key path, username, or host path into any committed file, PR, or comment
- **API contract**: The endpoint surface is `GET /api/public/timeline → Page<Chirp>` as defined in `../contracts/_MANIFEST.yaml`. Do not deviate from this surface
- **No auth removal**: Do not modify or remove authentication from any existing route
- **Repository trait pattern**: All persistence through `ChirpRepository` trait; no direct database calls from handlers
- **Git**: Branch from `cb1ced3ffe6efc678d96a26ae16a63cb948d4237`. One commit (or a small logical series). Commit message ends with:
  ```
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
  ```
- **SSH for kubectl**: The build server hosts the k3s cluster; use SSH for any kubectl/helm commands. This constraint is a runtime mechanics note — do not put SSH details in committed files.

## Suggested Methodology Files

Domain mapping row matched: **"Rust web services / Axum / Tower / server-side HTTP"** →
primary bundle `Rust`, supporting bundle `Framework Design`.

**Primary:**
- `rust/Rust_Web_Services_Axum_Methodology.md` — Axum extractor pattern, State injection, router builder, handler signatures. Directly applicable to adding an unauthenticated handler and route. The existing `timeline` handler is the reference pattern; this task adds a variant without the `AuthUser` extractor.
- `rust/Rust_Trait_Design_Methodology.md` — Adding a method to an existing trait and ensuring both implementations satisfy it without breaking the existing API surface. Required because `pub_timeline` extends `ChirpRepository`.
- `rust/Rust_Testing_Methodology.md` — Integration test patterns for Axum services; `axum::test` or similar; async test setup. Required for the integration tests covering the new endpoint.

**Supporting:**
- `core/BestPractices_Error_Handling_Methodology.md` — Error propagation from repository to handler; `?` operator; mapping `ServerError` to HTTP status codes.
- `core/CodeManagement_Commit_Practices_Methodology.md` — Commit message format and attribution.

The above are the parent's flagged methodologies based on the task type. The child agent SHOULD load these as a starting point but is the final judge of what its work requires — load fewer if some are clearly inapplicable; load more if the child's own reading of the brief reveals additional methodology surface the parent did not anticipate.

## Out-of-Scope Methodologies

- `frontend/` bundle — no frontend changes in this task
- `rust/Rust_WebAssembly_Browser_Methodology.md` — WASM is the frontend task's concern
- `Synthesis` bundle — synthesis is a separate child task
