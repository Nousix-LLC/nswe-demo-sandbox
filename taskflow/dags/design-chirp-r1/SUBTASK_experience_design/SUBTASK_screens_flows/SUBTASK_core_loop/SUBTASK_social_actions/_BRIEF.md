# Task: Like/unlike and follow/unfollow — the in-place social actions (with error / loading states)

## Task Specification
**Slug**: SUBTASK_social_actions
**Task Kind**: standard
**Status**: Pending

### Objective
Design the two **in-place social-action behaviors** of the core loop — like/unlike and follow/unfollow —
as designed controls with their layout (where they sit), content (label + count + state), primary action,
and their active/default, error, and loading states, to the bar of *designed, not a skeleton*.

### Context
Part of the core-loop screens subtree (see `../_GLOBAL.md`, `../contracts/`). You own the **like_unlike**
and **follow_unfollow** surfaces and `REQ-UX-059..060`. These are not standalone screens; they are the
in-place controls that live on other screens' components — the like control on every `ChirpCard`, the
follow control on `ProfileHeader` and on the person cards in discovery and lists. You compose against the
frozen **component library** and do not redefine those components; you specify how the behavior reads and
behaves across the places it appears.

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Scope — the two behaviors to design
- **Like / unlike** (the `ChirpCard` like `IconButton`): an in-place control that is **idempotent** (liking
  twice does not double-count) and shows an **accurate count** that reflects the result; the active "liked"
  state is a colour *and* a filled heart *and* a "Liked" label (never colour alone) (J4.4 / REQ-PROD-005).
  States: **default/active** (not-liked vs liked); **error** (a failed like/unlike → `InlineFeedback` in
  the danger role at the control, optimistic change reverted so the control never lies about the count);
  **loading** (in-flight → the control's own busy treatment).
- **Follow / unfollow** (the `ProfileHeader` / person-card follow control, `PrimaryButton` "Follow" /
  `SecondaryButton` "Following"): an in-place, **idempotent** control that shapes the timeline; a person
  **cannot follow themselves** (the self-follow case is refused and the control reflects that) (J4.5 /
  REQ-PROD-006). States: **default/active** (Follow vs Following); **error** (a failed follow/unfollow →
  `InlineFeedback` danger, reverted); **loading** (in-flight busy treatment).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surfaces + id range, the surface map, the shared-vocab rule, the trace rule, identities. |
| Screen inventory | `../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | Where these controls appear (timeline, conversation, profile, lists) and the transient-feedback convention. |
| Component library | `../../../SUBTASK_visual_system/outputs/visual-system.md` | `ChirpCard`, `IconButton`, `ProfileHeader`, `PrimaryButton`, `SecondaryButton`, `InlineFeedback` and their states. |
| Product requirements | `../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J4 and `REQ-PROD-005, 006` these behaviors serve and trace to. |

### Output
- `outputs/screens-social-actions.md` — the like and follow in-place behaviors at wireframe-level detail
  (where they sit, content, primary action, default/active/error/loading states) and `REQ-UX-059..060`
  entries (`statement`, testable `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*`).
  Repository-ready; no host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/` and the component library; nothing redefined.
- [ ] Like/unlike and follow/unfollow are each designed with their default/active, error, and loading
      states, including the idempotency, the accurate-count, and the cannot-follow-self behaviors.
- [ ] Each behavior specifies where it sits, its content, and its primary action — not a bare name.
- [ ] Every `REQ-UX-059..060` is testable, `release_gating`-flagged, unique, in-range, and traces to ≥1
      `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Product Strategy (support). Load bundle bodies on demand; if
  the `design` loader is unavailable, design from the bundle intent and competence and record the
  limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist over the narrative before
  finalizing.
