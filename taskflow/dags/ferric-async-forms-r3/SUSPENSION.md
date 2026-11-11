# SUSPENSION — ferric-async-forms-r3

**Status**: suspended / NeedsDecompose  
**Suspended at**: 2026-11-05

## Reason

The three blocking findings (B1, B2, B3) span distinct system components and cannot be safely executed in a single invocation. This node has decomposed the work into a three-task linear chain:

1. **SUBTASK_b1_reactive_resource** — adds `create_resource` to `async_resource.rs` (independent of B2/B3)
2. **SUBTASK_b2_b3_event_dom** — adds event-carrying `EventHandler` and fixes Bind DOM plumbing (entangled; depends on SUBTASK_b1)
3. **SUBTASK_synthesis** — verifies CI, writes final `SYNTHESIS.md` verdict (depends on SUBTASK_b2_b3_event_dom)

## Resumption condition

This node resumes when the entire child subtree (SUBTASK_b1_reactive_resource → SUBTASK_b2_b3_event_dom → SUBTASK_synthesis) reaches terminal states and the observation seam `taskflow/dags/ferric-async-forms-r3/SYNTHESIS.md` is observable.
