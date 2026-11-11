# SUSPENSION.md — SUBTASK_design-doc-review

## Status: Suspended (NeedsDecompose)

SUBTASK_design-doc-review decomposed into four children and is now suspended pending their completion.

## Decomposition Rationale

The brief enumerated three distinct concerns:
1. Completeness against directive #114
2. Release bar quality (testability of BAR-FERRIC-* items)
3. Internal coherence and traceability (REQ-* IDs, artifact map, issues)

Each concern requires a different methodology lens, different primary source documents, and different analytical approach. The scope trigger and distinct-concerns test both fired on enumeration. The task decomposed rather than attempting all three concerns in a single invocation.

## Subtree Authored

Hub document: `SUBTASK_design-doc-review/_GLOBAL.md`  
Contract: `SUBTASK_design-doc-review/contracts/_MANIFEST.yaml`  
Spoke findings schema: `SUBTASK_design-doc-review/contracts/spoke_findings_schema.yaml`

Children materialized:
- `SUBTASK_completeness-review` — concern 1, no dependencies
- `SUBTASK_release-bar-quality` — concern 2, no dependencies
- `SUBTASK_traceability-review` — concern 3, no dependencies
- `SUBTASK_findings-synthesis` — synthesis gate, depends on the three spokes

## Resumption Condition

All four child tasks reach terminal lifecycle state (SUBTASK_completeness-review, SUBTASK_release-bar-quality, SUBTASK_traceability-review, SUBTASK_findings-synthesis completed). The final deliverable `design-doc-findings.md` is written by SUBTASK_findings-synthesis.
