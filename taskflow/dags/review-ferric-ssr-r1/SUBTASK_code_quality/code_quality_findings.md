# PR #228 Code Quality and Design Findings

## Summary

The SSR render path (`render_to_string`, `assemble_document`, `ssr_handler`) is structurally correct, well-factored, and thoroughly tested; five areas found non-blocking issues worth tracking but none that impair correctness. Area E is the exception: `hydrate.rs` carries the full implementation of three release-gating acceptance criteria from issues #224 and #226 — the adopt walk, event wiring, and mismatch fallback — and contains no tests of any kind. Both issues explicitly require headless `wasm-bindgen-test` coverage, and the PR's own identity table does not assert it. That gap is a blocker. The remaining non-blockers span naming asymmetries (Area A), a missing compile-time gate on `ferric::dom` now that `ferric` is a native dependency (Area B), two silent or debug-only error handling choices (Area C), seven duplicated private helpers that will silently diverge on the next edit to either file (Area D), and underdocumented calling contracts on `hydrate` and the text-sentinel constants (Area F). None of the non-blocking findings affect the correctness of the SSR path; all should be filed as follow-on work before the surface stabilises.

---

## Findings by Area

### A. API Surface and Naming

**Status**: FINDING (NON-BLOCKER)

**What was checked**: Public items introduced by PR #228 across both crates: `ferric::lib.rs` module declarations and crate-root re-exports (lines 25–44), `ferric::ssr` public surface (`TEXT_OPEN_MARKER`, `TEXT_CLOSE_MARKER`, `render_to_string`), `ferric::hydrate` public surface (`hydrate`), `chirp-server::ssr` public surface (`assemble_document`, `ssr_handler`). Naming consistency checks run against Rust API Guidelines (C-CASE, C-CONV, C-WORD-ORDER), the existing ferric naming register (`mount`, `create_signal`, `create_effect`, `diff`), placement relative to the frozen `prelude`, and collision between module and value namespaces.

**Evidence**:

Finding 1 — `hydrate` names both a module and a crate-root re-export (naming collision):

```
crates/ferric/src/lib.rs:31   pub mod hydrate;
crates/ferric/src/lib.rs:42   #[cfg(target_arch = "wasm32")]
crates/ferric/src/lib.rs:43   pub use crate::hydrate::hydrate;
```

The module `ferric::hydrate` (type namespace) and the re-exported function `ferric::hydrate` (value namespace) share a path at the crate root. `use ferric::hydrate;` imports the module, not the function; the function requires `use ferric::hydrate::hydrate;`. Compare with `render_to_string`, where the module is `ferric::ssr` and the function is `ferric::render_to_string` — the names are distinct and there is no collision.

Finding 2 — `ssr_handler` stutters the module name:

```
crates/chirp-server/src/ssr.rs:159   pub async fn ssr_handler() -> Response {
```

The fully qualified path is `chirp_server::ssr::ssr_handler`. Rust API Guideline C-WORD-ORDER encodes the convention that a module's name is not repeated inside its items. The idiomatic name is `chirp_server::ssr::handler`.

**Finding**:

Finding 1 (NON-BLOCKER): `ferric::hydrate` names both a module and a function at the crate root. The two items resolve in different namespaces, so the crate compiles. The practical harm is to first-time users: `use ferric::hydrate;` does not bring the function into scope (it brings the module), which is the opposite of what `use ferric::render_to_string;` does for the SSR path. Satisfying resolution: rename the module from `hydrate` to `hydration` (or `client`) so the crate-root function is `ferric::hydrate` and the module is `ferric::hydration`. Because `ferric` is at `0.x` this is a freely-revisable surface, but correcting it now costs little.

Finding 2 (NON-BLOCKER): `chirp_server::ssr::ssr_handler` stutters the module name. The idiomatic name under the existing module is `handler`. Because this handler is currently wired into the router directly and no external callers exist yet, the rename is cheap now and costs at least a grep-and-replace once more consumers arrive. Neither finding blocks merge; both are worth a cleanup issue before the surface stabilises.

What was clean: `render_to_string` and `hydrate` are clear and idiomatic names; `ferric::ssr` and `ferric::hydrate` module names accurately describe contents; `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` are correctly SCREAMING_SNAKE_CASE and public because they form a cross-crate protocol boundary; closure bounds (`FnOnce` for `render_to_string`, `Fn + 'static` for `hydrate`) are as permissive as the implementation allows; `assemble_document` and its parameters are unambiguous; new exports are correctly excluded from the frozen `prelude`.

