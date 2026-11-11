# T01 — Reactive core and VDOM foundation (#137, #138) — COMPLETE

**Task ID:** ferric-authoring-137-138  
**Branch:** `work/ferric-epic-authoring-r1`  
**Baseline commit:** `1ccdce0` (full: see branch HEAD)  
**Closed issues:** #137, #138  
**Completed:** 2026-11-03

---

## What was done

Created the epic branch `work/ferric-epic-authoring-r1` from `65413bbe59cb65641d6f1a85123a87f300900b83`
(the stated main HEAD) and performed a baseline audit confirming the existing code satisfies the
acceptance criteria for both issues.

---

## Acceptance criteria audit

### #137 — BAR-FERRIC-001: Reactive state primitives

| Criterion | Test / Evidence | Verdict |
|---|---|---|
| Prelude exports `create_signal`, `create_memo`, `create_effect`, `batch`, `Signal`, `Memo` | `crates/ferric/src/lib.rs` `pub mod prelude` | ✅ PASS |
| Compiles on stable Rust at MSRV 1.82 | CI matrix (stable target, `ada3aa9`) | ✅ PASS |
| `create_memo` does not recompute when output unchanged | `signal::tests::memo_computes_and_memoizes` — asserts `compute_runs == 1` after second read | ✅ PASS |
| `batch` defers effect execution until batch closes | `signal::tests::batch_coalesces_notifications` — asserts `runs == 2` (not 3) after two batched writes | ✅ PASS |
| Scoped cleanup unsubscribes without stale leaks | `signal::tests::no_stale_subscriber_leak` — subscriber count → 0 after scope drop | ✅ PASS |
| Prelude preserved verbatim | No previously exported item removed or redefined | ✅ PASS |

### #138 — BAR-FERRIC-002: Virtual DOM and keyed DOM patching

| Criterion | Test / Evidence | Verdict |
|---|---|---|
| Keyed list reorder moves nodes, not recreates | `vdom::tests::keyed_children_reorder_emits_moves_not_replaces` | ✅ PASS |
| Partial attribute change produces single `SetAttr`, not `Replace` | `vdom::tests::partial_attr_change_in_subtree_produces_single_setattr` — **added in baseline commit** | ✅ PASS |
| Signal write after mount updates only affected DOM text node | `dom::wasm_tests::mount_renders_initial_view_and_reacts_to_signal_change` | ✅ PASS |

---

## Work performed

One test was missing for a specific acceptance criterion (BAR-FERRIC-002's "partial state update
affects only relevant DOM nodes" at the native vdom-diff layer). Added
`partial_attr_change_in_subtree_produces_single_setattr` to `crates/ferric/src/vdom.rs`:
verifies that a single attribute change inside a subtree produces exactly one `SetAttr` patch
and no `Replace`. All 37 `cargo test -p ferric --lib` tests pass.

No new feature code was added. No existing test, existing public API, or file outside
`crates/ferric/` was modified.

---

## Declared outputs

- ✅ Branch `work/ferric-epic-authoring-r1` created from `65413bbe59cb65641d6f1a85123a87f300900b83`
- ✅ Baseline commit `1ccdce0` on the branch (adds the one missing test)
- ✅ Issue #137 closed with comment referencing the commit
- ✅ Issue #138 closed with comment referencing the commit
- ✅ Branch pushed to `origin/work/ferric-epic-authoring-r1`; CI-ready for T02
