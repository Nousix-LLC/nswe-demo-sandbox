# _GLOBAL.md — SUBTASK_screens_flows (screens-&-flows subtree hub)

## Project Context

**Status**: Active

### Objective

Design the **actual screens and flows** for every journey a releasable chirp needs — each screen's
layout, content, and primary action, and **each screen's empty, error, and loading states** — to the
bar of *designed screens, not a skeleton*. This subtree produces the single deliverable
`outputs/screens-flows.md` (the `screens_and_flows` and `empty_error_loading_states` sections of the
parent subtree's `experience-design.md`) and the `REQ-UX-040..089` register.

This node (`SUBTASK_screens_flows`) evaluated its brief against the decomposition triggers and found it
spans many distinct surfaces — the entry/authentication flows, the core social loop, the
account-lifecycle surfaces, the safety/notifications surfaces, and a cross-cutting empty/error/loading
pattern section — a fired Scope-Based trigger (the enumerated-concerns rule), a failed Distinct-Concerns
test, a failed Single-Responsibility test, and an over-400-line deliverable. It therefore decomposes.
The five spokes below each design one cluster of surfaces (or the cross-cutting pattern section);
`SUBTASK_synthesis` assembles their outputs into the one `outputs/screens-flows.md`, consolidates the
`REQ-UX-040..089` register, verifies the identities, and folds this node to COMPLETED.

**This hub is this decomposing node's own `_GLOBAL.md`. The parent subtree's hub is `../_GLOBAL.md`
(experience-design) and the whole-design hub is `../../_GLOBAL.md`; both govern above this one, and on
any conflict the ancestor wins.**

### What this subtree designs into (grounding, from the dependencies)

chirp is a **hosted, public, account-based consumer web application** — a Twitter-style microblog. At
commit `c805525` the live product presents **three screens** (timeline `/`, a compose+sign-in view
`/compose`, a profile `/user/:id`) above a persistent nav bar. This subtree takes that three-screen
skeleton to a designed, releasable set of screens and flows: the full account lifecycle, the core loop,
onboarding, settings, safety, notifications, export/deletion, and considered empty/error/loading states
throughout — each a designed screen with a testable `REQ-UX-*`.

The two shared vocabularies this subtree composes against are **already frozen upstream** and MUST NOT be
redefined here:

- the **Screen inventory** — the canonical set of screens, routes, archetypes, and auth states — in
  `../SUBTASK_ia_interaction/outputs/ia-interaction.md` (COMPLETED);
- the **Component library** — the named reusable components and their states — in
  `../SUBTASK_visual_system/outputs/visual-system.md` (COMPLETED).

Every screen designed in this subtree refers to screens by their **screen-inventory names** and is built
from **component-library components by name**; no spoke invents a new screen or component outside those
vocabularies without an additive amendment to this subtree's contract.

The authoritative upstream for journeys and requirements is
`../../SUBTASK_product_requirements/outputs/product-requirements.md` (personas P1–P5, journeys J1–J10,
the `REQ-PROD-001..042` register). Every `REQ-UX-*` this subtree mints MUST reference ≥1 `REQ-PROD-*`.

### Scope

**In scope (this subtree):**
- The `screens_and_flows` section: a designed screen for every journey a releasable chirp needs — the
  entry/auth flows, the core loop, account-lifecycle surfaces, and safety/notifications surfaces — each
  with its **layout, content, primary action**, and its **empty, error, and loading states**.
- The `empty_error_loading_states` section: the product-wide empty/loading/error **patterns** and the
  expired-session / transient-error recovery that preserves a drafted chirp, applied across the screens.
- The `REQ-UX-040..089` register: each entry testable by a stranger on the live product, with a
  `release_gating` flag and ≥1 `REQ-PROD-*` trace.

**Out of scope (this subtree):**
- Front-end code or any implementation "how" — design only.
- The IA/screen inventory (owned by `../SUBTASK_ia_interaction`), the visual system/component library
  (owned by `../SUBTASK_visual_system`), responsive behavior (owned by `../SUBTASK_responsive`), and the
  accessibility standard (owned by `../SUBTASK_accessibility`). Where a screen depends on one of those,
  compose against it and refer to it; do not redefine it or mint its ids.
- `REQ-UX` ids outside `040..089`, and every other area's ids (`REQ-PROD-*`, `REQ-DOM-*`, `REQ-ID-*`,
  `REQ-OPS-*`, `BAR-*`).
