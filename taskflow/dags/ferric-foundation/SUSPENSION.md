# SUSPENSION.md — ferric-foundation (NeedsDecompose)

**Task**: `ferric-foundation` (forked root DAG node, swe-coder)
**Terminal state**: SUSPENDED · `decompose_evaluation = NeedsDecompose`
**Resumption**: implicit — all child tasks reach terminal lifecycle state; the subtree resolves
via the synthesis fold (`SUBTASK_synthesis` authors `SYNTHESIS.md` at this workspace and calls
`engine_resume_suspended` to flip this node SUSPENDED → COMPLETED).

## Why decomposed (evaluation summary)
The brief (issue #4) enumerates distinct system components — workspace scaffolding, reactive signal
graph, component/view-tree model, DOM rendering + keyed diff via wasm-bindgen/web-sys, wasm build +
example, and a verification/PR gate. The Scope-Based trigger fires by enumeration; the Distinct
Concerns Test fails (reactive-systems vs wasm/web-sys are different specialties); the
Single-Responsibility Rule fails (scaffold **and** signals **and** components **and** DOM **and**
build **and** test **and** PR); Output Size ≫ 400 lines; the work far exceeds the 100-tool-call
atomic floor. Verdict: **NeedsDecompose**.

## Chosen cut — layered serial spine + synthesis gate
One crate split into layers sharing a public surface. A parallel feature fan-out was rejected
because the layers carry a real compile-and-test dependency (the view layer tests the *real*
`Signal`; the DOM runtime renders *real* `VNode`s) — mocking those to parallelize would be L3 mock
depth (forbidden). So the signal→view and view→dom seams are **serialized**; the crate's public API
surface is **frozen** (`contracts/ferric_api.rs`, kind `rust_trait`, mock depth L0) because it is
the shared `lib.rs`/prelude mount surface and the stable surface later engagement crates depend on.

## Subtree (DAG)
```
SUBTASK_scaffold ─> SUBTASK_reactive_core ─> SUBTASK_view_and_diff ─> SUBTASK_dom_runtime ─┐
       └──────────────────────────────────────────────────────────────────────────────> SUBTASK_synthesis
```
| Group | Task id | Depends on | Owns |
|---|---|---|---|
| 0 | `SUBTASK_scaffold` | none | clone+branch, root/crate `Cargo.toml`, `lib.rs`+prelude, compiling stubs |
| 1 | `SUBTASK_reactive_core` | scaffold | `src/signal.rs` + native tests (incl. leak test) |
| 2 | `SUBTASK_view_and_diff` | reactive_core | `src/vdom.rs`, `src/component.rs` + diff tests |
| 3 | `SUBTASK_dom_runtime` | view_and_diff | `src/dom.rs`, `examples/counter.rs`, `README.md` |
| 4 | `SUBTASK_synthesis` (gate) | all above | `SYNTHESIS.md` + branch push + PR into `main` |

## Named state authored before suspend
- `contracts/_MANIFEST.yaml` (ownership + 8 identities) and `contracts/ferric_api.rs` (frozen API).
- `_GLOBAL.md` (subtree hub: posture, constraints, chosen-cut rationale, Task Summary table).
- One `_BRIEF.md` per child (methodology IDs propagated; inherited constraints; Task Kind set;
  the synthesis brief authored as a verification gate).
- Five `engine_amend_plan { add_task }` calls — all applied.

## Shared working tree
A single git clone at `checkout/` under this workspace (created by `SUBTASK_scaffold`), branch
`work/ferric-foundation` from `main`; serial single-writer access; `main` never touched.
