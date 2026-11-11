# SYNTHESIS.md — Ferric 1.0 framework design

Overseer observation seam for the `design-ferric-1_0` subtree.

Design PR: [Nousix-LLC/nswe-demo#128](https://github.com/Nousix-LLC/nswe-demo/pull/128)
Branch: `work/design-ferric-1_0`
Board: `Nousix-LLC/nswe-demo`, parent epic #1

---

## Ferric 1.0 release bar

The full bar is at `design/ferric/release-bar.md` (PR #128). This section states the bar in the form the
overseer reads — criteria organized by stage, with the must-have called out.

### Two stages

**`usable_early`** — the floor at which a developer can build a real client-side app: signals/memos/effects/batch
with scoped cleanup, a VDOM with keyed diff, the `view!` macro and component model (props/children/slots/context),
async resources with suspense and error boundaries, forms with two-way binding, the full DOM event range, client
routing with nested routes and History-API navigation, and an HTTP/JSON client with typed request building and a
matchable error model.

**`one_oh`** — everything in `usable_early`, plus SSR + hydration (the single gating must-have), active-route
awareness, PATCH and per-request timeout in the HTTP client, complete documentation (guide, tutorial, API docs,
curated examples including an SSR + Axum + hydrate example, a `cargo-generate` starter, the `chirp-frontend`
reference app), crates.io publishing with semver enforcement and a changelog, a written compatibility policy for the
1.x line, and reproducible js-framework-benchmark numbers against the named Rust/WASM peers.

### Must-have: BAR-FERRIC-004 — Hydration without re-render

The client WASM bundle attaches to the server-rendered DOM without replacing any server-rendered element. After
hydration, event handlers fire and reactive state responds to changes. An SSR + hydrate example demonstrates the
full path. This is the single `must_have: true` criterion in the register.

### Complete BAR-FERRIC-* register (29 criteria)

| id | capability | stage |
|---|---|---|
| BAR-001 | Reactive state model | usable_early |
| BAR-002 | Virtual DOM and keyed DOM patching | usable_early |
| BAR-003 | SSR — HTML rendering | one_oh |
| BAR-004 | Hydration — no re-render **(must-have)** | one_oh |
| BAR-005 | State carry and async resource resume across SSR seam | one_oh |
| BAR-006 | Hydration mismatch detection and Axum integration | one_oh |
| BAR-007 | view! macro — elements, dynamics, component invocation | usable_early |
| BAR-008 | view! macro — compile-time diagnostics | usable_early |
| BAR-009 | Component model — props, children, named slots | usable_early |
| BAR-010 | Component model — type-level diagnostics | usable_early |
| BAR-011 | Context / dependency injection | usable_early |
| BAR-012 | Async resources and suspense | usable_early |
| BAR-013 | DOM event handling | usable_early |
| BAR-014 | Forms and two-way binding | usable_early |
| BAR-015 | Client-side routing | usable_early |
| BAR-016 | Active-route awareness | one_oh |
| BAR-017 | HTTP client — methods, JSON bodies, error handling | usable_early |
| BAR-018 | HTTP client — PATCH, timeout, lean footprint | one_oh |
| BAR-019 | Conceptual guide and start-to-finish tutorial | one_oh |
| BAR-020 | API docs and curated examples | one_oh |
| BAR-021 | Starter template, reference app, new-user acceptance path | one_oh |
| BAR-022 | README, troubleshooting entry, CI doc sync | one_oh |
| BAR-023 | Publishing readiness — crates.io, licensing, workspace versioning | one_oh |
| BAR-024 | Semver contract and mechanical enforcement | one_oh |
| BAR-025 | Changelog — Keep a Changelog 1.1.0 | one_oh |
| BAR-026 | js-framework-benchmark entry and per-operation results | one_oh |
| BAR-027 | Bundle size and dependency footprint | one_oh |
| BAR-028 | Peer comparison methodology | one_oh |
| BAR-029 | Versioning and compatibility policy | one_oh |

**12 usable_early, 17 one_oh, 1 must_have.**

### Out-of-1.0 (recorded, not silent)

| Item | REQ-FW-* |
|---|---|
| Scoped CSS / styling story | REQ-FW-015 |
| Browser devtools / component inspector | REQ-FW-016 |
| Hot reload / live reload | REQ-FW-017 |
| Desktop / mobile targets (non-WASM) | REQ-FW-018 |

None of these is referenced by any BAR-FERRIC-* criterion.

### Gap findings (not identity failures; open design questions)

Two surfaces are neither covered by the design nor explicitly deferred:

- **Accessibility of framework output.** No REQ-* requires the framework's generated markup to meet an
  accessibility standard beyond the link component. The release plan should decide whether to record this as a
  known 1.0 limitation or to add a minimal framework-level accessibility requirement.
- **Testing story.** No REQ-* provides an app author a path to test Ferric components, routes, or async flows
  with framework-provided helpers. The release plan should decide whether to address this with at minimum a
  testing guide section in the docs.

---

## Filed issues indexed by epic

All issues are in `Nousix-LLC/nswe-demo`. Design docs referenced are in PR #128.

### Epic #129 — Authoring Model (`usable_early`)

| Issue | Title | BAR |
|---|---|---|
| #137 | Reactive state primitives | BAR-001 |
| #138 | Virtual DOM and keyed DOM patching | BAR-002 |
| #139 | view! macro surface and compile-time diagnostics | BAR-007, BAR-008 |
| #140 | Component model: props, children, named slots, and dynamic dispatch | BAR-009 |
| #141 | Component type-level diagnostics | BAR-010 |
| #142 | Context and dependency injection | BAR-011 |

### Epic #130 — Async, Forms, and Events (`usable_early`)

| Issue | Title | BAR |
|---|---|---|
| #143 | Async resources and suspense | BAR-012 |
| #144 | DOM event handling | BAR-013 |
| #145 | Forms and two-way binding | BAR-014 |

### Epic #131 — Client-side Router (`usable_early`, extends #5)

| Issue | Title | BAR |
|---|---|---|
| #146 | Core routing: path parameters, nested routes, navigation, and accessible links | BAR-015 |
| #147 | Active-route awareness | BAR-016 |

### Epic #132 — HTTP/JSON Client (`usable_early`, extends #6)

| Issue | Title | BAR |
|---|---|---|
| #148 | HTTP methods, JSON bodies, and error handling | BAR-017 |
| #149 | PATCH method, per-request timeout, and lean dependency footprint | BAR-018 |

### Epic #133 — SSR and Hydration (`one_oh`, must-have)

| Issue | Title | BAR |
|---|---|---|
| #150 | Server-side HTML rendering and per-request scope isolation | BAR-003 |
| #151 | Client hydration without re-render **(must-have)** | BAR-004 |
| #152 | State carry and async resource resume across the SSR seam | BAR-005 |
| #153 | Hydration mismatch detection and Axum integration | BAR-006 |

### Epic #134 — Docs and DX (`one_oh`)

| Issue | Title | BAR |
|---|---|---|
| #154 | Conceptual guide and start-to-finish tutorial | BAR-019 |
| #155 | API docs and curated examples | BAR-020 |
| #156 | Starter template, reference app, and new-user acceptance path | BAR-021 |
| #157 | README, troubleshooting entry, and CI doc sync | BAR-022 |

### Epic #135 — Performance and Benchmark (`one_oh`)

| Issue | Title | BAR |
|---|---|---|
| #158 | js-framework-benchmark entry and per-operation results | BAR-026 |
| #159 | Bundle size and dependency footprint | BAR-027 |
| #160 | Peer comparison table and methodology | BAR-028 |

### Epic #136 — Release and Distribution (`one_oh`)

| Issue | Title | BAR |
|---|---|---|
| #161 | Publishing readiness: crates.io metadata, licensing, and workspace versioning | BAR-023 |
| #162 | Semver contract and cargo semver-checks CI enforcement | BAR-024 |
| #163 | Changelog: Keep a Changelog 1.1.0 | BAR-025 |
| #164 | Versioning and compatibility policy | BAR-029 |

**28 work items across 8 epics. Issues #5 and #6 received additive comments (not re-opened).**

---

## Contract identity assertions (I1–I9)

Asserted against `contracts/_MANIFEST.yaml`, `release-bar.md`, `release-plan.md`, `design_pr.md`, and
`filed_backlog.md`. A finding is stated directly; no result is plugged or invented.

### I1 — Disjoint registers

**PASS (structural).** The contract partitions the nine REQ namespaces (REQ-FW-*, REQ-SSR-*, REQ-API-*,
REQ-ASYNC-*, REQ-RT-*, REQ-HTTP-*, REQ-DX-*, REQ-REL-*, REQ-PERF-*) to distinct owning children.
The BAR-FERRIC-* coverage map in release-bar.md §4 references each area's ids only within its registered
namespace — no cross-namespace authoring is visible in the assembled artifacts. Full per-file verification
(reading every spoke's REQ id list against its declared namespace) was not run; I1 is stated as structurally
enforced by the contract and confirmed by the assembled outputs read at synthesis time.

### I2 — No invented REQ

**PASS.** Every BAR-FERRIC-* criterion in release-bar.md cites ≥1 REQ-* id. All cited ids fall within the
registered namespaces in the contract ownership table. No BAR criterion invents a REQ id outside a registered
area.

### I3 — Gating coverage

**PASS.** The coverage map in release-bar.md §4 lists every one_oh-stage REQ-* id across all eight areas and
maps each to ≥1 BAR-FERRIC-* entry. The map has no empty rows. All 17 one_oh BAR-FERRIC-* criteria are
covered by ≥1 work item (confirmed by release-plan.md's own J3 check and filed_backlog.md's BAR coverage
table).

### I4 — SSR is the must-have

**PASS.** BAR-FERRIC-004 (Hydration — client picks up server HTML, no re-render) carries `must_have: true`
and stage `one_oh` in release-bar.md. It is the only criterion in the register with that field.

### I5 — Out-of-1.0 is recorded

**PASS.** Scoped CSS/styling (REQ-FW-015), browser devtools (REQ-FW-016), hot reload (REQ-FW-017), and
desktop/mobile targets (REQ-FW-018) are explicitly listed as out-of-1.0 in release-bar.md §5. None is
referenced by any BAR-FERRIC-* criterion. The additional spoke-level deferrals (streaming SSR, server actions,
islands/partial hydration, URL query parameters) are also recorded as out-of-1.0 in the same section.

### I6 — Plan traces

**PASS.** Each of the eight epics in release-plan.md names the design-doc area(s) it covers and the
BAR-FERRIC-* criteria it satisfies. Each work item cites the REQ-* and BAR-FERRIC-* ids it satisfies and the
design-doc section it traces to. The plan's own J1–J3 verification confirms: no orphan work items (J1); fold
is explicit with issue numbers in the fold table (J2); all 17 one_oh BAR-FERRIC-* covered by ≥1 work item (J3).

### I7 — #5 and #6 folded, not duplicated

**PASS.** The release plan's fold table records that issue #5 (ferric-router scaffold) is extended by epic #131
and issue #6 (ferric-http scaffold) is extended by epic #132, each additively over the frozen prelude surface.
filed_backlog.md confirms: both issues remain closed; a comment was added to each pointing to the extending
epic; no router or HTTP duplicate issues were created.

### I8 — Artifacts placed once

**PASS.** design_pr.md lists each of the ten owned design artifacts (plus README and three contract files)
placed at its declared `design/ferric/` repo path in PR #128. Each path appears exactly once in the files-placed
table. The design_pr.md I8 check confirms no artifact is unplaced or double-placed.

### I9 — Frozen surfaces respected

**PASS.** BAR-FERRIC-015 requires all ferric-router prelude surfaces from the #5 baseline to be present at 1.0
without removal or redefinition; the Client-side Router epic adds capabilities additively. BAR-FERRIC-017
requires all ferric-http prelude surfaces from the #6 baseline to be present at 1.0 without removal or
redefinition; the HTTP/JSON Client epic adds capabilities additively. Both work items carry explicit acceptance
criteria confirming the additive-over-frozen-surface constraint. The release plan's fold section states: "the
frozen prelude carried forward unchanged."

### Summary

All nine identities **PASS**. No identity failure to report. The two gap findings above (accessibility and
testing story) are open design questions the release plan should address; they do not constitute identity
failures for this subtree.

---

*Authored by SUBTASK_synthesis · fold target: design-ferric-1_0 · 2026-10-29*
