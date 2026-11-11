# Task: Ferric 1.0 release plan — work-items with traced acceptance criteria

## Task Specification

**Slug**: SUBTASK_rplan_work_items
**Task Kind**: standard
**Depends on**: SUBTASK_rplan_epics
**Status**: Pending
**Assigned To**: swe-designer

### Objective

For each epic defined in `epics-and-order.md`, write the work-items that make the epic
buildable and verifiable: a title stating what the framework needs (not how to build it),
acceptance criteria that cite the specific `REQ-*` and `BAR-FERRIC-*` ids the item
satisfies plus the design-doc section it traces to, and `depends_on` edges within and
across epics. Produce `work-items.md`.

### Context

Part of the SUBTASK_release_plan subtree (see `../_GLOBAL.md`). This task reads the
epic landscape from SUBTASK_rplan_epics and populates it. The output is the second
input to SUBTASK_rplan_synthesis, which assembles the final `release-plan.md`.

**Work-items say what and how to judge; code DAGs handle how to build.** An acceptance
criterion reads: "A test of X passes" or "A reviewer can confirm Y from the docs" — not
"implement class Z using pattern W."

**Do not redefine any REQ-* or BAR-FERRIC-* ids.** Those are read from the inputs.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Shared context + constraints. |
| Grand subtree hub | `../../_GLOBAL.md` | Project-level constraints. |
| Contracts (parent) | `../../contracts/id_and_traceability_schema.yaml` | Work-item schema (fields, acceptance-criterion format, verification_method vocab). |
| Contracts (this level) | `../contracts/_MANIFEST.yaml` | Intermediate seam + inherited refs. |
| Epic landscape | `../SUBTASK_rplan_epics/epics-and-order.md` | The epics to populate — authoritative source of epic ids/titles and stages. |
| Release bar | `../../SUBTASK_release_bar/release-bar.md` | The BAR-FERRIC-* list; every one_oh BAR must be covered by ≥1 work-item. |
| Scope + requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | REQ-FW-*; framework-level requirements. |
| SSR/hydration | `../../SUBTASK_ssr_hydration/ssr-hydration.md` | REQ-SSR-*; the must-have. |
| Authoring model | `../../SUBTASK_authoring_model/authoring-model.md` | REQ-API-*. |
| Async/forms/events | `../../SUBTASK_async_forms_events/async-forms-events.md` | REQ-ASYNC-*. |
| Router + HTTP | `../../SUBTASK_router_and_http/router-and-http.md` | REQ-RT-*, REQ-HTTP-*. |
| Docs + DX | `../../SUBTASK_docs_and_dx/docs-and-dx.md` | REQ-DX-*. |
| Release + distribution | `../../SUBTASK_release_and_distribution/release-and-distribution.md` | REQ-REL-*. |
| Performance + benchmark | `../../SUBTASK_performance_and_benchmark/performance-and-benchmark.md` | REQ-PERF-*. |

---

## Distinct concerns to cover

- **Work-item population per epic**: for each epic in epics-and-order.md, produce the
  work-items that make it buildable. Each work-item is the smallest unit of work that
  can be assigned, built, reviewed, and merged independently.
- **Acceptance-criteria tracing**: each work-item's acceptance criteria must cite the
  specific REQ-*/BAR-FERRIC-* ids it satisfies and the design-doc section
  (e.g. "SSR/hydration design §3.2") it traces to. A work-item with no REQ/BAR
  citation is incomplete.
- **Coverage verification**: before finalizing, confirm that every `one_oh`
  BAR-FERRIC-* from the release bar appears in at least one work-item's acceptance
  criteria. Record any gap explicitly.
- **depends_on edges**: note work-item dependencies (within an epic or across epics)
  where one item must land before another can start or be verified.

---

## Declared output

- `work-items.md` — in this task's workspace (`SUBTASK_rplan_work_items/`)

The output must be structured as a list of work-items grouped by epic. For each
work-item:
```
### [Epic title] — [work-item title]
- **Acceptance criteria**: [checkable condition(s) citing REQ-*/BAR-* and design section]
- **Depends on**: [other work-item or epic, or "none"]
- **Verification**: [one value from the verification_method vocabulary]
```

The verification_method vocabulary (from id_and_traceability_schema.yaml):
- `automated_test` — a Rust test passes
- `example_build` — an example or starter scaffolds and runs
- `doc_inspection` — a reviewer confirms the doc/policy exists and is accurate
- `benchmark_run` — the benchmark entry runs and produces the stated numbers
- `publishability` — cargo publish dry-run succeeds

---

## Success criteria

- [ ] Every epic in epics-and-order.md has ≥1 work-item.
- [ ] Every work-item title states what the framework needs, not how to build it.
- [ ] Every work-item's acceptance criteria cite ≥1 REQ-* or BAR-FERRIC-* id.
- [ ] Every `one_oh` BAR-FERRIC-* from release-bar.md is covered by ≥1 work-item
      acceptance criterion (identity I6/J3).
- [ ] Every work-item uses one of the five verification_method values.
- [ ] No REQ-*/BAR-FERRIC-* is redefined; all ids used come from the input files.

## Constraints

- Write work-items, not epics. The epic structure comes from epics-and-order.md and
  must be taken as authoritative.
- Honor the writing-voice rules.
- The work-item schema in `../../contracts/id_and_traceability_schema.yaml` is
  authoritative. Conform to it; do not redefine it.
