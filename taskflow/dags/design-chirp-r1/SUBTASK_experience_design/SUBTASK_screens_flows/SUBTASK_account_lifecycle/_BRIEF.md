# Task: Account-lifecycle screens for chirp (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_account_lifecycle
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **account-lifecycle surfaces** that make the account feel like the person's own — first-run
onboarding off the empty state, editing the profile, the settings hub and its sub-sections, exporting
one's data, and deleting the account with a confirmed, explained outcome — each a designed screen with
its layout, content, and primary action, and **each with its empty, error, and loading states**, to the
bar of *designed screens, not a skeleton*.

### Context
Part of the screens-&-flows subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
**account_lifecycle** part of the `screens_and_flows` section and `REQ-UX-065..077`. You compose against
the frozen **screen inventory** and **component library**; you do not invent screens or components
outside those vocabularies without an additive amendment to `../contracts/`. These are the "unglamorous"
surfaces a releasable account-based product is expected to have — onboarding, settings, export, deletion
— and their absence is the gap this design closes. Align them with the identity requirements (the
verified contact, session/device management, the defined deletion outcome).

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Scope — distinct surfaces to weigh in your own evaluation
This brief covers **many distinct screens/flows**; evaluate your own scope against the decomposition
triggers and decompose if warranted. Each surface is designed with its happy path **and** its empty /
error / loading states, and each maps to its journey and `REQ-PROD-*`:
- **Onboarding** — first-run off the empty timeline: explain the empty state and offer at least one route
  to a non-empty one (find people, first post) (J5 / REQ-PROD-032).
- **Edit profile** — change display name and bio after sign-up (J6 / REQ-PROD-016).
- **Settings hub** — the grouped settings surface listing its sub-sections, each addressable and
  returnable (J6 / REQ-PROD-017).
- **Account & contact** — view/update the verified contact; the stated handle-change position (J6 /
  REQ-PROD-017, 018).
- **Notification preferences** — choose which activity categories notify (settings sub-section; the
  activity surface itself is owned by `SUBTASK_safety_notifications` — cross-reference, do not redesign
  it) (J6 / REQ-PROD-017, 029).
- **Sessions & devices** — view active sessions/devices, end a session, sign out (J6 / REQ-PROD-017, 014).
- **Data export** — request and obtain one's own data (chirps, profile, follows) in a portable form (J8 /
  REQ-PROD-019).
- **Account deletion** — delete with a confirmation that names the consequence, states what is/is not
  retained, and points to export first (J8 / REQ-PROD-020, 021, 022).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your section-part + id range, the surface map, the shared-vocab rule, the trace rule, identities. |
| Screen inventory | `../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The settings/form/confirmation screens, routes, and the settings-as-secondary-nav and destructive-confirmation conventions you design into. |
| Component library | `../../SUBTASK_visual_system/outputs/visual-system.md` | The components (SettingRow, Toggle, TextField, Dialog confirmation variant, EmptyState, LoadingState, …) you assemble these screens from. |
| Product requirements | `../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journeys J5, J6, J8 and the `REQ-PROD-*` each screen serves and traces to. |

### Output
- `outputs/screens-account-lifecycle.md` — the **account_lifecycle** screens/flows at wireframe-level
  detail (each screen's layout, content, primary action, and empty/error/loading states), and
  `REQ-UX-065..077` entries (`statement`, testable `acceptance_criteria`, `release_gating`, ≥1
  `REQ-PROD-*`). Repository-ready; no host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- [ ] Onboarding, edit profile, settings hub, account & contact, notification preferences, sessions &
      devices, export, and deletion are each designed with their empty/error/loading states — or recorded
      out-of-scope with a reason.
- [ ] Each screen specifies layout, content, and a primary action — not a bare route name.
- [ ] Every `REQ-UX-065..077` is testable, `release_gating`-flagged, unique, in-range, and traces to ≥1
      `REQ-PROD-*` (honouring REQ-PROD-018/029's non-gating staging where it applies).

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Identity & Trust, Product Strategy (support). Load bundle
  bodies on demand; if the `design` loader is unavailable, design from the bundle intent and competence
  and record the limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist over the narrative before
  finalizing.
