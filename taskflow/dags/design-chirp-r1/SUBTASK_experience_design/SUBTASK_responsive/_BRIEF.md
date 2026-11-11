# Task: Responsive layout for chirp

## Task Specification
**Slug**: SUBTASK_responsive
**Task Kind**: standard
**Status**: Pending

### Objective
Design chirp's **responsive behavior** — how the product works and adapts across viewports, from a phone
browser up to larger screens — so the core loop is fully usable on a phone (REQ-PROD-035).

### Context
Part of the experience-design subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`responsive_layout` section of `design/experience-design.md` and `REQ-UX-090..099`. You design responsive
rules for the screen archetypes in the IA inventory and the components in the design system, not a new
screen set.

**Dependencies**: `SUBTASK_ia_interaction`, `SUBTASK_visual_system`. **Dependents**: `SUBTASK_synthesis`.

### Scope
- Breakpoints and the layout strategy (phone-first), stated as design intent.
- How each **screen archetype** (feed/list, form, profile, settings, modal/dialog) and the navigation
  shell adapt across viewports — what moves, collapses, stacks, or is reachable where.
- Touch-target sizing, reachability, and input ergonomics on a phone.
- What MUST hold on a phone for the core loop (read timeline, compose/post, reply, like, follow, view
  profile) with no broken layout or unreachable control.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Internal contract | `../contracts/` (read-only) | Section ownership, your id range, trace rule |
| IA & screen inventory | `../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The archetypes/nav shell your rules adapt |
| Component library | `../SUBTASK_visual_system/outputs/visual-system.md` | The components whose responsive behavior you specify |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | REQ-PROD-035 (works on a phone) and the core loop to trace to |

### Methodology
Design-domain bundle: **Experience Design** (primary — responsive/layout). Load on demand; if the loader
is unavailable, design from bundle intent and competence and record the limitation.

### Output
- `outputs/responsive.md` — the `responsive_layout` section content and `REQ-UX-090..099` entries
  (statement, testable acceptance criteria, `release_gating`, ≥1 `REQ-PROD-*`). Repository-ready; no
  host/system/taskflow detail or attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library.
- [ ] Breakpoints and per-archetype + nav-shell adaptation are specified concretely.
- [ ] The phone-usable core loop is stated as a testable requirement.
- [ ] Every `REQ-UX-090..099` is testable, release-gating-flagged, and traces to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
