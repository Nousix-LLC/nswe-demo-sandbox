# hydrate() Findings (REQ-HYD-001–004)

## Summary

The `hydrate()` function at `crates/ferric/src/hydrate.rs` is correctly implemented: the adopt
pass walks the server-rendered DOM positionally without re-creating matching nodes, signal
subscriptions are established identically to `dom::mount`, and the text-node sentinel mechanism
shares a single-source-of-truth constant from `crates/ferric/src/ssr.rs`. One blocker holds
this PR from landing: `hydrate()` is never called from the WASM entry point — the browser-side
start function calls `ferric::dom::mount()` instead, which replaces the server-rendered markup
rather than adopting it. Two non-blockers also merit attention: neither the hydrate→signal→DOM
sequence nor the full SSR→hydrate path has an integration test.

---

## Findings by Criterion

### REQ-HYD-001 — hydrate() attaches without re-creating nodes

**Status**: CLEAN

**What was checked**: The adopt pass entry points (`adopt_root_vnode` → `adopt_vnode` →
`adopt_children`) in `crates/ferric/src/hydrate.rs`. Every call site of `appendChild`,
`replace_child`, `create_element`, and `create_text_node` in that file. The signal-listener
wiring path (`set_events`).

**Evidence**:
- `crates/ferric/src/hydrate.rs:98–105` — `adopt_vnode` casts the existing DOM node with
  `dyn_ref::<Element>()` (no `create_element`), calls `set_events` on the already-present
  element, and recurses into children without any structural mutation on tag match.
- `crates/ferric/src/hydrate.rs:113–115` — text-node happy path: branch comment "Perfect text
  match — nothing to do"; no operations performed.
- `crates/ferric/src/hydrate.rs:102–103`, `280–325` — `set_events` calls
  `add_event_listener_with_callback` on the existing server-rendered element.
- `crates/ferric/src/hydrate.rs:148–192` — `adopt_children` iterates `child_nodes()` in order,
  skipping sentinel comment nodes. No `querySelector` or `data-hydration-id` attribute is used.
- `crates/ferric/src/hydrate.rs:88`, `187`, `120–122`, `131–133` — `append_child` and
  `replace_child` appear only in mismatch-recovery branches (empty root, missing child,
  tag mismatch, type mismatch).
- `crates/ferric/src/hydrate.rs:5–11` — module-level doc comment: "No structural DOM mutation
  occurs when every node matches (REQ-SSR-004)."
- `crates/ferric/src/hydrate.rs:65–67` — `strip_sentinels` removes SSR comment artifacts
  after the adopt pass; this is not a content-node mutation.

**Finding**: none. The adopt pass satisfies REQ-HYD-001.

---

### REQ-HYD-002 — Signal updates propagate post-hydration

**Status**: FINDING (NON-BLOCKER)

**What was checked**: The `hydrate()` reactive-update code path in
`crates/ferric/src/hydrate.rs`. Whether the same `diff`/`apply_patches_impl` machinery used
by `dom::mount` is reused for post-hydration updates. All test functions added in PR #228 across
`crates/ferric/src/ssr.rs`, `crates/ferric/src/hydrate.rs`, `crates/chirp-server/src/ssr.rs`,
and the `crates/ferric/tests/` path on branch `work/ferric-ssr-r1`.

**Evidence (reactive path — CLEAN)**:
- `crates/ferric/src/hydrate.rs:1–57` — `hydrate()` calls `create_effect`; first closure
  run calls `adopt_root_vnode` (the `None` arm), establishing signal subscriptions. Subsequent
  runs take the `Some(prev)` branch, calling `diff` and `apply_patches_impl`. This is
  structurally identical to `dom::mount`. No separate subscription mechanism is introduced.

**Finding**: No `wasm_bindgen_test` or integration test exercises the hydrate→signal→DOM
sequence. The `crates/ferric/tests/` directory does not exist on branch `work/ferric-ssr-r1`.
The test modules in `crates/ferric/src/hydrate.rs` contain zero `#[test]` or
`#[wasm_bindgen_test]` functions. Issue #224, REQ-HYD-002 acceptance criterion 2 — "After
hydrate, an event dispatch updates the DOM in place through the signal/patch path; the element
is not recreated" — has no test verifying it.

The reactive path is correctly implemented and reuses proven `dom::mount` machinery. The gap
is test observability, not a demonstrable code defect. Per inherited constraints, this does
not hold landing.

**What would satisfy this finding**: A `wasm_bindgen_test` test that calls `render_to_string`,
inserts the HTML into a test DOM, calls `hydrate()`, triggers a signal update, and asserts
the DOM node changed in place (text content updated; no element recreated).

---

### REQ-HYD-003 — hydrate() called once from WASM entry point

**Status**: FINDING (BLOCKER)

**What was checked**: The WASM entry point (`crates/chirp-frontend/examples/chirp.rs`
`fn main()` and `crates/chirp-frontend/src/app.rs` `pub fn start()`). The `ferric::hydrate()`
implementation in `crates/ferric/src/hydrate.rs`. The server-side document assembly in
`crates/chirp-server/src/ssr.rs`. The full call chain from `chirp.rs:fn main()` through to
DOM interaction.

