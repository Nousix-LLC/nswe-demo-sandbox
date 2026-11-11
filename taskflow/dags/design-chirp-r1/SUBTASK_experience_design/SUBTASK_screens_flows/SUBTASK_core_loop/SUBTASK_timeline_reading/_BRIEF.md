# Task: Home timeline — the core reading surface (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_timeline_reading
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **Home timeline** — the signed-in reading surface chirp opens to — as a designed screen with
its layout, content, and primary action, and its empty, error, and loading states, to the bar of
*designed screens, not a skeleton*.

### Context
Part of the core-loop screens subtree (see `../_GLOBAL.md`, `../contracts/`). You own the **home_timeline**
surface and `REQ-UX-051..053`. You compose against the frozen **screen inventory** and **component
library**; you do not invent screens or components outside those vocabularies without an additive
amendment to `../contracts/`. This is the default thing a chirper does on opening the app — it must be
fast, behave sensibly when there is nothing to show, and recover visibly when a page fails to load.

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Scope — what this surface must cover
- **Home timeline** (`/` with a session, archetype feed/list): the person's own chirps and those of the
  people they follow, newest-first, in **bounded pages** — the `ListView` hosting `ChirpCard`s inside the
  signed-in `NavShell`, with the **load-older** affordance and the **catch-up ("N new chirps")** affordance
  for chirps posted since the person last looked (J4.1 / REQ-PROD-002; the pagination/catch-up convention
  is set by the IA — compose against it, do not redefine it).
- Its **states**, as the relevant components' own named states consistent with the global patterns owned
  by `../../SUBTASK_considered_states`: **empty** (a brand-new account that follows no one and has posted
  nothing → the `ListView`/`EmptyState` empty block pointing to Explore and composing a first chirp, not a
  blank area — noting that first-run onboarding itself is the account-lifecycle spoke's surface, so here
  design only the timeline's own empty treatment and hand off to onboarding); **error** (a page or the
  catch-up fetch fails → `ListView` error / `InlineError` with retry at the point of failure, already-shown
  chirps not discarded); **loading** (first load → `LoadingState` skeleton rows, not a spinner on a blank
  screen; loading older → a bounded spinner at the load-more boundary).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surface + id range, the surface map, the shared-vocab rule, the trace rule, identities. |
| Screen inventory | `../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The feed/list screen, route, and the pagination/catch-up/back conventions you design into. |
| Component library | `../../../SUBTASK_visual_system/outputs/visual-system.md` | `NavShell`, `ListView`, `ChirpCard`, `EmptyState`, `LoadingState`, `InlineError` and their states. |
| Product requirements | `../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J4 and `REQ-PROD-002` this screen serves and traces to. |

### Output
- `outputs/screens-timeline-reading.md` — the Home timeline at wireframe-level detail (layout, content,
  primary action, empty/error/loading states) and `REQ-UX-051..053` entries (`statement`, testable
  `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*`). Repository-ready; no host/system/taskflow
  detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- [ ] The Home timeline is designed with its empty, error, and loading states.
- [ ] The screen specifies layout, content, and a primary action — not a bare route name.
- [ ] Every `REQ-UX-051..053` is testable, `release_gating`-flagged, unique, in-range, and traces to ≥1
      `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Product Strategy (support). Load bundle bodies on demand; if
  the `design` loader is unavailable, design from the bundle intent and competence and record the
  limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist over the narrative before
  finalizing.
