# Area E: Test Coverage — PR #228

**Status**: FINDING (BLOCKER)

## What Was Checked

### `crates/ferric/src/ssr.rs` — 13 tests (lines 151–347)

Examined against issues #223 acceptance criteria (REQ-SSR-001, REQ-SSR-003, REQ-SSR-010, REQ-SSR-012):

| Test | Criterion covered | Assertion style |
|------|-------------------|-----------------|
| `renders_empty_element` (163) | REQ-SSR-001: render returns HTML | `assert_eq!` exact match |
| `renders_element_with_attributes` (169) | REQ-SSR-001: attribute output | `assert_eq!` exact match |
| `renders_element_with_text_child` (175) | REQ-SSR-001: text content + TEXT_OPEN/CLOSE_MARKER | `assert_eq!` exact match |
| `escapes_all_five_injection_chars_in_text_content` (189) | REQ-SSR-010: HTML escaping in text | `assert_eq!` per-character |
| `escapes_all_five_injection_chars_in_attribute_values` (199) | REQ-SSR-010: HTML escaping in attributes | `assert_eq!` per-character |
| `text_node_wrapped_in_markers` (213) | REQ-SSR-001: TEXT_OPEN/CLOSE_MARKER sentinel placement | `assert_eq!` exact match |
| `empty_text_node_wrapped_in_markers` (220) | Edge case: empty text with markers | `assert_eq!` exact match |
| `renders_nested_children_at_correct_depth` (229) | REQ-SSR-012: nested element output | `assert_eq!` exact match |
| `renders_deeply_nested_structure` (246) | Edge case: deeply nested | `assert_eq!` exact match |
| `void_element_emits_self_closing_tag` (263) | REQ-SSR-012: void elements | `assert_eq!` exact match |
| `void_element_with_attributes_emits_self_closing` (269) | REQ-SSR-012: void elements with attrs | `assert_eq!` exact match |
| `two_renders_produce_independent_outputs` (280) | REQ-SSR-003: concurrent render isolation | `contains` / `!contains` on output HTML |
| `signal_created_inside_render_does_not_survive_beyond_call` (316) | REQ-SSR-003: signal scope | `contains` / `!contains` on output HTML |

Assertions are exact-match where the expected output is deterministic; the two isolation tests use `contains` checks, which are intentional given the structure (text markers embedded in HTML output).

**REQ-SSR-003 subscriber-count sub-criterion**: both isolation tests verify that signal values from one render do not appear in a subsequent render's HTML output. Neither asserts the subscriber count on the signal objects themselves (the second half of the REQ-SSR-003 contract: "a signal seeded only for one render has zero subscribers after the call completes"). The HTML-output check demonstrates functional isolation but leaves the subscriber-count contract unverified by test.

### `crates/chirp-server/src/ssr.rs` — 3 tests (lines 188–226)

Examined against issue #226 REQ-SSR-011:

| Test | Criterion covered |
|------|-------------------|
| `assemble_document_contains_required_structure` (193) | REQ-SSR-011: doctype, app div, WASM script, ES module type |
| `assemble_document_empty_server_html` (215) | Edge case: empty server HTML |
| `assemble_document_rejects_quoted_script_path` (224) | Injection guard on script path (debug_assert) |

The `ssr_handler` function itself (the Axum HTTP handler) has no test: no axum test-client call, no response status check, no content-type header check.

### `crates/ferric/src/hydrate.rs` — examined for tests

The file is 466 lines. It implements `hydrate` (line 40), `adopt_root_vnode` (76), `adopt_vnode` (91), `adopt_children` (149), `emit_mismatch_warning` (259/276), and the sentinel-cleanup and event-wiring logic throughout. The module attribute at line 22 (`#![cfg(target_arch = "wasm32")]`) restricts the file to WASM compilation.

There is no `#[cfg(test)]` section of any kind in this file.

---

## Evidence

**Blocker — zero hydration tests:**
- `crates/ferric/src/hydrate.rs:1` — entire file, 466 lines, no `#[cfg(test)]` block

The PR description's identity assertions list only:
- `native-tests-pass`: 56 unit + 7 doc tests
- `wasm-compile`: ✅

There is no `wasm-bindgen-test` assertion. The PR claims to close issues #224 and #226.

Issue #224 (BAR-004, `release-gating: true`) acceptance criteria, verbatim:

