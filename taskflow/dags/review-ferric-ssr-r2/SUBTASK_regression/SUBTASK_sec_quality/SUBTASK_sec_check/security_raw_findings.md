## Security Findings

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

### DOM Spoofing in app.rs

**Result**: Clean
**Evidence**: `app.rs:L154-L161` at commit `75c1eef` — Read the full `start()` function (L111–L162). Traced how `root` is acquired (L141–L148: `document.get_element_by_id("app")` falling back to `document.body()`), then followed the `has_child_nodes()` branch at L155: when the mount root contains children it calls `ferric::hydrate(root, app)`; when empty it calls `mount(root, app)`. Confirmed the `#[cfg(target_arch = "wasm32")]` guard is correctly scoped — the conditional only compiles on the WASM32 target; non-WASM builds unconditionally call `mount`.

For this to be a DOM spoofing attack, an attacker must place nodes in `#app` (or `<body>`) before the WASM module's `start()` runs, pushing `has_child_nodes()` to `true` and routing execution into `ferric::hydrate()` against attacker-controlled markup. Two preconditions could produce that DOM state: (1) JavaScript already executing on the same origin — which is XSS and already constitutes full DOM control, making this branch irrelevant; or (2) server-side HTML injection in the SSR path — which is the separate concern analyzed by `SUBTASK_html_inj` in `ssr.rs`. Neither case introduces a new attack vector through the `has_child_nodes()` gate: an attacker who can reach the DOM before WASM runs already has capabilities that dwarf what this branch could add.

The threat is not realistic for this crate's distribution model. `chirp-frontend` is a `wasm32-unknown-unknown` WASM binary served as part of the same-origin web application; the browser's Same-Origin Policy prevents cross-origin scripts from modifying its DOM. A WASM library crate is not a served page controlled by an attacker — it executes in the user's browser, under the same origin as the host page, with no external party able to inject into its DOM without a pre-existing same-origin vulnerability.

### Test Injection Safety in hydrate_wasm.rs

**Result**: Clean
**Evidence**: `hydrate_wasm.rs:L9,L17,L30-L47,L57-L195` at commit `75c1eef` — Read the full file (195 lines). Three sub-checks were performed:

**(a) `set_inner_html` calls — L62, L113, L174.** All three test fixtures call `container.set_inner_html(...)` with a hardcoded string literal: `"<div><span>hello</span></div>"` (L62), `"<button>0</button>"` (L113), and `"<div>text</div>"` (L174). No test-controlled variable or external input is concatenated into any of these strings.

**(b) Dynamic DOM text — L110, L123, L129.** The only non-literal value that reaches the DOM via `VNode::Text` is `val.to_string()` at L129. Tracing back: `val = count.get()` at L123, and `count = create_signal(0_i32)` at L110. The source is a typed Rust `i32` initialized to a constant inside the test function; it is not an externally-sourced or test-caller-controlled string. The remaining `VNode::Text` calls at L75 and L178 use fixed literals (`"hello".into()`, `"text".into()`).

**(c) WASM test entry points — L57–L58, L105–L106, L169–L170.** All three `#[wasm_bindgen_test]` functions take no parameters. No function in the file carries a `#[wasm_bindgen]` export attribute. There is no callable surface through which an external caller could supply input that would reach the DOM. The module-level `#![cfg(target_arch = "wasm32")]` gate at L9 and `wasm_bindgen_test_configure!(run_in_browser)` at L17 further confine the entire file to WASM browser test execution. Test scaffolding (`make_container`, L30–L40; `cleanup`, L43–L47) constructs DOM nodes through the typed `web-sys` API (`doc.create_element("div")`); no raw HTML string is built in the helpers.

## What Was Examined and Found Clean

- **HTML Injection in ssr.rs** — Checked `escape_html` (L69-L82) and all string-building paths in `render_node` (L89-L122) at `75c1eef`. All five injection-risky characters are escaped for both text-content and attribute-value contexts. Tag and attribute names are developer-controlled static values, not user-submitted data. Escaping tests at the same commit would fail if coverage were removed.

- **DOM Spoofing in app.rs** — Checked the `has_child_nodes()` branch in `start()` (L154-L161) at `75c1eef`. Attack preconditions (pre-WASM DOM manipulation) require either XSS (which already grants full DOM control) or server-side HTML injection (analyzed in the HTML Injection concern). Neither constitutes a new attack vector through this gate. Threat is not realistic for a WASM library crate distributed under the browser's Same-Origin Policy.

- **Test Injection Safety in hydrate_wasm.rs** — Checked all `set_inner_html` calls (L62, L113, L174), dynamic DOM text paths (L110, L123, L129), and `#[wasm_bindgen_test]` entry points (L57-L58, L105-L106, L169-L170) at `75c1eef`. All `set_inner_html` calls use hardcoded literals. The only non-literal DOM value is a typed `i32` initialized to a constant. No `#[wasm_bindgen]` export provides an external callable surface. The file is confined to WASM browser test execution.
