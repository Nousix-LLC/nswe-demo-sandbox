# SUBTASK_rbar_synthesis — subtree hub

## Project Context

**Status**: Active

### Objective

Produce `release-bar.md` (the Ferric 1.0 release bar) and fold both SUBTASK_rbar_synthesis and SUBTASK_release_bar
to COMPLETED. The work splits into a serial pipeline: an independent gap sweep of all framework surfaces, a
BAR-FERRIC-* criteria pass for every covered surface, and a final assembly + identity verification pass that
writes the deliverables and executes both fold calls.

The sibling `SUBTASK_rbar_gap_review` completed its own gap-analysis.md before this subtree was materialized;
SUBTASK_rbar_gap should read it as a cross-check but produce its own independent assessment. SUBTASK_rbar_assembly
should also read the sibling's gap-analysis.md if readable, as a secondary cross-check during assembly.

### Scope

**In Scope:**
- Independent gap sweep of all 24 canonical surfaces from the parent brief plus any additional surfaces found
  in the spoke docs
- BAR-FERRIC-* criteria for every covered surface (not for out-of-1.0 surfaces, per identity IB/I5)
- Assembly of release-bar.md (five sections) and verification of identities IA, IB, I2, I3, I4, I5
- Writing SYNTHESIS.md at the SUBTASK_release_bar root and folding SUBTASK_release_bar
- Writing SYNTHESIS.md at this workspace root and folding SUBTASK_rbar_synthesis

**Out of Scope:**
- Authoring or modifying any REQ-* (those belong to the spoke owners)
- Implementation choices for how Ferric meets any criterion

### Success Criteria

- [ ] gap-analysis-internal.md covers all 24 canonical surfaces and any additional surfaces found in spoke docs
- [ ] bar-criteria-draft.md has a BAR-FERRIC-* criterion for every covered surface; every criterion references
      ≥1 real REQ-* id (identity I2)
- [ ] release-bar.md is assembled with all five sections, passes the avoid-ai-writing pass, and is written at
      `../release-bar.md` (SUBTASK_release_bar root)
- [ ] Identities IA, IB, I2, I3, I4, I5 are verified at assembly with results recorded in SYNTHESIS.md
- [ ] SYNTHESIS.md at `../SYNTHESIS.md` folds SUBTASK_release_bar; SYNTHESIS.md at `./SYNTHESIS.md` folds
      SUBTASK_rbar_synthesis

---

## Input Specifications

| Source | Location | Purpose |
|--------|----------|---------|
| Parent hub | `../_GLOBAL.md` | Shared context, identity table, output location |
| Parent contracts | `../../contracts/id_and_traceability_schema.yaml` | BAR-FERRIC-* schema, REQ-* namespaces |
| Subtree contract | `contracts/_MANIFEST.yaml` | Format schemas, ownership, identities |
| Parent manifest | `../../contracts/_MANIFEST.yaml` | gap_analysis_row and bar_criterion format contracts |
| Scope + requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | REQ-FW-* register |
| SSR/hydration design | `../../SUBTASK_ssr_hydration/ssr-hydration.md` | REQ-SSR-* register |
| Authoring model | `../../SUBTASK_authoring_model/authoring-model.md` | REQ-API-* register |
| Async/forms/events | `../../SUBTASK_async_forms_events/async-forms-events.md` | REQ-ASYNC-* register |
| Router + HTTP | `../../SUBTASK_router_and_http/router-and-http.md` | REQ-RT-*, REQ-HTTP-* registers |
| Docs + DX | `../../SUBTASK_docs_and_dx/docs-and-dx.md` | REQ-DX-* register |
| Release + distribution | `../../SUBTASK_release_and_distribution/release-and-distribution.md` | REQ-REL-* register |
| Performance + benchmark | `../../SUBTASK_performance_and_benchmark/performance-and-benchmark.md` | REQ-PERF-* register |
| Sibling gap analysis | `../../SUBTASK_rbar_gap_review/gap-analysis.md` (read-only cross-check) | Supplemental reference |

---

## Task Structure

```
_GLOBAL.md (this hub)
├── contracts/
│   └── _MANIFEST.yaml
├── SUBTASK_rbar_gap/
│   └── _BRIEF.md
├── SUBTASK_rbar_criteria/
│   └── _BRIEF.md  ← authored as design reference; NOT a DAG node (scheduling cycle)
└── SUBTASK_rbar_assembly/
    └── _BRIEF.md
```

### Task Summary

