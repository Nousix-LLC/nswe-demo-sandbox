# Task: Safety, notifications & public-explanatory screens for chirp (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_safety_notifications
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **safety, notifications, and public-explanatory surfaces** a releasable public social product
needs — the notifications activity surface, reporting content/accounts, blocking/muting and managing the
blocked-&-muted list, the user-facing help/support entry, the rules & terms screen, and the not-found
screen — each a designed screen with its layout, content, and primary action, and **each with its empty,
error, and loading states**, to the bar of *designed screens, not a skeleton*.

### Context
Part of the screens-&-flows subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
**safety_notifications** part of the `screens_and_flows` section and `REQ-UX-078..085`. You compose
against the frozen **screen inventory** and **component library**; you do not invent screens or
components outside those vocabularies without an additive amendment to `../contracts/`. For a space where
strangers post at each other, the absence of any way to report, block, or get help is a releasability
concern — these surfaces make it feel minded. The notification **preferences** settings sub-section is
owned by `SUBTASK_account_lifecycle`; cross-reference it (which categories notify), do not redesign it.
The operator/moderation tooling is the OPS area — design only the user-facing help/support **entry**.

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Scope — distinct surfaces to weigh in your own evaluation
This brief covers **several distinct screens/flows**; evaluate your own scope against the decomposition
triggers and decompose if warranted. Each surface is designed with its happy path **and** its empty /
error / loading states, and each maps to its journey and `REQ-PROD-*`:
- **Notifications** — the activity surface (replies, follows, likes) with the unseen-activity indicator
  and its cleared state (J7 / REQ-PROD-029).
- **Report** — the report dialog on a chirp or account, with the receipt acknowledgement (J7 /
  REQ-PROD-025, 026).
- **Block / mute** — the block-or-mute confirmation stating the effect (J7 / REQ-PROD-027).
- **Blocked & muted** — the settings screen managing the accounts the person has blocked or muted
  (J7 / REQ-PROD-027).
- **Help & support** — the user-facing entry to recovery, reporting, and contacting the operator (J9
  entry only / REQ-PROD-028).
- **Rules & terms** — the stated rules a report references (J7 / REQ-PROD-026).
- **Not found** — the screen for an unresolved/removed resource that routes back to a known place.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your section-part + id range, the surface map, the shared-vocab rule, the trace rule, identities. |
| Screen inventory | `../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The feed/list, dialog, confirmation, and empty/landing screens, routes, and conventions you design into. |
| Component library | `../../SUBTASK_visual_system/outputs/visual-system.md` | The components (ListView, Dialog modal + confirmation variants, SettingRow, Toast, EmptyState, LoadingState, …) you assemble these screens from. |
| Product requirements | `../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journeys J7 and the user-facing part of J9 and the `REQ-PROD-*` each screen serves and traces to. |

### Output
- `outputs/screens-safety-notifications.md` — the **safety_notifications** screens/flows at
  wireframe-level detail (each screen's layout, content, primary action, and empty/error/loading
  states), and `REQ-UX-078..085` entries (`statement`, testable `acceptance_criteria`, `release_gating`,
  ≥1 `REQ-PROD-*`). Repository-ready; no host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- [ ] Notifications, report, block/mute, blocked & muted, help/support entry, rules & terms, and
      not-found are each designed with their empty/error/loading states — or recorded out-of-scope with a
      reason.
- [ ] Each screen specifies layout, content, and a primary action — not a bare route name.
- [ ] Every `REQ-UX-078..085` is testable, `release_gating`-flagged, unique, in-range, and traces to ≥1
      `REQ-PROD-*` (honouring REQ-PROD-029/027's non-gating staging where it applies).

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Identity & Trust, Product Strategy (support). Load bundle
  bodies on demand; if the `design` loader is unavailable, design from the bundle intent and competence
  and record the limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist over the narrative before
  finalizing.
