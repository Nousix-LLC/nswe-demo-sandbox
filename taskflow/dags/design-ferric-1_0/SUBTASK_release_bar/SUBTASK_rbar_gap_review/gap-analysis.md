# Ferric 1.0 — Framework Surface Gap Analysis

This document sweeps the surfaces a Rust/WASM UI framework at Ferric's level is expected to have and records,
for each, whether the Ferric 1.0 design covers it, places it explicitly out of 1.0, or leaves a gap. It is the
input `SUBTASK_rbar_criteria` reads to write the `BAR-FERRIC-*` register.

Each row carries the four fields the `../contracts/_MANIFEST.yaml` schema requires: **surface**, **status**
(`covered` | `out-of-1.0` | `gap`), **req_refs** (comma-separated `REQ-*` ids for covered surfaces; empty
otherwise), and **notes** (one sentence stating which REQ covers it, why it is out of 1.0, or what the gap is).

The required surfaces below come from the `_BRIEF.md` canonical list. Surfaces found explicitly deferred or
noted in the spoke docs beyond that list are added in a second table.

---

## Required surfaces

| Surface | Status | req_refs | Notes |
|---|---|---|---|
| Reactive state model (signals, memos, effects, batch) | covered | REQ-FW-005 | REQ-FW-005 requires fine-grained signal reactivity (create_signal, create_memo, create_effect, batch, scoped cleanup); the baseline crate already implements all of these. |
| Virtual DOM and DOM patching | covered | REQ-FW-005, REQ-API-001 | The baseline ships a keyed VNode diff applied to the live DOM via web-sys; REQ-FW-005 covers the reactive rendering model and REQ-API-001 grounds the view macro in that same layer. |
| Server-side rendering (SSR) | covered | REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-011 | REQ-SSR-001 through REQ-SSR-003 require server HTML rendering, a renderable core that builds off WASM, and per-request isolation; REQ-SSR-011 requires Axum integration. |
| Hydration (client picks up server HTML, no re-render) | covered | REQ-SSR-004, REQ-SSR-005, REQ-SSR-007, REQ-SSR-008, REQ-SSR-009 | REQ-SSR-004 (the gating must-have) requires hydration with no client re-render; the remaining ids cover event wiring on hydrate, state carry from server-resolved resources, first-render determinism, and mismatch detection and recovery. |
| Authoring ergonomics / view macro / JSX-style DSL | covered | REQ-API-001 | Band A (REQ-API-001..029) covers the view! macro surface: HTML elements with attributes and properties, dynamic expressions, conditionals, keyed list rendering via `<For>`, and component invocation; all stage usable_early. |
| Component model (props, children, slots) | covered | REQ-API-030, REQ-API-034, REQ-API-045, REQ-API-049 | Band B (REQ-API-030..052) covers required and optional props with defaults, children as VNode, named slots, converting props (REQ-API-034), parameterized slots (REQ-API-045), and dynamic dispatch (REQ-API-049); the last three are one_oh. |
| Context / dependency injection | covered | REQ-API-060 | Band C (REQ-API-060..070) requires provide_context, use_context, and expect_context over the component tree; all stage usable_early. |
| Async resources and suspense | covered | REQ-ASYNC-001, REQ-ASYNC-012, REQ-ASYNC-013 | REQ-ASYNC-001..016 cover create_resource with four resource states (loading, loaded, empty, error), suspense boundaries, and the SSR resource seam; REQ-ASYNC-012 and REQ-ASYNC-013 (SSR seam) are one_oh, the rest usable_early. |
| Forms and two-way data binding | covered | REQ-ASYNC-040, REQ-ASYNC-041, REQ-ASYNC-042, REQ-ASYNC-043 | REQ-ASYNC-040..043 cover two-way binding, the full input-kind range (text, checkbox, select), validation ergonomics, and form submission; all stage usable_early. |
| DOM event handling | covered | REQ-ASYNC-020, REQ-ASYNC-021, REQ-ASYNC-022, REQ-ASYNC-023, REQ-ASYNC-024, REQ-FW-006 | REQ-ASYNC-020..024 and REQ-FW-006 cover the payload handler form, the full DOM event range (submit, keyboard, focus/blur, change), default prevention, propagation control, and an escape hatch for events named by string; all usable_early. |
| Client-side routing (URL params, nested routes, navigation) | covered | REQ-RT-001, REQ-RT-002, REQ-RT-003, REQ-RT-004, REQ-RT-005, REQ-RT-006, REQ-RT-007, REQ-RT-008 | REQ-RT-001..008 cover the route table with path parameters, a reactive outlet, History-API push and replace navigation, in-app focusable links, nested routes with a nested outlet, per-level fallback, active-route awareness, and the additive-over-frozen-surface identity; URL query/search parameters are a recorded post-1.0 deferral (REQ-RT-009). |
| HTTP / JSON client | covered | REQ-HTTP-001, REQ-HTTP-004, REQ-HTTP-005, REQ-HTTP-007, REQ-HTTP-008, REQ-HTTP-009, REQ-HTTP-010, REQ-HTTP-013 | REQ-HTTP-001..013 cover client configuration, fluent request building with URL resolution and RFC-3986 encoding, typed JSON request and response bodies, a matchable error model, safe-by-default non-2xx handling, PATCH method coverage (one_oh), and per-request timeout and cancellation (one_oh). |
| Developer documentation (guide, tutorial, API reference) | covered | REQ-DX-001, REQ-DX-002, REQ-DX-003, REQ-DX-004, REQ-DX-008, REQ-DX-009, REQ-DX-010 | REQ-DX-001..010 require a conceptual guide, a tutorial whose end state compiles, rendered API docs for all three preludes on docs.rs, a curated examples set across the capability span (including an SSR + hydrate example), a troubleshooting entry, an accurate landing README, and CI-enforced sync between docs and the shipped API. |
| DX (starter template, cargo-generate, error messages) | covered | REQ-DX-005, REQ-DX-006, REQ-DX-007, REQ-FW-014 | REQ-DX-005..007 require a cargo-generate CSR starter and an SSR + Axum variant, build and toolchain documentation for both paths, and the integrating new-user acceptance path (scaffold → serve → tutorial to compiling end state); REQ-FW-014 requires trybuild-checkable macro diagnostics. |
| Release and publishing (crates.io, semver, changelog) | covered | REQ-REL-001, REQ-REL-004, REQ-REL-005, REQ-REL-009, REQ-REL-020, REQ-REL-021, REQ-REL-026, REQ-REL-030, REQ-REL-031 | REQ-REL-001..011 cover licensing, per-crate crates.io metadata, the path→version conversion for intra-workspace deps, cargo package readiness, and coordinated lockstep release; REQ-REL-020..033 cover the semver level contract, breaking-vs-additive classification with mechanical enforcement via cargo-semver-checks, and changelog practice following Keep a Changelog 1.1.0. |
| Versioning / compatibility policy | covered | REQ-REL-040, REQ-REL-041, REQ-REL-042, REQ-REL-043, REQ-REL-044, REQ-REL-046, REQ-REL-047 | REQ-REL-040..047 declare the 1.0 MSRV via the rust-version field, the MSRV raise rule within 1.x (minor release only, changelog-recorded), frozen-prelude stability for the 1.x line, additive-only public-surface evolution, lockstep versioning of the three crates, and a written discoverable compatibility policy that names both what the promise covers and what it does not. |
| Performance and bundle size | covered | REQ-PERF-001, REQ-PERF-002, REQ-PERF-003, REQ-PERF-004, REQ-PERF-010 | REQ-PERF-001..004 and REQ-PERF-010 require a keyed js-framework-benchmark entry using Ferric's public API, per-operation speed metrics for every standard operation, memory metrics, and bundle and startup size from the optimized build; REQ-PERF-010 ties the measured size to the documented dependency set as the objective check on the lean-footprint commitment. |
| Named-peer comparison methodology | covered | REQ-PERF-005, REQ-PERF-006, REQ-PERF-007, REQ-PERF-008, REQ-PERF-009 | REQ-PERF-006..009 require a stated comparison method (same conditions, keyed category, full per-operation table, no cherry-picking, measured results kept distinct from pre-measurement targets), comparison against the named Rust/WASM peers (Leptos, Sycamore, Dioxus, Yew), and the JS field as context with the WASM-vs-JS memory and bundle caveats explicitly stated. |
| Accessibility of framework output (ARIA, semantic HTML) | gap | | No REQ-* in any spoke requires the framework's generated markup to meet any accessibility standard — no ARIA role coverage, no semantic HTML expectation, no keyboard navigation requirement beyond the link component; REQ-RT-004 requires the link component specifically to be keyboard-focusable and announced by assistive technology, but the general case (all framework-generated markup) is not addressed. |
| Testing story (how app authors test components, routes, async) | gap | | No REQ-* in any spoke addresses how an app author tests their Ferric components, routes, or async flows — no component testing API, no test utilities, no integration test patterns; REQ-FW-014 and REQ-API-* cover trybuild-checkable macro diagnostics, and REQ-DX-010 covers CI for the framework's own docs and examples, but neither provides a path for app authors to write component or integration tests. |
| MSRV policy | covered | REQ-FW-003, REQ-REL-040, REQ-REL-041 | REQ-FW-003 requires stable Rust and the standard WASM toolchain; REQ-REL-040 requires the MSRV to be declared at 1.0 via the rust-version field (the workspace already pins rust-version = "1.82" in [workspace.package]); REQ-REL-041 states the rule for raising it within 1.x. |
| Scoped CSS / styling story | out-of-1.0 | | REQ-FW-015 defers scoped CSS and a first-class styling story to post-1.0; app authors use global stylesheets and external CSS tooling for 1.0. |
| Browser devtools / inspector integration | out-of-1.0 | | REQ-FW-016 defers browser devtools integration (component inspector, signal viewer) to post-1.0. |
| Hot reload / live reload | out-of-1.0 | | REQ-FW-017 defers hot/live reload to post-1.0; the standard edit-rebuild-refresh loop is the documented 1.0 development path (REQ-DX-007 covers build path documentation). |
| Desktop / mobile targets (non-WASM) | out-of-1.0 | | REQ-FW-018 defers non-WASM targets (desktop, mobile, native) to post-1.0; Ferric 1.0 targets wasm32-unknown-unknown only. |

---

## Additional surfaces found in spoke docs

The following surfaces are explicitly deferred or named in spoke outputs but do not appear in the brief's
canonical list.

| Surface | Status | req_refs | Notes |
|---|---|---|---|
| Streaming SSR | out-of-1.0 | | The SSR design explicitly records streaming SSR as outside the 1.0 bar, with no REQ-SSR-* assigned; the 1.0 model is full-page, eager server rendering. |
| Server functions / server actions | out-of-1.0 | | The SSR design explicitly records server functions and server actions as outside the 1.0 bar, with no REQ-SSR-* assigned; the async resource pattern (REQ-ASYNC-001..016) is the 1.0 data-loading model. |
| Islands / partial hydration | out-of-1.0 | | The SSR design explicitly records islands architecture and partial hydration as outside the 1.0 bar; REQ-SSR-004 covers full-page hydration only. |
| URL query / search-string parameters | out-of-1.0 | | REQ-RT-009 explicitly defers router-owned reactive query/search-string parameters to post-1.0; app authors can read window.location.search directly for 1.0. |