**Note on scheduling**: The original design was a sequential chain rbar_gap → rbar_criteria →
rbar_assembly. The engine rejected a dependency from rbar_criteria onto rbar_gap because adding a
second sequential tier under SUBTASK_rbar_synthesis (group 1 in the outer DAG) creates a cycle in
execution group recomputation — the same constraint the parent documented in `../_GLOBAL.md`. The
resolution mirrors the parent's resolution: rbar_gap and rbar_assembly run concurrently. rbar_criteria's
work (writing BAR-FERRIC-* criteria) is incorporated into rbar_assembly, which reads the already-complete
sibling's gap analysis as primary input.

`SUBTASK_rbar_criteria/_BRIEF.md` is retained on disk as a design artifact documenting the criteria
format and staging principle. It is NOT registered as a DAG task and will not execute.

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_rbar_gap` | none | Sweep all 24+ framework surfaces against the 8 spoke REQ-* registers; produce gap-analysis-internal.md | `gap-analysis-internal.md` |
| `SUBTASK_rbar_assembly` | none (concurrent with rbar_gap) | Read sibling's gap-analysis.md; write BAR-FERRIC-* criteria; assemble release-bar.md (five sections); verify identities; fold both parents | `../../release-bar.md`, `../../SYNTHESIS.md`, `../SYNTHESIS.md` |

### Dependency Graph

```
SUBTASK_rbar_gap ─┐
                  ├── (concurrent; rbar_assembly reads sibling gap analysis, not rbar_gap output)
SUBTASK_rbar_assembly ─┘
```

---

## Contract

**Contract location**: `contracts/` · **Contract kind**: `yaml_schema`

### Inherited Contracts

| Ancestor contract | Path | What it binds here |
|---|---|---|
| id_and_traceability_schema | `../../contracts/id_and_traceability_schema.yaml` | BAR-FERRIC-* pattern, field requirements, verification vocabulary, stage vocabulary |
| parent release_bar manifest | `../../contracts/_MANIFEST.yaml` | gap_analysis_row schema, bar_criterion schema, identities IA/IB/I2/I3/I4/I5 |

### Structural Declarations

| Artifact | Kind | Declares |
|---|---|---|
| `contracts/_MANIFEST.yaml` | yaml_schema | Format of gap-analysis-internal.md rows; format of bar-criteria-draft.md entries; ownership; inherited identities |

### Ownership

| Artifact | Owning subtask |
|---|---|
| `gap-analysis-internal.md` | `SUBTASK_rbar_gap` |
| `bar-criteria-draft.md` | `SUBTASK_rbar_criteria` |
| `../../release-bar.md` | `SUBTASK_rbar_assembly` |
| `../../SYNTHESIS.md` | `SUBTASK_rbar_assembly` |
| `./SYNTHESIS.md` | `SUBTASK_rbar_assembly` |

### Identities (rbar_assembly asserts; no silent plugs)

- [ ] **IA** — every covered surface in gap-analysis-internal.md has ≥1 BAR-FERRIC-* in bar-criteria-draft.md
- [ ] **IB** — every out-of-1.0 surface is enforced by no BAR-FERRIC-*
- [ ] **I2** — every BAR-FERRIC-* references ≥1 REQ-* id that exists in a spoke register
- [ ] **I3** — every one_oh / release_gating=true REQ-* is referenced by ≥1 BAR-FERRIC-*
- [ ] **I4** — ≥1 one_oh BAR-FERRIC-* marks SSR+hydration must_have: true
- [ ] **I5** — the four named out-of-1.0 items appear in gap-analysis-internal.md with status=out-of-1.0 and are enforced by no BAR-FERRIC-*

---

## Output Specifications

| Deliverable | Location | Description |
|-------------|----------|-------------|
| `gap-analysis-internal.md` | `SUBTASK_rbar_gap/` | Gap sweep table: 24+ surfaces with status/req_refs/notes |
| `bar-criteria-draft.md` | `SUBTASK_rbar_criteria/` | Complete BAR-FERRIC-* register with all fields |
| `release-bar.md` | `../release-bar.md` (SUBTASK_release_bar root) | Final five-section release bar document |
| `SYNTHESIS.md` (release_bar fold) | `../SYNTHESIS.md` (SUBTASK_release_bar root) | Fold record for SUBTASK_release_bar |
| `SYNTHESIS.md` (rbar_synthesis fold) | `./SYNTHESIS.md` (this workspace) | Fold record for SUBTASK_rbar_synthesis |
