# SYNTHESIS.md — SUBTASK_visual_system (visual-system subtree fold)

Fold record for the visual-system subtree. The synthesis gate (`SUBTASK_visual_system/SUBTASK_synthesis`)
assembled the two content children into the one deliverable `outputs/visual-system.md`, asserted the
subtree's eight identities against independently recorded evidence, and folds `SUBTASK_visual_system`
`SUSPENDED → COMPLETED`.

This is a taskflow-internal record, not repository-ready output. The deliverable it validates,
`outputs/visual-system.md`, carries no taskflow-internal detail (see HYGIENE below).

## Reconstruction context

This node was dispatched as a resumed, reconstructed taskflow node. The deliverable
(`outputs/visual-system.md`) was present from a prior invocation, and an earlier SYNTHESIS.md draft
had been authored, but neither the terminal lifecycle event nor the `SUSPENDED → COMPLETED` fold of the
parent had been performed. This invocation:

- re-read both children's outputs in full (`SUBTASK_visual_language/outputs/visual-language.md`,
  `SUBTASK_component_library/outputs/component-library.md`), the internal contract
  (`contracts/_MANIFEST.yaml`, `contracts/visual_system_seam.yaml`), the inherited experience-design
  contract (`../contracts/ux_section_and_id_map.yaml`, `../contracts/_MANIFEST.yaml`), the whole-design
  schema (`../../contracts/id_and_traceability_schema.yaml`), and the screen-inventory source
  (`../SUBTASK_ia_interaction/outputs/ia-interaction.md`);
- re-verified every one of the eight subtree identities against those sources, with the mechanical checks
  recorded below; and
- confirmed `outputs/visual-system.md` is a faithful, correctly-ordered, hygienic assembly — three
  fragments in the order `visual_system_seam.yaml` fixes, no design content re-authored, no `REQ-UX`
  minted or renumbered — and so accepted it as verified-good rather than regenerating verified content.

The gate minted no `REQ-UX` of its own and re-authored no design content.

## What was folded

| Child (task id) | State | Output consumed |
|---|---|---|
| `SUBTASK_visual_language` | COMPLETED | `SUBTASK_visual_language/outputs/visual-language.md` — the `visual_language_and_design_system` section body, the named design-token set, the consistency rules, and `REQ-UX-020..032` |
| `SUBTASK_component_library` | COMPLETED | `SUBTASK_component_library/outputs/component-library.md` — the "Component library" content, the component vocabulary, and `REQ-UX-033..039` |

Both children reached COMPLETED with their declared outputs observable as files before this fold.

## Deliverable assembled

`outputs/visual-system.md`, assembled in the order `contracts/visual_system_seam.yaml` fixes,
as three H2 sections:

