# Task: Ferric 1.0 Release Bar — framework surface gap sweep

## Task Specification

**Slug**: SUBTASK_rbar_gap
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Sweep the 24 canonical framework surfaces from the brief's surface list, plus any surfaces found in the spoke
docs that the list does not name, against the 8 spoke REQ-* registers. For each surface: determine its status
(`covered` | `out-of-1.0` | `gap`), record the REQ-* ids that cover it (for covered surfaces), and write one
sentence of notes. Produce `gap-analysis-internal.md` in the `gap_analysis_row` format declared by
`../_GLOBAL.md` and `../contracts/_MANIFEST.yaml`.

The sibling task `SUBTASK_rbar_gap_review` already produced `../../../SUBTASK_rbar_gap_review/gap-analysis.md`;
read it as a cross-check and starting reference. The output of this task must reflect an independent reading
of the spoke docs against the canonical surface list, not a copy of the sibling's document.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Canonical surface list, context, constraints |
| Subtree contract | `../contracts/_MANIFEST.yaml` | gap_analysis_row format (surface, status, req_refs, notes) |
| Scope + requirements | `../../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | REQ-FW-* register; out-of-1.0 list |
| SSR/hydration design | `../../../SUBTASK_ssr_hydration/ssr-hydration.md` | REQ-SSR-* register |
| Authoring model | `../../../SUBTASK_authoring_model/authoring-model.md` | REQ-API-* register |
| Async/forms/events | `../../../SUBTASK_async_forms_events/async-forms-events.md` | REQ-ASYNC-* register |
| Router + HTTP | `../../../SUBTASK_router_and_http/router-and-http.md` | REQ-RT-*, REQ-HTTP-* registers |
| Docs + DX | `../../../SUBTASK_docs_and_dx/docs-and-dx.md` | REQ-DX-* register |
| Release + distribution | `../../../SUBTASK_release_and_distribution/release-and-distribution.md` | REQ-REL-* register |
| Performance + benchmark | `../../../SUBTASK_performance_and_benchmark/performance-and-benchmark.md` | REQ-PERF-* register |
| Sibling gap analysis | `../../../SUBTASK_rbar_gap_review/gap-analysis.md` | Cross-check reference (read-only) |

---

## Canonical surface list (from parent brief — sweep all of these, extend if spoke docs add more)

| Surface | Primary spoke |
|---------|--------------|
| Reactive state model (signals, memos, effects, batch) | REQ-FW-* |
| Virtual DOM and DOM patching | REQ-FW-*, REQ-API-* |
| Server-side rendering (SSR) | REQ-SSR-* |
| Hydration (no re-render on client pick-up) | REQ-SSR-* |
| Authoring ergonomics / view macro / JSX-style DSL | REQ-API-* |
| Component model (props, children, slots) | REQ-API-* |
| Context / dependency injection | REQ-API-* |
| Async resources and suspense | REQ-ASYNC-* |
| Forms and two-way data binding | REQ-ASYNC-* |
| DOM event handling | REQ-ASYNC-* |
| Client-side routing (URL params, nested routes, navigation) | REQ-RT-* |
| HTTP / JSON client | REQ-HTTP-* |
| Developer documentation (guide, tutorial, API reference) | REQ-DX-* |
| DX (starter template, cargo-generate, error messages) | REQ-DX-*, REQ-FW-* |
| Release and publishing (crates.io, semver, changelog) | REQ-REL-* |
| Versioning / compatibility policy | REQ-REL-* |
| Performance and bundle size | REQ-PERF-* |
| Named-peer comparison methodology | REQ-PERF-* |
| Accessibility of framework output (ARIA, semantic HTML) | REQ-FW-* |
| Testing story (how app authors test components, routes, async) | REQ-FW-* |
| MSRV policy | REQ-FW-*, REQ-REL-* |
| Scoped CSS / styling story | explicitly out-of-1.0 |
| Browser devtools / inspector integration | explicitly out-of-1.0 |
| Hot reload / live reload | explicitly out-of-1.0 |
| Desktop / mobile targets (non-WASM) | explicitly out-of-1.0 |

---

## Declared output

- `gap-analysis-internal.md` at this workspace root

### Output format

A markdown document with two tables (required surfaces; additional surfaces found in spoke docs):

```markdown
| Surface | Status | req_refs | Notes |
|---------|--------|----------|-------|
| <surface name> | covered | REQ-X-001, REQ-Y-002 | One sentence: which REQ(s) cover it. |
| <surface name> | out-of-1.0 | | One sentence: which REQ records the deferral and why. |
| <surface name> | gap | | One sentence: what is missing and why it is a gap. |
```

Every row must include all four fields. For covered surfaces, req_refs must list at least one real REQ-* id
from the spoke documents. For out-of-1.0 surfaces, req_refs is empty. For gaps, req_refs is empty.

---

## Success criteria

- [ ] All 24 canonical surfaces assessed with a status and notes
- [ ] Any additional surfaces found in spoke docs assessed and added
- [ ] All four required out-of-1.0 surfaces (scoped CSS/styling, devtools, hot/live reload, desktop/mobile)
      are present with status=out-of-1.0
- [ ] All covered surfaces cite at least one real REQ-* id from a spoke register
- [ ] Accessibility of framework output and testing story are assessed (they may be gaps)
- [ ] gap-analysis-internal.md is written at this workspace root
