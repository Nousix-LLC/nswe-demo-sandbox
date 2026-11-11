# Task: Assemble & verify the account-lifecycle screens; fold the subtree

## Task Specification
**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Assemble the three account-lifecycle spoke outputs into the one `account_lifecycle` deliverable, verify
this subtree's identities with recorded evidence, and fold the account-lifecycle node to COMPLETED.

### Context
The verification gate and fold for the account-lifecycle subtree (see `../_GLOBAL.md`, `../contracts/`).
The three spokes each designed one surface cluster of the `account_lifecycle` part and minted a slice of
`REQ-UX-065..077`. This task composes them into one part, consolidates the register, asserts the
contract's identities, and resolves this node via the synthesis fold. A fixable gap is remediated by
decomposing a remediation subtree — never a silent plug.

**Dependencies**: `SUBTASK_onboarding_profile`, `SUBTASK_settings_management`, `SUBTASK_leaving`.
**Dependents**: this subtree's parent (`SUBTASK_account_lifecycle` folds to COMPLETED on this task's fold).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, assembled order, identities, hygiene. |
| Internal contract | `../contracts/` (read-only) | The surface→owner map, id sub-ranges, identities, trace rule to assert against. |
| Onboarding + profile screens | `../SUBTASK_onboarding_profile/outputs/screens-onboarding-profile.md` | The onboarding & edit-profile surfaces + `REQ-UX-065..068`. |
| Account-settings screens | `../SUBTASK_settings_management/outputs/screens-settings-management.md` | The settings hub & sub-sections + `REQ-UX-069..074`. |
| Leaving screens | `../SUBTASK_leaving/outputs/screens-leaving.md` | Export & deletion + `REQ-UX-075..077`. |
| Screen inventory & component library | `../../../SUBTASK_ia_interaction/outputs/ia-interaction.md`, `../../../SUBTASK_visual_system/outputs/visual-system.md` | To check COMPOSES_AGAINST_VOCAB and STATES_CONSISTENT against the frozen vocabularies. |
| Product requirements | `../../../../SUBTASK_product_requirements/outputs/product-requirements.md` | To check UX_TRACES_TO_PROD and release-gating staging. |

### Process (approach, not a runbook)
Assemble the `account_lifecycle` part from the three spoke outputs in the screen-inventory order recorded
in `../contracts/account_lifecycle_seam.yaml`; consolidate the `REQ-UX-065..077` register; then evaluate
each contract identity (SURFACE_COVERAGE, ID_UNIQUE_IN_RANGE, NOT_SKELETAL, UX_TESTABLE_AND_GATED,
UX_TRACES_TO_PROD, COMPOSES_AGAINST_VOCAB, STATES_CONSISTENT, HYGIENE) as an assertion with recorded
evidence. On a clean pass, author the deliverable and the fold record and resolve the fold. On a fixable
failure, decompose a remediation subtree rather than plugging the gap.

### Output
- `../outputs/screens-account-lifecycle.md` — the assembled `account_lifecycle` part (each surface
  designed with layout/content/primary action and empty/error/loading states, in inventory order) plus
  the consolidated `REQ-UX-065..077` register. Repository-ready; no host/system/taskflow detail, no
  workspace paths, no attribution.
- `../SYNTHESIS.md` — the fold record: per-identity evidence, surface/id coverage, and the fold of the
  account-lifecycle node. Authored at the fold location (the account-lifecycle node's own workspace), then
  used to resolve the fold so the node becomes COMPLETED.

### Success criteria
- [ ] `../outputs/screens-account-lifecycle.md` carries all eight surfaces, each by exactly one spoke, in
      inventory order, with the consolidated register.
- [ ] Every contract identity is asserted with recorded evidence; no identity silently plugged.
- [ ] `REQ-UX-065..077` is complete, unique, in-range, each testable + gated + traced.
- [ ] `../SYNTHESIS.md` authored and the fold resolved so the account-lifecycle node is COMPLETED.

### Constraints
- Design/verification only — no front-end code. Repository-ready hygiene on the deliverable.
- Methodology: Experience Design. If the `design` loader is unavailable, work from the bundle intent and
  competence and record the limitation (do not block).
- Write in a plain, checkable human voice; run the avoid-ai-writing checklist (or the P0/P1 catalog by
  hand when the skill is absent) over the narrative before finalizing, and record the limitation.
