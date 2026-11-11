# Task: Information architecture & interaction model for chirp

## Task Specification
**Slug**: SUBTASK_ia_interaction
**Task Kind**: standard
**Status**: Pending

### Objective
Design chirp's **information architecture and interaction model** — the structure of the product and how
a user moves through it — and publish the canonical **screen inventory** every sibling composes against.

### Context
Part of the experience-design subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`information_architecture_and_interaction` section of `design/experience-design.md`, the **screen
inventory** shared vocabulary, and `REQ-UX-001..019`. This is the foundation the visual system and the
screens build on, so it runs first. A product's structure is what lets a stranger find their way without
being taught; a flat list of features is not an architecture.

**Dependencies**: none. **Dependents**: `SUBTASK_visual_system`, `SUBTASK_screens_flows`,
`SUBTASK_responsive`, `SUBTASK_accessibility`, `SUBTASK_synthesis`.

### Scope — distinct concerns to weigh in your own evaluation
- **Screen/route inventory & archetypes** — the canonical set of screens with user-facing routes, each
  classified by archetype (feed/list, form, profile, settings, modal/dialog, confirmation, empty/landing)
  and auth state (signed-out vs signed-in). This is the shared vocabulary siblings refer to by name.
- **Navigation & wayfinding** — the signed-out shell vs the signed-in shell, global navigation, how a
  user knows where they are and gets to every surface (timeline, compose, profile, notifications,
  settings, help), and the paths between account states.
- **Interaction conventions** — the product-wide patterns: how destructive actions are confirmed, how
  lists paginate/catch-up, how transient feedback is shown, how routing/deep-linking and the browser back
  behave from the user's side, and the signed-out→sign-up→signed-in transitions.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Internal contract | `../contracts/` (read-only) | Section ownership, your id range, screen-inventory required shape |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | Personas P1–P5, journeys J1–J10, `REQ-PROD-*` to structure around and trace to |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | Current SPA structure (timeline `/`, compose `/compose`, profile `/user/:id`, nav bar) — the "from" state; clone into your own workspace if you need a tree |

### Methodology
Design-domain bundles (by Domain Mapping): **Experience Design** (primary — information architecture &
interaction); **Product Strategy** (support). Load bundle bodies on demand; if the methodology loader is
unavailable in this environment, design from the bundle intent and product-design competence and record
the limitation.

### Output
- `outputs/ia-interaction.md` — the `information_architecture_and_interaction` section content, including
  a clearly-headed **"Screen inventory"** in the shape `../contracts/ux_section_and_id_map.yaml` requires,
  and `REQ-UX-001..019` entries (each with statement, testable acceptance criteria, `release_gating`, and
  ≥1 `REQ-PROD-*` reference). Repository-ready content; no host/system/taskflow detail or attribution.

### Success criteria
- [ ] Composes against `../contracts/`; uses the `REQ-UX` scheme and your id range; nothing redefined.
- [ ] Publishes a complete screen inventory (every screen a releasable chirp needs), archetyped, with
      auth state and purpose — the set siblings will design against.
- [ ] Signed-out and signed-in navigation shells and the interaction conventions are specified, not named.
- [ ] Every `REQ-UX-001..019` is testable, release-gating-flagged, and traces to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code; implementation deferred to code DAGs.
- Repository-ready hygiene on all output content.
