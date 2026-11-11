# _GLOBAL.md — SUBTASK_release_plan (release plan subtree hub)

## Project Context

**Status**: Active

### Objective

Produce `release-plan.md` — the epics and work-items under the Ferric epic (#1) in the
`Nousix-LLC/nswe-demo` board, with every work-item's acceptance criteria tracing to
`REQ-*`/`BAR-FERRIC-*`, an order that reaches a usable framework early and the full
1.0 bar after, and an explicit fold of board issues #5 and #6 into the router/HTTP
epic(s).

This is a three-child decomposition: define the epic landscape first, then populate
each epic with work-items, then synthesize into the final document.

### Inherited Context

This subtree is part of the Ferric 1.0 framework design. See `../_GLOBAL.md` for the
full project context, scope, constraints, and methodology. This hub carries only
the decomposition-specific context for the release-plan task.

### Scope

**In Scope:**
- The epic structure under #1: what each epic is, which design areas it covers, its
  stage (usable_early vs one_oh), dependencies on other epics, and the #5/#6 fold
- Work-items per epic: title, acceptance criteria citing REQ-*/BAR-*, depends_on
- Dependency order: the sequence that reaches a usable framework early, then 1.0
- The final `release-plan.md` artifact

**Out of Scope:**
- Redefining any REQ-*/BAR-* (those are owned by their respective spokes; read-only here)
- Filing or editing board issues (that is SUBTASK_file_backlog's job)
- Writing framework code

### Success Criteria

- [ ] Every epic sits under #1, maps to ≥1 design area, is a single coherent landable
      capability with dependencies stated (identity I6 + J1)
- [ ] Every `one_oh` BAR-FERRIC-* is covered by ≥1 work-item; every work-item cites
      the REQ-*/BAR-* and design section it traces to (I6 + J3)
- [ ] Order reaches a usable framework early; the SSR must-have epic is marked
- [ ] #5/#6 fold is explicit: which issue each router/HTTP epic extends/supersedes (I7 + J2)
- [ ] Tickets say what the framework needs and how it will be judged; not how to build it

---

## Contract

**REQUIRED and present.** See `contracts/_MANIFEST.yaml`. The children inherit the
parent's id_and_traceability_schema.yaml for the epic/work-item schemas and share
an intermediate seam at `epics-and-order.md` (SUBTASK_rplan_epics → others) and
`work-items.md` (SUBTASK_rplan_work_items → synthesis).

---

## Input Specifications

All predecessor outputs are in the parent workspace. Key inputs per child:

| Source | Location | Used by |
|--------|----------|---------|
| Release bar | `../SUBTASK_release_bar/release-bar.md` | epics, work_items, synthesis |
| Scope + requirements | `../SUBTASK_scope_and_requirements/scope-and-requirements.md` | epics, work_items |
| SSR/hydration | `../SUBTASK_ssr_hydration/ssr-hydration.md` | epics, work_items |
| Authoring model | `../SUBTASK_authoring_model/authoring-model.md` | epics, work_items |
| Async/forms/events | `../SUBTASK_async_forms_events/async-forms-events.md` | epics, work_items |
| Router + HTTP | `../SUBTASK_router_and_http/router-and-http.md` | epics, work_items |
| Docs + DX | `../SUBTASK_docs_and_dx/docs-and-dx.md` | epics, work_items |
| Release + distribution | `../SUBTASK_release_and_distribution/release-and-distribution.md` | epics, work_items |
| Performance + benchmark | `../SUBTASK_performance_and_benchmark/performance-and-benchmark.md` | epics, work_items |
| Board issue #1 | GitHub `Nousix-LLC/nswe-demo` issue #1 | epics (#5/#6 fold) |
| Board issue #5 | GitHub `Nousix-LLC/nswe-demo` issue #5 | epics (#5 fold) |
| Board issue #6 | GitHub `Nousix-LLC/nswe-demo` issue #6 | epics (#6 fold) |
| Parent contracts | `../contracts/` | all children |
| This hub's contracts | `contracts/` | all children |

---

## Task Structure

### Overview

```
_GLOBAL.md (this hub)
├── contracts/
│   └── _MANIFEST.yaml
├── SUBTASK_rplan_epics/
│   └── _BRIEF.md      → produces: epics-and-order.md
├── SUBTASK_rplan_work_items/
│   └── _BRIEF.md      → produces: work-items.md
└── SUBTASK_rplan_synthesis/
    └── _BRIEF.md      → produces: release-plan.md (the declared output)
```

### Task Summary

| Task id | Depends on | Description | Output |
|---------|------------|-------------|--------|
| `SUBTASK_rplan_epics` | none | Define the epic landscape: what each epic is, its design-doc area mappings, stage, dependencies on other epics, and the explicit #5/#6 fold. | `epics-and-order.md` |
| `SUBTASK_rplan_work_items` | `SUBTASK_rplan_epics` | For each epic in epics-and-order.md, write the work-items: title, epic, acceptance criteria tracing to REQ-*/BAR-*, depends_on. | `work-items.md` |
| `SUBTASK_rplan_synthesis` | `SUBTASK_rplan_epics`, `SUBTASK_rplan_work_items` | Assemble the final release-plan.md from epics-and-order.md + work-items.md; verify identities J1/J2/J3; produce the clean document. | `release-plan.md` |

### Dependency Graph

```
SUBTASK_rplan_epics ──► SUBTASK_rplan_work_items ──┐
                    └──────────────────────────────►│ SUBTASK_rplan_synthesis
                                                    │
                                                    ▼
                                               release-plan.md
```
