# COMPLETE — SUBTASK_conformance

**Status**: completed  
**Branch**: `work/ferric-epic-authoring-r1`

---

## Deliverables

| File | Description | Commits |
|------|-------------|---------|
| `crates/ferric-macros/tests/lowering.rs` | 16 conformance tests covering every §2.12 lowering-table row | `4c77b9a`, `c28b0e1`, `d027534` |
| `crates/ferric-macros/Cargo.toml` | Added `[dev-dependencies] ferric = { path = "../ferric" }` | `4c77b9a` |
| `crates/ferric/src/lib.rs` | Added `pub use crate::vdom::{EventKind, VElement, VNode};` crate-root re-exports | `c28b0e1` |

---

## Test Results

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

`cargo test -p ferric --lib`: 37 passed; 0 failed (no regressions from the additive re-exports).

---

## Identity Assertions Satisfied

| Assertion | Evidence |
|-----------|----------|
| **I-LOWER-01** — all §2.12 rows covered | 15 tests cover each row; `test_nested_element` adds extra coverage for the open/close row |
| **I-LOWER-02** — `<For>` produces all_keyed Vec<VNode> with correct keys | `test_for_list_all_keyed` asserts `el.key.is_some()` and `el.key == key_fn(item)` for each child |

---

## Design Decisions

**VNode equality helper**: `VNode`/`VElement` do not derive `PartialEq` (handlers are
`Rc<dyn Fn()>`). Used recursive `vnode_eq` / `velem_eq` helpers that compare tag, key,
attrs, event *kinds* (not handler identity), and children. All assertion messages carry
`{:?}` output for debuggability.

**Type-inference ambiguity (E0283)**: The `view!` macro generates a local
`enum __FerricChildren` with `impl From<VElement>` inside blocks that have `{expr}`
interpolations. Rust's coherence checker sees these as competing candidates even across
function boundaries in the same file. Fixed in `test_nested_element` by binding the inner
VNode explicitly: `let inner: VNode = VNode::from(VElement::new(...));` — this removes the
ambiguous `.into()` call.

**Crate-root re-exports**: The `view!` macro generates code using absolute paths
`::ferric::VElement`, `::ferric::VNode`, `::ferric::EventKind`. These only existed as
`ferric::vdom::*`. Added `pub use crate::vdom::{EventKind, VElement, VNode};` at the
ferric crate root (additive-only — `ferric::vdom::*` and `ferric::prelude::*` unchanged).

---

## Constraints Respected

- No files in `crates/ferric-macros/src/` were modified
- No server address, SSH key path, user name, or host paths in committed files
- Rust workspace rust-version 1.82 — no nightly features used
