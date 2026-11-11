# Ferric 1.0 — epic landscape and order

*All epics sit under issue #1 (the Ferric epic). Each epic is one coherent, landable capability
with its own code DAG; none mixes concerns from unrelated design areas. Design references are
read-only: no `REQ-*` or `BAR-FERRIC-*` id is redefined here.*

---

## Epics under issue #1

| Title | Design area(s) | BAR-FERRIC covered | Stage | Depends on | Issue fold |
|---|---|---|---|---|---|
| Authoring Model | authoring-model (`REQ-API-*`); scope-and-requirements (`REQ-FW-003/005/014`) | BAR-001, BAR-002, BAR-007, BAR-008, BAR-009, BAR-010, BAR-011 | usable_early | none | — |
| Async, Forms, and Events | async-forms-events (`REQ-ASYNC-*`); scope-and-requirements (`REQ-FW-006`) | BAR-012, BAR-013, BAR-014 | usable_early | Authoring Model | — |
| Client-side Router | router-and-http Part 1 (`REQ-RT-*`); scope-and-requirements (`REQ-FW-007`) | BAR-015, BAR-016 | usable_early | Authoring Model | extends #5 |
| HTTP/JSON Client | router-and-http Part 2 (`REQ-HTTP-*`); scope-and-requirements (`REQ-FW-007`, `REQ-FW-013`) | BAR-017, BAR-018 | usable_early | Authoring Model | extends #6 |
| SSR and Hydration | ssr-hydration (`REQ-SSR-*`); scope-and-requirements (`REQ-FW-004`) | BAR-003, BAR-004, BAR-005, BAR-006 | one_oh | Authoring Model, Async/Forms/Events | — |
| Docs and DX | docs-and-dx (`REQ-DX-*`); scope-and-requirements (`REQ-FW-002`, `REQ-FW-008`, `REQ-FW-011`) | BAR-019, BAR-020, BAR-021, BAR-022 | one_oh | Authoring Model, Async, Forms, and Events, Client-side Router, HTTP/JSON Client, SSR and Hydration | — |
| Performance and Benchmark | performance-and-benchmark (`REQ-PERF-*`); scope-and-requirements (`REQ-FW-012`) | BAR-026, BAR-027, BAR-028 | one_oh | Authoring Model, Async, Forms, and Events, SSR and Hydration | — |
| Release and Distribution | release-and-distribution (`REQ-REL-*`); scope-and-requirements (`REQ-FW-001`, `REQ-FW-010`) | BAR-023, BAR-024, BAR-025, BAR-029 | one_oh | Docs and DX, Performance and Benchmark | — |

---

## Issues #5 and #6 fold

**Issue #5 (ferric-router scaffold) — extended by the Client-side Router epic.** Issue #5 shipped
`crates/ferric-router` as a working walking skeleton: a flat route table with path parameters,
History-API push navigation, a reactive outlet, and an in-app link, all with a frozen `prelude`
surface. That surface is carried forward unchanged. The Client-side Router epic adds, additively,
nested routes with a nested outlet, replace navigation, active-route awareness for links (`REQ-RT-007`,
`BAR-016`), and per-level fallback handling. Issue #5 is closed (done); the epic extends its scope
without reopening or superseding it.

**Issue #6 (ferric-http scaffold) — extended by the HTTP/JSON Client epic.** Issue #6 shipped
`crates/ferric-http` as a working fetch-based HTTP/JSON client: typed get/post/put/delete with serde,
error handling, and a frozen `prelude` surface. That surface is carried forward unchanged. The
HTTP/JSON Client epic adds, additively, PATCH support, configurable timeout, and a lean-dependency-
footprint requirement (`REQ-HTTP-*` additions, `BAR-018`). Issue #6 is closed (done); the epic
extends its scope without reopening or superseding it.

---

## Rationale per epic

**Authoring Model.** The reactive signals and VDOM engine (`BAR-001`, `BAR-002`) and the
developer-facing authoring surface — the `view!` macro, `#[component]` with props and children,
and context (`BAR-007` through `BAR-011`) — are a single landable capability at the `ferric`
crate level. `BAR-001` and `BAR-002` represent the floor the engine already meets in the current
codebase; the 1.0 work verifies those criteria with automated tests and completes the full authoring
surface. Every other epic in this list depends on this one landing first.