> During hydration, **zero** structural mutations (create/replace/move/remove) occur under the hydration root. Observable via `MutationObserver` or node-identity check in a **headless `wasm-bindgen-test`**.

> After hydrate, an event dispatch (e.g. a click) updates the DOM in place through the signal/patch path; the element is not recreated.

> Hydration wires the event handlers carried in the first render's VNode tree onto the adopted elements...

Issue #226 (BAR-006, `release-gating: true`) acceptance criteria, verbatim:

> A headless `wasm-bindgen-test` hydrates against a deliberately mismatched server DOM and confirms: the diagnostic fires, the resulting live DOM matches the client render of that subtree, and the rest remains adopted.

**Non-blocker — REQ-SSR-003 subscriber count:**
- `crates/ferric/src/ssr.rs:280` — `two_renders_produce_independent_outputs` checks HTML output content, not signal subscriber count
- `crates/ferric/src/ssr.rs:316` — `signal_created_inside_render_does_not_survive_beyond_call` same pattern

---

## Finding

### BLOCKER: `hydrate.rs` has no tests; issues #224 and #226 require headless `wasm-bindgen-test`

`crates/ferric/src/hydrate.rs` carries the full implementation of three release-gating acceptance criteria:

- **REQ-SSR-004** (adopt walk, zero structural mutations, reactive effect establishment) — required by issue #224
- **REQ-SSR-005** (event handler wiring on adopted elements, dispatch updates DOM in place) — required by issue #224
- **REQ-SSR-009** (mismatch detection, diagnostic fires, rest remains adopted) — required by issue #226

Both issues mark these requirements as `release-gating: true` and both explicitly name "headless `wasm-bindgen-test`" as the required test form. No such tests exist in the PR. The PR's own identity assertions table confirms this: it records `native-tests-pass` and `wasm-compile` but no `wasm-bindgen-test` check.

The core hydration behavior — the adopt walk emitting zero DOM mutations, event wiring on adopted nodes, and the mismatch fallback path — cannot be verified by native unit tests because the implementation is `#![cfg(target_arch = "wasm32")]` and depends on `web_sys` DOM types that have no native equivalent. The `wasm-bindgen-test` runner with `--headless` and a real browser or Node DOM is the only execution path that can test this code.

**What satisfies this finding**: a `#[cfg(test)]` module in `crates/ferric/src/hydrate.rs` (or a companion `crates/ferric/tests/hydrate_*.rs`) with `wasm-bindgen-test` test cases that:

1. For REQ-SSR-004: hydrate a component against an SSR-rendered DOM and assert zero structural mutations via `MutationObserver` callback count or pre/post node-identity check on the root's children.
2. For REQ-SSR-005: after hydration, dispatch a click event on a wired element and assert the DOM reflects the signal-driven update without the element being recreated (node identity preserved).
3. For REQ-SSR-009: hydrate against a deliberately mismatched server DOM (e.g., a `<span>` where a `<div>` is expected) and assert `emit_mismatch_warning` fires and the resulting DOM reflects the client render of that subtree.

These tests must be runnable via `wasm-pack test --headless` or `cargo test --target wasm32-unknown-unknown` with `wasm-bindgen-test-runner`, and the PR identity table should include a `wasm-tests-pass` assertion before merge.

---

### NON-BLOCKER: REQ-SSR-003 subscriber-count contract is not directly tested

Issue #223 states: "a signal seeded only for one render has zero subscribers after `render_to_string` completes." The two isolation tests at lines 280 and 316 demonstrate that one render's signal value does not appear in another render's HTML output — a valid functional check — but neither one inspects the subscriber list on the `Signal` object after `render_to_string` returns.

If `ReactiveScope` teardown were broken in a way that left subscribers registered but suppressed (not firing, not propagating), the HTML-output check would still pass. The contract would be violated without a test catching it.

**What would satisfy this**: after `render_to_string` returns, retrieve the `Signal` created inside the closure (via a shared `Arc` or `Cell` written inside the closure and read outside) and assert `signal.subscriber_count() == 0` or the equivalent inspection the `Signal` type exposes. If `Signal` does not currently expose a subscriber count, a `#[cfg(test)]` accessor is acceptable.

This is not a blocker because the functional isolation is verified and the absence of leaked subscribers is consistent with the passing tests; the gap is in directness of assertion, not in observed behavior.
