# Task: Synthesis & verification — consolidate the domain & application design, fold the node

## Task Specification
**Slug**: SUBTASK_dad_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Assemble the three parts (domain model, persistence & state, module & interface structure) into the one
consolidated `design/domain-application-design.md`, verify this subtree's contract identities with recorded
evidence, and fold the `SUBTASK_domain_app_design` node. This is the subtree's verification gate, not a prose
summary.

### Context
Part of `SUBTASK_domain_app_design` (see `../_GLOBAL.md`, `../contracts/`). You own the consolidated file
`../outputs/domain-application-design.md`, the consolidated `requirements_and_acceptance_criteria` section (the
union of all `REQ-DOM-*`, carried verbatim from the three parts — you mint no new `REQ-DOM-*`), and the fold
record `../SYNTHESIS.md` at the node's directory (the fold location).
**Dependencies**: `SUBTASK_domain_model`, `SUBTASK_persistence_state`, `SUBTASK_module_structure`.
**Dependents**: folds the parent `SUBTASK_domain_app_design` node to COMPLETED, unblocking its dependents
(`SUBTASK_operational_readiness`, `SUBTASK_release_bar`).

### What to verify (assert with recorded evidence; no silent plugs)
Assemble the consolidated file so it carries every required section in `../../contracts/design_artifact_map.yaml`
for `domain-application-design.md`, then assert each identity in `../contracts/_MANIFEST.yaml`:
all required sections present; every `REQ-DOM-*` well-formed (id, statement, testable acceptance_criteria,
`release_gating`); `REQ-DOM-*` ids unique with no cross-part collision (ranges `001..049` / `100..149` /
`200..249`); one entity vocabulary throughout (persistence and module-structure reference only entities the model
names); the durable-persistence requirement names a concrete, operationally-checkable set of what survives a
restart; `REQ-PROD-*` traces present where a `REQ-DOM-*` refines a product requirement; repo hygiene clean. Record
the evidence for each in `SYNTHESIS.md`. Where a fixable design or coverage gap is found, remediate by decomposing
a remediation subtree — never by a silent plug or a quiet pass. The method for running a synthesis gate is
engineering practice in the `software` domain's `synthesis` bundle, reached by prose.

### Fold
Author `../SYNTHESIS.md` (the fold record at the parent node's directory), then fold the parent node
(`engine_resume_suspended` with the parent `SUBTASK_domain_app_design` as target, this task as the synthesized
task, and `../SYNTHESIS.md` as the seam). The consolidated file becomes the parent node's declared output.

## Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context, task tree, identities to assert |
| Subtree contract | `../contracts/` (read-only) | Identities, section ownership, `REQ-DOM-*` partition |
| Inherited contract | `../../contracts/` (read-only) | Required sections of the file; `REQ`/trace schema |
| Domain model part | `../SUBTASK_domain_model/outputs/domain-model.md` | `domain_model` section + entity vocabulary + `REQ-DOM-001..049` |
| Persistence part | `../SUBTASK_persistence_state/outputs/persistence-state.md` | `persistence_requirement` section + `REQ-DOM-100..149` |
| Module/interface part | `../SUBTASK_module_structure/outputs/module-structure.md` | `modules_and_responsibilities` + `interfaces_and_entry_points` + `REQ-DOM-200..249` |

## Output
- `../outputs/domain-application-design.md`: the consolidated, repository-ready design file with every required
  section and the union of all `REQ-DOM-*`.
- `../SYNTHESIS.md`: the fold record — recorded evidence for each contract identity, the ownership/coverage map,
  any remediation decomposed, and the fold.

## Success criteria
- [ ] Consolidated file carries every required section and the full `REQ-DOM-*` set, repository-ready.
- [ ] Every contract identity in `../contracts/_MANIFEST.yaml` asserted with recorded evidence; any failure
      remediated by a decomposed subtree, not plugged.
- [ ] `../SYNTHESIS.md` authored at the fold location and the parent node folded.

## Constraints
- Consolidate the parts; do not re-author their requirements or mint new `REQ-DOM-*`.
- Repository-ready hygiene on the consolidated file: no host/system/taskflow detail, no attribution trailers.
