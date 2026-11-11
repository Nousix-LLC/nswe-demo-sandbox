# _GLOBAL.md — SUBTASK_visual_system (visual-system subtree hub)

## Project Context

**Status**: Active

### Objective

Design chirp's **visual language and design system** and publish the canonical **component library**
(component vocabulary) that the screens, responsive, and accessibility siblings compose against. This
subtree produces the one deliverable `outputs/visual-system.md` — the `visual_language_and_design_system`
section plus a clearly-headed **"Component library"** in the shape the parent contract requires, and the
`REQ-UX-020..039` entries — assembled by `SUBTASK_synthesis` and folded to COMPLETED.

This node (`SUBTASK_visual_system`) evaluated its brief against the decomposition triggers. The Output-Size
trigger fired (a full visual language across seven sub-areas + a design-token set + a ~14-component library
each with its states + up to twenty testable `REQ-UX` entries is a ~600-line deliverable, over the 400-line
MUST-decompose line), and the brief enumerates distinct concerns (visual language; component library; design
tokens/consistency rules) whose component-library half composes against the visual-language half across a real
token seam. It therefore decomposes into two content children plus a synthesis gate. **This hub is this
decomposing node's own `_GLOBAL.md`; the experience-design subtree hub is `../_GLOBAL.md` and the whole-design
hub is `../../_GLOBAL.md`.**

### What this subtree designs (grounding)

chirp is a hosted, public, account-based consumer web application — a Twitter-style microblog (post ≤280-char
chirps, read a paginated home timeline, reply, like, follow, view profiles), today a WebAssembly single-page
app presenting three screens above a persistent nav bar. The experience design takes it from that skeleton to
a designed, releasable product. The visual system is why its many screens read as **one product** and why a
stranger trusts it in the first minute: a coherent type/color/spacing/motion language, a named token set that
keeps every screen consistent, and a reusable component vocabulary that furnishes every screen archetype in the
IA inventory with its default/empty/error/loading/disabled states.

### Scope

**In scope (this subtree):**
- The **visual language** — typography scale, color palette and semantic roles with light/dark theming,
  spacing and layout grid, radii and elevation, iconography, imagery/avatars, motion, and the product's
  tone/voice in UI copy.
- The **design tokens** — a named token set (color roles, type scale, spacing scale, radii, elevation, motion
  durations/easings) stated as design intent, and the consistency rules that keep screens coherent.
- The **component library** — the named, reusable UI components and their behavior and states (at least the
  chirp card, compose box, primary/secondary buttons, text field with validation, navigation shell,
  dialog/confirmation, toast/inline feedback, empty-state block, inline error, loading/skeleton — extended as
  the IA archetypes require), composing against the published tokens and the screen inventory.
- The `REQ-UX-020..039` register entries (statement, testable acceptance criteria, `release_gating`, ≥1
  `REQ-PROD-*` trace), sub-ranged across the two content children.

**Out of scope (this subtree):**
- Front-end code or any implementation "how" — design only.
- The screens & flows, responsive layout, and accessibility work owned by sibling subtrees; the IA/screen
  inventory owned by `SUBTASK_ia_interaction`. Where this subtree depends on those, it composes against the
  published screen inventory and names the owning area; it does not mint their ids.
- The `requirements_and_acceptance_criteria` cross-child register consolidation for the whole experience design
  (the parent `../SUBTASK_synthesis`); this subtree's synthesis consolidates only its own `REQ-UX-020..039`.

### Success Criteria (this subtree)
- [ ] `outputs/visual-system.md` carries the `visual_language_and_design_system` section AND a clearly-headed
      **"Component library"** in the shape `../contracts/ux_section_and_id_map.yaml` requires.
- [ ] A complete, named component library covering every screen archetype in the IA inventory and every
      required named component, each with its states (default/empty/error/loading/disabled as applicable).
- [ ] Typography, color/theme, spacing, iconography, motion, and tone are specified concretely enough to build
      and judge against, through a named token set components reference by name (no ad-hoc values).
- [ ] Every `REQ-UX-020..039` is testable by a stranger on the live product, carries a `release_gating` flag,
      references ≥1 `REQ-PROD-*`, and is unique and within its owning child's sub-range.
- [ ] Composes against `../contracts/` and the published screen inventory; the parent `REQ-UX` scheme, field
      set, and section list are used, never redefined.
- [ ] Repository-ready hygiene in all output content: no host/system/taskflow detail, no agent/DAG/run ids, no
      workspace paths, no attribution trailers. (Internal workspace files — this hub, briefs, contracts — are
      taskflow-internal and are never posted to GitHub.)

---

