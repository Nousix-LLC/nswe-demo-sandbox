# Regression Verdict — ferric-ssr-r4

**Scope**: commits `7fb90c7`, `e625c3f`, `75c1eef` on branch `work/ferric-ssr-r1`  
**Pinned commit**: `75c1eef`  
**Produced by**: SUBTASK_verdict_synthesis (synthesis of SUBTASK_reg_criteria + SUBTASK_sec_quality)

---

## Verdict

**PASS**

All 9 regression criteria hold at pinned commit `75c1eef`. All three security surfaces are clean. Two code quality findings are present at Note and Non-blocker severity; neither blocks the verdict.

---

## Requirements Covered

REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-005, REQ-HYD-001, REQ-HYD-002, REQ-HYD-004, REQ-MIS-001, REQ-MIS-002

---

## Evidence

**Criteria evidence** (from `SUBTASK_reg_criteria/criteria_findings.md`):

- **REQ-SSR-001**: `crates/ferric/src/ssr.rs` at `75c1eef` — only import is `use crate::vdom::VNode;` (line 20). No `web_sys` or `wasm_bindgen` import present or added by any ferric-ssr-r4 commit.
- **REQ-SSR-002**: `crates/ferric/src/signal.rs` at `75c1eef` — `impl Drop for ReactiveScope` at line 502 purges subscriptions. `ssr_handler` closure in `crates/chirp-server/src/ssr.rs` contains no `create_signal` calls.
- **REQ-SSR-003**: `crates/ferric/src/ssr.rs` at `75c1eef` — `render_node` recurses via `for child in &el.children { render_node(child, out); }` with no depth counter or recursion guard.
- **REQ-SSR-005**: `crates/ferric/src/lib.rs` at `75c1eef` — `pub use crate::ssr::render_to_string;` present (unconditional). `ssr_handler` calls `ferric::render_to_string(...)` via the crate-root path.
- **REQ-HYD-001**: `crates/ferric/src/hydrate.rs` at `75c1eef` — `adopt_vnode` checks tag equality on match; calls `set_events` and `adopt_children` without `create_node` on the matching path.
- **REQ-HYD-002**: `crates/ferric/src/hydrate.rs` at `75c1eef` — `hydrate` wraps updates in `create_effect → diff → apply_patches_impl`. `crates/chirp-frontend/src/app.rs` `start()` calls `ferric::hydrate(root, app)` on the SSR path without introducing an alternative reactive update path.
- **REQ-HYD-004**: `crates/ferric/src/hydrate.rs` at `75c1eef` — `use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER};` is the sole source. No local copies in `hydrate.rs` or `hydrate_wasm.rs`.
- **REQ-MIS-001**: `crates/chirp-server/src/ssr.rs` at `75c1eef` — `assemble_document` uses a valid HTML5 `format!()` template; `{server_html}` slot receives `escape_html`-processed output. `7fb90c7` touches doc comments only; no new string interpolation introduced.
- **REQ-MIS-002**: `crates/ferric/src/hydrate.rs` at `75c1eef` — element-tag mismatch uses `replace_child`; text-content mismatch uses `set_data`; type mismatch uses `replace_child`. All three operate on the target node only without corrupting siblings or ancestors.

**Security evidence** (from `SUBTASK_sec_quality/sec_quality_findings.md`):

- **HTML Injection in ssr.rs**: `crates/ferric/src/ssr.rs:L69-L122` at `75c1eef` — `escape_html` covers all five injection-risky characters (`<>&"'`) for both text-content and attribute-value contexts. Tag and attribute names are developer-controlled static values. Escaping tests at the same commit would fail if coverage were removed.
- **DOM Spoofing in app.rs**: `crates/chirp-frontend/src/app.rs:L154-L161` at `75c1eef` — attack preconditions require prior XSS or server-side HTML injection; neither constitutes a new vector through `has_child_nodes()`. Threat is not realistic for a WASM library crate under the browser's Same-Origin Policy.
- **Test Injection Safety in hydrate_wasm.rs**: `crates/ferric/tests/hydrate_wasm.rs` at `75c1eef` — all `set_inner_html` calls use hardcoded literals. The only non-literal DOM value is a typed `i32` initialized to a constant. No `#[wasm_bindgen]` export provides an external callable surface.

---

## Findings

### Finding 1

- **Severity**: Note
- **Requirement**: REQ-HYD-002 (hydrate dispatch correctness)
- **Location**: `crates/chirp-frontend/src/app.rs:154` at `75c1eef`
- **Principle**: Predicate should match the documented invariant it enforces
- **Why it matters**: `Element::has_child_nodes()` returns `true` for any child node — element, text node (including whitespace `"\n"` from template indentation), or comment — not only for element nodes produced by SSR markup. The comment at lines 149–152 describes the else branch as firing "when there is no server-rendered content in the root," but the actual predicate is weaker: it fires when there are no child nodes of any kind. If the HTML template has `<div id="app">\n</div>` or a placeholder comment in `#app`, `has_child_nodes()` returns `true` on a root containing no SSR markup, and the wasm32 path calls `ferric::hydrate` with that root. Per the behavior described in issue #240, `ferric::hydrate` encountering a mismatch warns but does not remove nodes; invoking it on a whitespace-only root triggers the mismatch path rather than falling through to `mount`. The comment's characterization of the invariant is imprecise relative to what the predicate actually checks.
- **Resolution**: Either tighten the predicate to `root.first_element_child().is_some()` — which returns `true` only for element-node children, the kind SSR markup always produces — or add an explicit invariant comment stating that `#app` must contain no child nodes at all (no whitespace, no comments) when SSR is not in use, so the assumption the predicate relies on is documented at the call site.