**Evidence**:
- `crates/chirp-frontend/examples/chirp.rs:16` — entry point: `fn main()` calls
  `chirp_frontend::start()`.
- `crates/chirp-frontend/src/app.rs:114–135` — `start()` calls `mount(root, app)`, not
  `ferric::hydrate(root, app)`.
- PR #228 does not modify either file. The diff touches only: `Cargo.lock`,
  `crates/chirp-server/Cargo.toml`, `crates/chirp-server/src/api/router.rs`,
  `crates/chirp-server/src/lib.rs`, `crates/chirp-server/src/ssr.rs`,
  `crates/ferric/src/hydrate.rs`, `crates/ferric/src/lib.rs`, `crates/ferric/src/ssr.rs`.

**What this means**: When the browser loads the SSR page, the WASM bundle's start function calls
`chirp_frontend::start()`, which calls `ferric::dom::mount()`. `mount()` creates a new reactive
tree and replaces the existing DOM under `#app` with client-rendered content — it does not
adopt the server-rendered markup. `ferric::hydrate()` is never called.

The PR delivers a correct `hydrate()` implementation and a correct SSR document shell, but no
wiring between them. The SSR+hydration feature is not functional end-to-end: every SSR page
load degrades to a client-side re-render.

**Secondary false docstring**: `crates/chirp-server/src/ssr.rs:141` asserts "the WASM bundle
initialises and calls `ferric::hydrate` after the document is parsed." This is incorrect given
the current entry point.

**What satisfies this finding**: A change to `crates/chirp-frontend/src/app.rs::start()` (or
a new `start_ssr()` variant) that calls `ferric::hydrate(root, app_closure)` when the page
already contains server-rendered markup in `#app`, together with the corresponding wiring update
to `chirp.rs` and correction of the `ssr.rs` docstring at line 141.

**What was clean**: `hydrate()` itself (`crates/ferric/src/hydrate.rs`) — adopt pass, sentinel
cleanup, and reactive-effect wiring are correctly implemented; the function is `wasm32`-gated
and re-exported cleanly. `assemble_document`/`ssr_handler` (`crates/chirp-server/src/ssr.rs`) —
HTML shell shape matches the design spec; unit tests cover structure, the empty-HTML case, and
the quote-injection guard. Module layout: `ferric/src/lib.rs` correctly gates `hydrate` on
`target_arch = "wasm32"` and keeps `ssr` unconditional.

---

### REQ-HYD-004 — Marker format consistency between SSR and hydration

**Status**: CLEAN

**What was checked**: The two files that own the marker scheme — `crates/ferric/src/ssr.rs`
(constants defined and used by the server render) and `crates/ferric/src/hydrate.rs` (constants
imported and used by the client adopt walk). Whether either side defines its own copy of the
marker literals. Whether the client's sentinel-detection logic matches what the server emits.
Determinism of the marker values.

**Evidence**:
- `crates/ferric/src/ssr.rs:28,35` — `TEXT_OPEN_MARKER = "<!--$t-->"` and
  `TEXT_CLOSE_MARKER = "<!--/$t-->"` defined as `pub const &str`. No counter, timestamp, hash,
  or per-render state. Same component tree always produces the same sentinel placement.
- `crates/ferric/src/hydrate.rs:32` — `use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER}`;
  no local string literal copy.
- `crates/ferric/src/hydrate.rs` `is_sentinel_comment` — strips `<!--`/`-->` delimiters from
  the imported constants and compares against `comment.data()`. Comparison is exact. The
  `.unwrap_or("")` fallback is dead code (constants always carry delimiters) but cannot produce
  a false positive.

**Finding**: none. The design enforces single-source-of-truth at the type level. No
`data-hydration-id` attribute, `get_attribute`, `dataset`, or `querySelector` calls appear in
`hydrate.rs`; the marker mechanism uses HTML comment nodes. REQ-HYD-004 is satisfied.

---

## Marker Schema (REQ-HYD-004) — for synthesis cross-check

**Attribute name**: None. The PR does not use `data-hydration-id` or any element attribute.
Markers are HTML comment nodes that bracket each `VNode::Text` boundary in the serialized HTML.

**Value format**:
- Open sentinel: an HTML comment node whose `.data()` is `$t` — written into the HTML string
  as `<!--$t-->`; constant `TEXT_OPEN_MARKER = "<!--$t-->"` at `crates/ferric/src/ssr.rs:28`
- Close sentinel: an HTML comment node whose `.data()` is `/$t` — written as `<!--/$t-->`;
  constant `TEXT_CLOSE_MARKER = "<!--/$t-->"` at `crates/ferric/src/ssr.rs:35`
- Example: `VNode::Text("hello")` renders as `<!--$t-->hello<!--/$t-->`

**Determinism mechanism**: Both constants are `pub const &str` values. They contain no counter,
timestamp, hash, or any per-render state. Sentinel placement is fully deterministic for any
given component tree.
