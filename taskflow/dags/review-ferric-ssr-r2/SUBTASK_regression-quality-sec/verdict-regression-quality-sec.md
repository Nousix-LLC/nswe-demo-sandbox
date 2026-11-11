# Regression, Quality, and Security — Verdict

Commits reviewed: `7fb90c7`, `e625c3f`, `75c1eef` (branch `work/ferric-ssr-r1`, PR #228).

## Summary

**Overall Verdict: FAIL.** All 10 previously-clean regression criteria pass and no security blockers were found. The code quality spoke returns FAIL on one Blocker: all three `wasm-bindgen-test` fixtures inject HTML without the `<!--$t-->` / `<!--/$t-->` sentinel markers that `render_to_string` emits for every `VNode::Text`, so the sentinel-handling code paths in `hydrate.rs` are never exercised. The adopt-walk coverage claimed for REQ-SSR-004 is false.

---

## Regression Check — Previously-Clean Criteria

**Verdict: PASS**

The ferric-ssr-r4 commits touched `app.rs` (hydrate/mount conditional), `lib.rs` (cfg wasm32 gate on the `hydrate` module), and added `hydrate_wasm.rs`. They did not modify `ssr.rs` or `chirp-server/src/ssr.rs`. Criteria whose implementation was not touched carry status UNCHANGED.

| Criterion | Status | Note |
|---|---|---|
| REQ-SSR-001 — `render_to_string` no `web_sys`/DOM dep | PASS | `lib.rs` cfg gate on `pub mod hydrate` / `pub use crate::hydrate::hydrate` correctly excludes DOM imports from native builds; `ssr.rs` unchanged |
| REQ-SSR-002 — Reactive scope isolation during SSR | UNCHANGED | `ssr.rs` not changed; `ReactiveScope` drop/purge logic intact |
| REQ-SSR-003 — Nested VNode recursion unbounded | UNCHANGED | `render_node` recursion not changed |
| REQ-SSR-004 — SSR/hydration markers defined once, imported not copied | PASS | `hydrate.rs` has single import `use crate::ssr::{TEXT_CLOSE_MARKER, TEXT_OPEN_MARKER}`; new `hydrate_wasm.rs` imports neither constant and contains no inline sentinel literals |
| REQ-SSR-005 — `render_to_string` crate-root export intact | PASS | `pub use crate::ssr::render_to_string` is unconditional in `lib.rs` after the cfg gate changes; `chirp-server` call site unaffected |
| REQ-HYD-001 — Adopt pass reuses existing DOM nodes | PASS | No new commit changes `adopt_vnode`; `create_element` only on mismatch paths; `app.rs` wires the entry point without altering adopt-pass logic |
| REQ-HYD-002 — Reactive updates via `create_effect → diff → apply_patches_impl` | UNCHANGED | `hydrate.rs` logic reformatted only; effect chain unchanged |
| REQ-HYD-004 — Marker format enforced at type level, single import | PASS | Confirmed no new local copies in any file added by these commits |
| REQ-MIS-001 — `assemble_document` produces valid HTML5 fragment | UNCHANGED | `chirp-server/src/ssr.rs` not changed |
| REQ-MIS-002 — Mismatch detection+recovery replaces nodes without structural corruption | UNCHANGED | `hydrate.rs` mismatch paths reformatted only; `replace_child` logic intact |

(The brief and manifest label these "9 previously-clean criteria" but the list contains 10 items. The regression check covers all 10 named criteria.)

---

## Code Quality — New Code

**Verdict: FAIL**

### app.rs

**cfg-gate pattern**: PASS. `#[cfg(target_arch = "wasm32")]` applied at statement level is the correct scope; the two `#[cfg]` / `#[cfg(not)]` guards are exhaustive with no gap. `ferric::hydrate` called fully-qualified, so no conditional import needed. Pattern is idiomatic.

**Readability**: PASS. Inline comment at lines 150–153 names both paths, states the condition, and explains why a compile-time gate is used.

Non-blocker findings on `app.rs` are listed in the Fresh Non-Blocking Issues section.

### hydrate_wasm.rs

**Duplication**: PASS. `make_container()` and `cleanup()` correctly extract the only genuinely shared scaffolding. The per-test content (HTML fixtures, VNode closures, assertions) is meaningfully distinct; no copy-paste risk.

**Hardcoded strings vs. imported constants — BLOCKER**  
**Location**: `hydrate_wasm.rs:62`, `hydrate_wasm.rs:113`, `hydrate_wasm.rs:174`

All three tests inject HTML using bare string fixtures with no `<!--$t-->` / `<!--/$t-->` sentinel markers:

| Test | Injected fixture | Actual `render_to_string` output |
|---|---|---|
| `hydrate_adopt_walk_no_structural_mutations` | `<div><span>hello</span></div>` | `<div><span><!--$t-->hello<!--/$t--></span></div>` |
| `hydrate_event_wiring_post_hydration` | `<button>0</button>` | `<button><!--$t-->0<!--/$t--></button>` |
| `hydrate_mismatch_detection_recovery` | `<div>text</div>` | `<div><!--$t-->text<!--/$t--></div>` |

`render_to_string` in `ssr.rs` wraps every `VNode::Text` in `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER`. The sentinel-handling code paths in `hydrate.rs` (the `is_sentinel_comment` check and `strip_sentinels` logic) are never reached by any test. All three tests — including the REQ-SSR-004 adopt-walk test — pass on DOM input that production SSR cannot produce. The adopt-walk node-identity coverage is false.

**What must be fixed**: update all three `set_inner_html` calls to use sentinel-wrapped fixtures, or import and use `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER` from `ferric::ssr`. After updating fixtures, verify that `ferric::hydrate` handles the flanking comment nodes correctly and that the existing `is_same_node` / `text_content` assertions still hold.

Non-blocker findings on `hydrate_wasm.rs` are listed below.

---

## Security — New Code

**Verdict: PASS**

**HTML injection and escaping**: `escape_html` in `ferric/ssr.rs` escapes all five injection-risky characters (`<`, `>`, `&`, `"`, `'`) in both text-content and attribute-value contexts. Test coverage for all five is present in `ssr.rs`. No unescaped user data reaches the HTML output on any path through `render_node` / `render_to_string`.

**`assemble_document`**: inserts already-escaped `server_html` raw (by design). `wasm_script_path` is inserted verbatim but its current value is the hardcoded literal `"/pkg/chirp.js"` — no user input reaches this parameter. The `debug_assert!` quote-guard is noted as advisory below.

**`hydrate.rs` DOM writes**: all use safe browser APIs — `create_text_node`, `set_attribute`, `set_text_content`, `replace_child`, `append_child`. No `innerHTML` usage anywhere in `hydrate.rs`. No injection path.

**`hydrate_wasm.rs` test security**: no sensitive data, no hardcoded secrets, no token values. All `set_inner_html` calls use developer-authored string literals. The `#[cfg(target_arch = "wasm32")]` gate confines these tests to the WASM harness.

---

## Fresh Non-Blocking Issues

The following do not block merge. They are listed here for the parent DAG's synthesis task to decide whether to file issues.

1. **`app.rs:155` — predicate precision**: `has_child_nodes()` returns true for whitespace text nodes and HTML comment nodes. If `#app` can contain incidental whitespace on a non-SSR page load, the wasm32 path incorrectly routes to `ferric::hydrate`. Use `root.first_element_child().is_some()`, or verify the server template guarantees `#app` is empty when SSR is not in use.

2. **`app.rs:156` — discarded return value**: `ferric::hydrate(root, app)` return not checked. If `hydrate` returns `Result`, a mismatch fails silently. Verify the return type; annotate with `#[must_use]` in the library or handle at the call site.

3. **`app.rs:8`, `103–104` — docstrings describe only mount**: neither the module-level docstring nor `start()`'s docstring mentions that on wasm32 with SSR markup present, `start()` hydrates rather than mounts. Both should be updated to describe the conditional behavior.

4. **`hydrate_wasm.rs` — test name covers one of two assertions**: `hydrate_event_wiring_post_hydration` verifies both that the click handler fires (text content becomes `"1"`) and that node identity is preserved after re-render. The name covers only the first. Consider `hydrate_click_handler_fires_and_node_identity_preserved` or splitting into two functions.

5. **`hydrate_wasm.rs:97, 158, 194` — cleanup not RAII**: `cleanup(&container)` is called at the end of each test body. If any earlier `.expect()` or assertion panics, cleanup is skipped and the container stays in `<body>` for the rest of the test session. Replace with a RAII guard (`ContainerGuard` struct with `Drop` calling `cleanup`) to ensure teardown on both normal and panic exit.

6. **`hydrate_wasm.rs:65–70` — text node identity not captured in Test 1**: `hydrate_adopt_walk_no_structural_mutations` captures `before_div` and `before_span` but not the text node `"hello"` inside `<span>`. An implementation that re-creates the text node while preserving element nodes would pass. Capture `let before_text = before_span.first_child()` before hydration and assert `is_same_node` afterward.

7. **`chirp-server/src/ssr.rs assemble_document` — `debug_assert!` stripped in release**: the `debug_assert!` guard on `wasm_script_path`'s double-quote constraint is elided in release builds. The value is currently a hardcoded constant so there is no present vulnerability, but `assert!` would protect future callers who might pass a computed path.

8. **`app.rs:156` — style inconsistency**: `ferric::hydrate` is called fully-qualified while `mount` arrives via `use ferric::prelude::*`. Not actionable unless `hydrate` is added to the prelude in a later revision.

---

**Overall Verdict: FAIL**