## Constraints
- **Design, not code.** State what the product must look like and do; defer the build to code DAGs.
- **Compose against the inherited contracts.** `../../contracts/id_and_traceability_schema.yaml` fixes the
  `REQ-<AREA>-NNN` format and the per-requirement field set; `../contracts/ux_section_and_id_map.yaml` fixes
  the section list, the `REQ-UX-020..039` range, the "Component library" required shape, and the trace rule.
  `contracts/` here sub-ranges the id space between the two content children and declares the token seam;
  children extend additively and MUST NOT redefine any inherited declaration.
- **Methodology posture.** The design-domain methodology loader is unavailable in the current reconstructed
  environment (the loader syscall reports the agent domain unset). Each child designs from the **Experience
  Design** bundle intent (visual design & design systems) and its own product-design competence, and records
  the limitation in its output — it does not block.
- **Repository-ready output content.** Everything that lands in `visual-system.md` is written for the
  repository's readers; hygiene as in Success Criteria.

---

## Input Specifications

| Source | Identity | Role |
|--------|----------|------|
| Experience-design subtree hub | `../_GLOBAL.md` | The experience-design context, constraints, hygiene. |
| Whole-design hub | `../../_GLOBAL.md` | Whole-design context (read as needed). |
| Inherited parent contract | `../contracts/` (read-only) | Section list, `REQ-UX-020..039` range, "Component library" required shape, trace rule, identities. |
| Inherited grandparent contract | `../../contracts/` (read-only) | `REQ-<AREA>-NNN` format + per-requirement field set; `experience-design.md` section list. |
| Internal contract | `contracts/` (read-only for children) | Section split, `REQ-UX` sub-ranges, the token seam, identities. |
| Screen inventory & archetypes | `../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The screens/archetypes the component library must furnish; refer to screens by these names. |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | Personas, journeys, `REQ-PROD-*` — what the visual system serves and traces to. |
| Repository | `Nousix-LLC/nswe-demo` @ `c805525` | The current SPA look as the "from" state; clone into a child's own workspace if a working tree is wanted. |

---

## Task Structure

### Overview

```
SUBTASK_visual_system/
├── _GLOBAL.md                          (this hub)
├── contracts/                          (READ-ONLY for descendants — the internal seam)
│   ├── _MANIFEST.yaml                  (section split, REQ-UX sub-ranges, token seam, identities)
│   └── visual_system_seam.yaml         (what each child owns; the token vocabulary; the component coverage rule)
├── SUBTASK_visual_language/_BRIEF.md
├── SUBTASK_component_library/_BRIEF.md
├── SUBTASK_synthesis/_BRIEF.md
└── outputs/
    └── visual-system.md                (the deliverable — written by SUBTASK_synthesis)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_visual_language` | none | Design the visual language and the named design-token set: typography scale, color palette + semantic roles + light/dark theming, spacing/layout grid, radii, elevation, iconography, imagery/avatars, motion, and tone/voice; derive the token set and the consistency rules that keep screens coherent. Publishes the **token vocabulary** the component library composes against. Bundle: Experience Design. Owns the `visual_language_and_design_system` section body and `REQ-UX-020..032`. | `outputs/visual-language.md` |
| `SUBTASK_component_library` | `SUBTASK_visual_language` | Design the **component library**: the named, reusable UI components (chirp card, compose box, primary/secondary buttons, text field with validation, navigation shell, dialog/confirmation, toast/inline feedback, empty-state block, inline error, loading/skeleton, and the rest the IA archetypes require), each with its behavior and its default/empty/error/loading/disabled states, composing against the published token vocabulary and the screen inventory. Publishes the **component vocabulary** screens/responsive/accessibility refer to by name. Bundle: Experience Design. Owns the "Component library" heading content and `REQ-UX-033..039`. | `outputs/component-library.md` |
| `SUBTASK_synthesis` | `SUBTASK_visual_language`, `SUBTASK_component_library` | **Verification gate + fold.** Assemble the two child outputs into `../outputs/visual-system.md` — the `visual_language_and_design_system` section, then a clearly-headed "Component library" in the parent-contract shape, then the consolidated `REQ-UX-020..039` register. Assert the subtree identities with recorded evidence (section/heading present in required shape; tokens published and composed-against; archetype & required-component coverage with states; id uniqueness/range; every `REQ-UX` testable + release-gating + traces to `REQ-PROD-*`; composes-against-parent; hygiene); remediate a fixable gap by decomposing a remediation subtree, never a silent plug; author `SYNTHESIS.md` and fold this node to COMPLETED. Bundle: Experience Design. | `../outputs/visual-system.md` + `SYNTHESIS.md` |

### Dependency Graph (human-readable; the table is authoritative)

```
visual_language ──> component_library ──┐
                 └──────────────────────┴──> synthesis
