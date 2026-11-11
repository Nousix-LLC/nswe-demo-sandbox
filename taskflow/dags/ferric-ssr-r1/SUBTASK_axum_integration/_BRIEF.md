# _BRIEF.md — ferric-ssr-r1-axum-integration

## Objective

Wire `render_to_string` from `crates/ferric` into an Axum handler in `crates/chirp-server`,
addressing the Axum server integration portion of Issue #226 (BAR-006). The integration runs
on branch `work/ferric-ssr-r1-axum`, branched from `work/ferric-ssr-r1` after the skeleton
task has committed.

This spoke can proceed concurrently with the server-render and client-hydrate spokes. The
skeleton provides the `render_to_string` stub in `crates/ferric`; this spoke wires against
that signature (the synthesis gate verifies the full end-to-end once all spokes land).

## Inputs

- **Branch**: `work/ferric-ssr-r1` after the skeleton task has committed (use as base for
  `work/ferric-ssr-r1-axum`).
- **Owned files to modify/create**:
  - `crates/chirp-server/Cargo.toml` — add `ferric` dependency if not present; ensure no
    wasm-only features are pulled into the server binary.
  - `crates/chirp-server/src/main.rs` — additive route registration only (the existing
    structure and `build_router` are not restructured).
  - New files in `crates/chirp-server/src/` for the SSR handler and document assembly helper.
- **Source references** (read-only):
  - `crates/chirp-server/src/main.rs` — existing server entry point and `build_router`.
  - `crates/ferric/src/ssr.rs` (stub at this point) — `render_to_string` signature to call.
  - `contracts/ferric_ssr_contract.rs` — authoritative `render_to_string` signature.
  - `design/ferric/ssr-hydration.md` — §Axum integration shape (document assembly helper
    structure: HTML shell + mount container + server markup + WASM bootstrap script).

## Declared Output

Commits on branch `work/ferric-ssr-r1-axum` with:

1. New file(s) in `crates/chirp-server/src/` implementing:
   - A document assembly helper that takes the server-rendered HTML string from
     `render_to_string` and wraps it in a full HTML document (shell + mount container +
     server markup + WASM bootstrap `<script>`). The shape is specified in
     `design/ferric/ssr-hydration.md`.
   - An Axum route handler that calls `render_to_string` with a Ferric component and returns
     the assembled HTML document as an HTTP response.

2. `crates/chirp-server/Cargo.toml` updated with the `ferric` dependency (native build;
   no wasm-only features that would break server compilation).

3. `crates/chirp-server/src/main.rs` updated with the minimum wiring needed to register the
   new route handler with the existing `build_router` — no restructuring of existing routes.

4. Usage documentation: either (a) inline doc comments on the assembly helper and handler
   showing a minimal usage example, or (b) a runnable example file under
   `crates/chirp-server/examples/`.

## Success Criteria

- `cargo build -p chirp-server` exits zero — the integration compiles successfully.
- The new route handler composes with `build_router`; the existing router structure is
  unchanged.
- Usage is documented so a developer joining the project can understand how to call
  `render_to_string` from an Axum handler without reading the implementation.
- Requirement REQ-SSR-011 is addressed.
- The frozen ferric files (`src/dom.rs`, `src/signal.rs`, `src/vdom.rs`, `src/component.rs`)
  are unmodified.

## Constraints

- **Owns**: new files in `crates/chirp-server/src/`, `crates/chirp-server/Cargo.toml`,
  and additive changes to `crates/chirp-server/src/main.rs`. Do not modify any file in
  `crates/ferric/`.
- **Do not restructure** the existing `build_router` or change the existing server entry point
  beyond the minimum route-registration addition.
- **BAR-005 (#225)** is out of scope; do not implement state island serialization (the
  `<script type="application/json">` state island described in the design spec is a BAR-005
  concern). The document assembly helper may include a placeholder comment where the state
  island would go.
- Branch: `work/ferric-ssr-r1-axum`. Do not force-push to `main`.
- Commit attribution: end commit messages with `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`.
- Security: do not put server hostnames, IP addresses, SSH key paths, or cluster details in
  any committed file or PR content.
