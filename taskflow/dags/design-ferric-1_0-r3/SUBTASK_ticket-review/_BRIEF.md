# _BRIEF.md — SUBTASK_ticket-review

## Task Specification

**Slug**: SUBTASK_ticket-review  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Evaluate concern 5: **Ticket quality and wave plan**.

Read all 36 issues (#129–#164: 8 epics + 28 feature issues) and the `release-plan.md` design document. Evaluate:

- **Ticket completeness**: Does each epic accurately capture its design area's scope? Does each feature issue accurately represent a buildable unit of work?
- **Acceptance criteria quality**: Does each feature issue carry acceptance criteria that a reviewer can check against the implementation? Are the criteria specific enough to be testable (not "component model works" but "a component accepts required and optional props and the example compiles")?
- **Traceability**: Does each issue trace to one or more `REQ-*` or `BAR-FERRIC-*` IDs? Are those IDs actually from the design documents (not invented)?
- **Wave plan coherence**: Does `release-plan.md` give a valid dependency ordering? Is it true that the `usable_early` epics (#129–#132) are independent of SSR (#133)? Are any declared cross-dependencies contradicted by the design?
- **Epic–feature alignment**: Does each feature issue appear under the right epic? Are there feature issues that belong to a different epic, or design areas with no corresponding feature issues?
- **Coverage**: Are there capabilities described in the design documents that have no corresponding feature issue? Are there feature issues that describe capabilities not in the design?

### Context

This task is part of the Ferric 1.0 design gap review (see `_GLOBAL.md` in the parent workspace at `taskflow/dags/design-ferric-1_0-r3/`).

**Depends on**: none (runs in parallel with design-doc-review and foundation-buildability)  
**Dependents**: SUBTASK_synthesis depends on this task's output

### Inputs

| Input | Source | Purpose |
|---|---|---|
| Parent hub | `taskflow/dags/design-ferric-1_0-r3/_GLOBAL.md` | Shared context |
| Findings schema | `taskflow/dags/design-ferric-1_0-r3/contracts/findings_schema.yaml` | Output format contract |
| All 36 issues | `gh issue view <n>` for #129–#164 from `taskflow/dags/ferric-foundation/checkout/` | Issues to review |
| `release-plan.md` | `git show origin/work/design-ferric-1_0:design/ferric/release-plan.md` | Wave plan and work items |
| `release-bar.md` | `git show origin/work/design-ferric-1_0:design/ferric/release-bar.md` | Release criteria each feature should trace to |
| `scope-and-requirements.md` | `git show origin/work/design-ferric-1_0:design/ferric/scope-and-requirements.md` | REQ-FW-* IDs to match against tickets |
| Artifact map | `git show origin/work/design-ferric-1_0:design/ferric/contracts/design_artifact_map.yaml` | Cross-check of design area → issue mapping |

Issues to read: `gh issue view` for each of #129, #130, #131, #132, #133, #134, #135, #136 (epics) and #137–#164 (feature issues), run from `taskflow/dags/ferric-foundation/checkout/`.

### Methodology

Apply `delivery/Delivery_DesignToBacklogPlanning_Methodology.md` for evaluating whether the backlog accurately represents the design and whether the wave ordering is buildable.

### Output

| Attribute | Value |
|---|---|
| Filename | `ticket-findings.md` |
| Format | YAML conforming to `contracts/findings_schema.yaml` |
| Location | `SUBTASK_ticket-review/` (this workspace) |

The output is a YAML file with:
- `spoke: ticket-review`
- `concern_ids: [5]`
- `findings: [...]` — one entry per finding
- `summary: { blocking_count, non_blocking_count }`

A finding is BLOCKING if it means a ticket, as written, cannot be built correctly (missing acceptance criteria, wrong scope, wrong dependency, tracing to a nonexistent REQ-* ID). A finding is non-blocking if it is a quality improvement (clearer acceptance criteria, better epic scoping, a missing but implied trace ID).

### Success Criteria

- All 36 issues read.
- `release-plan.md` and `release-bar.md` read.
- Each epic (#129–#136) evaluated for scope accuracy and completeness.
- Each feature issue (#137–#164) evaluated for acceptance criteria quality and traceability.
- Wave ordering in `release-plan.md` checked against declared design dependencies.
- Output file `ticket-findings.md` written at this workspace, conforming to the findings schema.
- A BLOCKING finding about a ticket names the specific issue number and the specific criterion it fails.