```

---

## Contract

The two co-designed outputs of this decomposition are the task tree above and the contract in `contracts/`.
The children are parts of ONE visual system and share a real seam: one output document whose
`visual_language_and_design_system` section and "Component library" heading must assemble in the parent-contract
shape; one `REQ-UX-020..039` id space that must stay collision-free and `REQ-PROD`-traceable; and a named
**design-token vocabulary** the component library composes against by name. That seam is frozen before any
child runs.

**Contract location**: `contracts/` (read-only for every descendant)
**Contract kind**: `yaml_schema` (section split + `REQ-UX` sub-range partition + token seam + identities),
extending `../contracts/` and `../../contracts/` additively — never overriding them.

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Experience-design seam | `../contracts/ux_section_and_id_map.yaml`, `../contracts/_MANIFEST.yaml` | The `visual_language_and_design_system` section and the `component_library` "Component library" heading are this node's to produce; `REQ-UX-020..039`; the `req_ux_fields` field set; the trace rule; the component-library required shape. |
| Whole-design schema | `../../contracts/id_and_traceability_schema.yaml`, `../../contracts/design_artifact_map.yaml` | `REQ-<AREA>-NNN` format (3-digit, unique within area); per-requirement fields; `experience-design.md`'s section list. |

### Structural Declarations
- `contracts/visual_system_seam.yaml` — the one owning child per output fragment (the section body; the
  "Component library" heading); the `REQ-UX` sub-range assigned to each content child; the named token
  vocabulary (`color.*`, `type.*`, `space.*`, `radius.*`, `elevation.*`, `motion.*`) `SUBTASK_visual_language`
  publishes and `SUBTASK_component_library` composes against; and the archetype/required-component coverage rule.

### Ownership (one producer per artifact / id range)

| Artifact / id range | Owning child |
|---|---|
| `visual_language_and_design_system` section body + token vocabulary + consistency rules + `REQ-UX-020..032` | `SUBTASK_visual_language` |
| "Component library" heading content + component vocabulary + `REQ-UX-033..039` | `SUBTASK_component_library` |
| assembled `outputs/visual-system.md`, consolidated `REQ-UX-020..039` register, `SYNTHESIS.md` | `SUBTASK_synthesis` |

### Identities (asserted by `SUBTASK_synthesis` with recorded evidence; no silent plugs)
1. **SECTION_AND_HEADING_SHAPE** — `visual-system.md` contains the `visual_language_and_design_system` section
   and a clearly-headed "Component library" in the shape `../contracts/ux_section_and_id_map.yaml` requires.
2. **TOKENS_PUBLISHED_AND_COMPOSED** — `SUBTASK_visual_language` publishes a named token set; every component in
   the component library references token names from that set, not ad-hoc values.
3. **ARCHETYPE_AND_COMPONENT_COVERAGE** — the component library furnishes every screen archetype in the IA
   inventory (feed/list, form, profile, settings, modal/dialog, confirmation, empty/landing) and every required
   named component, each with its applicable states (default/empty/error/loading/disabled).
4. **ID_UNIQUE_IN_RANGE** — every `REQ-UX-*` id is unique, within its owning child's sub-range, and within
   `REQ-UX-020..039`; no collisions, no out-of-range ids.
5. **UX_TESTABLE_AND_GATED** — every `REQ-UX-*` has a `statement`, an `acceptance_criteria` a stranger could
   check on the live product, and a `release_gating` flag (a `false` carries a one-line reason).
6. **UX_TRACES_TO_PROD** — every `REQ-UX-*` references ≥1 `REQ-PROD-*`.
7. **COMPOSES_AGAINST_PARENT** — the inherited `REQ-UX` format, field set, section list, and "Component library"
   required shape are used, not redefined; this contract only sub-ranges ids and splits the section.
8. **HYGIENE** — nothing in `visual-system.md` carries host/system/taskflow detail, workspace paths,
   agent/DAG/run ids, or an attribution trailer.

### Shared vocabulary (the seam the dependency edge carries)
- **Design-token vocabulary** — the named token set (color roles, type scale, spacing scale, radii, elevation,
  motion), produced by `SUBTASK_visual_language` in `outputs/visual-language.md` under a clearly-labelled
  "Design tokens" heading. `SUBTASK_component_library` refers to tokens by these names.

### Thin-Seam Note
The seam is not thin: a shared document in a fixed shape, a partitioned id space with cross-artifact
traceability, and a named token vocabulary the component library composes against are a rich contract. Children
MUST compose against `contracts/` and MUST NOT redefine the `REQ-UX` scheme, the section list, the id ranges, or
the token vocabulary.
