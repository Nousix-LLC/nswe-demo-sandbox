# COMPLETE — SUBTASK_scaffold_and_repository

**Task:** Scaffold `crates/chirp-server` in the shared clone and deliver its persistence layer
(`ChirpRepository` trait + `ServerError` enum + in-memory impl + unit tests), committed to
`work/chirp-server`.

**Decompose-evaluation:** Atomic — one responsibility (the persistence layer of one crate), one
coherent output; tightly-coupled serial facets (trait → error enum → in-memory impl → self-tests)
that no parallel specialists could split. Executed in a single invocation.

## What was produced

- **Clone + branch:** `checkout/` clone created at the contract's `clone_path`; `work/chirp-server`
  cut off `main`. Commit `6ba64d0`.
- **`crates/chirp-server`** workspace member (auto-included by the `crates/*` glob):
  - `Cargo.toml` — crate manifest + full dependency set provisioned for downstream spokes.
  - `src/lib.rs` — crate-root skeleton: `error` + `repository` module declarations and re-exports;
    documented seam where the api-layer adds the router/binary.
  - `src/error.rs` — `ServerError` enum (`thiserror`, `#[non_exhaustive]`), `#[from] ValidationError`,
    HTTP-free `code()` / `into_api_error()` helpers onto `chirp-types` `ApiError`/`ErrorCode`.
  - `src/repository/mod.rs` — the `ChirpRepository` async, object-safe trait (full capability seam)
    + timeline limit constants.
  - `src/repository/in_memory.rs` — `InMemoryRepository` default backing + 18 unit tests.
- **`IMPLEMENTATION_NOTES.md`** — handoff for `SUBTASK_api_layer`: final trait signature, error
  enum + mapping recipe, module layout, concurrency choice + rationale, clone/branch pointers, and
  local verification status.

## Success criteria — all met

- [x] Clone at the contract `clone_path`; branch `work/chirp-server` off `main`.
- [x] `crates/chirp-server` is a workspace member; `cargo build -p chirp-server` succeeds.
- [x] `ChirpRepository` covers every `repository_seam` operation (create/get user, handle-based
      login + token resolution, create chirp, home timeline w/ cursor pagination, follow/unfollow,
      like/unlike), typed over `chirp-types`; `resolve_token` added to satisfy the contract's
      `auth_note` (api-layer resolves bearer tokens through the trait).
- [x] `ServerError` enum lines up with the contract's `error_mapping` table (api-layer adds
      `IntoResponse`).
- [x] In-memory impl maintains denormalized follower/following/like counts and the documented
      invariants (no self-follow, at-most-one-like-per-pair, reverse-chronological timeline);
      repository unit tests pass with no database.
- [x] Work committed to `work/chirp-server`; `IMPLEMENTATION_NOTES.md` written.

## Verification (all clean)

| Check | Command | Result |
|-------|---------|--------|
| build (pkg) | `cargo build -p chirp-server` | ✅ |
| build (workspace) | `cargo build --workspace` | ✅ |
| test | `cargo test -p chirp-server` | ✅ 18 passed / 0 failed (no DB) |
| fmt | `cargo fmt -p chirp-server --check` | ✅ clean |
| clippy | `cargo clippy -p chirp-server --all-targets -- -D warnings` | ✅ clean |

## Constraints honored

- Edition 2021 / rust-version 1.82; inherits `[lints] workspace = true`; `clippy -D warnings` clean.
- All wire types imported from `chirp-types` via the path dependency — **no DTO re-declared**.
- In-memory default; no database required for build or test.
- HTTP-free: no axum handlers, routing, `IntoResponse`, static serving, health endpoint, `tracing`,
  or `main.rs` (all deferred to the api-layer spoke).
- Single shared clone; `main` never committed to or force-pushed; **no commit-attribution trailers**.

## Boundary notes for downstream

- `timeline` is a **home** timeline (self + followees). A per-user profile feed, if the acceptance
  surface needs one, is a thin api/service-layer derivation on top of the repository.
- The api-layer's `IntoResponse` maps `ServerError::code()` → `StatusCode` per the error table and
  serializes `into_api_error()`; the auth extractor resolves bearer tokens via `resolve_token`.
