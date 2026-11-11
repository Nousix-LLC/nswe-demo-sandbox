# Task: Visual language & design system for chirp

## Task Specification
**Slug**: SUBTASK_visual_system
**Task Kind**: standard
**Status**: Pending

### Objective
Design chirp's **visual language and design system**, and publish the canonical **component library**
(component vocabulary) that the screens, responsive, and accessibility work compose against.

### Context
Part of the experience-design subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`visual_language_and_design_system` section of `design/experience-design.md`, the **component library**
shared vocabulary, and `REQ-UX-020..039`. People judge the whole product in the first minute on how it
looks and feels; a consistent visual system is why screens feel like one product rather than many.

**Dependencies**: `SUBTASK_ia_interaction` (compose against its screen inventory/archetypes).
**Dependents**: `SUBTASK_screens_flows`, `SUBTASK_responsive`, `SUBTASK_accessibility`, `SUBTASK_synthesis`.

### Scope — distinct concerns to weigh in your own evaluation
- **Visual language** — typography scale, color palette and theming (incl. light/dark if in scope),
  spacing/layout grid, iconography, imagery/avatars, motion, and the product's tone/voice in UI copy.
- **Component library** — the named, reusable UI components and their behavior and states (at least:
  the chirp card, compose box, primary/secondary buttons, text fields with validation, the navigation
  shell, dialogs/confirmations, toasts/inline feedback, empty-state block, inline error, loading/skeleton
  — extend as the archetypes require). This is the shared vocabulary siblings refer to by name.
- **Design tokens / consistency rules** — how the language is applied consistently (the token set and the
  rules that keep screens coherent), stated as design intent, not code.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Internal contract | `../contracts/` (read-only) | Section ownership, your id range, component-library required shape |
| IA & screen inventory | `../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The screens/archetypes your components must furnish |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | What the product is and must feel like; `REQ-PROD-*` to trace to |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | Current SPA look as the starting point (clone into your own workspace if needed) |

### Methodology
Design-domain bundle: **Experience Design** (primary — visual design & design systems). Load on demand;
if the loader is unavailable, design from bundle intent and competence and record the limitation.

### Output
- `outputs/visual-system.md` — the `visual_language_and_design_system` section content, including a
  clearly-headed **"Component library"** in the shape `../contracts/ux_section_and_id_map.yaml` requires,
  and `REQ-UX-020..039` entries (statement, testable acceptance criteria, `release_gating`, ≥1
  `REQ-PROD-*`). Committed design assets are welcome **only** in a form the repository can hold (e.g.
  markdown + token tables/SVG); do not require tooling the repo cannot keep. Repository-ready; no
  host/system/taskflow detail or attribution.

### Success criteria
- [ ] Composes against `../contracts/` and the screen inventory; uses the `REQ-UX` scheme and your range.
- [ ] A complete, named component library covering every archetype in the inventory, each with its
      states (default/empty/error/loading/disabled as applicable).
- [ ] Typography, color/theme, spacing, iconography, motion, and tone are specified concretely enough to
      build and judge against.
- [ ] Every `REQ-UX-020..039` is testable, release-gating-flagged, and traces to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
