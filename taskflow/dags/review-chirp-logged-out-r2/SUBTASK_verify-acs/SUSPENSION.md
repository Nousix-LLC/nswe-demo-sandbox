# SUSPENSION.md — SUBTASK_verify-acs

## Decomposition Summary

**Decompose evaluation**: NeedsDecompose  
**Reason**: The brief enumerates five distinct AC verifications (AC-1 through AC-5), each with its own verification protocol targeting different source files and different aspects of the codebase. The scope trigger and Distinct Concerns Test fired by that enumeration. Five concerns mapping to separate components can be verified in parallel by independent agents.

## Children Materialized

| Task ID | Workspace | Purpose |
|---------|-----------|---------|
| `SUBTASK_ac1-verify` | `SUBTASK_ac1-verify/` | Verify AC-1: B1 fix and public endpoint guard status |
| `SUBTASK_ac4-verify` | `SUBTASK_ac4-verify/` | Verify AC-4: B2 fix and CTA routing |
| `SUBTASK_ac235-confirm` | `SUBTASK_ac235-confirm/` | Confirm AC-2, AC-3, AC-5 unchanged |
| `SUBTASK_acs-gate` | `SUBTASK_acs-gate/` | Synthesis gate: compile findings-acs.md |

## Resumption Condition

All children (`SUBTASK_ac1-verify`, `SUBTASK_ac4-verify`, `SUBTASK_ac235-confirm`, `SUBTASK_acs-gate`) reach terminal lifecycle states. The synthesis child (`SUBTASK_acs-gate`) will fold this parent SUSPENDED → COMPLETED by calling `engine_resume_suspended` after writing `findings-acs.md` and `SYNTHESIS.md`.

## Named State Authored

- `_GLOBAL.md` — subtree hub document
- `contracts/_MANIFEST.yaml` — subtree contract (spoke output schema)
- `SUBTASK_ac1-verify/_BRIEF.md`
- `SUBTASK_ac4-verify/_BRIEF.md`
- `SUBTASK_ac235-confirm/_BRIEF.md`
- `SUBTASK_acs-gate/_BRIEF.md`
