# SUSPENSION.md — design-ferric-1_0-r3

## Status

SUSPENDED — NeedsDecompose

## Decomposition

This node decomposed the Ferric 1.0 design gap review into four child tasks:

| Task | Kind | Description |
|---|---|---|
| SUBTASK_design-doc-review | standard | Evaluates concerns 1–3 (completeness, release bar, coherence) against all 14 design documents and directive #114 |
| SUBTASK_foundation-buildability | standard | Evaluates concern 4 (buildability on existing ferric/router/http foundation) |
| SUBTASK_ticket-review | standard | Evaluates concern 5 (ticket quality and wave plan for all 36 issues #129–#164) |
| SUBTASK_synthesis | synthesis | Compiles all findings, posts verdict on PR#128, files board issues, writes root SYNTHESIS.md |

The three analysis spokes (design-doc-review, foundation-buildability, ticket-review) run in parallel with no inter-spoke dependencies. The synthesis gate depends on all three.

## Resumption Condition

All child tasks reach terminal lifecycle states. The synthesis task (SUBTASK_synthesis) writes `SYNTHESIS.md` at this workspace root and folds this node SUSPENDED → COMPLETED.

## Artifacts Authored

- `_GLOBAL.md` — subtree hub with shared context, task structure, methodology posture, and contract declarations
- `contracts/_MANIFEST.yaml` — ownership and identities contract
- `contracts/findings_schema.yaml` — YAML schema all spoke findings files must conform to
- `SUBTASK_design-doc-review/_BRIEF.md`
- `SUBTASK_foundation-buildability/_BRIEF.md`
- `SUBTASK_ticket-review/_BRIEF.md`
- `SUBTASK_synthesis/_BRIEF.md`
