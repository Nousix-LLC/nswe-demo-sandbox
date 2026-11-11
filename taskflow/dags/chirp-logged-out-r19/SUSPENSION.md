# SUSPENSION.md — chirp-logged-out-r19

**Status**: SUSPENDED (NeedsDecompose)

## Decomposition Summary

This DAG root task has decomposed into two serial child tasks:

| Task | Description | Status |
|------|-------------|--------|
| `SUBTASK_ac-verify-remediate` | Verify AC-1–AC-5, fix gaps, write ac-verdicts.yaml | PENDING |
| `SUBTASK_synthesis` | Read verdicts, write SYNTHESIS.md, fold parent | PENDING (depends on first) |

## Resumption Condition

All child tasks reach terminal lifecycle states. The synthesis task writes
`SYNTHESIS.md` at this workspace root and calls `engine_resume_suspended` to fold
this SUSPENDED node to COMPLETED.

## Context

Branch: `work/chirp-logged-out`  
Current HEAD: `decb6196c2c1e6ed421d393a642f0c844cc333ba`  
PR: #263 (OPEN/MERGEABLE/CLEAN)  
r18 verdict: PASS for all 5 ACs  

The decomposition was triggered by the serial pipeline of distinct responsibilities:
verify → (optionally fix) → synthesize. Prior rounds r10–r18 stalled before synthesis;
decomposing guarantees the synthesis step runs as a committed separate invocation.
