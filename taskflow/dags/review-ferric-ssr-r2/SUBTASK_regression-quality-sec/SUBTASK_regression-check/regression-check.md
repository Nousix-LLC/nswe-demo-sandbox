# Regression Check — 10 Previously-Clean Criteria

## Summary

All 10 criteria pass. The ferric-ssr-r4 commits (`7fb90c7`, `e625c3f`, `75c1eef`) changed
`chirp-frontend/src/app.rs` (hydrate/mount conditional), added
`crates/ferric/tests/hydrate_wasm.rs` (new test file), applied a cfg wasm32 gate to
`crates/ferric/src/lib.rs`, and reformatted `crates/ferric/src/hydrate.rs` (no logic changes).
They did not modify `crates/ferric/src/ssr.rs` or `crates/chirp-server/src/ssr.rs`.

Criteria whose implementation code was not touched carry "unchanged" status. The five focus-area
criteria were examined at source-file depth.

---

## Per-Criterion Findings

### REQ-SSR-001 — PASS

**Criterion**: `render_to_string` has no `web_sys`/DOM dependency; compiles on native.

Touched by ferric-ssr-r4: `lib.rs` (commit `75c1eef`).

Commit `75c1eef` added `#[cfg(target_arch = "wasm32")]` gates on `pub mod hydrate` and
`pub use crate::hydrate::hydrate` in `lib.rs`. This is directly relevant: the `hydrate` module
imports `web_sys`; gating it means non-wasm builds exclude it and compile cleanly.

`ssr.rs` itself was not changed. At branch HEAD the only import in `ssr.rs` is
`use crate::vdom::VNode;` — no `web_sys`, no `wasm_bindgen`. The module doc states the
constraint explicitly: "it must never reference `web_sys` or `wasm_bindgen`." The cfg gate
added by `75c1eef` strengthens this: the hydrate module's DOM dependencies are excluded from
native builds.

**What was checked**: `crates/ferric/src/lib.rs` and `crates/ferric/src/ssr.rs` at HEAD commit
`75c1eef`. No `web_sys` or `wasm_bindgen` import in `ssr.rs`. Cfg gate on hydrate module present
in `lib.rs`.

### REQ-SSR-002 — PASS (unchanged)

**Criterion**: Reactive scope isolated during SSR; `impl Drop for ReactiveScope` purges subscribers.

`ssr.rs` was not changed by the ferric-ssr-r4 commits. The implementation at HEAD:
`render_to_string` creates `crate::signal::ReactiveScope::new()`, executes the closure via
`scope.run(f)`, and drops `scope` at function exit (reverse declaration order: `vnode` drops,
then `scope`, disposing all reactive nodes before the caller resumes). The comment in the
source spells this out explicitly.

No new code touched this area.

### REQ-SSR-003 — PASS (unchanged)

**Criterion**: Nested VNode recursion in SSR is unbounded (no artificial cap).

`ssr.rs` not changed by ferric-ssr-r4. `render_node` in `ssr.rs` recurses via
`for child in &el.children { render_node(child, out); }` — no depth counter, no limit.
Tests `renders_nested_children_at_correct_depth` and `renders_deeply_nested_structure` cover
multi-level nesting, both present in `ssr.rs` at HEAD.

No new code touched this area.

### REQ-SSR-004 — PASS

**Criterion**: SSR/hydration markers defined once in `ssr.rs`, imported (not copied) by `hydrate.rs`.

**Focus area**: Did any ferric-ssr-r4 commit copy the marker constants rather than importing them?
Specifically, does `hydrate_wasm.rs` reference markers by literal or import?

`hydrate_wasm.rs` (new file, commit `e625c3f`): imports are `ferric::signal::create_signal`,
`ferric::vdom::VElement`, `ferric::{EventKind, VNode}`. No import of `TEXT_OPEN_MARKER` or
`TEXT_CLOSE_MARKER`. No inline string `"<!--$t-->"` or `"<!--/$t-->"` anywhere in the file
(confirmed by grep). The three tests work at the element level — `set_inner_html` with plain
element trees — and do not touch text boundary markers.

`hydrate.rs` (reformatted by `75c1eef`, no logic change): `use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER};` — single import. `is_sentinel_comment` strips the HTML comment delimiters
from the imported constants at runtime (`TEXT_OPEN_MARKER.strip_prefix("<!--").and_then(...)`);
the stripped data strings `"$t"` and `"/$t"` are never hardcoded.

`ssr.rs`: `pub const TEXT_OPEN_MARKER: &str = "<!--$t-->";` and
`pub const TEXT_CLOSE_MARKER: &str = "<!--/$t-->";` — the single definition point.

No copies introduced by the new commits.

**What was checked**: `crates/ferric/src/hydrate.rs`, `crates/ferric/tests/hydrate_wasm.rs`,
`crates/ferric/src/ssr.rs` at HEAD.

### REQ-SSR-005 — PASS

**Criterion**: `render_to_string` is a crate-root export; `chirp-server` can call it.

**Focus area**: Did `lib.rs` change? Is `render_to_string` still exported?

`lib.rs` was changed by commit `75c1eef` to add cfg gates on the `hydrate` module. The
`render_to_string` export is unaffected: `pub use crate::ssr::render_to_string;` is unconditional
(no cfg gate) in `lib.rs` at HEAD. `pub mod ssr;` is also unconditional.

