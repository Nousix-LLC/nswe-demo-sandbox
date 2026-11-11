# Mismatch Detection Findings (REQ-SSR-006 / REQ-SSR-009)

> **Requirement ID note**: The brief labels this criterion "REQ-SSR-006"; issue #226 and the
> PR's own code comments label it "REQ-SSR-009" (e.g., `hydrate.rs` line 11: "emit a
> `console.warn` (debug builds only, REQ-SSR-009)"). Both refer to the same mismatch-detection
> acceptance criterion. This document uses REQ-SSR-009 as the authoritative label (matches the
> issue and the code) and notes the divergence so the synthesis step can flag it.

---

## REQ-SSR-009 — Mismatch detection: detection fires on structural mismatch

**Status**: CLEAN

**What was checked**: The `adopt_vnode` and `adopt_children` functions in
`crates/ferric/src/hydrate.rs` cover every structural divergence the acceptance criterion
names. Trigger conditions verified:

- **Wrong element tag**: `adopt_vnode` → `VNode::Element` branch; `dom_node.dyn_ref::<Element>()`
  returns an element whose `tag_name()` does not case-insensitively equal `ve.tag` → fires mismatch.
  (`hydrate.rs:93–109`)
- **Non-element where element expected**: same branch, `dyn_ref` returns `None` → fires mismatch.
- **Text content mismatch**: `adopt_vnode` → `VNode::Text` branch; `dyn_ref::<Text>()` succeeds but
  `t.data() != *text` → fires mismatch. (`hydrate.rs:112–125`)
- **Non-text where text expected**: `dyn_ref::<Text>()` returns `None` → fires mismatch.
  (`hydrate.rs:126–134`)
- **Empty root DOM**: `adopt_root_vnode` finds `first_child()` is `None` → fires mismatch.
  (`hydrate.rs:72–80`)
- **VNode children with no DOM counterpart**: `adopt_children` outer loop exhausts non-sentinel DOM
  nodes before exhausting `vnode_children`; inner recovery loop fires mismatch per missing child.
  (`hydrate.rs:170–181`)
- **Extra DOM nodes beyond VNode list**: `adopt_children` detects `vnode_idx >=
  vnode_children.len()` while DOM nodes remain → fires mismatch. (`hydrate.rs:154–163`)

**Evidence**: `crates/ferric/src/hydrate.rs:72–181`

**Finding**: None. Detection is comprehensive across the conditions named in the criterion.

---

## REQ-SSR-009 — Mismatch detection: warning not panic

**Status**: CLEAN

**What was checked**: `emit_mismatch_warning` and all call sites.

`#[cfg(debug_assertions)]`: calls `web_sys::console::warn_1` with a formatted string that
includes the VNode path (as a `[idx, idx, …]` sequence), the expected label, and the found
label. (`hydrate.rs:188–200`)

`#[cfg(not(debug_assertions))]`: empty no-op, `#[inline]`. (`hydrate.rs:202–203`)

No `panic!`, `unwrap()`, or `expect()` appears on the detection path. The `.expect()` calls
present in `adopt_vnode` and `adopt_children` are on the DOM mutation operations that execute
*after* the warn, in the recovery path (e.g., `replace_child`, `append_child`). Those DOM
operations would need to fail — which does not happen under normal browser conditions — to
reach a panic.

The debug-only gate is consistent with issue #226's criterion ("emit actionable diagnostic in
dev build"). The diagnostic message includes path and expected-vs-found divergence, satisfying
the "actionable" requirement.

**Evidence**: `crates/ferric/src/hydrate.rs:188–203`, call sites at lines 78, 103, 119,
130, 158, 175

**Finding**: None. The warn path is correct; no panic on detection.

---

## REQ-SSR-009 — Mismatch detection: recovery by fresh mount

**Status**: FINDING (NON-BLOCKER)

**What was checked**: Recovery operations in `adopt_root_vnode`, `adopt_vnode`, and
`adopt_children`; the `create_node` helper; and the `strip_sentinels` / subsequent
diff-patch path.

**What is clean**:

- Element tag mismatch → `parent.replace_child(&new_node, dom_node)` where `new_node` is built
  by `create_node(document, vnode)`. `create_node` recursively constructs the full VNode
  subtree including attributes, children, and event handlers. This is a genuine fresh
  client-side mount of the diverged subtree. (`hydrate.rs:106–110`, `hydrate.rs:239–265`)
- Text content mismatch → `t.set_data(text)` corrects the text in-place. This is not a
  "subtree" replacement, but text nodes have no children; in-place correction is equivalent.
  (`hydrate.rs:118–121`)
- Wrong node type where text expected → `parent.replace_child(&new_text, dom_node)`.
  (`hydrate.rs:128–133`)
- Empty root → `root.append_child(&new_node)` with a full fresh render.
  (`hydrate.rs:78–80`)
- Missing VNode children → `parent_dom.append_child(&new_node)` per child.
  (`hydrate.rs:175–180`)

**Finding**: Extra DOM nodes beyond the VNode child list are warned about but **not removed**.
`adopt_children` calls `emit_mismatch_warning` and then `break`s. The comment at that site
reads "only warn, do not remove." (`hydrate.rs:154–163`)

This is a gap in recovery. After `strip_sentinels` runs, the diff/patch path resolves nodes by
`child_nodes().item(index)` where the index is derived from VNode path coordinates
(`resolve_impl`, `hydrate.rs:382–393`). Extra DOM nodes left at positions beyond the VNode
list do not shift the indices of positions *within* the VNode list (they lie past the end), so
they do not corrupt existing patch targets. However, the live DOM after hydration contains more
children than the VNode tree expects, violating the acceptance criterion's "live DOM matches
client render of subtree." A later diff/patch that inserts or removes children at the parent
could also interact unexpectedly with the unremoved nodes.

