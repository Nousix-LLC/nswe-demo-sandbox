# SYNTHESIS.md — SUBTASK_tests verification gate

## Gate Result: PASS

---

## Identity Assertions

| Assertion | Status | Evidence |
|-----------|--------|----------|
| **I-LOWER-01** | SATISFIED | 16 conformance tests in `lowering.rs`; all pass. Every §2.12 lowering table row has a dedicated test (`test_dom_element_self_closing`, `test_dom_element_open_close`, `test_static_attribute`, `test_dynamic_attribute`, `test_static_text_child`, `test_dynamic_text_into_string`, `test_dynamic_vnode_child`, `test_nested_element`, `test_on_click_handler`, `test_on_input_handler`, `test_for_list`, `test_for_list_all_keyed`, `test_key_attribute`, `test_vec_children`, `test_view_produces_vnode`, `test_component_invocation`). |
| **I-LOWER-02** | SATISFIED | `test_for_list_all_keyed` asserts `el.key.is_some()` and `el.key == key_fn(item)` for every child produced by `<For>`. |
| **I-DIAG-01** | SATISFIED | Exactly 7 trybuild fixtures present in `tests/compile_fail/`; all 7 pass. `.stderr` files committed and generated on build server via `TRYBUILD=overwrite`. |

---

## Check Results

### Check 1 — Behavioral-Contract Verification (I-LOWER-01, I-LOWER-02): PASS

```
running 16 tests
test test_component_invocation ... ok
test test_dom_element_open_close ... ok
test test_dom_element_self_closing ... ok
test test_dynamic_attribute ... ok
test test_dynamic_text_into_string ... ok
test test_dynamic_vnode_child ... ok
test test_for_list ... ok
test test_for_list_all_keyed ... ok
test test_key_attribute ... ok
test test_nested_element ... ok
test test_on_click_handler ... ok
test test_on_input_handler ... ok
test test_static_attribute ... ok
test test_static_text_child ... ok
test test_vec_children ... ok
test test_view_produces_vnode ... ok

test result: ok. 16 passed; 0 failed; 0 ignored; 0 measured
```

### Check 2 — Wiring Verification (I-DIAG-01): PASS

```
test tests/compile_fail/dynamic_not_into_string.rs ... ok
test tests/compile_fail/for_missing_key.rs ... ok
test tests/compile_fail/handler_not_closure.rs ... ok
test tests/compile_fail/mismatched_close_tag.rs ... ok
test tests/compile_fail/multiple_top_level.rs ... ok
test tests/compile_fail/unclosed_element.rs ... ok
test tests/compile_fail/unknown_event_name.rs ... ok

test compile_fail ... ok
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

Note: `dynamic_not_into_string.stderr` required regeneration via `TRYBUILD=overwrite` because SUBTASK_conformance's crate-root re-exports (`pub use crate::vdom::{EventKind, VElement, VNode}`) resolved the previously-stale golden file. See BAR-FERRIC-008 notes below.

### Check 3 — Pre-existing Test Regression (I-ADDITIVE-01): PASS

```
cargo test -p ferric --lib: 37 passed; 0 failed
```

No regressions from the additive crate-root re-exports added by SUBTASK_conformance.

### Check 4 — Code Review: PASS

- All 7 fixtures are minimal (3–10 lines each), each targeting exactly one intended error
- Descriptive docstrings (`//! §2.9: ...`) referencing the spec
- No server credentials, SSH key paths, user names, or host paths in committed files
- No files in `crates/ferric-macros/src/` were modified by either spoke

---

## Pre-existing Test Regression

- **I-ADDITIVE-01** (scope): `cargo test -p ferric --lib` — all 37 tests pass ✓

---

## Code Review Notes

**BAR-FERRIC-008: CLEARED** (no violations in final committed `.stderr` files)

SUBTASK_trybuild originally flagged a BAR-FERRIC-008 violation in `dynamic_not_into_string.stderr`: the initial `.stderr` showed macro-internal errors (`E0433: cannot find 'VElement' in 'ferric'`) because the ferric crate-root re-exports did not yet exist. SUBTASK_conformance added `pub use crate::vdom::{EventKind, VElement, VNode};` at the ferric crate root, which resolved the generated code paths. After regenerating with `TRYBUILD=overwrite`, the `.stderr` now correctly shows:

```
error[E0277]: the trait bound `String: From<i32>` is not satisfied
 --> tests/compile_fail/dynamic_not_into_string.rs:3:48
```

This is exactly the author-vocabulary error described in §2.9 — the type error at the `{expr}` span naming the required conversion. BAR-FERRIC-008 is fully cleared across all 7 fixtures.

---

## Commit

| Field | Value |
|-------|-------|
| Commit hash | `6b86b85` |
| Branch | `work/ferric-epic-authoring-r1` |
| Message | `feat(ferric-macros): add view! trybuild suite + Cargo.toml updates (closes #139)` |
| Files committed (17) | `Cargo.lock`, `crates/ferric-macros/Cargo.toml`, `crates/ferric-macros/tests/compile_fail.rs`, 7 fixture `.rs` files, 7 fixture `.stderr` files |

Note: `crates/ferric-macros/tests/lowering.rs` and the ferric crate-root re-exports were committed by SUBTASK_conformance in earlier commits (`4c77b9a`, `c28b0e1`, `d027534`).

---

## Final Branch State

```
6b86b85 feat(ferric-macros): add view! trybuild suite + Cargo.toml updates (closes #139)
d027534 fix(conformance): resolve VElement::into() type ambiguity in test_nested_element
c28b0e1 fix(ferric): re-export VElement, VNode, EventKind at crate root
4c77b9a test(ferric-macros): conformance tests for view! lowering table (§2.12)
3c3d4aa feat(ferric-macros): implement view! macro (#139)
```
