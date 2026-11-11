# Task: Sessions & devices screen for chirp (with empty / error / loading states)

## Task Specification
**Slug**: SUBTASK_sessions_devices
**Task Kind**: standard
**Status**: Pending

### Objective
Design the **Sessions & devices** surface — the inventory's `Sessions & devices` screen
(`/settings/sessions`, settings archetype, signed-in) — as a designed screen with its layout, content,
and primary action, and its **empty, error, and loading states**, to the bar *designed screens, not a
skeleton*.

### Context
Part of the account-settings subtree (see `../_GLOBAL.md`, `../contracts/`). You own the
`sessions_and_devices` surface and `REQ-UX-073..074`. This surface lets a signed-in person **see their
active sessions/devices** (the current one marked), **end a session on another device** — a confirmed,
destructive action via the Dialog confirmation variant — and **sign out**, the session end being
server-side so the ended session can no longer be used. It is addressable and returns to the Settings hub.

Design *what the person can see and do*: the list of sessions with enough to recognise each (device,
when, current-marker), the confirmed end-session action and its effect, and the sign-out entry that
leads into the signed-out shell. Design sign-out **into** the inventory's sign-out transition (ends the
session, returns to the signed-out landing, back does not re-expose a protected screen) — do not redesign
that transition. Do **not** design the session/token mechanism — that is the identity design's
`REQ-ID-*`. Compose against the frozen **screen inventory** and **component library** by name; invent no
screen or component outside them without an additive amendment to `../contracts/`.

J6 / REQ-PROD-017, 014 (sign-out that ends the session server-side).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, constraints, hygiene, methodology posture. |
| Internal contract | `../contracts/` (read-only) | Your surface + ids (073–074), the destructive-confirmation and sign-out-transition conventions in use, shared-vocab rule, trace rule, identities. |
| Screen inventory | `../../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The `Sessions & devices` screen, the confirming-destructive-actions convention (REQ-UX-011), the sign-out transition (REQ-UX-016), the `Sign out` dialog. |
| Component library | `../../../../SUBTASK_visual_system/outputs/visual-system.md` | The components you assemble this screen from (ListView, SettingRow, SecondaryButton/IconButton, Dialog confirmation variant, InlineFeedback, InlineError, EmptyState, LoadingState; `type.family.mono` for a session identifier) with their named states. |
| Product requirements | `../../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J6 and REQ-PROD-014/017 this screen serves and traces to. |

### Output
- `outputs/screen-sessions-devices.md` — the Sessions & devices screen at wireframe-level detail (layout,
  content, primary action, and empty/error/loading states — including the empty "only this session" case,
  the confirmed end-session flow, and the sign-out confirmation), and `REQ-UX-073..074` entries
  (`statement`, testable `acceptance_criteria`, `release_gating`, ≥1 `REQ-PROD-*` each). Give viewing +
  ending another session its own gated requirement, and server-side sign-out its own gated requirement.
  Repository-ready; no host/system/taskflow detail, no workspace paths, no attribution.

### Success criteria
- [ ] Composes against `../contracts/`, the screen inventory, and the component library by name; nothing
      redefined.
- [ ] The screen is designed with layout, content, and a primary action (not a bare route name); lists
      active sessions with the current one marked, lets the person end another session through a
      confirmation that names the effect, and offers sign-out that ends the session server-side; is
      addressable and returns to the hub.
- [ ] Empty, error, and loading states are designed (or "does not apply" with a component-matching reason).
- [ ] Designs user-visible behaviour only — not the session/token mechanism; designs sign-out into the
      inventory's transition without redesigning it.
- [ ] `REQ-UX-073` and `REQ-UX-074` are each testable on the live product, `release_gating`-flagged,
      unique, in-range (073–074), and trace to ≥1 `REQ-PROD-*`.

### Constraints
- Design only — no front-end code. Repository-ready hygiene on all output content.
- Methodology: Experience Design (primary); Identity & Trust (support). If the `design` loader is
  unavailable, design from the bundle intent and competence and record the limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist (or the P0/P1 catalog by
  hand when the skill is absent — it is absent here) over the narrative before finalizing, and record the
  limitation.
- Evaluate your own scope against the decomposition triggers at dispatch; this is one surface and is
  expected to be atomic, but the decision is yours to make against your actual brief.
