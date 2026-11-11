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
