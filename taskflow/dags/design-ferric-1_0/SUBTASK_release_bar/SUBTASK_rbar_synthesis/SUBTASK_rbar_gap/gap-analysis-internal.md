# Ferric 1.0 — Gap Analysis (internal)

Independent sweep of all canonical framework surfaces against the 8 spoke REQ-* registers.
Produced by `SUBTASK_rbar_gap`. Format: `gap_analysis_internal_row` per `contracts/_MANIFEST.yaml`.

---

## Table 1 — Canonical surfaces

| Surface | Status | req_refs | Notes |
|---------|--------|----------|-------|
| Reactive state model (signals, memos, effects, batch) | covered | REQ-FW-005, REQ-FW-009 | REQ-FW-005 registers the usable_early reactive primitives baseline (create_signal, create_memo, create_effect, batch, scoped cleanup) at the frozen 276138f surface; REQ-FW-009 holds that surface additive-only. |
| Virtual DOM and DOM patching | covered | REQ-FW-005, REQ-API-001 | REQ-FW-005 covers the frozen VNode/VElement keyed-diff surface; REQ-API-001..023 (view! macro Band A) cover the authoring interface that produces and patches VNode trees. |
| Server-side rendering (SSR) | covered | REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-005 | REQ-SSR-001..012 register the full SSR surface—render to HTML, lifecycle separation, async SSR, and the Axum integration—all one_oh and release_gating:true. |
| Hydration (no re-render on client pick-up) | covered | REQ-SSR-004 | REQ-SSR-004 is the gating must-have: client hydration from server-rendered HTML must complete without triggering a re-render of the component tree. |
| Authoring ergonomics / view macro / JSX-style DSL | covered | REQ-API-001, REQ-API-023, REQ-API-028 | REQ-API-001..029 (Band A) register the full view! macro surface—element/attribute/event syntax, conditional rendering, keyed lists, text interpolation, and trybuild diagnostics—all usable_early. |
| Component model (props, children, slots) | covered | REQ-API-030, REQ-API-034, REQ-API-045, REQ-API-049 | REQ-API-030..052 (Band B) cover typed props, optional prop defaulting, children, and slots; REQ-API-034, 045, 049 are one_oh; remainder usable_early; all release_gating:true. |
| Context / dependency injection | covered | REQ-API-060, REQ-API-065, REQ-API-070 | REQ-API-060..070 (Band C) register provide/use/expect_context, all usable_early and release_gating:true. |
| Async resources and suspense | covered | REQ-ASYNC-001, REQ-ASYNC-011, REQ-ASYNC-015, REQ-ASYNC-016 | REQ-ASYNC-001..016 cover async resource creation, the four suspense states (loading/loaded/empty/error), derived resources, and the additive-over-frozen-reactive-core rule; REQ-ASYNC-012..013 are one_oh, rest usable_early. |
| Forms and two-way data binding | covered | REQ-ASYNC-040, REQ-ASYNC-041, REQ-ASYNC-043 | REQ-ASYNC-040..043 register two-way binding for text inputs, checkboxes, selects, and textareas, all usable_early and release_gating:true. |
| DOM event handling | covered | REQ-ASYNC-020, REQ-ASYNC-021, REQ-FW-006 | REQ-ASYNC-020..024 cover the payload-carrying handler form and the full DOM event coverage surface; REQ-FW-006 registers EventKind as #[non_exhaustive] so the event range stays additive as coverage grows. |
| Client-side routing (URL params, nested routes, navigation) | covered | REQ-RT-001, REQ-RT-003, REQ-RT-005, REQ-RT-007, REQ-RT-008 | REQ-RT-001..008 cover route table with path parameters, reactive outlet, push/replace History navigation, in-app links (focusable, role="link"), nested routes with a nested outlet, per-level fallback, and active-route awareness (aria-current), all release_gating:true. |
| HTTP / JSON client | covered | REQ-HTTP-001, REQ-HTTP-007, REQ-HTTP-010, REQ-HTTP-013 | REQ-HTTP-001..013 cover the configured shareable client, fluent request builder, typed JSON round-trip, one matchable error type, PATCH method (additive), per-request timeout/cancellation, and frozen-surface forward-compatibility. |
| Developer documentation (guide, tutorial, API reference) | covered | REQ-DX-001, REQ-DX-002, REQ-DX-003, REQ-DX-010 | REQ-DX-001..003 register the conceptual guide, start-to-finish tutorial (end state compiles), and rendered API docs on docs.rs; REQ-DX-010 requires CI to keep examples and doctests in sync with the release. |
| DX (starter template, cargo-generate, error messages) | covered | REQ-DX-005, REQ-DX-006, REQ-DX-008, REQ-FW-014 | REQ-DX-005..006 cover the cargo-generate starter (CSR + SSR variant) and the scripted new-user acceptance path; REQ-DX-008 covers the troubleshooting/diagnostics doc; REQ-FW-014 owns authoring-level diagnostic quality. |
| Release and publishing (crates.io, semver, changelog) | covered | REQ-REL-001, REQ-REL-005, REQ-REL-009, REQ-REL-030 | REQ-REL-001..011 cover crates.io publishing readiness (license, metadata, path+version fix, dry-run, name ownership, lockstep coordinated release); REQ-REL-030..033 register the changelog practice. |
| Versioning / compatibility policy | covered | REQ-REL-020, REQ-REL-042, REQ-REL-043, REQ-REL-046 | REQ-REL-020..033 define the semver contract and breaking-vs-additive classification (including cargo-semver-checks gate); REQ-REL-040..047 register the 1.x compatibility policy: frozen preludes, additive-only evolution, lockstep versioning, and a discoverable written policy. |
| Performance and bundle size | covered | REQ-PERF-001, REQ-PERF-004, REQ-PERF-005, REQ-PERF-010 | REQ-PERF-001..005 cover the keyed js-framework-benchmark entry, per-operation speed/memory/size metrics, and a reproducible rerun procedure; REQ-PERF-010 ties the measured bundle size to the lean-footprint commitment (REQ-FW-013). |
| Named-peer comparison methodology | covered | REQ-PERF-006, REQ-PERF-007, REQ-PERF-008 | REQ-PERF-006..008 register the stated comparison method: same-conditions runs in the keyed category, Rust/WASM peers (Leptos, Sycamore, Dioxus, Yew) as the primary bar, full per-operation reporting with no cherry-picking, and the WASM-vs-JS memory caveat. |
| Accessibility of framework output (ARIA, semantic HTML) | gap | | No REQ-FW-* or other register entry covers general ARIA utilities or semantic HTML guidance for app-authored components; router links carry role="link" and aria-current (REQ-RT-004, REQ-RT-007) but those are routing-specific affordances, not a framework-level accessibility provision, leaving general component accessibility a design gap. |
| Testing story (how app authors test components, routes, async) | gap | | No register entry specifies a testing harness, helper crate, or methodology for app authors testing their own Ferric components, routes, or async resources; the spoke docs use automated_test as a verification method for the framework's own acceptance criteria but define no requirement about the testing surface offered to app authors. |
| MSRV policy | covered | REQ-FW-003, REQ-REL-040, REQ-REL-041 | REQ-FW-003 anchors the usable_early baseline to stable Rust (workspace declares rust-version = "1.82"); REQ-REL-040 commits 1.0 to a declared MSRV; REQ-REL-041 states that MSRV may rise only in a minor (not patch) release, recorded in the changelog. |
| Scoped CSS / styling story | out-of-1.0 | | REQ-FW-015 records scoped CSS and a styling story as a post_one_oh deferral (release_gating:false); the 1.0 design makes no styling provision beyond inline styles achievable through the view! macro. |
| Browser devtools / inspector integration | out-of-1.0 | | REQ-FW-016 records devtools and inspector integration as a post_one_oh deferral (release_gating:false), explicitly cut so the absence is not mistaken for oversight. |
| Hot reload / live reload | out-of-1.0 | | REQ-FW-017 records hot reload / HMR as a post_one_oh deferral (release_gating:false), noted in docs-and-dx.md §7 as requiring deep build-pipeline changes that are workable but not 1.0 scope. |
| Desktop / mobile targets (non-WASM) | out-of-1.0 | | REQ-FW-018 records desktop and mobile non-WASM targets as a post_one_oh deferral (release_gating:false); Ferric 1.0 targets wasm32-unknown-unknown only. |

