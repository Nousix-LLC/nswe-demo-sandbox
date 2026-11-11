# COMPLETE — SUBTASK_reply_conversation

## What this task did

Designed the **Chirp / conversation** screen (`/@:handle/chirp/:id`) — reading a chirp in the conversation
it belongs to (the chirp it answers and its replies) and replying from that screen — as a designed screen
with its layout, content, primary action (Reply), and its empty, error, and loading states. Minted the
`REQ-UX-057..058` register. Sole output: `outputs/screens-reply-conversation.md`.

## How it composes with the subtree

- Owns exactly the `reply_and_conversation` surface and `REQ-UX-057..058`, per the subtree contract.
- Composes the frozen **screen inventory** (Chirp / conversation screen, its route, feed/list archetype,
  both auth states, addressability, deep-linking, pagination/catch-up, back behaviour, Not found) and
  **component library** (`ChirpCard` incl. its tombstone *error* and *loading*, `ListView`, `ComposeBox`,
  `PrimaryButton`, `InlineError`, `EmptyState`, `LoadingState`, `Avatar`, `IconButton`, `NavShell`) by name;
  nothing redefined; no screen or component invented.
- The shared **ComposeBox** is composed by name in the conversation's reply slot (reply-position
  placement); its counter, 280-char limit, disabled/empty/error/loading behaviour, and keep-the-draft
  recovery are left to the compose/post surface and the component library, not redesigned here.
- `SUBTASK_synthesis` will assemble this output after compose_post (writing → reading-and-replying) into
  `outputs/screens-posting-conversation.md` and consolidate `REQ-UX-054..058`.

## Success criteria met

- [x] Composes against `../contracts/`, the screen inventory, and the component library; nothing redefined;
      `ComposeBox` composed by name in the reply slot, not redesigned.
- [x] The Chirp / conversation screen is designed with its empty, error (removed focused chirp → tombstone /
      Not found; reply to a gone chirp → not-found at the compose control with the draft kept; replies fail
      to load → `ListView` error with retry), and loading (`LoadingState` skeleton for the focused chirp,
      parent-context slot, and reply rows) states.
- [x] The screen specifies layout, content, and a primary action (Reply) — not a bare route name.
- [x] `REQ-UX-057` and `REQ-UX-058` are each testable by a stranger on the live product, `release_gating`-
      flagged, unique, in range (057..058), and trace to ≥1 `REQ-PROD-*`:
      - REQ-UX-057 (reading-in-context) → REQ-PROD-004, `release_gating: false` with a one-line reason
        (honouring the non-gating staging).
      - REQ-UX-058 (reply action incl. not-found and the signed-out path) → REQ-PROD-003,
        `release_gating: true`.

## Notes recorded

- **Methodology posture**: the `design` methodology loader was unavailable in this reconstructed
  environment (the domain is unset). Per the subtree hub's recorded posture, the screen was designed from
  the Experience Design (primary) and Product Strategy (support) bundle intent and product-design practice,
  composing the already-frozen upstream vocabularies. The limitation did not block the work and is recorded
  in the output's scope/method notes.
- **Hygiene**: the output carries no host/system/taskflow detail, no workspace paths, no agent/DAG/run ids,
  and no attribution trailer — repository-ready.
- **States consistency**: the per-screen states compose the components' own named states and the global
  keep-the-draft / expired-session recovery owned by the considered-states surface, for `SUBTASK_synthesis`
  to assert STATES_CONSISTENT across the assembled whole.

## Output

- `outputs/screens-reply-conversation.md`
</content>
