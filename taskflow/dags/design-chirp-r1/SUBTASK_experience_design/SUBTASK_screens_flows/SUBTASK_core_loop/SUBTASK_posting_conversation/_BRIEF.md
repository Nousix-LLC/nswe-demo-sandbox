# Task: Composing, posting, replying, and reading a conversation (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_posting_conversation
**Task Kind**: standard
**Status**: Pending

### Objective
Design the surfaces where a chirper **writes** and **reads what was written in context** — composing and
publishing a chirp within the 280-character limit, replying to a chirp, and the Chirp / conversation
screen — each a designed screen with its layout, content, and primary action, and its empty, error, and
loading states, to the bar of *designed screens, not a skeleton*.

### Context
Part of the core-loop screens subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
**compose_and_post** and **reply_and_conversation** surfaces and `REQ-UX-054..058`. You compose against
the frozen **screen inventory** and **component library**; you do not invent screens or components outside
those vocabularies without an additive amendment to `../contracts/`. Composing and reading-in-context are
two distinct surfaces of one writing concern — weigh them in your own scope evaluation.

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Scope — distinct surfaces to weigh in your own evaluation
- **Compose & post** (`ComposeBox`, the **Compose** screen/dialog, archetype modal/dialog): write and
  publish a chirp within the published 280-character limit, with the remaining-character affordance that
  warns as the limit nears and blocks an over-limit or empty post (J4.2 / REQ-PROD-001). Design the three
  places `ComposeBox` appears — inline at the top of the timeline, as the body of the **Compose** dialog,
  and in a conversation's reply position — and the primary action ("Post" / "Reply"). States: **empty**
  (placeholder prompt, counter at full, Post disabled); **error** (over the limit, or a failed publish →
  `InlineError` with the draft kept so the person can retry — the keep-the-draft recovery is the global
  pattern owned by `../../SUBTASK_considered_states`, composed here); **loading** (publish in flight →
  Post busy, field briefly locked so the chirp is not double-posted).
- **Reply & reading a conversation** (the **Chirp / conversation** screen `/@:handle/chirp/:id`, archetype
  feed/list): a chirp shown with the chirp it replies to and its replies — the conversation in context —
  and replying from that screen (J4.3 / REQ-PROD-003, 004). States: **empty** (a chirp with no replies yet
  — shown as the root chirp with an invitation to reply, not a blank area); **error** (replying to a chirp
  that no longer exists → reported not-found via the `ChirpCard` tombstone / `InlineError`, not a silent
  drop; a failed page load → `ListView` error with retry); **loading** (`LoadingState` skeleton for the
  root chirp and replies).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surfaces + id range, the surface map, the shared-vocab rule, the trace rule, identities. |
| Screen inventory | `../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The Compose and Chirp/conversation screens, routes, archetypes, and the back/dialog and session-expiry conventions. |
| Component library | `../../../SUBTASK_visual_system/outputs/visual-system.md` | `ComposeBox`, `Dialog`, `ChirpCard`, `ListView`, `PrimaryButton`, `InlineError`, `Toast`, `LoadingState` and their states. |
| Product requirements | `../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J4 and `REQ-PROD-001, 003, 004` these surfaces serve and trace to. |

### Output
- `outputs/screens-posting-conversation.md` — the compose/post and conversation surfaces at wireframe-level
  detail (layout, content, primary action, empty/error/loading states) and `REQ-UX-054..058` entries
  (`statement`, testable `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*`). Repository-ready; no
  host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined.
- [ ] Compose/post and reply/conversation are each designed with their empty/error/loading states — or
      recorded out-of-scope with a reason.
- [ ] Each surface specifies layout, content, and a primary action — not a bare route name.
- [ ] Every `REQ-UX-054..058` is testable, `release_gating`-flagged, unique, in-range, and traces to ≥1
      `REQ-PROD-*` (honouring REQ-PROD-004's non-gating staging where it applies).

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Product Strategy (support). Load bundle bodies on demand; if
  the `design` loader is unavailable, design from the bundle intent and competence and record the
  limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist over the narrative before
  finalizing.