**Async, Forms, and Events.** Async resources with Suspense (`BAR-012`), full DOM event coverage
(`BAR-013`), and form and input bindings (`BAR-014`) are the three capabilities that turn the
authoring model into something an author can build a data-backed UI with. They share a design doc
(`REQ-ASYNC-*`) and a crate context and are shipped together. Two requirements in this epic
(`REQ-ASYNC-012` and `REQ-ASYNC-013`, the SSR resource seam) are one_oh and do not gate the
usable-early floor; the work-items task will stage them accordingly.

**Client-side Router.** An author cannot build a multi-view SPA without routing. The core routing
requirements (`REQ-RT-001` through `REQ-RT-006` and `REQ-RT-008`) are usable_early; active-route
awareness (`REQ-RT-007`, `BAR-016`) is one_oh polish on the same crate. Keeping both in one epic
means the `ferric-router` crate has one delivery lifecycle. The epic extends #5 rather than reopening
it, because the frozen `ferric-router` prelude from #5 is the base the 1.0 additions compose over.

**HTTP/JSON Client.** An author cannot build a real data-backed app without typed HTTP. The core HTTP
requirements (`BAR-017`) are usable_early; lean-dependency footprint and PATCH and timeout additions
(`BAR-018`) are one_oh. Same single-crate logic as the router. The epic extends #6.

**SSR and Hydration.** All twelve `REQ-SSR-*` requirements are one_oh: there is no partial SSR state
that belongs on the usable-early floor. SSR and hydration is an all-or-nothing capability — a
framework that renders HTML on the server but re-renders on hydration, or drops typed async state
across the boundary, is not shippable. The epic depends on Authoring Model (to render a component
tree) and Async, Forms, and Events (to serialize and resume async resources — `REQ-ASYNC-012` and
`REQ-ASYNC-013`).

**Docs and DX.** The guide, tutorial, API documentation, starter template, reference app, and
repository documentation (`BAR-019` through `BAR-022`) are the publication surface without which a
developer cannot adopt the framework. These are one_oh because they require the full 1.0 capability
set — including SSR — to be accurate. Writing the starter template or the guide before SSR lands
produces docs that go stale when SSR ships.

**Performance and Benchmark.** A credible 1.0 includes a js-framework-benchmark run, bundle-size
measurement, and peer comparison (`BAR-026` through `BAR-028`). These require a working application
built on the full framework, including SSR, so the numbers represent what ships. The benchmark is run
once the usable-early capabilities and SSR are both in place.

**Release and Distribution.** Publishing to crates.io, the semver policy, changelog, and the
versioning and compatibility contract (`BAR-023`, `BAR-024`, `BAR-025`, `BAR-029`) are the final
gate: the framework is not published until documentation and benchmark data are both ready. Release
and Distribution depends on Docs and DX and Performance and Benchmark, making it the last epic to
land.

---

## Ordering narrative

**To reach a usable framework:** the Authoring Model epic lands first — it is the foundation every
other epic builds on. After it lands, Async, Forms, and Events and Client-side Router and HTTP/JSON
Client can proceed in any order or in parallel; they share only the Authoring Model as a common
dependency and have no dependency on each other. When those four usable_early epics are done, an
author has a complete client-side framework: signals, components, context, async resources, forms,
events, routing, and HTTP. Real applications can be built and exercised against `chirp-frontend`.

**To complete the 1.0 bar:** SSR and Hydration lands next — it is the one_oh must-have and depends
on Authoring Model and Async, Forms, and Events. After SSR and Hydration lands, Docs and DX and
Performance and Benchmark can proceed in parallel (both depend on SSR plus the usable_early epics).
Release and Distribution is the final epic; it waits on Docs and DX and Performance and Benchmark so
the crates.io publish happens when documentation and benchmark data are both complete.

```
Authoring Model
    ├── Async, Forms, and Events ──────────────────────┐
    ├── Client-side Router (extends #5) ───────────────┤
    └── HTTP/JSON Client (extends #6) ─────────────────┤
                                                       │
         Async, Forms, and Events ─────────────────────┤
         Authoring Model ─────────────────────────────►  SSR and Hydration
                                                                │
                 all usable_early + SSR ────────────────────────┤
                                                       ┌────────┘
                                                       ├── Docs and DX
                                                       └── Performance and Benchmark
                                                                │
                                                         Release and Distribution
```

---

## SSR and Hydration as the one_oh must-have

The SSR and Hydration epic is the one_oh must-have: `BAR-FERRIC-004` (hydrate without re-render)
carries `must_have: true`, and `REQ-FW-004` states server-side rendering and hydration as the single
capability whose absence makes a 1.0 release incomplete regardless of everything else being done.
