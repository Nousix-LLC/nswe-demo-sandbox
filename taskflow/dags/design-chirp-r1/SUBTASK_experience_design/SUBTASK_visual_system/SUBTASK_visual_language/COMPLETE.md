# COMPLETE — SUBTASK_visual_language

**Task**: Design chirp's visual language and the named design-token set; write the
`visual_language_and_design_system` section body plus `REQ-UX-020..032`.

**Decompose evaluation**: Atomic. Applied the decomposition triggers to this brief fresh (not
leaning on the parent having already split off the component library): the token trigger clears
(inputs well under 50% of context); the Distinct-Concerns and Single-Responsibility tests both
pass because the sub-areas (typography, colour/theming, spacing, radii, elevation, iconography,
imagery, motion, tone) are mutually-constraining facets of one interlocking visual language, the
design tokens are the formalization of that same language, and `REQ-UX-020..032` are its testable
restatement — one responsibility, one kind of output; the output-size signal (one ~430-line
document) is the weakest trigger and does not override a cleared scope result. Executed to
completion.

## Output produced

- `outputs/visual-language.md` — the `visual_language_and_design_system` section body
  (typography; colour and light/dark theming; spacing and the layout grid; corner radii;
  elevation; iconography; imagery/avatars; motion; tone and voice), a clearly-headed **"Design
  tokens"** set covering all six required families (`color.*` with a light value, a dark value,
  and a contrast intent per role; `type.*`; `space.*`; `radius.*`; `elevation.*`; `motion.*`),
  the consistency rules, and the `REQ-UX-020..032` register fragment.

## How it composes with the parent

- Composes against `../contracts/visual_system_seam.yaml` and `../contracts/_MANIFEST.yaml`: uses
  only the `REQ-UX-020..032` sub-range, the inherited `REQ-UX` field set, and publishes the
  **design-token vocabulary** under the required "Design tokens" heading in the required shape —
  the seam `SUBTASK_component_library` composes against by token name, and that
  `SUBTASK_synthesis` assembles into `outputs/visual-system.md`.
- Supports the subtree identities: SECTION_AND_HEADING_SHAPE (the section body + a "Design tokens"
  heading), TOKENS_PUBLISHED_AND_COMPOSED (a named set, referenced by name, no ad-hoc values —
  enforced by consistency rule 1 and REQ-UX-020), ID_UNIQUE_IN_RANGE, UX_TESTABLE_AND_GATED,
  UX_TRACES_TO_PROD, COMPOSES_AGAINST_PARENT, and HYGIENE.

## Success-criteria self-check

- [x] Composes against `../contracts/`; `REQ-UX` scheme; `REQ-UX-020..032` range only (13 ids).
- [x] Typography, colour/theme (light + dark), spacing, radii, elevation, iconography,
      imagery/avatars, motion, and tone specified concretely enough to build and judge against.
- [x] Named token set under a "Design tokens" heading, required shape, every required family
      present; it is the vocabulary a component references by name.
- [x] Every `REQ-UX-020..032` is stranger-testable on the live product, `release_gating`-flagged
      (020,021,022,025,026,027,028,029,031,032 = true; 023,024,030 = false with a one-line reason),
      unique, in range, and traces to ≥1 `REQ-PROD-*`.
- [x] Repository-ready hygiene: markdown + tables only, no host/system/taskflow detail, no
      workspace paths, no ids, no attribution.

## Limitation recorded (taskflow-internal; deliberately kept out of the repository-ready output)

The design-domain methodology loader is unavailable in this reconstructed environment — the
methodology-glob syscall reports the agent domain unset (`agent_domain_unset`). As the hub and
brief direct, the visual language was designed from the **Experience Design** bundle intent
(visual design and design systems) and product-design competence; this did not block the work.
The deliverable's closing note states the design posture (designed to the Experience Design
intent, WCAG 2.1 AA named explicitly) without any taskflow/system detail, so the output stays
repository-ready while the limitation is recorded here.
