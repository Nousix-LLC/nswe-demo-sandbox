# Task: Ferric 1.0 Release Bar — framework surface gap analysis

## Task Specification
**Slug**: SUBTASK_rbar_gap_review
**Task Kind**: standard
**Depends on**: SUBTASK_scope_and_requirements, SUBTASK_ssr_hydration, SUBTASK_authoring_model, SUBTASK_async_forms_events, SUBTASK_router_and_http, SUBTASK_docs_and_dx, SUBTASK_release_and_distribution, SUBTASK_performance_and_benchmark
**Status**: Pending

### Objective

Sweep the surfaces a Rust/WASM UI framework at Ferric's level is expected to have, and for each
surface record whether the Ferric 1.0 design covers it, places it explicitly out-of-1.0, or leaves a
gap. This gap analysis is the input the criteria task reads to write the `BAR-FERRIC-*` register.

### Context

Part of the SUBTASK_release_bar decomposition (see `../_GLOBAL.md`). The surface list is anchored in the
parent brief: reactivity, rendering, SSR/hydration, authoring ergonomics, async/data, routing, HTTP,
docs/DX, release/semver, performance, accessibility-of-output, testing story, MSRV — plus any surfaces
the spoke designs surface beyond that list. For each surface, check what the relevant spoke output says
about REQ-* coverage, and what the scope-and-requirements doc says about explicit in/out-of-1.0
decisions. Peer frameworks (Leptos, Sycamore, Dioxus, Yew) and design docs can be consulted to confirm
surface expectations; cite what you actually read.

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Context, constraints, surface list |
| Parent contracts | `../../contracts/id_and_traceability_schema.yaml` | Stage vocabulary; out-of-1.0 surface list |
| This contract | `../contracts/_MANIFEST.yaml` | Required gap-analysis.md format |
| Scope + requirements | `../../SUBTASK_scope_and_requirements/scope-and-requirements.md` | Master in/out-of-1.0 decisions; `REQ-FW-*` |
| SSR/hydration design | `../../SUBTASK_ssr_hydration/ssr-hydration.md` | `REQ-SSR-*`; SSR + hydration surface coverage |
| Authoring model design | `../../SUBTASK_authoring_model/authoring-model.md` | `REQ-API-*`; view macro, props, slots, context |
| Async/forms/events | `../../SUBTASK_async_forms_events/async-forms-events.md` | `REQ-ASYNC-*`; async, forms, events |
| Router + HTTP design | `../../SUBTASK_router_and_http/router-and-http.md` | `REQ-RT-*`, `REQ-HTTP-*`; routing, HTTP client |
| Docs + DX design | `../../SUBTASK_docs_and_dx/docs-and-dx.md` | `REQ-DX-*`; documentation, DX |
| Release + distribution | `../../SUBTASK_release_and_distribution/release-and-distribution.md` | `REQ-REL-*`; publish, semver, changelog |
| Performance + benchmark | `../../SUBTASK_performance_and_benchmark/performance-and-benchmark.md` | `REQ-PERF-*`; benchmarks, bundle size |

---

## Declared output

`gap-analysis.md` — a structured surface sweep. Each entry covers one framework surface area and carries
the four fields from `../contracts/_MANIFEST.yaml`:
- **surface**: the framework surface name
- **status**: `covered` | `out-of-1.0` | `gap`
- **req_refs**: the `REQ-*` ids that address it (if `covered`; otherwise empty)
- **notes**: one sentence stating which REQ covers it, why it is out-of-1.0, or what the gap is

### Required surface list (minimum — extend if the spoke docs surface more)

| Surface | Notes to drive the sweep |
|---------|--------------------------|
| Reactive state model (signals, memos, effects, batch) | Core primitive — already in the crate |
| Virtual DOM and DOM patching | Already in the crate |
| Server-side rendering (SSR) | The must-have — check REQ-SSR-* |
| Hydration (client picks up server HTML, no re-render) | The must-have pair — check REQ-SSR-* |
| Authoring ergonomics / view macro / JSX-style DSL | Check REQ-API-* |
| Component model (props, children, slots) | Check REQ-API-* |
| Context / dependency injection | Check REQ-API-* |
| Async resources and suspense | Check REQ-ASYNC-* |
| Forms and two-way data binding | Check REQ-ASYNC-* |
| DOM event handling | Check REQ-ASYNC-* |
| Client-side routing (URL params, nested routes, navigation) | Check REQ-RT-* |
| HTTP / JSON client | Check REQ-HTTP-* |
| Developer documentation (guide, tutorial, API reference) | Check REQ-DX-* |
| DX (starter template, cargo-generate, error messages) | Check REQ-DX-* |
| Release and publishing (crates.io, semver, changelog) | Check REQ-REL-* |
| Versioning / compatibility policy | Check REQ-REL-* |
| Performance and bundle size | Check REQ-PERF-* |
| Honest peer comparison methodology | Check REQ-PERF-* |
| Accessibility of framework output (ARIA, semantic HTML) | Check REQ-FW-* and the scope doc; may be a gap |
| Testing story (how app authors test components, routes, async) | Check REQ-FW-* and the scope doc |
| MSRV policy | Check REQ-REL-* or REQ-FW-* |
| Scoped CSS / styling story | Named out-of-1.0 in scope doc — status=out-of-1.0 |
| Browser devtools / inspector integration | Named out-of-1.0 in scope doc — status=out-of-1.0 |
| Hot reload / live reload | Named out-of-1.0 in scope doc — status=out-of-1.0 |
| Desktop / mobile targets (non-WASM) | Named out-of-1.0 in scope doc — status=out-of-1.0 |

---

## Success criteria

- [ ] Every surface in the required list appears in `gap-analysis.md`; surfaces found in spoke docs
      beyond the list are added
- [ ] Every entry has a status of `covered`, `out-of-1.0`, or `gap`
- [ ] Covered entries cite ≥1 real `REQ-*` id from the relevant spoke output
- [ ] The four named out-of-1.0 items are present with `status=out-of-1.0`
- [ ] The document does not contain any `BAR-FERRIC-*` ids (those belong to SUBTASK_rbar_criteria)
- [ ] Plain prose voice; no machine-writing tells

### Constraints

- Own `gap-analysis.md` only; do not create or modify any `REQ-*`, `BAR-FERRIC-*`, or `release-bar.md`
- Cite REQ-* ids as they actually appear in the spoke outputs — do not invent ids
- Do not make implementation choices or judgments about how Ferric should meet any surface
