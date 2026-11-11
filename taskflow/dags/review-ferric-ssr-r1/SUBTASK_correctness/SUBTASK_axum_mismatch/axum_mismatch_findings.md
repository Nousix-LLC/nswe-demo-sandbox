# Mismatch Detection + Axum Integration Findings (REQ-SSR-006, REQ-MIS-001–002)

## Summary

REQ-SSR-006 (mismatch detection) blocks: the implementation is substantively correct across all structural-divergence cases, but the acceptance criterion requires a `wasm-bindgen-test` covering the mismatch code path and none exists in the PR. A secondary non-blocker — extra DOM nodes beyond the VNode list are warned but not removed — should be addressed in a follow-up. REQ-MIS-001 (Axum handler pattern) and REQ-MIS-002 (HTML well-formedness and markers) are clean; a stale code comment in the server implementation is a non-blocker. REQ-SSR-007 is confirmed as a non-goal with explicit documentation in the PR. The marker format cross-check passes: both sides use the same text-boundary HTML comment sentinels sharing the constants by direct import — agreement by construction, not coincidence.

**Label note**: The PR (issue #226, `crates/ferric/src/hydrate.rs:11`) identifies the mismatch-detection criterion as REQ-SSR-009; the subtree brief uses REQ-SSR-006 for the same criterion. The mismatch-detect spoke (`mismatch_detect_findings.md`) adopted the code/issue label and explicitly flagged the divergence. This findings document uses REQ-SSR-006 to match the subtree specification but notes the discrepancy at the relevant criterion. The label inconsistency in the review infrastructure should be resolved.

---

## Findings by Criterion

### REQ-SSR-006 — Mismatch detection

**Status**: FINDING (BLOCKER)

**What was checked**: All structural-divergence detection paths in `adopt_vnode` and `adopt_children` (wrong element tag, non-element where element expected, text content mismatch, non-text where text expected, empty root DOM, missing VNode children, extra DOM nodes beyond VNode list); the `emit_mismatch_warning` function and all call sites for the warn-not-panic requirement; all recovery operations (fresh subtree mount for mismatched element types, in-place text correction, full append for empty root, per-child append for missing children); and the full branch file tree for `wasm-bindgen-test` coverage of the mismatch path.

> *Label discrepancy (non-blocker)*: Issue #226 and `crates/ferric/src/hydrate.rs:11` use REQ-SSR-009 for this criterion; the subtree brief uses REQ-SSR-006. Same criterion, two labels. The spoke adopted REQ-SSR-009 (the code/issue label); this document uses the brief's REQ-SSR-006 to maintain contract consistency. This discrepancy should be resolved.

**Evidence**:
- Detection (all conditions): `crates/ferric/src/hydrate.rs:72–181`
- Warn path (debug-only, no panic): `crates/ferric/src/hydrate.rs:188–203`; call sites at lines 78, 103, 119, 130, 158, 175
- Recovery — element replace: `crates/ferric/src/hydrate.rs:106–110`
- Recovery — text correct: `crates/ferric/src/hydrate.rs:118–121`
- Recovery — type replace: `crates/ferric/src/hydrate.rs:128–133`
- Recovery — empty root: `crates/ferric/src/hydrate.rs:78–80`
- Recovery — missing children: `crates/ferric/src/hydrate.rs:175–180`
- Extra-nodes non-removal: `crates/ferric/src/hydrate.rs:154–163`
- Absence of test coverage: `crates/ferric/src/hydrate.rs` (466 lines, no `#[cfg(test)]` block); no `crates/ferric/tests/` directory on the branch

**Finding (BLOCKER)**: No `wasm-bindgen-test` covering the mismatch detection, warning, or recovery code paths exists anywhere in the PR. Issue #226's REQ-SSR-006/REQ-SSR-009 acceptance criterion explicitly requires a headless `wasm-bindgen-test` that: hydrates against a deliberately mismatched server DOM; confirms the diagnostic fires; confirms the live DOM matches the client render of the mismatched subtree; and confirms sibling elements remain adopted. `crates/ferric/src/hydrate.rs` (466 lines) has no `#[cfg(test)]` block; no `crates/ferric/tests/` directory exists in the branch. The existing tests in `crates/ferric/src/ssr.rs` cover SSR render output — none cover the hydration or mismatch path. CI passing on those tests does not satisfy this acceptance criterion.

What a satisfying test would look like: build a minimal server HTML string with a deliberate structural divergence (e.g., the component returns `<p>` but the server DOM contains `<div>`); inject it into the headless browser DOM under `#app`; call `ferric::hydrate(root, || ...)`; assert that `console.warn` fired with a message containing the VNode path and expected/found labels; assert that the live DOM under `#app` matches the client-rendered component output; assert that siblings of the mismatched element are still adopted with event handlers wired. This test does not exist and must be written and pass before this criterion is met.

**Finding (NON-BLOCKER)**: Extra DOM nodes beyond the VNode child list are warned about but not removed. At `crates/ferric/src/hydrate.rs:154–163`, when DOM nodes remain after the VNode list is exhausted, `adopt_children` calls `emit_mismatch_warning` and then `break`s (comment: "only warn, do not remove"). After `strip_sentinels` runs, the live DOM contains more children than the VNode tree expects. While existing patch targets are not corrupted (extra nodes lie past the end of the VNode index range and do not shift earlier indices), the live DOM no longer matches the client render of the subtree, violating the acceptance criterion's "live DOM matches client render" guarantee. A later diff/patch operation that inserts or removes at the same parent may interact unexpectedly with the unremoved nodes. The extra-nodes case is comparatively rare (server renders more children than the component produces, which suggests a component-level bug rather than a normal divergence scenario); address in a follow-up.

---

### REQ-MIS-001 — Axum handler pattern

**Status**: CLEAN

**What was checked**: The `ssr_handler` function signature, return type, and body; the `render_to_string` call and its match to the ferric function signature; the response construction and Content-Type header; the router wiring that registers `GET /` before the SPA fallback; and the `ferric = { path = "../ferric" }` dependency in `crates/chirp-server/Cargo.toml`.

**Evidence**:
- Handler declaration: `crates/chirp-server/src/ssr.rs:159`
- `render_to_string` call: `crates/chirp-server/src/ssr.rs:169–176`
- Response construction: `crates/chirp-server/src/ssr.rs:180–185`
- Router import: `crates/chirp-server/src/api/router.rs:45`
- Router registration: `crates/chirp-server/src/api/router.rs:69`

**What was found sound**: `ssr_handler` is `pub async fn ssr_handler() -> Response` — a valid zero-extractor Axum handler (no extractors needed for this stub). The return type `Response` satisfies Axum's `IntoResponse` bound, and `.into_response()` is called on the tuple. The response is `(StatusCode::OK, [(header::CONTENT_TYPE, "text/html; charset=utf-8")], doc).into_response()`, which is functionally equivalent to `Html(doc)` and satisfies the "or equivalent" language in the criterion. `GET /` is registered before the SPA fallback at `crates/chirp-server/src/api/router.rs:69`, so the SSR handler takes precedence over `fallback_service`.

**Finding (NON-BLOCKER)**: A code comment at `crates/chirp-server/src/ssr.rs:165–168` describes `ferric::render_to_string` as a stub that panics via `todo!()`. On `work/ferric-ssr-r1`, the function is fully implemented and tested. The stale comment will mislead reviewers into expecting a panic that will not occur. Remove or update it before merging.

---

### REQ-MIS-002 — HTML well-formedness and markers

**Status**: CLEAN

**What was checked**: The HTML document shell in `assemble_document`; the text-node marker output from `render_node` for a representative component; marker placement correctness relative to the client's `adopt_children` and `is_sentinel_comment` logic; and the dedicated marker tests in `crates/ferric/src/ssr.rs`.

**Evidence**:
- Document shell: `crates/chirp-server/src/ssr.rs:104–119`
- Marker constants: `crates/ferric/src/ssr.rs:33` (`TEXT_OPEN_MARKER`), `crates/ferric/src/ssr.rs:50` (`TEXT_CLOSE_MARKER`)
- `render_node` text wrapping: `crates/ferric/src/ssr.rs:88–92`
- Client sentinel check: `crates/ferric/src/hydrate.rs:242–261`
- Client import of same constants: `crates/ferric/src/hydrate.rs:35`
- Marker tests: `crates/ferric/src/ssr.rs:193–212`

**What was found sound**: The HTML5 document produced by `assemble_document` has balanced tags and valid attribute syntax. Void elements (`<meta>`) correctly omit closing slashes. The body BAR-005 placeholder comment does not contain `-->` internally and does not prematurely close the comment node. Text nodes are wrapped as `<!--$t-->text<!--/$t-->` by `render_node`, producing well-formed HTML Comment nodes the client's `is_sentinel_comment` check recognizes by the same constants (single definition at `crates/ferric/src/ssr.rs:33,50`, imported by both server and client via `hydrate.rs:35`). Three dedicated tests assert the exact marker literals for non-empty text, empty text, and nested children. The hydration entry point `<div id="app">` is correctly placed in the document body.

---

## Non-goal Boundary

### REQ-SSR-007 / #225 — Async resource state (non-goal)

**Status**: CONFIRMED NON-GOAL

**What was checked**: The `ssr_handler` function signature for a `State` extractor and `AppState` import; the `assemble_document` template for a live `<script type="application/json">` state island; the module-level doc comment for explicit non-goal annotation; and the handler doc comment naming BAR-005 as the deferred tracking item.

**Evidence**: `crates/chirp-server/src/ssr.rs:138–143`, `crates/chirp-server/src/ssr.rs:114`, `crates/chirp-server/src/ssr.rs:160–163`

Async resource state carry across the SSR seam is absent in every dimension. The `ssr_handler` signature has no `State` extractor and no `AppState` import. The `assemble_document` template contains only a placeholder HTML comment for the BAR-005 state island — no live `<script type="application/json" id="__state">` tag and no serialized state payload. The module doc comment at lines 45–46 and the handler doc comment at lines 138–143 both explicitly defer to BAR-005 (#225) and describe the placeholder comment as a structural anchor for the future implementation. The absence is deliberate and fully annotated; it is not a deficiency.

---

## Cross-check: Marker Format Agreement

**Client-side format** (from SUBTASK_mismatch_detect): Text-boundary HTML Comment sentinels. `TEXT_OPEN_MARKER = "<!--$t-->"` (DOM `comment.data()` = `"$t"`); `TEXT_CLOSE_MARKER = "<!--/$t-->"` (DOM `comment.data()` = `"/$t"`). No element-level attributes or `data-hydration-id` markers. Constants defined in `crates/ferric/src/ssr.rs:28–43`, imported by `crates/ferric/src/hydrate.rs:35`.

**Server-side format** (from SUBTASK_axum_server): Text-boundary HTML Comment sentinels. `TEXT_OPEN_MARKER = "<!--$t-->"` (HTML Comment node, `comment.data()` = `"$t"`); `TEXT_CLOSE_MARKER = "<!--/$t-->"` (HTML Comment node, `comment.data()` = `"/$t"`). No element-level markers. Constants defined once in `crates/ferric/src/ssr.rs:33, 50`, imported by `crates/ferric/src/hydrate.rs:35`.

**Agreement**: MATCHES. Both sides share the identical literals via the same import path (`use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER}` at `hydrate.rs:35`). There are no inline copies and no separate server-side vs client-side schemas. Agreement is by construction: the client cannot diverge from the server's format without changing the same constants that both sides read.
