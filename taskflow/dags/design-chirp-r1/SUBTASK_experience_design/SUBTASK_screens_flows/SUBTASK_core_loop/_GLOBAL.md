# _GLOBAL.md — SUBTASK_core_loop (core-loop screens subtree hub)

## Project Context

**Status**: Active

### Objective

Design the **core social loop** a chirper performs every day — reading the home timeline, composing and
posting, replying and reading a conversation, liking, following, discovering people to follow, and
viewing a profile — as **designed screens** (each with its layout, content, primary action, and its
**empty, error, and loading states**), to the bar of *designed screens, not a skeleton*. This subtree
produces the single deliverable `outputs/screens-core-loop.md` — the `core_loop` part of the parent
subtree's `screens_and_flows` section — and the `REQ-UX-051..064` register (14 ids).

This node (`SUBTASK_core_loop`) evaluated its brief against the decomposition triggers and found it spans
**seven distinct surfaces**, each a separate design responsibility mapping to its own `REQ-PROD-*`: a
fired Scope-Based trigger (the enumerated-concerns rule), a failed Distinct-Concerns test, a failed
Single-Responsibility test, and an over-400-line estimated deliverable. It therefore decomposes. The four
spokes below each design one coherent cluster of the loop; `SUBTASK_synthesis` assembles their outputs
into the one `outputs/screens-core-loop.md`, consolidates `REQ-UX-051..064`, asserts the identities, and
folds this node to COMPLETED.

**This hub is this decomposing node's own `_GLOBAL.md`. Ancestor hubs govern above it — the screens-&-flows
hub is `../_GLOBAL.md`, the experience-design hub is `../../_GLOBAL.md`, the whole-design hub is
`../../../_GLOBAL.md`. On any conflict, the ancestor wins.** Likewise the ancestor contracts
(`../contracts/` screens-&-flows seam, `../../contracts/` experience-design seam, `../../../contracts/`
whole-design seam) bind this subtree; this subtree's `contracts/` extends them additively and never
overrides them.

### What this subtree designs into (grounding, from the dependencies)

chirp is a **hosted, public, account-based consumer web application** — a Twitter-style microblog. The
core loop is the activity the product exists for: *post short messages, read a timeline, follow people,
like what you like.* It must be fast, behave sensibly when there is nothing new or the person is brand
new, and recover visibly when something fails.

