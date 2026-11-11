# _BRIEF.md — ferric-ssr-r1-server-render

## Objective

Implement `render_to_string` fully in `crates/ferric/src/ssr.rs`, addressing Issue #223
(BAR-003): server-side HTML rendering and per-request reactive scope isolation. The
implementation runs on branch `work/ferric-ssr-r1-server`, branched from `work/ferric-ssr-r1`
after the skeleton task has committed.

## Inputs

- **Branch**: `work/ferric-ssr-r1` after the skeleton task has committed (use this as the
  base for `work/ferric-ssr-r1-server`).
- **Owned file to implement**: `crates/ferric/src/ssr.rs` (the skeleton left a stub here).
- **Contract** (read-only): `contracts/ferric_ssr_contract.rs` — the `render_to_string`
  signature, the `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` constants, and the full constraint
  list (HTML escaping rules, reactive isolation requirement, void-element list).
- **Source references** (read-only):
  - `crates/ferric/src/vdom.rs` — `VNode` and `VElement` definitions.
  - `crates/ferric/src/signal.rs` — `ReactiveScope` for per-request isolation.
  - `design/ferric/ssr-hydration.md` — authoritative architecture spec (REQ-SSR-*).

## Declared Output

Commits on branch `work/ferric-ssr-r1-server` with:

1. `crates/ferric/src/ssr.rs` fully implemented — `render_to_string` replaces the `todo!()`
   stub with working logic.

2. Native Rust unit tests (in `src/ssr.rs` or `tests/ssr.rs`) covering at minimum:
   - Basic element rendering: a simple VNode tree produces the expected HTML string.
   - Text escaping: each of the five injection-risky characters (`<`, `>`, `&`, `"`, `'`)
     in text content is correctly escaped.
   - Text-boundary markers: a VNode::Text node is wrapped in `TEXT_OPEN_MARKER` and
     `TEXT_CLOSE_MARKER` exactly as declared in the contract.
   - Nested elements: children render at correct depth.
   - Per-request isolation: two concurrent `render_to_string` calls with different signal
     state return independent, correct HTML strings without leaking state across calls.

## Success Criteria

- `cargo test -p ferric` (native target) exits zero — all tests including new ones pass.
- `cargo check --lib -p ferric` (native target) exits zero — no `web_sys` import in scope.
- `src/ssr.rs` uses `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER` as declared in
  `contracts/ferric_ssr_contract.rs`; no other marker format is used.
- The five injection-risky characters are correctly escaped in both text content and
  attribute values.
- Each `render_to_string` call completes in its own reactive scope; signal subscriptions do
  not leak between concurrent calls (demonstrated by the concurrent-render test).
- Requirements REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-010, REQ-SSR-012 are addressed.
- The frozen files (`src/dom.rs`, `src/signal.rs`, `src/vdom.rs`, `src/component.rs`) are
  unmodified.

## Constraints

- **Owns**: `crates/ferric/src/ssr.rs` (and sub-files if implementation is split into
  `src/ssr/` subdirectory). Do not modify any other file.
- **No browser APIs**: `src/ssr.rs` must not import `web_sys`, `wasm_bindgen`, or any
  browser-only crate. The file must compile cleanly on a native host target.
- **Marker constants**: import `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER` from `crate::ssr`
  or define them in `src/ssr.rs` matching the contract exactly — never use inline string
  literals for the marker bytes.
- **Frozen files** must not be touched.
- **BAR-005 (#225)** is out of scope; do not introduce state-island or async serialization.
- Branch: `work/ferric-ssr-r1-server`. Do not force-push to `main`.
- Commit attribution: end commit messages with `Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>`.
