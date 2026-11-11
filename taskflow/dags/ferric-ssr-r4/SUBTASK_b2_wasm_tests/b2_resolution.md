# B2 Resolution: wasm-bindgen-test coverage for hydrate.rs

## Summary

Finding B2 (REQ-SSR-006 / Area E) has been remediated. Three `#[wasm_bindgen_test]`
functions were added in `crates/ferric/tests/hydrate_wasm.rs` covering all three
required areas. All three tests pass under `wasm-pack test --headless --chrome`.

---

## Commit SHA

`e625c3f` on branch `work/ferric-ssr-r1`, pushed to origin (`Nousix-LLC/nswe-demo`, PR #228).

---

## Test Functions

| Test name | Requirement |
|---|---|
| `hydrate_adopt_walk_no_structural_mutations` | REQ-SSR-004 / #224 — adopt walk without structural mutations |
| `hydrate_event_wiring_post_hydration` | REQ-SSR-005 / #224 — event wiring preserved post-hydration |
| `hydrate_mismatch_detection_recovery` | REQ-SSR-006 / #226 — mismatch detection and DOM recovery |

File: `crates/ferric/tests/hydrate_wasm.rs` (197 lines)

---

## wasm-pack test Output Summary

```
     Running tests/hydrate_wasm.rs (.../debug/deps/hydrate_wasm-d2045e14cd1e4a77.wasm)
Running headless tests in Chrome on `http://127.0.0.1:41255/`
Loading Wasm module...

running 3 tests
test hydrate_mismatch_detection_recovery ... ok
test hydrate_event_wiring_post_hydration ... ok
test hydrate_adopt_walk_no_structural_mutations ... ok

test result: ok. 3 passed; 0 failed; 0 ignored; 0 filtered out; finished in 0.05s
```

The existing `dom` unit test (`dom::wasm_tests::mount_renders_initial_view_and_reacts_to_signal_change`)
also continued to pass (1 passed) under the same run.

**Command used** (run in a Docker container with `rust:1.86` + `chromium` + `wasm-pack` on the
build server, since `chromium` is not installed natively on the server):

```
wasm-pack test --headless --chrome crates/ferric
```

Exit code: 0.

---

## Implementation Notes

### Test approach

- File `crates/ferric/tests/hydrate_wasm.rs` gated with `#![cfg(target_arch = "wasm32")]`.
- Each test: creates a `<div>` container attached to `document.body`, injects SSR-like
  `innerHTML`, calls `ferric::hydrate(container, closure)`, asserts post-condition, and
  removes the container (`cleanup`).
- `wasm_bindgen_test_configure!(run_in_browser)` — runs in a real headless browser context
  so all `web_sys` DOM APIs work correctly.

### Test 1 — adopt walk without structural mutations
- Injects `<div><span>hello</span></div>` as `innerHTML`.
- Captures `before_div` and `before_span` node handles.
- Hydrates with an identical component.
- Asserts `before_div.is_same_node(after_div)` and `before_span.is_same_node(after_span)`.
- Both nodes have the same identity ⇒ no `appendChild`/`replaceChild` fired.

### Test 2 — event wiring post-hydration
- Creates `Signal<i32>` initialized to `0`.
- Injects `<button>0</button>` as SSR markup.
- Hydrates with a component that reads the signal (subscribing the effect) and wires
  `EventKind::Click` → `count.set(val + 1)`.
- Calls `HtmlElement::click()` on the button.
- Asserts `button.text_content() == Some("1")` (signal-driven re-render applied).
- Asserts `before_button.is_same_node(after_button)` (element patched, not recreated).

### Test 3 — mismatch detection and recovery
- Injects `<div>text</div>` as SSR markup (server has `<div>`).
- Hydrates with a component that returns `<p>text</p>` (client expects `<p>` — deliberate mismatch).
- Asserts that `container.first_child().tag_name() == "p"` after hydration.
- Verifies that `replace_child` in `adopt_vnode`'s mismatch branch correctly swaps the node.
- Note: `emit_mismatch_warning` is `cfg(debug_assertions)`-gated; this test verifies DOM
  recovery rather than the console output.

---

## Complications

### No native Chrome on build server

The build server (`100.90.75.93`) does not have Chrome/Chromium installed natively, and
`sudo` is not available to `mattm`. The tests were run in a temporary Docker container
(`rust:1.86` + `apt-get install chromium chromium-driver` + wasm-pack installed via
the official installer) using the Docker daemon that is already available to `mattm` on
the server (required for k3d). The container mounts the repository and the Cargo registry
cache for fast compilation.

### wasm-pack not pre-installed on build server

`wasm-pack` was installed on the build server via its official install script
(`curl … | sh`) and confirmed at version 0.13.1 before the Docker-based test run.
Inside the container, a fresh wasm-pack install was used for the test run itself.
