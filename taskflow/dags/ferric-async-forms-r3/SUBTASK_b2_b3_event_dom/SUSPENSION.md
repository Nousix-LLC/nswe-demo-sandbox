# SUSPENSION — SUBTASK_b2_b3_event_dom

**Status**: Suspended — NeedsDecompose  
**Suspended at**: 2026-11-05

## Decomposition

This node decomposed into two serial child tasks:

| Child slug | Concern | Depends on |
|-----------|---------|------------|
| `SUBTASK_b2_event_handler` | B2: `EventHandler` enum in `vdom.rs`; dispatch in `dom.rs`; prevent_default WASM test | none (within subtree) |
| `SUBTASK_b3_bind_dom` | B3: `Bind::on_input_event_handler()` in `form.rs`; DOM→signal WASM test | `SUBTASK_b2_event_handler` |

## Resumption condition

Both child tasks must reach terminal COMPLETED state. HAL will resume this node when the subtree resolves.

## Named-state artifacts

- Hub: `taskflow/dags/ferric-async-forms-r3/SUBTASK_b2_b3_event_dom/_GLOBAL.md`
- B2 brief: `taskflow/dags/ferric-async-forms-r3/SUBTASK_b2_b3_event_dom/SUBTASK_b2_event_handler/_BRIEF.md`
- B3 brief: `taskflow/dags/ferric-async-forms-r3/SUBTASK_b2_b3_event_dom/SUBTASK_b3_bind_dom/_BRIEF.md`
