# hydrate_wasm.rs Quality Notes

## Test structure and naming

**Severity**: Warning
**Evidence**: `hydrate_wasm.rs`, function `hydrate_event_wiring_post_hydration`

### What was examined

All three `#[wasm_bindgen_test]` functions were assessed for behavioral naming and
single-behavior focus. Both helpers (`make_container`, `cleanup`) and the private
`document()` bridge were assessed for naming clarity. The file's section structure
was reviewed.

### What is clean

- `hydrate_adopt_walk_no_structural_mutations` names the behavior directly: the adopt
  walk produces no structural mutations. The name is actionable as a coverage label.

- `hydrate_mismatch_detection_recovery` is equally clear: a mismatch is detected and
  the DOM is recovered. Both parts of the behavior appear in the name.

- `make_container` and `cleanup` are well-named for their roles. `make_container`
  signals construction (Rust convention), `cleanup` signals teardown. Both are
  correctly placed before the test section and separated by the `// ── Helpers ──`
  marker.

- `document()` is a minimal private bridge to `web_sys::Document`. Its name is
  unambiguous and its scope is narrow.

- Section markers (`// ── Helpers ──`, `// ── Tests ──`) give the file clear visual
  structure. Each test has a doc comment that links it to its requirement.

### Finding

`hydrate_event_wiring_post_hydration` verifies two distinct properties in one test
body without structural separation between them:

1. After a programmatic click, the button's text content updates to `"1"` — the click
   handler fired and the signal-driven re-render applied.
2. After that same re-render, the button's DOM node identity is preserved — the element
   was patched, not replaced.

The function name covers only the first. A reader scanning test names to find out
which test asserts "node identity preserved after reactive update" would not stop
at this function. The doc comment does list both assertions explicitly, so the intent
is not hidden from someone who opens the body — but test names are the primary
navigation surface.

The second assertion (node identity preserved on re-render) is thematically adjacent
to `hydrate_adopt_walk_no_structural_mutations`, which checks node identity during the
initial adopt walk. The event test checks the same invariant under a different
trigger: a reactive re-render after a click. These are worth distinguishing by name
because they exercise different code paths.

Concretely: renaming or splitting would look like:

- `hydrate_click_handler_fires_and_rerenders` (assertion 1 only), and
- `hydrate_reactive_rerender_preserves_node_identity` (assertion 2 only)

or keeping them together under a name that covers both:

- `hydrate_click_handler_fires_and_node_identity_preserved`

This is a Warning, not a Blocker. The current name does not misrepresent coverage —
both assertions are present in the body and listed in the doc comment — but it leaves
one of the two asserted behaviors unnamed in the function signature.

## Setup/teardown and DOM cleanup

**Severity**: Warning
**Evidence**: hydrate_wasm.rs:97, 158, 194 (cleanup calls); hydrate_wasm.rs:59, 107, 171 (container allocations)

All three tests follow the same pattern: `make_container()` appends a `<div>` to `<body>` at the top of the function, and `cleanup(&container)` removes it at the very end — after every `.expect()` and assertion. That placement is the problem. If any earlier operation panics, the cleanup line is never reached.

In `wasm-bindgen-test` with `run_in_browser` configured (line 17), all tests share one browser page. When a test panics before returning, the container it allocated stays in `<body>` for the rest of the session. In this framework, cleanup code that follows a failed assertion does not run — the panic exits the test body before reaching it.

The early-exit points in each test, all preceding `cleanup()`:

- **`hydrate_adopt_walk_no_structural_mutations`**: `.expect()` at lines 67, 70, 82, 91; `assert!` at lines 83–86 and 92–95. `cleanup()` is at line 97.
- **`hydrate_event_wiring_post_hydration`**: `.expect()` at lines 118, 137, 139, 145; `assert_eq!` at lines 146–150; `assert!` at lines 153–156. `cleanup()` is at line 158.
- **`hydrate_mismatch_detection_recovery`**: `.expect()` at lines 184, 187; `assert_eq!` at lines 188–192. `cleanup()` is at line 194.

