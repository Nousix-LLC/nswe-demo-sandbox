# Task: Composing and posting a chirp (the ComposeBox writing surface, with empty / error / loading states)

## Task Specification

**Slug**: SUBTASK_compose_post
**Task Kind**: standard
**Status**: Pending

### Objective

Design the **compose & post** surface — where a chirper writes and publishes a chirp within the published
280-character limit — as a designed surface with its layout, content, primary action, and its empty, error,
and loading states, to the bar of *designed screens, not a skeleton*.

### Context

Part of the writing-and-reading-in-context subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
**compose_and_post** surface and `REQ-UX-054..056`. You compose against the frozen **screen inventory** and
**component library**; you do not invent screens or components outside those vocabularies without an
additive amendment to `../contracts/`. You design the `ComposeBox` component in all three of its placements,
including the reply-position variant that the sibling `SUBTASK_reply_conversation` composes into the
conversation screen — so your design of the reply placement is the one the conversation screen refers to.

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Scope — the one surface you design

- **Compose & post** (`ComposeBox`, the **Compose** screen/dialog, archetype modal/dialog): write and
  publish a chirp within the published 280-character limit, with the remaining-character affordance that
  warns as the limit nears and blocks an over-limit or empty post (J4.2 / REQ-PROD-001). Design the three
  places `ComposeBox` appears — inline at the top of the home timeline, as the body of the **Compose**
  dialog (`/compose` and the overlay dialog), and in a conversation's reply position — and the primary
  action ("Post" / "Reply"). Design these states:
  - **empty** — placeholder prompt, counter at full, Post disabled (compose against `ComposeBox`'s *empty*
    and `PrimaryButton`'s *disabled* states).
  - **error** — over the limit (counter in the danger role, Post disabled) **or** a failed publish →
    `InlineError` below the field with the draft kept so the person can retry. The keep-the-draft recovery
    is the global pattern owned by `SUBTASK_considered_states` (outside this subtree); compose it, do not
    redefine it.
  - **loading** — publish in flight → Post shows its busy state and the field briefly locks so the chirp is
    not double-posted (compose against `ComposeBox`'s *loading* and `PrimaryButton`'s *loading* states).

### Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surface + id range, the surface map, the shared-vocab rule, the shared-`ComposeBox` ownership note, the trace rule, identities. |
| Screen inventory | `../../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The Compose screen, its route and overlay-dialog form, the archetype, the back/dialog-dismiss and session-expiry (keep-the-draft) conventions, the always-available compose affordance. |
| Component library | `../../../../SUBTASK_visual_system/outputs/visual-system.md` | `ComposeBox`, `Dialog`, `PrimaryButton`, `Avatar`, `InlineError`, `Toast` and their named states; the 280-char counter affordance and tabular-figure counter. |
| Product requirements | `../../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J4 (step 2, compose & post) and `REQ-PROD-001` this surface serves and traces to. |

### Output

- `outputs/screens-compose-post.md` — the compose/post surface at wireframe-level detail (layout, content,
  primary action, empty/error/loading states across the three `ComposeBox` placements) and
  `REQ-UX-054..056` entries (`statement`, testable `acceptance_criteria`, `release_gating`, ≥1
  `REQ-PROD-*`). Repository-ready; no host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- [ ] The compose/post surface is designed with its empty/error/loading states across all three `ComposeBox`
      placements — or a state recorded out-of-scope with a reason.
- [ ] The surface specifies layout, content, and a primary action — not a bare route name.
- [ ] Every `REQ-UX-054..056` is testable, `release_gating`-flagged, unique, in-range (054..056), and traces
      to ≥1 `REQ-PROD-*` (REQ-PROD-001 is `release_gating: true`).

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Product Strategy (support). Load bundle bodies on demand; if the
  `design` loader is unavailable, design from the bundle intent and competence and record the limitation (do
  not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist over the narrative before
  finalizing.
