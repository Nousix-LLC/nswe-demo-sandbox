### HTML Injection in ssr.rs

**Result**: Clean
**Evidence**: `crates/ferric/src/ssr.rs:L69-L122` at commit `75c1eef` — read the full `escape_html` function and all string-building paths in `render_node`; traced every point where data reaches the HTML output string.

The SSR output path runs through `render_node` (L89-L122), which handles two `VNode` variants:

- **`VNode::Text(s)` (L91-L95):** the text string is passed through `escape_html(s)` before being appended to output. No unescaped text content enters the HTML string.
- **`VNode::Element(el)` attribute values (L99-L104):** each attribute value is passed through `escape_html(value)` in the attribute loop. No unescaped attribute value enters the HTML string.

`escape_html` (L69-L82) covers all five injection-risky characters: `<`→`&lt;`, `>`→`&gt;`, `&`→`&amp;`, `"`→`&quot;`, `'`→`&#39;`. The coverage is complete for both the text-content and attribute-value contexts where it is applied.

Tag names (`el.tag`, L98, L117) and attribute names (`name`, L101) are written without escaping. These are developer-controlled static values in component definitions — the VNode tree is constructed from `VElement::new("div")`, `.attr("class", "nav")`, etc., not from user-submitted data. No runtime path in the library routes user input through the tag-name or attribute-name positions.

**Docstring fix in `7fb90c7`:** that commit's diff touches `crates/chirp-server/src/ssr.rs` (item 4 of the `assemble_document` docstring) and `crates/chirp-frontend/src/app.rs`. `crates/ferric/src/ssr.rs` does not appear in the `7fb90c7` diff. The ferric SSR module was not modified by that commit, so it introduces no new string interpolation into the HTML output path.

The two escaping tests in the same file — `escapes_all_five_injection_chars_in_text_content` and `escapes_all_five_injection_chars_in_attribute_values` — both assert each of the five escape substitutions and are present and passing at `75c1eef`. They would fail if the escaping were removed or incomplete.
