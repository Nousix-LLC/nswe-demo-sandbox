# Task: Settings hub screen for chirp (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_settings_hub
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **Settings hub** — the inventory's `Settings` screen (`/settings`, settings archetype,
signed-in) — as a designed screen with its layout, content, and primary action, and its **empty, error,
and loading states**, to the bar *designed screens, not a skeleton*.

### Context
Part of the account-settings subtree (see `../_GLOBAL.md`, `../contracts/`). You own the `settings_hub`
surface and `REQ-UX-069`. The Settings hub is the grouped secondary-navigation surface that lists every
settings sub-section, each independently addressable (openable by its own URL) and each returning to the
hub (the settings-as-secondary-nav convention, REQ-UX-017). Compose against the frozen **screen
inventory** and **component library** by name; do not invent screens or components outside those
vocabularies without an additive amendment to `../contracts/`.

The hub **lists** these sub-sections and links to each — but designs none of their contents:
- designed within this subtree by sibling spokes: **Account & contact**, **Notification preferences**,
  **Sessions & devices**;
- owned elsewhere (link by inventory name/route only): **Edit profile** (`/settings/profile`),
  **Blocked & muted** (`/settings/blocks`), **Export your data** (`/settings/export`), **Delete account**
  (`/settings/delete`). The Delete account row is the destructive one (`color.danger` label, routes to a
  confirmation) — list and style it as such; its confirmation is designed by the owning spoke, not here.

J6 / REQ-PROD-017.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surface + id (069), the surface map, the sub-section link list, shared-vocab rule, trace rule, identities. |
| Screen inventory | `../../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The `Settings` screen, the full settings sub-section list, the settings-as-secondary-nav and wayfinding conventions. |
| Component library | `../../../../SUBTASK_visual_system/outputs/visual-system.md` | The components you assemble the hub from (NavShell signed-in, SettingRow, IconButton chevron, EmptyState, LoadingState, InlineError, …) with their named states. |
| Product requirements | `../../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J6 and REQ-PROD-017 this screen serves and traces to. |

### Output
- `outputs/screen-settings-hub.md` — the Settings hub at wireframe-level detail (layout, content, primary
  action, and empty/error/loading states — recording a state "does not apply" with a reason only where
  the composed component itself records it so), and a `REQ-UX-069` entry (`statement`, testable
  `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*`). Repository-ready; no host/system/taskflow
  detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library by name; nothing
      redefined.
- [ ] The hub is designed with layout, content, and a primary action (not a bare route name), lists every
      settings sub-section with each addressable and returning to the hub, and links to — without
      designing — the sub-sections owned elsewhere.
- [ ] Empty, error, and loading states are designed (or "does not apply" with a component-matching reason).
- [ ] `REQ-UX-069` is testable on the live product, `release_gating`-flagged, unique, in-range (069), and
      traces to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Product Strategy (support). If the `design` loader is
  unavailable, design from the bundle intent and competence and record the limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist (or the P0/P1 catalog by
  hand when the skill is absent — it is absent here) over the narrative before finalizing, and record the
  limitation.
- Evaluate your own scope against the decomposition triggers at dispatch; this is one surface and is
  expected to be atomic, but the decision is yours to make against your actual brief.
