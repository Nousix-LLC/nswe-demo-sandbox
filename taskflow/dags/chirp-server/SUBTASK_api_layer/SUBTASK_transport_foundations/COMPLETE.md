# COMPLETE — SUBTASK_transport_foundations

**Task:** Transport-layer foundations — error rendering, app state, auth extraction.
**Evaluation:** Atomic (one responsibility — establish the transport primitives handlers compile
against; one kind of output — committed foundational Rust + its handoff notes).
**Status:** completed.

## What was done

Implemented the three transport-layer primitives in the shared clone
(`…/chirp-server/checkout`, branch `work/chirp-server`), composing on the predecessor's **real
committed** `ServerError` enum and `ChirpRepository` trait (imported, never re-declared):

1. **`impl IntoResponse for ServerError`** — `src/error.rs`. Maps `err.code()` → `StatusCode`
   per the parent contract `error_mapping` table (Validation→400, Unauthorized→401, Forbidden→403,
   NotFound→404, Conflict→409, Internal→500) and serializes `err.into_api_error()` as the JSON
   `ApiError` body. `Internal` logs its message via `tracing::error!` but returns a generic wire
   body (no detail leak); `Validation` `details` are populated by the predecessor's
   `into_api_error()`.
2. **`AppState { repo: Arc<dyn ChirpRepository> }`** — `src/api/state.rs`. `Clone`, usable as axum
   `State`, with an `AppState::new(repo)` constructor.
3. **`AuthUser` Bearer extractor** — `src/api/auth.rs`. A `FromRequestParts<S>` extractor
   (`where AppState: FromRef<S>`) that reads `Authorization: Bearer <token>`, resolves it via
   `repo.resolve_token(&SessionToken(raw)).await` → `UserId`, and yields `AuthUser(UserId)`.
   Missing/malformed/non-Bearer/empty/unresolvable token → `ServerError::Unauthorized` (401).

Created the `src/api/` module (`mod.rs` + `state.rs` + `auth.rs`) and wired `pub mod api;` plus the
`AppState` / `AuthUser` re-exports into `src/lib.rs`. `Cargo.toml` was **not** edited (transport
deps already provisioned by the scaffold spoke).

## Verification (local gate, all clean)

| Check | Command | Result |
|-------|---------|--------|
| build | `cargo build -p chirp-server` | ✅ |
| clippy | `cargo clippy -p chirp-server --all-targets -- -D warnings` | ✅ clean |
| fmt | `cargo fmt -p chirp-server --check` | ✅ clean |
| test | `cargo test -p chirp-server` | ✅ 18 passed, 0 failed (no DB) |

`missing_docs` / `clippy::all` (workspace lints, promoted by `-D warnings`) satisfied — every public
item is documented.

## Commit

- `6f32dc0` — `feat(chirp-server): add error IntoResponse, AppState, auth extractor`
  on `work/chirp-server` (parent `6ba64d0`; `main` untouched; no attribution trailers).

## Success criteria — met

- [x] `impl IntoResponse for ServerError` maps every variant to the contract status + `ApiError`
      body (validation `details` populated).
- [x] `AppState { repo: Arc<dyn ChirpRepository> }` defined, `Clone`, usable as axum `State`.
- [x] Bearer auth extractor resolves `UserId` via `repo.resolve_token`; missing/invalid → 401.
- [x] `api` module created; `pub mod api;` added to `lib.rs`; build + clippy `-D warnings` + fmt
      `--check` clean.
- [x] Committed to `work/chirp-server`; `FOUNDATIONS_NOTES.md` written with exposed-symbol
      locations.

## Handoff

`FOUNDATIONS_NOTES.md` (this workspace) records the exposed symbols, their locations, and how a
handler names each — the input `SUBTASK_handlers` reads to compose. Out of scope and left for later
spokes: handlers, `build_router` + its `lib.rs` re-export, static/SPA, `/healthz`, tracing init,
`main.rs`.
