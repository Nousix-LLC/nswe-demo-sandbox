# COMPLETE — SUBTASK_rbar_gap_review

**Status:** completed  
**Task:** Ferric 1.0 framework surface gap analysis  
**Output:** `gap-analysis.md`

## What was produced

`gap-analysis.md` sweeps all surfaces a Rust/WASM UI framework at Ferric's level is expected to have.
It covers the 25 required surfaces from the `_BRIEF.md` canonical list plus 4 additional surfaces
found explicitly deferred in the spoke docs.

**Summary by status:**
- **covered** (19 surfaces): reactive state model, virtual DOM and DOM patching, SSR, hydration,
  view macro, component model, context, async resources/suspense, forms/binding, DOM events,
  client routing, HTTP/JSON client, developer docs, DX/starter, release and publishing,
  versioning/compatibility policy, performance and bundle size, named-peer comparison methodology,
  MSRV policy
- **out-of-1.0** (8 surfaces): scoped CSS/styling, browser devtools, hot reload, desktop/mobile
  targets (the four named in the brief), plus streaming SSR, server functions, islands/partial
  hydration, and URL query/search parameters (from spoke docs)
- **gap** (2 surfaces): accessibility of framework output (ARIA, semantic HTML); testing story
  (how app authors test components, routes, async)

## Success criteria check

- [x] Every required surface from the brief's canonical list is present
- [x] Every entry carries a status of `covered`, `out-of-1.0`, or `gap`
- [x] Every covered entry cites ≥1 real `REQ-*` id from the relevant spoke output
- [x] The four named out-of-1.0 items appear with `status=out-of-1.0`
- [x] No `BAR-FERRIC-*` ids in the document (those belong to SUBTASK_rbar_criteria)
- [x] Plain prose voice; no machine-writing tells
- [x] Surfaces found in spoke docs beyond the required list are added

## Input sources read

All 8 spoke design documents were read in full:
- `SUBTASK_scope_and_requirements/scope-and-requirements.md` — REQ-FW-001..018
- `SUBTASK_ssr_hydration/ssr-hydration.md` — REQ-SSR-001..012
- `SUBTASK_authoring_model/authoring-model.md` — REQ-API-001..079 (63 assigned)
- `SUBTASK_async_forms_events/async-forms-events.md` — REQ-ASYNC-001..043 (25 assigned)
- `SUBTASK_router_and_http/router-and-http.md` — REQ-RT-001..009, REQ-HTTP-001..013
- `SUBTASK_docs_and_dx/docs-and-dx.md` — REQ-DX-001..010
- `SUBTASK_release_and_distribution/release-and-distribution.md` — REQ-REL-001..047
- `SUBTASK_performance_and_benchmark/performance-and-benchmark.md` — REQ-PERF-001..010