- Assembling the parent `experience-design.md` or the repo `design/` tree (the grandparent's tasks).

### Success Criteria (this subtree)
- [ ] `outputs/screens-flows.md` carries the `screens_and_flows` and `empty_error_loading_states`
      sections, assembled in order, each part written by exactly one spoke.
- [ ] Every required surface in `../contracts/ux_section_and_id_map.yaml` `required_surfaces` is designed
      with its empty/error/loading states, OR recorded out-of-scope with a reason.
- [ ] Each screen specifies layout, content, and a primary action — designed, not a bare route name.
- [ ] Every `REQ-UX-040..089` is testable, `release_gating`-flagged, traces to ≥1 `REQ-PROD-*`, is
      unique, and falls within its owning spoke's assigned sub-range.
- [ ] Every screen refers to the screen inventory and component library by name; nothing redefined; no
      new screen/component invented without an additive contract amendment.
- [ ] Repository-ready hygiene: no host/system/taskflow detail, no agent/DAG/run ids, no workspace
      paths, no attribution trailers, in all output content.

---

## Constraints and Requirements

- **Design, not code.** State what each screen must show and do and what "done" looks like from the
  user's side; defer the build to later code DAGs.
- **Compose against the frozen vocabularies.** The screen inventory and the component library are inputs,
  not things to redesign. A screen is described as an arrangement of named components realising a named
  inventory screen; its states are the components' named states (`EmptyState`, `LoadingState`,
  `InlineError`, the `ListView`/`ChirpCard` states, etc.), not new inventions.
- **Compose against the parent and this contract.** The parent `../contracts/` fixes the `REQ-UX` format,
  field set, section list, required surfaces, and trace rule. This subtree's `contracts/` only
  sub-ranges the `040..089` id space among the spokes and maps surfaces to owners; it extends the parent
  additively and never overrides it.
- **Methodology posture.** The Phase-B `design` methodology loader is **unavailable in the current
  reconstructed environment** (the loader syscall reports the agent domain unset). Per the parent hub's
  recorded posture, each spoke designs from the named bundle intent — **Experience Design** (primary);
  **Product Strategy** and **Identity & Trust** (support, so the auth/account screens align with the
  identity requirements) — and its own product-design competence, and records the limitation; it does
  not block.
- **Repository-ready output content.** Everything that lands in `screens-flows.md` is written for the
  repository's readers; hygiene as in Success Criteria.
- **Avoid machine-writing tells.** Narrative output is written in a plain, checkable human voice; run the
  `avoid-ai-writing` checklist (or `references/patterns.md` P0/P1 by hand when the skill is absent) over
  every narrative deliverable before finalizing.

---

## Input Specifications

