# Area C: Error Handling — PR #228

**Status**: FINDING (NON-BLOCKER)

## What Was Checked

**`ferric::render_to_string` (`crates/ferric/src/ssr.rs`)**

Signature (`-> String`), `render_node` recursion, and `escape_html`. Neither contains `unwrap`, `expect`, `panic!`, or `todo!`. String serialization of VNode trees is a closed operation with no I/O and no allocation-failure surface. Infallible by design.

**`ferric::hydrate` (`crates/ferric/src/hydrate.rs`)**

Signature (`-> ()`), the fifteen `expect()` calls in production code, and three `let _ =` result discards. Work done:

- Lines 44–47 (`window()` / `.document()` expects): appropriate for a `#![cfg(target_arch = "wasm32")]` function that documents a browser-context requirement; the messages name the invariant. Acceptable.
- Lines 44–47 also examined for the question the brief poses: *can callers handle a mismatch without panicking?* Mismatch recovery in `adopt_vnode` / `adopt_children` is handled in-place (emit warning + client-render recovery path); callers never see a panic from a structural mismatch. What callers cannot observe is *whether* recovery ran — `hydrate` returns `()` with no error type. Noted but not elevated: this is primarily an API surface question (Area A), and the current browser-only deployment context makes it low-risk.
- Twelve `expect()` calls in `adopt_root_vnode`, `adopt_vnode`, `adopt_children`, `create_node`, `apply_patches_impl`, `resolve_impl`, `resolve_element_impl`, and `set_events`: each names the invariant it asserts. The DOM operations they guard (`replace_child`, `append_child`, `parent_node`, `create_element`, `set_attribute`, `add_event_listener_with_callback`) can fail when the DOM tree is in a state inconsistent with Ferric's model. Panicking on a corrupt-model invariant is acceptable per the methodology; messages are actionable.
- `let _ = element.remove_child(node)` at line 217 (`strip_sentinels`): **see Finding 1**.
- `let _ = element.remove_event_listener_with_callback(...)` at line 426 and `let _ = js_sys::Reflect::delete_property(...)` at line 427: best-effort cleanup of a previously stashed listener before rebinding; failure here leaks the old listener (a hazard) but does not corrupt the new binding. The idiom is consistent with the pre-existing `dom.rs` pattern.
- `let _ = js_sys::Reflect::set(...)` at line 445: writes the new listener into the stash. Failure here would prevent the stashed-listener cleanup on the next render cycle, allowing event-listener accumulation over re-renders. `Reflect::set` on a live browser `Element` does not fail under normal conditions; the concern is bounded. Noted but not elevated to its own finding given the low failure probability.

**`chirp-server::ssr_handler` and `chirp-server::assemble_document` (`crates/chirp-server/src/ssr.rs`)**

- `ssr_handler` (line 159): calls `ferric::render_to_string`, which is infallible. No error handling needed; the handler correctly returns `200 OK` unconditionally. The inline comment at lines 166–168 incorrectly states `render_to_string` "currently panics (via `todo!()`)"; the implemented function in this PR has no `todo!()`. Stale comment is an Area F concern; the runtime panic-safety is correct.
- `assemble_document` (line 98): **see Finding 2**.

**`crates/ferric/src/lib.rs`**

Examined the new `pub mod ssr` and `#[cfg(target_arch = "wasm32")] pub mod hydrate` declarations and their re-exports. No new error handling surface.

## Evidence

**Finding 1 — `strip_sentinels` discards `remove_child` result silently**

```
crates/ferric/src/hydrate.rs:204   fn strip_sentinels(element: &web_sys::Element)
crates/ferric/src/hydrate.rs:217       let _ = element.remove_child(node);
```

Sentinel removal is correctness-critical: `hydrate`'s doc comment and the module-level comment both state that after `strip_sentinels` the DOM child indices must align with VNode path indices used by all subsequent diff/patch passes. The `let _ =` discards the `Result<Node, JsValue>` without explaining why failure is impossible and without any fallback.

The failure mode is in practice unreachable: nodes are collected from `element.child_nodes()` on the same call stack with no event-loop interleaving (single-threaded WASM), so each node is a valid child of `element` when `remove_child` is called. But the silent discard obscures this reasoning. A reader cannot distinguish "we know this is infallible and here is why" from "we forgot to handle this." If the invariant ever breaks — say, through a future refactor that introduces an async yield between collection and removal — the failure would go undetected and produce index misalignment that corrupts all subsequent reactive renders silently.

**Finding 2 — `assemble_document` injection guard elided in release builds**

```
crates/chirp-server/src/ssr.rs:98    pub fn assemble_document(server_html: &str, wasm_script_path: &str) -> String
crates/chirp-server/src/ssr.rs:99    debug_assert!(!wasm_script_path.contains('"'), ...)
```

The function interpolates `wasm_script_path` verbatim into an HTML `src` attribute. It guards against attribute injection (a double-quote in the path that would close the attribute early) with `debug_assert!`, which the Rust compiler elides in release builds. The current call site always passes the trusted literal `"/pkg/chirp.js"`, so the injection risk is currently zero. However, `assemble_document` is `pub`; a future caller that passes a dynamic or user-influenced path would have no production-build protection.

## Finding

**Finding 1 (NON-BLOCKER) — Replace `let _ = element.remove_child(node)` with an asserting call that names the invariant**

Location: `crates/ferric/src/hydrate.rs:217`

The silent discard on a correctness-critical operation is a maintenance hazard: it suppresses any failure that breaks the index-alignment invariant `strip_sentinels` is responsible for, and it offers no documentation to future readers of why the discard is intentional. Per Rust error handling practice, discarding a `Result` requires either an `unwrap_or_else` with a comment or an `expect` whose message names the invariant.

Satisfying resolution: replace `let _ = element.remove_child(node)` with:

```rust
element
    .remove_child(node)
    .expect("strip_sentinels: remove_child failed — node was just read from child_nodes() on this element");
```

This documents the invariant, panics loudly if it is ever violated (allowing the fault to surface rather than propagating silently into corrupted index state), and matches the style of the other `expect()` calls throughout this file.

---

**Finding 2 (NON-BLOCKER) — Promote `debug_assert!` to `assert!` or escape `wasm_script_path` before interpolation**

Location: `crates/chirp-server/src/ssr.rs:99`

A `debug_assert!` on an injection-prevention check is effectively no check in production. The invariant ("this argument must not contain a double-quote") should hold in all build profiles, not only in development. The function is `pub`, so its callers are not restricted to the current trusted call site.

Satisfying resolution: either (a) change `debug_assert!` to `assert!` so the guard fires in all builds regardless of optimization level, or (b) HTML-escape `wasm_script_path` before interpolation (replacing `"` with `&quot;`) as a defense-in-depth measure that makes the function safe regardless of its callers' discipline. Option (b) is preferred because it eliminates the injection risk entirely rather than making the function abort on bad input.
