# _BRIEF.md — SUBTASK_design-doc-review

## Task Specification

**Slug**: SUBTASK_design-doc-review  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Read all 14 Ferric 1.0 design files (from PR#128, branch `work/design-ferric-1_0`) and the directive issue #114. Evaluate three concerns:

1. **Completeness against the directive** — Does the design cover everything #114 calls for, and everything a 1.0 Rust/Wasm UI framework with SSR must include to be a product someone can build with? Are there capabilities the bar would require that the design documents do not address?

2. **Release bar quality** — Is `release-bar.md` a concrete, testable checklist (each `BAR-FERRIC-*` item verifiable by someone who was not in the room) or does it contain aspirational, non-checkable language? Is every dimension of the release bar adjudicated (reactive core, SSR, authoring model, async, routing, HTTP, docs, performance, distribution)?

3. **Internal coherence and traceability** — Do the requirements (`scope-and-requirements.md`, `REQ-*` IDs), the design artifact map (`contracts/design_artifact_map.yaml`), and the issue register (#129–#164) agree? Does every `REQ-*` ID in scope-and-requirements.md appear in the artifact map? Does every epic and feature issue trace to at least one `REQ-*` ID? Are there requirements with no corresponding ticket?

### Context

This task is part of the Ferric 1.0 design gap review (see `_GLOBAL.md` in the parent workspace at `taskflow/dags/design-ferric-1_0-r3/`).

**Depends on**: none (runs in parallel with foundation-buildability and ticket-review)  
**Dependents**: SUBTASK_synthesis depends on this task's output

### Inputs

| Input | Source | Purpose |
|---|---|---|
| Parent hub | `taskflow/dags/design-ferric-1_0-r3/_GLOBAL.md` | Shared context and methodology guidance |
| Findings schema | `taskflow/dags/design-ferric-1_0-r3/contracts/findings_schema.yaml` | Output format contract |
| All 14 design files | `git show origin/work/design-ferric-1_0:design/ferric/<file>` from `taskflow/dags/ferric-foundation/checkout/` | Primary review material |
| Directive | `gh issue view 114` from the checkout repo | What the design must satisfy |
| Artifact map | `design/ferric/contracts/design_artifact_map.yaml` on the PR branch | Traceability cross-check |
| ID schema | `design/ferric/contracts/id_and_traceability_schema.yaml` on the PR branch | ID format contract |

Design files to read (all via `git show origin/work/design-ferric-1_0:design/ferric/<file>`):
- `README.md`
- `scope-and-requirements.md`
- `ssr-hydration.md`
- `authoring-model.md`
- `async-forms-events.md`
- `router-and-http.md`
- `docs-and-dx.md`
- `release-and-distribution.md`
- `performance-and-benchmark.md`
- `release-bar.md`
- `release-plan.md`
- `contracts/_MANIFEST.yaml`
- `contracts/design_artifact_map.yaml`
- `contracts/id_and_traceability_schema.yaml`

### Methodology

Apply the following methodology bundles from `infrastructure/methodologies/design/`:

- `release-definition/ReleaseDefinition_CompletenessAndGapReview_Methodology.md` — for concerns 1 and 3 (what a complete design for this framework kind must include; how to audit for gaps)
- `release-definition/ReleaseDefinition_ReleaseBar_Methodology.md` — for concern 2 (what makes a release bar concrete and testable vs. aspirational)
- `product-strategy/ProductStrategy_RequirementsAndAcceptanceCriteria_Methodology.md` — for concern 3 (traceability; what testable acceptance criteria look like)

### Output

| Attribute | Value |
|---|---|
| Filename | `design-doc-findings.md` |
| Format | YAML conforming to `contracts/findings_schema.yaml` |
| Location | `SUBTASK_design-doc-review/` (this workspace) |

The output is a YAML file (also readable as text) with:
- `spoke: design-doc-review`
- `concern_ids: [1, 2, 3]`
- `findings: [...]` — one entry per finding, each with `id`, `severity`, `concern`, `location`, `statement`, `recommendation`
- `summary: { blocking_count, non_blocking_count }`

A finding is BLOCKING if it represents a gap that would require a REQUEST-CHANGES verdict: a missing required surface in the design, a bar item that cannot be verified by an outside reviewer, or a traceability break that means tickets may not implement what the design specifies.

### Success Criteria

- All 14 design files read.
- Directive #114 read and its requirements list extracted.
- Every concern (1, 2, 3) evaluated with findings recorded.
- Output file `design-doc-findings.md` written at this workspace, conforming to the findings schema.
- No finding omits `severity`, `location`, `statement`, or `recommendation`.
- A finding about a gap in the design names the specific document and section where the gap appears, not just "the design".
