# _GLOBAL.md — SUBTASK_posting_conversation (writing-and-reading-in-context subtree hub)

## Project Context

**Status**: Active

### Objective

Design the surfaces where a chirper **writes** and **reads what was written in context**: composing and
publishing a chirp within the 280-character limit, and the Chirp / conversation screen where a chirp is
shown with the chirp it replies to and its replies and where a reply is written. Each is a **designed
screen** — its layout, content, primary action, and its **empty, error, and loading states** — to the bar
of *designed screens, not a skeleton*. This subtree produces the single deliverable
`outputs/screens-posting-conversation.md` (the `posting_conversation` part of the parent core-loop
section) and the `REQ-UX-054..058` register (5 ids).

### Why this node decomposed

This node (`SUBTASK_posting_conversation`) evaluated its brief against the decomposition triggers and found
it spans **two distinct surfaces**, each a separate design responsibility of a different screen archetype
and a different product-requirement trace:

- **compose_and_post** — a *modal/dialog* writing surface (`ComposeBox` in three placements, the 280-char
  affordance, the Post/Reply primary action), tracing `REQ-PROD-001`.
- **reply_and_conversation** — a *feed/list* reading-in-context screen (the Chirp / conversation screen: a
  chirp with its parent and replies, the reply affordance, the reply-to-a-gone-chirp not-found case),
  tracing `REQ-PROD-003` and the non-gating `REQ-PROD-004`.

A fired Scope-Based trigger (the enumerated-concerns rule: two distinct surfaces), a failed
Distinct-Concerns test (two archetypes a different specialist could design in parallel against the
already-frozen components), a failed Single-Responsibility test (compose **and** read-a-conversation are
two kinds of designed screen), and an estimated deliverable near the output-size ceiling drove the split.
Two spokes each design one surface; `SUBTASK_synthesis` assembles their outputs into the one
`outputs/screens-posting-conversation.md`, consolidates `REQ-UX-054..058`, asserts this subtree's
identities, and folds this node to COMPLETED.

**This hub is this decomposing node's own `_GLOBAL.md`. Ancestor hubs govern above it — the core-loop hub
is `../_GLOBAL.md`, the screens-&-flows hub is `../../_GLOBAL.md`, the experience-design hub is
`../../../_GLOBAL.md`, the whole-design hub is `../../../../_GLOBAL.md`. On any conflict, the ancestor
wins.** Likewise the ancestor contracts (`../contracts/` core-loop seam, and the seams above it) bind this
subtree; this subtree's `contracts/` extends them additively and never overrides them.

### What this subtree designs into (grounding, from the dependencies)

chirp is a **hosted, public, account-based consumer web application** — a Twitter-style microblog. Writing
a chirp and reading a conversation in context are the heart of the core loop: the product exists so people
post short messages and read and answer each other. These surfaces must enforce the published length limit
*before* submission, keep a person's draft safe when something fails, and make a conversation legible —
showing a reply against the chirp it answers rather than stranded in a flat list.

