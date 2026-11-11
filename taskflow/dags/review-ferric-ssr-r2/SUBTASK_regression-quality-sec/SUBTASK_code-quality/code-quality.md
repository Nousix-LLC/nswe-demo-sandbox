# Code Quality Review — New Code

Reviewed at commits `7fb90c7`, `e625c3f`, `75c1eef` (branch `work/ferric-ssr-r1`, PR #228).
Files in scope: `crates/chirp-frontend/src/app.rs` and `crates/ferric/tests/hydrate_wasm.rs`.

---

## app.rs — cfg-gate Pattern

### cfg-gate idiom

**Severity**: Pass
**Evidence**: `app.rs:154–161`

`#[cfg(target_arch = "wasm32")]` is applied at the statement level, which is the
correct scope: `ferric::hydrate` does not exist on non-wasm32 targets, so a
compile-time gate is required (a runtime `cfg!()` branch would not suppress the
missing-symbol error). The two guards — `#[cfg(target_arch = "wasm32")]` and
`#[cfg(not(target_arch = "wasm32"))]` — are mutually exclusive and exhaustive with
no gap between them. `ferric::hydrate` is called fully-qualified, so no conditional
import is needed. The pattern is idiomatic statement-level cfg for conditional
wasm32 behavior.

---

### Conditional dispatch logic

**Severity**: Warning
**Evidence**: `app.rs:155`

`has_child_nodes()` returns `true` for any child node — element nodes, whitespace
text nodes, and HTML comments. If the server's HTML template wraps SSR content with
surrounding whitespace inside `#app` (e.g., `<div id="app">\n  {content}\n</div>`),
a fresh page load with no SSR content could arrive with whitespace text-node
children and incorrectly trigger `ferric::hydrate` on an empty VNode tree.

`Element::first_element_child()` counts only element children — it excludes text and
comment nodes — and matches the actual intent of "SSR markup is present". The check
at line 155 should be verified against the server's HTML template (in
`chirp-server/src/ssr.rs`) to confirm that `#app` cannot contain incidental text
nodes on a non-SSR page load, or the guard should be changed to
`root.first_element_child().is_some()`.

---

### Error handling

**Severity**: Warning
**Evidence**: `app.rs:156`

`ferric::hydrate(root, app)` on line 156 discards its return value. If `hydrate`
returns a `Result` without a `#[must_use]` annotation, a mismatch between the
server-rendered DOM and the client VNode tree fails silently — the DOM is left in a
partially-patched state with no log entry. The adjacent `mount(root, app)` calls on
lines 158 and 161 share this gap, so the PR is consistent with the surrounding code,
but hydration failures differ in kind: `mount` on a non-empty root replaces the
content cleanly, while a hydration mismatch corrupts the existing DOM in place.

Verify `ferric::hydrate`'s return type and whether the library signals mismatch
through a returned error, a panic, or a side-channel. If it returns `Result`, either
annotate it `#[must_use]` in the library or handle the error at the call site.

---

### Docstring accuracy

**Severity**: Warning
**Evidence**: `app.rs:8`, `app.rs:103–104`

The module-level docstring on line 8 describes the module as one that "mounts the
application into `#app` (falling back to `<body>`)". The `start()` function
docstring on lines 103–104 says the function will "mount the app into `#app`
(falling back to `<body>`)". Neither mentions that on wasm32 targets `start()` now
conditionally hydrates server-rendered content rather than always mounting.

A reader consulting either docstring would not know hydration occurs. Both should be
updated to describe the conditional behavior: hydrate when SSR markup is present in
the mount root on wasm32; mount fresh otherwise; always mount on non-wasm32.

---

### Readability

**Severity**: Pass
**Evidence**: `app.rs:150–161`

The inline comment at lines 150–153 names both paths (hydrate vs mount), gives the
condition that determines which runs, and explains why a compile-time cfg gate is
used rather than a runtime branch. The two sequential `#[cfg]`-gated statements form
an exhaustive pair that Rust readers familiar with cfg attributes will follow without
ambiguity. Variable names `root` and `app` carry through unchanged from the
surrounding code. The structure is clear for the target audience.

---

## hydrate_wasm.rs — Test File

### Test structure and naming

**Severity**: Warning
**Evidence**: `hydrate_wasm.rs`, function `hydrate_event_wiring_post_hydration`

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

---

### Setup/teardown and DOM cleanup

**Severity**: Warning
**Evidence**: `hydrate_wasm.rs:97, 158, 194` (cleanup calls); `hydrate_wasm.rs:59, 107, 171` (container allocations)

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

What was checked: `cleanup()` itself is correct — it checks `parent_node()` before attempting removal, so calling it on an already-detached element is a no-op. The `make_container()` helper correctly returns the appended element. The issue is exclusively placement of the teardown call.

---

### Hardcoded strings vs. imported constants

**Severity**: Blocker
**Evidence**: `hydrate_wasm.rs:62`, `hydrate_wasm.rs:113`, `hydrate_wasm.rs:174`

All three tests inject HTML whose text nodes are bare strings — no `<!--$t-->` / `<!--/$t-->` sentinel markers. `render_to_string` in `ssr.rs` wraps every `VNode::Text` in `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER`, so actual SSR output for any text node contains flanking comment nodes the hydration path must handle. The gap between what each test injects and what SSR would produce:

