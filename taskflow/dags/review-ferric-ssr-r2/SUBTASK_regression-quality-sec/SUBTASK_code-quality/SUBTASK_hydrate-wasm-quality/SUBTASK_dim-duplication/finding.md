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
