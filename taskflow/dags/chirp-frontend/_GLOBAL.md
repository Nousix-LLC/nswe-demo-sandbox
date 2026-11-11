# chirp-frontend (#9) — subtree hub (_GLOBAL.md)

## Project Context

**Status**: Active

### Objective

Build **`crates/chirp-frontend`** — the chirp Twitter-style client **SPA**, a client-side
**WASM** app on the landed `ferric` framework, composing the landed `chirp-types` REST
contract. Deliver as a PR into `main` on branch **`work/chirp-frontend`**, `Closes #9`,
behind a terminal **Synthesis verification gate** that folds the subtree.

### Scope

**In scope:** a new workspace-member crate `crates/chirp-frontend` building for
`wasm32-unknown-unknown`; a coherent SPA — timeline (`Page<Chirp>` pagination), compose-chirp
form (login + create-chirp), user/profile route (`/user/:id`), follow/like actions — each
wired through `ferric-http` to the `chirp-types` REST endpoints with reactive re-render via
`ferric` signals; loading/error handling surfacing `ApiError`/`ErrorCode`; a wasm mount
entry + static `index.html` harness; native unit tests where logic is off-DOM; README +
rustdoc; `fmt`/`clippy -D warnings` clean.

**Out of scope:** re-implementing any framework crate (`ferric`/`ferric-router`/`ferric-http`)
or redefining any `chirp-types` DTO; building or build-depending on `chirp-server` #8 (it is a
parallel work-item, called at runtime over HTTP via the `chirp-types` contract); a headless
browser test runner (`wasm-bindgen-test` compile-only is acceptable, documented — not a FAIL,
mirroring the ferric/ferric-router precedent).

### Success criteria

- [ ] `cargo build -p chirp-frontend --target wasm32-unknown-unknown` succeeds (combined tree).
- [ ] `cargo fmt --all --check` clean; `cargo clippy --workspace --all-targets -- -D warnings` clean.
- [ ] `cargo test -p chirp-frontend` passes (native, off-DOM logic).
- [ ] The SPA mounts and renders; timeline/compose/profile + follow/like are wired to the
      REST endpoints via `ferric-http`, reactive via signals, with loading/error states.
- [ ] No `unwrap`/`expect`/`panic!`/`todo!`/`unsafe` in library/runtime modules (thin wasm
      mount entry MAY `expect()` for mount-point acquisition, documented).
- [ ] PR opened into `main` on `work/chirp-frontend`, `Closes #9`; no attribution trailer.

## Inputs (landed dependencies — all on `main` @ `25e90c0`)

The repo at current `main` includes the four dependency crates. A known-good local checkout
at that commit is available to clone/copy from:

- Reference checkout (main @ `25e90c0`, has `crates/{ferric,ferric-router,ferric-http,chirp-types}`):
  `/home/user/nousix-runtime/nswe-demo/taskflow/dags/chirp-server/checkout`
- Origin: `https://github.com/Nousix-LLC/nswe-demo.git`
- Root `Cargo.toml` already globs `members = ["crates/*"]` and defines
  `[workspace.dependencies]` (wasm-bindgen, js-sys, web-sys, wasm-bindgen-test) and
  `[workspace.lints]` (missing_docs=warn, unsafe_code=warn, clippy::all=warn).

Read the actual public APIs in those crates; they are summarized in `contracts/` but the
crates are the ground truth.

## Shared checkout

A single working clone lives at **`chirp-frontend/checkout/`** (established by
`SUBTASK_scaffold` off `main` @ `25e90c0` on branch `work/chirp-frontend`). All spokes write
the new crate's files there under `crates/chirp-frontend/`.

## Task Structure

```
chirp-frontend/
├── _GLOBAL.md                      (this hub)
├── contracts/                      (FROZEN seam — read-only to all spokes)
│   ├── _MANIFEST.yaml              (kind, ownership, identities, derived mocks)
│   ├── app_api.rs                  (frozen in-crate Rust signatures)
│   └── rest_endpoints.md           (REST method+path ⇄ DTO map; #8 assumptions)
├── checkout/                       (shared working clone on work/chirp-frontend)
├── SUBTASK_scaffold/_BRIEF.md
├── SUBTASK_api_client/_BRIEF.md
├── SUBTASK_timeline/_BRIEF.md
├── SUBTASK_compose/_BRIEF.md
├── SUBTASK_profile/_BRIEF.md
└── SUBTASK_synthesis_gate/_BRIEF.md
```

