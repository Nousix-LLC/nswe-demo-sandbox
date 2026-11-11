# SUSPENSION — SUBTASK_account_lifecycle (NeedsDecompose)

## Status
Suspended pending child-subtree completion. `decompose_evaluation = NeedsDecompose`.

## Why this node decomposed
The brief — design eight account-lifecycle surfaces (onboarding, edit profile, settings hub, account &
contact, notification preferences, sessions & devices, data export, account deletion), each with layout,
content, primary action, and empty/error/loading states, plus `REQ-UX-065..077` — was evaluated against
the decomposition triggers at the evaluation point:

- **Output Size trigger — FIRES.** Eight non-skeletal designed screens, each with three designed states,
  plus thirteen traceable `REQ-UX` entries, is a >400-line deliverable (MUST decompose).
- **Scope-Based trigger (enumerated-concerns rule) — FIRES.** The brief enumerates eight distinct
  surfaces spanning separable concerns (first-run experience, settings information architecture, the
  verified contact/identity, session security, data portability, destructive deletion).
- **Token trigger — cleared** (inputs well under threshold).
- **Single-Responsibility conjunction test — one verb ("design")**, but a cleared test does not cancel a
  fired trigger; the trigger set is a disjunction and two triggers fired.

Per trigger precedence and the asymmetric bias, the verdict is `NeedsDecompose`. The instinct that a
product design is one coherent picture one designer holds carries no weight at this evaluation point, and
"this task is already a spoke" is not evidence of atomicity.

## Children materialized (one _BRIEF.md each, authored before add_task)
| Child task id | Surfaces | REQ-UX | Depends on |
|---|---|---|---|
| `SUBTASK_onboarding_profile` | Onboarding, Edit profile | 065..068 | none |
| `SUBTASK_settings_management` | Settings hub, Account & contact, Notification preferences, Sessions & devices | 069..074 | none |
| `SUBTASK_leaving` | Data export, Account deletion | 075..077 | none |
| `SUBTASK_account_lifecycle/SUBTASK_synthesis` | assemble + verify + fold | (consolidated) | the three spokes |

## Contract authored (required output of the decomposition)
- `_GLOBAL.md` — subtree hub (context, constraints, task tree, identities, outputs).
- `contracts/_MANIFEST.yaml` + `contracts/account_lifecycle_seam.yaml` — surface→owner map, the
  `REQ-UX-065..077` sub-range partition, the shared-vocabulary composition rule, the per-`REQ-UX` trace
  rule, and the identities the synthesis gate asserts. Extends the parent (`../contracts/`) and
  grandparent (`../../contracts/`) seams additively; overrides nothing.

## Resumption condition
All child tasks reach terminal lifecycle state. `SUBTASK_account_lifecycle/SUBTASK_synthesis` authors
`outputs/screens-account-lifecycle.md` (this node's declared deliverable) and `SYNTHESIS.md` at this
node's workspace, and resolves the fold so this node becomes COMPLETED.

## Environment limitation recorded
The Phase-B `design` methodology loader is unavailable in this reconstructed environment (the loader
reports the agent domain unset), and no `avoid-ai-writing` skill / `references/patterns.md` is present.
Per the brief, the decomposition proceeds from the named bundle intent (Experience Design primary;
Identity & Trust, Product Strategy support) and product-design competence; each spoke carries the same
posture and records the limitation. The limitation does not block the work.
