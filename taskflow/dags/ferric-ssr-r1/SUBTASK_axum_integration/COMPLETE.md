# COMPLETE — ferric-ssr-r1-axum-integration

## Status

Completed. `cargo build -p chirp-server` exits zero; all three SSR unit tests pass.

## Declared Outputs Delivered

### 1. `crates/chirp-server/src/ssr.rs` (new)

Document assembly helper and Axum route handler:

- **`assemble_document(server_html: &str, wasm_script_path: &str) -> String`**
  Pure function that wraps server-rendered markup in a full HTML document shell matching
  `design/ferric/ssr-hydration.md §2.1`:
  `<!doctype html>` + `<head>` + `<div id="app">{server_html}</div>` +
  BAR-005 state island placeholder comment +
  `<script type="module" src="{wasm_script_path}">`.

- **`ssr_handler() -> Response`**
  Stateless async Axum handler: calls `ferric::render_to_string` with a placeholder root
  component closure; wraps the result via `assemble_document`; returns `200 OK` with
  `Content-Type: text/html; charset=utf-8`.

- **3 unit tests** (`ssr::tests::*`) covering document structure, empty markup, and the
  debug-assert injection guard.

### 2. `crates/chirp-server/Cargo.toml` (modified)

Added `ferric = { path = "../ferric" }`. The `ferric::ssr` module compiles on native targets;
`dom`/`hydrate` are `#[cfg(target_arch = "wasm32")]` inside `ferric` and do not affect the
server build.

### 3. `crates/chirp-server/src/lib.rs` (modified)

`pub mod ssr;` added (additive only).

### 4. `crates/chirp-server/src/api/router.rs` (modified)

Additive `.route("/", get(ssr_handler))` registered in `build_router`; no existing route,
fallback, or middleware modified.

## Success Criteria — Verification

| Criterion | Result |
|-----------|--------|
| `cargo build -p chirp-server` exits zero | ✅ verified locally |
| New route composes with `build_router`; existing router structure unchanged | ✅ additive only |
| Usage documented (inline doc comments + example) | ✅ `ssr.rs` module-level + per-item docs |
| REQ-SSR-011 addressed | ✅ |
| Frozen ferric files unmodified | ✅ no changes in `crates/ferric/` |

## Deliverable Locations

- Branch: `work/ferric-ssr-r1-axum`
- Commit: `36b6ea9`
- PR: https://github.com/Nousix-LLC/nswe-demo/pull/227

## Out of Scope (by brief)

- BAR-005 state island serialization — placeholder comment left at the correct location in
  `assemble_document`; BAR-005 spoke anchors its implementation there.
- `render_to_string` implementation — stub in `ferric::ssr` (panics); the
  `ferric-ssr-r1-server-render` spoke provides the real implementation.
