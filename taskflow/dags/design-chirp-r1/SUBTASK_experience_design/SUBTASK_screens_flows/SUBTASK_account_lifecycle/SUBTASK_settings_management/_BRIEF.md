# Task: Account-settings screens for chirp (hub + sub-sections, with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_settings_management
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **account-settings** surfaces — the settings hub and three management sub-sections — each a
designed screen with its layout, content, and primary action, and **each with its empty, error, and
loading states**, to the bar *designed screens, not a skeleton*.

### Context
Part of the account-lifecycle subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`settings_management` surfaces and `REQ-UX-069..074`. You compose against the frozen **screen inventory**
and **component library** (read-only inputs); you do not invent screens or components outside those
vocabularies without an additive amendment to `../contracts/`. These surfaces align with the identity
requirements — the verified contact and sign-out that ends the session — so design *what the person can
see and do*, not the credential/session mechanism (that is the identity design's).

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Surfaces to design — these are distinct surfaces; evaluate your own scope against the decomposition triggers and decompose if warranted
Each surface is designed with its happy path AND its empty/error/loading states, and each maps to its
journey and `REQ-PROD`:
- **Settings hub** — the IA inventory's `Settings` screen (`/settings`, settings archetype, signed-in).
  The grouped surface that lists every sub-section (edit profile, account & contact, notification
  preferences, sessions & devices, blocked & muted, export, delete), each independently addressable and
  each returning to the hub (J6 / REQ-PROD-017). It LINKS to sub-sections owned by sibling spokes/subtrees
  (edit profile; blocked & muted; export; delete) — list them; do not design their contents here.
- **Account & contact** — the IA inventory's `Account & contact` screen (`/settings/account`, settings
  archetype, signed-in). View and update the verified point of contact (with the control-you-own
  verification step), and state the product's handle-change position (J6 / REQ-PROD-017, 018, 012).
- **Notification preferences** — the IA inventory's `Notification preferences` screen
  (`/settings/notifications`, settings archetype, signed-in). Choose which activity categories (replies,
  follows, likes) send a notification (J6 / REQ-PROD-017, 029). The notifications *activity surface*
  itself is owned by `../../SUBTASK_safety_notifications` — cross-reference it; do not redesign it.
- **Sessions & devices** — the IA inventory's `Sessions & devices` screen (`/settings/sessions`, settings
  archetype, signed-in). View active sessions/devices, end a session on another device (a confirmed,
  destructive action), and sign out — the session end being server-side (J6 / REQ-PROD-017, 014).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surfaces + id range, the surface map, shared-vocab rule, trace rule, identities. |
| Screen inventory | `../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The settings screens/routes/archetypes, the settings-as-secondary-nav convention, the destructive-confirmation convention, and the sign-out transition you design into. |
| Component library | `../../../SUBTASK_visual_system/outputs/visual-system.md` | The components (SettingRow, Toggle, TextField, PrimaryButton, SecondaryButton, IconButton, Dialog confirmation variant, ListView, InlineFeedback, InlineError, EmptyState, LoadingState, Toast, …) you assemble these screens from, with their named states. |
| Product requirements | `../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journeys J6 and the `REQ-PROD-*` each screen serves and traces to. |

### Output
- `outputs/screens-settings-management.md` — the four screens at wireframe-level detail (each screen's
  layout, content, primary action, and empty/error/loading states), and `REQ-UX-069..074` entries
  (`statement`, testable `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*`, honouring
  REQ-PROD-018/029's non-gating staging where it applies). Repository-ready; no host/system/taskflow
  detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- [ ] Settings hub, Account & contact, Notification preferences, and Sessions & devices are each designed
      with their empty/error/loading states — or recorded out-of-scope with a reason.
- [ ] Each screen specifies layout, content, and a primary action — not a bare route name; each sub-section
      is addressable and returns to the hub.
- [ ] Every `REQ-UX-069..074` is testable on the live product, `release_gating`-flagged, unique,
      in-range, and traces to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Identity & Trust, Product Strategy (support). If the `design`
  loader is unavailable, design from the bundle intent and competence and record the limitation (do not
  block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist (or the P0/P1 catalog by
  hand when the skill is absent) over the narrative before finalizing, and record the limitation.
