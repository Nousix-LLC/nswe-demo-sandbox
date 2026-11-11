# COMPLETE — SUBTASK_scaffold (chirp-frontend walking skeleton + composition root)

**Task kind:** standard (Group-0 walking skeleton) · **Evaluation:** Atomic · **Status:** completed

## What was done

Established the `crates/chirp-frontend` workspace member in the shared checkout and realized the
frozen `contracts/app_api.rs` surface in `src/` as a **compiling walking skeleton that builds for
`wasm32-unknown-unknown` and mounts**. This resumed a partially-scaffolded node: the checkout,
branch, `Cargo.toml`, and `src/lib.rs` already existed; this invocation authored the missing
composition root, error type, compiling stubs, wasm entry, harness, and README, then made the
initial skeleton commit.

### Resumed-state assessment (at boot)
- Branch `work/chirp-frontend` already existed off `main @ 25e90c0`; `crates/chirp-frontend/`
  held only `Cargo.toml`, `src/lib.rs` (declaring six modules), and an empty `examples/`.
- No module files, no `index.html`/`README.md`, and **no commit** (the crate was untracked). The
  lib would not compile until the declared modules existed. This invocation finished all of that.

### Files authored/completed (owned by SUBTASK_scaffold; in `../checkout/crates/chirp-frontend/`)
- `Cargo.toml` — workspace member; path-deps on `ferric`, `ferric-router`, `ferric-http`,
  `chirp-types`; reuses `[workspace.dependencies]`; adds `wasm-bindgen-futures` + additive
  `web-sys` features; `[lints] workspace = true`. (pre-existing; verified correct)
- `src/lib.rs` — module root declaring `api`, `app`, `compose`, `error`, `profile`, `timeline`
  and re-exporting `app::start`. (pre-existing; verified correct)
- `src/app.rs` — composition root: `Session`, `AppContext` (+ `new`, `client`), the `Router`
  route table (`/`→`timeline_view`, `/compose`→`compose_view`, `/user/:id`→`profile_view`, +
  fallback), persistent nav (`link`s), reactive outlet, and the thin wasm mount entry `start()`
  (mounts into `#app`, falling back to `<body>`). Build-time `CHIRP_API_BASE_URL` override;
  default base `/api`.
- `src/error.rs` — real `AppError` (`from_http`/`user_message`/`code` + `From<ferric_http::Error>`)
  decoding a `chirp_types::ApiError` out of a non-2xx `ferric_http::Error::Status` body; 4 native
  unit tests.
- `src/api.rs`, `src/timeline.rs`, `src/compose.rs`, `src/profile.rs` — minimal, non-panicking
  compiling stubs behind the frozen signatures (API methods return `Err(AppError::Transport(..))`;
  views render placeholders). Each is replaced by its owning feature spoke.
- `examples/chirp.rs` — wasm entry binary calling `chirp_frontend::start()`.
- `index.html` — static harness with a `#app` mount point and the wasm/JS glue.
- `README.md` — crate overview, wasm build + wasm-bindgen invocation, and API-base-URL config.
- Initial skeleton commit `abee995` on `work/chirp-frontend` (off `25e90c0`); `Cargo.lock` updated
  by Cargo and committed. **No attribution trailer** (per `_GLOBAL.md` §6).

## Verification (all green)
- `cargo build -p chirp-frontend --target wasm32-unknown-unknown` — succeeds (lib).
- `cargo build -p chirp-frontend --example chirp --target wasm32-unknown-unknown` — succeeds.
- `cargo fmt --all --check` — clean.
- `cargo clippy -p chirp-frontend --all-targets -- -D warnings` — clean; `cargo clippy --workspace
  --all-targets -- -D warnings` — clean.
- `cargo test -p chirp-frontend` — 4 passed, 0 failed.

## Contract identities satisfied by the skeleton
- `wasm_target_builds` ✓ · `workspace_quality_clean` ✓ (fmt/clippy/tests) ·
  `dtos_used_not_redefined` ✓ (no parallel DTO structs/enums; grep clean) ·
  `routes_bind_frozen_views` ✓ (route table binds the three frozen view fns + fallback) ·
  `no_panic_no_unsafe_in_runtime` ✓ (the only `expect()`s are the documented mount-point
  acquisition in `start()`, the thin wasm entry; test code aside — no `unwrap`/`panic!`/`todo!`/
  `unimplemented!`/`unsafe` in runtime modules). The combined-tree identities
  (`every_client_method_one_endpoint`, `errors_surface_to_ui`) are the feature spokes' + gate's.

## Handoff to the feature spokes (Group 1)
The scaffold stubs ARE the L1 (shape-only) mocks the spokes compile against. Each spoke
**replaces** exactly one file it owns — `SUBTASK_api_client`→`src/api.rs`,
`SUBTASK_timeline`→`src/timeline.rs`, `SUBTASK_compose`→`src/compose.rs`,
`SUBTASK_profile`→`src/profile.rs` — writing files only (no git). The synthesis gate performs all
remaining git (stage/commit, final build/test/fmt/clippy, PR `Closes #9`).
