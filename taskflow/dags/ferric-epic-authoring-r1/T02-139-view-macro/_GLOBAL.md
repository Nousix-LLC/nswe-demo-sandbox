# _GLOBAL.md — T02-139-view-macro hub

**Task ID:** ferric-authoring-139-view  
**Hub:** ferric-epic-authoring-r1  
**Branch:** `work/ferric-epic-authoring-r1`  
**Closes:** GitHub issue #139  
**Depends on:** T01 (ferric-authoring-137-138, COMPLETE at commit `1ccdce0`)

---

## Objective

Deliver the `view!` declarative proc-macro that enables angle-bracket HTML-like view trees, lowering
each construct to existing `VNode` builder calls. Everything is strictly additive (identity IA4); no
frozen prelude item is modified. When this subtree COMPLETES, issue #139 is closed and the branch is
CI-ready for T03.

The authoritative specification is `design/ferric/authoring-model.md` §2 (lowering table §2.12,
diagnostics §2.9, single-root rule §2.10, interop §2.11). The VNode API is `crates/ferric/src/vdom.rs`
(frozen builders: `VElement::new`, `.key`, `.attr`, `.on`, `.child`, `.children`, `vdom::text`).

---

## Task structure

```
SUBTASK_impl (implement the macro)
       |
SUBTASK_tests (write conformance + trybuild suite)
       |
SUBTASK_synthesis (verify all criteria, close #139)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_impl` | none | Create `crates/ferric-macros/`, implement `view!` macro (parser + lowering + diagnostics), wire into workspace and ferric prelude | Commit on `work/ferric-epic-authoring-r1` with new crate |
| `SUBTASK_tests` | `SUBTASK_impl` | Write native conformance tests (lowering equality) and trybuild fixtures (7 diagnostic cases) with committed `.stderr` files | Commit on `work/ferric-epic-authoring-r1` with test suite |
| `SUBTASK_synthesis` | `SUBTASK_tests` | Synthesis gate: verify all identity assertions from `contracts/_MANIFEST.yaml`, close issue #139, leave branch CI-ready for T03 | `SYNTHESIS.md` at this hub workspace |

### Dependency graph

```
SUBTASK_impl ──→ SUBTASK_tests ──→ SUBTASK_synthesis
```

---

## Shared input sources (read-only for all subtasks)

| Source | Location | Note |
|--------|----------|------|
| Specification | `design/ferric/authoring-model.md` §2 | Lowering table §2.12, diagnostics §2.9, single-root §2.10 |
| VNode builder API | `crates/ferric/src/vdom.rs` | Frozen — no new builders may be introduced |
| Release bar | `design/ferric/release-bar.md` §BAR-FERRIC-007, §BAR-FERRIC-008 | verification requirement |
| Epic contract | `../contracts/_MANIFEST.yaml` | Identity IA4 (additive only), IA6 (trybuild in cargo test) |
| This subtree contract | `contracts/_MANIFEST.yaml` | Ownership + identity assertions |
| T01 output | Branch tip `1ccdce0` | The starting state of the branch |

---

## Subtree Methodology Posture

**Dominant task type:** Rust proc-macro implementation (SUBTASK_impl) + Rust testing (SUBTASK_tests).

**Primary bundles across the subtree:**
- `rust` — Rust macros & codegen (`Rust_Macros_And_Codegen_Methodology.md`), library diagnostics
  (`Rust_Library_Diagnostics_Methodology.md`), testing, cargo ecosystem
- `testing` — conformance testing (`Testing_Conformance_Against_External_Reference_Methodology.md`),
  unit testing methodology
- `synthesis` — SUBTASK_synthesis is a verification gate, not a prose summary

**Cross-cutting binding on all subtasks:**
- MSRV stable Rust 1.82; no nightly features.
- All additions are strictly additive; `crates/ferric`'s frozen prelude surface is preserved verbatim.
- The lowering table in authoring-model.md §2.12 is the behavioral contract; every row is both
  the implementation target (SUBTASK_impl) and the test oracle (SUBTASK_tests).
- Diagnostic messages must be in terms of the author's code, not macro internals (BAR-FERRIC-008).

---

## Contract

**Contract location:** `contracts/` (read-only for all descendants)  
**Contract kind:** `behavioral_spec`  
**Manifest:** `contracts/_MANIFEST.yaml`

The seam between SUBTASK_impl and SUBTASK_tests is the behavior of the `view!` macro as specified
by authoring-model.md §2.12 and §2.9. SUBTASK_impl produces the behavior; SUBTASK_tests verifies it.
SUBTASK_synthesis asserts all six identity assertions in `contracts/_MANIFEST.yaml` before closing #139.

Ownership:
- `SUBTASK_impl` owns all `crates/ferric-macros/` files and the ferric crate wiring changes.
- `SUBTASK_tests` owns all test files under `crates/ferric-macros/tests/`.
- `SUBTASK_synthesis` reads both outputs; writes no implementation code.

---

## Branch protocol

Each subtask commits to `work/ferric-epic-authoring-r1` from the previous subtask's tip.
SUBTASK_impl begins from `1ccdce0`. SUBTASK_tests begins from SUBTASK_impl's tip commit.
SUBTASK_synthesis begins from SUBTASK_tests' tip commit.
