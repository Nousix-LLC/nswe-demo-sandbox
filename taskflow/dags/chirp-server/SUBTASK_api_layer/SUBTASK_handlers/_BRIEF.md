# Task: axum handlers for the full chirp-server endpoint surface

## Task Specification

**Slug**: SUBTASK_handlers
**Task Kind**: standard
**Status**: Pending

### Objective

Implement the axum handler functions for the full `repository_seam` endpoint surface over `chirp-types`
DTOs, each delegating to `ChirpRepository` through the foundations' `AppState` and auth extractor.

### Context

This task is part of the chirp-server API-layer subtree (see `../_GLOBAL.md`) — the transform stage of
the serial pipeline, and its bulk. The predecessor spoke `SUBTASK_transport_foundations` has committed
`AppState`, the Bearer auth extractor, and `impl IntoResponse for ServerError` into the shared clone;
read its `FOUNDATIONS_NOTES.md` for the exposed symbols and compose against the real committed code.
The async `ChirpRepository` trait and all DTOs are the predecessor-of-the-subtree's / `chirp-types`'
— import, never re-declare.

This brief names a **broad surface** — nine repository operations spanning three resource groups
(users/auth, chirps/timeline, social graph). That breadth is the real scope; run your own
decompose-evaluation against it. If, in your reading, translating + delegating across these nine
operations is genuinely one responsibility for one invocation, execute it; if it proves to be more
than one (e.g. the resource groups want separate ownership), decompose further rather than pushing
through — the decision is yours at dispatch, not pre-made here.

**Dependencies**: `SUBTASK_transport_foundations`.
**Dependents**: `SUBTASK_router_and_bootstrap` (mounts your handlers into `build_router`).

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, success criteria |
| Sub-contract | `../contracts/_MANIFEST.yaml` | The `endpoint_surface` you must cover, your ownership, the symbol seam |
| Parent contract | `../../contracts/_MANIFEST.yaml` | `repository_seam` semantics + `error_mapping` the handlers surface through |
| Foundations handoff | `../SUBTASK_transport_foundations/FOUNDATIONS_NOTES.md` | `AppState`, the auth extractor, the error `IntoResponse` your handlers rely on |
| Predecessor handoff | `../../SUBTASK_scaffold_and_repository/IMPLEMENTATION_NOTES.md` | Real `ChirpRepository` op signatures + behavioral contract (idempotency, errors, timeline semantics) |
| Committed code | the shared clone at the contract's `clone_path` | The real trait + foundations to compose against |
| Wire contract | `crates/chirp-types` | Request/response DTOs (import; never re-declare) |

---

## Process / Approach

Keep the layering clean: each handler translates HTTP ⇄ DTOs and delegates to the repository trait;
it does NOT re-implement persistence. Cover the full `endpoint_surface` in `../contracts/_MANIFEST.yaml`
— create/get user + profile, login, create chirp, timeline, follow/unfollow, like/unlike. Handlers
that act on behalf of a caller take the authenticated `UserId` from the foundations' extractor;
others (create_user, login) are unauthenticated. Return `Result<Json<T>, ServerError>` (or your
chosen success wrapper) and lean on the committed `IntoResponse` for error paths — `?` on a
`chirp-types::ValidationError` already yields `ServerError::Validation`. Honor the repository's
documented behavioral contract (idempotency, `NotFound`/`Conflict`/`Forbidden` conditions, the
home-timeline semantics + limit clamp + opaque cursor). Choose HTTP method + path + success status
for each endpoint (follow REST + status-code discipline) and record them. Build locally and commit to
`work/chirp-server`. Extractor usage, request/response shaping, and how you surface the timeline cursor
are your calls — document them.

### Methodology

Apply the suggested methodology below; you are the final judge of what you load.

---

## Output Specification

### Primary Output (handoff)

| Attribute | Value |
|-----------|-------|
| Filename | `HANDLERS_NOTES.md` |
| Location | this workspace (`SUBTASK_handlers/`) |

Record the **route metadata table** — for each endpoint: HTTP method, path, request DTO, response DTO,
success status, and the handler fn name/path — plus any auth requirement per route. This is exactly
what `SUBTASK_router_and_bootstrap` reads to mount the router and what the integration-test spoke will
later exercise.

### Code output

The handler functions for the full endpoint surface, committed to `work/chirp-server`.

---

## Success Criteria

- [ ] Every `endpoint_surface` operation has a handler over `chirp-types` DTOs delegating to `ChirpRepository` (no persistence re-implemented, no bypass).
- [ ] Authenticated endpoints use the foundations' extractor; unauthenticated ones (create_user, login) do not require a token.
- [ ] Error paths surface through the committed `IntoResponse` (validation `details` populated); the repository's documented error/idempotency/timeline semantics are honored.
- [ ] `cargo build -p chirp-server` + `clippy --all-targets -- -D warnings` + `fmt --check` clean.
- [ ] Committed to `work/chirp-server`; `HANDLERS_NOTES.md` written with the full route-metadata table.

---

## Suggested Methodology Files

Matched Domain-Mapping rows: **Writing Rust code → primary `rust`; supporting `core`** and
**API design → `architecture`.** Load via `engine_load_methodology { name: "<bundle_id>" }`.

- `rust` — `rust/Rust_Async_Tokio_Methodology.md` (axum async handler design over tokio),
  `rust/Rust_Error_Handling_Methodology.md` (`?` / error-as-value through `ServerError`),
  `rust/Rust_Type_System_Methodology.md` (extractors / typed request+response).
- `architecture` — `architecture/Architecture_API_Design_Methodology.md` (REST surface, method/path/status-code discipline).
- `core` — `core/BestPractices_Coding_Standards_Methodology.md`, `core/BestPractices_Error_Handling_Methodology.md`, `core/CodeManagement_Commit_Practices_Methodology.md`.

These are the parent's flagged methodologies; load them as a starting point and exercise your own judgment.

## Inherited Constraints

- Compose against the REAL committed `ChirpRepository`, `ServerError`/`IntoResponse`, and `AppState`/extractor; import DTOs from `chirp-types`. Re-declare nothing.
- Handlers are `async`, `.await` the repo, and hold nothing across the await beyond what the repo already does internally.
- `timeline` is a HOME timeline (self + followees); a per-user profile feed, if routed, is a thin derivation — not a repository change.
- Edition 2021 / rust 1.82 / stable; `clippy --all-targets -- -D warnings` clean. ONE shared clone; branch `work/chirp-server`; never touch `main`; no commit-attribution trailers. Do NOT edit `Cargo.toml`.

## Out-of-Scope Methodologies

- Do NOT assemble the router, static serving, SPA fallback, `/healthz`, tracing init, or `main.rs` — that is `SUBTASK_router_and_bootstrap`. (Register routes by naming method+path in your notes; the router spoke mounts them.)
- Do NOT author the end-to-end integration tests — that is the next sibling at the parent level. Thin handler-level unit checks are fine where genuinely helpful.