---

## Table 2 — Additional surfaces found in spoke docs

| Surface | Status | req_refs | Notes |
|---------|--------|----------|-------|
| URL query / search parameters | out-of-1.0 | | REQ-RT-009 explicitly records router-owned reactive query/search-parameter accessors as a post_one_oh deferral (release_gating:false); an app can read window.location.search directly until this is designed post-1.0. |
| Streaming SSR / server functions / islands hydration | out-of-1.0 | | ssr-hydration.md records streaming, server functions, and islands/partial hydration as post-1.0 deferrals without REQ-SSR-* ids; all three are cut from the 1.0 SSR scope so the absence is explicit. |
| Typed / enum routes | out-of-1.0 | | router-and-http.md records Dioxus-style compile-checked typed-enum routes as a deliberate non-adoption for 1.0: retrofitting them would require redefining the frozen RoutePattern surface, which REQ-FW-009 forbids, so they are recorded as a possible future direction rather than a 1.0 capability. |

---

## Summary counts

| Status | Count |
|--------|-------|
| covered | 18 |
| gap | 2 |
| out-of-1.0 | 7 (4 canonical + 3 additional) |

**Gaps:** accessibility of framework output, testing story for app authors.

**Covered surfaces with one_oh gating:** SSR (REQ-SSR-*), hydration (REQ-SSR-004 must_have), component model partial (REQ-API-034, 045, 049), async resources partial (REQ-ASYNC-012..013), active-route awareness (REQ-RT-007), HTTP additions (REQ-HTTP-009..010, 012), all DX (REQ-DX-001..003, 005..006, 009..010), all REL (REQ-REL-001..047), all PERF (REQ-PERF-001..010).

**Note on sibling cross-check:** The sibling task's `gap-analysis.md` was not present at the expected path and could not be read; this analysis is based entirely on a direct independent sweep of the 8 spoke documents.