This is a **non-blocker**: the extra-nodes case is real but comparatively rare (server renders
more children than the component produces, which suggests a component-level bug rather than a
normal divergence scenario), and the primary mismatch cases (tag, text, type, missing) all
recover correctly. Flag it and address in a follow-up.

---

## REQ-SSR-009 — Mismatch detection: test coverage

**Status**: FINDING (BLOCKER)

**What was checked**: The full file tree of branch `work/ferric-ssr-r1` for
`crates/ferric/` test files; the content of `crates/ferric/src/hydrate.rs` for a
`#[cfg(test)]` inline test module.

**Evidence**:

- `crates/ferric/src/hydrate.rs`: 466 lines; no `#[cfg(test)]` block. Zero tests for the
  mismatch detection path, the recovery path, the sentinel-skip logic, or the
  `strip_sentinels` function.
- No `crates/ferric/tests/` directory exists in the branch. The only ferric test files are
  for `ferric-macros` (compile-fail and integration tests) — none cover `ferric/src/hydrate.rs`.
- `crates/ferric/src/ssr.rs` has an inline `#[cfg(test)]` module with 11 tests covering
  SSR render output, text markers, and reactive scope isolation — but nothing on the
  hydration or mismatch path.

**Finding (BLOCKER)**: Issue #226's REQ-SSR-009 acceptance criterion explicitly requires:

> A headless `wasm-bindgen-test` test: hydrates against deliberately mismatched server DOM;
> confirms diagnostic fires, live DOM matches client render of subtree, rest remains adopted.

No such test exists anywhere in the PR. The mismatch detection implementation ships with
zero behavioral test coverage. The acceptance criterion for the criterion is not met. This
is a blocker: CI passed on SSR unit tests and existing DOM/hydration paths, but the stated
requirement for a `wasm-bindgen-test` covering the mismatch code path is unmet.

What a satisfying test would look like: build a minimal server HTML string with a deliberate
structural divergence (e.g., the component returns `<p>` but the server DOM contains `<div>`);
inject it into the headless browser DOM under `#app`; call `ferric::hydrate(root, || ...)`;
assert that `console.warn` fired with a message containing the path and the expected/found
labels; assert that the live DOM under `#app` matches the client-rendered component output;
assert that siblings of the mismatched element are still adopted (unchanged, event handlers
wired). The test does not exist; it needs to be written and pass before this criterion is met.

---

## Marker Format Observed

**Client-side marker format**: Text-boundary sentinel Comment nodes; **not** DOM attributes.

The client recognizes two HTML comment markers imported from `crate::ssr`:

| Constant | Value | DOM `comment.data()` |
|---|---|---|
| `TEXT_OPEN_MARKER` | `"<!--$t-->"` | `"$t"` |
| `TEXT_CLOSE_MARKER` | `"<!--/$t-->"` | `"/$t"` |

**How detection works**: `is_sentinel_comment` checks `node.node_type() ==
web_sys::Node::COMMENT_NODE` and then `comment.data() ∈ {"$t", "/$t"}`. The data values are
derived at call time by stripping the `<!--` prefix and `-->` suffix from the constants.
(`hydrate.rs:214–237`)

**Purpose**: These are text-boundary markers, not element-identity markers. The server emits
`<!--$t-->text<!--/$t-->` around every `VNode::Text` child. The client's adopt walk skips
sentinel Comment nodes when advancing the VNode child index, so text boundaries do not inflate
the structural position count. After the adopt pass, `strip_sentinels` removes all sentinel
Comment nodes from the tree, aligning DOM child indices with VNode path indices for
subsequent diff/patch operations.

**No `data-hydration-id` attribute**: There is no attribute-based hydration-root marker in
this design. The only hydration seam is the text-boundary Comment sentinel.

**Evidence**: `crates/ferric/src/ssr.rs:28–43` (constant definitions),
`crates/ferric/src/hydrate.rs:35` (import), `crates/ferric/src/hydrate.rs:148–152`
(skip in adopt), `crates/ferric/src/hydrate.rs:214–237` (`is_sentinel_comment`),
`crates/ferric/src/hydrate.rs:184–209` (`strip_sentinels`)

**Consistency note**: `hydrate.rs` imports `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER`
directly from `crate::ssr` (line 35: `use crate::ssr::{TEXT_CLOSE_MARKER,
TEXT_OPEN_MARKER}`). There is a single definition shared by both the server and client paths;
the marker schema is consistent by construction, not by coincidence.

---

## Summary

| Criterion | Status | Short description |
|---|---|---|
| Detection fires on structural mismatch | CLEAN | All named conditions covered |
| Warning not panic | CLEAN | `console.warn` debug-only; no panic on detection path |
| Recovery by fresh mount | FINDING (NON-BLOCKER) | Extra DOM nodes not removed; primary cases clean |
| Test coverage | FINDING (BLOCKER) | No `wasm-bindgen-test` for mismatch path |

**Overall REQ-SSR-009 verdict: FINDING (BLOCKER)** — the implementation is substantively
correct on the detection and recovery paths, but the acceptance criterion requires a
behavioral `wasm-bindgen-test` and none exists. The test gap blocks the criterion from being
met; the extra-nodes recovery gap is a follow-up item.
