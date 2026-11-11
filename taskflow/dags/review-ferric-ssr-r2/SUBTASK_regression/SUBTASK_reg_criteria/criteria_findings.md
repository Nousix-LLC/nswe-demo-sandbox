# Criteria Findings — ferric-ssr-r4 Regression Check

**Scope**: commits `7fb90c7`, `e625c3f`, `75c1eef` on branch `work/ferric-ssr-r1`  
**Pinned commit**: `75c1eef`  
**Criteria checked**: REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-005, REQ-HYD-001, REQ-HYD-002, REQ-HYD-004, REQ-MIS-001, REQ-MIS-002

---

## Criteria Results

### REQ-SSR-001: No web_sys or DOM dependency in ssr.rs
**Verdict**: PASS  
**Evidence**: `crates/ferric/src/ssr.rs` at `75c1eef` — only import is `use crate::vdom::VNode;` (line 20). Module-level doc states the constraint explicitly: "it must never reference `web_sys` or `wasm_bindgen`." The `7fb90c7` docstring-fix commit adds doc text to `ssr.rs` only; no `use` statements were added or changed. `crates/chirp-server/src/ssr.rs` (new in this PR) is a separate crate and uses `axum` + `ferric` through the public crate API — it has no direct `web_sys` import and does not alter `ferric/src/ssr.rs`'s dependency surface.

### REQ-SSR-002: Drop for ReactiveScope still present and purges subscribers; app.rs doesn't leak subscriptions during SSR
**Verdict**: PASS  
**Evidence**: `crates/ferric/src/signal.rs` at `75c1eef` — `impl Drop for ReactiveScope` at line 502 calls `with_rt(|rt| rt.dispose(self.id))`. The `dispose` method at line 310 iterates all owned nodes recursively, removes each from every source's subscriber set, and clears the arena entry. The module doc confirms: "dropping a reactive scope unsubscribes everything it owns." `render_to_string` in `crates/ferric/src/ssr.rs` creates a `ReactiveScope`, runs the closure, and returns — the scope and vnode both drop at the function's close brace. The new `app.rs` `start()` function is the wasm entry point and is never called server-side; the `ssr_handler` in `crates/chirp-server/src/ssr.rs` calls `ferric::render_to_string` with a standalone closure that contains no `create_signal` calls, so no signals from `AppContext::new()` are created during server-side rendering.

### REQ-SSR-003: VNode recursion in ssr.rs still unbounded — no stack limit introduced
**Verdict**: PASS  
**Evidence**: `crates/ferric/src/ssr.rs` at `75c1eef` — `render_node` recurses via `for child in &el.children { render_node(child, out); }` with no depth counter, no recursion guard, and no call to any depth-limiting primitive. The `7fb90c7` commit added only doc text; no code was inserted between the recursive child-iteration loop and the caller.

### REQ-SSR-005: render_to_string still a crate-root export; ssr_handler still calls it correctly
**Verdict**: PASS  
**Evidence**: `crates/ferric/src/lib.rs` at `75c1eef` — `pub use crate::ssr::render_to_string;` is present (unconditional, not cfg-gated). `crates/chirp-server/src/ssr.rs` `ssr_handler` calls `ferric::render_to_string(|| { ferric::VElement::new("div")... })` via the crate-root path. `crates/chirp-server/src/api/router.rs` at line 69 registers `.route("/", get(ssr_handler))` with the import `use crate::ssr::ssr_handler;` at line 45.

### REQ-HYD-001: Adopt-pass still reuses existing DOM nodes on matching paths — no createElement on matching paths
**Verdict**: PASS  
**Evidence**: `crates/ferric/src/hydrate.rs` at `75c1eef` — in `adopt_vnode`, the `VNode::Element` match arm checks tag equality; on match it calls `set_events` and `adopt_children` without calling `create_node`. `create_node` is called only in the mismatch branch (`other =>`) or in `adopt_children` for VNode children that have no corresponding DOM node. Text node matching path (`Some(t) if t.data() == *text`) is a no-op — no DOM mutation. The `adopt_children` loop skips sentinel Comment nodes and calls `adopt_vnode` for each matched pair; `create_node` is called only for the missing-child recovery path (`for missing_idx in vnode_idx..vnode_children.len()`).

