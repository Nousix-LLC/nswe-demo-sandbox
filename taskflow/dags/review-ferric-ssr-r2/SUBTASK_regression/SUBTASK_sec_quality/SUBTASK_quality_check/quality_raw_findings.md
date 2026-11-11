# quality_raw_findings.md — Code Quality Findings for ferric-ssr-r4

Scope: ferric-ssr-r4 commits `7fb90c7`, `e625c3f`, `75c1eef`. New code in app.rs and hydrate_wasm.rs only.
Pinned commit: `75c1eef`.

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

- **app.rs: Branch logic readability** — clean: the if/else structure is straightforward
  (`has_child_nodes()` → hydrate, else → mount), and the two cfg blocks are individually readable.
  No readability issues.

- **app.rs: Dead code** — clean: on wasm32 both the hydrate and mount branches of the if/else are
  reachable (depending on the SSR state of the root). On non-wasm32 the
  `#[cfg(target_arch = "wasm32")]` gate excludes the entire if/else from compilation, and
  `#[cfg(not(target_arch = "wasm32"))]` includes the fallback `mount` call. No branch is
  unreachable on the target where it compiles.

- **app.rs: cfg gate correctness** — clean: `#[cfg(target_arch = "wasm32")]` on the if/else block
  and `#[cfg(not(target_arch = "wasm32"))]` on the fallback `mount(root, app)` are complementary
  and together cover all targets without gap or overlap. The arrangement correctly isolates the
  `ferric::hydrate` call (wasm32-only API) from non-wasm32 compilation paths.

- **app.rs: Comment accuracy on the cfg gate** (lines 151–152) — clean: "`ferric::hydrate` is
  wasm32-only; the cfg gate keeps non-wasm (native test / clippy) compilation clean while
  preserving the runtime conditional on the wasm32 target." Accurate description of the cfg
  structure and its purpose.

- **app.rs: Comment accuracy on mount root acquisition** (line 139) — clean: "Acquire the mount
  root: `#app` if the page provides it, otherwise `<body>`." The change from "Mount into `#app`..."
  accurately separates the acquisition step from the dispatch logic below it.

- **app.rs: Fresh #229–#242 patterns in new app.rs code** — clean: checked every new line from
  commits `7fb90c7` and `75c1eef` against each of the 14 filed patterns. None appear in the new
  app.rs code.

- **hydrate_wasm.rs: New test helpers — naming clarity** — clean: `document()`,
  `make_container()`, and `cleanup()` are unambiguous. `make_container` carries a doc comment that
  states the pairing contract with `cleanup`. No abbreviations.

- **hydrate_wasm.rs: New test helpers — non-redundancy** — clean: the three helpers serve
  distinct, non-overlapping roles: document accessor, container factory, and cleanup. No two
  helpers duplicate behavior.

- **hydrate_wasm.rs: Assertion specificity — `hydrate_adopt_walk_no_structural_mutations`** —
  clean: both `is_same_node` assertions check node identity directly against the before-hydration
  captures. If `hydrate` recreated a node rather than adopting it, `is_same_node` returns `false`
  and the assertion fails. The error message in each assertion names the criterion (REQ-SSR-004).

- **hydrate_wasm.rs: Assertion specificity — `hydrate_event_wiring_post_hydration`** — clean:
  `after_button.text_content().as_deref() == Some("1")` verifies that the click handler was wired
  and the reactive re-render applied. `before_button.is_same_node(Some(&after_button))` verifies
  that the patch preserved element identity rather than replacing it. A broken event wiring or a
  replace-instead-of-patch strategy each fail a different one of these two assertions.

- **hydrate_wasm.rs: Copy-paste patterns** — clean: all three tests share the scaffold
  (`make_container` / `set_inner_html` / `ferric::hydrate` / assertions / `cleanup`). The reusable
  pieces are already extracted into the two helpers. The assertion bodies are substantively
  different across the three tests and reflect distinct behavioral properties. No parameterization
  opportunity survives inspection.

- **hydrate_wasm.rs: Fresh #229–#242 patterns in new hydrate_wasm.rs code** — clean: all 14
  patterns reviewed against the new file. No fresh instances found.