The two shared vocabularies this subtree composes against are **already frozen upstream** and MUST NOT be
redefined here (only referred to by name; a genuinely needed screen/component absent from them is an
additive amendment to this subtree's contract, never a silent invention):

- the **Screen inventory** — canonical screens, routes, archetypes, auth states — in
  `../../SUBTASK_ia_interaction/outputs/ia-interaction.md` (COMPLETED). The core-loop screens it names:
  Home timeline (`/`), Compose (`/compose` + overlay dialog), Chirp / conversation (`/@:handle/chirp/:id`),
  Explore / find people (`/explore`), Public profile (`/@:handle`), Own profile (`/@:handle` own),
  Followers (`/@:handle/followers`), Following (`/@:handle/following`).
- the **Component library** — named reusable components and their states — in
  `../../SUBTASK_visual_system/outputs/visual-system.md` (COMPLETED). The core-loop screens are assembled
  from: `NavShell`, `ListView`, `ChirpCard`, `ComposeBox`, `ProfileHeader`, `Avatar`, `IconButton`,
  `PrimaryButton`, `SecondaryButton`, `TextField`, `Dialog`, `Toast`, `InlineFeedback`, `InlineError`,
  `EmptyState`, `LoadingState`. A screen's empty/error/loading states are those components' own named
  states, not new inventions.

The authoritative upstream for journeys and requirements is
`../../../SUBTASK_product_requirements/outputs/product-requirements.md` — journey **J4** (the core loop)
and the `REQ-PROD-001..007, 042` each surface serves. Every `REQ-UX-051..064` this subtree mints MUST
reference ≥1 `REQ-PROD-*`.

The per-screen empty/error/loading states each spoke designs MUST be consistent with the product-wide
empty/loading/error **patterns** and the expired-session / transient-error (keep-the-draft) recovery
owned by the sibling `../SUBTASK_considered_states` spoke (`empty_error_loading_states` section, outside
this subtree) and with the components' own named states — spokes compose that global treatment, they do
not invent a conflicting per-screen pattern.

### Scope

**In scope (this subtree):** the `core_loop` part of `screens_and_flows` — a designed screen for each of
the seven core-loop surfaces, each with layout, content, primary action, and empty/error/loading states;
and the `REQ-UX-051..064` register, each entry testable by a stranger on the live product, flagged
`release_gating`, and tracing to ≥1 `REQ-PROD-*`.

**Out of scope (this subtree):**
- Front-end code or any implementation "how" — design only.
- The other `screens_and_flows` parts (get_in, account_lifecycle, safety_notifications), the
  `empty_error_loading_states` section (owned by sibling spokes of `../`), the IA/screen inventory, the
  component library, responsive behavior, and the accessibility standard — compose against them, do not
  redefine them or mint their ids.
- `REQ-UX` ids outside `051..064`, and every other area's ids.
- Assembling the parent `screens-flows.md` (the grandparent `../SUBTASK_synthesis`'s task).

### Success Criteria (this subtree)
- [ ] `outputs/screens-core-loop.md` carries the `core_loop` part, with each of the seven surfaces
      designed by exactly one spoke and assembled in a readable order.
- [ ] Home timeline, compose & post, reply & conversation, like/unlike, follow/unfollow, discovery, and
      view-profile (incl. followers/following) are each designed with their empty/error/loading states, OR
      recorded out-of-scope with a reason.
- [ ] Each screen specifies layout, content, and a primary action — designed, not a bare route name.
- [ ] Every `REQ-UX-051..064` is testable, `release_gating`-flagged, traces to ≥1 `REQ-PROD-*`, is unique,
      and falls within its owning spoke's assigned sub-range (honouring the non-gating staging of
      `REQ-PROD-042`/`004` where it applies).
- [ ] Every screen refers to the screen inventory and component library by name; nothing redefined; no new
      screen/component invented without an additive contract amendment.
- [ ] Repository-ready hygiene: no host/system/taskflow detail, no agent/DAG/run ids, no workspace paths,
      no attribution trailers, in all output content.

---

## Constraints and Requirements

- **Design, not code.** State what each screen must show and do and what "done" looks like from the
  user's side; defer the build to later code DAGs.
- **Compose against the frozen vocabularies and the contracts.** The screen inventory and component
  library are inputs, not things to redesign. The ancestor contracts fix the `REQ-UX` format, field set,
  section list, required surfaces, and trace rule; this subtree's `contracts/` only sub-ranges
  `051..064` among the spokes and maps surfaces to owners. Extend additively; never override.
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

Paths below are written from a spoke child's own workspace (`SUBTASK_core_loop/SUBTASK_<slug>/`).

| Source | Identity | Role |
|--------|----------|------|
| This subtree hub | `../_GLOBAL.md` | Shared context, constraints, the contract pointer, hygiene. |
| This subtree contract | `../contracts/` (read-only) | Surface→owner map, `REQ-UX-051..064` sub-ranges, shared-vocab rule, trace rule, identities. |
| Screens-&-flows hub | `../../_GLOBAL.md` | Parent context (the core_loop section-part, the frozen vocabularies). |
| Screens-&-flows contract | `../../contracts/` (read-only) | The core_loop section-part ownership, the `051..064` range, the `required_surfaces` checklist, the per-screen↔global-pattern cross-reference. |
| Screen inventory | `../../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The canonical screens/routes/archetypes/auth states every spoke designs into. |
| Component library | `../../../SUBTASK_visual_system/outputs/visual-system.md` | The named components (and their states) every screen is assembled from. |
| Product requirements | `../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Journey J4 and `REQ-PROD-001..007, 042` the screens serve and trace to. |

*(The screen inventory and component library are outputs of already-COMPLETED sibling tasks of this node's
parent; spokes read them directly as immutable inputs and MUST NOT poll for or re-verify their existence.)*

---

## Task Structure

### Overview

```
SUBTASK_core_loop/
├── _GLOBAL.md                          (this hub)
├── contracts/                          (READ-ONLY for descendants — the internal seam)
│   ├── _MANIFEST.yaml                  (surface→owner, REQ-UX-051..064 sub-ranges, identities)
│   └── core_loop_seam.yaml             (surface→owner map, id sub-ranges, shared-vocab rule, trace rule)
├── SUBTASK_timeline_reading/_BRIEF.md
├── SUBTASK_posting_conversation/_BRIEF.md
├── SUBTASK_social_actions/_BRIEF.md
├── SUBTASK_profiles_discovery/_BRIEF.md
├── SUBTASK_synthesis/_BRIEF.md
└── outputs/
    └── screens-core-loop.md            (the deliverable — written by SUBTASK_synthesis)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_timeline_reading` | none | Design the **Home timeline** reading surface — own + followed chirps, newest-first, in bounded pages, with the load-older and catch-up ("N new chirps") affordances — as a designed screen with its layout, content, primary action, and its empty (brand-new / nothing-followed), error (page/catch-up load failure), and loading (first-load skeleton) states (J4 / REQ-PROD-002). Owns `REQ-UX-051..053`. | `outputs/screens-timeline-reading.md` |
| `SUBTASK_posting_conversation` | none | Design the **writing-and-reading-in-context** surfaces — composing and publishing a chirp within the 280-char limit (inline at the timeline top, the Compose dialog, and the reply position), and the Chirp / conversation screen where a chirp is shown with its parent and replies and a reply is written — each with its layout, content, primary action, and its empty / error (over-limit, failed publish keep-the-draft, reply-to-a-gone-chirp not-found) / loading states (J4 / REQ-PROD-001, 003, 004). Owns `REQ-UX-054..058`. | `outputs/screens-posting-conversation.md` |
| `SUBTASK_social_actions` | none | Design the **in-place social-action behaviors** — like/unlike (idempotent, accurate count) and follow/unfollow (idempotent, cannot follow self) — as they appear on `ChirpCard`s and `ProfileHeader`/person cards, each with its default/active, error (failed action reverts with feedback), and loading (in-flight) states expressed over the components' own named states (J4 / REQ-PROD-005, 006). Owns `REQ-UX-059..060`. | `outputs/screens-social-actions.md` |
| `SUBTASK_profiles_discovery` | none | Design the **identity-and-find-people** surfaces — the Public and Own profile screens (identity block + their chirps), the Followers and Following lists, and the Explore / find-people discovery screen — each a designed screen with its layout, content, primary action, and its empty / error / loading states (J4 / REQ-PROD-007, 042). Owns `REQ-UX-061..064`. | `outputs/screens-profiles-discovery.md` |
| `SUBTASK_synthesis` | `SUBTASK_timeline_reading`, `SUBTASK_posting_conversation`, `SUBTASK_social_actions`, `SUBTASK_profiles_discovery` | **Verification gate + fold.** Assemble the four spoke outputs into `../outputs/screens-core-loop.md` in a readable order; consolidate the `REQ-UX-051..064` register; assert this subtree's identities with recorded evidence (surface coverage & single owner, id uniqueness/range, each screen not-skeletal, every `REQ-UX` testable + gated + traces to `REQ-PROD`, composed against the frozen vocabularies, per-screen states consistent with the global patterns, hygiene); remediate a fixable gap by decomposing a remediation subtree, never a silent plug; author `../SYNTHESIS.md` and fold this node to COMPLETED. | `../outputs/screens-core-loop.md` + `../SYNTHESIS.md` |

### Dependency Graph (human-readable; the table above is authoritative)

```
timeline_reading ─────┐
posting_conversation ─┤
social_actions ───────┼─> synthesis
profiles_discovery ───┘
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the contract in
`contracts/`. The four spokes are parts of ONE core-loop screen set and share a real seam: one
`core_loop` section of one output document, one `REQ-UX-051..064` id space that must stay collision-free
and `REQ-PROD`-traceable, one checklist of the seven core-loop surfaces that must be fully covered, two
frozen upstream vocabularies every spoke composes against, and one internal cross-reference (each
screen's empty/error/loading states must be consistent with the global patterns the sibling
`considered_states` spoke sets and with the components' own named states). That seam is frozen here,
before any spoke runs.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (surface-ownership map + `REQ-UX-051..064` sub-range partition +
identities), extending the ancestor `../contracts/` additively — never overriding it.

### Inherited Contracts

| Ancestor contract | Path (from a spoke) | What it binds here |
|---|---|---|
| Screens-&-flows seam | `../../contracts/` | The `REQ-UX-NNN` format and field set; the `core_loop` section-part and its `051..064` range assigned to this node; the `required_surfaces` checklist (the seven core-loop surfaces); the two shared vocabularies and their producers; the per-`REQ-UX` trace rule and the non-gating staging note (REQ-PROD-042/004); the per-screen↔global-pattern cross-reference. |
| Experience-design seam | `../../../contracts/` | The `REQ-<AREA>-NNN` scheme and the `experience-design.md` section list. |
| Whole-design seam | `../../../../contracts/` | The area id scheme across the whole design. |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | `yaml_schema` | kind, per-spoke ownership of surfaces / id sub-ranges, the identities synthesis asserts, derived register. |
| `contracts/core_loop_seam.yaml` | `yaml_schema` | the surface→owning-spoke map (covering every core-loop surface), the `REQ-UX-051..064` sub-range per spoke, the shared-vocabulary composition rule, the per-screen↔global-pattern cross-reference, and the per-`REQ-UX` trace rule. |

### Ownership (one producer per surface cluster / id range)

| Surface cluster / id range | Owning spoke |
|---|---|
| Home timeline (reading, pagination, catch-up) + `REQ-UX-051..053` | `SUBTASK_timeline_reading` |
| Compose & post + Reply & conversation + `REQ-UX-054..058` | `SUBTASK_posting_conversation` |
| Like/unlike + Follow/unfollow (in-place behaviors) + `REQ-UX-059..060` | `SUBTASK_social_actions` |
| Public/Own profile + Followers/Following + Explore/discovery + `REQ-UX-061..064` | `SUBTASK_profiles_discovery` |
| assembled `outputs/screens-core-loop.md`, consolidated `REQ-UX-051..064` register, `../SYNTHESIS.md` | `SUBTASK_synthesis` |

### Identities (asserted by `SUBTASK_synthesis` with recorded evidence; no silent plugs)
1. **SURFACE_COVERAGE** — each of the seven core-loop surfaces (home timeline, compose & post, reply &
   conversation, like/unlike, follow/unfollow, discovery/find-people, view profile incl.
   followers/following) is designed with its empty/error/loading states by its owning spoke, OR recorded
   out-of-scope with a reason. Every surface maps to exactly one spoke (no hole, no double-write).
2. **ID_UNIQUE_IN_RANGE** — every `REQ-UX-051..064` id is unique and within its owning spoke's sub-range;
   no collisions, no out-of-range ids, no gaps claimed as covered.
3. **NOT_SKELETAL** — each designed screen specifies layout, content, and a primary action, and its
   empty, error, and loading states — not a bare route name.
4. **UX_TESTABLE_AND_GATED** — every `REQ-UX-*` has a `statement`, an `acceptance_criteria` a stranger
   could check on the live product, and a `release_gating` flag (with a one-line reason when `false`).
5. **UX_TRACES_TO_PROD** — every `REQ-UX-*` references ≥1 `REQ-PROD-*`.
6. **COMPOSES_AGAINST_VOCAB** — every screen refers to screen-inventory screens by name and is built from
   component-library components by name; nothing is redefined and no new screen/component appears without
   an additive contract amendment.
7. **STATES_CONSISTENT** — each per-screen empty/error/loading state is consistent with the global
   patterns in the `empty_error_loading_states` section (sibling of `../`) and with the components' own
   named states.
8. **HYGIENE** — nothing in the output carries host/system/taskflow detail, workspace paths,
   agent/DAG/run ids, or an attribution trailer.

### Derived Artifacts

- Consolidated `REQ-UX-051..064` register — assembled by `SUBTASK_synthesis` from the four spokes'
  REQ-UX entries; consumed by the parent `../SUBTASK_synthesis` (screens-&-flows) when it builds the
  `core_loop` part of the `screens_and_flows` section and the consolidated `REQ-UX-040..089` register.

### Thin-Seam Note

The seam is not thin: one section of one document, a partitioned 14-id space, a seven-surface coverage
checklist, two frozen vocabularies, and a per-screen↔global-pattern cross-reference are a real contract.
Spokes MUST compose against `contracts/` and MUST NOT redefine the `REQ-UX` scheme, the id ranges, the
surface→owner map, or the shared vocabularies.

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| Timeline reading screen | Markdown | `SUBTASK_timeline_reading/outputs/screens-timeline-reading.md` | Home timeline designed + `REQ-UX-051..053`. |
| Posting & conversation screens | Markdown | `SUBTASK_posting_conversation/outputs/screens-posting-conversation.md` | Compose/post + conversation designed + `REQ-UX-054..058`. |
| Social-action behaviors | Markdown | `SUBTASK_social_actions/outputs/screens-social-actions.md` | Like & follow in-place designed + `REQ-UX-059..060`. |
| Profiles & discovery screens | Markdown | `SUBTASK_profiles_discovery/outputs/screens-profiles-discovery.md` | Profiles/followers/following + explore designed + `REQ-UX-061..064`. |
| Assembled deliverable | Markdown | `outputs/screens-core-loop.md` | The `core_loop` part assembled + the consolidated `REQ-UX-051..064` register. |
| Fold record | Markdown | `SYNTHESIS.md` | Identity evidence and the fold of this node. |

### Output Quality Criteria

- [ ] Each screen is designed (layout, content, primary action, empty/error/loading states), not skeletal.
- [ ] Every core-loop surface is covered or recorded out-of-scope with a reason.
- [ ] Every `REQ-UX-051..064` is testable, gated, traced, unique, and in-range.
- [ ] Everything composes against the frozen vocabularies by name.
- [ ] Repository-ready hygiene throughout.