| Source | Identity | Role |
|--------|----------|------|
| This subtree hub | `../_GLOBAL.md` (from a spoke's view) | Shared context, constraints, the contract pointer, hygiene. |
| This subtree contract | `../contracts/` (read-only) | Section/surface ownership, `REQ-UX-040..089` sub-ranges, the internal seam, identities. |
| Screen inventory | `../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The canonical screens/routes/archetypes/auth states every spoke designs into. |
| Component library | `../../SUBTASK_visual_system/outputs/visual-system.md` | The named components (and their states) every screen is assembled from. |
| Product requirements | `../../../SUBTASK_product_requirements/outputs/product-requirements.md` | Personas, journeys J1–J10, `REQ-PROD-001..042` the screens serve and trace to. |
| Parent subtree hub | `../../_GLOBAL.md` | Whole experience-design context and hygiene rules. |
| Parent contract | `../../contracts/` (read-only) | The `REQ-UX` scheme, field set, section list, required surfaces, trace rule. |

*(Paths above are written from a spoke child's own workspace. The screen inventory and component library
are outputs of already-COMPLETED sibling tasks of this node; spokes read them directly as immutable
inputs and MUST NOT poll for or re-verify their existence.)*

---

## Task Structure

### Overview

```
SUBTASK_screens_flows/
├── _GLOBAL.md                          (this hub)
├── contracts/                          (READ-ONLY for descendants — the internal seam)
│   ├── _MANIFEST.yaml                  (section/surface ownership, REQ-UX-040..089 sub-ranges, identities)
│   └── screens_seam.yaml               (section-part→owner, surface→owner, id sub-ranges, shared-vocab rule, trace rule)
├── SUBTASK_get_in/_BRIEF.md
├── SUBTASK_core_loop/_BRIEF.md
├── SUBTASK_account_lifecycle/_BRIEF.md
├── SUBTASK_safety_notifications/_BRIEF.md
├── SUBTASK_considered_states/_BRIEF.md
├── SUBTASK_synthesis/_BRIEF.md
└── outputs/
    └── screens-flows.md                (the deliverable — written by SUBTASK_synthesis)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_get_in` | none | Design the entry & authentication flows a releasable chirp needs — first-visit landing, sign-up, sign-in, account recovery (and setting a new credential), and sign-out — each a designed screen with its layout, content, primary action, and empty/error/loading states, composing against the screen inventory and component library. Bundles: Experience Design (primary); Identity & Trust, Product Strategy (support). Owns `REQ-UX-040..050`. | `outputs/screens-get-in.md` |
| `SUBTASK_core_loop` | none | Design the core social loop — the home timeline incl. bounded catch-up, compose & post, reply & reading a conversation, like/unlike, follow/unfollow, discovery / find people, and viewing a profile (incl. followers/following) — each a designed screen with its layout, content, primary action, and empty/error/loading states. Bundle: Experience Design (primary); Product Strategy (support). Owns `REQ-UX-051..064`. | `outputs/screens-core-loop.md` |
| `SUBTASK_account_lifecycle` | none | Design the account-lifecycle surfaces — first-run onboarding off the empty state, edit profile, the settings hub and its sub-sections (account & contact, notification preferences, sessions & devices), data export, and account deletion with a confirmed, explained outcome — each a designed screen with its layout, content, primary action, and empty/error/loading states. Bundles: Experience Design (primary); Identity & Trust, Product Strategy (support). Owns `REQ-UX-065..077`. | `outputs/screens-account-lifecycle.md` |
| `SUBTASK_safety_notifications` | none | Design the safety, notifications, and public-explanatory surfaces — the notifications activity surface, reporting content/accounts, block/mute and the blocked-&-muted management screen, the user-facing help/support entry, the rules & terms screen, and the not-found screen — each a designed screen with its layout, content, primary action, and empty/error/loading states. Bundles: Experience Design (primary); Identity & Trust, Product Strategy (support). Owns `REQ-UX-078..085`. | `outputs/screens-safety-notifications.md` |
| `SUBTASK_considered_states` | none | Design the `empty_error_loading_states` section: the product-wide empty / loading / error **patterns** every screen obeys, and the expired-session / transient-error recovery that routes to sign-in and preserves a drafted chirp — expressed over the component library's state components and the IA's session-expiry convention, as the cross-cutting treatment the per-screen designs reference. Bundle: Experience Design (primary). Owns `REQ-UX-086..089`. | `outputs/empty-error-loading-states.md` |
| `SUBTASK_screens_flows_synthesis` (workspace dir `SUBTASK_synthesis/`) | `SUBTASK_get_in`, `SUBTASK_core_loop`, `SUBTASK_account_lifecycle`, `SUBTASK_safety_notifications`, `SUBTASK_considered_states` | **Verification gate + fold.** Assemble the five outputs into `../outputs/screens-flows.md` (`screens_and_flows` then `empty_error_loading_states`, in order); consolidate the full `REQ-UX-040..089` register; assert this subtree's identities with recorded evidence (section/part coverage & single owner, id uniqueness/range, every required surface designed-with-states or recorded out-of-scope, each screen not-skeletal, every `REQ-UX` testable + gated + traces to `REQ-PROD`, composed against the frozen vocabularies, per-screen states consistent with the global patterns, hygiene); remediate a fixable gap by decomposing a remediation subtree, never a silent plug; author `../SYNTHESIS.md` and fold this node to COMPLETED. Bundle: Experience Design. | `../outputs/screens-flows.md` + `../SYNTHESIS.md` |

### Dependency Graph (human-readable; the table above is authoritative)

```
get_in ──────────────┐
core_loop ───────────┤
account_lifecycle ───┼─> synthesis
safety_notifications ┤
considered_states ───┘
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the contract in
`contracts/`. The five spokes are parts of ONE screens-&-flows design and share a real seam: two sections
of one output document, one `REQ-UX-040..089` id space that must stay collision-free and
`REQ-PROD`-traceable, one required-surface checklist that must be fully covered, two frozen upstream
vocabularies every spoke composes against (screen inventory, component library), and one internal
cross-reference (each screen's empty/error/loading states must be consistent with the global patterns the
`considered_states` spoke sets). That seam is frozen before any spoke runs.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (section/surface-ownership map + `REQ-UX-040..089` sub-range partition +
identities), extending the parent `../contracts/` additively — never overriding it.

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Experience-design seam | `../contracts/` | The `REQ-UX-NNN` format and field set; the `experience-design.md` section list (this subtree owns `screens_and_flows` + `empty_error_loading_states`); the `REQ-UX-040..089` range assigned to this node; the `required_surfaces` checklist; the two shared vocabularies and their producers; the per-`REQ-UX` trace rule. |
| Whole-design seam | `../../contracts/` | The `REQ-<AREA>-NNN` scheme and the `experience-design.md` required-section list. |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | `yaml_schema` | kind, per-spoke ownership of section-parts / surfaces / id sub-ranges, the identities synthesis asserts, derived register. |
| `contracts/screens_seam.yaml` | `yaml_schema` | the section-part→owning-spoke map, the surface→owning-spoke map (covering every required surface and every screen-inventory screen), the `REQ-UX-040..089` sub-range per spoke, the shared-vocabulary composition rule, and the per-`REQ-UX` trace rule. |

### Ownership (one producer per artifact / id range)

| Artifact / id range | Owning spoke |
|---|---|
| Entry & auth screens (Landing, Sign up, Sign in, Recover access, Set new credential, Sign out) + `REQ-UX-040..050` | `SUBTASK_get_in` |
| Core-loop screens (Home timeline, Compose, Chirp/conversation, Explore, Public/Own profile, Followers, Following; like & follow behaviors) + `REQ-UX-051..064` | `SUBTASK_core_loop` |
| Account-lifecycle screens (Onboarding, Edit profile, Settings hub, Account & contact, Notification preferences, Sessions & devices, Export, Delete account) + `REQ-UX-065..077` | `SUBTASK_account_lifecycle` |
| Safety/notifications/public-explanatory screens (Notifications, Report, Block/mute, Blocked & muted, Help & support, Rules & terms, Not found) + `REQ-UX-078..085` | `SUBTASK_safety_notifications` |
| `empty_error_loading_states` section (global patterns + expired-session/transient-error recovery) + `REQ-UX-086..089` | `SUBTASK_considered_states` |
| assembled `outputs/screens-flows.md`, consolidated `REQ-UX-040..089` register, `../SYNTHESIS.md` | `SUBTASK_synthesis` |

### Identities (asserted by `SUBTASK_synthesis` with recorded evidence; no silent plugs)
1. **SECTION_PART_COVERAGE** — `screens_and_flows` and `empty_error_loading_states` are both present and
   assembled in order; every section-part maps to exactly one spoke (no hole, no double-write).
2. **ID_UNIQUE_IN_RANGE** — every `REQ-UX-040..089` id is unique and within its owning spoke's sub-range;
   no collisions, no out-of-range ids, no gaps claimed as covered.
3. **SURFACE_COVERAGE** — every surface in the parent `required_surfaces` checklist (and every
   screen-inventory screen) is designed with its empty/error/loading states by its owning spoke, OR
   recorded out-of-scope with a reason.
4. **NOT_SKELETAL** — each designed screen specifies layout, content, and a primary action, and its
   empty, error, and loading states — not a bare route name.
5. **UX_TESTABLE_AND_GATED** — every `REQ-UX-*` has a `statement`, an `acceptance_criteria` a stranger
   could check on the live product, and a `release_gating` flag (with a one-line reason when `false`).
6. **UX_TRACES_TO_PROD** — every `REQ-UX-*` references ≥1 `REQ-PROD-*`.
7. **COMPOSES_AGAINST_VOCAB** — every screen refers to screen-inventory screens by name and is built from
   component-library components by name; nothing is redefined and no new screen/component appears without
   an additive contract amendment.
8. **STATES_CONSISTENT** — each per-screen empty/error/loading state is consistent with the global
   patterns in the `empty_error_loading_states` section and with the components' own named states.
9. **HYGIENE** — nothing in `screens-flows.md` carries host/system/taskflow detail, workspace paths,
   agent/DAG/run ids, or an attribution trailer.

### Derived Artifacts

- Consolidated `REQ-UX-040..089` register — assembled by `SUBTASK_synthesis` from the five spokes' REQ-UX
  entries; consumed by the grandparent `SUBTASK_synthesis` (experience-design) when it builds the whole
  `requirements_and_acceptance_criteria` register.

### Thin-Seam Note

The seam is not thin: two sections of one document, a partitioned 50-id space, a required-surface
checklist, two frozen vocabularies, and a per-screen↔global-pattern cross-reference are a rich contract.
Spokes MUST compose against `contracts/` and MUST NOT redefine the `REQ-UX` scheme, the section list, the
id ranges, or the shared vocabularies.

---

## Output Specifications

| Deliverable | Format | Location | Description |
|-------------|--------|----------|-------------|
| Entry & auth screens | Markdown | `SUBTASK_get_in/outputs/screens-get-in.md` | Designed screens + `REQ-UX-040..050`. |
| Core-loop screens | Markdown | `SUBTASK_core_loop/outputs/screens-core-loop.md` | Designed screens + `REQ-UX-051..064`. |
| Account-lifecycle screens | Markdown | `SUBTASK_account_lifecycle/outputs/screens-account-lifecycle.md` | Designed screens + `REQ-UX-065..077`. |
| Safety/notifications screens | Markdown | `SUBTASK_safety_notifications/outputs/screens-safety-notifications.md` | Designed screens + `REQ-UX-078..085`. |
| Empty/error/loading states | Markdown | `SUBTASK_considered_states/outputs/empty-error-loading-states.md` | The `empty_error_loading_states` section + `REQ-UX-086..089`. |
| Assembled deliverable | Markdown | `outputs/screens-flows.md` | Both sections assembled + the consolidated `REQ-UX-040..089` register. |
| Fold record | Markdown | `SYNTHESIS.md` | Identity evidence and the fold of this node. |

### Output Quality Criteria

- [ ] Each screen is designed (layout, content, primary action, empty/error/loading states), not skeletal.
- [ ] Every required surface is covered or recorded out-of-scope with a reason.
- [ ] Every `REQ-UX-040..089` is testable, gated, traced, unique, and in-range.
- [ ] Everything composes against the frozen vocabularies by name.
- [ ] Repository-ready hygiene throughout.
