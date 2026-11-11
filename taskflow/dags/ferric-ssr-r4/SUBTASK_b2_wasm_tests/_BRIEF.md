# SUBTASK_b2_wasm_tests: Remediate B2 — Add wasm-bindgen-test coverage to hydrate.rs

## Task Specification

**Slug**: SUBTASK_b2_wasm_tests  
**Task Kind**: standard  
**Depends on**: SUBTASK_b1_hydrate_fix  
**Status**: Pending  

### Objective

Remediate blocking finding B2 (REQ-SSR-006 / Area E): add three `#[wasm_bindgen_test]` tests to `crates/ferric/src/hydrate.rs` (or `crates/ferric/tests/hydrate_wasm.rs`) covering adopt-walk without structural mutations, event wiring post-hydration, and mismatch detection. All three tests must pass under `wasm-pack test --headless`.

### Context

This task is part of ferric-ssr-r4 (see `_GLOBAL.md` in the parent workspace).

**Branch**: `work/ferric-ssr-r1` in `/home/user/nswe-demo` (B1 commit already applied by predecessor task)  
**PR**: #228 (Nousix-LLC/nswe-demo)

`wasm-bindgen-test` is already declared as a dev-dependency in `crates/ferric/Cargo.toml`. The hydrate.rs implementation is at `/home/user/nswe-demo/crates/ferric/src/hydrate.rs` (466 lines). There is no existing `#[cfg(test)]` block.

#### Three required tests (from review comment and brief):

1. **REQ-SSR-004 / #224 — adopt walk without structural mutations**  
   Build a minimal SSR HTML string, inject it into a headless DOM under `#app`, call `ferric::hydrate(root, || ...)`, confirm zero `appendChild`/`replaceChild` calls via pre/post node-identity check (`is_same_node`) or MutationObserver.

2. **REQ-SSR-005 / #224 — event wiring post-hydration**  
   After hydration, dispatch a `click` event on a wired element, assert the DOM reflects the signal-driven update, and assert the element's node identity is preserved (not recreated — `is_same_node` before/after click).

3. **REQ-SSR-006 / #226 — mismatch detection**  
   Build a server HTML string with a deliberate structural divergence (server DOM has `<div>`, component returns `<p>`), call `hydrate`, assert that the live DOM matches the client-rendered component (the `<div>` was replaced with `<p>`).

#### Technical notes

- The `#![cfg(target_arch = "wasm32")]` attribute at the top of hydrate.rs already gates the whole module; a `#[cfg(test)]` block at the bottom of the file inherits this gate and is correct.
- Alternatively, a separate `crates/ferric/tests/hydrate_wasm.rs` file with `#![cfg(target_arch = "wasm32")]` works equally well.
- Each test needs `use wasm_bindgen_test::*;` and `wasm_bindgen_test_configure!(run_in_browser);`.
- DOM setup: `web_sys::window().unwrap().document().unwrap().create_element("div")` for the root container; `innerHTML` for injecting SSR HTML.
- For event-wiring test: use `create_signal` from `ferric::signal` and a component closure that reads the signal; dispatch click via `HtmlElement::click()` or `element.dispatch_event(&MouseEvent::new("click").unwrap())`.
- For mismatch test: check `cfg(debug_assertions)` gating — `emit_mismatch_warning` is only active in debug builds; test should still verify the DOM structure is recovered (the `<div>` replaced by `<p>`), not necessarily the console.warn output (which is hard to capture in tests).

---

## Inputs

| Input | Location |
|---|---|
| Subtree hub | `taskflow/dags/ferric-ssr-r4/_GLOBAL.md` |
| B1 resolution (predecessor output) | `taskflow/dags/ferric-ssr-r4/SUBTASK_b1_hydrate_fix/b1_resolution.md` |
| hydrate.rs full implementation | `/home/user/nswe-demo/crates/ferric/src/hydrate.rs` |
| ferric Cargo.toml | `/home/user/nswe-demo/crates/ferric/Cargo.toml` |
| ferric signal API | `/home/user/nswe-demo/crates/ferric/src/signal.rs` |
| ferric vdom API | `/home/user/nswe-demo/crates/ferric/src/vdom.rs` |

---

## Success Criteria

- `crates/ferric/src/hydrate.rs` (or `crates/ferric/tests/hydrate_wasm.rs`) contains three `#[wasm_bindgen_test]` functions: one for adopt-walk, one for event-wiring, one for mismatch-detection.
- `wasm-pack test crates/ferric --headless` (or equivalent) exits 0 with all three tests PASSED on the build server.
- Changes committed to `work/ferric-ssr-r1` and pushed to origin.

---

## Declared Output

`taskflow/dags/ferric-ssr-r4/SUBTASK_b2_wasm_tests/b2_resolution.md`

The file must record:
- Commit SHA(s) pushed to `work/ferric-ssr-r1`
- Names of the three test functions
- `wasm-pack test` output summary (pass/fail counts)
- Any complications encountered
