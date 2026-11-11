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
