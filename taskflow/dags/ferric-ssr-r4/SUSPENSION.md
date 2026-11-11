# SUSPENSION — ferric-ssr-r4

**Status**: Suspended / NeedsDecompose  
**Suspended at**: 2026-11-05  

## Reason

The task spans two distinct blocking concerns (B1 and B2) that fired the scope-based decomposition trigger. The brief explicitly enumerates two separate findings requiring different kinds of changes: a behavioral code fix to the WASM entry point (B1) and test authorship for hydrate.rs (B2). The enumerated-concerns rule mandates decomposition.

## Subtree Materialized

Three child tasks have been created and will be dispatched by the scheduler:

| Task | Kind | Purpose |
|---|---|---|
| `SUBTASK_b1_hydrate_fix` | standard | Fix app.rs to call ferric::hydrate(); correct ssr.rs docstring |
| `SUBTASK_b2_wasm_tests` | standard | Add 3 wasm_bindgen_test tests to hydrate.rs |
| `SUBTASK_synthesis_report` | synthesis | Verify CI + update PR identity table + write SYNTHESIS.md |

## Resumption Condition

All three child tasks reach terminal lifecycle state (COMPLETED or FAILED).

## Context Preserved

- Branch: `work/ferric-ssr-r1` in `/home/user/nswe-demo`  
- PR: #228 (Nousix-LLC/nswe-demo)  
- Declared output: `taskflow/dags/ferric-ssr-r4/SYNTHESIS.md`  
- Hub document: `taskflow/dags/ferric-ssr-r4/_GLOBAL.md`
