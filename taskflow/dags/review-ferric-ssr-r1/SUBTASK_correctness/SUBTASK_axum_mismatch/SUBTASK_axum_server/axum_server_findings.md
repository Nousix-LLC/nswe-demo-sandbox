# Axum Server-Side Findings (REQ-MIS-001, REQ-MIS-002, REQ-SSR-007)

---

## REQ-MIS-001 — Axum handler pattern

**Status**: CLEAN (with one non-blocker finding)

**What was checked**:
- The new `ssr_handler` function in `crates/chirp-server/src/ssr.rs`
- The `build_router` wiring in `crates/chirp-server/src/api/router.rs`
- The `ferric = { path = "../ferric" }` dependency in `crates/chirp-server/Cargo.toml`
- The full `ferric::render_to_string` implementation in `crates/ferric/src/ssr.rs`

**Evidence**:
- Handler declaration: `crates/chirp-server/src/ssr.rs:159`
- `render_to_string` call: `crates/chirp-server/src/ssr.rs:169–176`
- Response construction: `crates/chirp-server/src/ssr.rs:180–185`
- Router import: `crates/chirp-server/src/api/router.rs:45`
- Router registration: `crates/chirp-server/src/api/router.rs:69`

**What was found sound**:

The handler is `pub async fn ssr_handler() -> Response` — a valid zero-extractor Axum handler
(no extractors are needed because the stub has no request-bound dependencies). The return type
`Response` (re-exported from `axum::response::Response`) satisfies Axum's `IntoResponse` bound,
and `.into_response()` is called on the tuple to produce it.

The `render_to_string` call at lines 169–176 passes a `FnOnce() -> VNode` closure, which matches
the function's signature in `crates/ferric/src/ssr.rs`. The result is passed to `assemble_document`
(line 178), and the return value is a tuple
`(StatusCode::OK, [(header::CONTENT_TYPE, "text/html; charset=utf-8")], doc)` converted with
`.into_response()`. This is the textbook Axum alternative to `Html(...)`: the `Html<T>` wrapper in
Axum sets `Content-Type: text/html; charset=utf-8` automatically, while this form sets it explicitly.
The two are functionally identical on the wire; "or equivalent" in REQ-MIS-001's criterion is met.

Router wiring (`crates/chirp-server/src/api/router.rs:69`) registers `GET /` as the first route in
`build_router`, before the SPA fallback. Axum's matching rules ensure the explicit route takes
precedence over `fallback_service`, so the SSR handler replaces the placeholder `index.html` at the
root path without touching any other route.

**Finding** (NON-BLOCKER):

A code comment at `crates/chirp-server/src/ssr.rs:165–168` reads:

> "The stub implementation in `ferric::ssr` currently panics (via `todo!()`); the
> `ferric-ssr-r1-server-render` spoke provides the real implementation."

The actual `ferric::render_to_string` on the `work/ferric-ssr-r1` branch is fully implemented and
tested — it does not `todo!()`. The comment is stale: it describes an earlier draft of the branch
where the ferric side was not yet merged. It does not affect correctness or CI, but a reviewer or
collaborator reading this comment will expect a panic that will not occur. The comment should be
removed or updated to reflect the current state.

---

## REQ-MIS-002 — HTML well-formedness and markers

**Status**: CLEAN

**What was checked**:
- The HTML document template in `assemble_document` (`crates/chirp-server/src/ssr.rs:104–119`)
- The `render_node` function in `crates/ferric/src/ssr.rs` (the SSR rendering path)
- The `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` constants and their use in `render_node`
- The hydration client's `adopt_children` and `is_sentinel_comment` functions in
  `crates/ferric/src/hydrate.rs`, to confirm the client can consume the server's markers
- The test at `crates/chirp-server/src/ssr.rs:193–212`

**Evidence**:
- Document shell: `crates/chirp-server/src/ssr.rs:104–119`
- Marker constants: `crates/ferric/src/ssr.rs:33` (`TEXT_OPEN_MARKER`), `crates/ferric/src/ssr.rs:50` (`TEXT_CLOSE_MARKER`)
- `render_node` text wrapping: `crates/ferric/src/ssr.rs:88–92`
- Client sentinel check: `crates/ferric/src/hydrate.rs:242–261`
- Client import of same constants: `crates/ferric/src/hydrate.rs:35`

**What was found sound**:

*Document well-formedness.*
`assemble_document` produces a complete, balanced HTML5 document:
```
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>chirp</title>
</head>
<body>
  <div id="app">{server_html}</div>
  <!-- BAR-005 state island: … -->
  <script type="module" src="{wasm_script_path}"></script>
</body>
</html>
```
All tags are balanced; attribute syntax is valid HTML5; void elements (`<meta>`) require no closing
slash in HTML5 and do not have one here. The body comment does not contain `-->` internally, so it
does not prematurely close the comment.