### Finding 2

- **Severity**: Non-blocker
- **Requirement**: REQ-MIS-002 (mismatch detection + recovery)
- **Location**: `crates/ferric/tests/hydrate_wasm.rs:185–189` at `75c1eef`
- **Principle**: Test assertions should check behavioral output, not only structural form
- **Why it matters**: `hydrate_mismatch_detection_recovery` asserts `el.tag_name().to_lowercase() == "p"` after recovery. The component's view returns `VNode::Element(VElement::new("p").child(VNode::Text("text".into())))`, so the recovered DOM should be `<p>text</p>`. The tag assertion does not check `text_content()`. A regression that replaces `<div>text</div>` with an empty `<p>` — rendering the element but failing to append the `VNode::Text` child during the recovery render — would leave this assertion passing while content fidelity after mismatch recovery is broken.
- **Resolution**: Add `assert_eq!(el.text_content().as_deref(), Some("text"), "REQ-SSR-006: recovered <p> missing text content")` immediately after the `tag_name` assertion. This asserts the full client-rendered output, not only the structural fix.

---

## What Was Examined and Found Clean

### Regression Criteria

- REQ-SSR-001: `crates/ferric/src/ssr.rs` import list at `75c1eef` → clean (no web_sys or wasm_bindgen)
- REQ-SSR-002: `crates/ferric/src/signal.rs` `impl Drop for ReactiveScope` at `75c1eef` → clean; `crates/chirp-server/src/ssr.rs` `ssr_handler` closure contents → clean (no create_signal calls)
- REQ-SSR-003: `crates/ferric/src/ssr.rs` `render_node` recursion path at `75c1eef` → clean (no depth limiter)
- REQ-SSR-005: `crates/ferric/src/lib.rs` re-export at `75c1eef` → clean; `crates/chirp-server/src/ssr.rs` call site → clean; `crates/chirp-server/src/api/router.rs` route registration → clean
- REQ-HYD-001: `crates/ferric/src/hydrate.rs` `adopt_vnode` match path at `75c1eef` → clean (no createElement on match)
- REQ-HYD-002: `crates/ferric/src/hydrate.rs` `hydrate` effect body at `75c1eef` → clean; `crates/chirp-frontend/src/app.rs` `start()` hydrate dispatch → clean
- REQ-HYD-004: `crates/ferric/src/hydrate.rs` marker imports at `75c1eef` → clean (single import from ssr); `crates/ferric/tests/hydrate_wasm.rs` → clean (no local marker definitions)
- REQ-MIS-001: `crates/chirp-server/src/ssr.rs` `assemble_document` format string at `75c1eef` → clean (valid HTML5 template, escaping intact); ferric `ssr.rs` docstring-fix scope → clean (doc only)
- REQ-MIS-002: `crates/ferric/src/hydrate.rs` mismatch recovery paths at `75c1eef` → clean (node-scoped replacement, no structural corruption)

### Security Surface

- HTML Injection in ssr.rs — `escape_html` covers all five injection-risky characters for text-content and attribute-value contexts; tag and attribute names are developer-controlled static values; escaping tests would fail if coverage were removed → clean
- DOM Spoofing in app.rs — attack preconditions (XSS or server-side HTML injection) constitute a pre-existing vulnerability that already grants capabilities exceeding this branch; no new attack vector through `has_child_nodes()`; WASM under Same-Origin Policy → clean
- Test Injection Safety in hydrate_wasm.rs — all `set_inner_html` calls use hardcoded literals; only non-literal DOM value is a typed `i32` constant; no `#[wasm_bindgen]` export provides external callable surface → clean

### Code Quality (app.rs)

- Branch logic readability: if/else structure is straightforward; two cfg blocks individually readable → clean
- Dead code: both branches reachable on wasm32; non-wasm32 excluded by cfg gate → clean
- cfg gate correctness: `#[cfg(target_arch = "wasm32")]` and `#[cfg(not(target_arch = "wasm32"))]` are complementary; no gap or overlap → clean
- Comment accuracy on cfg gate (lines 151–152): accurate description of cfg structure and purpose → clean
- Comment accuracy on mount root acquisition (line 139): accurately separates acquisition from dispatch logic → clean
- Fresh #229–#242 patterns in new app.rs code: 14 patterns checked against new lines from `7fb90c7` and `75c1eef`; none present → clean

### Code Quality (hydrate_wasm.rs)

- New test helpers — naming clarity: `document()`, `make_container()`, `cleanup()` are unambiguous; `make_container` doc comment states pairing contract with `cleanup` → clean
- New test helpers — non-redundancy: three helpers serve distinct, non-overlapping roles → clean
- Assertion specificity — `hydrate_adopt_walk_no_structural_mutations`: `is_same_node` assertions check node identity directly against before-hydration captures; a recreated node fails the assertion → clean
- Assertion specificity — `hydrate_event_wiring_post_hydration`: `text_content() == Some("1")` verifies event wiring and reactive re-render; `is_same_node` verifies patch preserved element identity; a broken wiring or replace-instead-of-patch strategy each fail a different assertion → clean
- Copy-paste patterns: shared scaffold already extracted into two helpers; assertion bodies are substantively different across the three tests → clean
- Fresh #229–#242 patterns in new hydrate_wasm.rs code: all 14 patterns reviewed; no fresh instances → clean
