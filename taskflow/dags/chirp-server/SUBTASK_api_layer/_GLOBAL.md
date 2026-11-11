# chirp-server API layer — transport/service subtree (hub)

## Project Context

**Status**: Active (decomposed; awaiting subtree resolution)

This is the decomposition of **`SUBTASK_api_layer`** — the HTTP transport/service layer of
`crates/chirp-server` (work-item #8 of `Nousix-LLC/nswe-demo`). The parent subtree hub is
`../_GLOBAL.md`; the frozen conventions, repository-trait seam, and error-mapping table are in
`../contracts/_MANIFEST.yaml`. The predecessor (`../SUBTASK_scaffold_and_repository`) has committed
the crate skeleton, the **async `ChirpRepository` trait** (object-safe via `async-trait`, held as
`Arc<dyn ChirpRepository>`), the **`ServerError` enum** with HTTP-free `code()` / `into_api_error()`
helpers, and the in-memory impl — all in the shared clone. Its handoff is
`../SUBTASK_scaffold_and_repository/IMPLEMENTATION_NOTES.md`.

### Why this task decomposed

`SUBTASK_api_layer` enumerates several genuinely distinct responsibilities — per-endpoint HTTP⇄DTO
handlers, typed-error→HTTP response mapping, router/static/SPA composition, and the server bootstrap
binary — whose combined Rust output is ~500–600 lines. The Scope-Based trigger, the
Single-Responsibility Test, and the Output-Size trigger all fire; by trigger precedence the task is
not atomic. The pieces are coupled (handlers must compile against the error `IntoResponse`, the shared
`AppState`, and the auth extractor; the router mounts the handlers; `main` wires the router), so the
decomposition is a **serial pipeline**, not a parallel fan-out — which also respects the subtree-wide
rule that the single shared clone is written serially.

### Objective

Deliver the axum transport/service layer committed to `work/chirp-server`: handlers for the full
`repository_seam` endpoint surface over `chirp-types` DTOs delegating to `ChirpRepository`,
`impl IntoResponse for ServerError` per the contract error-mapping table, `build_router` + `AppState`
exposed from `lib.rs`, static-file service + SPA fallback, `GET /healthz`, `tracing` structured
logging, and `main.rs` — and the `API_NOTES.md` handoff the integration-test spoke reads.

### Scope

**In scope:** everything owned by `SUBTASK_api_layer` in `../contracts/_MANIFEST.yaml §ownership`
(handlers, router, `AppState`, error `IntoResponse`, static+SPA serving, `/healthz`, tracing,
`main.rs`), built and committed into the one shared clone; plus the `API_NOTES.md` handoff and a
subtree verification gate.

**Out of scope:** redefining the repository trait or `ServerError` enum (predecessor's, committed —
import/extend only); the end-to-end integration test suite and the crate `README.md` (the next
sibling `../SUBTASK_integration_tests_and_docs`); the PR into `main` and the authoritative full
`cargo test` / four-check parent gate (the parent's `../SUBTASK_synthesis_gate`); building the real
SPA (#9 — wire serving to a placeholder dir and document it).

### Success Criteria

- [ ] Every `repository_seam` endpoint is routed over `chirp-types` DTOs and delegates to `ChirpRepository` (no bypass).
- [ ] `ServerError` → `ApiError` + HTTP status matches `../contracts/_MANIFEST.yaml §error_mapping` (validation `details` populated).
- [ ] Static-file service + SPA fallback wired to a placeholder static dir; `GET /healthz` returns a health response.
- [ ] `tracing` initialized with a request-trace layer; `main.rs` builds state + router and serves.
- [ ] `build_router` (app builder) exposed from `lib.rs`; `cargo build -p chirp-server` + `cargo clippy -p chirp-server --all-targets -- -D warnings` + `cargo fmt -p chirp-server --check` clean.
- [ ] Code committed to `work/chirp-server`; `API_NOTES.md` written at the `SUBTASK_api_layer/` workspace (the fold location).

---

## Constraints and Requirements

Inherited from `../_GLOBAL.md` and `../contracts/_MANIFEST.yaml`; descendants conform and do not re-litigate:

- **Compose against the REAL committed code.** Import `ChirpRepository`, `ServerError`,
  `InMemoryRepository`, and `code()` / `into_api_error()` from the predecessor's committed modules;
  import ALL wire types (`User`, `Chirp`, `CreateUserRequest`, `LoginRequest`, `AuthResponse`,
  `SessionToken`, `CreateChirpRequest`, `TimelineQuery`, `Page`, `FollowResponse`, `LikeResponse`,
  `ApiError`, `ErrorCode`, `ValidationError`, `UserId`, `ChirpId`, …) from `chirp-types`. **Never
  re-declare a DTO, the trait, or the error enum.**
- **Edition 2021 / rust 1.82 / stable**; inherit workspace `[lints]`; additionally satisfy
  `clippy --all-targets -- -D warnings`.
- **In-memory repo is the default; the server boots with no DB.** SPA assets (#9) are not built —
  wire the serving path to a placeholder static dir and document it.
- **ALL work in the ONE shared clone** at `../checkout` (`clone_path` in the contract), branch
  `work/chirp-server`. Never touch or push `main`. **No commit-attribution trailers.** The clone is
  serially shared — the dependency chain below guarantees no two children write it concurrently.
- The deps the transport layer needs (`axum 0.8`, `tower 0.5`, `tower-http 0.6` `{fs,trace}`,
  `tracing`, `tracing-subscriber` `{env-filter}`, `tokio` `{rt-multi-thread,macros,net,signal}`) are
  already provisioned in `Cargo.toml` by the scaffold spoke — children do NOT edit the manifest.

---

## Subtree Methodology Posture

- **Dominant task type**: *Writing Rust code* (axum transport) → primary bundle **`rust`**; plus
  **`core`** (coding standards, error handling, commit practices) and **`architecture`** (the
  transport→service→repository layering; REST API shape; how static serving + SPA fallback compose).
  The terminal gate is *Synthesizing/verifying a hub-and-spoke decomposition* → **`synthesis`**
  (+ **`code-review`**).
- **Primary bundles in scope subtree-wide**: `rust`, `core`, `architecture` for the three
  implementation spokes; `synthesis`, `code-review` for the gate. Descendants may assume these
  without re-justifying, and each re-runs its OWN decompose-evaluation.
- **Cross-cutting bindings** (bind every leaf even though one leaf owns each): the error discipline
  is **typed `ServerError` → `code()`/`into_api_error()` → `ApiError`/`ErrorCode` → HTTP status**
  per the contract table; the persistence seam is the **async `ChirpRepository` behind
  `Arc<dyn …>`**; `chirp-types` is the single source of truth for wire types. Handlers are `async`,
  `.await` the repo, and hold nothing across the await beyond what the repo already does.
- **Suggestion, not prescription**: descendants retain final judgment over what methodology they load.

## Subtree-Wide Constraints

- The symbol-level seam below (what each child exposes for the next) and the module ownership in
  `contracts/_MANIFEST.yaml` are fixed; a child MAY refine internal module names but MUST preserve
  the lib/bin split and the exposed symbols so the next child composes.
- Shared files touched by more than one child (`src/lib.rs`, `src/error.rs`, `src/api/mod.rs`) are
  edited **serially** along the dependency chain — never concurrently.

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/_MANIFEST.yaml                 (ownership + symbol seam + identities the gate asserts)
├── SUBTASK_transport_foundations/_BRIEF.md  (error IntoResponse + AppState + Bearer auth extractor; commit)
├── SUBTASK_handlers/_BRIEF.md               (axum handlers for the full endpoint surface over DTOs; commit)
├── SUBTASK_router_and_bootstrap/_BRIEF.md   (build_router + static/SPA + /healthz + tracing + main.rs; commit)
└── SUBTASK_api_synthesis/_BRIEF.md          (verification gate; API_NOTES.md + SYNTHESIS.md at this hub)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_transport_foundations` | none | Implement `impl IntoResponse for ServerError` (error→`ApiError` JSON + HTTP status per the contract table), the `AppState { repo: Arc<dyn ChirpRepository> }` shared-state type, and the `Authorization: Bearer` auth extractor that resolves a `UserId` via `repo.resolve_token`. Build + commit. | `SUBTASK_transport_foundations/FOUNDATIONS_NOTES.md` (exposed symbols + their locations) + committed code |
| `SUBTASK_handlers` | `SUBTASK_transport_foundations` | axum handler functions for the full `repository_seam` surface (create/get user + profile, login, create chirp, timeline, follow/unfollow, like/unlike) over `chirp-types` DTOs, delegating to `ChirpRepository`, using the foundations' `AppState`/extractor/error mapping. Build + commit. | `SUBTASK_handlers/HANDLERS_NOTES.md` (route metadata: method+path+request DTO+response DTO+status+handler fn) + committed code |
| `SUBTASK_router_and_bootstrap` | `SUBTASK_handlers` | `build_router(state)` mounting all handlers + `GET /healthz` + static `ServeDir` + SPA fallback, exposed from `lib.rs`; `tracing` init + request-trace layer; `main.rs` (init tracing, build state+router, bind, serve). Build + commit. | `SUBTASK_router_and_bootstrap/BOOTSTRAP_NOTES.md` (router shape, serving/fallback wiring, run instructions) + committed code |
| `SUBTASK_api_synthesis` | `SUBTASK_transport_foundations`, `SUBTASK_handlers`, `SUBTASK_router_and_bootstrap` | **Verification gate** (Task Kind: synthesis): run the four-check model (contract/wiring/dedup/review) over the combined api-layer output + authoritative `cargo build -p chirp-server` / `clippy -D warnings` / `fmt --check`; author the `API_NOTES.md` handoff; record PASS/FAIL; schedule remediation fix-tasks on FAIL rather than green-washing. | `SYNTHESIS.md` + `API_NOTES.md` at the `SUBTASK_api_layer/` workspace (fold location) |

### Dependency Graph

```
SUBTASK_transport_foundations ──► SUBTASK_handlers ──► SUBTASK_router_and_bootstrap ──► SUBTASK_api_synthesis
```

---

## Contract

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (ownership + symbol-level seam + the identities the gate asserts)

The cross-sibling edges in this subtree are **serialized** by the dependency chain (each spoke reads
the real committed clone produced by its predecessor), so the shared symbols (`AppState`, the auth
extractor, `IntoResponse`, the handler set, `build_router`) are NOT frozen here as compilable Rust —
the consumer reads the real committed code. What the manifest DOES freeze before any child runs:
(1) per-child **ownership** (every artifact has exactly one producer); (2) the **symbol seam** (what
each child exposes for the next so the pipeline composes with no gap); and (3) the **identities** the
synthesis gate asserts. See `contracts/_MANIFEST.yaml`. This sub-contract **extends** the parent
`../contracts/_MANIFEST.yaml` (same `error_mapping` table and `repository_seam`); it MUST NOT
override it.

### Identities (the gate asserts; no silent plug)

- [ ] Every `repository_seam` operation has exactly one routed, reachable handler delegating through `ChirpRepository`.
- [ ] `ServerError` → HTTP status + `ErrorCode` matches `../contracts/_MANIFEST.yaml §error_mapping` for every variant.
- [ ] No DTO / trait / error type re-declared in `chirp-server` (all imported from `chirp-types` / the predecessor's modules).
- [ ] `build_router` is exposed from `lib.rs`; `cargo build -p chirp-server`, `clippy --all-targets -D warnings`, `fmt --check` clean.
- [ ] No detached dead code (every handler is mounted; every helper is reachable).

---

## Output Specifications

| Deliverable | Location | Description |
|-------------|----------|-------------|
| Foundations code + notes | committed to `work/chirp-server`; `SUBTASK_transport_foundations/FOUNDATIONS_NOTES.md` | error `IntoResponse`, `AppState`, auth extractor |
| Handlers code + notes | committed to `work/chirp-server`; `SUBTASK_handlers/HANDLERS_NOTES.md` | handlers + route metadata |
| Router/bootstrap code + notes | committed to `work/chirp-server`; `SUBTASK_router_and_bootstrap/BOOTSTRAP_NOTES.md` | `build_router`, serving, tracing, `main.rs` |
| API-layer handoff | `SUBTASK_api_layer/API_NOTES.md` (this workspace) | route table, `AppState` design, error→HTTP mapping as implemented, static/SPA wiring, run instructions, local build status — read by `../SUBTASK_integration_tests_and_docs` |
| Verdict / fold record | `SUBTASK_api_layer/SYNTHESIS.md` (this workspace, fold location) | four-check + build/clippy/fmt verdict, PASS/FAIL |
