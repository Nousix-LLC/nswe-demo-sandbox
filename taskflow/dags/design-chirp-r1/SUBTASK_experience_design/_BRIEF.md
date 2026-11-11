# Task: User experience & visual design for chirp

## Task Specification
**Slug**: SUBTASK_experience_design
**Task Kind**: standard
**Status**: Pending

### Objective
Design how chirp looks and behaves to a user — the information architecture and interaction, the actual screens
and flows, a visual language and design system, responsive layout, and accessibility — to the bar of
**designed screens, not a bare skeleton**.

### Context
Part of design-chirp-r1 (see `../_GLOBAL.md`, `../contracts/`). You own `design/experience-design.md` and
`REQ-UX-*`. A product with no designed screens has not been designed; people judge the whole product in the
first minute.
**Dependencies**: `SUBTASK_product_requirements`. **Dependents**: `SUBTASK_release_bar` consolidates `REQ-UX-*`.

## Distinct concerns in this task
Evaluate your own scope against these and decompose if warranted:
- **Information architecture & interaction** — the structure of the product and how users move through it.
- **Screens & flows** — sign-up / sign-in / recovery, the core posting & timeline/reading loops, following,
  onboarding, settings, and the **empty / error / loading** states for each (not just the happy path).
- **Visual language & design system** — type, color, spacing, components, consistency.
- **Responsive layout** — behavior across phone and larger screens.
- **Accessibility** — inclusive design to a stated standard.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context/constraints |
| Contract | `../contracts/` (read-only) | `REQ-UX-*` scheme; your file + required sections |
| Product requirements | `../SUBTASK_product_requirements/outputs/product-requirements.md` | Journeys/requirements to design screens for |
| Repo + live product | `Nousix-LLC/nswe-demo` @ `c805525`; live deployment (read-only) | The current SPA/screens as the starting point |

## Methodology
Bundle IDs (Domain Mapping): **Experience Design** (primary — IA & interaction, visual design & design systems,
accessibility); **Product Strategy** and **Identity and Trust** (supporting — so auth screens and journeys
align with the requirements).

## Output
- `SUBTASK_experience_design/outputs/experience-design.md` with the required sections in
  `../contracts/design_artifact_map.yaml` and `REQ-UX-*` ids. Repository-ready content (screen/flow
  descriptions, wireframe-level detail, and/or committed design assets — specify what the bar needs; do not
  require tooling the repo cannot hold).

## Success criteria
- [ ] Composes against `../contracts/`; `REQ-UX-*` used; schema not redefined.
- [ ] Screens & flows cover sign-up/in/recovery, the posting/timeline loops, onboarding, and settings, each
      with empty/error/loading states — designed, not skeletal.
- [ ] A visual language/design system, responsive behavior, and an accessibility standard are stated.
- [ ] Every `REQ-UX-*` has testable acceptance criteria and a release-gating flag; traces to `REQ-PROD-*`.

## Constraints
- Design only — no front-end code; defer implementation to code DAGs.
- Repository-ready hygiene (no host/system/taskflow detail, no attribution trailers).
