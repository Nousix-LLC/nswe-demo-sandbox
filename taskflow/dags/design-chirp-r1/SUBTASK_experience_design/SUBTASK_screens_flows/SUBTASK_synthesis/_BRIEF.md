# Task: Assemble, verify, and fold the screens-&-flows subtree

## Task Specification
**Slug**: SUBTASK_synthesis
**Task Kind**: synthesis
**Status**: Pending

### Objective
Assemble the five spoke outputs into the single deliverable `../outputs/screens-flows.md`, consolidate
the `REQ-UX-040..089` register, verify this subtree's identities with recorded evidence, and **fold this
subtree's root (`SUBTASK_screens_flows`) to COMPLETED** — so the parent experience-design subtree can
consume `screens-flows.md` as the `screens_and_flows` + `empty_error_loading_states` sections.

### Context
This is the verification gate and fold for the screens-&-flows subtree (see `../_GLOBAL.md`,
`../contracts/`). You read the five spoke outputs and this subtree's contract; you do not re-design any
screen. You are the only child that writes the assembled deliverable and the fold record, and you
assemble in the order the contract fixes: `screens_and_flows` (its four parts — get_in, core_loop,
account_lifecycle, safety_notifications, in that order) then `empty_error_loading_states`.

**Dependencies**: `SUBTASK_get_in`, `SUBTASK_core_loop`, `SUBTASK_account_lifecycle`,
`SUBTASK_safety_notifications`, `SUBTASK_considered_states`. **Dependents**: none (folds the subtree root).

### Inputs
| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | The task tree, the contract pointer, success criteria, hygiene. |
| Internal contract | `../contracts/` (read-only) | The section/surface ownership map, id sub-ranges, the identities to assert, the shared-vocab and states-consistency rules. |
| get_in output | `../SUBTASK_get_in/outputs/screens-get-in.md` | The entry/auth screens-part + `REQ-UX-040..050`. |
| core_loop output | `../SUBTASK_core_loop/outputs/screens-core-loop.md` | The core-loop screens-part + `REQ-UX-051..064`. |
| account_lifecycle output | `../SUBTASK_account_lifecycle/outputs/screens-account-lifecycle.md` | The account-lifecycle screens-part + `REQ-UX-065..077`. |
| safety_notifications output | `../SUBTASK_safety_notifications/outputs/screens-safety-notifications.md` | The safety/notifications screens-part + `REQ-UX-078..085`. |
| considered_states output | `../SUBTASK_considered_states/outputs/empty-error-loading-states.md` | The `empty_error_loading_states` section + `REQ-UX-086..089`. |
| Required-surface checklist | `../../contracts/ux_section_and_id_map.yaml` | The `required_surfaces` SURFACE_COVERAGE is checked against. |

### Approach
Assemble the deliverable, consolidate the register, and run the contract's identities as checks against
the assembled whole. Verify, with recorded evidence rather than assertion:
- **SECTION_PART_COVERAGE** — both sections present, assembled in order; every section-part from exactly
  one spoke; no hole, no double-write.
- **ID_UNIQUE_IN_RANGE** — every `REQ-UX-040..089` unique and within its owning spoke's sub-range.
- **SURFACE_COVERAGE** — every `required_surfaces` surface (and every screen-inventory screen) designed
  with its empty/error/loading states, or recorded out-of-scope with a reason.
- **NOT_SKELETAL** — each screen has layout, content, a primary action, and its three states.
- **UX_TESTABLE_AND_GATED** / **UX_TRACES_TO_PROD** — each `REQ-UX` testable, gated, ≥1 `REQ-PROD` trace.
- **COMPOSES_AGAINST_VOCAB** — every screen refers to inventory screens and library components by name;
  no redefinition; no new screen/component without an additive amendment.
- **STATES_CONSISTENT** — each per-screen empty/error/loading state is consistent with the global
  patterns and the components' own named states.
- **HYGIENE** — no host/system/taskflow detail, workspace paths, agent/DAG/run ids, or attribution.

If an identity fails and the gap is fixable, remediate by **decomposing a remediation subtree** (amend
the plan with a fix task), never by silently plugging the hole; record the failure and the remediation.

### Output
- `../outputs/screens-flows.md` — the assembled deliverable: `screens_and_flows` (four parts in order)
  then `empty_error_loading_states`, plus the consolidated `REQ-UX-040..089` register. Repository-ready;
  no host/system/taskflow detail, no workspace paths, no attribution trailers.
- `../SYNTHESIS.md` — the fold record at this subtree's root (the fold location): the identity evidence,
  any remediation, and the fold of `SUBTASK_screens_flows` to COMPLETED.

### Success criteria
- [ ] `../outputs/screens-flows.md` carries both sections in order and the full `REQ-UX-040..089` register.
- [ ] Every identity in `../contracts/_MANIFEST.yaml` is asserted with recorded evidence; no silent plugs.
- [ ] A failing identity is remediated by an amendment, not a hand-edit, with the remediation recorded.
- [ ] `../SYNTHESIS.md` authored at the subtree root and the node folded to COMPLETED.

### Constraints
- Verify and assemble only — do not re-design screens or mint new `REQ-UX` ids (beyond what a recorded
  remediation subtree produces). Repository-ready hygiene on all output content.
- Methodology: Experience Design. Load bundle bodies on demand; if the `design` loader is unavailable,
  verify from the contract and competence and record the limitation (do not block).
- Run the avoid-ai-writing checklist over the assembled narrative before finalizing.