The comment on `make_container()` (line 29) already states the invariant: "Must be paired with `cleanup` to avoid leaking between tests." The code acknowledges the contract but does not enforce it mechanically.

**Why Warning and not Blocker**: every test scopes its DOM queries to its own `container` reference. `container.first_child()` looks inside the specific element that test created, not across `<body>`. Orphaned containers from a failed prior test accumulate in `<body>` but do not reach those queries, so test results stay correct in the current suite. This becomes a Blocker if any test adds a broader query — `body.children`, `document.query_selector("div")`, or similar — which would see leftovers from earlier failures.

**What would satisfy this finding**: replace the end-of-function cleanup with a RAII guard. A local struct holding the container element, with a `Drop` implementation that calls `parent.remove_child(&el)`, runs cleanup on both the happy path and on any panic exit. One guard per test function; the existing `cleanup()` helper can be called from `Drop`. Example shape:

```rust
struct ContainerGuard(web_sys::Element);
impl Drop for ContainerGuard {
    fn drop(&mut self) { cleanup(&self.0); }
}
let _g = ContainerGuard(make_container());
let container = _g.0.clone();
```

The three tests are otherwise structurally identical in this regard, so the fix applies uniformly.

**What was clean**: `cleanup()` itself is correct — it checks `parent_node()` before attempting removal, so calling it on an already-detached element is a no-op. The `make_container()` helper correctly returns the appended element. The issue is exclusively placement of the teardown call.

## Hardcoded strings vs. imported constants

**Severity**: Blocker
**Evidence**: hydrate_wasm.rs:62, hydrate_wasm.rs:113, hydrate_wasm.rs:174

All three tests inject HTML whose text nodes are bare strings — no `<!--$t-->` / `<!--/$t-->` sentinel markers. `render_to_string` in `ssr.rs` wraps every `VNode::Text` in `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER`, so actual SSR output for any text node contains flanking comment nodes the hydration path must handle. The gap between what each test injects and what SSR would produce:

| Test | Injected (line) | Actual SSR output |
|---|---|---|
| `hydrate_adopt_walk_no_structural_mutations` | `<div><span>hello</span></div>` (line 62) | `<div><span><!--$t-->hello<!--/$t--></span></div>` |
| `hydrate_event_wiring_post_hydration` | `<button>0</button>` (line 113) | `<button><!--$t-->0<!--/$t--></button>` |
| `hydrate_mismatch_detection_recovery` | `<div>text</div>` (line 174) | `<div><!--$t-->text<!--/$t--></div>` |

The import block (lines 11–15) imports nothing from `ferric::ssr`. There are no local constant definitions for `TEXT_OPEN_MARKER` or `TEXT_CLOSE_MARKER` anywhere in the file — the sentinels are absent entirely, not duplicated.

The hydration walk in `hydrate.rs` must count or skip the `<!--$t-->` and `<!--/$t-->` comment nodes when determining structural VNode children and when adopting text nodes. Because no test injects those comment nodes, the sentinel-handling code paths are never reached. All three tests — including the REQ-SSR-004 adopt-walk test — pass on input that production SSR cannot generate. The adopt-walk coverage is false: the test verifies identity preservation against a DOM whose structure differs from what `render_to_string` would produce.

## Duplication

**Severity**: Pass
**Evidence**: N/A

The two shared-scaffolding helpers, `make_container()` (hydrate_wasm.rs:31) and
`cleanup()` (hydrate_wasm.rs:45), already extract the only setup/teardown that is
genuinely the same across all three tests: create a fresh `<div>`, attach it to
`<body>`, remove it after the assertion. That is the right extraction boundary —
same boilerplate every time, no test-specific parameters.

The remaining outer frame is structurally similar (call `set_inner_html`, call
`ferric::hydrate`, assert, call `cleanup`) but the content inside each step is
meaningfully distinct for each acceptance criterion:

