# SUSPENSION.md — spoke-ui-states

## Status

**Lifecycle**: SUSPENDED / NeedsDecompose

## Decomposition summary

The spoke-ui-states task was decomposed into three child tasks after the Scope-Based trigger
fired: the brief enumerates five distinct concerns (enumerated-concerns rule) across two
separable code clusters (Distinct Concerns Test).

**Cut**: landing.rs states (AC-2, AC-3, header_nav aspect of AC-4) versus routing/CTA files
(AC-4 sign-up path, CTA link correctness, route annotation anomaly).

## Children materialized

| Task id | Workspace | Concern cluster | Dependencies |
|---------|-----------|-----------------|--------------|
| `SUBTASK_landing-states` | `spoke-ui-states/SUBTASK_landing-states` | AC-2, AC-3, header_nav | none |
| `SUBTASK_routing-ctas` | `spoke-ui-states/SUBTASK_routing-ctas` | AC-4 routing, CTA link, annotation | none |
| `SUBTASK_synthesis` | `spoke-ui-states/SUBTASK_synthesis` | Verification gate + REVIEW.md | both spokes |

## Resumption condition

This node resumes (and folds to COMPLETED) when SUBTASK_synthesis completes and calls
`engine_resume_suspended` with its SYNTHESIS.md at `spoke-ui-states/SYNTHESIS.md` as the
seam path.

## Named state authored

- `spoke-ui-states/_GLOBAL.md` — subtree hub
- `spoke-ui-states/contracts/_MANIFEST.yaml` — structural contract
- `spoke-ui-states/SUBTASK_landing-states/_BRIEF.md`
- `spoke-ui-states/SUBTASK_routing-ctas/_BRIEF.md`
- `spoke-ui-states/SUBTASK_synthesis/_BRIEF.md`
