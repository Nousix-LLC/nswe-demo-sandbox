# Task: Component library for chirp

## Task Specification
**Slug**: SUBTASK_component_library
**Task Kind**: standard
**Status**: Pending

### Objective
Design chirp's **component library** — the named, reusable UI components with their behavior and states — and
publish it as the canonical **component vocabulary** the screens, responsive, and accessibility siblings refer
to by name, plus `REQ-UX-033..039`.

### Context
Part of the visual-system subtree (see `../_GLOBAL.md`). You own the **"Component library"** heading content, the
component vocabulary (the shared seam later siblings compose against), and `REQ-UX-033..039`. The component
library is why screens feel like one product and why the unglamorous surfaces (empty, error, loading) are
designed rather than left blank: each component carries its states so every screen inherits them.

Compose against the **design-token vocabulary** your dependency publishes — build each component from token
names (`color.*`, `type.*`, `space.*`, `radius.*`, `elevation.*`, `motion.*`), not ad-hoc values — and against
the **screen inventory and archetypes** so the library furnishes every archetype a releasable chirp needs.

**Dependencies**: `SUBTASK_visual_language` (read its published "Design tokens" set and compose against it).
**Dependents**: `SUBTASK_synthesis`.

### Scope — distinct concerns to weigh in your own evaluation
- **Component vocabulary** — the named components and what each is for. At least the chirp card, compose box,
  primary/secondary buttons, text field with validation, navigation shell, dialog/confirmation, toast/inline
  feedback, empty-state block, inline error, loading/skeleton, and avatar — extended as the IA archetypes
  require (the required floor and the archetype-coverage rule are in `../contracts/visual_system_seam.yaml`).
- **Behavior and states** — for each component, its behavior and its states from {default, empty, error,
  loading, disabled}, recording where a state does not apply.
- **Composition against tokens and archetypes** — each component built from the published token names, and the
  set furnishing every screen archetype in the IA inventory (feed/list, form, profile, settings, modal/dialog,
  confirmation, empty/landing).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene. |
| Internal contract | `../contracts/` (read-only) | The "Component library" required shape, the required-component floor and coverage rule, `REQ-UX-033..039`, identities. |
| Published design tokens | `../SUBTASK_visual_language/outputs/visual-language.md` | The "Design tokens" set to compose against by name. |
| Inherited contracts | `../../contracts/` and `../../../contracts/` (read-only) | `REQ-UX` section list; `REQ-<AREA>-NNN` format + field set. |
| Screen inventory & archetypes | `../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The archetypes/screens the library must furnish; refer to screens by these names. |
| Product requirements | `../../../SUBTASK_product_requirements/outputs/product-requirements.md` | What components serve; `REQ-PROD-*` to trace to. |

### Methodology
Design-domain bundle: **Experience Design** (design systems & component design). The methodology loader is
unavailable in the current reconstructed environment; design from the bundle intent and your product-design
competence and record the limitation — it does not block.

### Output
- `outputs/component-library.md` — the clearly-headed **"Component library"** content in the shape
  `../contracts/visual_system_seam.yaml` requires: every required named component (and any the archetypes add),
  each with its purpose, the tokens it is built from, its behavior, and its states; and `REQ-UX-033..039`
  entries (statement, testable acceptance criteria, `release_gating`, ≥1 `REQ-PROD-*`). Repository-ready: no
  host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the published token set, and the screen inventory; uses the `REQ-UX`
      scheme and your `REQ-UX-033..039` range only.
- [ ] A complete, named component library covering every archetype in the IA inventory and every required named
      component, each with its applicable states (default/empty/error/loading/disabled), each built from token
      names rather than ad-hoc values.
- [ ] Every `REQ-UX-033..039` is testable by a stranger on the live product, `release_gating`-flagged, unique,
      in range, and traces to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Do not mint ids outside `REQ-UX-033..039`; do not redefine the token vocabulary, the `REQ-UX` scheme, or the
  "Component library" required shape. If the token set is inadequate for a component you need, request a plan
  amendment rather than inventing an off-contract value silently.
