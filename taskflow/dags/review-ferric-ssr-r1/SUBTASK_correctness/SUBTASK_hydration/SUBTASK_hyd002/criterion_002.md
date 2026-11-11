# REQ-HYD-002 — Signal Updates Propagate Post-Hydration

**Status**: FINDING (NON-BLOCKER)

**What was checked**:
1. The `hydrate()` reactive-update code path in `crates/ferric/src/hydrate.rs`.
2. Whether the same `diff`/`apply_patches_impl` machinery used by `dom::mount` is reused for post-hydration signal updates.
3. All test functions added in PR #228 across `crates/ferric/src/ssr.rs`, `crates/ferric/src/hydrate.rs`, `crates/chirp-server/src/ssr.rs`, and the `crates/ferric/tests/` path on branch `work/ferric-ssr-r1`.

---

## Reactive-Update Path: Mechanically Correct

**Evidence**: `crates/ferric/src/hydrate.rs:1–57` (diff lines 299–357)

```rust
pub fn hydrate<F>(root: web_sys::Element, f: F)
where
    F: Fn() -> VNode + 'static,
{
    let previous: Rc<RefCell<Option<VNode>>> = Rc::new(RefCell::new(None));

    create_effect(move || {
        let next = f();                        // ← reactive read; subscribes signals
        let mut slot = previous.borrow_mut();
        match slot.take() {
            None => {
                adopt_root_vnode(&document, &root, &next);  // first run: adopt server DOM
                strip_sentinels(&root);
            }
            Some(prev) => {
                let patches = diff(&prev, &next);            // subsequent runs: keyed diff
                apply_patches_impl(&document, &root, &patches);
            }
        }
        *slot = Some(next);
    });
}
```

The first closure run (the `None` arm) calls `f()` inside `create_effect`, establishing signal subscriptions identically to `dom::mount`'s own `create_effect` wrapper. Every subsequent signal update re-runs the closure, taking the `Some(prev)` branch, which calls `diff` and `apply_patches_impl` — the same keyed-patch path `dom::mount` uses. No separate subscription mechanism is introduced. The reactive-update path is structurally sound.

---

## Finding: No Test Exercises the Hydrate → Signal Update → DOM Change Sequence

**Evidence of absence**:
- `crates/ferric/src/hydrate.rs` (diff lines 298–769): zero `#[test]` or `#[wasm_bindgen_test]` functions.
- `crates/ferric/tests/` on `work/ferric-ssr-r1`: directory does not exist (HTTP 404 from GitHub Contents API).
- Diff-wide search for `wasm_bindgen_test`: no matches at all.
- `crates/ferric/src/ssr.rs` tests (diff lines 958–1200): all test `render_to_string` (SSR path only — REQ-SSR-002, REQ-SSR-003, REQ-SSR-012). None touch `hydrate()`.
- `crates/chirp-server/src/ssr.rs` tests (diff lines 258–292): test `assemble_document` HTML structure only.

**Issue #224, REQ-HYD-002 acceptance criterion 2** states:

> "After hydrate, an event dispatch (e.g. a click) updates the DOM in place through the signal/patch path; the element is not recreated."

No test verifies this. A complete test would need to:
1. Render a component with a signal to an HTML string via `render_to_string`.
2. Mount that HTML into a fake DOM (e.g., `gloo_utils::document()` or a `web-sys` mock in a `wasm_bindgen_test` context).
3. Call `hydrate()` over the mounted HTML.
4. Trigger a signal update (e.g., `counter.set(counter.get() + 1)`).
5. Assert the DOM node changed in place (text content updated; no element recreated).

No such test exists in this PR.

**Severity reasoning**: The reactive path is correctly implemented and reuses the proven `dom::mount` machinery. The gap is test observability, not a demonstrable code defect. Per inherited constraints, non-blockers flag but do not hold landing.

---

## Summary

| Check | Result |
|-------|--------|
| Signal subscriptions wired via `create_effect` on first hydrate run | ✓ Correct |
| Subsequent updates routed through `diff` / `apply_patches_impl` | ✓ Same path as `dom::mount` |
| Test: hydrate + signal update + DOM assertion | ✗ Absent — no `wasm_bindgen_test` integration test |
| `crates/ferric/tests/` integration test directory | ✗ Does not exist on branch |
