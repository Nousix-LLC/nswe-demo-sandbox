# Task: Core-loop screens for chirp (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_core_loop
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **core social loop** chirp exists for — the home timeline, composing and posting, replying and
reading a conversation, liking, following, discovering people, and viewing a profile — each a designed
screen with its layout, content, and primary action, and **each with its empty, error, and loading
states**, to the bar of *designed screens, not a skeleton*.

### Context
Part of the screens-&-flows subtree (see `../_GLOBAL.md`, `../contracts/`). You own the **core_loop** part
of the `screens_and_flows` section and `REQ-UX-051..064`. You compose against the frozen **screen
inventory** and **component library**; you do not invent screens or components outside those vocabularies
without an additive amendment to `../contracts/`. This is the loop a chirper performs every day — it must
be fast, behave sensibly when there is nothing new or the person is brand new, and recover visibly when
something fails.

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Scope — distinct surfaces to weigh in your own evaluation
This brief covers **many distinct screens/flows**; evaluate your own scope against the decomposition
triggers and decompose if warranted. Each surface is designed with its happy path **and** its empty /
error / loading states, and each maps to its journey and `REQ-PROD-*`:
- **Home timeline** — own + followed chirps, newest-first, bounded pages, with the load-older and
  catch-up ("N new chirps") affordances (J4 / REQ-PROD-002).
- **Compose & post** — write and publish a chirp within the 280-char limit, with the remaining-character
  affordance and over-limit/empty rejection (J4 / REQ-PROD-001); inline at the timeline top, the Compose
  dialog, and the reply position.
- **Reply & reading a conversation** — the Chirp / conversation screen: a chirp shown with its parent and
  its replies; replying to a gone chirp reported not-found (J4 / REQ-PROD-003, 004).
- **Like / unlike** — the in-place like control and its idempotent, accurate count (J4 / REQ-PROD-005).
- **Follow / unfollow** — the in-place follow control on profiles and cards; cannot follow self (J4 /
  REQ-PROD-006).
- **Discovery / find people** — the Explore screen: search for and discover people/content to follow
  (J4 / REQ-PROD-042).
- **View a profile** — the Public and Own profile screens (identity block + their chirps) and the
  Followers / Following lists (J4 / REQ-PROD-007).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your section-part + id range, the surface map, the shared-vocab rule, the trace rule, identities. |
| Screen inventory | `../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The feed/list and profile screens, routes, and the pagination/back/feedback conventions you design into. |
| Component library | `../../SUBTASK_visual_system/outputs/visual-system.md` | The components (ListView, ChirpCard, ComposeBox, ProfileHeader, IconButton, InlineFeedback, EmptyState, LoadingState, …) you assemble these screens from. |
| Product requirements | `../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J4 and the `REQ-PROD-*` each screen serves and traces to. |

### Output
- `outputs/screens-core-loop.md` — the **core_loop** screens/flows at wireframe-level detail (each
  screen's layout, content, primary action, and empty/error/loading states), and `REQ-UX-051..064`
  entries (`statement`, testable `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*`).
  Repository-ready; no host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- [ ] Timeline, compose, conversation, like, follow, discovery, and profile (incl. followers/following)
      are each designed with their empty/error/loading states — or recorded out-of-scope with a reason.
- [ ] Each screen specifies layout, content, and a primary action — not a bare route name.
- [ ] Every `REQ-UX-051..064` is testable, `release_gating`-flagged, unique, in-range, and traces to ≥1
      `REQ-PROD-*` (honouring REQ-PROD-042/004's non-gating staging where it applies).

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Product Strategy (support). Load bundle bodies on demand; if
  the `design` loader is unavailable, design from the bundle intent and competence and record the
  limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist over the narrative before
  finalizing.
