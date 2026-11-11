# Task: The Chirp / conversation screen — reading in context and replying (with empty / error / loading states)

## Task Specification

**Slug**: SUBTASK_reply_conversation
**Task Kind**: standard
**Status**: Pending

### Objective

Design the **Chirp / conversation** screen — where a chirp is shown with the chirp it replies to and its
replies (the conversation in context) and a reply is written from that screen — as a designed screen with
its layout, content, primary action, and its empty, error, and loading states, to the bar of *designed
screens, not a skeleton*.

### Context

Part of the writing-and-reading-in-context subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
**reply_and_conversation** surface and `REQ-UX-057..058`. You compose against the frozen **screen
inventory** and **component library**; you do not invent screens or components outside those vocabularies
without an additive amendment to `../contracts/`. The reply control on this screen is the `ComposeBox`
reply-position placement designed by the sibling `SUBTASK_compose_post`: **compose it by name in the
conversation's reply slot; do not redesign `ComposeBox`, its 280-char counter, or its keep-the-draft
recovery** (those are compose_post's and the component library's).

**Dependencies**: none (within this subtree). **Dependents**: `SUBTASK_synthesis`.

### Scope — the one screen you design

- **Reply & reading a conversation** (the **Chirp / conversation** screen `/@:handle/chirp/:id`, archetype
  feed/list, reachable in both auth states, inside the appropriate `NavShell`): a chirp shown with the
  chirp it replies to and its replies — the conversation in context — and replying from that screen
  (J4.3 / REQ-PROD-003, 004). Design its layout (root chirp, the parent it answers, the replies as a
  bounded, newest-or-oldest-first list via `ListView`; the reply `ComposeBox` in its slot), its content,
  and its primary action (Reply). Design these states:
  - **empty** — a chirp with no replies yet: shown as the root chirp with an invitation to reply, **not** a
    blank area (compose against `ListView`'s *empty* / `EmptyState` and the `ChirpCard` default).
  - **error** — replying to a chirp that no longer exists → reported not-found via the `ChirpCard`
    tombstone / `InlineError`, **not** a silent drop; a failed page load → `ListView` error with retry.
  - **loading** — `LoadingState` skeleton for the root chirp and the replies (compose against
    `ChirpCard`'s and `ListView`'s *loading* states).
- The reading-in-context behaviour rides `REQ-PROD-004`, which the release bar does **not** gate; the reply
  action itself rides `REQ-PROD-003`, which it does. Reflect that staging in your `release_gating` flags
  per `../contracts/` (`trace_rule`).

### Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surface + id range, the surface map, the shared-vocab rule, the shared-`ComposeBox` composition note, the trace rule (incl. the REQ-PROD-004 non-gating staging), identities. |
| Screen inventory | `../../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The Chirp / conversation screen, its route and feed/list archetype, deep-linking/addressable-chirp, pagination/catch-up, back-behaviour, and not-found conventions. |
| Component library | `../../../../SUBTASK_visual_system/outputs/visual-system.md` | `ChirpCard` (incl. its tombstone *error* and *loading*), `ListView`, `ComposeBox` (reply placement), `PrimaryButton`, `InlineError`, `EmptyState`, `LoadingState` and their states. |
| Product requirements | `../../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J4 (step 3, reply) and `REQ-PROD-003` (reply, gating) and `REQ-PROD-004` (read a reply in its conversation, non-gating) this screen serves and traces to. |

### Output

- `outputs/screens-reply-conversation.md` — the Chirp / conversation screen at wireframe-level detail
  (layout, content, primary action, empty/error/loading states) and `REQ-UX-057..058` entries (`statement`,
  testable `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*`). Repository-ready; no
  host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined;
      `ComposeBox` composed by name in the reply slot, not redesigned.
- [ ] The Chirp/conversation screen is designed with its empty/error/loading states — or a state recorded
      out-of-scope with a reason.
- [ ] The screen specifies layout, content, and a primary action — not a bare route name.
- [ ] Every `REQ-UX-057..058` is testable, `release_gating`-flagged, unique, in-range (057..058), and traces
      to ≥1 `REQ-PROD-*`, honouring REQ-PROD-004's non-gating staging where a REQ-UX rides it alone.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Product Strategy (support). Load bundle bodies on demand; if the
  `design` loader is unavailable, design from the bundle intent and competence and record the limitation (do
  not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist over the narrative before
  finalizing.
