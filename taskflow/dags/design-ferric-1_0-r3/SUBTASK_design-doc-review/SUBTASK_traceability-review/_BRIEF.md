# _BRIEF.md — SUBTASK_traceability-review

## Task Specification

**Slug**: SUBTASK_traceability-review  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Read `scope-and-requirements.md`, `contracts/design_artifact_map.yaml`, `contracts/id_and_traceability_schema.yaml`, and issues #129–#164 (36 items). Determine whether the REQ-* IDs, the artifact map, and the issue register agree with each other. Record each disagreement, gap, or orphan as a finding.

Specifically, check:
- Does every REQ-* ID declared in scope-and-requirements.md appear in the artifact map?
- Does every REQ-* ID in the artifact map correspond to a declared requirement?
- Does every epic and feature issue (#129–#164) trace to at least one REQ-* ID?
- Are there requirements with no corresponding ticket in #129–#164?

### Context

This task is part of the design-doc-review subtree (see `_GLOBAL.md` in the parent workspace at `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/`).

This is review **concern 3**: internal coherence and traceability. The risk is that tickets may build something different from what the design specifies if IDs are missing, orphaned, or inconsistently mapped.

**Depends on**: none (runs in parallel with SUBTASK_completeness-review and SUBTASK_release-bar-quality)  
**Dependents**: SUBTASK_findings-synthesis depends on this task's output

---

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Parent hub (design-doc-review) | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/_GLOBAL.md` | Shared context |
| Subtree hub (ferric review) | `taskflow/dags/design-ferric-1_0-r3/_GLOBAL.md` | Project-level context |
| Findings schema | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/contracts/spoke_findings_schema.yaml` | Output format contract |
| scope-and-requirements.md | `git show origin/work/design-ferric-1_0:design/ferric/scope-and-requirements.md` from `taskflow/dags/ferric-foundation/checkout/` | Source of REQ-* ID declarations |
| design_artifact_map.yaml | `git show origin/work/design-ferric-1_0:design/ferric/contracts/design_artifact_map.yaml` from `taskflow/dags/ferric-foundation/checkout/` | Cross-reference map |
| id_and_traceability_schema.yaml | `git show origin/work/design-ferric-1_0:design/ferric/contracts/id_and_traceability_schema.yaml` from `taskflow/dags/ferric-foundation/checkout/` | ID format contract |
| Issues #129–#164 | `gh issue view <n>` (for each of the 36 issues) from `taskflow/dags/ferric-foundation/checkout/` | Issue register for traceability check |

### Methodology

Load and apply from `infrastructure/methodologies/design/`:

- `product-strategy/ProductStrategy_RequirementsAndAcceptanceCriteria_Methodology.md`

This methodology defines what complete traceability looks like, how to audit REQ-* ID coverage, and what constitutes a traceability break.

---

## Output

| Attribute | Value |
|---|---|
| Filename | `traceability-findings.yaml` |
| Format | YAML conforming to `contracts/spoke_findings_schema.yaml` |
| Location | this workspace (`SUBTASK_traceability-review/`) |

The output is a YAML file with:
- `spoke: design-doc-review`
- `concern_ids: [3]`
- `findings: [...]` — one entry per traceability gap or inconsistency, each with `id` (DDR-T-NNN), `severity`, `concern: 3`, `location`, `statement`, `recommendation`
- `summary: { blocking_count, non_blocking_count }`

A finding is BLOCKING if it is a traceability break that means tickets may implement something different from what the design specifies: a REQ-* ID with no artifact map entry, an artifact map entry referencing a non-existent REQ-*, or a requirement with no ticket.

---

## Success Criteria

- scope-and-requirements.md read and all REQ-* IDs extracted.
- design_artifact_map.yaml read and all REQ-* mappings extracted.
- id_and_traceability_schema.yaml read.
- All 36 issues (#129–#164) inspected for REQ-* traceability.
- Every traceability gap, orphan REQ-*, and unticketed requirement recorded as a finding.
- Output file `traceability-findings.yaml` written conforming to the spoke findings schema.
- No finding omits `severity`, `location`, `statement`, or `recommendation`.
