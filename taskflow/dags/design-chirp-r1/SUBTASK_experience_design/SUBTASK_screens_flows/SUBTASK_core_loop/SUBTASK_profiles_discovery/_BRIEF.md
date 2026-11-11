# Task: Profiles, followers/following, and discovery (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_profiles_discovery
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **identity-and-find-people** surfaces of the core loop — the Public and Own profile screens,
the Followers and Following lists, and the Explore / find-people discovery screen — each a designed screen
with its layout, content, and primary action, and its empty, error, and loading states, to the bar of
*designed screens, not a skeleton*.

### Context
Part of the core-loop screens subtree (see `../_GLOBAL.md`, `../contracts/`). You own the **view_profile**
and **discovery_find_people** surfaces and `REQ-UX-061..064`. You compose against the frozen **screen
inventory** and **component library**; you do not invent screens or components outside those vocabularies
without an additive amendment to `../contracts/`. Viewing people and finding people are two distinct
surfaces of one identity/discovery concern — weigh them in your own scope evaluation. The follow control
that lives on these screens is designed by the sibling `../SUBTASK_social_actions` spoke; compose against
it and refer to it, do not redesign it.

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Scope — distinct surfaces to weigh in your own evaluation
- **View a profile** (`ProfileHeader` + a `ListView` of `ChirpCard`s, archetype profile):
  - **Public profile** (`/@:handle`, reachable signed-out and signed-in) — handle, display name, bio,
    follower/following counts, and their chirps (J4.6 / REQ-PROD-007; public, needs no session).
  - **Own profile** (`/@:handle` own, signed-in) — the person's own public face, with the entry to edit it
    (edit-profile itself is the account-lifecycle spoke's surface — link to it, do not design it here).
  - **Followers** (`/@:handle/followers`) and **Following** (`/@:handle/following`) — the paginated lists
    of accounts, each row a person card with the follow control.
  - States across these: **empty** (a sparse profile with no bio and zero counts → calm labelled zeros and
    a prompt; an empty followers/following list → `EmptyState`); **error** (profile fails to load, or a
    blocked/suspended/not-found account → `ProfileHeader`/`EmptyState` error variant, not a broken header;
    a list page fails → `ListView` error with retry); **loading** (`ProfileHeader` + `ListView` skeletons).
- **Discovery / find people** (the **Explore / find people** screen `/explore`, archetype feed/list):
  search for and discover people/content to follow beyond already holding a profile link (J4.5 /
  REQ-PROD-042). States: **empty** (no query yet → a prompt and any suggestions; a query with no matches →
  `EmptyState` "no results" with a way to refine); **error** (search fails → `ListView`/`InlineError` with
  retry); **loading** (skeleton results).
- Note the staging: `REQ-PROD-042` (discovery) and the second-visit catch-up are non-gating in the product
  requirements — honour that where it applies while still designing the surface fully.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surfaces + id range, the surface map, the shared-vocab rule, the trace rule, identities. |
| Screen inventory | `../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The profile, followers/following, and Explore screens, routes, archetypes, auth states, and pagination convention. |
| Component library | `../../../SUBTASK_visual_system/outputs/visual-system.md` | `ProfileHeader`, `ListView`, `ChirpCard`, `Avatar`, `EmptyState`, `LoadingState`, `InlineError`, `TextField` and their states. |
| Product requirements | `../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J4 and `REQ-PROD-007, 042` these surfaces serve and trace to. |

### Output
- `outputs/screens-profiles-discovery.md` — the profile, followers/following, and discovery surfaces at
  wireframe-level detail (layout, content, primary action, empty/error/loading states) and
  `REQ-UX-061..064` entries (`statement`, testable `acceptance_criteria`, `release_gating`, ≥1
  `REQ-PROD-*`). Repository-ready; no host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- [ ] Public/Own profile, followers/following, and discovery are each designed with their
      empty/error/loading states — or recorded out-of-scope with a reason.
- [ ] Each surface specifies layout, content, and a primary action — not a bare route name.
- [ ] Every `REQ-UX-061..064` is testable, `release_gating`-flagged, unique, in-range, and traces to ≥1
      `REQ-PROD-*` (honouring REQ-PROD-042's non-gating staging where it applies).

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Product Strategy (support). Load bundle bodies on demand; if
  the `design` loader is unavailable, design from the bundle intent and competence and record the
  limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist over the narrative before
  finalizing.
