# Task: Screens & flows for chirp (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_screens_flows
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **actual screens and flows** for every journey a releasable chirp needs — each screen's
layout, content, and primary action, and **each screen's empty, error, and loading states** — to the bar
of *designed screens, not a skeleton*.

### Context
Part of the experience-design subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`screens_and_flows` and `empty_error_loading_states` sections of `design/experience-design.md`, and
`REQ-UX-040..089`. You compose against the IA **screen inventory** and the **component library**; you do
not invent new screens or components outside those vocabularies without extending the contract. A product
with no designed screens has not been designed.

**Dependencies**: `SUBTASK_ia_interaction`, `SUBTASK_visual_system`. **Dependents**: `SUBTASK_synthesis`.

### Scope — distinct surfaces to weigh in your own evaluation
This brief covers **many distinct screens/flows**; evaluate your own scope against them and decompose if
warranted. Each surface is designed with its happy path **and** its empty / error / loading states, and
each maps to the journeys and `REQ-PROD-*` named:
- **Get in**: first-visit landing (J1, REQ-PROD-030/031); sign-up (J2, 008/009/031); sign-in (J3,
  010/011); account recovery (J3a, 012/013); sign-out (J3b, 014).
- **The core loop**: home timeline incl. bounded catch-up (J4, 002); compose & post (J4, 001); reply &
  reading a conversation (J4, 003/004); like/unlike (J4, 005); follow/unfollow (J4, 006); discovery /
  find people (J4, 042); view a profile (J4, 007).
- **Onboarding**: first-run off the empty state (J5, 032).
- **Manage the account**: edit profile (J6, 016); account settings — contact, sessions/devices,
  notification preferences, handle-change position (J6, 017/018).
- **Leaving**: data export (J8, 019); account deletion with confirmation and explained outcome (J8,
  020/021/022).
- **Safety & notifications (user-facing)**: notifications surface (J7, 029); report content/account
  (J7, 025/026); block/mute (J7, 027); the user-facing help/support entry point (J9, 028 — entry only;
  operator tooling is the OPS area).
- **Global considered states**: the empty/loading/error patterns and expired-session/transient-error
  recovery that keep a drafted chirp (REQ-PROD-033/034), applied across the screens above.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene |
| Internal contract | `../contracts/` (read-only) | Section ownership, your id range, required surfaces, trace rule |
| IA & screen inventory | `../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The screen set/archetypes and navigation you design into |
| Component library | `../SUBTASK_visual_system/outputs/visual-system.md` | The components you assemble screens from |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journeys J1–J10 and `REQ-PROD-*` each screen serves and traces to |
| Repository / live product | `Nousix-LLC/nswe-demo` @ `c805525`; live deployment (read-only) | The current three screens as the "from" state |

### Methodology
Design-domain bundles: **Experience Design** (primary); **Product Strategy** and **Identity and Trust**
(support — so auth/account screens align with the identity requirements). Load on demand; if the loader
is unavailable, design from bundle intent and competence and record the limitation.

### Output
- `outputs/screens-flows.md` — the `screens_and_flows` and `empty_error_loading_states` section content
  (screen/flow descriptions at wireframe-level detail and/or repo-holdable design assets), and
  `REQ-UX-040..089` entries (statement, testable acceptance criteria, `release_gating`, ≥1 `REQ-PROD-*`).
  Repository-ready; no host/system/taskflow detail or attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- [ ] Every required surface in `../contracts/ux_section_and_id_map.yaml` is designed with its
      empty/error/loading states — or recorded out-of-scope with a reason.
- [ ] Each screen specifies layout, content, and primary action — designed, not a bare route name.
- [ ] Every `REQ-UX-040..089` is testable, release-gating-flagged, and traces to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
