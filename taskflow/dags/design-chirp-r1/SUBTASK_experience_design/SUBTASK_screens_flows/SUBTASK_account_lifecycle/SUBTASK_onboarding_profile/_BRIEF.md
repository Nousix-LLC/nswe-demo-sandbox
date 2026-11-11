# Task: Onboarding & edit-profile screens for chirp (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_onboarding_profile
**Task Kind**: standard
**Status**: Pending

### Objective
Design the two first-run / self-presentation account surfaces — **Onboarding** and **Edit profile** — each
a designed screen with its layout, content, and primary action, and **each with its empty, error, and
loading states**, to the bar *designed screens, not a skeleton*.

### Context
Part of the account-lifecycle subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`onboarding_profile` surfaces and `REQ-UX-065..068`. You compose against the frozen **screen inventory**
and **component library** (read-only inputs); you do not invent screens or components outside those
vocabularies without an additive amendment to `../contracts/`.

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Surfaces to design (each with happy path AND empty/error/loading states)
- **Onboarding** — the IA inventory's `Onboarding` screen (`/welcome`, empty/landing archetype,
  signed-in). First run straight after sign-up, when the timeline is empty: explain the empty state and
  offer **at least one route to a non-empty one** (find people to follow, write a first post), rather than
  dropping the new account on a blank page (J5 / REQ-PROD-032). Note the sign-up→onboarding landing is an
  IA convention (REQ-UX-014) — compose with it; do not redesign sign-up.
- **Edit profile** — the IA inventory's `Edit profile` screen (`/settings/profile`, form archetype,
  signed-in). Change display name and bio after sign-up, persisting so the change shows on the profile on
  the next view (J6 / REQ-PROD-016). It is a settings sub-section reachable from the settings hub (owned
  by a sibling spoke) and from the own-profile "Edit profile" action — reference those entries; do not
  design the hub here.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surfaces + id range, the surface map, shared-vocab rule, trace rule, identities. |
| Screen inventory | `../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The `Onboarding` and `Edit profile` screens, routes, archetypes, auth states, and the sign-up→onboarding / return-to-hub conventions you design into. |
| Component library | `../../../SUBTASK_visual_system/outputs/visual-system.md` | The components (EmptyState, TextField, PrimaryButton, SecondaryButton, ProfileHeader, Avatar, ListView, InlineError, LoadingState, Toast, …) you assemble these screens from, with their named states. |
| Product requirements | `../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journeys J5, J6 and the `REQ-PROD-*` each screen serves and traces to. |

### Output
- `outputs/screens-onboarding-profile.md` — the two screens at wireframe-level detail (each screen's
  layout, content, primary action, and empty/error/loading states), and `REQ-UX-065..068` entries
  (`statement`, testable `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*`). Repository-ready; no
  host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- [ ] Onboarding and Edit profile are each designed with their empty/error/loading states — or recorded
      out-of-scope with a reason.
- [ ] Each screen specifies layout, content, and a primary action — not a bare route name.
- [ ] Every `REQ-UX-065..068` is testable on the live product, `release_gating`-flagged, unique,
      in-range, and traces to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Product Strategy, Identity & Trust (support). If the `design`
  loader is unavailable, design from the bundle intent and competence and record the limitation (do not
  block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist (or the P0/P1 catalog by
  hand when the skill is absent) over the narrative before finalizing, and record the limitation.
