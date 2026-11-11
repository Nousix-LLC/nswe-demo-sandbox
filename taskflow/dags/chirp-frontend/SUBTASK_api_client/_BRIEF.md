# Task: SUBTASK_api_client — typed REST client (src/api.rs)

## Task Specification
**Slug**: SUBTASK_api_client
**Task Kind**: standard
**Status**: Pending

### Objective
Implement the real `ApiClient` (`src/api.rs`): a typed async REST client over `ferric-http`
that (de)serializes `chirp-types` DTOs, attaches the bearer token, and maps every failure to
`AppError` — exactly the seam frozen in `contracts/app_api.rs` and `contracts/rest_endpoints.md`.

### Context
Part of chirp-frontend (#9) — see `../_GLOBAL.md`. **Dependency**: `SUBTASK_scaffold` (provides
the crate, `AppError`, `AppContext`, and the compiling `api.rs` stub you replace). **Dependents**:
the synthesis gate. The feature-view spokes run in parallel with you and compose against the
frozen signatures (the scaffold stub is their L1 mock), so your public signatures MUST remain
signature-identical to `contracts/app_api.rs`.

### Inputs
- `../_GLOBAL.md`, `../contracts/app_api.rs`, `../contracts/rest_endpoints.md`, `../contracts/_MANIFEST.yaml`.
- The real `ferric-http` API (`Client`/`RequestBuilder`/`Response`/`Error`) and `chirp-types`
  DTOs in the checkout's `crates/`.

### Declared output (you own this)
- `../checkout/crates/chirp-frontend/src/api.rs` — real `ApiClient`: `new`, `with_token`, and the
  seven methods (`login`, `create_user`, `create_chirp`, `timeline`, `get_user`, `set_follow`,
  `set_like`) each hitting the one REST method+path in `rest_endpoints.md` with the declared DTOs;
  non-2xx bodies decoded into `AppError::Api(ApiError)`, `fetch` failures into `AppError::Network`,
  other failures into `AppError::Transport`. Write files only — **no git** (the gate commits).

### Success criteria
- [ ] Every method matches `rest_endpoints.md` one-to-one (method, path, request/response DTO,
      auth-header rule, `TimelineQuery` query-string building, `{id}` path interpolation).
- [ ] Error mapping decodes a `chirp_types::ApiError` from a non-2xx body; distinguishes
      network vs transport; no `unwrap`/`expect`/`panic`/`unsafe`.
- [ ] Native unit tests (off-DOM) for URL/path/query building and `AppError` decoding from a
      sample non-2xx JSON body. (No headless browser needed; `send`/`send_json` are browser-only.)
- [ ] `cargo fmt`/`clippy -D warnings` clean on the crate; public items documented.

## Suggested Methodology Files
Domain Mapping: *Writing Rust code → Rust + Core + Code Quality*; *Rust testing → Rust + Testing*.
- `rust/Rust_Error_Handling_Methodology.md` — the `AppError` mapping, `Result` discipline, no panics.
- `rust/Rust_Async_Tokio_Methodology.md` — async method shape (note: the runtime is the browser
  Fetch executor via `wasm-bindgen-futures`, not Tokio; apply the async-design parts, not the runtime parts).
- `rust/Rust_Testing_Methodology.md`, `testing/Testing_Unit_Testing_Methodology.md` — native tests for the pure logic.
- `core/BestPractices_Error_Handling_Methodology.md`.
Suggestions only; `ferric-http`'s own source is the authoritative usage reference.

## Inherited Constraints
`../_GLOBAL.md` §Subtree-Wide Constraints. Keep signatures identical to the frozen contract; use
`chirp-types` DTOs directly (no redefinition); surface errors, never panic; write files only.

## Out-of-Scope Methodologies
Not frontend/component or router methodologies (you render no UI). Not synthesis/decomposition.