*Text-node marker output.*
`ferric::render_to_string` is called with a component closure returning:
```
VElement("div", id="ferric-root")
  └── VNode::Text("Loading…")
```
`render_node` traverses this tree and produces:
```
<div id="ferric-root"><!--$t-->Loading&#8230;<!--/$t--></div>
```
(The `…` Unicode ellipsis is passed through `escape_html`, which does not escape it since it is
not one of the five injection-risky characters `<>&"'`. The character is therefore emitted
verbatim as UTF-8 — `Loading…` — not as `Loading&#8230;`. The document carries
`<meta charset="utf-8">` and the response sets `Content-Type: text/html; charset=utf-8`, so the
browser decodes it correctly.)

The full assembled document body injection point is `<div id="app">…</div>`, so the client
hydration entry point is correctly established.

*Hydration marker placement and correctness.*
Both `<!--$t-->` and `<!--/$t-->` are HTML Comment nodes. The client's `adopt_children` function
(lines ~171–194 of `crates/ferric/src/hydrate.rs`) iterates DOM child nodes, calls
`is_sentinel_comment` on each, and skips any that match — advancing the VNode child index only on
non-sentinel nodes. After the adopt pass, `strip_sentinels` removes all sentinel Comment nodes
recursively so DOM child indices align with VNode path indices for the diff/patch pass. This means
the markers serve exactly the purpose their doc comment describes: they delimit text-node boundaries
in the serialized HTML so the client can walk the VNode tree and the DOM in lock-step, then
disappear cleanly before reactive updates begin. Placement is correct.

*Test coverage.*
`crates/ferric/src/ssr.rs` contains dedicated marker tests: `text_node_wrapped_in_markers` asserts
the wrap for a non-empty text node; `empty_text_node_wrapped_in_markers` checks the degenerate
empty case; `renders_nested_children_at_correct_depth` verifies marker placement in a multi-level
tree. These assert the exact marker literals (using the same constants), not just presence.

---

## Marker Format Observed (Server Side)

**Server-side marker format**:

| Constant | Value | HTML structure |
|----------|-------|----------------|
| `TEXT_OPEN_MARKER` | `"<!--$t-->"` | HTML Comment node, `comment.data()` == `"$t"` |
| `TEXT_CLOSE_MARKER` | `"<!--/$t-->"` | HTML Comment node, `comment.data()` == `"/$t"` |

Every `VNode::Text(s)` node is serialized as:
```
<!--$t-->{html_escaped_text_content}<!--/$t-->
```

There are no element-level markers (no `data-hk`, no `data-ferric-id` or similar). Element adoption
in the hydration client matches by tag name and structural position, not by id attribute. Only text
nodes receive sentinels, to disambiguate text nodes from sibling Comment and Element nodes during
the adopt walk.

The constants are defined once in `crates/ferric/src/ssr.rs:33` and `:50`, then imported by
`crates/ferric/src/hydrate.rs:35` (`use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER}`).
Server and client share the identical literals through this import — there are no inline copies.

**Evidence**: `crates/ferric/src/ssr.rs:33,50,88–92`; `crates/ferric/src/hydrate.rs:35,242–261`

---

## Non-goal Boundary

### REQ-SSR-007 / #225 — Async resource state (non-goal)

**Status**: CONFIRMED NON-GOAL

**What was checked**:
- The module-level doc comment of `crates/chirp-server/src/ssr.rs`
- The `assemble_document` body template (`crates/chirp-server/src/ssr.rs:104–119`)
- The `ssr_handler` function signature and body (`crates/chirp-server/src/ssr.rs:159–186`)
- The `ssr_handler` inline comments (`crates/chirp-server/src/ssr.rs:160–163`)

**Evidence**: `crates/chirp-server/src/ssr.rs:138–143`, `:114`, `:160–163`

Async resource state carry across the SSR seam (REQ-SSR-007 / BAR-005 / issue #225) is absent
from this PR in every dimension:

- The `ssr_handler` signature is `pub async fn ssr_handler() -> Response` with no `State(state):
  State<AppState>` extractor and no `AppState` import.
- The `assemble_document` template contains the placeholder comment
  `<!-- BAR-005 state island: <script type="application/json" id="__state">…</script> -->` but
  no live `<script type="application/json">` tag and no serialized state payload.
- The module doc comment (lines 45–46) explicitly defers: "The `<script
  type="application/json" id="__state">` state island is deferred to BAR-005 (#225); a
  placeholder comment marks its intended location."
- The handler doc comment (lines 138–143) names BAR-005 as the tracking item and explains that
  the placeholder comment is a structural anchor for the future implementation.

The absence is deliberate and fully annotated. It is not a deficiency.
