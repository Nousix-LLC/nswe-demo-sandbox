# SUSPENSION — SUBTASK_async_forms_events (NeedsDecompose)

## Why suspended
Concern 4 (async resources, forms, full DOM event coverage) decomposed into a subtree. This task is
SUSPENDED pending its child subtree reaching terminal state, then folds to COMPLETED via the synthesis
child's `engine_resume_suspended`.

## Decompose evaluation (mechanical, per TASK_DECOMPOSITION_FRAMEWORK.md)
- **Scope-Based trigger — FIRED.** The brief enumerates three distinct capabilities (async resources +
  suspense; forms + two-way binding; full DOM event coverage). Per the Enumerated-concerns rule, the
  Scope trigger and the Distinct Concerns Test fire by that enumeration alone.
- **Single-Responsibility Test — FIRED.** A faithful description joins three distinct design areas with
  "and"; three kinds of design output.
- **Output-Size / Token — clear, but subordinate.** One declared file (`async-forms-events.md`) and one
  `REQ-ASYNC-*` register are the weakest signal and, per Trigger Precedence, do NOT cancel the fired
  Scope trigger ("N distinct concerns writing into 1 file is still N concerns").
- **Verdict: NeedsDecompose.** The shared event-payload seam between forms and events is handled by the
  sub-contract (freeze the seam), not by collapsing the concerns into one task.

## Children materialized (recursive-depth placement = this task)
| Child | Owns | Output | Depends on |
|---|---|---|---|
| `SUBTASK_afe_async_resources` | REQ-ASYNC-001..019 | `async-resources.md` | none |
| `SUBTASK_afe_events_payloads` | REQ-ASYNC-020..039 + event-payload seam | `events-and-payloads.md` | none |
| `SUBTASK_afe_forms_binding` | REQ-ASYNC-040..059 | `forms-binding.md` | `SUBTASK_afe_events_payloads` |
| `SUBTASK_afe_synthesis` (synthesis gate) | assembly + J1–J7 | `../async-forms-events.md`, `../SYNTHESIS.md` | all three above |

## Named state authored before this suspension
- `_GLOBAL.md` (subtree hub) at this workspace.
- `contracts/_MANIFEST.yaml` (sub-contract: REQ-ASYNC sub-partition + event-payload seam + J1–J7),
  additive over the parent contract.
- One `_BRIEF.md` per child at each child's workspace.

## Resumption condition
All child tasks reach terminal state; `SUBTASK_afe_synthesis` folds this parent SUSPENDED → COMPLETED by
authoring `../SYNTHESIS.md` and `../async-forms-events.md` and calling `engine_resume_suspended`.

## Environment note
Phase B methodology access (`engine_methodology_glob` / `engine_load_methodology`) returned
`agent_domain_unset` for this invocation; the subtree hub confirms no methodology is named by the fork or
the brief and each child selects its own. Decomposition proceeded on the brief, hub, inherited contract,
and the grounded Ferric baseline source.
