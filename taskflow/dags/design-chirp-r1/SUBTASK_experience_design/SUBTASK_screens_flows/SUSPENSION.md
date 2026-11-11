# SUSPENSION.md — SUBTASK_screens_flows (decomposition suspension)

## Status
**Suspended — NeedsDecompose.** This node evaluated its brief against the decomposition triggers and
decomposed into a five-spoke-plus-synthesis subtree. It remains SUSPENDED until its subtree resolves to
terminal states; `SUBTASK_synthesis` folds it to COMPLETED via the synthesis fold.

## Why decomposition (trigger evidence)
The brief covers many distinct surfaces — the entry/authentication flows, the core social loop, the
account-lifecycle surfaces, the safety/notifications surfaces, and a cross-cutting empty/error/loading
pattern section. Applied at the evaluation point:
- **Scope-Based trigger — FIRED** via the enumerated-concerns rule (the brief enumerates ~22 distinct
  screens/flows across clear clusters, and invites decomposition explicitly).
- **Distinct Concerns Test — FAILED** (the clusters could be designed by different specialists in
  parallel, each composing against the already-frozen screen inventory and component library).
- **Single-Responsibility Test — FAILED** (the faithful description joins many distinct responsibilities).
- **Output Size trigger — FIRED** (~22 screens × layout/content/action + three states + 50 requirements
  far exceeds 400 lines).
- **Token trigger** — moderate, not decisive. **Trigger Precedence:** the single declared output file
  does not override the fired scope/concern signals.

The coherence a single author would give the document is preserved structurally: the shared vocabularies
are frozen upstream, and `SUBTASK_synthesis` assembles the one `screens-flows.md`, consolidates
`REQ-UX-040..089`, and verifies cross-screen consistency.

## Children materialized
| Child | Role | REQ-UX | Output |
|---|---|---|---|
| `SUBTASK_get_in` | Entry & authentication screens | 040..050 | `SUBTASK_get_in/outputs/screens-get-in.md` |
| `SUBTASK_core_loop` | Core social-loop screens | 051..064 | `SUBTASK_core_loop/outputs/screens-core-loop.md` |
| `SUBTASK_account_lifecycle` | Onboarding, management, leaving | 065..077 | `SUBTASK_account_lifecycle/outputs/screens-account-lifecycle.md` |
| `SUBTASK_safety_notifications` | Safety, notifications, public-explanatory | 078..085 | `SUBTASK_safety_notifications/outputs/screens-safety-notifications.md` |
| `SUBTASK_considered_states` | The empty_error_loading_states section | 086..089 | `SUBTASK_considered_states/outputs/empty-error-loading-states.md` |
| `SUBTASK_screens_flows_synthesis` (workspace dir `SUBTASK_synthesis/`) | Assemble, verify, fold | (consolidates) | `outputs/screens-flows.md` + `SYNTHESIS.md` |

## Resumption condition
All child tasks reach terminal lifecycle state; `SUBTASK_synthesis` authors `SYNTHESIS.md` at this node's
workspace and folds `SUBTASK_screens_flows` SUSPENDED → COMPLETED.

## Co-designed outputs of this decomposition
- Task tree: the hub `_GLOBAL.md` (Task Summary table is authoritative).
- Contract: `contracts/_MANIFEST.yaml` + `contracts/screens_seam.yaml` (section/surface ownership,
  `REQ-UX-040..089` sub-ranges, shared-vocabulary and states-consistency rules, identities).
