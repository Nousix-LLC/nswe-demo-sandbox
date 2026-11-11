# Task: Synthesis & verification gate for the chirp experience design

## Task Specification
**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Assemble the five sibling outputs into the single deliverable `../outputs/experience-design.md`,
consolidate the full `REQ-UX-*` register, **verify the subtree's contract identities with recorded
evidence**, and fold `SUBTASK_experience_design` to COMPLETED. This is a verification gate, not a prose
summary.

### Context
The integration child of the experience-design subtree (see `../_GLOBAL.md`, `../contracts/`). You own
the assembled `outputs/experience-design.md` (this subtree's declared deliverable), its consolidated
`requirements_and_acceptance_criteria` register, and `SYNTHESIS.md` (the fold record at this subtree
root). You mint no new `REQ-UX-*` of your own except where remediation requires it.

**Dependencies**: `SUBTASK_ia_interaction`, `SUBTASK_visual_system`, `SUBTASK_screens_flows`,
`SUBTASK_responsive`, `SUBTASK_accessibility`.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Context, identities, success criteria |
| Internal contract | `../contracts/` (read-only) | Section map, id ranges, identities, required surfaces, trace rule |
| Parent contract | `../../contracts/` (read-only) | The `REQ-UX` scheme and `experience-design.md` required-section list to compose against |
| IA output | `../SUBTASK_ia_interaction/outputs/ia-interaction.md` | IA section + screen inventory + REQ-UX-001..019 |
| Visual output | `../SUBTASK_visual_system/outputs/visual-system.md` | Visual section + component library + REQ-UX-020..039 |
| Screens output | `../SUBTASK_screens_flows/outputs/screens-flows.md` | Screens/states sections + REQ-UX-040..089 |
| Responsive output | `../SUBTASK_responsive/outputs/responsive.md` | Responsive section + REQ-UX-090..099 |
| Accessibility output | `../SUBTASK_accessibility/outputs/accessibility.md` | Accessibility section + REQ-UX-100..119 |
| Product requirements | `../../SUBTASK_product_requirements/outputs/product-requirements.md` | `REQ-PROD-*` the trace checks resolve against |

### Approach
Assemble the required sections in the order fixed by `../contracts/ux_section_and_id_map.yaml`, carry each
child's `REQ-UX-*` into one consolidated register, and check each contract identity (SECTION_COVERAGE,
ID_UNIQUE_IN_RANGE, UX_TESTABLE_AND_GATED, UX_TRACES_TO_PROD, COMPOSES_AGAINST_PARENT, SURFACE_COVERAGE,
NOT_SKELETAL, HYGIENE) with recorded evidence in `SYNTHESIS.md`. The method for *how* to run a synthesis
gate is engineering practice (the `software` domain's `synthesis` bundle, reached by prose); do not
duplicate it here. On a **fixable** gap (a missing surface, an untestable or untraced `REQ-UX-*`, a
collision, a hygiene breach), remediate by **decomposing a remediation subtree** — never a silent plug or
a quiet pass.

### Output
- `../outputs/experience-design.md` — the assembled deliverable: every required section in order, the
  consolidated `REQ-UX-*` register, repository-ready and hygienic.
- `SYNTHESIS.md` (at this subtree root, the fold location) — the verification record: each identity with
  its evidence (pass/fail), the surface-coverage checklist, the `REQ-UX ↔ REQ-PROD` trace table, and any
  remediation taken.

### Success criteria
- [ ] `experience-design.md` carries all required sections (per `../../contracts/design_artifact_map.yaml`),
      in order, each from exactly one child.
- [ ] The consolidated `REQ-UX-*` register is collision-free, in-range, each entry testable +
      release-gating-flagged + tracing to ≥1 `REQ-PROD-*`.
- [ ] Every required user-facing surface is designed-with-states or recorded out-of-scope with a reason.
- [ ] All eight identities asserted with recorded evidence; any gap remediated by decomposition, not plug.
- [ ] Deliverable is repository-ready: no host/system/taskflow detail, workspace paths, ids, or attribution.

### Constraints
- Design only — no front-end code. Verify; do not rewrite a sibling's owned content beyond assembly and
  reconciliation. Repository-ready hygiene on the deliverable.
