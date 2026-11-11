# Filed backlog — Ferric 1.0

Board: `Nousix-LLC/nswe-demo` · Parent epic: #1 · Design PR: #128 (`work/design-ferric-1_0`)

---

## De-duplication scan

Before creating any issues, the board was scanned for existing framework issues. The only issues with the `framework` label were:

| Issue | State | Description |
|---|---|---|
| #1 | Open | EPIC: ferric — the parent epic; not a work item |
| #4 | Closed | ferric-foundation: Cargo workspace + ferric core |
| #5 | Closed | ferric-router: client-side router scaffold |
| #6 | Closed | ferric-http: fetch-based HTTP/JSON client scaffold |

No existing issues correspond to any work item in the 1.0 release plan. No duplicates were created.

---

## Epics created

Eight epic issues were filed under #1, each with labels `epic` + `framework`, in dependency order:

| Issue | Title | Stage | Depends on |
|---|---|---|---|
| #129 | EPIC: Ferric 1.0 — Authoring Model | usable_early | none |
| #130 | EPIC: Ferric 1.0 — Async, Forms, and Events | usable_early | #129 |
| #131 | EPIC: Ferric 1.0 — Client-side Router | usable_early | #129 |
| #132 | EPIC: Ferric 1.0 — HTTP/JSON Client | usable_early | #129 |
| #133 | EPIC: Ferric 1.0 — SSR and Hydration | one_oh | #129, #130 |
| #134 | EPIC: Ferric 1.0 — Docs and DX | one_oh | #129–#133 |
| #135 | EPIC: Ferric 1.0 — Performance and Benchmark | one_oh | #129, #130, #133 |
| #136 | EPIC: Ferric 1.0 — Release and Distribution | one_oh | #134, #135 |

---

## Work items created

Twenty-eight work items were filed with labels `framework` + `type:feature`. Each body cites the `REQ-*`/`BAR-FERRIC-*` ids and the `design/ferric/…` section it traces to (all paths in PR #128).

### Authoring Model (under #129)

| Issue | Title | BAR-FERRIC | Depends on |
|---|---|---|---|
| #137 | Reactive state primitives | BAR-001 | none |
| #138 | Virtual DOM and keyed DOM patching | BAR-002 | #137 |
| #139 | view! macro surface and compile-time diagnostics | BAR-007, BAR-008 | #138 |
| #140 | Component model: props, children, named slots, and dynamic dispatch | BAR-009 | #139 |
| #141 | Component type-level diagnostics | BAR-010 | #140 |
| #142 | Context and dependency injection | BAR-011 | #140 |

### Async, Forms, and Events (under #130)

| Issue | Title | BAR-FERRIC | Depends on |
|---|---|---|---|
| #143 | Async resources and suspense | BAR-012 | #140 |
| #144 | DOM event handling | BAR-013 | #139 |
| #145 | Forms and two-way binding | BAR-014 | #144 |

### Client-side Router (under #131, extends #5)

| Issue | Title | BAR-FERRIC | Depends on |
|---|---|---|---|
| #146 | Core routing: path parameters, nested routes, navigation, and accessible links | BAR-015 | #139 |
| #147 | Active-route awareness | BAR-016 | #146 |

### HTTP/JSON Client (under #132, extends #6)

| Issue | Title | BAR-FERRIC | Depends on |
|---|---|---|---|
| #148 | HTTP methods, JSON bodies, and error handling | BAR-017 | #137 |
| #149 | PATCH method, per-request timeout, and lean dependency footprint | BAR-018 | #148, #159 |

### SSR and Hydration (under #133)

| Issue | Title | BAR-FERRIC | Depends on |
|---|---|---|---|
| #150 | Server-side HTML rendering and per-request scope isolation | BAR-003 | #139 |
| #151 | Client hydration without re-render **(must-have)** | BAR-004 | #150, #143 |
| #152 | State carry and async resource resume across the SSR seam | BAR-005 | #151 |
| #153 | Hydration mismatch detection and Axum integration | BAR-006 | #151 |

### Docs and DX (under #134)

| Issue | Title | BAR-FERRIC | Depends on |
|---|---|---|---|
| #154 | Conceptual guide and start-to-finish tutorial | BAR-019 | #151 |
| #155 | API docs and curated examples | BAR-020 | #154 |
| #156 | Starter template, reference app, and new-user acceptance path | BAR-021 | #155 |
| #157 | README, troubleshooting entry, and CI doc sync | BAR-022 | #154 |

### Performance and Benchmark (under #135)

| Issue | Title | BAR-FERRIC | Depends on |
|---|---|---|---|
| #158 | js-framework-benchmark entry and per-operation results | BAR-026 | #151, #143 |
| #159 | Bundle size and dependency footprint | BAR-027 | #158 |
| #160 | Peer comparison table and methodology | BAR-028 | #159 |

### Release and Distribution (under #136)

| Issue | Title | BAR-FERRIC | Depends on |
|---|---|---|---|
| #161 | Publishing readiness: crates.io metadata, licensing, and workspace versioning | BAR-023 | #156, #160 |
| #162 | Semver contract and cargo semver-checks CI enforcement | BAR-024 | #161 |
| #163 | Changelog: Keep a Changelog 1.1.0 | BAR-025 | #161 |
| #164 | Versioning and compatibility policy | BAR-029 | #161 |

---

## #5 and #6 — fold record

**Neither issue was re-opened or superseded; both received an additive comment.**

| Issue | State | Action taken |
|---|---|---|
| #5 — ferric-router scaffold | Closed (unchanged) | Comment added pointing to epic #131 (Client-side Router); notes that #131 extends #5 additively — frozen `ferric-router` prelude carried forward unchanged |
| #6 — ferric-http scaffold | Closed (unchanged) | Comment added pointing to epic #132 (HTTP/JSON Client); notes that #132 extends #6 additively — frozen `ferric-http` prelude carried forward unchanged |

The plan's fold table (add a comment, leave closed) was followed exactly. No router or HTTP duplicate issues were created (Identity I7).

---

## BAR-FERRIC coverage check

All 17 `one_oh` BAR-FERRIC-* criteria from the release plan are covered by at least one work item:

BAR-003 → #150 · BAR-004 → #151 · BAR-005 → #152 · BAR-006 → #153 · BAR-007 → #139 · BAR-008 → #139 · BAR-009 → #140 · BAR-010 → #141 · BAR-011 → #142 · BAR-015 → #146 · BAR-016 → #147 · BAR-017 → #148 · BAR-018 → #149 · BAR-019 → #154 · BAR-020 → #155 · BAR-021 → #156 · BAR-022 → #157 · BAR-023 → #161 · BAR-024 → #162 · BAR-025 → #163 · BAR-026 → #158 · BAR-027 → #159 · BAR-028 → #160 · BAR-029 → #164

usable_early BAR covered: BAR-001 → #137 · BAR-002 → #138 · BAR-012 → #143 · BAR-013 → #144 · BAR-014 → #145

---

*Sources: `../SUBTASK_release_plan/release-plan.md`, `../SUBTASK_design_pr/design_pr.md`, board scan at filing time*