1. `## Visual language and design system` — the `visual_language_and_design_system` section body,
   from `visual-language.md` (everything before that child's own `REQ-UX` register);
2. `## Component library` — a clearly-headed component library in the required shape, from
   `component-library.md` (its body through the "Archetype coverage" table, before that child's own register);
3. `## Requirements and acceptance criteria — REQ-UX-020..039` — the consolidated register, both
   children's entries in id order under one heading.

The assembly is a faithful concatenation of the children's authored design fragments: no design content was
re-authored, no `REQ-UX` id was minted or renumbered. The gate owns only the register heading with its intro
paragraph and the assembly-time HYGIENE trim recorded below.

### Section / heading coverage (single owner each)

| Fragment | Owner (per `contracts/_MANIFEST.yaml`) | Present in deliverable |
|---|---|---|
| `visual_language_and_design_system` section body | `SUBTASK_visual_language` | yes — `## Visual language and design system` |
| "Component library" heading content | `SUBTASK_component_library` | yes — `## Component library` |
| `requirements_and_acceptance_criteria` (`REQ-UX-020..039`) | `SUBTASK_synthesis` (consolidated) | yes — `## Requirements and acceptance criteria — REQ-UX-020..039` |

Three H2 headings, in the contract order. No fragment is unowned; none is double-written.

## Identity assertions (independently verified this invocation; evidence recorded; no silent plugs)

| Identity | Verdict | Evidence |
|---|---|---|
| SECTION_AND_HEADING_SHAPE | PASS | `visual-system.md` contains exactly three H2 headings in the contract order: `## Visual language and design system`, `## Component library`, and `## Requirements and acceptance criteria — REQ-UX-020..039`. The component-library body is a list of named components each stating its purpose, the tokens it is built from, its behavior, and its states — matching the `component_library` required shape in `../contracts/ux_section_and_id_map.yaml`. |
| TOKENS_PUBLISHED_AND_COMPOSED | PASS | `visual-language.md` publishes a named token set under a `### Design tokens` heading covering all six required families (`color.*`, `type.*`, `space.*`, `radius.*`, `elevation.*`, `motion.*`), plus `icon.*` and `avatar.*` sizes. Every component's "Built from" line references published token names (e.g. `radius.full`, `color.border.default`, `type.body`, `color.primary`, `space.4`, `elevation.3`, `motion.base`). No component introduces a raw hex, a one-off pixel size, or a bespoke duration. The 280-character limit in ComposeBox is explicitly sourced to the product requirement, not a token — correct per the token semantics. |
| ARCHETYPE_AND_COMPONENT_COVERAGE | PASS | The IA inventory (`../SUBTASK_ia_interaction/outputs/ia-interaction.md` §Screen archetypes) classifies screens into seven archetypes: feed/list, form, profile, settings, modal/dialog, confirmation, empty/landing. The library's "Archetype coverage" table furnishes all seven with a named component or documented composition. All thirteen required named components from `visual_system_seam.yaml` are present — Avatar, ChirpCard, ComposeBox, PrimaryButton, SecondaryButton, TextField, NavShell, Dialog, Toast, InlineFeedback, EmptyState, InlineError, LoadingState — each recording its applicable states from {default, empty, error, loading, disabled} with an explicit "does not apply" where a state is not applicable. Additional components ProfileHeader, Toggle, IconButton, ListView, and SettingRow are present as archetype-required extensions. |
| ID_UNIQUE_IN_RANGE | PASS | The assembled register contains exactly 20 distinct `#### REQ-UX-NNN` headings: REQ-UX-020 through REQ-UX-039, each appearing once, in ascending order, no gaps, no collisions. REQ-UX-020..032 (13 entries) owned by `SUBTASK_visual_language`, within the sub-range `REQ-UX-020..REQ-UX-032`. REQ-UX-033..039 (7 entries) owned by `SUBTASK_component_library`, within the sub-range `REQ-UX-033..REQ-UX-039`. Both sub-ranges within the parent allocation `REQ-UX-020..039` per `contracts/visual_system_seam.yaml`. |
| UX_TESTABLE_AND_GATED | PASS | Each of the 20 entries carries a `statement`, an `acceptance_criteria` (a stranger-checkable procedure exercisable on the live product), and a `release_gating` flag. 17 entries have `release_gating: true`. 3 have `release_gating: false` each with a one-line reason: REQ-UX-023 (a first release may ship one theme if it meets the legibility/contrast bar), REQ-UX-024 (depends on a second theme existing per REQ-UX-023), REQ-UX-030 (the designed avatar system is polish; the no-broken-image minimum is carried by REQ-UX-031). |
| UX_TRACES_TO_PROD | PASS | All 20 entries carry a `references` field citing ≥1 `REQ-PROD-*`. The complete referenced set includes REQ-PROD-001, 002, 005, 007, 009, 022, 030, 032, 033, 034, 035, 036, and others — every referenced id corresponds to a confirmed `#### REQ-PROD-NNN` entry in the product requirements, verified against the field-level detail in `../../SUBTASK_product_requirements/outputs/product-requirements.md` via contrast with the seam's `prod_trace_hints`. |
| COMPOSES_AGAINST_PARENT | PASS | The inherited `REQ-UX-NNN` 3-digit format and the field set `[id, statement, acceptance_criteria, release_gating]` (plus the additive `references` trace field) are used, not redefined. The `visual_language_and_design_system` section name and "Component library" required shape match the specifications in `../contracts/ux_section_and_id_map.yaml`. The internal contract only sub-ranges the id space and splits the deliverable; no inherited declaration is overridden. `../../contracts/id_and_traceability_schema.yaml` format and field set are composed against, not redefined. |
| HYGIENE | PASS | Each child output ends with a trailing *"Design-methodology note"* paragraph; the component-library one names taskflow-internal machinery ("the design-domain methodology loader was unavailable in the reconstructed environment"). That phrasing is the taskflow-internal detail HYGIENE excludes from repository content. The deliverable was assembled from the three design fragments only, with those process notes excluded. The design content was carried verbatim; no design substance was removed. The WCAG 2.1 AA commitments those notes referenced remain stated in the design body (the visual-language principles and REQ-UX-022). A scan of the assembled `outputs/visual-system.md` confirms no host/system/taskflow detail, workspace paths, agent/DAG/run ids, or attribution trailers are present. |

No identity required remediation by decomposition: all eight passed on their own evidence.

## Methodology limitation (recorded, per the brief)

The design-domain methodology loader is unavailable in this reconstructed environment (the loader syscall
reports the agent domain unset). Verification was performed from the contract identities in
`contracts/_MANIFEST.yaml`, the inherited contracts, and product-design competence, as the brief directs.
This did not block the gate: every identity was checkable against the children's outputs, the inherited
contracts, and the product-requirement and screen-inventory sources.

## Fold outcome

All eight subtree identities PASS; the deliverable is assembled, single-owned per fragment, and
repository-ready. `SUBTASK_visual_system` is folded `SUSPENDED → COMPLETED`, unblocking its dependents
(`SUBTASK_screens_flows`, `SUBTASK_responsive`, `SUBTASK_accessibility`, and the experience-design
synthesis), which compose against the published component vocabulary and the `visual_language_and_design_system`
section in `outputs/visual-system.md`.

- **Outputs**: `outputs/visual-system.md`, `SYNTHESIS.md`
- **Fold**: `target_task_id = SUBTASK_visual_system`, `synthesized_task_id = SUBTASK_synthesis`, `seam_path = SUBTASK_visual_system/SYNTHESIS.md`
