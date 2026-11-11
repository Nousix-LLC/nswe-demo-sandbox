# _GLOBAL.md — SUBTASK_experience_design (experience-design subtree hub)

## Project Context

**Status**: Active

### Objective

Design how chirp (`Nousix-LLC/nswe-demo`) **looks and behaves to a user**, to the bar of *designed
screens, not a bare skeleton*. This subtree produces the single design document
`design/experience-design.md` (assembled later by the parent subtree's `SUBTASK_design_pr`) and the
`REQ-UX-*` register, composing against the parent contract at `../contracts/` and tracing every
`REQ-UX-*` to the product requirements (`REQ-PROD-*`).

This node (`SUBTASK_experience_design`) evaluated its brief against the decomposition triggers and found
it spans five distinct design disciplines plus a large, cross-referencing deliverable; it therefore
decomposes. The children below each own one discipline; `SUBTASK_synthesis` assembles their outputs into
the one `outputs/experience-design.md`, consolidates the `REQ-UX-*` register, verifies the identities,
and folds this node to COMPLETED. **This hub is the decomposing node's own `_GLOBAL.md`; the parent
subtree's hub is `../_GLOBAL.md` and governs the whole design.**

### What the product is (grounding, from the dependency)

chirp is a **hosted, public, account-based consumer web application** — a Twitter-style microblog:
post short messages (≤280 chars), read a paginated home timeline of people you follow, reply, like,
follow, view profiles. At commit `c805525` the live product is a WebAssembly single-page app
(`crates/chirp-frontend`, on the in-house `ferric` UI framework + router) over a REST backend
(`crates/chirp-server`), presenting **three screens** today — timeline `/`, a compose+sign-in view
`/compose`, and a profile view `/user/:id` — above a persistent nav bar. The experience design takes the
product from that three-screen skeleton to a designed, releasable consumer web product: the full
account lifecycle, onboarding, settings, safety, notifications, export/deletion, and considered
empty/error/loading states throughout, each as a designed screen with a testable `REQ-UX-*`.

The authoritative upstream is `../SUBTASK_product_requirements/outputs/product-requirements.md`
(personas P1–P5, journeys J1–J10, the `REQ-PROD-001..042` register). Every `REQ-UX-*` this subtree
mints MUST reference ≥1 `REQ-PROD-*`.

### Scope

**In scope (this subtree):**
- Information architecture & interaction model (structure, navigation, interaction conventions,
  signed-out vs signed-in shells, route/URL structure from the user's side).
- The screens & flows for every journey a releasable product of this kind needs — sign-up / sign-in /
  recovery / sign-out, the posting & timeline/reading loops, reply & conversation reading, profile &
  profile editing, follow / discovery, onboarding off the empty state, settings, data export, account
  deletion, notifications, report/block, and the minimal operator/support surface **as far as it has a
  user-facing UX** — each **with its empty / error / loading states**, designed not skeletal.
- A visual language & design system (type, color, spacing, iconography, component library, tone).
- Responsive layout (phone-first through larger viewports).
- Accessibility to a stated standard.
- The `REQ-UX-*` register with testable acceptance criteria, release-gating flags, and `REQ-PROD-*`
  traces.

**Out of scope (this subtree):**
- Front-end code or any implementation "how" (defer to later code DAGs) — design only.
- The requirements owned by sibling design areas (`REQ-PROD-*`, `REQ-DOM-*`, `REQ-ID-*`, `REQ-OPS-*`,
  `BAR-*`). Where an experience depends on one of those, design the surface and reference the owning
  area; do not mint its ids.
- Assembling the repo `design/` tree / opening the PR (parent's `SUBTASK_design_pr`); filing the board
  backlog (parent's `SUBTASK_delivery_backlog`); the live-product measurement (parent's
  `SUBTASK_synthesis`). This subtree's synthesis verifies only the experience-design output and folds.

### Success Criteria (this subtree)
- [ ] `outputs/experience-design.md` carries all required sections from `../contracts/design_artifact_map.yaml`
      for `experience-design.md`, in order, each owned by exactly one child.
- [ ] Screens & flows cover sign-up/in/recovery/sign-out, the posting/timeline/reply loops, profile &
      editing, follow/discovery, onboarding, settings, export, deletion, notifications, report/block —
      each with empty/error/loading states, designed not skeletal.
- [ ] A visual language/design system, responsive behavior, and an accessibility standard are stated.
- [ ] Every `REQ-UX-*` has a testable acceptance criterion a stranger could check, a `release_gating`
      flag, and references ≥1 `REQ-PROD-*`. Ids are unique and within the assigned ranges.
- [ ] Composes against `../contracts/`; the parent `REQ-UX-*` / schema is used, never redefined.
- [ ] Repository-ready hygiene in all output content: no host/system/taskflow detail, no agent/DAG/run
      ids, no workspace paths, no attribution trailers. (Internal workspace files — this hub, briefs,
      contracts — are taskflow-internal and are never posted to GitHub.)

---

## Constraints
- **Design, not code.** State what the product must look like and do; defer the build to code DAGs.
- **Compose against the parent contract.** `../contracts/id_and_traceability_schema.yaml` fixes the
  `REQ-<AREA>-NNN` format (3-digit, unique within area), the per-requirement fields
  (`id`, `statement`, `acceptance_criteria`, `release_gating`), and that `UX` is owned by this subtree.
  `../contracts/design_artifact_map.yaml` fixes the file's required sections. Children extend additively
  (sub-range the id space); they MUST NOT redefine the scheme or the section list.
- **Methodology posture.** Phase-B boot file is the `design` domain loader/index; each child's brief
  names the design bundle ID(s) its concern maps to (Experience Design primary; Product Strategy,
  Identity and Trust supporting), and the executing child loads bundle bodies on demand. NOTE: in the
  current reconstructed environment the methodology-loader syscall reports the agent domain unset; a
  child that meets the same condition designs from the named bundle intent and its own product-design
  competence, and records the limitation — it does not block.
- **Repository-ready output content.** Everything that lands in `experience-design.md` is written for
  the repository's readers; hygiene as in Success Criteria.

---

## Input Specifications

| Source | Identity | Role |
|--------|----------|------|
| Parent subtree hub | `../_GLOBAL.md` | Whole-design context, constraints, the board, hygiene rules. |
| Parent contract | `../contracts/` (read-only) | `REQ-UX-*` scheme; this file's required sections; identities. |
| Product requirements | `../SUBTASK_product_requirements/outputs/product-requirements.md` | Personas, journeys J1–J10, `REQ-PROD-001..042` — what the screens serve and trace to. |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | The current SPA (`crates/chirp-frontend`: timeline `/`, compose `/compose`, profile `/user/:id`, nav bar) as the starting point; clone into your own workspace if you need a working tree. |
| Live deployment | ArgoCD app `chirp` @ `c805525` (read-only) | Exercise the current screens to ground the "from" state (read-only; reached per the project environment facts, which never appear in output content). |

---

## Task Structure

### Overview

```
SUBTASK_experience_design/
├── _GLOBAL.md                         (this hub)
├── contracts/                         (READ-ONLY for descendants — the internal seam)
│   ├── _MANIFEST.yaml                 (section ownership, REQ-UX id ranges, identities)
│   └── ux_section_and_id_map.yaml     (section→owner map, id ranges, shared vocabularies, trace rule)
├── SUBTASK_ia_interaction/_BRIEF.md
├── SUBTASK_visual_system/_BRIEF.md
├── SUBTASK_screens_flows/_BRIEF.md
├── SUBTASK_responsive/_BRIEF.md
├── SUBTASK_accessibility/_BRIEF.md
├── SUBTASK_synthesis/_BRIEF.md
└── outputs/
    └── experience-design.md           (the deliverable — written by SUBTASK_synthesis)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_ia_interaction` | none | Design the information architecture & interaction model: the canonical screen/route inventory and screen archetypes, the signed-out vs signed-in navigation shells, global navigation and wayfinding, and the interaction conventions the whole product obeys. Publishes the **screen inventory** every sibling composes against. Bundles: Experience Design (primary); Product Strategy (support). Owns `REQ-UX-001..019`. | `outputs/ia-interaction.md` |
| `SUBTASK_visual_system` | `SUBTASK_ia_interaction` | Design the visual language & design system: typography, color (incl. theme), spacing/layout grid, iconography, tone, and the **component library** (naming and behavior of the reusable UI pieces — chirp card, compose box, buttons, fields, nav, dialogs, toasts, empty-state blocks, etc.). Publishes the **component vocabulary** screens/responsive/accessibility compose against. Bundle: Experience Design (primary). Owns `REQ-UX-020..039`. | `outputs/visual-system.md` |
| `SUBTASK_screens_flows` | `SUBTASK_ia_interaction`, `SUBTASK_visual_system` | Design the screens & flows for every journey (J1–J8 and the user-facing parts of J9), each **with its empty / error / loading states** — sign-up/in/recovery/sign-out, the posting/timeline/reply loops, profile & editing, follow/discovery, onboarding, settings, export, deletion, notifications, report/block. Composes against the screen inventory and component vocabulary. Bundles: Experience Design (primary); Product Strategy, Identity and Trust (support). Owns `REQ-UX-040..089`. | `outputs/screens-flows.md` |
| `SUBTASK_responsive` | `SUBTASK_ia_interaction`, `SUBTASK_visual_system` | Design responsive behavior across phone→larger viewports: breakpoints, how each screen archetype and nav shell adapt, touch targets and reachability, and what must hold on a phone. Bundle: Experience Design (primary). Owns `REQ-UX-090..099`. | `outputs/responsive.md` |
| `SUBTASK_accessibility` | `SUBTASK_ia_interaction`, `SUBTASK_visual_system` | Set the accessibility standard (a named WCAG level/version) and design to it: keyboard operability, accessible names/roles/states, focus management, contrast, reduced-motion, error/announcement patterns, applied across the screen archetypes and components. Bundle: Experience Design (primary). Owns `REQ-UX-100..119`. | `outputs/accessibility.md` |
| `SUBTASK_synthesis` | `SUBTASK_ia_interaction`, `SUBTASK_visual_system`, `SUBTASK_screens_flows`, `SUBTASK_responsive`, `SUBTASK_accessibility` | **Verification gate + fold.** Assemble the five outputs into `../outputs/experience-design.md` with every required section in order; consolidate the full `REQ-UX-*` register; assert the subtree identities with recorded evidence (section coverage & single owner, id uniqueness/range, every `REQ-UX-*` testable + release-gating + traces to `REQ-PROD-*`, parent contract composed-against, surface coverage, hygiene); remediate a fixable gap by decomposing a remediation subtree, never a silent plug; author `SYNTHESIS.md` and fold this node to COMPLETED. Bundle: Experience Design. | `../outputs/experience-design.md` + `SYNTHESIS.md` |

### Dependency Graph (human-readable; the table is authoritative)

```
ia_interaction ──> visual_system ──┬─> screens_flows ──┐
                                    ├─> responsive ─────┤
                                    └─> accessibility ──┴─> synthesis
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the contract in
`contracts/`. The children are parts of ONE experience design and share a real seam: one output document
with a fixed set of required sections, one `REQ-UX-*` id space that must stay collision-free and
`REQ-PROD`-traceable, and two shared vocabularies (the **screen inventory** and the **component
vocabulary**) that the later children compose against. That seam is frozen before any child runs.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (section-ownership map + REQ-UX id-range partition + identities), extending
the parent `../contracts/` additively — never overriding it.

### Structural Declarations
- `contracts/ux_section_and_id_map.yaml` — the one owning child per required section of
  `experience-design.md`; the `REQ-UX-NNN` sub-range assigned to each child; the two shared vocabularies
  (screen inventory, component vocabulary) with their producing child and required shape; and the
  per-`REQ-UX` trace rule (references ≥1 `REQ-PROD-*`; has a testable acceptance criterion and a
  `release_gating` flag).

### Ownership (one producer per artifact / id range)

| Artifact / id range | Owning child |
|---|---|
| `information_architecture_and_interaction` section + screen inventory + `REQ-UX-001..019` | `SUBTASK_ia_interaction` |
| `visual_language_and_design_system` section + component vocabulary + `REQ-UX-020..039` | `SUBTASK_visual_system` |
| `screens_and_flows` + `empty_error_loading_states` sections + `REQ-UX-040..089` | `SUBTASK_screens_flows` |
| `responsive_layout` section + `REQ-UX-090..099` | `SUBTASK_responsive` |
| `accessibility` section + `REQ-UX-100..119` | `SUBTASK_accessibility` |
| assembled `experience-design.md`, consolidated `requirements_and_acceptance_criteria` register, `SYNTHESIS.md` | `SUBTASK_synthesis` |

### Identities (asserted by `SUBTASK_synthesis` with recorded evidence; no silent plugs)
1. **SECTION_COVERAGE** — every required section of `experience-design.md` (per
   `../contracts/design_artifact_map.yaml`) is present, in order, and written by exactly one child.
2. **ID_UNIQUE_IN_RANGE** — every `REQ-UX-*` id is unique and falls within its owning child's assigned
   range; no collisions, no out-of-range ids.
3. **UX_TESTABLE_AND_GATED** — every `REQ-UX-*` has a `statement`, an `acceptance_criteria` a stranger
   could check against the live product, and a `release_gating` flag (`true`/`false`).
4. **UX_TRACES_TO_PROD** — every `REQ-UX-*` references ≥1 `REQ-PROD-*`; and every `REQ-PROD-*` with a UX
   surface (the experience-quality set 030–036, and the user-facing surface of 001–028, 032–034, 042) is
   covered by ≥1 `REQ-UX-*` or recorded as having no distinct UX requirement with a reason.
5. **COMPOSES_AGAINST_PARENT** — the parent `../contracts/` `REQ-UX` format, field set, and section list
   are used, not redefined; the internal contract only sub-ranges and maps.
6. **SURFACE_COVERAGE** — every account/operational surface with a user-facing UX (sign-up/in/recovery/
   sign-out, onboarding, settings, edit profile, data export, account deletion, notifications,
   report/block, and the user-visible help/support entry) is designed with its empty/error/loading
   states OR recorded out-of-scope with a reason.
7. **NOT_SKELETAL** — each designed screen specifies layout/content/primary action and its empty, error,
   and loading states — not a bare route name.
8. **HYGIENE** — nothing in `experience-design.md` carries host/system/taskflow detail, workspace paths,
   agent/DAG/run ids, or an attribution trailer.

### Shared vocabularies (the seam the dependency edges carry)
- **Screen inventory** — the canonical list of screens/routes and their archetypes, produced by
  `SUBTASK_ia_interaction` in `outputs/ia-interaction.md` under a clearly labelled "Screen inventory"
  heading. Every sibling refers to screens by these names.
- **Component vocabulary** — the canonical list of named reusable components and their behavior, produced
  by `SUBTASK_visual_system` in `outputs/visual-system.md` under a clearly labelled "Component library"
  heading. `screens_flows`, `responsive`, and `accessibility` compose against these names.

### Thin-Seam Note
The seam is not thin: a shared document with fixed sections, a partitioned id space, cross-artifact
traceability, and two shared vocabularies are a rich contract. Children MUST compose against `contracts/`
and MUST NOT redefine the `REQ-UX` scheme, the section list, or the id ranges.
