# SUSPENSION.md — SUBTASK_posting_conversation (decomposition suspension)

**Terminal state**: SUSPENDED · **decompose_evaluation**: NeedsDecompose

## Why this node decomposed

The brief for `SUBTASK_posting_conversation` spans **two distinct surfaces**, each a separate design
responsibility of a different screen archetype and a different product-requirement trace:

- **compose_and_post** — a *modal/dialog* writing surface (`ComposeBox` in three placements, the 280-char
  affordance, the Post/Reply action), tracing `REQ-PROD-001`.
- **reply_and_conversation** — a *feed/list* reading-in-context screen (the Chirp / conversation screen),
  tracing `REQ-PROD-003` and the non-gating `REQ-PROD-004`.

Trigger evaluation against the actual brief (recorded for audit):

| Trigger / test | Outcome | Evidence |
|---|---|---|
| Token | cleared | Inputs ≪ 50% of context; one markdown deliverable. |
| Scope-Based / enumerated-concerns | **fired** | Two distinct surfaces enumerated in the brief and `../contracts/`. |
| Distinct Concerns | **failed** | Two different archetypes (modal/dialog vs feed/list) a different specialist could design in parallel against the already-frozen `ComposeBox` / `ChirpCard` / `ListView`. |
| Single-Responsibility / conjunction | **failed** | A faithful description joins distinct verbs/artifacts: design a compose surface **and** design a conversation-reading screen. |
| Output Size | fired | Estimated ~400–460 lines across two surfaces + 5 REQ-UX. |

Precedence: scope/concern outcomes win over size/token; multiple triggers fired → **NeedsDecompose**. The
evaluation was made independently of the parent's clustering; the persona instinct to hold the writing
experience as one picture carried no weight at the evaluation point, per the standing contract.

## Children materialized (one `_BRIEF.md` per child; subtree hub + contract authored)

- Hub: `_GLOBAL.md` (this workspace); Contract: `contracts/_MANIFEST.yaml` + `contracts/posting_conversation_seam.yaml`.
- `SUBTASK_compose_post` — compose & post surface + `REQ-UX-054..056`. Depends on: none.
- `SUBTASK_reply_conversation` — Chirp / conversation screen + `REQ-UX-057..058`. Depends on: none.
- `SUBTASK_posting_conversation_synthesis` — assemble `outputs/screens-posting-conversation.md`,
  consolidate `REQ-UX-054..058`, assert identities, author `SYNTHESIS.md`, fold this node. Depends on: both
  spokes.

## Resumption condition

Implicit: all child tasks reach a terminal lifecycle state. The synthesis child authors `SYNTHESIS.md` at
this fold location and folds `SUBTASK_posting_conversation` `SUSPENDED → COMPLETED`; the assembled
`outputs/screens-posting-conversation.md` and the consolidated `REQ-UX-054..058` register are this node's
result, consumed by the parent core-loop synthesis.