The two shared vocabularies this subtree composes against are **already frozen upstream** and MUST NOT be
redefined here (referred to by name only; a genuinely needed screen/component absent from them is an
additive amendment to this subtree's contract, never a silent invention):

- the **Screen inventory** — canonical screens, routes, archetypes, auth states — in
  `../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` (COMPLETED). The surfaces this subtree
  designs: **Compose** (`/compose` and an overlay dialog, archetype modal/dialog) and **Chirp /
  conversation** (`/@:handle/chirp/:id`, archetype feed/list, reachable in both auth states).
- the **Component library** — named reusable components and their states — in
  `../../../SUBTASK_visual_system/outputs/visual-system.md` (COMPLETED). These surfaces are assembled from:
  `ComposeBox`, `Dialog`, `ChirpCard`, `ListView`, `PrimaryButton`, `Avatar`, `IconButton`, `InlineError`,
  `InlineFeedback`, `Toast`, `EmptyState`, `LoadingState`, within the `NavShell`. A screen's
  empty/error/loading states are those components' own named states, not new inventions.

The authoritative upstream for journeys and requirements is
`../../../../SUBTASK_product_requirements/outputs/product-requirements.md` — journey **J4** (the core loop)
and `REQ-PROD-001` (post), `REQ-PROD-003` (reply), `REQ-PROD-004` (read a reply in its conversation —
`release_gating: false`). Every `REQ-UX-054..058` this subtree mints MUST reference ≥1 `REQ-PROD-*`.

The per-screen empty/error/loading states each spoke designs MUST be consistent with the product-wide
empty/loading/error **patterns** and the expired-session / transient-error (keep-the-draft) recovery owned
by the sibling `SUBTASK_considered_states` spoke (the `empty_error_loading_states` section, outside this
subtree, in the screens-&-flows subtree) and with the components' own named states — spokes compose that
global treatment, they do not invent a conflicting per-screen pattern.

### Scope

**In scope (this subtree):** the `posting_conversation` part of the core-loop screen set — the compose/post
surface and the Chirp/conversation surface, each with layout, content, primary action, and
empty/error/loading states; and the `REQ-UX-054..058` register, each entry testable by a stranger on the
live product, carrying a `release_gating` flag, and tracing to ≥1 `REQ-PROD-*`.

**Out of scope (this subtree):**
- Front-end code or any implementation "how" — design only.
- The other core-loop surfaces (home timeline, like/unlike, follow/unfollow, profiles, discovery) and the
  other screens-&-flows parts; the IA/screen inventory and the component library; the global
  `empty_error_loading_states` patterns (owned by `SUBTASK_considered_states`) — compose against them, do
  not redefine them or mint their ids.
- `REQ-UX` ids outside `054..058`, and every other area's ids.
- Assembling the parent `screens-core-loop.md` (the grandparent `../SUBTASK_synthesis`'s task).

### Success Criteria (this subtree)
- [ ] `outputs/screens-posting-conversation.md` carries the compose/post surface and the Chirp/conversation
      surface, each designed by exactly one spoke and assembled in a readable order (compose → conversation).
- [ ] Both surfaces are designed with their empty/error/loading states, OR a state is recorded
      out-of-scope with a reason.
- [ ] Each surface specifies layout, content, and a primary action — designed, not a bare route name.
- [ ] Every `REQ-UX-054..058` is testable, `release_gating`-flagged, traces to ≥1 `REQ-PROD-*`, is unique,
      and falls within its owning spoke's assigned sub-range (honouring `REQ-PROD-004`'s non-gating staging
      where it applies).
- [ ] Every screen refers to the screen inventory and component library by name; nothing redefined; no new
      screen/component invented without an additive contract amendment.
- [ ] Repository-ready hygiene: no host/system/taskflow detail, no agent/DAG/run ids, no workspace paths,
      no attribution trailers, in all output content.

---

## Constraints and Requirements

- **Design, not code.** State what each surface must show and do and what "done" looks like from the
  user's side; defer the build to later code DAGs.
- **Compose against the frozen vocabularies and the contracts.** The screen inventory and component library
  are inputs, not things to redesign. The ancestor contracts fix the `REQ-UX` format, field set, required
  surfaces, and trace rule; this subtree's `contracts/` only sub-ranges `054..058` between the two spokes
  and maps the two surfaces to owners. Extend additively; never override.
- **Methodology posture.** The Phase-B `design` methodology loader is **unavailable in the current
  reconstructed environment** (the loader syscall reports the agent domain unset). Per the ancestor hubs'
  recorded posture, each spoke designs from the named bundle intent — **Experience Design** (primary) and
  **Product Strategy** (support) — and its own product-design competence, and records the limitation; it
  does not block.
- **Repository-ready output content.** Everything in a spoke's output is written for the repository's
  readers; hygiene as in Success Criteria.
- **Avoid machine-writing tells.** Narrative output is written in a plain, checkable human voice; run the
  `avoid-ai-writing` checklist (or `references/patterns.md` P0/P1 by hand when the skill is absent) over
  every narrative deliverable before finalizing.

---

## Input Specifications

Paths below are written from a spoke child's own workspace
(`SUBTASK_posting_conversation/SUBTASK_<slug>/`).

| Source | Identity | Role |
|--------|----------|------|
| This subtree hub | `../_GLOBAL.md` | Shared context, constraints, the contract pointer, hygiene. |
| This subtree contract | `../contracts/` (read-only) | Surface→owner map, `REQ-UX-054..058` sub-ranges, shared-vocab rule, trace rule, identities. |
| Core-loop hub | `../../_GLOBAL.md` | Parent context (the `posting_conversation` part, the frozen vocabularies). |
| Core-loop contract | `../../contracts/` (read-only) | The `posting_conversation` surfaces, the `054..058` range, the per-screen↔global-pattern cross-reference, the trace rule. |
| Screen inventory | `../../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The Compose and Chirp/conversation screens, routes, archetypes, auth states, and the back/dialog and session-expiry conventions. |
| Component library | `../../../../SUBTASK_visual_system/outputs/visual-system.md` | `ComposeBox`, `Dialog`, `ChirpCard`, `ListView`, `PrimaryButton`, `InlineError`, `InlineFeedback`, `Toast`, `EmptyState`, `LoadingState` and their states. |
| Product requirements | `../../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J4 and `REQ-PROD-001, 003, 004` these surfaces serve and trace to. |

*(The screen inventory and component library are outputs of already-COMPLETED tasks; spokes read them
directly as immutable inputs and MUST NOT poll for or re-verify their existence.)*

---

## Task Structure

### Overview

```
SUBTASK_posting_conversation/
├── _GLOBAL.md                          (this hub)
├── contracts/                          (READ-ONLY for descendants — the internal seam)
│   ├── _MANIFEST.yaml                  (surface→owner, REQ-UX-054..058 sub-ranges, identities)
│   └── posting_conversation_seam.yaml  (surface→owner map, id sub-ranges, shared-vocab rule, trace rule)
├── SUBTASK_compose_post/_BRIEF.md
├── SUBTASK_reply_conversation/_BRIEF.md
├── SUBTASK_synthesis/_BRIEF.md
└── outputs/
    └── screens-posting-conversation.md (the deliverable — written by SUBTASK_synthesis)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_compose_post` | none | Design the **compose & post** surface — `ComposeBox` in its three placements (inline at the top of the timeline, the body of the **Compose** dialog, and the reply position), the remaining-character affordance that warns as the 280-char limit nears and blocks an over-limit or empty post, and the Post/Reply primary action — as a designed surface with its empty (placeholder, counter at full, Post disabled), error (over-limit; failed publish → keep-the-draft), and loading (publish in flight → Post busy, field briefly locked) states (J4.2 / REQ-PROD-001). Owns `REQ-UX-054..056`. | `SUBTASK_compose_post/outputs/screens-compose-post.md` |
| `SUBTASK_reply_conversation` | none | Design the **Chirp / conversation** screen (`/@:handle/chirp/:id`) — a chirp shown with the chirp it replies to and its replies, and replying from that screen — as a designed screen with its layout, content, primary action, and its empty (a chirp with no replies yet, shown as the root chirp with an invitation to reply), error (reply to a gone chirp → not-found tombstone / `InlineError`; a failed page load → `ListView` error with retry), and loading (`LoadingState` skeleton for root chirp and replies) states (J4.3 / REQ-PROD-003, 004). Owns `REQ-UX-057..058`. | `SUBTASK_reply_conversation/outputs/screens-reply-conversation.md` |
| `SUBTASK_synthesis` | `SUBTASK_compose_post`, `SUBTASK_reply_conversation` | **Verification gate + fold.** Assemble the two spoke outputs into `../outputs/screens-posting-conversation.md` in a readable order (compose → conversation); consolidate the `REQ-UX-054..058` register; assert this subtree's identities with recorded evidence (surface coverage & single owner, id uniqueness/range, each surface not-skeletal, every `REQ-UX` testable + gated + traces to `REQ-PROD`, composed against the frozen vocabularies, per-screen states consistent with the global patterns, hygiene); remediate a fixable gap by decomposing a remediation subtree, never a silent plug; author `../SYNTHESIS.md` and fold this node to COMPLETED. | `../outputs/screens-posting-conversation.md` + `../SYNTHESIS.md` |

### Dependency Graph (human-readable; the table above is authoritative)

```
compose_post ───────┐
reply_conversation ─┴─> synthesis
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the contract in `contracts/`.
The two spokes are parts of ONE writing-and-reading-in-context surface set and share a real seam: one
`posting_conversation` section of one output document, one `REQ-UX-054..058` id space that must stay
collision-free and `REQ-PROD`-traceable, one two-surface coverage checklist, two frozen upstream
vocabularies every spoke composes against, and one internal cross-reference (each surface's
empty/error/loading states must be consistent with the global patterns the sibling `considered_states`
spoke sets and with the components' own named states — the shared `ComposeBox` is the explicit shared
component: compose_post owns its design, reply_conversation composes it in the reply position). That seam
is frozen here, before any spoke runs.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (surface-ownership map + `REQ-UX-054..058` sub-range partition +
identities), extending the ancestor `../contracts/` additively — never overriding it.

### Inherited Contracts

| Ancestor contract | Path (from a spoke) | What it binds here |
|---|---|---|
| Core-loop seam | `../../contracts/` | The `posting_conversation` surfaces (compose_and_post, reply_and_conversation) and their `054..058` range assigned to this node; the two frozen vocabularies and their producers; the per-`REQ-UX` trace rule and the non-gating staging note (`REQ-PROD-004`); the per-screen↔global-pattern cross-reference. |
| Screens-&-flows seam | `../../../contracts/` | The `REQ-UX-NNN` format and field set; the `core_loop` section-part. |
| Experience-design seam | `../../../../contracts/` | The `REQ-<AREA>-NNN` scheme and the `experience-design.md` section list. |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | `yaml_schema` | kind, per-spoke ownership of surfaces / id sub-ranges, the identities synthesis asserts, derived register. |
| `contracts/posting_conversation_seam.yaml` | `yaml_schema` | the surface→owning-spoke map (both surfaces), the `REQ-UX-054..058` sub-range per spoke, the shared-vocabulary composition rule, the shared-`ComposeBox` ownership note, the per-screen↔global-pattern cross-reference, and the per-`REQ-UX` trace rule. |

### Ownership (one producer per surface / id range)

| Surface / id range | Owning spoke |
|---|---|
| compose_and_post (the `ComposeBox` writing surface in its three placements) + `REQ-UX-054..056` | `SUBTASK_compose_post` |
| reply_and_conversation (the Chirp / conversation screen) + `REQ-UX-057..058` | `SUBTASK_reply_conversation` |
| assembled `outputs/screens-posting-conversation.md`, consolidated `REQ-UX-054..058` register, `../SYNTHESIS.md` | `SUBTASK_synthesis` |

### Identities (asserted by `SUBTASK_synthesis` with recorded evidence; no silent plugs)
1. **SURFACE_COVERAGE** — the compose/post surface and the Chirp/conversation surface are each designed with
   their empty/error/loading states by their owning spoke, OR a state is recorded out-of-scope with a
   reason. Each surface maps to exactly one spoke (no hole, no double-write).
2. **ID_UNIQUE_IN_RANGE** — every `REQ-UX-054..058` id is unique and within its owning spoke's sub-range
   (compose 054..056, conversation 057..058); no collisions, no out-of-range ids, no gaps claimed as
   covered.
3. **NOT_SKELETAL** — each designed surface specifies layout, content, and a primary action, and its empty,
   error, and loading states — not a bare route name.
4. **UX_TESTABLE_AND_GATED** — every `REQ-UX-*` has a `statement`, an `acceptance_criteria` a stranger could
   check on the live product, and a `release_gating` flag (with a one-line reason when `false`).
5. **UX_TRACES_TO_PROD** — every `REQ-UX-*` references ≥1 `REQ-PROD-*`.
6. **COMPOSES_AGAINST_VOCAB** — every screen refers to screen-inventory screens by name and is built from
   component-library components by name; nothing is redefined and no new screen/component appears without an
   additive contract amendment. In particular both spokes compose the frozen `ComposeBox` rather than
   redefining it.
7. **STATES_CONSISTENT** — each per-screen empty/error/loading state is consistent with the global patterns
   in the `empty_error_loading_states` section (owned by `SUBTASK_considered_states`, outside this subtree)
   and with the components' own named states — in particular the keep-the-draft recovery on a failed publish.
8. **HYGIENE** — nothing in the output carries host/system/taskflow detail, workspace paths, agent/DAG/run
   ids, or an attribution trailer.

### Derived Artifacts

- Consolidated `REQ-UX-054..058` register — assembled by `SUBTASK_synthesis` from the two spokes' REQ-UX
  entries; consumed by the parent `../SUBTASK_synthesis` (core-loop) when it builds the `core_loop` part of
  the `screens_and_flows` section and the consolidated `REQ-UX-051..064` register.

### Thin-Seam Note

The seam is not thin: one section of one document, a partitioned 5-id space, a two-surface coverage
checklist, two frozen vocabularies, one explicitly shared component (`ComposeBox`), and a
per-screen↔global-pattern cross-reference are a real contract. Spokes MUST compose against `contracts/` and
MUST NOT redefine the `REQ-UX` scheme, the id ranges, the surface→owner map, or the shared vocabularies.

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| Compose & post surface | Markdown | `SUBTASK_compose_post/outputs/screens-compose-post.md` | Compose/post designed + `REQ-UX-054..056`. |
| Chirp / conversation screen | Markdown | `SUBTASK_reply_conversation/outputs/screens-reply-conversation.md` | Conversation screen + reply designed + `REQ-UX-057..058`. |
| Assembled deliverable | Markdown | `outputs/screens-posting-conversation.md` | The `posting_conversation` part assembled + the consolidated `REQ-UX-054..058` register. |
| Fold record | Markdown | `SYNTHESIS.md` | Identity evidence and the fold of this node. |

### Output Quality Criteria

- [ ] Each surface is designed (layout, content, primary action, empty/error/loading states), not skeletal.
- [ ] Both surfaces are covered or a state recorded out-of-scope with a reason.
- [ ] Every `REQ-UX-054..058` is testable, gated, traced, unique, and in-range.
- [ ] Everything composes against the frozen vocabularies by name.
- [ ] Repository-ready hygiene throughout.
