# SSR render_to_string Findings (REQ-SSR-001–005)

## Summary

The `render_to_string` implementation in `crates/ferric/src/ssr.rs` correctly renders a VNode tree
to an HTML string on a native (non-wasm32) host, with no DOM dependency. The cfg split is exact:
the `ssr` module compiles on all targets; the `hydrate` module is `#![cfg(target_arch = "wasm32")]`
only. Per-request reactive isolation is mechanically sound — `render_to_string` creates a fresh
`ReactiveScope`, runs the component closure once inside it, serialises the resulting VNode tree,
then drops the scope, which disposes all reactive nodes created during the call and removes every
signal subscription before the function returns. Nested VNode trees render recursively at arbitrary
depth, confirmed by tests at two and three levels. Text-boundary markers (`<!--$t-->` /
`<!--/$t-->`) wrap every `VNode::Text` node; both sides of the hydration contract import these as
constants from `ssr.rs`, with no local copies. `render_to_string` is a crate-root `pub` re-export,
ungated, and is called directly from the Axum handler in `chirp-server`. All five criteria are met.
Two non-blockers are recorded below: a test gap (the SSR tests do not directly assert
`subscriber_count == 0` after a render, as the issue #223 acceptance criterion states), and a stale
comment in `chirp-server/src/ssr.rs` that incorrectly claims the implementation "currently panics
(via `todo!()`)."

---

## Findings by Criterion

### REQ-SSR-001 — render_to_string renders without DOM

**Status**: CLEAN

**What was checked**: Imports and module-level doc in `crates/ferric/src/ssr.rs`; cfg guards on the
`ssr` and `hydrate` modules in `crates/ferric/src/lib.rs`; `ferric` dependency entry in
`crates/chirp-server/Cargo.toml`; test-macro style in `ssr.rs` (native `#[test]` vs.
`#[wasm_bindgen_test]`).

**Evidence**:

- `crates/ferric/src/ssr.rs:827` (module doc): "it must never reference `web_sys` or
  `wasm_bindgen`" — borne out by the imports: the only import is `use crate::vdom::VNode;`. No
  `web_sys`, no `wasm_bindgen`, no DOM call anywhere in the file.
- `crates/ferric/src/lib.rs` diff, `+pub mod ssr;`: no `#[cfg(target_arch = "wasm32")]` guard —
  the SSR module compiles on all targets.
- `crates/ferric/src/lib.rs` diff, `+pub use crate::ssr::render_to_string;`: also ungated.
- `crates/ferric/src/hydrate.rs:325`: `#![cfg(target_arch = "wasm32")]` — the DOM-dependent
  hydration module is correctly wasm32-only. The cfg split between the two modules is exact.
- `crates/chirp-server/Cargo.toml` diff: `ferric = { path = "../ferric" }` with no Cargo features
  gate; comment says "NATIVE (non-wasm) dependency: `ferric::ssr` compiles and runs on the server
  target."
- `ssr.rs` test suite: all tests use `#[test]` (native), not `#[wasm_bindgen_test]`.

The server crate can depend on `ferric` as a plain Rust library dependency and call
`ferric::render_to_string` with no wasm toolchain involvement.

---

### REQ-SSR-002 — Signal-driven components render from initial state; no reactivity during SSR

**Status**: CLEAN (with NON-BLOCKER — see below)

**What was checked**: `render_to_string` body in `ssr.rs`; `ReactiveScope::run` and `Drop`
implementations in `signal.rs`; the `no_stale_subscriber_leak` proof test in `signal.rs`; isolation
tests in `ssr.rs`.

**Evidence**:

- `crates/ferric/src/ssr.rs:942–955`: `render_to_string` creates a `ReactiveScope`, calls
  `scope.run(f)` once to obtain the VNode, then renders it to a string. The scope drops at the end
  of the function (comment at line 955 names the reverse-declaration-order drop: `vnode` then
  `scope`), which runs `impl Drop for ReactiveScope`.
- `crates/ferric/src/signal.rs:486–493`: `ReactiveScope::run` pushes this scope's `NodeId` onto
  `owner_stack` before calling `f` and pops it after. It does **not** push onto `observer_stack`.
  Because the runtime's `track` function at line 246 only records a subscription when
  `observer_stack` is non-empty, bare `signal.get()` calls inside `f()` during SSR read the current
  value without registering any subscription.
- `crates/ferric/src/signal.rs:502–506`: `impl Drop for ReactiveScope` calls
  `rt.dispose(self.id)`, which at lines 312–338 recursively disposes all owned children, removes
  the disposed node from every `subscribers` and `sources` set, and purges any pending-effect entry
  for it. No subscription survives the scope drop.
- `crates/ferric/src/signal.rs:985–1022`: `no_stale_subscriber_leak` test demonstrates the
  full proof path: a `create_effect` inside a `ReactiveScope` subscribes to a signal; dropping the
  scope reduces `subscriber_count` to 0 and reclaims arena nodes. This is the same dispose path
  `render_to_string` takes.
- `crates/ferric/src/ssr.rs:1087–1120`: `two_renders_produce_independent_outputs` — two
  consecutive renders with distinct seeded `create_signal` values produce independent HTML; neither
  output contains the other's content.
- `crates/ferric/src/ssr.rs:1123–1153`: `signal_created_inside_render_does_not_survive_beyond_call`
  — signals created in one render do not appear in the next render's output.

**NON-BLOCKER**: Issue #223 states the acceptance criterion as "a signal seeded only for one render
has zero subscribers after `render_to_string` completes." The SSR tests verify HTML independence but
do not directly assert `subscriber_count == 0` on a signal after the render that created it. The
isolation mechanism is mechanically correct (proven in `signal.rs:985–1022`), but the
SSR-specific invariant from the acceptance criterion is not directly asserted in `ssr.rs` tests. A
test like `assert_eq!(subscriber_count(sig), 0)` immediately after a `render_to_string` call that
created `sig` internally would close this gap.

---

### REQ-SSR-003 — Child components and slot-based composition render correctly; nested trees exercised

**Status**: CLEAN

**What was checked**: `render_node` recursion in `ssr.rs`; `VNode` data model in `vdom.rs`;
nesting tests in `ssr.rs`.

**Evidence**:

- `crates/ferric/src/ssr.rs:896–928`: `render_node` for `VNode::Element` iterates
  `el.children` and recurses into each — arbitrary nesting is supported with no depth limit.
- `crates/ferric/src/vdom.rs:35–56`: `VNode::Element(VElement)` with `children: Vec<VNode>` —
  the data model supports unbounded nesting, with child appending via `VElement::child()` and
  `VElement::children()` builders.
- `crates/ferric/src/ssr.rs:1036–1050`: `renders_nested_children_at_correct_depth` — renders
  `ul > li(text "one") + li(text "two")` and asserts the full byte-exact output including markers.
- `crates/ferric/src/ssr.rs:1053–1065`: `renders_deeply_nested_structure` — renders
  `section > div > p > text("deep")` (three levels of nesting) and asserts byte-exact output.

In this framework, "components" are closures or functions returning `VNode`, and "slots" are
expressed as `VElement::child()` calls passing child nodes. There is no separate `Component` or
`Slot` variant in `VNode` — composition is function composition producing nested `VElement` trees.
`render_node`'s recursion over `el.children` handles this correctly with no component-specific
dispatch path needed. The two nesting tests cover the recursive case at the depths required by the
acceptance criteria.

---

### REQ-SSR-004 — Rendered HTML includes well-formed, stable hydration markers

**Status**: CLEAN

**What was checked**: The two marker constants in `ssr.rs`; `render_node` text-node emission;
import of these constants in `hydrate.rs`; marker-specific tests in `ssr.rs`.

**Evidence**:

- `crates/ferric/src/ssr.rs:835`: `pub const TEXT_OPEN_MARKER: &str = "<!--$t-->";`
- `crates/ferric/src/ssr.rs:842`: `pub const TEXT_CLOSE_MARKER: &str = "<!--/$t-->";`
- `crates/ferric/src/ssr.rs:897–901`: for `VNode::Text(s)`, `render_node` emits
  `TEXT_OPEN_MARKER` + `escape_html(s)` + `TEXT_CLOSE_MARKER` — every text node is wrapped.
- `crates/ferric/src/hydrate.rs:335`: `use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER};` —
  the client's hydration walk imports the same constants; no local copies exist.
- `crates/ferric/src/ssr.rs:1020–1024`: `text_node_wrapped_in_markers` asserts that
  `render_to_string(|| text("world"))` produces `"<!--$t-->world<!--/$t-->"`.
- `crates/ferric/src/ssr.rs:1026–1030`: `empty_text_node_wrapped_in_markers` covers the
  empty-text edge case.

The markers are HTML comment nodes, not element attributes. All text nodes receive the same
open/close pair. The hydration protocol is positional (tree walk), with the comment sentinels
used to adjust child-index counting so VNode indices align with DOM child indices after the
`strip_sentinels` pass in `hydrate.rs:507–531`. See the **Marker Schema** section below.

**Note for synthesis**: The brief anticipated `data-hydration-id` attribute-style markers. This
implementation uses HTML comment sentinels instead. The synthesis task should verify that
SUBTASK_hydration found the same comment-based protocol and that both spokes agree on the constant
values and their usage.

---

### REQ-SSR-005 — `render_to_string` callable from an Axum handler

**Status**: CLEAN (with NON-BLOCKER — see below)

**What was checked**: Export declaration in `ferric/src/lib.rs`; `ferric` dependency in
`chirp-server/Cargo.toml`; call site in `chirp-server/src/ssr.rs`; routing in
`chirp-server/src/api/router.rs`.

**Evidence**:

- `crates/ferric/src/lib.rs` diff: `pub use crate::ssr::render_to_string;` — public crate-root
  re-export with no `#[cfg(target_arch = "wasm32")]` gate.
- `crates/chirp-server/Cargo.toml` diff: `ferric = { path = "../ferric" }` — native workspace
  dependency; no features gate.
- `crates/chirp-server/src/ssr.rs:239`: `let server_html = ferric::render_to_string(|| { ... });`
  — called directly inside `pub async fn ssr_handler() -> Response`.
- `crates/chirp-server/src/lib.rs` diff: `pub mod ssr;` — module is pub, making `ssr_handler`
  accessible.
- `crates/chirp-server/src/api/router.rs` diff: `use crate::ssr::ssr_handler;` and
  `.route("/", get(ssr_handler))` — wired into the Axum router.

`render_to_string` is in scope, exported, and called. The SSR handler compiles and links without a
wasm toolchain.

**NON-BLOCKER** (documentation accuracy): `crates/chirp-server/src/ssr.rs:236–237` contains the
comment: "The stub implementation in `ferric::ssr` currently panics (via `todo!()`); the
`ferric-ssr-r1-server-render` spoke provides the real implementation." This is incorrect.
`ferric::render_to_string` in this PR is a complete implementation with no `todo!()` or deliberate
panic. The comment is stale development-phase text that was not removed when the full implementation
landed in the same PR. The code is correct; the comment misleads. It should be removed.

---

## Marker Schema (REQ-SSR-004) — for synthesis cross-check

**Attribute name**: N/A — markers are HTML comments, not element attributes.

**Value format**:
- Open marker: the literal string `<!--$t-->` (constant `TEXT_OPEN_MARKER`,
  `crates/ferric/src/ssr.rs:835`)
- Close marker: the literal string `<!--/$t-->` (constant `TEXT_CLOSE_MARKER`,
  `crates/ferric/src/ssr.rs:842`)
- These wrap every `VNode::Text` node's HTML-escaped text content:
  - `VNode::Text("hello")` → `<!--$t-->hello<!--/$t-->`
  - `VNode::Text("<foo>")` → `<!--$t-->&lt;foo&gt;<!--/$t-->`
- Element nodes (`VNode::Element`) receive no marker of any kind.

**Stability mechanism**: Static string constants. The same `<!--$t-->` / `<!--/$t-->` pair wraps
every text node on every render, regardless of content, tree position, depth, or component
identity. No sequence number or positional ID is encoded in the marker. Uniqueness is not a
property of these markers — the hydration protocol relies on structural agreement (same VNode tree
structure on server and client) and uses the comment sentinels only to adjust DOM child-index
counting. The `strip_sentinels` pass in `crates/ferric/src/hydrate.rs:507–531` removes all Comment
nodes whose `.data()` equals `"$t"` or `"/$t"` after the adopt walk, restoring DOM child indices to
match VNode path indices for subsequent diff/patch passes.
