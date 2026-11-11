# Task: Accessibility for chirp

## Task Specification
**Slug**: SUBTASK_accessibility
**Task Kind**: standard
**Status**: Pending

### Objective
Set chirp's **accessibility standard** — a named, versioned conformance target — and design to it, so the
product is usable with assistive technology to a stated baseline (REQ-PROD-036).

### Context
Part of the experience-design subtree (see `../_GLOBAL.md`, `../contracts/`). You own the `accessibility`
section of `design/experience-design.md` and `REQ-UX-100..119`. Accessibility is part of whether people
can trust and use the product, not a decoration added at the end; you design it across the screen
archetypes and components the siblings produce.

**Dependencies**: `SUBTASK_ia_interaction`, `SUBTASK_visual_system`. **Dependents**: `SUBTASK_synthesis`.

### Scope
- **The standard**: name the exact target (a specific WCAG version and level) and say what it commits the
  product to; this is the baseline the rest of the design is held to.
- **Operability**: keyboard operability and focus order/visible focus across the archetypes and the nav
  shell; no keyboard trap; skip-to-content.
- **Semantics**: accessible names, roles, and states for the components in the library; landmark/heading
  structure.
- **Perception**: color-contrast rules against the design system's palette; text resizing; reduced-motion.
- **Feedback & errors**: how errors, empty states, loading, and status changes are announced to assistive
  technology (the accessible counterpart of the considered-states work).
- **Verification**: how conformance is checked (the acceptance criteria a tester exercises).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Internal contract | `../contracts/` (read-only) | Section ownership, your id range, trace rule |
| IA & screen inventory | `../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The archetypes/nav you apply a11y to |
| Component library | `../SUBTASK_visual_system/outputs/visual-system.md` | The components whose names/roles/states you specify; the palette you set contrast against |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | REQ-PROD-036 (a11y baseline) + the core loop to trace to |

### Methodology
Design-domain bundle: **Experience Design** (primary — accessibility). Prefer citing the actual standard
(WCAG) over asserting best practice. Load on demand; if the loader is unavailable, design from bundle
intent and competence and record the limitation.

### Output
- `outputs/accessibility.md` — the `accessibility` section content and `REQ-UX-100..119` entries
  (statement, testable acceptance criteria, `release_gating`, ≥1 `REQ-PROD-*`). Repository-ready; no
  host/system/taskflow detail or attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library.
- [ ] A specific, versioned accessibility standard is named, and operability/semantics/perception/
      feedback are designed against it across archetypes and components.
- [ ] Every `REQ-UX-100..119` is testable (a tester can exercise it), release-gating-flagged, and traces
      to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