- `set_inner_html`: three different HTML fixtures (`<div><span>hello</span></div>`,
  `<button>0</button>`, `<div>text</div>`), each the SSR output for a different scenario.
- `ferric::hydrate` closure: a static nested div/span in test 1, a reactive signal
  plus click handler in test 2, and a deliberately mismatched `<p>` element in test 3.
  No shared body to extract.
- Pre-hydration captures: tests 1 and 2 each capture node refs between `set_inner_html`
  and `hydrate`; test 3 does not. The interleaved structure makes a single "run test"
  wrapper awkward rather than helpful.

There is no "structure AND content the same" copy-paste anywhere in the file. The
closest echo is `VElement::new("TAG").child(VNode::Text("...".into()))` appearing in
tests 1 and 3, but the tags and text differ, and the structural context is different
(test 1 nests it inside a `<div>`, test 3 uses it as the entire component). No
correctness risk: a fix to the VNode pattern in one test would not leave the other
silently wrong, because the components are testing distinct behaviors.

## Assertion quality

**Severity**: Warning
**Evidence**: hydrate_wasm.rs:65–70 (Test 1 node capture), :83–95 (Test 1 assertions)

---

### Test 1 — REQ-SSR-004 (`hydrate_adopt_walk_no_structural_mutations`)

The test captures `before_div` (line 65) and `before_span` (line 68) before calling `ferric::hydrate`, then asserts `before_div.is_same_node(Some(&after_div))` and `before_span.is_same_node(Some(&after_span))` after (lines 83–95). `is_same_node` checks reference equality, not value equality — a re-created element with identical HTML fails these checks. That coverage is real and would catch the most common form of structural mutation.

The gap: the SSR markup is `<div><span>hello</span></div>`. The text node `"hello"` is a child of `<span>`. No reference to that text node is captured before hydration, and no assertion is made on its identity afterward. If `ferric::hydrate` preserves `<div>` and `<span>` as objects but re-creates the text node — for example by calling `set_text_content` or by clearing and rebuilding child nodes during the adopt walk — this test passes. Text nodes are DOM nodes; re-creating one is a structural mutation under REQ-SSR-004.

What would close this: capture `let before_text = before_span.first_child().expect(...)` before hydration, then after hydration capture `let after_text = after_span.first_child().expect(...)` and assert `before_text.is_same_node(Some(&after_text))`. That would fail if the text node is replaced.

---

### Test 2 — REQ-SSR-005 (`hydrate_event_wiring_post_hydration`)

Both assertions check the right conditions. `text_content().as_deref() == Some("1")` at line 145 fails if the click handler is not wired or the signal-driven re-render does not run after the click. `before_button.is_same_node(Some(&after_button))` at line 152 fails if `ferric::hydrate` discards the server node and creates a fresh one — `before_button` was captured before hydration and would no longer match the container's first child. The two assertions together would catch: unwired events, failed reactive updates, and fresh-mount instead of adoption. No gap in assertion coverage for this test.

---

### Test 3 — REQ-SSR-006 (`hydrate_mismatch_detection_recovery`)

`el.tag_name().to_lowercase() == "p"` at line 188 checks that the container's first child has the client tag after mismatch recovery. This fails if the server `<div>` is not replaced. The test does not explicitly check that the original `<div>` node is removed from the document — an implementation that prepended `<p>` before the `<div>` without removing `<div>` would pass, since `first_child` would then be the new `<p>`. That failure mode is not a realistic implementation path; the assertion covers the cases worth guarding against. The comment in the test acknowledges that detection (the `cfg(debug_assertions)`-gated warning) is not tested here, which is a deliberate scope choice.

---

### Summary

The combined severity is **Warning**: Tests 2 and 3 would each catch a regression in the behavior they claim, and Test 1 would catch element-level mutations. The gap is confined to text node identity in Test 1. A broken adopt walk that recreates text nodes while preserving element nodes would not be detected by this suite.

## Fresh Non-Blockers (if any)

None found.
