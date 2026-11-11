# Design Doc Review — Decomposition Hub

## Context

This is the subtree hub for the `SUBTASK_design-doc-review` node of the Ferric 1.0 design gap review. The parent hub is at `taskflow/dags/design-ferric-1_0-r3/_GLOBAL.md`.

The review mandate covers three concerns against the 14 Ferric 1.0 design files in PR#128 (branch `work/design-ferric-1_0`):

1. **Completeness against directive #114** — Does the design address every capability the directive calls for, and every surface a 1.0 Rust/Wasm UI framework with SSR must include to be buildable?
2. **Release bar quality** — Are the BAR-FERRIC-* items in `release-bar.md` concrete and testable by an outside reviewer, or aspirational?
3. **Internal coherence and traceability** — Do the REQ-* IDs in `scope-and-requirements.md`, the `design_artifact_map.yaml`, and the filed issues #129–#164 agree?

These concerns require different analytical lenses and different primary sources; they decompose into three parallel spokes with a synthesis gate.

---

## Scope

**In Scope:**
- Reading and evaluating all 14 design files from branch `work/design-ferric-1_0`
- Reading directive #114 and extracting its requirements list
- Evaluating concern 1: coverage gap between #114's requirements and the design
- Evaluating concern 2: testability of each BAR-FERRIC-* item in `release-bar.md`
- Evaluating concern 3: consistency between REQ-* IDs, the artifact map, and the issue register
- Producing `../design-doc-findings.md` conforming to the parent hub's `contracts/findings_schema.yaml`

**Out of Scope:**
- Buildability on the existing codebase (SUBTASK_foundation-buildability)
- Ticket quality and wave ordering (SUBTASK_ticket-review)

---

## Shared Inputs

All spokes access the PR branch via:

```
git show origin/work/design-ferric-1_0:design/ferric/<file>
```

from the checkout at `taskflow/dags/ferric-foundation/checkout/`.

Issues are accessible via `gh issue view <n>` from that checkout directory.

**Design document inventory** (all via `git show origin/work/design-ferric-1_0:design/ferric/<file>`):

| File | REQ ID register | Notes |
|---|---|---|
| `README.md` | — | Navigation index |
| `scope-and-requirements.md` | REQ-FW-* | Framework definition, users, requirements, MVP/1.0 line |
| `ssr-hydration.md` | REQ-SSR-* | SSR + hydration architecture |
| `authoring-model.md` | REQ-API-* | view! macro, props, children, slots, context |
| `async-forms-events.md` | REQ-ASYNC-* | Async resources, suspense, forms, events |
| `router-and-http.md` | REQ-RT-*, REQ-HTTP-* | Router + HTTP/JSON client |
| `docs-and-dx.md` | REQ-DX-* | Guide, tutorial, API docs, examples, starter template |
| `release-and-distribution.md` | REQ-REL-* | crates.io, semver, changelog, versioning |
| `performance-and-benchmark.md` | REQ-PERF-* | js-framework-benchmark, peer comparison |
| `release-bar.md` | BAR-FERRIC-* | Consolidated 1.0 release bar, checkable criteria |
| `release-plan.md` | — | 8 epics, ordering, work items, wave plan |
| `contracts/_MANIFEST.yaml` | — | Contract manifest |
| `contracts/design_artifact_map.yaml` | — | Maps REQ-* to design artifacts and issues |
| `contracts/id_and_traceability_schema.yaml` | — | ID and traceability schema |

**Methodology bundles** (from `infrastructure/methodologies/design/`):

| Bundle file | Concern |
|---|---|
| `release-definition/ReleaseDefinition_CompletenessAndGapReview_Methodology.md` | Concern 1 |
| `release-definition/ReleaseDefinition_ReleaseBar_Methodology.md` | Concern 2 |
| `product-strategy/ProductStrategy_RequirementsAndAcceptanceCriteria_Methodology.md` | Concern 3 |

---

## Subtree Methodology Posture

Each spoke loads its corresponding methodology bundle and applies it to its concern. The synthesis gate (SUBTASK_findings-synthesis) does not require methodology loading; it reads and merges structured YAML.

The synthesis gate asserts the following identities with recorded evidence before writing the final output:
- Every finding from every spoke is present in the merged output
- All `concern_ids` [1, 2, 3] are covered
- `summary.blocking_count` matches the count of findings where `severity == BLOCKING`
- No finding is silently dropped or severity-adjusted without a recorded rationale

---

## Task Structure

| Task id | Task Kind | Depends on | Description | Output |
|---|---|---|---|---|
| `SUBTASK_completeness-review` | standard | none | Concern 1: completeness of design against directive #114 | `completeness-findings.yaml` |
| `SUBTASK_release-bar-quality` | standard | none | Concern 2: testability of BAR-FERRIC-* items in release-bar.md | `release-bar-findings.yaml` |
| `SUBTASK_traceability-review` | standard | none | Concern 3: coherence between REQ-* IDs, artifact map, and issue register | `traceability-findings.yaml` |
| `SUBTASK_findings-synthesis` | synthesis | `SUBTASK_completeness-review`, `SUBTASK_release-bar-quality`, `SUBTASK_traceability-review` | Merge spoke findings into design-doc-findings.md | `../design-doc-findings.md` |

### Dependency Graph

```
SUBTASK_completeness-review  ──┐
                               │
SUBTASK_release-bar-quality  ──┼── SUBTASK_findings-synthesis ──→ ../design-doc-findings.md
                               │
SUBTASK_traceability-review  ──┘
```

---

## Contract

Contract location: `contracts/` (read-only for all descendants).  
Contract kind: `yaml_schema`

Each spoke produces an intermediate YAML findings file conforming to `contracts/spoke_findings_schema.yaml`. The synthesis task reads all three and produces the final `../design-doc-findings.md` conforming to the ancestor hub's `contracts/findings_schema.yaml` (at `taskflow/dags/design-ferric-1_0-r3/contracts/findings_schema.yaml`).

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| Parent findings schema | `taskflow/dags/design-ferric-1_0-r3/contracts/findings_schema.yaml` | Final output structure for `../design-doc-findings.md` |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/spoke_findings_schema.yaml` | yaml_schema | Structure every spoke's intermediate findings file must follow |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `SUBTASK_completeness-review/completeness-findings.yaml` | SUBTASK_completeness-review |
| `SUBTASK_release-bar-quality/release-bar-findings.yaml` | SUBTASK_release-bar-quality |
| `SUBTASK_traceability-review/traceability-findings.yaml` | SUBTASK_traceability-review |
| `../design-doc-findings.md` | SUBTASK_findings-synthesis |

### Identities

- [ ] Each spoke's `concern_ids` field names exactly the concern number(s) that spoke addresses (1, 2, or 3)
- [ ] Every finding in every spoke output has `severity`, `concern`, `location`, `statement`, `recommendation`
- [ ] Merged output in `../design-doc-findings.md` covers all concern_ids [1, 2, 3]
- [ ] `summary.blocking_count` in the merged output equals the count of findings with `severity: BLOCKING`

---

## Output Specifications

| Deliverable | Format | Location | Description |
|---|---|---|---|
| Final merged findings | YAML (design-doc-findings.md) | `../design-doc-findings.md` | All findings from concerns 1, 2, 3 merged and conforming to parent findings_schema.yaml |