### REQ-HYD-002: Reactive updates post-hydration still use create_effect → diff → apply_patches_impl path; new app.rs wiring doesn't bypass this
**Verdict**: PASS  
**Evidence**: `crates/ferric/src/hydrate.rs` at `75c1eef` — the `hydrate` function wraps all update logic in `create_effect(move || { ... Some(prev) => { let patches = diff(&prev, &next); apply_patches_impl(&document, &root, &patches); } ... })`. Every subsequent signal-driven re-render follows this exact path. `crates/chirp-frontend/src/app.rs` at `75c1eef` — `start()` calls `ferric::hydrate(root, app)` on the SSR path (`if root.has_child_nodes()`), passing the `app` closure through `ferric::hydrate` unchanged. No alternative reactive update path is introduced.

### REQ-HYD-004: Marker format still type-level enforced: single import from ssr.rs, no local copies
**Verdict**: PASS  
**Evidence**: `crates/ferric/src/hydrate.rs` at `75c1eef` — `use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER};` is the sole source of the marker constants; no `const TEXT_OPEN_MARKER` or `const TEXT_CLOSE_MARKER` definition appears in `hydrate.rs`. `crates/ferric/tests/hydrate_wasm.rs` (new in `e625c3f`) contains no `TEXT_OPEN_MARKER` or `TEXT_CLOSE_MARKER` definition or import — the test file uses `web_sys` and `wasm_bindgen_test` only. No other file in the PR changed set defines a local copy of the marker constants.

### REQ-MIS-001: assemble_document still produces valid HTML5; no new string interpolation introduced by 7fb90c7 docstring fix
**Verdict**: PASS  
**Evidence**: `crates/chirp-server/src/ssr.rs` at `75c1eef` — `assemble_document` uses a single `format!()` call with the template `<!doctype html>`, `<html lang="en">`, `<meta charset="utf-8">`, `<meta name="viewport" ...>`, `<title>chirp</title>`, `<div id="app">{server_html}</div>`, ES-module `<script>` tag. The `{server_html}` slot receives output from `render_to_string`, which HTML-escapes all text and attribute values via `escape_html`. The `{wasm_script_path}` slot is guarded by `debug_assert!(!wasm_script_path.contains('"'))`. The `7fb90c7` docstring-fix commit changes doc comments in `crates/ferric/src/ssr.rs`; it does not touch `assemble_document` or introduce any new string interpolation in the HTML assembly path.

### REQ-MIS-002: Mismatch detection+recovery still replaces mismatched nodes without structural corruption
**Verdict**: PASS  
**Evidence**: `crates/ferric/src/hydrate.rs` at `75c1eef` — `adopt_vnode` handles all three mismatch cases without corrupting surrounding structure: (1) element tag mismatch — `parent.replace_child(&new_node, dom_node)` replaces exactly the mismatched node; (2) text content mismatch — `t.set_data(text)` updates the existing text node in place; (3) expected text, found non-text — `parent.replace_child(&new_text, dom_node)` replaces exactly the mismatched node. The `adopt_children` extra-DOM-node case emits a warning and breaks without removing nodes. None of these operations modify siblings or ancestors of the target node.

---

## What Was Examined and Found Clean

- REQ-SSR-001: `crates/ferric/src/ssr.rs` import list at `75c1eef` → clean (no web_sys or wasm_bindgen)
- REQ-SSR-002: `crates/ferric/src/signal.rs` `impl Drop for ReactiveScope` at `75c1eef` → clean; `crates/chirp-server/src/ssr.rs` `ssr_handler` closure contents → clean (no create_signal calls)
- REQ-SSR-003: `crates/ferric/src/ssr.rs` `render_node` recursion path at `75c1eef` → clean (no depth limiter)
- REQ-SSR-005: `crates/ferric/src/lib.rs` re-export at `75c1eef` → clean; `crates/chirp-server/src/ssr.rs` call site → clean; `crates/chirp-server/src/api/router.rs` route registration → clean
- REQ-HYD-001: `crates/ferric/src/hydrate.rs` `adopt_vnode` match path at `75c1eef` → clean (no createElement on match)
- REQ-HYD-002: `crates/ferric/src/hydrate.rs` `hydrate` effect body at `75c1eef` → clean; `crates/chirp-frontend/src/app.rs` `start()` hydrate dispatch → clean
- REQ-HYD-004: `crates/ferric/src/hydrate.rs` marker imports at `75c1eef` → clean (single import from ssr); `crates/ferric/tests/hydrate_wasm.rs` → clean (no local marker definitions)
- REQ-MIS-001: `crates/chirp-server/src/ssr.rs` `assemble_document` format string at `75c1eef` → clean (valid HTML5 template, escaping intact); ferric `ssr.rs` docstring-fix scope → clean (doc only)
- REQ-MIS-002: `crates/ferric/src/hydrate.rs` mismatch recovery paths at `75c1eef` → clean (node-scoped replacement, no structural corruption)
