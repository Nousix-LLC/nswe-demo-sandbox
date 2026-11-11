# B2 Verdict — REQ-SSR-006: wasm-bindgen-test coverage

## Verdict: PASS

Commits `e625c3f` and `75c1eef` resolve blocker B2. All three `#[wasm_bindgen_test]`
functions in `crates/ferric/tests/hydrate_wasm.rs` carry behavioral assertions; the
mismatch detection, warning, and recovery paths in `hydrate.rs` are exercised and their
outcomes verified by DOM state checks. CI's `wasm` job reports `success`.

---

## Finding — hydrate_adopt_walk_no_structural_mutations

**REQ-SSR-004 / #224** — adopt walk without structural mutations.

**Code path covered** (`hydrate.rs`): `hydrate` → `create_effect` (first run, `slot = None`)
→ `adopt_root_vnode` → `adopt_vnode` (matching branch: `el.tag_name().eq_ignore_ascii_case(&ve.tag)`)
→ `adopt_children` → recursive `adopt_vnode` on the `<span>` child. The mismatch recovery
branch is not exercised here; this test targets the clean-match path only, which is correct.

**Assertion quality**: The test captures `before_div` and `before_span` as `web_sys::Node`
references before hydration, then retrieves the same positions after hydration and asserts
`is_same_node`. These are identity checks against live DOM nodes — not "ran without panic"
markers. If `hydrate` called `appendChild` or `replaceChild` on a matching subtree, the
returned node would be a different object and both assertions would fail.

**What is clean**: The setup (`set_inner_html("<div><span>hello</span></div>")`) exactly
mirrors the VNode passed to `hydrate`, so the test isolates the adopt walk from any recovery
logic. The cleanup helper removes the container from the document after the test, preventing
state leakage between tests.

---

## Finding — hydrate_event_wiring_post_hydration

**REQ-SSR-005 / #224** — event handlers wired post-hydration.

**Code path covered** (`hydrate.rs`): `hydrate` → `create_effect` → `adopt_root_vnode`
→ `adopt_vnode` (matching `<button>`) → `set_events` (wires the click handler via
`add_event_listener_with_callback` and stashes under `__ferric_on_click`). After the click,
the signal setter fires, `create_effect` re-runs (second run, `slot = Some(prev)`), `diff`
produces a `Patch::SetText` for the updated counter, and `apply_patches_impl` applies it.

**Assertion quality**: Two assertions, both behavioral.

1. `after_button.text_content().as_deref() == Some("1")` — this fails if the click handler
   was not wired (the signal would not update, the text would remain `"0"`). It also fails
   if the reactive patch loop is broken after hydration.

2. `before_button.is_same_node(Some(&after_button))` — this fails if the diff/patch loop
   replaced the button element instead of patching its text content, confirming that the
   element is updated in-place.

The test dispatches a programmatic click via `HtmlElement::click()` (not a mock event), so
the full browser event dispatch path runs. The signal subscription established during
`adopt_vnode` (via `count.get()` inside the component closure) correctly drives the re-render.

**What is clean**: The SSR markup (`<button>0</button>`) matches the component's initial
render, so the adopt walk proceeds without mismatch. Any regression in `set_events` or in the
reactive-update path would surface immediately on the click assertion.

---

## Finding — hydrate_mismatch_detection_recovery

**REQ-SSR-006 / #226** — mismatch detection and DOM recovery.

**Code path covered** (`hydrate.rs`): `hydrate` → `create_effect` → `adopt_root_vnode`
→ `adopt_vnode`, where `dom_node` is a `<div>` element but `vnode` is
`VNode::Element(VElement::new("p")...)`. The tag comparison
`el.tag_name().eq_ignore_ascii_case(&ve.tag)` fails → execution reaches the `other =>` branch
→ `emit_mismatch_warning` is called (in debug builds) → `parent.replace_child(&new_node, dom_node)`
replaces the `<div>` with a freshly client-rendered `<p>`.

**Detection**: Exercised. The `other =>` arm in `adopt_vnode` runs only when tag comparison
fails. If the detection logic were broken such that all comparisons returned "match," `replace_child`
would never fire, the DOM would still contain `<div>`, and the assertion below would fail.

