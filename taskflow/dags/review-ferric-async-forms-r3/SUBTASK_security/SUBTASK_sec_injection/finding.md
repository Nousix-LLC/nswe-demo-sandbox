## Finding

- **severity**: clean
- **concern**: HTML injection / escaping
- **location**: N/A
- **description**: Neither `on_input_event_handler` nor any other new code path in commits 9fedad9, 9557f0c, and 838239e writes user-supplied input to the DOM without passing through the library's established safe-sink mechanism. The library's escaping approach is structural: `dom.rs` routes all text into the DOM through `document.create_text_node(content)` (initial render, line 106) and `node.set_text_content(Some(value))` (`Patch::SetText`, line 143), and routes attribute values through `element.set_attribute(name, value)`. All three are DOM text APIs; none invoke the HTML parser. Arbitrary user-supplied strings — including markup-bearing input like `<script>alert(1)</script>` — are treated as literal character data and cannot create executable DOM nodes. There is no `innerHTML`, `set_inner_html`, or equivalent HTML-parsing sink anywhere in the diff or in the existing rendering infrastructure.

The specific data-flow for `on_input_event_handler` (`form.rs`, B3):
1. `HtmlInputElement::value()` → `raw.set(value)` writes the raw DOM string into `Signal<String>`.
2. When the app author uses that signal in a render (e.g., as `VNode::Text(signal.get())`), the string travels through `create_text_node` or `set_text_content` — both of which bypass the HTML parser.
3. When used as an attribute (e.g., the `value` attribute of an `<input>` via `Bind::value_attr()`), it travels through `set_attribute` — also HTML-parser-free and safe for arbitrary string values.

No escaping gap was introduced by these commits. The DOM-text-API approach is the correct architectural choice; it makes explicit per-call escaping unnecessary by never crossing the data/markup boundary.

## What was examined

**Files read:**
- PR #193 diff (full, all three remediation commits)
- `crates/ferric/src/form.rs` — new file; reviewed `on_input_event_handler` body, `on_input_handler` body, and `Bind::value_attr`
- `crates/ferric/src/dom.rs` — full file; reviewed `create_node` (text branch: `create_text_node`), `apply_patches` (`SetText` branch: `set_text_content`; `SetAttr` branch: `set_attribute`), and confirmed the absence of any `innerHTML` / `set_inner_html` call
- `crates/ferric/src/vdom.rs` — reviewed `VNode` enum (Text variant), `Patch` enum (`SetText` variant), and confirmed no HTML-emitting output path in the new `EventHandler` enum or `on_with_event` builder

**Sub-questions answered:**

1. *Does `on_input_event_handler` write the raw `String` from `HtmlInputElement::value()` into a signal?* Yes. The closure calls `raw.set(input_el.value())` without transformation.

2. *Does the library's existing rendering path escape signal values before inserting them into the DOM?* Yes, by construction: `create_text_node` and `set_text_content` are the only code paths that write signal-derived strings to DOM text nodes; both are inherently safe (they set text content, not innerHTML). `set_attribute` handles attribute values equally safely.

   There is no explicit `html_escape()` call, nor is one needed. The DOM text API IS the escaping boundary.

3. *Does any new code path write user-supplied input to the DOM without the established mechanism?* No. Every path from user input to the DOM in this diff (signal → `VNode::Text` → `create_text_node`/`set_text_content`; signal → attribute → `set_attribute`) uses safe DOM APIs exclusively.
