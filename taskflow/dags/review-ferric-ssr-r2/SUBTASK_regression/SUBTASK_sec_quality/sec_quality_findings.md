# sec_quality_findings.md — Security and Code Quality Findings for ferric-ssr-r4

Scope: ferric-ssr-r4 commits `7fb90c7`, `e625c3f`, `75c1eef`. Pinned commit: `75c1eef`.

---

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

---

## Code Quality Findings

- **Severity**: Note
- **Location**: `crates/chirp-frontend/src/app.rs:154` (at pinned commit `75c1eef`)
- **Description**: `Element::has_child_nodes()` returns `true` for any child node — element, text
  (including whitespace `"\n"` from template indentation), or comment — not only for element nodes
  produced by SSR markup. The comment at lines 149–152 describes the else branch as firing "when
  there is no server-rendered content in the root," but the actual predicate is weaker: it fires
  when there are no child nodes at all. If the HTML template has `<div id="app">\n</div>` or a
  placeholder comment in `#app`, `has_child_nodes()` returns `true` on a root that contains no SSR
  markup, and the wasm32 path calls `ferric::hydrate` with that root. Per the behavior described in
  issue #240, `ferric::hydrate` encountering a mismatch warns but does not remove nodes; invoking it
  on a whitespace-only root triggers that mismatch path rather than falling through to `mount`. The
  comment's characterization of the invariant is imprecise relative to what the predicate actually
  checks.
- **Resolution**: Either tighten the predicate to `root.first_element_child().is_some()` — which
  returns `true` only for element-node children, the kind SSR markup always produces — or add an
  explicit invariant comment stating that `#app` must contain no child nodes at all (no whitespace,
  no comments) when SSR is not in use, so the assumption the predicate relies on is documented at
  the call site.

- **Severity**: Non-blocker
- **Location**: `crates/ferric/tests/hydrate_wasm.rs:185–189` (at pinned commit `75c1eef`)
- **Description**: `hydrate_mismatch_detection_recovery` asserts that
  `el.tag_name().to_lowercase() == "p"` after recovery. The component's view returns
  `VNode::Element(VElement::new("p").child(VNode::Text("text".into())))`, so the recovered DOM
  should be `<p>text</p>`. The tag assertion does not check `text_content()`. A regression that
  replaces `<div>text</div>` with an empty `<p>` — rendering the element but failing to append the
  `VNode::Text` child during the recovery render — leaves this assertion passing while content
  fidelity after mismatch recovery is broken.
- **Resolution**: Add `assert_eq!(el.text_content().as_deref(), Some("text"), "REQ-SSR-006:
  recovered <p> missing text content")` immediately after the `tag_name` assertion. This asserts
  the full client-rendered output, not only the structural fix.

---

## What Was Examined and Found Clean

### Security Surface

- **HTML Injection in ssr.rs** — Checked `escape_html` (L69-L82) and all string-building paths in `render_node` (L89-L122) at `75c1eef`. All five injection-risky characters are escaped for both text-content and attribute-value contexts. Tag and attribute names are developer-controlled static values, not user-submitted data. Escaping tests at the same commit would fail if coverage were removed.

- **DOM Spoofing in app.rs** — Checked the `has_child_nodes()` branch in `start()` (L154-L161) at `75c1eef`. Attack preconditions (pre-WASM DOM manipulation) require either XSS (which already grants full DOM control) or server-side HTML injection (analyzed in the HTML Injection concern). Neither constitutes a new attack vector through this gate. Threat is not realistic for a WASM library crate distributed under the browser's Same-Origin Policy.

- **Test Injection Safety in hydrate_wasm.rs** — Checked all `set_inner_html` calls (L62, L113, L174), dynamic DOM text paths (L110, L123, L129), and `#[wasm_bindgen_test]` entry points (L57-L58, L105-L106, L169-L170) at `75c1eef`. All `set_inner_html` calls use hardcoded literals. The only non-literal DOM value is a typed `i32` initialized to a constant. No `#[wasm_bindgen]` export provides an external callable surface. The file is confined to WASM browser test execution.

### Code Quality

- **app.rs: Branch logic readability** — clean: the if/else structure is straightforward (`has_child_nodes()` → hydrate, else → mount), and the two cfg blocks are individually readable. No readability issues.

- **app.rs: Dead code** — clean: on wasm32 both the hydrate and mount branches of the if/else are reachable (depending on the SSR state of the root). On non-wasm32 the `#[cfg(target_arch = "wasm32")]` gate excludes the entire if/else from compilation, and `#[cfg(not(target_arch = "wasm32"))]` includes the fallback `mount` call. No branch is unreachable on the target where it compiles.

- **app.rs: cfg gate correctness** — clean: `#[cfg(target_arch = "wasm32")]` on the if/else block and `#[cfg(not(target_arch = "wasm32"))]` on the fallback `mount(root, app)` are complementary and together cover all targets without gap or overlap. The arrangement correctly isolates the `ferric::hydrate` call (wasm32-only API) from non-wasm32 compilation paths.

- **app.rs: Comment accuracy on the cfg gate** (lines 151–152) — clean: "`ferric::hydrate` is wasm32-only; the cfg gate keeps non-wasm (native test / clippy) compilation clean while preserving the runtime conditional on the wasm32 target." Accurate description of the cfg structure and its purpose.

- **app.rs: Comment accuracy on mount root acquisition** (line 139) — clean: "Acquire the mount root: `#app` if the page provides it, otherwise `<body>`." The change from "Mount into `#app`..." accurately separates the acquisition step from the dispatch logic below it.

- **app.rs: Fresh #229–#242 patterns in new app.rs code** — clean: checked every new line from commits `7fb90c7` and `75c1eef` against each of the 14 filed patterns. None appear in the new app.rs code.

- **hydrate_wasm.rs: New test helpers — naming clarity** — clean: `document()`, `make_container()`, and `cleanup()` are unambiguous. `make_container` carries a doc comment that states the pairing contract with `cleanup`. No abbreviations.

- **hydrate_wasm.rs: New test helpers — non-redundancy** — clean: the three helpers serve distinct, non-overlapping roles: document accessor, container factory, and cleanup. No two helpers duplicate behavior.

- **hydrate_wasm.rs: Assertion specificity — `hydrate_adopt_walk_no_structural_mutations`** — clean: both `is_same_node` assertions check node identity directly against the before-hydration captures. If `hydrate` recreated a node rather than adopting it, `is_same_node` returns `false` and the assertion fails. The error message in each assertion names the criterion (REQ-SSR-004).

- **hydrate_wasm.rs: Assertion specificity — `hydrate_event_wiring_post_hydration`** — clean: `after_button.text_content().as_deref() == Some("1")` verifies that the click handler was wired and the reactive re-render applied. `before_button.is_same_node(Some(&after_button))` verifies that the patch preserved element identity rather than replacing it. A broken event wiring or a replace-instead-of-patch strategy each fail a different one of these two assertions.

- **hydrate_wasm.rs: Copy-paste patterns** — clean: all three tests share the scaffold (`make_container` / `set_inner_html` / `ferric::hydrate` / assertions / `cleanup`). The reusable pieces are already extracted into the two helpers. The assertion bodies are substantively different across the three tests and reflect distinct behavioral properties. No parameterization opportunity survives inspection.

- **hydrate_wasm.rs: Fresh #229–#242 patterns in new hydrate_wasm.rs code** — clean: all 14 patterns reviewed against the new file. No fresh instances found.