**Warning**: Exercised. `emit_mismatch_warning` is `#[cfg(debug_assertions)]`-gated, and
test builds compile with debug assertions active, so the `console.warn` path runs during this
test. The function is not a no-op in this context. The test does not intercept `console.warn`
output — the test comment is explicit about this — but the code path is reached. Direct
console interception in a headless wasm-bindgen-test is not straightforward and not a
requirement of REQ-SSR-006 as written.

**Recovery**: Asserted. After `replace_child`:

```
el.tag_name().to_lowercase() == "p"
```

This assertion fails if `replace_child` was not called (original `<div>` remains), if it
replaced with the wrong element, or if the client-rendered node was malformed. It is a check
on observable DOM state, not on internal function calls.

**Mutual implication of detection and recovery**: If the detection branch never fires, recovery
never fires, the `<div>` persists, and the assertion fails. So the recovery assertion is also
an implicit detection assertion — the two are not independently assertable with a DOM check
alone, but their combined path is covered. A deletion of the `other =>` branch from
`adopt_vnode` would cause the test to fail.

**Mismatch code existence in `hydrate.rs`**: The mismatch code is real and present. The
`other =>` branch (`hydrate.rs`, `adopt_vnode`) builds a new node via `create_node` and
calls `replace_child`. `emit_mismatch_warning` exists as a `#[cfg(debug_assertions)]` function
with the `console::warn_1` call, plus a matching `#[cfg(not(debug_assertions))]` no-op.
Both variants are present. The mismatch paths for text nodes (content mismatch and type mismatch)
are also implemented in `adopt_vnode`, though REQ-SSR-006 is covered by the element-tag mismatch
exercised here.

---

## CI Execution Status

The CI run at `https://github.com/Nousix-LLC/nswe-demo/actions/runs/42120246308` shows the
following jobs as `success`: `fmt`, `clippy`, `test`, `wasm`, `doc`, `image`.

The `wasm` job is the headless wasm-bindgen-test run. Its `success` status confirms
`wasm-pack test --headless` executed and all three test functions in `hydrate_wasm.rs` passed.

The test file has the correct infrastructure:
- `#![cfg(target_arch = "wasm32")]` at file level — the file is excluded from native `cargo test`
  runs and compiled only for `wasm32-unknown-unknown`.
- `wasm_bindgen_test_configure!(run_in_browser)` — tests run in a headless browser, not Node.
  This is required because the tests touch `web_sys::Document`, `web_sys::Element`, and
  `HtmlElement::click()`, none of which are available in Node.
- `wasm-bindgen-test` is in `[dev-dependencies]` in `crates/ferric/Cargo.toml`.
- The file lives in `crates/ferric/tests/`, which `wasm-pack test` picks up as an integration
  test target automatically.

No test-infrastructure concerns. The CI gate is real.

---

## If PASS: What Was Clean

The following was verified for each test:

**hydrate_adopt_walk_no_structural_mutations**: The adopt walk's clean-match path is exercised
end-to-end against a live headless browser DOM. The `is_same_node` assertions check the actual
property that REQ-SSR-004 cares about — node identity, not tag name or text content. The test
would not pass if `adopt_vnode` called any structural mutation on a matching subtree.

**hydrate_event_wiring_post_hydration**: The click-dispatch approach drives the full browser
event path rather than calling the handler directly. This means the test validates both that the
listener was attached (`add_event_listener_with_callback`) and that the reactive signal/effect
loop continues to work after hydration's initial adopt pass. The two assertions are independent
failure modes that together cover the wiring and the subsequent update loop.

**hydrate_mismatch_detection_recovery**: The test sets up a tag mismatch (not a text mismatch
or a missing node), which is the primary structural mismatch case REQ-SSR-006 describes. The
recovery assertion checks the post-replacement DOM tag name, confirming the right operation ran.
The comment in the test correctly characterizes the scope: DOM recovery is asserted; console
output is exercised but not intercepted, which is consistent with the `cfg(debug_assertions)`
nature of the warning.

The mismatch code paths in `hydrate.rs` are real: the detection branch, the `console.warn`
path, and `replace_child` are all present and reachable. The tests exercise each path that
produces an observable DOM result.

Blocker B2 from review-ferric-ssr-r1 is resolved.
