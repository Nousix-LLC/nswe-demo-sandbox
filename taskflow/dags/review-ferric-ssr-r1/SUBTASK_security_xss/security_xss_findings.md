# PR #228 HTML Escaping / XSS Security Findings

## Summary

The escaping posture is correct for every path where user-supplied data is expected to reach
the HTML output. `ferric/src/ssr.rs` implements a single `escape_html` helper that covers all
five injection characters (`<`, `>`, `&`, `"`, `'`), and the helper is called consistently for
both text node content and attribute values. No unescaped user-data path exists in the SSR
output.

Two non-blocker issues are worth recording. First, `assemble_document` in
`chirp-server/src/ssr.rs` inserts its `wasm_script_path` parameter into an HTML `src` attribute
without HTML-escaping it, protected only by a `debug_assert!` that is stripped in release builds;
this is not currently exploitable because the only caller passes a hardcoded literal, but the
function is public and future callers may not. Second, the existing test suite covers the two most
important escaping paths (text content, attribute values) but has no test for a full `<script>`
injection payload through the assembled document, and no test for `wasm_script_path` with HTML
metacharacters in a release build.

---

## Findings by Area

### A. Text node escaping

**Status**: CLEAN

**What was checked**: Every place a `VNode::Text` node's string content is written into the
HTML output.

**Evidence**: `ferric/src/ssr.rs`, `render_node`, lines 92–94:

```rust
out.push_str(TEXT_OPEN_MARKER);
out.push_str(&escape_html(s));   // ← escape_html called on s before insertion
out.push_str(TEXT_CLOSE_MARKER);
```

`escape_html` (lines 69–81) replaces all five injection characters:

```rust
'<' => out.push_str("&lt;"),
'>' => out.push_str("&gt;"),
'&' => out.push_str("&amp;"),
'"' => out.push_str("&quot;"),
'\'' => out.push_str("&#39;"),
```

The match arm is exhaustive and there is no other code path for text nodes.
Signal values reach this function as `VNode::Text` via `vdom::text(signal.get())`, so
signal-driven content is covered.

**Finding**: None.

---

### B. Attribute value escaping

**Status**: CLEAN (attribute values); NON-BLOCKER note on attribute names

**What was checked**: Every attribute emitted by `render_node`; whether `data-hydration-id`
or any other dynamically constructed attribute exists in this PR; and whether any attribute could
carry user-supplied data without escaping.

**Evidence — attribute values**: `ferric/src/ssr.rs`, `render_node`, lines 100–104:

```rust
out.push(' ');
out.push_str(name);                   // attribute name — see note below
out.push_str("=\"");
out.push_str(&escape_html(value));    // ← escape_html called on value
out.push('"');
```

Attribute values go through `escape_html` without exception. All five injection characters
are escaped.

**Evidence — attribute names**: Line 101 writes `name` directly without escaping. Attribute
names in this framework come from `VElement::attr(name, value)` in component code — authored
as Rust string literals (`"id"`, `"class"`, `"href"`, etc.). In the placeholder component added
by this PR (`chirp-server/src/ssr.rs:174`) all attribute names are string literals. There is no
API that feeds request-time user input into an attribute name today.

**Evidence — `data-hydration-id`**: This attribute does not appear in the PR. The hydration
boundary protocol uses HTML comment sentinels (`<!--$t-->` / `<!--/$t-->`) rather than element
attributes; `data-hydration-id` does not exist in this change.

**Finding (non-blocker)**: Attribute names are not HTML-escaped at
`ferric/src/ssr.rs:101`. The current component code is safe (names are literals), but `VElement`
accepts any `Into<String>` for the name, so there is no type-level barrier preventing a future
component from accidentally passing user-supplied data as an attribute name. No escaping is applied
in that case. This is a documentation / convention gap, not an active vulnerability.

---

### C. Raw HTML insertions

**Status**: CLEAN (intentional documented use); NON-BLOCKER on `wasm_script_path`

**What was checked**: Any location where a string is inserted into the HTML output without
passing through `escape_html`, including `format!` calls and `push_str` calls in both SSR files.

**Evidence — `server_html` raw insertion**: `chirp-server/src/ssr.rs:113`:

```rust
  <div id="app">{server_html}</div>
```

This inserts the return value of `ferric::render_to_string` directly into the document shell. The
insertion is intentional: `server_html` is structured markup produced by the renderer, not raw
user input. All user-controlled values within that markup have been escaped by `render_node` before
reaching this point. The docstring (line 64) makes this contract explicit.

**Evidence — `wasm_script_path` raw insertion**: `chirp-server/src/ssr.rs:115`:

```rust
  <script type="module" src="{wasm_script_path}"></script>
```

`wasm_script_path` is inserted verbatim into an HTML `src` attribute. The function guards
against a `"` character with a `debug_assert!` at lines 99–103:

```rust
debug_assert!(
    !wasm_script_path.contains('"'),
    "wasm_script_path must not contain '\"': {wasm_script_path:?}"
);
```

`debug_assert!` is a no-op in release builds. The check also covers only `"` — it does not cover
`<`, `>`, or `'`. A caller passing a path such as `"/evil.js' onerror='alert(1)"` or a path
containing `>` would produce malformed HTML in a release build.

The only current caller is `ssr_handler` at line 178, which passes the hardcoded literal
`"/pkg/chirp.js"` — this call is not exploitable. However, `assemble_document` is a `pub` function
and its docstring says the caller is responsible for the safety of `wasm_script_path`. That shifts
the burden to future callers with no release-build guard.

