# _BRIEF.md — SUBTASK_completeness-review

## Task Specification

**Slug**: SUBTASK_completeness-review  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Read directive #114 and all 14 Ferric 1.0 design files. Determine whether the design covers every capability the directive calls for and every surface a 1.0 Rust/Wasm UI framework with SSR is expected to include. Record each gap as a finding.

### Context

This task is part of the design-doc-review subtree (see `_GLOBAL.md` in the parent workspace at `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/`).

This is review **concern 1**: completeness against the directive. The question is not whether the implementation exists — only whether the design covers the surface. A design gap is a gap: a required capability that the design documents do not address at all, or address only by silence.

**Depends on**: none (runs in parallel with SUBTASK_release-bar-quality and SUBTASK_traceability-review)  
**Dependents**: SUBTASK_findings-synthesis depends on this task's output

---

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Parent hub (design-doc-review) | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/_GLOBAL.md` | Shared context, design file inventory |
| Subtree hub (ferric review) | `taskflow/dags/design-ferric-1_0-r3/_GLOBAL.md` | Project-level context and verdict rules |
| Findings schema | `taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/contracts/spoke_findings_schema.yaml` | Output format contract |
| Directive | `gh issue view 114` (from checkout at `taskflow/dags/ferric-foundation/checkout/`) | Requirements the design must satisfy |
| All 14 design files | `git show origin/work/design-ferric-1_0:design/ferric/<file>` from `taskflow/dags/ferric-foundation/checkout/` | Primary review material |

Design files to read (all via `git show origin/work/design-ferric-1_0:design/ferric/<file>`):
- `README.md`, `scope-and-requirements.md`, `ssr-hydration.md`, `authoring-model.md`
- `async-forms-events.md`, `router-and-http.md`, `docs-and-dx.md`, `release-and-distribution.md`
- `performance-and-benchmark.md`, `release-bar.md`, `release-plan.md`
- `contracts/_MANIFEST.yaml`, `contracts/design_artifact_map.yaml`, `contracts/id_and_traceability_schema.yaml`

### Methodology

Load and apply from `infrastructure/methodologies/design/`:

- `release-definition/ReleaseDefinition_CompletenessAndGapReview_Methodology.md`

This methodology defines what a complete design for a 1.0 framework of this kind must include, how to read a directive's requirements, and how to audit for gaps.

---

## Output

| Attribute | Value |
|---|---|
| Filename | `completeness-findings.yaml` |
| Format | YAML conforming to `contracts/spoke_findings_schema.yaml` |
| Location | this workspace (`SUBTASK_completeness-review/`) |

The output is a YAML file with:
- `spoke: design-doc-review`
- `concern_ids: [1]`
- `findings: [...]` — one entry per gap found, each with `id` (DDR-C-NNN), `severity`, `concern: 1`, `location`, `statement`, `recommendation`
- `summary: { blocking_count, non_blocking_count }`

A finding is BLOCKING if it represents a capability the design entirely omits that a 1.0 release of this kind requires.

---

## Success Criteria

- Directive #114 read and its requirements list extracted.
- All 14 design files read.
- Every gap between #114's requirements and the design documented as a finding.
- Every finding states the specific document and section where the gap appears.
- Output file `completeness-findings.yaml` written conforming to the spoke findings schema.
- No finding omits `severity`, `location`, `statement`, or `recommendation`.