### Task Summary (authoritative DAG)

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_scaffold` | none | Walking skeleton: establish checkout+branch; crate manifest; module layout; composition root (`AppContext`/`Session`/Router route table/outlet/nav/mount entry); `error.rs` (`AppError`); `index.html`; README; **compiling stubs** of `api.rs`/`timeline.rs`/`compose.rs`/`profile.rs` so the skeleton builds for wasm and mounts. Realizes `contracts/app_api.rs` in `src/`. | crate skeleton in `checkout/crates/chirp-frontend/` (builds for wasm; mounts) |
| `SUBTASK_api_client` | `SUBTASK_scaffold` | Real `src/api.rs`: `ApiClient` over `ferric-http` + `chirp-types`, all 7 methods per `rest_endpoints.md`, `AppError` mapping incl. decoding server `ApiError`. Native tests for URL/path building + error decoding. | `src/api.rs` |
| `SUBTASK_timeline` | `SUBTASK_scaffold` | Real `src/timeline.rs`: timeline view — load `Page<Chirp>`, keyed reactive list, loading/error/empty, cursor pagination. | `src/timeline.rs` |
| `SUBTASK_compose` | `SUBTASK_scaffold` | Real `src/compose.rs`: handle-based login (sets `ctx.session`) + validated compose-chirp form (`create_chirp`), loading/error. | `src/compose.rs` |
| `SUBTASK_profile` | `SUBTASK_scaffold` | Real `src/profile.rs`: `/user/:id` profile (load `User`, counts) + follow/unfollow + like actions with reactive count updates. | `src/profile.rs` |
| `SUBTASK_synthesis_gate` | `SUBTASK_scaffold`, `SUBTASK_api_client`, `SUBTASK_timeline`, `SUBTASK_compose`, `SUBTASK_profile` | **Verification gate** (Task Kind: synthesis): build workspace incl. wasm target, run tests/fmt/clippy, PASS/FAIL verdict + diff manifest + contract/wiring checks; commit + open PR `Closes #9`; write `SYNTHESIS.md` and fold. | `SYNTHESIS.md` (+ PR) |

### Dependency graph

```
                 ┌── SUBTASK_api_client ──┐
SUBTASK_scaffold ┼── SUBTASK_timeline  ───┼── SUBTASK_synthesis_gate
                 ├── SUBTASK_compose   ───┤
                 └── SUBTASK_profile   ───┘
```

## Contract

**Location**: `contracts/` (read-only for every descendant). **Kind**: `rust_api` (frozen
Rust signatures) + endpoint map. This is the load-bearing seam: `SUBTASK_scaffold` realizes
`app_api.rs` in `src/` as the compiling skeleton and pre-mounts the three route views; the
feature spokes import the frozen signatures from `crate::...` and fill their module behind the
seam, composing against the scaffold stubs (the L1 mocks) during Group-1 execution. The gate
verifies the real combined tree against the manifest's identities. See
`contracts/_MANIFEST.yaml` for ownership, identities, and derived mocks;
`contracts/rest_endpoints.md` for the wire contract. The chirp-types DTOs are an external
contract used directly and never redefined.

## Subtree Methodology Posture

- **Dominant task type**: *Writing Rust code* (a WASM SPA). Most leaves draw on **rust** +
  **core** (+ **code-quality** for module design). The gate leaf is *synthesizing/verifying a
  hub-and-spoke decomposition* → **synthesis** (+ **testing**, **code-review**).
- **Primary bundles in scope subtree-wide** (assume without re-justification): `rust`, `core`.
  Add per task type: `architecture` (scaffold's module/composition design), `testing`
  (api-client + gate), `synthesis` (gate only).
- **Cross-cutting bindings** (bind every leaf): the frozen `contracts/`; the four landed
  crates' real APIs as the composition surface; `Rust_Error_Handling_Methodology` discipline
  (no panics in runtime code — errors via `Result`/`AppError`/UI state).
- Suggestion, not prescription: each leaf agent is the final judge of what it loads; load
  fewer if clearly inapplicable, more if the brief reveals additional surface.

## Subtree-Wide Constraints (inherited by every descendant)

1. **Compose, do not re-implement.** `ferric`, `ferric-router`, `ferric-http` are path-deps;
   `chirp-types` DTOs are the wire contract used directly. Redefining any of them is a defect.
2. **Stack is fixed**: Rust, `wasm32-unknown-unknown`; reuse `[workspace.dependencies]`
   (serde, serde_json, wasm-bindgen, js-sys, web-sys) rather than re-pinning; add
   `wasm-bindgen-futures` for `spawn_local` (the fetch→signal async bridge) and any extra
   `web-sys` features additively.
3. **Reactivity model**: data loads/actions are async; drive them with
   `wasm_bindgen_futures::spawn_local` that writes `ferric` signals on completion → reactive
   re-render. `ferric` event handlers are zero-arg; to read an `<input>` value, query the DOM
   element (e.g. `web_sys` by id) — the compose spoke owns this pattern.
4. **No panics / no unsafe in runtime code** (`api/timeline/compose/profile/error` and view
   logic in `app`). Surface `ApiError`/`ErrorCode`/network failures as `AppError` UI state.
   The thin wasm mount entry MAY `expect()` for mount-point acquisition (documented).
5. **Quality gates**: `cargo fmt --all --check`; `cargo clippy --workspace --all-targets
   -- -D warnings`; rustdoc on public items. `missing_docs`/`unsafe_code` are `warn` and
   clippy is `-D warnings`, so document public items and avoid `unsafe`.
6. **git discipline**: `SUBTASK_scaffold` creates the checkout+branch and the initial skeleton
   commit; Group-1 spokes write files only (no git); the synthesis gate performs all remaining
   git (stage/commit/build/PR). Work only on `work/chirp-frontend`; never touch `main`; never
   force-push; no attribution trailer; let Cargo author `Cargo.lock`.
