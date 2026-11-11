# SUSPENSION.md — SUBTASK_domain_app_design (NeedsDecompose)

## Outcome
This node evaluated its brief at dispatch and reached **NeedsDecompose**. It has materialized a child subtree and
suspends pending the subtree's resolution. It executed none of the design work itself; the children produce it and
the synthesis gate folds the result back into this node.

## Why decompose (triggers applied to this brief)
- **Scope / enumerated-concerns**: the brief's `## Distinct concerns in this task` enumerates four distinct areas
  (domain model; modules & responsibilities; persistence & state; interfaces & entry points) — the scope trigger
  fires by that enumeration alone.
- **Output size**: a full `REQ-DOM-*` domain + application design for a Twitter-style product, each requirement
  with testable acceptance criteria, `release_gating`, and `REQ-PROD-*` traces, across model + persistence +
  modules + interfaces, exceeds the 400-line single-task threshold.
- **Token**: inputs sit well under 50% of context — clears (does not override the fired triggers).
- Evaluated independently against this node's own brief, not deferred to the parent's split; the single declared
  output file does not make the task atomic.

## Children materialized (hub-and-spoke, one entity vocabulary, partitioned REQ-DOM-* space)
| Child | Depends on | Owns |
|-------|------------|------|
| `SUBTASK_domain_model` | none | `domain_model` section + `REQ-DOM-001..049` + the canonical entity vocabulary |
| `SUBTASK_persistence_state` | `SUBTASK_domain_model` | `persistence_requirement` section + `REQ-DOM-100..149` (the durable-persistence blocker) |
| `SUBTASK_module_structure` | `SUBTASK_domain_model` | `modules_and_responsibilities` + `interfaces_and_entry_points` + `REQ-DOM-200..249` |
| `SUBTASK_dad_synthesis` (Task Kind: synthesis) | all three above | consolidated `outputs/domain-application-design.md` + `SYNTHESIS.md`; asserts contract identities; folds this node |

Subtree hub: `_GLOBAL.md`. Subtree contract: `contracts/_MANIFEST.yaml` + `contracts/req_dom_partition.yaml`
(extends the inherited `../contracts/`; does not override it).

## Resumption condition
All child tasks reach terminal lifecycle state. `SUBTASK_dad_synthesis` authors `SYNTHESIS.md` at this node's
directory (the fold location) and folds this node `SUSPENDED → COMPLETED` via `engine_resume_suspended`; the
consolidated `outputs/domain-application-design.md` becomes this node's declared output.

## Boot note (reconstructed node)
This invocation ran as a reconstructed taskflow node. The Phase-B `design` methodology loader was unreachable via
syscall (`agent_domain_unset`, empty `agent_id`): the domain binding was not restored on reconstruction. Per the
dispatch-ambiguity rule, the decomposition proceeded on the bundle IDs the brief names (**Product Strategy**,
**Release Definition**), propagated to each child brief for the executing child to load on demand once its domain
binding resolves. No child's correctness depends on this node having loaded bundle bodies; the decomposition,
contract, and briefs stand on the inherited contracts and the brief.
