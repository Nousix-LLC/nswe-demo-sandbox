# SUBTASK_b1_hydrate_fix: Remediate B1 — Wire ferric::hydrate() from WASM entry point

## Task Specification

**Slug**: SUBTASK_b1_hydrate_fix  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending  

### Objective

Remediate blocking finding B1 (REQ-HYD-003): change `crates/chirp-frontend/src/app.rs::start()` so the WASM bundle calls `ferric::hydrate(root, app)` when `#app` already contains server-rendered children, and falls back to `ferric::dom::mount(root, app)` for a fresh client-side render (no server markup). Also correct the `crates/chirp-server/src/ssr.rs` docstring (item 4 of the `assemble_document` doc, currently at ~line 71) to accurately describe the conditional hydration wiring.

### Context

This task is part of ferric-ssr-r4 (see `_GLOBAL.md` in the parent workspace).

**Branch**: `work/ferric-ssr-r1` in `/home/user/nswe-demo`  
**PR**: #228 (Nousix-LLC/nswe-demo)

The current `app.rs::start()` ends with `mount(root, app)` (line 150). `ferric::hydrate` is already implemented (466 lines, crates/ferric/src/hydrate.rs), re-exported from `ferric::hydrate`, and compiled only on `wasm32`. The fix must detect SSR markup and branch accordingly.

The `ssr.rs` docstring incorrectly asserts the WASM bundle will call `ferric::hydrate` unconditionally; it must be updated to reflect the conditional logic (hydrate when `#app` has children, mount otherwise), since `assemble_document` always populates `#app` with server markup.

---

## Inputs

| Input | Location |
|---|---|
| Subtree hub | `taskflow/dags/ferric-ssr-r4/_GLOBAL.md` |
| WASM entry point | `/home/user/nswe-demo/crates/chirp-frontend/src/app.rs` |
| SSR handler docstring | `/home/user/nswe-demo/crates/chirp-server/src/ssr.rs` (item 4 at ~line 71) |
| ferric hydrate signature | `/home/user/nswe-demo/crates/ferric/src/hydrate.rs` lines 40–45 |
| ferric lib.rs re-exports | `/home/user/nswe-demo/crates/ferric/src/lib.rs` |

---

## Success Criteria

- `start()` in `app.rs` calls `ferric::hydrate(root, app)` when `root.has_child_nodes()` is true, `ferric::dom::mount(root, app)` otherwise.
- `ssr.rs` docstring (item 4 of `assemble_document`) accurately describes the client-side hydration path.
- `cargo check --target wasm32-unknown-unknown -p chirp-frontend` exits 0 on the build server.
- `cargo check -p chirp-server` exits 0 on the build server.
- Changes committed to `work/ferric-ssr-r1` and pushed to origin.

---

## Declared Output

`taskflow/dags/ferric-ssr-r4/SUBTASK_b1_hydrate_fix/b1_resolution.md`

The file must record:
- Commit SHA(s) pushed to `work/ferric-ssr-r1`
- Exact lines changed in `app.rs` and `ssr.rs`
- Build verification results
- Any complications encountered
