# Task: The empty / error / loading states section for chirp

## Task Specification
**Slug**: SUBTASK_considered_states
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **`empty_error_loading_states` section**: the product-wide empty / loading / error **patterns**
every chirp screen obeys, and the **expired-session / transient-error recovery** that routes the person to
sign-in with their place explained and **preserves a drafted chirp** — the cross-cutting treatment the
per-screen designs reference, to the bar of *designed states, not blanks or silent failures*.

### Context
Part of the screens-&-flows subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`empty_error_loading_states` section and `REQ-UX-086..089`. This is the one cross-cutting part of the
deliverable: the four surface-cluster spokes design each screen's own empty/error/loading states by
composing the component library's named states and **your** global patterns; you set those patterns and
the session-expiry/draft-preservation recovery once, over the component library and the IA's
session-expiry convention, so the whole product is consistent. You compose against the frozen **component
library** and **screen inventory**; you do not invent new components or a conflicting per-screen pattern.

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Scope — the cross-cutting treatment to design
Design the product-wide patterns, expressed over the named state components (`EmptyState`,
`LoadingState`, `InlineError`, `InlineFeedback`, `Toast`, and the `ListView`/`ChirpCard`/`ProfileHeader`
states) and the IA conventions, so each is a designed state a person can understand and act on:
- **Empty** — the designed treatment for a surface with nothing in it (a brand-new timeline, an empty
  notifications list, no blocked accounts, not-found), explaining why and offering a next step rather
  than a blank area (REQ-PROD-033).
- **Loading** — skeletons at the real dimensions of the content for first loads, bounded spinners for
  in-place loads, nothing loading forever (REQ-PROD-033).
- **Error** — failures shown where the action was taken (field-level, control-level, list-level), in
  plain words with a way to retry, never a silent no-op, never a system/error code (REQ-PROD-033).
- **Expired-session & transient-error recovery** — an expired/invalid session routes to sign-in with the
  reason stated and returns the person to where they were; a transient error is retryable **without
  losing in-progress work such as a drafted chirp** (REQ-PROD-034; compose against the IA's
  session-expiry convention `REQ-UX-008` — do not redefine it).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your section + id range, the states cross-reference rule, the shared-vocab rule, the trace rule, identities. |
| Component library | `../../SUBTASK_visual_system/outputs/visual-system.md` | The named state components whose behaviour these patterns are expressed over. |
| Screen inventory | `../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The archetypes and the session-expiry/back/feedback conventions these patterns apply across. |
| Product requirements | `../../../SUBTASK_product_requirements/outputs/product-requirements.md` | REQ-PROD-033, 034 and the journeys the patterns serve. |

### Output
- `outputs/empty-error-loading-states.md` — the `empty_error_loading_states` section: the global
  empty/loading/error patterns and the expired-session/transient-error recovery, written so the
  surface-cluster spokes' per-screen states are consistent with it, and `REQ-UX-086..089` entries
  (`statement`, testable `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*`). Repository-ready; no
  host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/` and the component library; the patterns are expressed over the
      components' named states, not as new inventions.
- [ ] Empty, loading, error, and expired-session/transient-error recovery (keep-the-draft) are each
      designed as a product-wide pattern a stranger could check on the live product.
- [ ] Every `REQ-UX-086..089` is testable, `release_gating`-flagged, unique, in-range, and traces to ≥1
      `REQ-PROD-*` (033/034).

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary). Load bundle bodies on demand; if the `design` loader is
  unavailable, design from the bundle intent and competence and record the limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist over the narrative before
  finalizing.