**Finding (non-blocker)**: `chirp-server/src/ssr.rs:115` — `wasm_script_path` inserted into
the HTML `src` attribute without HTML-escaping; only a `debug_assert!` guards against `"`, not
other metacharacters, and that assert is stripped in release builds. The current call site is
safe. The public API exposes a risk to future callers. Consider either HTML-escaping the value
before insertion or restricting the type (e.g., a newtype that validates the path at construction
time).

---

### D. Format string trust boundaries

**Status**: CLEAN for user-data paths; NON-BLOCKER notes recorded above

**What was checked**: Every `format!`, `push_str`, and `push` call in the SSR code path that
interpolates a runtime value into an HTML context.

**`ferric/src/ssr.rs` — render_node (lines 89–119)**

| Line | Call | Value source | Escaped? |
|------|------|-------------|----------|
| 93 | `push_str(&escape_html(s))` | `VNode::Text` content (user data expected) | Yes — `escape_html` |
| 98 | `push_str(&el.tag)` | Tag name (component-authored literal) | No — by convention |
| 101 | `push_str(name)` | Attribute name (component-authored literal) | No — by convention |
| 103 | `push_str(&escape_html(value))` | Attribute value (user data expected) | Yes — `escape_html` |
| 117 | `push_str(&el.tag)` | Tag name in closing tag (same value) | No — by convention |

The two channels where user-supplied data is expected at runtime — text content and attribute
values — both go through `escape_html`. The two channels that are not escaped — tag names and
attribute names — are sourced from component code and are not expected to carry user input.

**`chirp-server/src/ssr.rs` — assemble_document (lines 104–120)**

| Line | Value | Source | Escaped? |
|------|-------|--------|----------|
| 113 | `{server_html}` | Renderer output (all inner values already escaped) | Intentional raw HTML |
| 115 | `{wasm_script_path}` | Caller-supplied path | No (see finding in C) |

**`ferric/src/hydrate.rs`** — the `format!("<{}>", ve.tag)` and similar calls at lines 113,
416 go into `emit_mismatch_warning`, which calls `web_sys::console::warn_1`. They are diagnostic
strings sent to the browser console, not inserted into the HTML document. They are also gated
behind `#[cfg(target_arch = "wasm32")]` and are entirely off the SSR code path.

**Finding**: No unescaped user-data value reaches the HTML output through any
`format!`/`push_str` call. The `wasm_script_path` finding is recorded above in C.

---

### E. Test coverage for escaping

**Status**: PARTIAL (non-blocker)

**What was checked**: Whether the test suite would detect a regression in escaping, whether a
`<script>` injection payload is specifically tested, and whether the `wasm_script_path` insertion
is tested in release conditions.

**Tests that exist and are strong**:

- `ferric/src/ssr.rs` — `escapes_all_five_injection_chars_in_text_content`: passes `<>&"'` as a
  text node and asserts all five escape sequences are present. This test would catch a missing
  character in `escape_html` and would catch removal of the `escape_html` call on line 93.
- `ferric/src/ssr.rs` — `escapes_all_five_injection_chars_in_attribute_values`: same five
  characters in an attribute value; covers the escape on line 103.
- `chirp-server/src/ssr.rs` — `assemble_document_rejects_quoted_script_path`: debug-only
  `should_panic` test that verifies a `"` in `wasm_script_path` triggers the assert.

**What is missing**:

1. No test passes a `<script>alert(1)</script>` or `<img src=x onerror=alert(1)>` payload into a
   component prop and asserts that the full assembled document contains only the escaped form
   (`&lt;script&gt;...`). The existing tests cover `render_to_string` output; they do not go
   through `assemble_document`. The gap is narrow because the escaping happens inside
   `render_to_string`, but an end-to-end test through `assemble_document` would catch any future
   shell-level bypass.

2. No release-build test for `wasm_script_path` with HTML metacharacters other than `"` (e.g., a
   path containing `>` or `'`). The `should_panic` test is `#[cfg(debug_assertions)]` only. In a
   release build, any character other than `"` passes silently.

**Finding (non-blocker)**: Test coverage for escaping is solid for the core cases. Two gaps:
(a) no end-to-end test through `assemble_document` with an injection payload in a text prop;
(b) the `wasm_script_path` guard is only tested in debug builds and only for `"`. Neither gap
represents a currently-exploitable path, but adding tests for them would prevent silent
regressions.

---

## Verdict

**PASS** — the HTML escaping posture is correct. All user-data paths in the SSR output
(`VNode::Text` content and attribute values) pass through `escape_html` before reaching the
HTML string. No unescaped user-supplied value can reach the document through the current code.

Two non-blocker findings are recorded:

1. **`assemble_document` / `wasm_script_path` insertion** (`chirp-server/src/ssr.rs:115`):
   the parameter is not HTML-escaped and is only guarded by a `debug_assert!` against `"`. The
   current caller is safe (hardcoded literal). The public function's caller contract should be
   enforced in release builds or the value should be HTML-escaped at the call site.

2. **Test gaps** (`ferric/src/ssr.rs`, `chirp-server/src/ssr.rs`): no end-to-end test for
   a `<script>` injection payload through the full document shell; no release-build test for
   `wasm_script_path` with metacharacters other than `"`. Both are worth filing before the
   escaping logic grows.

Neither finding blocks merge. No XSS risk is present in the code as shipped.