---

### B. Abstraction Boundaries

**Status**: FINDING (NON-BLOCKER)

**What was checked**: `ferric::ssr` (new, all imports and full module body), `ferric::hydrate` (new, module-level cfg gate and all browser-API references), `ferric::dom` (unchanged, module declaration and cfg gate status), `chirp-server::ssr` (new, full module body and import list), Cargo manifests (`crates/chirp-server/Cargo.toml`, `crates/ferric/Cargo.toml`), and all `#[cfg(target_arch = "wasm32")]` declarations in `lib.rs`.

**Evidence**:

The core SSR/client boundary (`ssr.rs` clean, `hydrate.rs` gated) is correct. The finding is an asymmetry between `dom` and `hydrate`, both browser-only modules:

```
crates/ferric/src/lib.rs:22   pub mod dom;
```

`pub mod dom;` carries no `#[cfg(target_arch = "wasm32")]` gate, while the peer declaration introduced by this PR does:

```
crates/ferric/src/lib.rs:33   #[cfg(target_arch = "wasm32")]
crates/ferric/src/lib.rs:34   pub mod hydrate;
```

`dom.rs` uses browser APIs without a module gate:

```
crates/ferric/src/dom.rs:46   use wasm_bindgen::closure::Closure;
crates/ferric/src/dom.rs:47   use wasm_bindgen::{JsCast, JsValue};
```

The prelude re-exports `dom::mount` without a cfg guard. The `dom.rs` module comment acknowledges the reliance on panicking stubs off-wasm — a rationale written before `ferric` was a native server dependency.

**Finding**:

The SSR separation is correct. The finding is that `pub mod dom;` is not gated to `wasm32` in `lib.rs`, and the PR does not add that gate even though it introduces the identical pattern for `hydrate`.

Impact: `ferric::dom` and `ferric::prelude::mount` are now reachable from `chirp-server` (native build) because this PR adds `ferric` as a native dependency. They compile only because `web-sys` ships panicking stubs for non-wasm targets. If any downstream code calls `ferric::dom::mount` or anything exported from `ferric::dom`, it will compile silently and panic at runtime — a silent correctness hazard that compile-time gating would prevent entirely.

This matters now because before this PR, `ferric` was always compiled for `wasm32`; the absence of a gate on `dom` had no consequence. The PR demonstrates the right fix (`#[cfg(target_arch = "wasm32")]` on `pub mod hydrate;`) but does not apply it to the equivalent existing module.

What would satisfy this finding:
1. Add `#[cfg(target_arch = "wasm32")]` to `pub mod dom;` in `crates/ferric/src/lib.rs`.
2. Add `#[cfg(target_arch = "wasm32")]` to `pub use crate::dom::mount;` in the `prelude` block.
3. Optionally, move `wasm-bindgen`, `js-sys`, and `web-sys` from `[dependencies]` to `[target.'cfg(target_arch = "wasm32")'.dependencies]` in `crates/ferric/Cargo.toml`.

---

### C. Error Handling

**Status**: FINDING (NON-BLOCKER)

**What was checked**: `ferric::render_to_string` signature, `render_node` recursion, and `escape_html` (all infallible); `ferric::hydrate` signature, all fifteen `expect()` calls, and three `let _ =` result discards in `crates/ferric/src/hydrate.rs`; `chirp-server::ssr_handler` and `chirp-server::assemble_document` in `crates/chirp-server/src/ssr.rs`; `crates/ferric/src/lib.rs` new declarations.

**Evidence**:

Finding 1 — `strip_sentinels` discards `remove_child` result silently:

```
crates/ferric/src/hydrate.rs:204   fn strip_sentinels(element: &web_sys::Element)
crates/ferric/src/hydrate.rs:217       let _ = element.remove_child(node);
```

Sentinel removal is correctness-critical: after `strip_sentinels` the DOM child indices must align with VNode path indices used by all subsequent diff/patch passes. The `let _ =` discards the `Result<Node, JsValue>` without explaining why failure is impossible and without any fallback.

Finding 2 — `assemble_document` injection guard elided in release builds:

```
crates/chirp-server/src/ssr.rs:98    pub fn assemble_document(server_html: &str, wasm_script_path: &str) -> String
crates/chirp-server/src/ssr.rs:99    debug_assert!(!wasm_script_path.contains('"'), ...)
```

The function interpolates `wasm_script_path` verbatim into an HTML `src` attribute. The injection guard is `debug_assert!`, which the Rust compiler elides in release builds. The function is `pub`; a future caller that passes a dynamic or user-influenced path would have no production-build protection.

**Finding**:

Finding 1 (NON-BLOCKER): Replace `let _ = element.remove_child(node)` with an asserting call that names the invariant. Location: `crates/ferric/src/hydrate.rs:217`. The silent discard on a correctness-critical operation is a maintenance hazard: it suppresses any failure that breaks the index-alignment invariant and offers no documentation to future readers of why the discard is intentional. Satisfying resolution:

```rust
element
    .remove_child(node)
    .expect("strip_sentinels: remove_child failed — node was just read from child_nodes() on this element");
```

Finding 2 (NON-BLOCKER): Promote `debug_assert!` to `assert!` or escape `wasm_script_path` before interpolation. Location: `crates/chirp-server/src/ssr.rs:99`. A `debug_assert!` on an injection-prevention check is effectively no check in production. Satisfying resolution: either (a) change `debug_assert!` to `assert!` so the guard fires in all builds, or (b) HTML-escape `wasm_script_path` before interpolation, replacing `"` with `&quot;` as defense-in-depth. Option (b) is preferred.

What was clean: `render_to_string` is infallible by design; the `window()` / `.document()` expects in `hydrate` are appropriate for a browser-context function with documented requirements; the twelve `expect()` calls throughout `hydrate.rs` name their invariants; the `let _ = remove_event_listener_with_callback(...)` and `let _ = Reflect::delete_property(...)` idioms are consistent with the pre-existing `dom.rs` pattern for best-effort cleanup.

---

### D. Function Size, Duplication, and Extensibility

**Status**: FINDING (NON-BLOCKER)

