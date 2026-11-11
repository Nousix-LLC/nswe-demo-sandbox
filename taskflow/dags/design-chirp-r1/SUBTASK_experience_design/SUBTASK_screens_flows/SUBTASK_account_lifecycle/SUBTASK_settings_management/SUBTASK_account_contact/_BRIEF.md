# Task: Account & contact screen for chirp (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_account_contact
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **Account & contact** surface — the inventory's `Account & contact` screen
(`/settings/account`, settings archetype, signed-in) — as a designed screen with its layout, content,
and primary action, and its **empty, error, and loading states**, to the bar *designed screens, not a
skeleton*.

### Context
Part of the account-settings subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`account_and_contact` surface and `REQ-UX-070..071`. This surface lets a signed-in person **view and
update their verified point of contact** — including the control-you-own verification step that confirms
the person controls the contact before the product relies on it — and **states the product's
handle-change position**. It is addressable and returns to the Settings hub.

Design *what the person can see and do*: the contact shown with its verification status (an unverified
contact reads as a caution, not an error), the field to change it, the action to re-verify, and the
plainly-stated handle position. Do **not** design the verification/credential/session mechanism — that is
the identity design's `REQ-ID-*`. Compose against the frozen **screen inventory** and **component
library** by name; invent no screen or component outside them without an additive amendment to
`../contracts/`.

J6 / REQ-PROD-017, 012 (verified contact), 018 (handle-change position).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surface + ids (070–071), the trace rule (incl. REQ-PROD-018's non-gating staging), shared-vocab rule, identities. |
| Screen inventory | `../../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The `Account & contact` screen, the settings-as-secondary-nav and transient-feedback conventions. |
| Component library | `../../../../SUBTASK_visual_system/outputs/visual-system.md` | The components you assemble this screen from (SettingRow, TextField, PrimaryButton, InlineFeedback, InlineError, EmptyState, LoadingState, Toast; the `color.warning` unverified-contact treatment) with their named states. |
| Product requirements | `../../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J6 and REQ-PROD-012/017/018 this screen serves and traces to. |

### Output
- `outputs/screen-account-contact.md` — the Account & contact screen at wireframe-level detail (layout,
  content, primary action, and empty/error/loading states), and `REQ-UX-070..071` entries (`statement`,
  testable `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*` each). Give the verified-contact
  view/update + verification its own gated requirement; give the handle-change position its own
  requirement honouring REQ-PROD-018's `release_gating:false` (a first release may state handles as
  fixed, provided the position is stated). Repository-ready; no host/system/taskflow detail, no workspace
  paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library by name; nothing
      redefined.
- [ ] The screen is designed with layout, content, and a primary action (not a bare route name); shows
      and lets the person update the verified contact with its verification step and verification status,
      and states the handle-change position; is addressable and returns to the hub.
- [ ] Empty, error, and loading states are designed (or "does not apply" with a component-matching reason).
- [ ] Designs user-visible behaviour only — not the verification/credential mechanism.
- [ ] `REQ-UX-070` and `REQ-UX-071` are each testable on the live product, `release_gating`-flagged
      (071 non-gating with its one-line reason), unique, in-range (070–071), and trace to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Identity & Trust, Product Strategy (support). If the `design`
  loader is unavailable, design from the bundle intent and competence and record the limitation (do not
  block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist (or the P0/P1 catalog by
  hand when the skill is absent — it is absent here) over the narrative before finalizing, and record the
  limitation.
- Evaluate your own scope against the decomposition triggers at dispatch; this is one surface and is
  expected to be atomic, but the decision is yours to make against your actual brief.
