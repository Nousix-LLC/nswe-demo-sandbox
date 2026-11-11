# Task: Notification preferences screen for chirp (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_notification_prefs
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **Notification preferences** surface — the inventory's `Notification preferences` screen
(`/settings/notifications`, settings archetype, signed-in) — as a designed screen with its layout,
content, and primary action, and its **empty, error, and loading states**, to the bar *designed screens,
not a skeleton*.

### Context
Part of the account-settings subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`notification_preferences` surface and `REQ-UX-072`. This surface lets a signed-in person **choose which
activity categories — replies, follows, likes — send a notification**; a category turned off stops
notifying. It is addressable and returns to the Settings hub, and a preference that takes effect
immediately confirms on its row.

The notifications **activity** surface itself (the `Notifications` list, `/notifications`) is owned by
the sibling `../../../SUBTASK_safety_notifications` — **cross-reference it, do not redesign it**. Compose
against the frozen **screen inventory** and **component library** by name; invent no screen or component
outside them without an additive amendment to `../contracts/`.

J6 / REQ-PROD-017, 029.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surface + id (072), the trace rule (incl. REQ-PROD-029's non-gating staging), shared-vocab rule, the cross-reference to the notifications activity surface, identities. |
| Screen inventory | `../../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The `Notification preferences` screen, the settings-as-secondary-nav and transient-feedback conventions, the Notifications activity entry to cross-reference. |
| Component library | `../../../../SUBTASK_visual_system/outputs/visual-system.md` | The components you assemble this screen from (SettingRow, Toggle [immediate-save, revert-on-failure], InlineFeedback, EmptyState, LoadingState) with their named states. |
| Product requirements | `../../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J6 and REQ-PROD-017/029 this screen serves and traces to. |

### Output
- `outputs/screen-notification-prefs.md` — the Notification preferences screen at wireframe-level detail
  (layout, content, primary action, and empty/error/loading states — including the immediate-save Toggle
  behaviour: confirm on success, revert and report on failure), and a `REQ-UX-072` entry (`statement`,
  testable `acceptance_criteria`, `release_gating` honouring REQ-PROD-029's `false` staging with a
  one-line reason, ≥1 `REQ-PROD-*`). Repository-ready; no host/system/taskflow detail, no workspace
  paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library by name; nothing
      redefined.
- [ ] The screen is designed with layout, content, and a primary action (not a bare route name); lets the
      person choose per-category notification on/off with immediate, confirmed effect; is addressable and
      returns to the hub; cross-references (does not redesign) the notifications activity surface.
- [ ] Empty, error, and loading states are designed (or "does not apply" with a component-matching reason).
- [ ] `REQ-UX-072` is testable on the live product, `release_gating`-flagged (non-gating with its one-line
      reason), unique, in-range (072), and traces to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Product Strategy (support). If the `design` loader is
  unavailable, design from the bundle intent and competence and record the limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist (or the P0/P1 catalog by
  hand when the skill is absent — it is absent here) over the narrative before finalizing, and record the
  limitation.
- Evaluate your own scope against the decomposition triggers at dispatch; this is one surface and is
  expected to be atomic, but the decision is yours to make against your actual brief.
