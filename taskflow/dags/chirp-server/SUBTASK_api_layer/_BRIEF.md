# Task: The axum API layer (transport + service) for `chirp-server`

## Task Specification

**Slug**: SUBTASK_api_layer
**Task Kind**: standard
**Status**: Pending

### Objective

Build the HTTP layer of `chirp-server` against the committed repository trait: axum handlers for the full
endpoint surface over `chirp-types` DTOs, the router + application state, typed-error → `ApiError`/HTTP-status
mapping, static-asset + SPA-fallback serving, a `GET /healthz` endpoint, `tracing` structured logging, and the
binary `main` that wires it all — committed to `work/chirp-server`.

### Context

This is the **transform stage** of the chirp-server pipeline. Your predecessor
(`SUBTASK_scaffold_and_repository`) has committed the crate skeleton, the `ChirpRepository` trait, the
`ServerError` enum, and the in-memory impl into the shared clone; read its `IMPLEMENTATION_NOTES.md` for the
real signatures and compose against the real committed code (do not re-derive the trait). The subtree hub
`_GLOBAL.md` and `contracts/_MANIFEST.yaml` bind you — especially the **error-mapping table** (you own the
`IntoResponse`) and the module-layout ownership.

**Dependencies**: `SUBTASK_scaffold_and_repository`.
**Dependents**: `SUBTASK_integration_tests_and_docs` (exercises your router end-to-end).

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, success criteria |
| Contract | `../contracts/_MANIFEST.yaml` | Error-mapping table, ownership, module layout, endpoint surface |
| Predecessor handoff | `../SUBTASK_scaffold_and_repository/IMPLEMENTATION_NOTES.md` | The real trait signature, error enum, module layout, clone/branch |
| Committed code | the shared clone at the contract's `clone_path` | The real `ChirpRepository` trait + `ServerError` + in-memory impl to build on |
| Wire contract | `crates/chirp-types` | Request/response DTOs the handlers accept + return (import; never re-declare) |

---

## Process / Approach

Keep the layering clean: handlers translate HTTP ⇄ DTOs and delegate to the repository trait; they do not
re-implement persistence. Expose the router via a builder in `lib.rs` (e.g. `build_router(state)`) so the
integration-test spoke can mount it without the binary. Cover the full endpoint surface in the contract's
`repository_seam` (timeline, post chirp, create user, login/session, user profile, follow/unfollow,
like/unlike), plus `GET /healthz`, plus a static-file service (`tower-http` `ServeDir`) with an SPA fallback
route serving from the placeholder static dir. Implement `IntoResponse` for `ServerError` per the contract's
error-mapping table so every failure surfaces as an `ApiError` JSON body with the right HTTP status. Initialize
`tracing` structured logging + a request-trace layer. Author `main.rs` to init tracing, build state + router,
bind, and serve. Build locally, then commit. Internal module structure, extractor design, and how you resolve
the session token are YOUR calls — document them. Re-run your own decompose-evaluation: this layer spans several
genuinely distinct pieces (handlers, error-response mapping, static/SPA serving, server bootstrap) — if that
proves to be more than one responsibility for a single invocation, decompose further rather than pushing through.

### Methodology

Apply the suggested methodology below; you are the final judge of what you load.

---

## Output Specification

### Primary Output (handoff)

| Attribute | Value |
|-----------|-------|
| Filename | `API_NOTES.md` |
| Location | this workspace (`SUBTASK_api_layer/`) |

Record: the route table (method + path + request DTO + response DTO + status), the `AppState` design, the
error→HTTP mapping as implemented, how static serving + SPA fallback are wired, how to run the server, and the
local `cargo build` status. This is what the integration-test spoke reads to know what to exercise.

### Code output

Handlers, router, `AppState`, `IntoResponse` for `ServerError`, static+SPA serving, `/healthz`, tracing, and
`main.rs`, committed to `work/chirp-server`.

---

## Success Criteria

- [ ] Every endpoint in the contract's `repository_seam` is routed, over `chirp-types` DTOs, delegating to `ChirpRepository`.
- [ ] `ServerError` → `ApiError` + HTTP status matches the contract's `error_mapping` table (validation details populated).
- [ ] Static-file service + SPA fallback wired to the placeholder static dir; `GET /healthz` returns a health response.
- [ ] `tracing` initialized with a request-trace layer; `main.rs` builds state + router and serves.
- [ ] `build_router`/app builder is exposed from `lib.rs` for integration testing; `cargo build -p chirp-server` succeeds.
- [ ] Work committed to `work/chirp-server`; `API_NOTES.md` written.

---

## Suggested Methodology Files

Matched Domain-Mapping row: **Writing Rust code → primary `rust`; supporting `core`**; plus
**Frontend architecture design / API design → `architecture`** for the transport↔service layering and API shape.

- `rust` — `rust/Rust_Async_Tokio_Methodology.md` (axum/tokio handler + runtime design), `rust/Rust_Error_Handling_Methodology.md` (error-as-value → `IntoResponse`), `rust/Rust_Trait_Design_Methodology.md` (generic `AppState<R: ChirpRepository>` vs `Arc<dyn ChirpRepository>`), `rust/Rust_Type_System_Methodology.md` (extractors / typed state).
- `core` — `core/BestPractices_Coding_Standards_Methodology.md`, `core/BestPractices_Error_Handling_Methodology.md`, `core/CodeManagement_Commit_Practices_Methodology.md`.
- `architecture` — `architecture/Architecture_API_Design_Methodology.md` (REST surface, status-code discipline), `architecture/Architecture_Styles_Methodology.md` (transport → service → repository layering; how static serving + SPA fallback compose).

These are the parent's flagged methodologies; load them as a starting point and exercise your own judgment.

## Inherited Constraints

- Compose against the REAL committed `ChirpRepository`/`ServerError` — do NOT redefine them; import wire types from `chirp-types`.
- Edition 2021 / rust 1.82 / stable; workspace lints + `clippy --all-targets -- -D warnings` clean.
- In-memory repo is the default; the server boots with no DB. SPA assets (#9) are not built yet — wire the serving path to a placeholder dir and document it.
- ALL work in the ONE shared clone; never touch `main`; no commit-attribution trailers.

## Out-of-Scope Methodologies

- Do NOT re-implement persistence or redefine the repository trait / error enum — they are the predecessor's, committed.
- Do NOT author the end-to-end integration tests or the README — those are `SUBTASK_integration_tests_and_docs`'s.
  (Thin handler-level unit checks are fine where helpful, but the API integration suite is the next spoke's.)
