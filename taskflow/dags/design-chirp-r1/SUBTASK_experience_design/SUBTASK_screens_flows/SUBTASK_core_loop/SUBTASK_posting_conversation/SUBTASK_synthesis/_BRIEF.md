# Task: Synthesis — assemble the posting/conversation surfaces, assert identities, and fold

## Task Specification

**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective

Assemble the two spoke outputs into the one `../outputs/screens-posting-conversation.md`, consolidate the
`REQ-UX-054..058` register, assert this subtree's identities with recorded evidence, and fold this node
(`SUBTASK_posting_conversation`) to COMPLETED.

### Context

The verification gate and fold for the writing-and-reading-in-context subtree (see `../_GLOBAL.md`,
`../contracts/`). The two spokes each designed one surface against the frozen screen inventory and
component library and the internal contract; your job is to integrate their outputs into the single
deliverable the parent core-loop subtree expects, verify the contract's identities mechanically, and
resolve this decomposing node.

**Dependencies**: `SUBTASK_compose_post`, `SUBTASK_reply_conversation` (both COMPLETED; read their outputs
directly — do not poll). **Dependents**: the parent core-loop synthesis (`../../SUBTASK_synthesis`), which
consumes this subtree's assembled part and consolidated register.

### Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, scope, success criteria, the assembled order. |
| Internal contract | `../contracts/` (read-only) | The surface→owner map, the `REQ-UX-054..058` sub-ranges, the identities to assert, the derived register, the trace rule. |
| Compose & post output | `../SUBTASK_compose_post/outputs/screens-compose-post.md` | The compose/post surface + `REQ-UX-054..056`. |
| Conversation output | `../SUBTASK_reply_conversation/outputs/screens-reply-conversation.md` | The Chirp/conversation screen + `REQ-UX-057..058`. |

### Output

- `../outputs/screens-posting-conversation.md` — the assembled `posting_conversation` part (compose/post
  surface, then the Chirp/conversation screen, then the consolidated `REQ-UX-054..058` register), in a
  readable order, repository-ready (no host/system/taskflow detail, no workspace paths, no attribution).
- `../SYNTHESIS.md` — the fold record at the fold location (this subtree root): the identity evidence and
  the fold of this node.

### Process (what the gate verifies — not a method script)

Assemble the parts in the contract's declared order, then assert each identity in `../contracts/` with
recorded evidence (pass/fail per identity, with the specific evidence): SURFACE_COVERAGE (both surfaces
present, each by its one owner, each with empty/error/loading or a recorded out-of-scope reason),
ID_UNIQUE_IN_RANGE (054..056 and 057..058, no collisions/gaps/out-of-range), NOT_SKELETAL (layout +
content + primary action + states per surface), UX_TESTABLE_AND_GATED (statement + stranger-checkable
acceptance_criteria + release_gating with a reason when false), UX_TRACES_TO_PROD (every REQ-UX names ≥1
REQ-PROD; the REQ-PROD-004-only entries are release_gating:false), COMPOSES_AGAINST_VOCAB (screens and
components by name; ComposeBox composed, not redefined), STATES_CONSISTENT (per-screen states consistent
with the global empty_error_loading_states patterns and the components' named states, incl. keep-the-draft),
HYGIENE. A fixable gap is remediated by decomposing a remediation subtree (author its briefs and amend the
plan), never a silent plug; a clean pass folds the node.

### Success criteria
- [ ] `../outputs/screens-posting-conversation.md` assembles both surfaces in the contract's order plus the
      consolidated `REQ-UX-054..058` register.
- [ ] Every identity in `../contracts/` is asserted with recorded pass/fail evidence in `../SYNTHESIS.md`;
      no identity is silently plugged.
- [ ] On a clean pass, the node is folded to COMPLETED (`../SYNTHESIS.md` authored at the fold location and
      the fold performed); on a fixable failure, a remediation subtree is materialised instead.
- [ ] Repository-ready hygiene throughout the assembled deliverable.

### Constraints
- Design-domain synthesis — integrate and verify; do not redesign the surfaces or mint new `REQ-UX` ids
  outside `054..058`.
- Repository-ready hygiene on all output content; plain, checkable human voice; run the avoid-ai-writing
  checklist over the assembled narrative before finalizing.
- Methodology: Experience Design (primary); Product Strategy (support). If the `design` loader is
  unavailable, synthesize from the bundle intent and competence and record the limitation (do not block).
