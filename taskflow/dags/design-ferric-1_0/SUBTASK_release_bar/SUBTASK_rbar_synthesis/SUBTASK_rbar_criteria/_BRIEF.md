# Task: Ferric 1.0 Release Bar — BAR-FERRIC-* criteria

## Task Specification

**Slug**: SUBTASK_rbar_criteria
**Task Kind**: standard
**Depends on**: SUBTASK_rbar_gap
**Status**: Pending

### Objective

Read `SUBTASK_rbar_gap/gap-analysis-internal.md` and the 8 spoke design documents. For every surface with
`status=covered` in the gap analysis, write one or more `BAR-FERRIC-*` criteria — concrete, checkable
conditions a stranger could verify against the framework. Apply the `usable_early` / `one_oh` staging principle
from the scope doc. Mark the SSR+hydration criterion(a) `must_have: true` (identity I4). Write the complete
register as `bar-criteria-draft.md`.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Context, staging principle, constraints |
| Subtree contract | `../contracts/_MANIFEST.yaml` | bar_criterion format (id, statement, references, verification_method, stage, must_have) |
| Parent contract | `../../../contracts/id_and_traceability_schema.yaml` | BAR-FERRIC-* id pattern, field requirements, verification_method vocabulary |
| Gap analysis | `../SUBTASK_rbar_gap/gap-analysis-internal.md` | Source of truth for which surfaces are covered vs out-of-1.0 vs gap |
| Scope + requirements | `../../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | REQ-FW-* register; staging principle (§5); out-of-1.0 list (§6) |
| SSR/hydration design | `../../../SUBTASK_ssr_hydration/ssr-hydration.md` | REQ-SSR-* register |
| Authoring model | `../../../SUBTASK_authoring_model/authoring-model.md` | REQ-API-* register |
| Async/forms/events | `../../../SUBTASK_async_forms_events/async-forms-events.md` | REQ-ASYNC-* register |
| Router + HTTP | `../../../SUBTASK_router_and_http/router-and-http.md` | REQ-RT-*, REQ-HTTP-* registers |
| Docs + DX | `../../../SUBTASK_docs_and_dx/docs-and-dx.md` | REQ-DX-* register |
| Release + distribution | `../../../SUBTASK_release_and_distribution/release-and-distribution.md` | REQ-REL-* register |
| Performance + benchmark | `../../../SUBTASK_performance_and_benchmark/performance-and-benchmark.md` | REQ-PERF-* register |

---

## Staging principle (from scope doc §5)

- **`usable_early`**: requirements whose absence makes building a real app impossible — declarative authoring,
  async/suspense, forms/events, routing/HTTP, stable-Rust build, actionable diagnostics.
- **`one_oh`**: requirements that a credible 1.0 of this framework kind must provide — SSR+hydration (the gating
  must-have, `must_have: true`), crates.io publishing, semver/compat policy, complete docs, named-peer
  performance numbers, lean/documented dependencies, the reference app.

Apply these stages consistently. When a surface spans both stages (some REQ-* are usable_early, some are
one_oh), write separate criteria per stage or mark the criterion at the higher stage if it covers all related
REQ-*.

---

## BAR-FERRIC-* id assignment

Assign ids sequentially: BAR-FERRIC-001, BAR-FERRIC-002, ... (zero-padded 3-digit). Each id is unique in this
document. Do not reuse an id. The complete list MUST NOT reference any REQ-* id that does not exist in a spoke
register (identity I2). Do NOT write criteria for out-of-1.0 surfaces (identity IB/I5).

---

## Declared output

- `bar-criteria-draft.md` at this workspace root

### Output format

A markdown document organized by capability area. Each criterion block:

```markdown
### BAR-FERRIC-NNN — <short title>

- **Statement**: <Checkable condition a stranger can verify against the framework without guessing.>
- **References**: REQ-X-001, REQ-Y-002
- **Verification method**: <automated_test | example_build | doc_inspection | benchmark_run | publishability>
- **Stage**: <usable_early | one_oh>
- **Must have**: true   ← SSR+hydration criteria only; omit this line for all other criteria
```

Include a coverage-map appendix at the end: a table mapping every `one_oh`-gating REQ-* id (from all spokes)
to the BAR-FERRIC-* criterion(a) that enforce(s) it.

---

## Success criteria

- [ ] A BAR-FERRIC-* criterion exists for every surface with status=covered in gap-analysis-internal.md
- [ ] No criterion references an out-of-1.0 surface (identity IB)
- [ ] Every criterion references ≥1 REQ-* id that exists in a spoke register (identity I2)
- [ ] ≥1 one_oh criterion for SSR+hydration is marked must_have: true (identity I4)
- [ ] Coverage-map appendix lists every one_oh / release_gating=true REQ-* mapped to its BAR criterion (identity I3)
- [ ] Stage assignments are consistent with the staging principle from the scope doc
- [ ] bar-criteria-draft.md is written at this workspace root
