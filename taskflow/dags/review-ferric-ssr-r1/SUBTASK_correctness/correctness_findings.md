# PR #228 Correctness Findings

## Summary

PR #228 (`work/ferric-ssr-r1`) lands a `render_to_string` implementation, a `hydrate()` function,
mismatch recovery logic, and an Axum handler that invokes SSR. Of the eleven in-scope acceptance
criteria, nine are met. Two block landing: `hydrate()` is never called from the WASM entry point
(REQ-HYD-003 — `start()` calls `mount()` instead, so every SSR page load falls back to a
client-side re-render), and the mismatch-detection acceptance criterion requires a
`wasm-bindgen-test` that does not exist in the PR (REQ-SSR-006). Four non-blockers are noted across
REQ-SSR-002, REQ-SSR-005, REQ-HYD-002, REQ-MIS-001, and a secondary finding under REQ-SSR-006
(extra DOM nodes warned but not removed). The marker format is consistent across SSR and hydration:
both sides share the same HTML comment sentinel constants defined once in `ssr.rs` and imported by
`hydrate.rs`, with no local copies. REQ-SSR-007 (async state carry, #225) is correctly absent and
explicitly annotated as deferred to BAR-005.

---

## Findings by Criterion

### REQ-SSR-001 — render_to_string renders without DOM

**Status**: CLEAN

**What was checked**: Imports and module-level cfg guards on the `ssr` and `hydrate` modules in
`crates/ferric/src/lib.rs`; the contents of `crates/ferric/src/ssr.rs` for any `web_sys` or
`wasm_bindgen` import; the dependency entry for `ferric` in `crates/chirp-server/Cargo.toml`;
the test macro style used in `ssr.rs`.

**Evidence**:
- `crates/ferric/src/ssr.rs:827` (module doc): "it must never reference `web_sys` or
  `wasm_bindgen`" — borne out by the imports: the only import is `use crate::vdom::VNode;`. No
  `web_sys`, `wasm_bindgen`, or DOM call in the file.
- `crates/ferric/src/lib.rs`: `pub mod ssr;` and `pub use crate::ssr::render_to_string;` are
  both ungated — the SSR module compiles on all targets.
- `crates/ferric/src/hydrate.rs:325`: `#![cfg(target_arch = "wasm32")]` — the DOM-dependent
  hydration module is correctly wasm32-only. The cfg split is exact.
- `crates/chirp-server/Cargo.toml`: `ferric = { path = "../ferric" }` with no Cargo features
  gate; comment names it a "NATIVE (non-wasm) dependency."
- `ssr.rs` test suite: all tests use `#[test]` (native), not `#[wasm_bindgen_test]`.

---

### REQ-SSR-002 — Signal-driven components render from initial state; no reactivity during SSR

**Status**: CLEAN (with NON-BLOCKER)

**What was checked**: The `render_to_string` body in `crates/ferric/src/ssr.rs`;
`ReactiveScope::run` and `impl Drop for ReactiveScope` in `crates/ferric/src/signal.rs`;
isolation tests in `ssr.rs`.

**Evidence**:
- `crates/ferric/src/ssr.rs:942–955`: `render_to_string` creates a fresh `ReactiveScope`,
  calls `scope.run(f)` once, then drops the scope. The drop order runs `impl Drop for
  ReactiveScope`.
- `crates/ferric/src/signal.rs:486–493`: `ReactiveScope::run` does not push onto
  `observer_stack`, so `signal.get()` calls during SSR do not register subscriptions.
- `crates/ferric/src/signal.rs:502–506`: `impl Drop for ReactiveScope` calls `rt.dispose`,
  which at lines 312–338 purges all subscriptions, sources, and pending effects.
- `crates/ferric/src/signal.rs:985–1022`: `no_stale_subscriber_leak` demonstrates the full
  dispose path.
- `crates/ferric/src/ssr.rs:1087–1120`, `1123–1153`: two tests confirm HTML isolation across
  consecutive renders with distinct signals.

**NON-BLOCKER** (`crates/ferric/src/ssr.rs`): Issue #223's acceptance criterion states a signal
created in one render has zero subscribers after `render_to_string` completes. The existing SSR
tests verify HTML independence between renders but do not directly assert `subscriber_count == 0`
on a signal created inside a render after that render returns. The isolation mechanism is
mechanically correct (proven in `signal.rs:985–1022`); the specific invariant from the criterion
is not directly asserted in the SSR test suite. A test asserting `subscriber_count(sig) == 0`
immediately after a `render_to_string` call that creates `sig` internally would close this gap.

---

### REQ-SSR-003 — Child components and slot-based composition render correctly; nested trees exercised

**Status**: CLEAN

**What was checked**: The `render_node` recursion in `crates/ferric/src/ssr.rs`; the `VNode`
data model in `crates/ferric/src/vdom.rs`; nesting tests.

**Evidence**:
- `crates/ferric/src/ssr.rs:896–928`: `render_node` for `VNode::Element` iterates
  `el.children` and recurses — no depth limit.
- `crates/ferric/src/vdom.rs:35–56`: `children: Vec<VNode>` supports unbounded nesting, with
  child appending via `VElement::child()` and `VElement::children()` builders.
- `crates/ferric/src/ssr.rs:1036–1050`: `renders_nested_children_at_correct_depth` — renders
  `ul > li(text "one") + li(text "two")` with byte-exact assertion.
- `crates/ferric/src/ssr.rs:1053–1065`: `renders_deeply_nested_structure` — `section > div > p
  > text("deep")` (three levels), byte-exact assertion.

In this framework, components are closures returning `VNode`; slots are `VElement::child()` calls.
No separate `Component` or `Slot` variant exists in `VNode`; composition is function composition
producing nested `VElement` trees. `render_node`'s recursion over `el.children` handles this
without any component-specific dispatch path.

---

### REQ-SSR-004 — Rendered HTML includes well-formed, stable hydration markers

**Status**: CLEAN

**What was checked**: The two marker constants in `crates/ferric/src/ssr.rs`; `render_node`
text-node emission; import of these constants in `crates/ferric/src/hydrate.rs`;
marker-specific tests.

**Evidence**:
- `crates/ferric/src/ssr.rs`: `pub const TEXT_OPEN_MARKER: &str = "<!--$t-->"` and
  `pub const TEXT_CLOSE_MARKER: &str = "<!--/$t-->"` — static string constants with no counter,
  timestamp, or per-render state.
- `crates/ferric/src/ssr.rs`: `render_node` emits `TEXT_OPEN_MARKER + escape_html(s) +
  TEXT_CLOSE_MARKER` for every `VNode::Text` node.
- `crates/ferric/src/hydrate.rs`: `use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER}` — a
  single import; no local copy of either constant.
- `crates/ferric/src/ssr.rs:1020–1030`: `text_node_wrapped_in_markers` asserts exact output
  `<!--$t-->world<!--/$t-->`; `empty_text_node_wrapped_in_markers` covers the empty-text edge
  case.

Markers are HTML comment sentinels, not element attributes. Every text node is wrapped; element
nodes receive no marker. Single source of truth enforced at the type level. See the **Marker
Format Consistency** section below.

---

### REQ-SSR-005 — `render_to_string` callable from an Axum handler

**Status**: CLEAN (with NON-BLOCKER)

**What was checked**: Export declaration in `crates/ferric/src/lib.rs`; `ferric` dependency in
`crates/chirp-server/Cargo.toml`; call site in `crates/chirp-server/src/ssr.rs`; routing in
`crates/chirp-server/src/api/router.rs`.

**Evidence**:
- `crates/ferric/src/lib.rs`: `pub use crate::ssr::render_to_string;` — public crate-root
  re-export, no `#[cfg(target_arch = "wasm32")]` gate.
- `crates/chirp-server/Cargo.toml`: `ferric = { path = "../ferric" }` — native workspace
  dependency; no features gate.
- `crates/chirp-server/src/ssr.rs:239`: `let server_html = ferric::render_to_string(|| { ... });`
  called directly inside `pub async fn ssr_handler() -> Response`.
- `crates/chirp-server/src/api/router.rs`: `GET /` registered before the SPA fallback via
  `.route("/", get(ssr_handler))`.

`render_to_string` is in scope, exported, and called. The SSR handler compiles and links without
a wasm toolchain.

**NON-BLOCKER** (`crates/chirp-server/src/ssr.rs:236–237`): The comment reads "The stub
implementation in `ferric::ssr` currently panics (via `todo!()`); the
`ferric-ssr-r1-server-render` spoke provides the real implementation." This is stale
development-phase text. `ferric::render_to_string` in this PR is a complete implementation with
no `todo!()`. The code is correct; the comment misleads and should be removed.

---

### REQ-HYD-001 — hydrate() attaches without re-creating nodes

**Status**: CLEAN

**What was checked**: The adopt pass entry points (`adopt_root_vnode` → `adopt_vnode` →
`adopt_children`) in `crates/ferric/src/hydrate.rs`; every call site of `appendChild`,
`replace_child`, `create_element`, and `create_text_node` in that file.

**Evidence**:
- `crates/ferric/src/hydrate.rs:98–105`: `adopt_vnode` casts the existing DOM node with
  `dyn_ref::<Element>()` — no `create_element` on a matching tag.
- `crates/ferric/src/hydrate.rs:113–115`: text-node happy path branch comment "Perfect text
  match — nothing to do"; no operations performed.
- `crates/ferric/src/hydrate.rs:102–103`, `280–325`: `set_events` calls
  `add_event_listener_with_callback` on the existing server-rendered element.
- `crates/ferric/src/hydrate.rs:88`, `187`, `120–122`, `131–133`: `append_child` and
  `replace_child` appear only in mismatch-recovery branches (empty root, missing child, tag
  mismatch, type mismatch).
- `crates/ferric/src/hydrate.rs:5–11`: module doc "No structural DOM mutation occurs when every
  node matches (REQ-SSR-004)."

The adopt pass satisfies REQ-HYD-001.

---

### REQ-HYD-002 — Signal updates propagate post-hydration

**Status**: CLEAN (with NON-BLOCKER)

**What was checked**: The `hydrate()` reactive-update code path in
`crates/ferric/src/hydrate.rs`; whether the same `diff`/`apply_patches_impl` machinery used by
`dom::mount` is reused; presence of tests in `crates/ferric/src/hydrate.rs` and
`crates/ferric/tests/`.

**Evidence** (reactive path — CLEAN):
- `crates/ferric/src/hydrate.rs:1–57`: `hydrate()` calls `create_effect`; first closure run
  calls `adopt_root_vnode` (the `None` arm), establishing signal subscriptions. Subsequent runs
  take the `Some(prev)` branch, calling `diff` and `apply_patches_impl` — structurally identical
  to `dom::mount`. No separate subscription mechanism is introduced.

**NON-BLOCKER** (`crates/ferric/src/hydrate.rs`): No `wasm_bindgen_test` exercises the
hydrate→signal→DOM sequence. The test modules in `hydrate.rs` contain no `#[test]` or
`#[wasm_bindgen_test]` functions; `crates/ferric/tests/` does not exist on branch
`work/ferric-ssr-r1`. Issue #224's acceptance criterion 2 — "After hydrate, an event dispatch
updates the DOM in place through the signal/patch path; the element is not recreated" — has no
test verifying it. The reactive path is correctly implemented; the gap is test observability, not
a demonstrable code defect. Per the subtree's inherited constraints, this does not hold landing.

---

### REQ-HYD-003 — hydrate() called once from WASM entry point

**Status**: FINDING (BLOCKER)

**What was checked**: The WASM entry point (`crates/chirp-frontend/examples/chirp.rs fn main()`)
and the app start function (`crates/chirp-frontend/src/app.rs pub fn start()`); the diff for PR
#228 — specifically which files it modifies; `ferric::hydrate()` in
`crates/ferric/src/hydrate.rs`.

**Evidence**:
- `crates/chirp-frontend/examples/chirp.rs:16`: `fn main()` calls
  `chirp_frontend::start()`.
- `crates/chirp-frontend/src/app.rs:114–135`: `start()` calls `mount(root, app)`, not
  `ferric::hydrate(root, app)`.
- PR #228 diff: does not modify `crates/chirp-frontend/examples/chirp.rs` or
  `crates/chirp-frontend/src/app.rs`. The diff touches only `Cargo.lock`,
  `crates/chirp-server/*`, and `crates/ferric/src/{hydrate.rs,lib.rs,ssr.rs}`.

**Finding**: `hydrate()` is never called from the browser. When the browser loads the SSR page,
the WASM bundle's start function calls `ferric::dom::mount()`, which creates a new reactive tree
and replaces the existing DOM under `#app` with client-rendered content — it does not adopt the
server-rendered markup. The PR delivers a correct `hydrate()` implementation and a correct SSR
document shell, but no wiring between them. The SSR+hydration feature is not functional
end-to-end: every SSR page load degrades to a client-side re-render.

A secondary false docstring at `crates/chirp-server/src/ssr.rs:141` asserts "the WASM bundle
initialises and calls `ferric::hydrate` after the document is parsed." This is incorrect given
the current entry point.

**What would satisfy this finding**: A change to `crates/chirp-frontend/src/app.rs::start()` (or
a new `start_ssr()` variant) that calls `ferric::hydrate(root, app_closure)` when the page
already contains server-rendered markup in `#app`, together with the corresponding wiring update
to `chirp.rs` and correction of the docstring at `crates/chirp-server/src/ssr.rs:141`.

---

### REQ-HYD-004 — Marker format consistency between SSR and hydration

**Status**: CLEAN

**What was checked**: The two files that own the marker scheme — `crates/ferric/src/ssr.rs`
(constants defined and used by the server render) and `crates/ferric/src/hydrate.rs` (constants
imported and used by the client adopt walk); whether either side defines its own copy of the
marker literals; whether the client's sentinel-detection logic matches what the server emits.

**Evidence**:
- `crates/ferric/src/ssr.rs`: `TEXT_OPEN_MARKER = "<!--$t-->"` and
  `TEXT_CLOSE_MARKER = "<!--/$t-->"` defined as `pub const &str`. No counter, timestamp, hash,
  or per-render state.
- `crates/ferric/src/hydrate.rs`: `use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER}` — a
  single import, no local string literal copy.
- `crates/ferric/src/hydrate.rs`: `is_sentinel_comment` strips `<!--`/`-->` delimiters from
  the imported constants and compares against `comment.data()`. The `.unwrap_or("")` fallback is
  dead code (constants always carry delimiters) and cannot produce a false positive.

Single source of truth enforced at the type level. The hydration protocol cannot diverge from the
server's sentinel values without changing the same constants both sides read.

---

### REQ-SSR-006 — Mismatch detection

**Status**: FINDING (BLOCKER)

**Label note**: Issue #226 and `crates/ferric/src/hydrate.rs:11` label this criterion
REQ-SSR-009. The subtree spec uses REQ-SSR-006 for the same criterion. This document uses
REQ-SSR-006 (the spec label); the discrepancy should be resolved before this review is filed.

**What was checked**: All structural-divergence detection paths in `adopt_vnode` and
`adopt_children`; the `emit_mismatch_warning` function and all call sites; all recovery
operations; the full branch file tree for `wasm-bindgen-test` coverage of the mismatch path.

**Evidence**:
- Detection (all conditions): `crates/ferric/src/hydrate.rs:72–181`
- `emit_mismatch_warning` (debug-only, no panic): `crates/ferric/src/hydrate.rs:188–203`;
  call sites at lines 78, 103, 119, 130, 158, 175
- Recovery — element replace: lines 106–110; text correct: 118–121; type replace: 128–133;
  empty root: 78–80; missing children: 175–180
- Absence of test coverage: `crates/ferric/src/hydrate.rs` (466 lines) has no `#[cfg(test)]`
  block; no `crates/ferric/tests/` directory exists on branch `work/ferric-ssr-r1`

**Finding (BLOCKER)**: No `wasm-bindgen-test` covering the mismatch detection, warning, or
recovery code paths exists in the PR. Issue #226's acceptance criterion explicitly requires a
headless test that: hydrates against a deliberately mismatched server DOM; confirms the diagnostic
fires; confirms the live DOM matches the client render of the mismatched subtree; and confirms
sibling elements remain adopted. CI passing on `ssr.rs` tests does not satisfy this criterion —
those tests cover server-render output, not the hydration or mismatch path.

A satisfying test would: build a minimal server HTML string with a structural divergence (e.g.,
the component returns `<p>` but the server DOM contains `<div>`); inject it into a headless
browser DOM under `#app`; call `ferric::hydrate(root, || ...)`; assert that `console.warn`
fired; assert the live DOM matches the client-rendered component; assert that siblings of the
mismatched element are still adopted with event handlers wired.

**Finding (NON-BLOCKER)**: Extra DOM nodes beyond the VNode child list are warned but not
removed. At `crates/ferric/src/hydrate.rs:154–163`, when DOM nodes remain after the VNode list
is exhausted, `adopt_children` calls `emit_mismatch_warning` and `break`s — comment "only warn,
do not remove." After `strip_sentinels` runs, the live DOM contains more children than the VNode
tree expects. While existing patch targets are not corrupted (extra nodes lie past the end of the
VNode index range), the live DOM no longer matches the client render of the subtree. Address in a
follow-up.

---

### REQ-MIS-001 — Axum handler pattern

**Status**: CLEAN (with NON-BLOCKER)

**What was checked**: The `ssr_handler` function signature, return type, and body; the
`render_to_string` call; the response construction and Content-Type header; the router wiring;
the `ferric` dependency in `crates/chirp-server/Cargo.toml`.

**Evidence**:
- Handler declaration: `crates/chirp-server/src/ssr.rs:159`
- `render_to_string` call: `crates/chirp-server/src/ssr.rs:169–176`
- Response construction: `crates/chirp-server/src/ssr.rs:180–185` —
  `(StatusCode::OK, [(header::CONTENT_TYPE, "text/html; charset=utf-8")], doc).into_response()`
- Router import: `crates/chirp-server/src/api/router.rs:45`
- Router registration: `crates/chirp-server/src/api/router.rs:69` — `GET /` registered before
  the SPA fallback

`ssr_handler` is `pub async fn ssr_handler() -> Response` — a valid zero-extractor Axum handler.
The response satisfies the "or equivalent" language in the criterion (functionally equivalent to
`Html(doc)`). `GET /` takes precedence over `fallback_service`.

**NON-BLOCKER** (`crates/chirp-server/src/ssr.rs:165–168`): A comment describes
`ferric::render_to_string` as a stub that panics via `todo!()`. On `work/ferric-ssr-r1`, the
function is fully implemented. The stale comment will mislead reviewers into expecting a panic
that will not occur. Remove or update it before merging.

---

### REQ-MIS-002 — HTML well-formedness and markers

**Status**: CLEAN

**What was checked**: The HTML document shell in `assemble_document`; text-node marker output
from `render_node` for a representative component; marker placement correctness relative to the
client's `adopt_children` and `is_sentinel_comment` logic; marker tests.

**Evidence**:
- Document shell: `crates/chirp-server/src/ssr.rs:104–119`
- Marker constants: `crates/ferric/src/ssr.rs` (see REQ-SSR-004 above)
- `render_node` text wrapping: `crates/ferric/src/ssr.rs:88–92` (axum_mismatch notation)
- Client sentinel check: `crates/ferric/src/hydrate.rs:242–261`
- Client import of same constants: `crates/ferric/src/hydrate.rs:35` (axum_mismatch notation)
- Marker tests: `crates/ferric/src/ssr.rs:193–212` (axum_mismatch notation)

The HTML5 document has balanced tags, valid attribute syntax, and void elements without closing
slashes. The BAR-005 placeholder comment does not contain `-->` internally and does not
prematurely close. Text nodes are wrapped as `<!--$t-->text<!--/$t-->`, producing well-formed
HTML Comment nodes the client's `is_sentinel_comment` check recognizes via the same constants.
The hydration entry point `<div id="app">` is correctly placed in the document body.

---

## Marker Format Consistency

**SSR format (REQ-SSR-004)**: HTML comment sentinels — no element attributes. Constants
`TEXT_OPEN_MARKER = "<!--$t-->"` and `TEXT_CLOSE_MARKER = "<!--/$t-->"` defined as `pub const
&str` in `crates/ferric/src/ssr.rs`. Every `VNode::Text` node is wrapped; element nodes receive
no marker. No `data-hydration-id`, no element-level markers. Sentinel placement is fully
deterministic (no counter, timestamp, or hash in either constant).

**Hydration format (REQ-HYD-004)**: HTML comment sentinels — no element attributes. Same
constants, imported via `use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER}` in
`crates/ferric/src/hydrate.rs`. No local string literal copy. `is_sentinel_comment` compares
`comment.data()` against the imported literals. The `.unwrap_or("")` fallback is dead code and
cannot produce a false positive.

**Consistency check**: CONSISTENT. Both sides share the identical literal values via the same
import path. Agreement is by construction: the client cannot diverge from the server's format
without changing the same constants both sides read.

**Documentation note**: The three spokes cite different line numbers for the two constants in
`crates/ferric/src/ssr.rs` — ssr_render says 835/842, hydration says 28/35, axum_mismatch says
33/50. All three agree on the constant names (`TEXT_OPEN_MARKER`, `TEXT_CLOSE_MARKER`), their
literal values, and their single-definition location in `crates/ferric/src/ssr.rs`. The line
number discrepancy reflects that each spoke viewed a different portion of the file. The functional
information is consistent; the citations should be verified against the current branch before this
review is merged.

---

## Non-goal Boundary

### REQ-SSR-007 / #225 — Async resource state (non-goal)

**Status**: CONFIRMED NON-GOAL

**What was checked**: The `ssr_handler` function signature for a `State` extractor and
`AppState` import; the `assemble_document` template for a live `<script
type="application/json">` state island; the module-level doc comment and handler doc comment for
explicit non-goal annotation.

**Evidence**:
- `crates/chirp-server/src/ssr.rs:138–143`: handler doc comment explicitly defers to BAR-005
  (#225) and describes the placeholder as a structural anchor for the future implementation.
- `crates/chirp-server/src/ssr.rs:114`: `assemble_document` contains only a placeholder HTML
  comment for the BAR-005 state island — no live `<script type="application/json"
  id="__state">` tag, no serialized state payload.
- `crates/chirp-server/src/ssr.rs:160–163`: `ssr_handler` has no `State` extractor and no
  `AppState` import.

The absence of async resource state carry is deliberate and annotated in both the module doc and
the handler doc. It is not a deficiency.