`crates/chirp-server/Cargo.toml` has `ferric = { path = "../ferric" }` (native). `chirp-server/src/ssr.rs` calls `ferric::render_to_string(...)`. The export chain is intact.

**What was checked**: `crates/ferric/src/lib.rs` and `crates/chirp-server/src/ssr.rs` at HEAD.

### REQ-HYD-001 — PASS

**Criterion**: Adopt pass reuses existing DOM nodes — no `createElement` calls on matching paths.

**Focus area**: Did new code change the adopt pass in `hydrate.rs`?

Commit `7fb90c7` changed `app.rs` to call `ferric::hydrate(root, app)` when the mount root has
server-rendered children, and `mount(root, app)` otherwise. This wires the entry point but does
not change the adopt pass implementation in `hydrate.rs`.

Commit `75c1eef` reformatted `hydrate.rs` (rustfmt). No logic changes.

The adopt pass at HEAD: in `adopt_vnode`, the tag-match branch calls `set_events(el, &ve.events)`
and recurses via `adopt_children(...)`. Neither branch creates an element. `create_element` is
called only inside `create_node`, which is reachable only from explicit mismatch recovery paths
(`adopt_root_vnode` when root is empty, `adopt_vnode` on tag mismatch, `adopt_children` for
VNode children with no corresponding DOM node).

Test `hydrate_adopt_walk_no_structural_mutations` in `hydrate_wasm.rs` injects
`<div><span>hello</span></div>`, captures node references before hydration, hydrates with a
structurally identical component, and asserts `before_div.is_same_node(Some(&after_div))` and
`before_span.is_same_node(Some(&after_span))`. This test would fail on any `create_element` call
on a matching path.

**What was checked**: `crates/ferric/src/hydrate.rs` adopt pass logic at HEAD; `app.rs` new
conditional; `hydrate_wasm.rs` node-identity test.

### REQ-HYD-002 — PASS (unchanged)

**Criterion**: Reactive updates after hydration use `create_effect → diff → apply_patches_impl`.

`hydrate.rs` logic was not changed by ferric-ssr-r4 (only reformatted). The `create_effect`
closure in `hydrate` maintains a `None`/`Some(prev)` state: the first run executes the adopt pass;
every subsequent run calls `diff(&prev, &next)` then `apply_patches_impl(&document, &root, &patches)`.
Chain: `create_effect → diff → apply_patches_impl`, exactly as the criterion states.

No new code touched this area's logic.

### REQ-HYD-004 — PASS

**Criterion**: Marker format enforced at type level — single import, no local copies.

**Focus area**: Did any new code add a local copy of the marker type?

Commit `e625c3f` added `hydrate_wasm.rs`. The file has no import of `TEXT_OPEN_MARKER`,
`TEXT_CLOSE_MARKER`, or any marker-adjacent constant (confirmed by grep). No inline literal
`"<!--$t-->"` or `"<!--/$t-->"` in the file.

`hydrate.rs` (reformatted, not changed): one import, `use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER};`. No local definition.

No new copies introduced.

**What was checked**: `crates/ferric/tests/hydrate_wasm.rs` at HEAD (grep for MARKER and marker
literal strings); `crates/ferric/src/hydrate.rs` import block.

### REQ-MIS-001 — PASS (unchanged)

**Criterion**: `assemble_document` produces valid HTML5 document fragment.

`crates/chirp-server/src/ssr.rs` was not changed by the ferric-ssr-r4 commits. `assemble_document`
was verified clean in review-ferric-ssr-r1; no new code touches it.

### REQ-MIS-002 — PASS

**Criterion**: Mismatch detection+recovery replaces mismatched DOM nodes without structural corruption.

**Focus area**: Did mismatch handling change?

`hydrate.rs` logic not changed by ferric-ssr-r4 (reformatted only). The mismatch recovery paths at
HEAD:

- Element tag mismatch (`adopt_vnode`): `parent.replace_child(&create_node(document, vnode), dom_node)` — the mismatched node is replaced with a fully client-rendered subtree; the parent's other children are unaffected.
- Text content mismatch: `t.set_data(text)` — corrected in-place, no structural mutation.
- Node type mismatch (expected Text, found other): `parent.replace_child(&document.create_text_node(text), dom_node)` — point replacement.
- Extra DOM nodes beyond the VNode child list: warning emitted, loop breaks; nothing removed.

`strip_sentinels` removes only Comment nodes whose `.data()` matches the two sentinel constants; it does not remove structural nodes.

Commit `e625c3f` added `hydrate_mismatch_detection_recovery` in `hydrate_wasm.rs`: injects
`<div>text</div>` as server HTML, hydrates with a component returning `VNode::Element(VElement::new("p")...)`, then asserts `el.tag_name().to_lowercase() == "p"`. This confirms the `<div>` was replaced and the container holds a valid `<p>` element after recovery.

**What was checked**: `crates/ferric/src/hydrate.rs` mismatch paths at HEAD; `hydrate_wasm.rs`
`hydrate_mismatch_detection_recovery` test.

---

## Overall Regression Verdict: PASS

All 10 previously-clean criteria remain satisfied after the ferric-ssr-r4 commits. The commits
added the hydrate entry point in `app.rs`, the cfg wasm32 gate in `lib.rs`, and the
`hydrate_wasm.rs` test file. None of these introduced marker copies, changed the adopt pass logic,
modified the reactive update path, or altered `assemble_document` or mismatch recovery. The
formatting-only change to `hydrate.rs` does not affect any criterion.
