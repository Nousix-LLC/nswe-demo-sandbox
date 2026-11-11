# Task: Leaving screens for chirp — data export & account deletion (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_leaving
**Task Kind**: standard
**Status**: Pending

### Objective
Design the two **leaving** surfaces — **Data export** and **Account deletion** — each a designed screen
with its layout, content, and primary action, and **each with its empty, error, and loading states**, to
the bar *designed screens, not a skeleton*. These are the surfaces that let a person take their data and
leave cleanly; their absence is a trust gap, not a missing nicety.

### Context
Part of the account-lifecycle subtree (see `../_GLOBAL.md`, `../contracts/`). You own the `leaving`
surfaces and `REQ-UX-075..077`. You compose against the frozen **screen inventory** and **component
library** (read-only inputs); you do not invent screens or components outside those vocabularies without
an additive amendment to `../contracts/`. These surfaces align with the identity/privacy requirements —
the defined deletion outcome for content and handle — so design *what the person is told and must
confirm*, not the data-removal mechanism (that is the identity/privacy design's).

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Surfaces to design (each with happy path AND empty/error/loading states)
- **Data export** — the IA inventory's `Export your data` screen (`/settings/export`, settings archetype,
  signed-in). Request and obtain one's own data — chirps, profile, follows — in an openable, portable form
  (a file or download readable outside chirp). Design the request, the in-progress/preparing state, and
  obtaining the result (J8 / REQ-PROD-019).
- **Account deletion** — the IA inventory's `Delete account` screen (`/settings/delete`, confirmation
  archetype, signed-in). Delete with a confirmation that **names the consequence**, **states what is and
  is not retained** (per the defined deletion outcome for replied-to/liked chirps and whether the handle
  frees up), and **points to export first** as the chance to keep a copy — proceeding only after explicit
  confirmation, with cancel leaving everything intact (J8 / REQ-PROD-020, 021, 022). Compose with the IA's
  destructive-confirmation convention and the `Dialog` confirmation variant; the sign-out-after-deletion
  return to the signed-out shell is an IA convention to compose with, not redesign.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surfaces + id range, the surface map, shared-vocab rule, trace rule, identities. |
| Screen inventory | `../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The `Export your data` and `Delete account` screens, routes, archetypes, and the destructive-confirmation / confirm-what-is-retained / points-to-export conventions you design into. |
| Component library | `../../../SUBTASK_visual_system/outputs/visual-system.md` | The components (SettingRow, PrimaryButton (danger variant), SecondaryButton, Dialog confirmation variant, TextField, InlineError, InlineFeedback, EmptyState, LoadingState, Toast, …) you assemble these screens from, with their named states. |
| Product requirements | `../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J8 and the `REQ-PROD-*` each screen serves and traces to. |

### Output
- `outputs/screens-leaving.md` — the two screens at wireframe-level detail (each screen's layout, content,
  primary action, and empty/error/loading states), and `REQ-UX-075..077` entries (`statement`, testable
  `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*`). Repository-ready; no host/system/taskflow
  detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- [ ] Data export and Account deletion are each designed with their empty/error/loading states — or
      recorded out-of-scope with a reason.
- [ ] Each screen specifies layout, content, and a primary action — not a bare route name; deletion's
      confirmation names the consequence, states what is/is not retained, and points to export first.
- [ ] Every `REQ-UX-075..077` is testable on the live product, `release_gating`-flagged, unique,
      in-range, and traces to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Identity & Trust, Product Strategy (support). If the `design`
  loader is unavailable, design from the bundle intent and competence and record the limitation (do not
  block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist (or the P0/P1 catalog by
  hand when the skill is absent) over the narrative before finalizing, and record the limitation.
