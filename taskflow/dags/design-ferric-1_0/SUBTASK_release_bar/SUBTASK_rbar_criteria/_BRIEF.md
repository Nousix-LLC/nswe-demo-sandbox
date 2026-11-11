# Task: Ferric 1.0 Release Bar — BAR-FERRIC-* criteria and staging

## Task Specification
**Slug**: SUBTASK_rbar_criteria
**Task Kind**: standard
**Depends on**: SUBTASK_rbar_gap_review, SUBTASK_scope_and_requirements, SUBTASK_ssr_hydration, SUBTASK_authoring_model, SUBTASK_async_forms_events, SUBTASK_router_and_http, SUBTASK_docs_and_dx, SUBTASK_release_and_distribution, SUBTASK_performance_and_benchmark
**Status**: Pending

### Objective

Read every `REQ-*` register from the eight spoke designs and the gap analysis, and write the complete
`BAR-FERRIC-*` register: every criterion a Ferric 1.0 must pass, each with a statement, REQ references,
a verification method, and a stage (`usable_early` | `one_oh`). Apply the MVP-vs-1.0 staging principle
consistently across all capability areas.

### Context

Part of the SUBTASK_release_bar decomposition (see `../_GLOBAL.md`). Reads the gap analysis (which
surfaces are covered, which are out-of-1.0) and maps covered surfaces to testable `BAR-FERRIC-*`
criteria. SSR+hydration is the gating must-have: at least one `one_oh` criterion must mark it
`must_have: true` (identity I4). The out-of-1.0 surfaces from the gap analysis must not appear in any
`BAR-FERRIC-*` (identity I5 / IB).

The staging principle: `usable_early` is the floor at which Ferric first lets an app author build a real
(non-toy) app. `one_oh` is the full credible 1.0 bar. A criterion with `stage=usable_early` should be
satisfiable before SSR/DX/release machinery is complete; a criterion with `stage=one_oh` is part of the
full release bar, and SSR+hydration lives here as the must-have.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Context, identity constraints |
| Parent contracts | `../../contracts/id_and_traceability_schema.yaml` | `BAR-FERRIC-*` schema, verification_method vocabulary, stage vocabulary |
| This contract | `../contracts/_MANIFEST.yaml` | Required `bar-criteria.md` format, identity definitions |
| Gap analysis | `../SUBTASK_rbar_gap_review/gap-analysis.md` | Which surfaces are covered → need criteria; which are out-of-1.0 → no criteria |
| Scope + requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | `REQ-FW-*`; the explicit MVP-vs-1.0 line; cross-cutting requirements |
| SSR/hydration design | `../../SUBTASK_ssr_hydration/ssr-hydration.md` | `REQ-SSR-*` |
| Authoring model design | `../../SUBTASK_authoring_model/authoring-model.md` | `REQ-API-*` |
| Async/forms/events | `../../SUBTASK_async_forms_events/async-forms-events.md` | `REQ-ASYNC-*` |
| Router + HTTP design | `../../SUBTASK_router_and_http/router-and-http.md` | `REQ-RT-*`, `REQ-HTTP-*` |
| Docs + DX design | `../../SUBTASK_docs_and_dx/docs-and-dx.md` | `REQ-DX-*` |
| Release + distribution | `../../SUBTASK_release_and_distribution/release-and-distribution.md` | `REQ-REL-*` |
| Performance + benchmark | `../../SUBTASK_performance_and_benchmark/performance-and-benchmark.md` | `REQ-PERF-*` |

---

## Declared output

`bar-criteria.md` — the complete `BAR-FERRIC-*` register in two parts:

**Part 1: criteria** — numbered `BAR-FERRIC-001`, `BAR-FERRIC-002`, … in order. Format each entry as:

```
### BAR-FERRIC-NNN: [short title]
- **statement**: [the checkable condition, stated plainly]
- **references**: [REQ-AREA-NNN, ...] (≥1 required)
- **verification_method**: automated_test | example_build | doc_inspection | benchmark_run | publishability
- **stage**: usable_early | one_oh
- **must_have**: true  ← only for SSR+hydration gating criteria; omit for all others
```

**Part 2: coverage map** — an appendix listing every `one_oh`-gating `REQ-*` across all spoke registers
and the `BAR-FERRIC-*` that enforces it. Format:

```
| REQ-* id | Statement summary | Enforced by |
|---|---|---|
| REQ-SSR-001 | ... | BAR-FERRIC-005 |
```

This coverage map is the direct evidence for identity I3.

---

## Success criteria

- [ ] A `BAR-FERRIC-*` criterion exists for every surface with `status=covered` in `gap-analysis.md`
- [ ] Every criterion's `references` list contains ≥1 `REQ-*` id that actually appears in the named spoke output (identity I2)
- [ ] No criterion references a surface with `status=out-of-1.0` (identity IB / I5)
- [ ] ≥1 `one_oh` criterion marks SSR+hydration with `must_have: true` (identity I4)
- [ ] Every `one_oh`-gating `REQ-*` appears in the coverage-map appendix with ≥1 `BAR-FERRIC-*` (identity I3)
- [ ] The staging principle is applied consistently throughout
- [ ] Criteria are checkable by a stranger — not aspirational prose
- [ ] Plain prose voice; no machine-writing tells

### Constraints

- Own the `BAR-FERRIC-*` namespace; do not create or modify any `REQ-*` (identity I1)
- IDs are sequential: `BAR-FERRIC-001`, `BAR-FERRIC-002`, … no gaps
- Every referenced `REQ-*` id must exist in the actual spoke output — do not invent ids
- Do not write `release-bar.md` (that belongs to `SUBTASK_rbar_synthesis`)