**What was checked**: All functions in `crates/ferric/src/ssr.rs` (new SSR path), all functions in `crates/ferric/src/hydrate.rs` (new hydration path), all private helpers in `crates/ferric/src/dom.rs` (existing client-side mount path), and `crates/chirp-server/src/ssr.rs` (`assemble_document`, `ssr_handler`). Three concerns examined: function sizes, logical duplication between `hydrate.rs` and `dom.rs`, and extensibility seam for async resource injection (#130).

**Evidence**:

Function sizes are clean — every function is individually reviewable; the largest are match dispatchers over exhaustive enums (`apply_patches_impl` ~65 lines, `adopt_children` ~54 lines, `adopt_vnode` ~57 lines). No function requires extraction for size alone.

Finding D-1 — Duplication between `hydrate.rs` and `dom.rs` (seven functions):

| `hydrate.rs` function | Line | `dom.rs` counterpart | Line |
|---|---|---|---|
| `create_node` | `crates/ferric/src/hydrate.rs:300` | `create_node` | `crates/ferric/src/dom.rs:104` |
| `apply_patches_impl` | `crates/ferric/src/hydrate.rs:327` | `apply_patches` | `crates/ferric/src/dom.rs:129` |
| `resolve_impl` | `crates/ferric/src/hydrate.rs:393` | `resolve` | `crates/ferric/src/dom.rs:197` |
| `resolve_element_impl` | `crates/ferric/src/hydrate.rs:407` | `resolve_element` | `crates/ferric/src/dom.rs:212` |
| `set_events` | `crates/ferric/src/hydrate.rs:417` | `set_events` | `crates/ferric/src/dom.rs:220` |
| `event_name` | `crates/ferric/src/hydrate.rs:454` | `event_name` | `crates/ferric/src/dom.rs:260` |
| `stash_key` | `crates/ferric/src/hydrate.rs:461` | `stash_key` | `crates/ferric/src/dom.rs:268` |

The source is structural: all seven `dom.rs` helpers are private (`fn`), so `hydrate.rs` cannot call them and had to copy them. Comments in `hydrate.rs` acknowledge the duplication for `apply_patches_impl`, `resolve_impl`, `resolve_element_impl`, and `set_events`.

Unprotected divergence paths: `create_node` body drift would corrupt the hand-off between the SSR adopt pass and subsequent reactive re-renders; the hardcoded event-detachment array in `set_events` (both files) would silently miss a new `EventKind` variant.

Finding D-2 — `render_to_string` has no seam for async resource injection (#130):

```
crates/ferric/src/ssr.rs:135   pub fn render_to_string<F>(f: F) -> String where F: FnOnce() -> VNode,
```

When #130 (async resources) lands, changing this function's signature will be a breaking change. The `chirp-server` layer carries an explicit seam (`async fn ssr_handler`, commented-out `State(state): State<AppState>` parameter); the ferric library layer does not.

**Finding**:

D-1 (NON-BLOCKER): Seven private helper functions in `crates/ferric/src/hydrate.rs` are copies of private helpers in `crates/ferric/src/dom.rs`. The practical risk is not in this change but in the next one: behavioral fixes must be applied in both files, and the unprotected divergence paths — `create_node` body drift and the hardcoded event-detachment array in `set_events` — are silent. Satisfying resolution: promote the shared helpers to `pub(crate)` visibility in `dom.rs`, or extract them to a crate-private `dom_ops.rs` module, so `hydrate.rs` imports rather than replicates them. Because both modules are `#[cfg(target_arch = "wasm32")]`-gated, the extraction does not require any cross-cfg changes.

D-2 (NON-BLOCKER): `crates/ferric/src/ssr.rs:135` — the synchronous `FnOnce() -> VNode` signature has no hook for async resource resolution. This is deferred by explicit design decision; the finding is that the current shape does not leave the door ajar: a resource-context parameter or a provisional `NoResources` unit type would signal the anticipated direction and avoid a full-signature break when #130 lands.

Neither issue blocks merge. D-1 should be tracked as a follow-on refactor before the next significant addition to `dom.rs` or `hydrate.rs`. D-2 should be revisited at the start of #130 implementation planning.

---

### E. Test Coverage

**Status**: FINDING (BLOCKER)

**What was checked**: `crates/ferric/src/ssr.rs` — 13 tests (lines 151–347) examined against issues #223 acceptance criteria (REQ-SSR-001, REQ-SSR-003, REQ-SSR-010, REQ-SSR-012); `crates/chirp-server/src/ssr.rs` — 3 tests (lines 188–226) examined against issue #226 REQ-SSR-011; `crates/ferric/src/hydrate.rs` — examined for any `#[cfg(test)]` section. The PR description identity assertions table was reviewed.

**Evidence**:

Blocker — zero hydration tests:
- `crates/ferric/src/hydrate.rs:1` — entire file, 466 lines, no `#[cfg(test)]` block

The PR description identity assertions list only `native-tests-pass` (56 unit + 7 doc tests) and `wasm-compile: ✅`. There is no `wasm-bindgen-test` assertion.

Issue #224 (BAR-004, `release-gating: true`) acceptance criteria require a headless `wasm-bindgen-test` for the adopt walk (zero structural mutations), event wiring, and reactive-effect establishment. Issue #226 (BAR-006, `release-gating: true`) acceptance criteria require a headless `wasm-bindgen-test` for mismatch detection, diagnostic firing, and partial adoption. No such tests exist in the PR.

Non-blocker — REQ-SSR-003 subscriber count:
- `crates/ferric/src/ssr.rs:280` — `two_renders_produce_independent_outputs` checks HTML output content, not signal subscriber count
- `crates/ferric/src/ssr.rs:316` — `signal_created_inside_render_does_not_survive_beyond_call` same pattern

**Finding**:

BLOCKER: `hydrate.rs` has no tests; issues #224 and #226 require headless `wasm-bindgen-test`.

`crates/ferric/src/hydrate.rs` carries the full implementation of three release-gating acceptance criteria:
- REQ-SSR-004 (adopt walk, zero structural mutations, reactive effect establishment) — required by issue #224
- REQ-SSR-005 (event handler wiring on adopted elements, dispatch updates DOM in place) — required by issue #224
- REQ-SSR-009 (mismatch detection, diagnostic fires, rest remains adopted) — required by issue #226

Both issues mark these requirements as `release-gating: true` and both explicitly name "headless `wasm-bindgen-test`" as the required test form. The core hydration behavior cannot be verified by native unit tests because the implementation is `#![cfg(target_arch = "wasm32")]` and depends on `web_sys` DOM types that have no native equivalent.

What satisfies this finding: a `#[cfg(test)]` module in `crates/ferric/src/hydrate.rs` (or a companion `crates/ferric/tests/hydrate_*.rs`) with `wasm-bindgen-test` test cases that:
1. For REQ-SSR-004: hydrate a component against an SSR-rendered DOM and assert zero structural mutations via `MutationObserver` callback count or pre/post node-identity check on the root's children.
2. For REQ-SSR-005: after hydration, dispatch a click event on a wired element and assert the DOM reflects the signal-driven update without the element being recreated (node identity preserved).
3. For REQ-SSR-009: hydrate against a deliberately mismatched server DOM and assert `emit_mismatch_warning` fires and the resulting DOM reflects the client render of that subtree.

These tests must be runnable via `wasm-pack test --headless` or `cargo test --target wasm32-unknown-unknown` with `wasm-bindgen-test-runner`, and the PR identity table should include a `wasm-tests-pass` assertion before merge.

NON-BLOCKER: REQ-SSR-003 subscriber-count contract is not directly tested. The two isolation tests at lines 280 and 316 demonstrate functional isolation via HTML output but do not inspect the subscriber list on the `Signal` object after `render_to_string` returns. What would satisfy this: after `render_to_string` returns, assert `signal.subscriber_count() == 0` or the equivalent inspection. This is not a blocker because the functional isolation is verified and the absence of leaked subscribers is consistent with the passing tests.

---

### F. Documentation

**Status**: FINDING (NON-BLOCKER)

**What was checked**: `ferric::render_to_string` doc comment (`crates/ferric/src/ssr.rs:124–138`); `ferric::hydrate` function doc and module-level `//!` comment (`crates/ferric/src/hydrate.rs:35–40`); `ferric::ssr::TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER` doc comments (`crates/ferric/src/ssr.rs:21–35`); `chirp-server::ssr::assemble_document` and `chirp-server::ssr::ssr_handler` doc comments; PR description prose for inflated language and machine-writing tells.

**Evidence**:

Finding 1 — `hydrate`: no timing caveat, no usage example:

`crates/ferric/src/hydrate.rs:35–40` — the entire function doc comment states what `hydrate` does and that `f` must match the SSR closure. Nothing states when this function must be called relative to DOM state. If called before the SSR HTML exists in the DOM, `root.first_child()` returns `None` and mismatch recovery silently client-renders the entire subtree — no error, only a `console.warn` in debug builds.

Finding 2 — `TEXT_OPEN_MARKER` / `TEXT_CLOSE_MARKER`: no version-stability note:

`crates/ferric/src/ssr.rs:21–28` and `:30–35` — both doc comments correctly instruct callers to import the constants rather than copy the literals, but neither states whether the marker format itself (`<!--$t-->` / `<!--/$t-->`) is stable across ferric versions. A user who pre-renders and caches server HTML then upgrades ferric could experience silent hydration failure if the marker format changes.

**Finding**:

Finding 1 (NON-BLOCKER): `hydrate` is underdocumented for a first-time user. The function and module docs cover the protocol overview and the `f`-must-match requirement but omit the most mistake-prone part of the calling contract: `hydrate` must be called only after the SSR HTML is already in the DOM under `root`. When called before that point, the code silently degrades to a full client-render via mismatch recovery — correct enough not to break the app, but wrong enough to defeat the SSR purpose. A sufficient addition: (1) a `# Calling Contract` or `# When to Call` note stating the function must be invoked after the SSR HTML is in the DOM; (2) a `# Examples` section showing how to obtain the mount element and call `hydrate`, mirroring the pattern in `chirp_server::ssr`'s module doc.

Finding 2 (NON-BLOCKER): `TEXT_OPEN_MARKER` and `TEXT_CLOSE_MARKER` are `pub const` values on `pub mod ssr` — first-class public API. Their doc comments correctly tell consumers to import the constants rather than copy the literals. What they do not say is whether the marker format is stable across ferric versions. A `# Stability` note — even a provisional one (e.g., "the marker format is not yet considered stable; pin your ferric dependency to a minor version if you cache server-rendered HTML") — would let users make informed decisions about upgrade cadence.

What was clean: `render_to_string` has adequate prose coverage for a first-time caller. `assemble_document` and `ssr_handler` in `chirp-server::ssr` are well-documented with examples, parameter descriptions, and a `# Panics` note. The PR description prose is factual and plain; no clustered machine-writing tells observed.
