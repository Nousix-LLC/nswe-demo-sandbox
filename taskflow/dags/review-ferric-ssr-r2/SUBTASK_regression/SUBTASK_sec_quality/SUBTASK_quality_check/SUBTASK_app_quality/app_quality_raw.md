# app_quality_raw.md — App.rs Code Quality Analysis

Scope: ferric-ssr-r4 commits `7fb90c7`, `e625c3f`, `75c1eef`. New app.rs code only.
Pinned commit: `75c1eef`.

---

## App.rs Code Quality Findings

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

---

## App.rs Fresh Non-blockers

No fresh non-blockers found in app.rs new code.

Patterns from #229–#242 target ferric internals (stale todo-panic comments in ssr.rs, naming
collision in lib.rs, cfg gates on pub mod dom, silent remove_child in hydrate.rs, HTML escaping in
assemble_document, helper duplication in hydrate.rs/dom.rs, hydrate() calling contract doc,
TEXT_OPEN/CLOSE_MARKER stability notes, SSR isolation assertions, mismatch node removal, attribute
escaping in render_node, injection test through assemble_document) or chirp-server rename (#231).
None of those patterns are present in the 15 new lines added to app.rs by commits 7fb90c7 and
75c1eef. Commit e625c3f added no app.rs changes.

---

## App.rs What Was Examined and Found Clean

- **Branch logic readability** — clean: the if/else structure is straightforward (`has_child_nodes()`
  → hydrate, else → mount), and the two cfg blocks are individually readable. No readability issues.

- **Dead code** — clean: on wasm32 both the hydrate and mount branches of the if/else are reachable
  (depending on the SSR state of the root). On non-wasm32 the `#[cfg(target_arch = "wasm32")]` gate
  excludes the entire if/else from compilation, and `#[cfg(not(target_arch = "wasm32"))]` includes
  the fallback `mount` call. No branch is unreachable on the target where it compiles.

- **cfg gate correctness** — clean: `#[cfg(target_arch = "wasm32")]` on the if/else block and
  `#[cfg(not(target_arch = "wasm32"))]` on the fallback `mount(root, app)` are complementary and
  together cover all targets without gap or overlap. The arrangement correctly isolates the
  `ferric::hydrate` call (wasm32-only API) from non-wasm32 compilation paths.

- **Comment accuracy on the cfg gate** (lines 151–152) — clean: "`ferric::hydrate` is wasm32-only;
  the cfg gate keeps non-wasm (native test / clippy) compilation clean while preserving the runtime
  conditional on the wasm32 target." Accurate description of the cfg structure and its purpose.

- **Comment accuracy on mount root acquisition** (line 139) — clean: "Acquire the mount root: `#app`
  if the page provides it, otherwise `<body>`." The change from "Mount into `#app`..." accurately
  separates the acquisition step from the dispatch logic below it.

- **Fresh #229–#242 patterns in new app.rs code** — clean: checked every new line from commits
  7fb90c7 and 75c1eef against each of the 14 filed patterns. None appear in the new app.rs code.
  (See Fresh Non-blockers section above for per-pattern rationale.)
