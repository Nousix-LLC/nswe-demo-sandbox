# Task: Ferric 1.0 release plan — epic landscape and order

## Task Specification

**Slug**: SUBTASK_rplan_epics
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read the completed Ferric 1.0 design outputs and the existing GitHub board, then define
the epic landscape: what coherent, landable capabilities sit under epic #1, which design
areas each one covers, how they stage (usable_early vs one_oh), how they depend on each
other, which epic is the SSR must-have, and how board issues #5 and #6 are
superseded/extended by the router/HTTP epic(s). Produce `epics-and-order.md`.

### Context

Part of the SUBTASK_release_plan subtree (see `../_GLOBAL.md`). This is the precursor
task: SUBTASK_rplan_work_items reads this output to know which epics to populate.

**The epics are the unit of delivery.** Each epic is a coherent capability a single code
DAG can build, review, and land as one change. An epic maps to one or more design areas;
it does not mix concerns. The dependency order (which epics must land before which) is
what determines how fast a framework user can start building real applications.

**Do not redefine any REQ-* or BAR-FERRIC-* ids.** Those are read-only inputs.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub (this task's) | `../_GLOBAL.md` | Shared context + constraints. |
| Grand subtree hub | `../../_GLOBAL.md` | Project-level context and out-of-scope list. |
| Contracts (parent) | `../../contracts/id_and_traceability_schema.yaml` | Epic schema: fields, stage vocab, trace rules. |
| Contracts (this level) | `../contracts/_MANIFEST.yaml` | Intermediate artifact ownership + inherited contract refs. |
| Release bar | `../../SUBTASK_release_bar/release-bar.md` | The BAR-FERRIC-* list that the epic ordering must cover. |
| Scope + requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | REQ-FW-*; the MVP-vs-1.0 line; the out-of-1.0 list. |
| SSR/hydration | `../../SUBTASK_ssr_hydration/ssr-hydration.md` | REQ-SSR-*; the must-have capability. |
| Authoring model | `../../SUBTASK_authoring_model/authoring-model.md` | REQ-API-*. |
| Async/forms/events | `../../SUBTASK_async_forms_events/async-forms-events.md` | REQ-ASYNC-*. |
| Router + HTTP | `../../SUBTASK_router_and_http/router-and-http.md` | REQ-RT-*, REQ-HTTP-*. Feeds the #5/#6 fold. |
| Docs + DX | `../../SUBTASK_docs_and_dx/docs-and-dx.md` | REQ-DX-*. |
| Release + distribution | `../../SUBTASK_release_and_distribution/release-and-distribution.md` | REQ-REL-*. |
| Performance + benchmark | `../../SUBTASK_performance_and_benchmark/performance-and-benchmark.md` | REQ-PERF-*. |
| Board issue #1 | `gh issue view 1 --repo Nousix-LLC/nswe-demo` | The parent Ferric epic; all epics sit under it. |
| Board issue #5 | `gh issue view 5 --repo Nousix-LLC/nswe-demo` | Existing router scaffold; to be folded into the router epic. |
| Board issue #6 | `gh issue view 6 --repo Nousix-LLC/nswe-demo` | Existing HTTP scaffold; to be folded into the HTTP epic. |

---

## Distinct concerns to cover

- **What epics exist**: one epic per coherent landable capability; each maps to the
  design area(s) it realizes. Do not conflate unrelated design concerns in one epic.
  Expected shape: roughly one epic per design area (SSR+hydration, authoring model,
  async/forms/events, router, HTTP client, docs/DX, release/distribution,
  performance/benchmark) — but the exact split is yours to determine from the design.
- **Stage and order**: which epics are usable_early (needed to build real apps before 1.0)
  vs one_oh (needed for the full release bar); the dependency edges between epics; the
  rationale that SSR+hydration is the one_oh must-have.
- **The #5/#6 fold**: for issue #5 (router) and #6 (HTTP), state precisely whether each
  is superseded (the epic replaces the issue entirely) or extended (the epic extends the
  existing issue scope). Name the issue numbers and the action. This is identity I7 from
  the parent contract.

---

## Declared output

- `epics-and-order.md` — in this task's workspace (`SUBTASK_rplan_epics/`)

The output must include:
1. A table or structured list of all epics under #1: id/title, design-doc area(s),
   stage (usable_early | one_oh), depends_on (other epic titles or "none"), and for
   the router/HTTP epic(s): the #5/#6 fold action.
2. A brief rationale for the epic split chosen (1-2 sentences per epic is enough).
3. An explicit ordering narrative: "to reach a usable framework, these epics must land
   first: …; the remaining epics complete the 1.0 bar."
4. A single sentence marking the SSR+hydration epic as the one_oh must-have.

---

## Success criteria

- [ ] Every epic maps to ≥1 design-doc area and is a single coherent landable capability.
- [ ] Every design area from the 7 capability spokes (SSR, authoring, async/forms/events,
      router, HTTP, docs/DX, release/distribution, performance/benchmark) appears in at
      least one epic.
- [ ] The SSR+hydration epic is marked as the one_oh must-have.
- [ ] An ordering is stated that reaches a usable framework early (before the full 1.0 bar).
- [ ] The #5/#6 fold is explicit: for each of issues #5 and #6, the action (supersede or
      extend) and the epic that folds it are named.
- [ ] No REQ-*/BAR-FERRIC-* is redefined; all REQ/BAR ids used are read from the inputs.

## Constraints

- Design the epic structure; do not write the work-items (that is SUBTASK_rplan_work_items).
- Honor the writing-voice rules. GitHub-bound text (epic titles) names only repository
  identities — no system paths, no attribution trailers.
- The epic/work-item schema in `../../contracts/id_and_traceability_schema.yaml` is
  authoritative. Conform to it; do not redefine it.