| Test | Injected (line) | Actual SSR output |
|---|---|---|
| `hydrate_adopt_walk_no_structural_mutations` | `<div><span>hello</span></div>` (line 62) | `<div><span><!--$t-->hello<!--/$t--></span></div>` |
| `hydrate_event_wiring_post_hydration` | `<button>0</button>` (line 113) | `<button><!--$t-->0<!--/$t--></button>` |
| `hydrate_mismatch_detection_recovery` | `<div>text</div>` (line 174) | `<div><!--$t-->text<!--/$t--></div>` |

The import block (lines 11–15) imports nothing from `ferric::ssr`. There are no local constant definitions for `TEXT_OPEN_MARKER` or `TEXT_CLOSE_MARKER` anywhere in the file — the sentinels are absent entirely, not duplicated.

The hydration walk in `hydrate.rs` must count or skip the `<!--$t-->` and `<!--/$t-->` comment nodes when determining structural VNode children and when adopting text nodes. Because no test injects those comment nodes, the sentinel-handling code paths are never reached. All three tests — including the REQ-SSR-004 adopt-walk test — pass on input that production SSR cannot generate. The adopt-walk coverage is false: the test verifies identity preservation against a DOM whose structure differs from what `render_to_string` would produce.

---

### Duplication

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

- `set_inner_html`: three different HTML fixtures, each the SSR output for a different scenario.
- `ferric::hydrate` closure: a static nested div/span in test 1, a reactive signal
  plus click handler in test 2, and a deliberately mismatched `<p>` element in test 3.
- Pre-hydration captures: tests 1 and 2 each capture node refs between `set_inner_html`
  and `hydrate`; test 3 does not.

There is no copy-paste where both structure and content are the same. No correctness
risk: a fix to the VNode pattern in one test would not leave another silently wrong,
because the tests cover distinct behaviors.

---

### Assertion quality

**Severity**: Warning
**Evidence**: `hydrate_wasm.rs:65–70` (Test 1 node capture), `:83–95` (Test 1 assertions)

**Test 1 — REQ-SSR-004 (`hydrate_adopt_walk_no_structural_mutations`)**

The test captures `before_div` and `before_span` before calling `ferric::hydrate`, then asserts `is_same_node` after. `is_same_node` checks reference equality — a re-created element with identical HTML fails these checks. That coverage is real and would catch the most common form of structural mutation.

The gap: the SSR markup is `<div><span>hello</span></div>`. The text node `"hello"` is a child of `<span>`. No reference to that text node is captured before hydration, and no assertion is made on its identity afterward. If `ferric::hydrate` preserves `<div>` and `<span>` as objects but re-creates the text node — for example by calling `set_text_content` or by clearing and rebuilding child nodes — this test passes. Text nodes are DOM nodes; re-creating one is a structural mutation under REQ-SSR-004.

What would close this: capture `let before_text = before_span.first_child().expect(...)` before hydration, then after hydration capture `let after_text = after_span.first_child().expect(...)` and assert `before_text.is_same_node(Some(&after_text))`. That would fail if the text node is replaced.

**Test 2 — REQ-SSR-005 (`hydrate_event_wiring_post_hydration`)**

Both assertions check the right conditions. `text_content().as_deref() == Some("1")` fails if the click handler is not wired or the signal-driven re-render does not run. `before_button.is_same_node(Some(&after_button))` fails if `ferric::hydrate` discards the server node and creates a fresh one. The two assertions together would catch: unwired events, failed reactive updates, and fresh-mount instead of adoption. No gap in assertion coverage for this test.

**Test 3 — REQ-SSR-006 (`hydrate_mismatch_detection_recovery`)**

`el.tag_name().to_lowercase() == "p"` checks that the container's first child has the client tag after mismatch recovery. This fails if the server `<div>` is not replaced. The test does not explicitly check that the original `<div>` node is removed — an implementation that prepended `<p>` before `<div>` without removing it would pass, since `first_child` would then be the new `<p>`. That failure mode is not a realistic implementation path; the assertion covers the cases worth guarding against.

The combined severity is **Warning**: Tests 2 and 3 would each catch a regression in the behavior they claim, and Test 1 would catch element-level mutations. The gap is confined to text node identity in Test 1. A broken adopt walk that re-creates text nodes while preserving element nodes would not be detected.

---

## Fresh Non-Blockers (if any)

**From app.rs**: `app.rs:156` — `ferric::hydrate` is called fully-qualified while `mount` arrives via `use ferric::prelude::*`. This is a minor style inconsistency; `hydrate` may not be re-exported from the prelude, so the full path may be the only option. No action needed unless `hydrate` is added to the prelude in a later revision.

**From hydrate_wasm.rs**: None found.

---

## Overall Code Quality Verdict: FAIL

The hardcoded strings finding at `hydrate_wasm.rs:62, 113, 174` is a **Blocker**.

All three tests inject HTML without the `<!--$t-->` / `<!--/$t-->` sentinel markers that `render_to_string` emits for every `VNode::Text`. The sentinel-handling code paths in the hydration walk (`hydrate.rs`) are never exercised. All three tests — including the REQ-SSR-004 adopt-walk test that must demonstrate structural-mutation safety — pass on input that production SSR cannot generate. The adopt-walk coverage is false: identity preservation is verified against a DOM structure that `render_to_string` does not produce.

**What must be fixed**: update all three `set_inner_html` fixtures to use the sentinel-wrapped form (`<!--$t-->text<!--/$t-->`), or import and use `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER` from `ferric::ssr`. Verify that `ferric::hydrate` handles the flanking comment nodes correctly and that the existing assertions still hold against the corrected fixtures.

The five Warning findings (conditional dispatch guard, error handling, docstring accuracy, test naming, setup/teardown cleanup, assertion text-node gap) do not block merge on their own but should be tracked.
