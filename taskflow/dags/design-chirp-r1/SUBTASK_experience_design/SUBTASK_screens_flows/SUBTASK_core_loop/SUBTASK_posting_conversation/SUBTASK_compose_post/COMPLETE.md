# COMPLETE — SUBTASK_compose_post

## What this task did

Designed the **compose & post** surface — the `ComposeBox` writing surface in all three placements —
to the bar of *designed screens, not a skeleton*, and minted its three requirements. One output:
`outputs/screens-compose-post.md`.

## Decompose evaluation

`Atomic`. The brief is one responsibility — design the single `ComposeBox` writing surface. Its three
placements are the same frozen component in different positions, and its three states are that
component's own named states; both concern tests pass and every trigger clears. The compose-vs-
conversation split was the parent's, not grounds for this node's verdict.

## How it composes (evidence for SUBTASK_synthesis's identities)

- **SURFACE_COVERAGE** — the `compose_and_post` surface is designed with its empty, error, and loading
  states. Error covers both the over-limit case (shown live in the counter and field) and the
  failed-publish case (draft kept, inline error, retry). No state recorded out of scope.
- **ID_UNIQUE_IN_RANGE** — `REQ-UX-054`, `REQ-UX-055`, `REQ-UX-056`: three unique ids, all within the
  assigned `054..056` sub-range, no gaps claimed.
- **NOT_SKELETAL** — the surface specifies layout and content (avatar, draft field, counter, action),
  a context-labelled primary action ("Post" / "Reply"), and the three states — not a bare route name.
- **UX_TESTABLE_AND_GATED** — each requirement has a statement, acceptance criteria a stranger can run
  on the live product, and `release_gating: true` (all three gate posting via REQ-PROD-001).
- **UX_TRACES_TO_PROD** — 054 → REQ-PROD-001; 055 → REQ-PROD-001; 056 → REQ-PROD-001, REQ-PROD-003.
- **COMPOSES_AGAINST_VOCAB** — `ComposeBox`, `PrimaryButton`, `SecondaryButton`, `Avatar`, `Dialog`,
  `InlineError`, `Toast`, `NavShell` used by name with their named states; the Compose, Home timeline,
  and Chirp / conversation screens used by name and route; the published 280 limit read from
  REQ-PROD-001. Nothing redefined; no screen or component invented.
- **STATES_CONSISTENT** — the failed-publish and session-expiry recovery compose the product-wide
  keep-the-draft pattern (owned by the considered-states spoke, outside this subtree) rather than
  redefining it; the states are the components' own named states.
- **HYGIENE** — the deliverable carries no host/system/taskflow detail, no workspace paths, no
  agent/DAG/run ids, and no attribution trailer. (This record is a lifecycle artifact, not the
  repository deliverable.)

## Shared-component note

`ComposeBox` is designed here in all three placements, including the reply-position variant that
`SUBTASK_reply_conversation` composes into the conversation screen — so the reply field the
conversation refers to is the one specified here.

## Methodology note

The `design` methodology loader was unavailable in this reconstructed environment (the loader syscall
reports the agent domain unset). Per the brief and the ancestor hubs' recorded posture, the surface was
designed from the Experience Design (primary) and Product Strategy (support) bundle intent and
product-design competence, composing the already-frozen IA and component-library decisions. The
limitation did not block the work.

## Output

- `outputs/screens-compose-post.md` — the compose/post surface (layout, content, primary action,
  empty/error/loading states across the three placements) and `REQ-UX-054..056`.
