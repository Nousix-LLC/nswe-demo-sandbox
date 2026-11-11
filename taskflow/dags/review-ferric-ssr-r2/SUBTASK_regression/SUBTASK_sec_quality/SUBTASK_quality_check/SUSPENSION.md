# SUSPENSION — SUBTASK_quality_check

**Status**: Suspended (NeedsDecompose)
**Decompose evaluation**: NeedsDecompose
**Reason**: The brief enumerates 3 distinct quality concerns across 2 source files (app.rs, hydrate_wasm.rs), firing the scope/distinct-concerns trigger by enumeration alone.

## Decomposition Summary

Split by source file (2 spokes + 1 synthesis gate):

| Child | Concern | Output |
|-------|---------|--------|
| SUBTASK_app_quality | app.rs new conditional quality + fresh non-blockers in app.rs | app_quality_raw.md |
| SUBTASK_test_quality | hydrate_wasm.rs test code quality + fresh non-blockers in hydrate_wasm.rs | test_quality_raw.md |
| SUBTASK_synthesis | Verification gate: combine both spoke outputs into quality_raw_findings.md | quality_raw_findings.md |

## Resumption Condition

All child tasks (SUBTASK_app_quality, SUBTASK_test_quality, SUBTASK_synthesis) reach terminal lifecycle states.

## State Files Authored

- `_GLOBAL.md` — subtree hub at this workspace
- `contracts/_MANIFEST.yaml` — ownership and identities
- `contracts/spoke_intermediate_schema.md` — spoke output schema
- `SUBTASK_app_quality/_BRIEF.md` — app.rs quality spoke brief
- `SUBTASK_test_quality/_BRIEF.md` — test code quality spoke brief
- `SUBTASK_synthesis/_BRIEF.md` — synthesis gate brief
