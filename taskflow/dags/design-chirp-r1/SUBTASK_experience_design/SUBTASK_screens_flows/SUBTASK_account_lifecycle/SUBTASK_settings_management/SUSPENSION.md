# SUSPENSION — SUBTASK_settings_management (NeedsDecompose)

## Why this node suspended
The account-settings brief was evaluated against the decomposition triggers and found **not atomic**.
The **Scope-Based** trigger fired by the enumerated-concerns rule — the brief enumerates four distinct
surfaces (Settings hub, Account & contact, Notification preferences, Sessions & devices) that span
separable concerns (settings information architecture / navigation, verified-contact & identity,
notification preferences, session security) — and the **Output-Size** trigger sat at its threshold
(four non-skeletal screens, each with three designed states, plus six traceable `REQ-UX` entries). Per
the kernel's asymmetric bias and trigger precedence, a fired scope trigger governs over any
"one coherent settings cluster" instinct; this node decomposes rather than executing inline.

## What was authored before suspending
- `_GLOBAL.md` — this subtree's hub (context, scope, constraints, Task Summary DAG, contract pointer).
- `contracts/_MANIFEST.yaml` and `contracts/settings_management_seam.yaml` — the internal seam:
  surface→owner map, `REQ-UX-069..074` sub-range partition, shared-vocabulary composition rule,
  per-screen↔global-pattern cross-reference, per-`REQ-UX` trace rule, the hub's sub-section link list,
  and the eight identities the synthesis gate asserts. Extends the ancestor contracts additively.
- One `_BRIEF.md` per child (five).

## Children materialized (via engine_amend_plan add_task)
| Task id | Workspace | Depends on | Owns |
|---|---|---|---|
| `SUBTASK_settings_hub` | `SUBTASK_settings_hub/` | none | Settings hub, `REQ-UX-069` |
| `SUBTASK_account_contact` | `SUBTASK_account_contact/` | none | Account & contact, `REQ-UX-070..071` |
| `SUBTASK_notification_prefs` | `SUBTASK_notification_prefs/` | none | Notification preferences, `REQ-UX-072` |
| `SUBTASK_sessions_devices` | `SUBTASK_sessions_devices/` | none | Sessions & devices, `REQ-UX-073..074` |
| `SUBTASK_settings_management_synthesis` | `SUBTASK_synthesis/` | the four spokes | assembled `outputs/screens-settings-management.md`, consolidated register, `SYNTHESIS.md` |

## Resumption condition
All child tasks reach terminal lifecycle state. The synthesis gate assembles the four screen parts into
`outputs/screens-settings-management.md` (screen-inventory order) with the consolidated `REQ-UX-069..074`
register, asserts the eight identities with recorded evidence, authors `SYNTHESIS.md`, and folds this
node `SUSPENDED → COMPLETED`.

## Note on environment
The Phase-B `design` methodology loader is unavailable in this reconstructed environment
(`agent_domain_unset`); the subtree designs from the named bundle intent (Experience Design primary;
Identity & Trust, Product Strategy support) and competence, and records the limitation. The
`avoid-ai-writing` skill is likewise absent; the P0/P1 machine-writing catalog is applied by hand. Both
limitations are recorded for the spokes and the synthesis gate to carry forward.
