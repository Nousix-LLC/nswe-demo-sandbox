# B2 Verdict — REQ-SSR-006 (wasm-bindgen-test coverage)

## Verdict

**RESOLVED**

Three `#[wasm_bindgen_test]` functions in `crates/ferric/tests/hydrate_wasm.rs` (commit `75c1eef`) provide
substantive behavioral coverage for the adopt-walk, event-wiring, and mismatch-detection + recovery code
paths in `hydrate.rs`. Each test makes assertions that would fail if the specific behavior it names were
broken. The `wasm` CI job passed on commit `75c1eef`.

---

## Requirements Covered

REQ-SSR-004, REQ-SSR-005, REQ-SSR-006

---

## Evidence

### Files read

| File | Commit | Lines |
|------|--------|-------|
| `crates/ferric/tests/hydrate_wasm.rs` | `75c1eef` | 197 |
| `crates/ferric/src/hydrate.rs` | `75c1eef` | ~350 |
| `crates/ferric/src/ssr.rs` | `75c1eef` | ~200 |

### CI run

Run 42120246308 (`work/ferric-ssr-r1`, PR #228) — 6 jobs, all PASS:

| Job | ID | Result |
|-----|----|--------|
| fmt | 127570408412 | ✓ |
| clippy | 127570408728 | ✓ |
| test | 127570408770 | ✓ |
| **wasm** | **127570408865** | **✓** |
| doc | 127570408977 | ✓ |
| image | 127570683825 | ✓ |

Annotations are infrastructure notices (Node.js 20 deprecation, ubuntu-latest runner migration), not
test failures. The `wasm` job ran on the commit that includes `75c1eef`.

### Module-level test setup

```rust
// hydrate_wasm.rs, lines 9–16
#![cfg(target_arch = "wasm32")]
wasm_bindgen_test_configure!(run_in_browser);
```

Module gate and `run_in_browser` are both present. All three tests access the DOM (`window`, `document`,
`Element`, `HtmlElement.click()`); `run_in_browser` is required and correctly set.

### Test 1 — `hydrate_adopt_walk_no_structural_mutations` (REQ-SSR-004)

**Code path in `hydrate.rs`**: `hydrate()` → `create_effect` first run → `adopt_root_vnode()` →
`adopt_vnode()` matching-tag branch (`Some(el) if el.tag_name().eq_ignore_ascii_case(&ve.tag)`) →
`adopt_children()` recursively.

**Setup** (hydrate_wasm.rs ~lines 55–76): injects `<div><span>hello</span></div>` via `set_inner_html`;
captures `before_div` and `before_span` node references before hydration.

**Component**: structurally identical — same `<div>/<span>/text` shape, same text `"hello"`.

**Assertions** (~lines 88–97):
```rust
assert!(
    before_div.is_same_node(Some(&after_div)),
    "REQ-SSR-004: <div> was recreated during the adopt walk (structural mutation detected)"
);
assert!(
    before_span.is_same_node(Some(&after_span)),
    "REQ-SSR-004: <span> was recreated during the adopt walk (structural mutation detected)"
);
```

**Mutation test**: `is_same_node()` returns `false` when a new element is created via `createElement`,
even if the new element has the same tag and content as the original. If `hydrate()` performed a
fresh-mount instead of an adopt walk, both assertions fail. The test cannot pass on a broken implementation.

### Test 2 — `hydrate_event_wiring_post_hydration` (REQ-SSR-005)

**Code path in `hydrate.rs`**: adopt-walk matching branch → `set_events()` wires click handler →
`create_effect` subsequent run (triggered by click → `count.set`) → `diff()` + `apply_patches_impl()`
(SetText patch on the button's text node).

**Setup** (~lines 108–130): injects `<button>0</button>`; creates `create_signal(0_i32)` and captures
button node. Component reads `count.get()` (reactive subscription) and wires `onClick { count.set(val + 1) }`.

**Action**: `.click()` on the button via `dyn_into::<web_sys::HtmlElement>()`.

**Assertions** (~lines 139–151):
```rust
assert_eq!(
    after_button.text_content().as_deref(),
    Some("1"),
    "REQ-SSR-005: button text did not update to \"1\" after click"
);
assert!(
    before_button.is_same_node(Some(&after_button)),
    "REQ-SSR-005: button node was recreated after click — element identity not preserved"
);
```

**Mutation test**: The first assertion requires the full reactive pipeline — event wired → handler fires →
signal increments → effect re-renders → DOM patches. Breaking event wiring leaves the DOM at "0"; the
assertion fails. The second assertion fails if the patch path replaced the element rather than patching
the text node.

### Test 3 — `hydrate_mismatch_detection_recovery` (REQ-SSR-006)

**Code path in `hydrate.rs`**: `adopt_root_vnode()` → `adopt_vnode()` → mismatch branch (`other =>`) →
`emit_mismatch_warning()` → `parent.replace_child(&new_node, dom_node)`.

**Setup** (~lines 165–174): injects `<div>text</div>` (server renders `<div>`); component returns
`VNode::Element(VElement::new("p")...)` — deliberate `<div>` vs `<p>` tag mismatch.

**Assertion** (~lines 183–188):
```rust
assert_eq!(
    el.tag_name().to_lowercase(),
    "p",
    "REQ-SSR-006: mismatch recovery did not replace server <div> with client <p>"
);
```

**Mutation test**: If `adopt_vnode()` hits the mismatch branch but skips `replace_child()` (early return,
wrong branch taken, or recovery path deleted), the container's first child remains `<div>`.
`el.tag_name().to_lowercase()` returns `"div"`, not `"p"` — the assertion fails. This test cannot pass
without `replace_child` executing on a tag mismatch.

The `emit_mismatch_warning()` function (defined in `hydrate.rs` as `#[cfg(debug_assertions)]`) is called
in the mismatch branch before `replace_child`. Because `wasm-pack test` compiles with debug assertions
by default, `emit_mismatch_warning()` executes during this test run. The test comment acknowledges
this explicitly: "this test verifies DOM recovery rather than the console output." The console.warn
path is exercised but not asserted (see Finding 1).

---

## Findings

### Finding 1 — Warning assertion absent in `hydrate_mismatch_detection_recovery`

- **Severity**: Note
- **Requirement**: REQ-SSR-009 (console.warn on mismatch — `cfg(debug_assertions)`)
- **Location**: `crates/ferric/tests/hydrate_wasm.rs` commit `75c1eef`, test function `hydrate_mismatch_detection_recovery`
- **Principle**: A test for a named behavior should assert that behavior, not only its downstream effects
- **Why it matters**: `emit_mismatch_warning()` is exercised in this test run (debug builds), but the test
  asserts only the DOM recovery outcome, not that `console.warn` was called. If `emit_mismatch_warning`
  were removed or silenced, this test would still pass. REQ-SSR-009 currently has no test that would fail
  if the warning were broken.
- **Resolution**: Add a `console.warn` capture assertion — for example, by installing a `window.console.warn`
  stub before calling `hydrate()` and asserting the stub was invoked with the expected mismatch message.
  This is a follow-on ticket, not a remediation for B2: REQ-SSR-009 is not in the in-scope requirement
  list for this re-review (`_GLOBAL.md` Identities section), and B2's blocker was "zero wasm-bindgen-test
  for `hydrate.rs`," which is resolved.

---

## What Was Examined and Found Clean

- **`wasm_bindgen_test_configure!(run_in_browser)`** — present at module level, applies to all three tests;
  correct because all tests use `window`, `document`, and DOM APIs that require a browser context.

- **`#[wasm_bindgen_test]` annotation on all three functions** — confirmed at the function level in
  `hydrate_wasm.rs`; no test is accidentally compiled as a plain `#[test]`.

- **`#![cfg(target_arch = "wasm32")]` module gate** — prevents the file from compiling on a native host,
  keeping the test suite correctly separated from native unit tests.

- **Test 1 assertions are behaviorally meaningful** — `is_same_node()` distinguishes the same DOM node
  from a structurally-identical replacement; the assertion would not pass on a fresh-mount path.

- **Test 2 exercises the full reactive pipeline** — the click handler → signal → effect → diff → patch
  chain must all function for the DOM text to show "1". Event-wiring failure is detected.

- **Test 2 node-identity assertion on the button** — confirms `apply_patches_impl` uses `SetText`
  (patch in place) rather than `Replace` (remove and recreate) for a text-content change.

- **Test 3 mismatch recovery path** — the `replace_child` call in `adopt_vnode`'s mismatch branch is
  the only code path that changes `<div>` to `<p>`; the DOM tag assertion is specific and would fail
  without it.

- **DOM cleanup between tests** — each test calls `cleanup(&container)` to remove the container from
  `document.body`, preventing state leakage between tests.

- **Helper functions** (`document()`, `make_container()`, `cleanup()`) — reusable, correctly abstracted,
  shared across all three tests with no copy-paste divergence.

- **No sentinel comment interaction issues** — tests inject raw HTML via `set_inner_html` without
  `TEXT_OPEN_MARKER / TEXT_CLOSE_MARKER` sentinels; `adopt_children` correctly handles this case
  (no sentinel nodes to skip, `is_sentinel_comment` returns false).

- **CI `wasm` job** — PASS on commit `75c1eef` (run 42120246308, job 127570408865); annotations are
  infrastructure notices unrelated to test outcomes.

- **Code quality of test file** — assertion messages consistently include the REQ ID; doc comments
  describe setup and behavioral intent; test isolation via per-test containers; no apparent copy-paste
  errors between the three test bodies.
