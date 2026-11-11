# Task: Assemble & verify the visual system (synthesis gate + fold)

## Task Specification
**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Assemble the two content children into the one deliverable `../outputs/visual-system.md`, verify the subtree's
identities with recorded evidence, and fold this subtree's root (`SUBTASK_visual_system`) to COMPLETED.

### Context
The verification gate and fold for the visual-system subtree (see `../_GLOBAL.md` and `../contracts/`). You read
the two children's outputs and assemble them; you do not re-design the visual system. You own the assembled
`visual-system.md`, the consolidated `REQ-UX-020..039` register, and `SYNTHESIS.md`. You mint no `REQ-UX` of
your own.

**Dependencies**: `SUBTASK_visual_language`, `SUBTASK_component_library`.
**Dependents**: folds `SUBTASK_visual_system` to COMPLETED, which the experience-design siblings
(`SUBTASK_screens_flows`, `SUBTASK_responsive`, `SUBTASK_accessibility`) and the parent synthesis depend on.

### Scope — what this gate must do
- **Assemble** `../outputs/visual-system.md` from the two child outputs, in the order
  `../contracts/visual_system_seam.yaml` fixes: the `visual_language_and_design_system` section body, then a
  clearly-headed **"Component library"** in the required shape, then the consolidated `REQ-UX-020..039` register.
- **Verify the identities** in `../contracts/_MANIFEST.yaml` with recorded evidence: SECTION_AND_HEADING_SHAPE,
  TOKENS_PUBLISHED_AND_COMPOSED (every component references published token names, no ad-hoc values),
  ARCHETYPE_AND_COMPONENT_COVERAGE (every IA archetype and required named component present, each with its
  states), ID_UNIQUE_IN_RANGE, UX_TESTABLE_AND_GATED, UX_TRACES_TO_PROD, COMPOSES_AGAINST_PARENT, HYGIENE.
- **Remediate, never plug.** A fixable gap (a missing archetype component, an off-range or off-contract id, a
  component with ad-hoc values, an untestable or untraced `REQ-UX`) is remediated by decomposing a remediation
  subtree, not by silently editing or inserting reconciling content.
- **Fold.** Author `SYNTHESIS.md` at the fold location and fold `SUBTASK_visual_system` to COMPLETED.

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, the identities, hygiene. |
| Internal contract | `../contracts/` (read-only) | Assembly order, ownership, `REQ-UX` sub-ranges, the identities to assert. |
| Visual language output | `../SUBTASK_visual_language/outputs/visual-language.md` | The section body, the token set, `REQ-UX-020..032`. |
| Component library output | `../SUBTASK_component_library/outputs/component-library.md` | The "Component library" content, `REQ-UX-033..039`. |
| Inherited contracts | `../../contracts/` and `../../../contracts/` (read-only) | The section list and `REQ-UX` scheme to check composition against. |
| Screen inventory | `../../SUBTASK_ia_interaction/outputs/ia-interaction.md` | The archetype/screen list to check component coverage against. |
| Product requirements | `../../../SUBTASK_product_requirements/outputs/product-requirements.md` | The `REQ-PROD-*` set to check traces against. |

### Methodology
Design-domain bundle: **Experience Design** (design-system review). Loader unavailable in the current
reconstructed environment; verify from the contract identities and your product-design competence, recording the
limitation.

### Output
- `../outputs/visual-system.md` — the assembled deliverable: the `visual_language_and_design_system` section, a
  clearly-headed "Component library" in the parent-contract shape, and the consolidated `REQ-UX-020..039`
  register. Repository-ready: no host/system/taskflow detail, no workspace paths, no attribution.
- `SYNTHESIS.md` — the fold record: per-identity pass/fail with the evidence consulted, section/heading
  coverage with single owner, and the fold outcome.

### Success criteria
- [ ] `../outputs/visual-system.md` exists with the section and the "Component library" heading in the required
      shape and order, plus the consolidated `REQ-UX-020..039`.
- [ ] Every identity in `../contracts/_MANIFEST.yaml` is asserted with recorded evidence; any failure is reported
      and remediated by decomposition, never silently plugged.
- [ ] `SYNTHESIS.md` authored at the fold location and `SUBTASK_visual_system` folded to COMPLETED.

### Constraints
- Assemble and verify only — do not re-author the visual system or mint `REQ-UX` ids. Repository-ready hygiene
  on all assembled content.
