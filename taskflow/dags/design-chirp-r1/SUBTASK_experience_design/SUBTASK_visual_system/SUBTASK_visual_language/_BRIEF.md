# Task: Visual language & design tokens for chirp

## Task Specification
**Slug**: SUBTASK_visual_language
**Task Kind**: standard
**Status**: Pending

### Objective
Design chirp's **visual language** and the named **design-token set** that makes it consistent, and write the
`visual_language_and_design_system` section body of the experience design, plus `REQ-UX-020..032`.

### Context
Part of the visual-system subtree (see `../_GLOBAL.md`). You own the `visual_language_and_design_system` section
body, the **design-token vocabulary** (the shared seam the component library composes against), and
`REQ-UX-020..032`. People judge the whole product in the first minute on how it looks and feels; a coherent
visual language and a token set that keeps every screen consistent is why chirp's many screens read as one
product rather than many.

chirp is a hosted, public, Twitter-style consumer web app, today a WebAssembly SPA of three screens above a nav
bar; the experience design takes it to a designed, releasable product. Design the visual language so it serves
that product — readable at a glance, calm enough to live in daily, and trustworthy on first sight.

**Dependencies**: none.
**Dependents**: `SUBTASK_component_library` (composes against your published token vocabulary),
`SUBTASK_synthesis`.

### Scope — distinct concerns to weigh in your own evaluation
- **Visual language** — typography (families/roles and a type scale), color (palette and semantic roles with a
  light theme and a dark theme), spacing and the layout grid, corner radii, elevation, iconography,
  imagery/avatars, motion, and the product's tone/voice in UI copy.
- **Design tokens** — a named token set (`color.*`, `type.*`, `space.*`, `radius.*`, `elevation.*`, `motion.*`)
  published under a clearly-labelled **"Design tokens"** heading in the shape `../contracts/visual_system_seam.yaml`
  requires, stated as design intent (not code), concrete enough to build to and to check against.
- **Consistency rules** — the rules that keep screens coherent (how the tokens are applied; what makes two
  screens feel like one product).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene. |
| Internal contract | `../contracts/` (read-only) | Your section/fragment, `REQ-UX-020..032`, the required token-vocabulary shape, identities. |
| Inherited contracts | `../../contracts/` and `../../../contracts/` (read-only) | `REQ-UX` section list; `REQ-<AREA>-NNN` format + field set. |
| Screen inventory & archetypes | `../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The archetypes and screens the language must serve. |
| Product requirements | `../../../SUBTASK_product_requirements/outputs/product-requirements.md` | What the product is and must feel like; `REQ-PROD-*` to trace to. |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | The current SPA look as the starting point; clone into your own workspace if you want a working tree. |

### Methodology
Design-domain bundle: **Experience Design** (visual design & design systems). The methodology loader is
unavailable in the current reconstructed environment; design from the bundle intent and your product-design
competence and record the limitation — it does not block.

### Output
- `outputs/visual-language.md` — the `visual_language_and_design_system` section body (typography, color +
  theming, spacing/grid, radii, elevation, iconography, imagery/avatars, motion, tone/voice), the clearly-headed
  **"Design tokens"** set in the required shape, the consistency rules, and `REQ-UX-020..032` entries (statement,
  testable acceptance criteria, `release_gating`, ≥1 `REQ-PROD-*`). Committed design assets are welcome only in a
  form the repository can hold (markdown + token tables/SVG); do not require tooling the repo cannot keep.
  Repository-ready: no host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`; uses the `REQ-UX` scheme and your `REQ-UX-020..032` range only.
- [ ] Typography, color/theme (light + dark), spacing, radii, elevation, iconography, imagery/avatars, motion,
      and tone are specified concretely enough to build and judge against.
- [ ] A named token set is published under a "Design tokens" heading in the required shape, with every required
      family present; it is the vocabulary a component references by name.
- [ ] Every `REQ-UX-020..032` is testable by a stranger on the live product, `release_gating`-flagged, unique,
      in range, and traces to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Do not mint ids outside `REQ-UX-020..032`; do not redefine any inherited scheme, section list, or token shape.
