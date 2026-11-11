# Task: Transport-layer foundations — error rendering, app state, auth extraction

## Task Specification

**Slug**: SUBTASK_transport_foundations
**Task Kind**: standard
**Status**: Pending

### Objective

Establish the transport-layer primitives every handler compiles against: render `ServerError` as an
HTTP response, define the shared `AppState`, and extract the authenticated caller from the Bearer token.

### Context

This task is part of the chirp-server API-layer subtree (see `../_GLOBAL.md`) — the first spoke of the
serial pipeline. The predecessor (`../../SUBTASK_scaffold_and_repository`) has committed the async
`ChirpRepository` trait, the `ServerError` enum with HTTP-free `code()` / `into_api_error()` helpers,
and the in-memory impl into the shared clone. Compose against that **real committed code** — read
`../../SUBTASK_scaffold_and_repository/IMPLEMENTATION_NOTES.md` for the exact signatures; do not
re-derive them. The sub-contract `../contracts/_MANIFEST.yaml` binds your ownership and the symbols you
must expose.

**Dependencies**: none within the subtree (the predecessor's code is already committed on `work/chirp-server`).
**Dependents**: `SUBTASK_handlers` (its handlers return `Result<_, ServerError>`, take `State<AppState>`, and use your extractor), then `SUBTASK_router_and_bootstrap`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, success criteria |
| Sub-contract | `../contracts/_MANIFEST.yaml` | Your ownership, the symbol seam you expose, error-mapping pointer |
| Parent contract | `../../contracts/_MANIFEST.yaml` | The authoritative `error_mapping` table (variant → `ErrorCode` → HTTP status) |
| Predecessor handoff | `../../SUBTASK_scaffold_and_repository/IMPLEMENTATION_NOTES.md` | Real `ServerError`, `code()`/`into_api_error()`, trait signature, `resolve_token`, module layout |
| Committed code | the shared clone at the contract's `clone_path` | The real `ServerError`, `ChirpRepository`, module skeleton to build on |
| Wire contract | `crates/chirp-types` | `ApiError`, `ErrorCode`, `SessionToken`, `UserId` (import; never re-declare) |

---

## Process / Approach

Three cohesive primitives, one small layer:

- **Error rendering** — `impl IntoResponse for ServerError` in `src/error.rs`: map `err.code()` →
  `StatusCode` per the parent `error_mapping` table (Validation→400, Unauthorized→401, Forbidden→403,
  NotFound→404, Conflict→409, Internal→500) and serialize `err.into_api_error()` as the JSON body.
  For `Internal`, log the message (`tracing`) but keep the wire body generic.
- **Shared state** — `AppState` holding `repo: Arc<dyn ChirpRepository>` (Clone; usable as axum
  `State`). This is what handlers and `build_router` take.
- **Auth extraction** — an axum extractor that reads `Authorization: Bearer <token>`, calls
  `repo.resolve_token(&SessionToken(raw)).await` → `UserId`, and yields the authenticated `UserId`;
  a missing/invalid token surfaces as `ServerError::Unauthorized` (401). Extractor design (what it
  yields, how it reaches `AppState`) is your call — document it.

Create the `src/api/` module and add `pub mod api;` to `src/lib.rs`. Build locally
(`cargo build -p chirp-server`, `clippy --all-targets -- -D warnings`, `fmt --check`) and commit to
`work/chirp-server`. Internal module names (e.g. `src/api/state.rs`) are yours — record them in your
notes so the handlers spoke composes without guessing.

### Methodology

Apply the suggested methodology below; you are the final judge of what you load.

---

## Output Specification

### Primary Output (handoff)

| Attribute | Value |
|-----------|-------|
| Filename | `FOUNDATIONS_NOTES.md` |
| Location | this workspace (`SUBTASK_transport_foundations/`) |

Record the exposed symbols and their locations: the `AppState` type + field(s), the extractor type +
what it yields + how a handler names it, and the `IntoResponse` mapping as implemented (variant →
status). This is what `SUBTASK_handlers` reads to compose.

### Code output

`impl IntoResponse for ServerError`, `AppState`, and the Bearer auth extractor, with the `api` module
wired into `lib.rs`, committed to `work/chirp-server`.

---

## Success Criteria

- [ ] `impl IntoResponse for ServerError` maps every variant to the status + `ApiError`/`ErrorCode` body in the parent `error_mapping` table (validation `details` populated).
- [ ] `AppState { repo: Arc<dyn ChirpRepository> }` defined, `Clone`, usable as axum `State`.
- [ ] Bearer auth extractor resolves `UserId` via `repo.resolve_token`; missing/invalid token → 401.
- [ ] `api` module created and `pub mod api;` added to `lib.rs`; `cargo build -p chirp-server` + `clippy --all-targets -- -D warnings` + `fmt --check` clean.
- [ ] Committed to `work/chirp-server`; `FOUNDATIONS_NOTES.md` written with exposed-symbol locations.

---

## Suggested Methodology Files

Matched Domain-Mapping row: **Writing Rust code → primary `rust`; supporting `core`.** Load via
`engine_load_methodology { name: "<bundle_id>" }` and reference the files below.

- `rust` — `rust/Rust_Error_Handling_Methodology.md` (error-as-value → `IntoResponse`; the central
  concern of this task), `rust/Rust_Trait_Design_Methodology.md` (`Arc<dyn ChirpRepository>` as state
  vs generics), `rust/Rust_Type_System_Methodology.md` (extractor / typed-state design).
- `core` — `core/BestPractices_Error_Handling_Methodology.md`, `core/BestPractices_Coding_Standards_Methodology.md`, `core/CodeManagement_Commit_Practices_Methodology.md`.

These are the parent's flagged methodologies; load them as a starting point and exercise your own judgment.

## Inherited Constraints

- Compose against the REAL committed `ServerError` / `ChirpRepository` / `code()` / `into_api_error()` / `resolve_token`; import `ApiError`/`ErrorCode`/`SessionToken`/`UserId` from `chirp-types`. Re-declare nothing.
- Edition 2021 / rust 1.82 / stable; `clippy --all-targets -- -D warnings` clean.
- ALL work in the ONE shared clone (`../contracts/_MANIFEST.yaml` `clone_path`); branch `work/chirp-server`; never touch `main`; no commit-attribution trailers.
- Do NOT edit `Cargo.toml` — the transport deps are already provisioned by the scaffold spoke.

## Out-of-Scope Methodologies

- Do NOT write handlers, the router, static serving, `/healthz`, tracing init, or `main.rs` — those are later spokes (`SUBTASK_handlers`, `SUBTASK_router_and_bootstrap`).
- Do NOT redefine the error enum or the repository trait — they are the predecessor's, committed.
