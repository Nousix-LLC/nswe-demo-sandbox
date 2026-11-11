# Task: SUBTASK_scaffold — chirp-frontend walking skeleton + composition root

## Task Specification
**Slug**: SUBTASK_scaffold
**Task Kind**: standard
**Status**: Pending

### Objective
Establish the `crates/chirp-frontend` crate skeleton and prove the end-to-end path: the SPA
**builds for `wasm32-unknown-unknown` and mounts**, with the composition root (shared state,
router, nav, mount entry) in place and every feature module pre-mounted behind the frozen
contract via compiling stubs.

### Context
Part of chirp-frontend (#9) — see `../_GLOBAL.md`. You are the **Group-0 walking skeleton** of
a contract-first fan-out: you own the composition root and the mount points; the feature spokes
(`api_client`, `timeline`, `compose`, `profile`) fill in their modules behind the seam you
realize. **Dependencies**: none. **Dependents**: all other subtasks.

### Inputs
- `../_GLOBAL.md`, `../contracts/_MANIFEST.yaml`, `../contracts/app_api.rs`, `../contracts/rest_endpoints.md`.
- The landed crates' real APIs (ground truth): `ferric`, `ferric-router`, `ferric-http`,
  `chirp-types` — study their `src/` and `examples/` (the ferric `counter` and ferric-router
  `app` examples show the real mount/router/outlet/nav/`spawn_local`-free patterns).
- A reference checkout at `main` @ `25e90c0` (has all four crates):
  `../../chirp-server/checkout` (and origin `https://github.com/Nousix-LLC/nswe-demo.git`).

### Declared outputs (you own these; see manifest)
Into the shared checkout at `../checkout/` (which you establish) under `crates/chirp-frontend/`:
- `Cargo.toml` — new workspace member; path-deps on the four crates; reuse `[workspace.dependencies]`;
  add `wasm-bindgen-futures` and any extra `web-sys` features additively; `[lints] workspace = true`.
- `src/lib.rs` — declares every module (`api`, `app`, `error`, `timeline`, `compose`, `profile`).
- `src/app.rs` — the composition root realizing `contracts/app_api.rs`: `Session`, `AppContext`
  (+ `new`, `client()`), the `Router` route table (`/`→`timeline_view`, `/compose`→`compose_view`,
  `/user/:id`→`profile_view`, + fallback), the reactive outlet, a persistent nav (`link`s), and
  the wasm mount entry (`start()`/`main`) that mounts into `#app`/`<body>`.
- `src/error.rs` — `AppError` (+ `from_http`, `user_message`, `code`) decoding a `chirp_types::ApiError`
  out of a non-2xx `ferric_http::Error::Status` body.
- `src/api.rs`, `src/timeline.rs`, `src/compose.rs`, `src/profile.rs` — **minimal compiling
  stubs** that satisfy the frozen signatures in `contracts/app_api.rs` and return empty/`Err`
  values (NEVER panic / `todo!`), so the skeleton builds for wasm and the app mounts. The owning
  feature spoke replaces each of these.
- `index.html` — a static harness demonstrating the app mounts (a `#app` mount point + the
  generated wasm/JS glue, or a documented `trunk`/`wasm-bindgen` invocation).
- `README.md` — what the crate is, how to build for wasm, how to set the API base URL.
- Establish `../checkout/` from `main` @ `25e90c0` on a fresh branch `work/chirp-frontend`, and
  make the **initial skeleton commit** (you are sole in Group 0; no attribution trailer).

### Success criteria
- [ ] `cd ../checkout && cargo build -p chirp-frontend --target wasm32-unknown-unknown` succeeds.
- [ ] `cargo fmt --all --check` and `cargo clippy -p chirp-frontend --all-targets -- -D warnings` clean.
- [ ] `src/` signatures are signature-identical to `contracts/app_api.rs` (feature spokes will
      compile against them).
- [ ] The route table binds the three frozen view fns + a fallback; nav + outlet render.
- [ ] Stubs return empty/`Err`, never panic; no `unsafe`; public items documented.
- [ ] Branch `work/chirp-frontend` exists off `25e90c0` with the skeleton committed.

## Suggested Methodology Files
Domain Mapping rows: *Frontend architecture design → Frontend + Architecture*; *Writing Rust
code → Rust + Core + Code Quality*. (This child is Rust + composition-root architecture.)
- `rust/Rust_Cargo_Ecosystem_Methodology.md` — workspace-member crate, path-deps, feature wiring.
- `rust/Rust_Trait_Design_Methodology.md`, `rust/Rust_Type_System_Methodology.md` — realize the frozen `AppContext`/`ApiClient`/view-fn surface cleanly.
- `rust/Rust_Error_Handling_Methodology.md` — `AppError` + `From<ferric_http::Error>`, no panics.
- `architecture/Architecture_Design_Patterns_Methodology.md` — composition root / mount-point pattern (pre-mount seams, spokes fill behind them).
- `core/BestPractices_Coding_Standards_Methodology.md`, `core/BestPractices_Error_Handling_Methodology.md`.
These are suggestions — load what the work needs; the landed crates' source/examples are the authoritative composition reference.

## Inherited Constraints
All of `../_GLOBAL.md` §Subtree-Wide Constraints. Specifically: you OWN the composition root,
`Cargo.toml`, `lib.rs`, and the initial stubs + the branch/commit; the feature spokes own and
replace their module files. Keep stubs minimal and non-panicking. Default API base URL `/api`
(configurable). You MAY `expect()` only in the thin mount entry (documented).

## Out-of-Scope Methodologies
Not the decomposition bundle (decomposer-side only). Not synthesis (that is the gate). Do not
implement real feature behaviour (timeline/compose/profile/api bodies) — only stubs; the spokes do that.
