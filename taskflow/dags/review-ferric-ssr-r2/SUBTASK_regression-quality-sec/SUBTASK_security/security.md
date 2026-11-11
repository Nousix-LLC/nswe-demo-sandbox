# Security Review — New Code

Commits reviewed: `7fb90c7`, `e625c3f`, `75c1eef` (PR #228, branch `work/ferric-ssr-r1`)

---

## HTML Injection and Escaping

### New rendering paths

`crates/ferric/src/ssr.rs` is the new render path. `render_node` calls `escape_html` for every
`VNode::Text` node and for every attribute value in `VNode::Element`. The escaping function
replaces all five injection-risky characters: `<`, `>`, `&`, `"`, `'`.

The tests in `ssr.rs` itself verify this explicitly — `escapes_all_five_injection_chars_in_text_content`
and `escapes_all_five_injection_chars_in_attribute_values` each assert all five escape sequences
are present in the output.

**Tag names and attribute names are not escaped.** Both come from developer-supplied literals in
this framework's usage pattern — `VElement::new("div")`, `.attr("id", "ferric-root")` — and are
never user data. No new code in these commits passes user input into tag or attribute names. This
is the same contract the existing `dom` module holds.

No finding.

### assemble_document

`assemble_document` in `crates/chirp-server/src/ssr.rs` inserts `server_html` raw into the
document shell. This is by design: `server_html` is the output of `ferric::render_to_string`,
which has already escaped every text node and attribute value. The function is a template
wrapper for already-safe markup.

`wasm_script_path` is inserted verbatim into the `src` attribute of a `<script>` tag. The
docstring marks the caller responsible for supplying a quote-free, URL-safe value, and a
`debug_assert!` enforces the double-quote constraint in debug builds. In release builds the
assertion is elided. The value in the current call site is always the hardcoded literal
`"/pkg/chirp.js"`, so no user input reaches this parameter.

**Advisory (not a blocker):** `debug_assert!` is stripped in release builds. If a future
caller ever passes a computed `wasm_script_path`, the quote check disappears and an injected
`"` could break the attribute boundary. Worth noting in a follow-up: either HTML-escape
`wasm_script_path` unconditionally, or change the assertion to `assert!`. Not a current
vulnerability because the value is a constant; flagged to avoid a gap opening silently.

No blocking finding.

### Hydration DOM writes

`hydrate.rs` constructs and updates the DOM using only safe browser APIs:

- `document.create_text_node(content)` — sets text node content; never parses HTML.
- `dom.set_attribute(name, value)` — passes through the browser's attribute-setting API;
  does not inject HTML.
- `set_text_content(Some(value))` — sets text content on existing nodes; does not parse HTML.
- `replace_child` / `append_child` / `insert_before` — structural DOM operations; no raw
  HTML string is parsed.

`innerHTML` does not appear in `hydrate.rs` anywhere. No unescaped string is written to a
DOM position where script could execute.

No finding.

### Attribute values

New attribute-setting code in `hydrate.rs` (mismatch recovery path):

```rust
for (name, value) in &ve.attrs {
    dom.set_attribute(name, value)
        .expect("create_node: set_attribute failed");
}
```

`set_attribute` in the browser DOM API does not parse `value` as HTML; special characters in
attribute values are handled by the browser's attribute storage. No injection path introduced.

No finding.

---

## Test File Security

### Logged or exposed data

`hydrate_wasm.rs` calls no logging functions. The test infrastructure interacts with
`container`, `document()`, and `body()` — standard WASM test plumbing. No config paths,
token values, or structural information about the test environment is emitted.

No finding.

### Hardcoded secrets or tokens

No API keys, auth tokens, passwords, or environment-specific values are present. Test strings
are `"hello"`, `"0"`, `"1"`, `"text"` — strictly behavioral assertions.

No finding.

### DOM manipulation in tests

The tests use `container.set_inner_html(...)` to simulate server-rendered HTML injected into
the page before hydration begins. The strings are developer-authored constants (`"<div><span>hello</span></div>"`,
`"<button>0</button>"`, `"<div>text</div>"`), not user data. Using `set_inner_html` to simulate
SSR output in a browser test is the correct technique here — `innerHTML` with literal, trusted
strings is accepted test scaffolding.

The tests are `#[cfg(target_arch = "wasm32")]` and gated by `wasm_bindgen_test`, so they run
only in the WASM test harness, not in any server-side context.

No concerning pattern. The `set_inner_html` calls here do not establish a precedent for use
with dynamic content in production code.

---

## Overall Security Verdict: PASS

**What was checked:**

- `escape_html` in `ferric/ssr.rs`: escapes all five injection-risky characters in both text
  content and attribute values. Test coverage for the escape function is present and complete.
- `render_node` / `render_to_string`: no path places unescaped user data into the HTML output.
- `assemble_document`: inserts already-escaped `server_html` raw (by design); `wasm_script_path`
  is a developer constant; `debug_assert` quote-guard noted as advisory only.
- `hydrate.rs` DOM writes: all use safe browser APIs (`create_text_node`, `set_attribute`,
  `set_text_content`); no `innerHTML` usage.
- `hydrate_wasm.rs`: no sensitive data, no hardcoded secrets, no concerning DOM patterns.
- `app.rs` cfg-gated dispatch: routes to `hydrate` vs `mount` based on DOM state; no injection
  path.

One advisory note raised: the `debug_assert!` guard on `wasm_script_path` in
`assemble_document` is elided in release builds. No current vulnerability (the value is a
constant), but the guard should be a release-build assertion to prevent future callers from
accidentally passing dynamic values.
