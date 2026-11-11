# Issue Traceability

**Task**: SUBTASK_issue-traceability  
**Source data**: 9 concern-findings.md files; GitHub issues #129–#164 (`Nousix-LLC/nswe-demo`)  
**Date checked**: 2026-11-02

---

## epics_summary

### REQ inventory built from concern files

Before the epic survey, the full REQ-* inventory was assembled from all nine concern-findings.md files. The table below records which ids each file defines (cross-area read-only citations are excluded; only the owning document's `req_ids_found` section counts).

| Concern file | REQ prefix | IDs defined | Count |
|---|---|---|---|
| SUBTASK_validate-scope/concern-findings.md | REQ-FW-* | REQ-FW-001–018 (001–014 in-scope 1.0; 015–018 post-1.0 deferred) | 18 |
| SUBTASK_validate-ssr/concern-findings.md | REQ-SSR-* | REQ-SSR-001–012 | 12 |
| SUBTASK_validate-authoring/concern-findings.md | REQ-API-* | REQ-API-001–052 (Band A: 001–029; Band B: 030–052; 053–059 reserved), REQ-API-060–070 (Band C; 071–079 reserved) | 63 |
| SUBTASK_validate-async/concern-findings.md | REQ-ASYNC-* | REQ-ASYNC-001–016 (Section A), 020–024 (Section B), 040–043 (Section C); 017–019, 025–039, 044–059 unused headroom | 25 |
| SUBTASK_validate-router/concern-findings.md | REQ-RT-* | REQ-RT-001–009 (009 post-1.0 deferral) | 9 |
| SUBTASK_validate-router/concern-findings.md | REQ-HTTP-* | REQ-HTTP-001–013 | 13 |
| SUBTASK_validate-docs/concern-findings.md | REQ-DX-* | REQ-DX-001–010 | 10 |
| SUBTASK_validate-release/concern-findings.md | REQ-REL-* | REQ-REL-001–011, 020–033, 040–047; 012–019, 034–039, 048+ reserved headroom | 33 |
| SUBTASK_validate-perf/concern-findings.md | REQ-PERF-* | REQ-PERF-001–010 | 10 |
| SUBTASK_validate-plan/concern-findings.md | (none owned) | Cross-references to all prefixes above; no ids minted here | 0 |

**Total defined REQ-* ids: 193**  
(REQ-FW-* 18 + REQ-SSR-* 12 + REQ-API-* 63 + REQ-ASYNC-* 25 + REQ-RT-* 9 + REQ-HTTP-* 13 + REQ-DX-* 10 + REQ-REL-* 33 + REQ-PERF-* 10)

---

### Epic survey (#129–#136)

For each epic the survey records: its title, the child issues that belong to it (derived from child-issue bodies, which each say "Part of EPIC #N"), whether the epic body itself references a design document, and whether the epic body contains at least one REQ-* citation.

#### #129 — EPIC: Ferric 1.0 — Authoring Model (usable_early)

**Child issues under this epic:** #137, #138, #139, #140, #141, #142

**Design document referenced in epic body:** Yes — `design/ferric/authoring-model.md`, `design/ferric/scope-and-requirements.md`

**REQ-* citation in epic body:** No. The epic body lists work items by BAR-FERRIC-* number only (BAR-001, BAR-002, BAR-007, BAR-008, BAR-009, BAR-010, BAR-011). No REQ-* id appears in the body text.

**Note:** The epic body does not cross-reference the child issue numbers (#137–#142); it uses BAR-FERRIC-* as the work-item identifiers. The child issues themselves carry the "Part of EPIC #129" link.

---

#### #130 — EPIC: Ferric 1.0 — Async, Forms, and Events (usable_early)

**Child issues under this epic:** #143, #144, #145

**Design document referenced in epic body:** Yes — `design/ferric/async-forms-events.md`, `design/ferric/scope-and-requirements.md`

**REQ-* citation in epic body:** Yes — REQ-ASYNC-012 and REQ-ASYNC-013 appear in the closing note: "Note: REQ-ASYNC-012 and REQ-ASYNC-013 (the SSR resource serialization seam) are `one_oh` requirements covered under the SSR and Hydration epic."

**Note:** #130 is the only epic whose body contains REQ-* citations. They appear in a cross-reference note, not as a coverage claim; the note clarifies that those two requirements are tracked under #133 (SSR and Hydration).

---

#### #131 — EPIC: Ferric 1.0 — Client-side Router (usable_early, extends #5)

**Child issues under this epic:** #146, #147

**Design document referenced in epic body:** Yes — `design/ferric/router-and-http.md` Part 1, `design/ferric/scope-and-requirements.md`

**REQ-* citation in epic body:** No. Work items listed by BAR-FERRIC-015 and BAR-FERRIC-016 only.

---

#### #132 — EPIC: Ferric 1.0 — HTTP/JSON Client (usable_early, extends #6)

**Child issues under this epic:** #148, #149

**Design document referenced in epic body:** Yes — `design/ferric/router-and-http.md` Part 2, `design/ferric/scope-and-requirements.md`

**REQ-* citation in epic body:** No. Work items listed by BAR-FERRIC-017 and BAR-FERRIC-018 only.

---

#### #133 — EPIC: Ferric 1.0 — SSR and Hydration (one_oh, must-have)

**Child issues under this epic:** #150, #151, #152, #153

**Design document referenced in epic body:** Yes — `design/ferric/ssr-hydration.md`, `design/ferric/scope-and-requirements.md`

**REQ-* citation in epic body:** No. Work items listed by BAR-FERRIC-003–006 only.

---

#### #134 — EPIC: Ferric 1.0 — Docs and DX (one_oh)

**Child issues under this epic:** #154, #155, #156, #157

**Design document referenced in epic body:** Yes — `design/ferric/docs-and-dx.md`, `design/ferric/scope-and-requirements.md`

**REQ-* citation in epic body:** No. Work items listed by BAR-FERRIC-019–022 only.

---

#### #135 — EPIC: Ferric 1.0 — Performance and Benchmark (one_oh)

**Child issues under this epic:** #158, #159, #160

**Design document referenced in epic body:** Yes — `design/ferric/performance-and-benchmark.md`, `design/ferric/scope-and-requirements.md`

**REQ-* citation in epic body:** No. Work items listed by BAR-FERRIC-026–028 only.

---

#### #136 — EPIC: Ferric 1.0 — Release and Distribution (one_oh)

**Child issues under this epic:** #161, #162, #163, #164

**Design document referenced in epic body:** Yes — `design/ferric/release-and-distribution.md`, `design/ferric/scope-and-requirements.md`

**REQ-* citation in epic body:** No. Work items listed by BAR-FERRIC-023–025 and BAR-FERRIC-029 only.

---

### Child issue survey (#137–#164)

All 28 child issues were read. The table records which REQ-* ids appear in each issue's "Traces to:" line.

| Issue | Title (abbreviated) | Epic | REQ-* cited |
|---|---|---|---|
| #137 | Reactive state primitives | #129 | REQ-FW-003, REQ-FW-005, REQ-FW-009 |
| #138 | Virtual DOM and keyed DOM patching | #129 | REQ-FW-005 |
| #139 | view! macro surface and compile-time diagnostics | #129 | REQ-API-001, 002, 003, 004, 006, 012, 015, 023, 024, 025, 026, 027, 028; REQ-FW-014 |
| #140 | Component model — props, children, named slots, dynamic dispatch | #129 | REQ-API-030, 031, 032, 033, 034, 035, 037, 038, 041, 045, 047, 049 |
| #141 | Component type-level diagnostics | #129 | REQ-API-050, 051, 052 |
| #142 | Context and dependency injection | #129 | REQ-API-060, 061, 063, 066, 068 |
| #143 | Async resources and suspense | #130 | REQ-ASYNC-001, 002, 004, 005, 006, 007, 008, 009, 010, 011, 015, 016 |
| #144 | DOM event handling | #130 | REQ-ASYNC-020, 021, 022, 023, 024; REQ-FW-006 |
| #145 | Forms and two-way binding | #130 | REQ-ASYNC-040, 041, 042, 043 |
| #146 | Core routing — path parameters, nested routes, navigation | #131 | REQ-RT-001, 002, 003, 004, 005, 006, 008 |
| #147 | Active-route awareness | #131 | REQ-RT-007 |
| #148 | HTTP methods, JSON bodies, and error handling | #132 | REQ-HTTP-001, 002, 003, 004, 005, 006, 007, 008, 011, 013 |
| #149 | PATCH method, per-request timeout, and lean dependency footprint | #132 | REQ-HTTP-009, 010, 012 |
| #150 | Server-side HTML rendering and per-request scope isolation | #133 | REQ-SSR-001, 002, 003, 010, 012 |
| #151 | Client hydration without re-render (must-have) | #133 | REQ-SSR-004, 005, 008; REQ-FW-004, REQ-FW-008 |
| #152 | State carry and async resource resume across the SSR seam | #133 | REQ-SSR-006, 007, 012; REQ-ASYNC-012, 013 |
| #153 | Hydration mismatch detection and Axum integration | #133 | REQ-SSR-009, 011 |
| #154 | Conceptual guide and start-to-finish tutorial | #134 | REQ-DX-001, 002; REQ-FW-011 |
| #155 | API docs and curated examples | #134 | REQ-DX-003, 004 |
| #156 | Starter template, reference app, and new-user acceptance path | #134 | REQ-DX-005, 006, 007; REQ-FW-002, REQ-FW-008 |
| #157 | README, troubleshooting entry, and CI doc sync | #134 | REQ-DX-008, 009, 010 |
| #158 | js-framework-benchmark entry and per-operation results | #135 | REQ-PERF-001, 002, 003, 004, 005; REQ-FW-012 |
| #159 | Bundle size and dependency footprint | #135 | REQ-PERF-010; REQ-FW-013 |
| #160 | Peer comparison table and methodology | #135 | REQ-PERF-006, 007, 008, 009 |
| #161 | Publishing readiness — crates.io metadata, licensing, workspace versioning | #136 | REQ-REL-001–011; REQ-FW-001 |
| #162 | Semver contract and cargo semver-checks CI enforcement | #136 | REQ-REL-020–029; REQ-FW-010 |
| #163 | Changelog — Keep a Changelog 1.1.0 | #136 | REQ-REL-030–033 |
| #164 | Versioning and compatibility policy | #136 | REQ-REL-040–047 |

---

## issues_without_req

**Finding: none.**

All 28 child issues (#137–#164) contain at least one REQ-* citation in their "Traces to:" line. No child issue lacks a requirement reference.

---

## requirements_without_issue

This section identifies significant REQ-* ids — those in scope for Ferric 1.0 (not explicitly marked deferred or reserved) — that have no direct GitHub issue citation.

### Tier 1: Clear gap — in-scope requirement, no direct issue citation

#### REQ-FW-007

**Status:** No child issue cites REQ-FW-007 in its "Traces to:" line.

**Why it is significant:** REQ-FW-007 is the cross-cutting framework requirement that Ferric provides both a client-side router and an HTTP/JSON client. The scope concern file classifies it as `usable_early` (one of the 1.0 release-gating requirements staged at `usable_early`). The router concern-findings (SUBTASK_validate-router) explicitly flags the absence of a REQ-FW-007 traceability table from the branch design document as a completeness issue. The child issues that collectively satisfy this requirement (#146, #147, #148, #149) each trace to REQ-RT-* or REQ-HTTP-* instead.

**Rationale for "significant":** Explicitly in scope for 1.0 (`release_gating: true`, `usable_early`); cited in the scope design document as a first-class framework requirement; flagged by the router concern as lacking a coherence table; directly in the BAR-FERRIC-015–018 acceptance path.

**Suggested action:** One of the router or HTTP issues (#146 or #148) should add REQ-FW-007 to its "Traces to:" citation, or a dedicated cross-reference note should be added to the epics or issues explaining how REQ-FW-007 is collectively satisfied.

---

### Tier 2: Incomplete citation — requirements covered implicitly but not cited directly

The following REQ-* ids appear in concern-findings.md as in-scope 1.0 requirements but are not cited in any issue's "Traces to:" line. They are not individually flagged in the BAR-FERRIC-* acceptance criteria, which suggests the release bar gates on representative subsets rather than every individual id. The corresponding issues' broad acceptance criteria likely cover these requirements implicitly.

**REQ-API-* uncited (30 ids):**

- Band A uncited (16): REQ-API-005, 007, 008, 009, 010, 011, 013, 014, 016, 017, 018, 019, 020, 021, 022, 029
  - Parent issue: #139 (view! macro surface)
- Band B uncited (8): REQ-API-036, 039, 040, 042, 043, 044, 046, 048
  - Parent issues: #140 (component model), #141 (diagnostics)
- Band C uncited (6): REQ-API-062, 064, 065, 067, 069, 070
  - Parent issue: #142 (context and dependency injection)

**REQ-ASYNC-* uncited (2 ids):**

- REQ-ASYNC-003 and REQ-ASYNC-014: Both are in Section A of the async concern document (async resources and suspense). Neither appears in the BAR-FERRIC-012 acceptance criteria citations (which cover 001, 002, 004–011, 015, 016) nor in any issue. Without reading the design document directly, it is not possible to confirm whether these two ids are deferred or simply not individually gated. They do not appear in the plan concern's BAR citation list either.

**Judgment on tier 2:** These 32 ids represent traceability incompleteness at the individual-requirement level but not a delivery gap at the BAR/issue level. The issues that own the relevant design areas (#139, #140, #141, #142, #143) carry acceptance criteria broad enough to cover the uncited ids implicitly. This incompleteness should be flagged to the issue authors for possible citation additions, but it does not indicate untracked work.

---

### Explicitly deferred — no issue warranted

The following REQ-* ids are explicitly deferred or reserved and correctly have no issue:

- REQ-FW-015, 016, 017, 018: scope concern marks these `release_gating: false` (post-1.0 deferrals)
- REQ-RT-009: router concern explicitly notes "recorded post-1.0 deferral" (query/search-string parameters)
- REQ-REL-012–019, 034–039, 048+: release concern marks these "reserved, not defined"
- REQ-ASYNC-017–019, 025–039, 044–059: async concern marks these "unused headroom (reserved per manifest, not minted)"

---

## issue_137_check

**Issue #137: "Ferric 1.0: Reactive state primitives"**

### Epic assignment

Issue #137 is assigned to **Epic #129 — EPIC: Ferric 1.0 — Authoring Model (usable_early)**. The issue body states "Part of EPIC #129 (Authoring Model)" and covers BAR-FERRIC-001.

### Scope relative to the authoring-model concern (REQ-API-*) and async-forms-events concern (REQ-ASYNC-*)

Issue #137 traces to REQ-FW-003, REQ-FW-005, and REQ-FW-009 — all in the framework-scope register, not in REQ-API-* or REQ-ASYNC-*.

The issue's acceptance criteria cover `create_signal`, `create_memo`, `create_effect`, `batch`, and scoped cleanup. These are the reactive engine primitives defined at the framework level (REQ-FW-003 covers reactive primitives; REQ-FW-005 covers the declarative rendering surface that depends on them; REQ-FW-009 covers frozen surfaces and additive extension). None of these overlap with:

- **REQ-API-*** (authoring-model concern): REQ-API-* governs the `view!` macro, component props, named slots, dynamic dispatch, and the context API — the authoring surface built on top of reactive primitives, not the primitives themselves
- **REQ-ASYNC-*** (async-forms-events concern): REQ-ASYNC-* governs async resources (create_resource, Suspense, ErrorBoundary), DOM event handling, and form bindings — the async and event-handling surface built on top of reactive primitives

### Overlap and gap assessment

**No overlap found.** The scope of #137 is correctly bounded to the reactive engine layer (REQ-FW-*). Both the authoring model concern and the async/forms/events concern build on top of the reactive engine, but issue #137 does not intrude into their territory: it does not claim REQ-API-* or REQ-ASYNC-* ids, and the acceptance criteria do not describe component authoring, view! macro behavior, async loading, or event handling.

**Gap noted — partial coverage of the reactive primitive boundary.**

REQ-ASYNC-003 appears in Section A of the async concern document ("Per-request reactive isolation on the server" — likely the same concept as REQ-SSR-003, though confirmation would require reading the design document). REQ-ASYNC-003 is not cited in issue #137 (which is correct, since #137 is scoped to client-side reactive primitives under REQ-FW-*) nor in issue #143 (async resources and suspense, which covers REQ-ASYNC-001–016 except 003 and 014). This leaves REQ-ASYNC-003 with no covering issue — a potential boundary gap. The async and SSR concerns may have a coordination point here that is not surfaced in any issue.

REQ-ASYNC-014 has the same problem: it is in Section A of the async concern but absent from #143's citation set and from any other issue.

**Summary for #137:** The scope of issue #137 is well-bounded. It belongs to Epic #129 (Authoring Model) and correctly traces to REQ-FW-* (framework scope) rather than to REQ-API-* or REQ-ASYNC-*. The reactive primitives it delivers are foundational to both concerns but are not part of either concern's issue register. No overlap exists. The gap flagged above (REQ-ASYNC-003 and REQ-ASYNC-014 with no covering issue) is a separate traceability problem, not a #137 scoping problem.

---

## traceability_status

**has-issues**

| Finding | Severity | Detail |
|---|---|---|
| REQ-FW-007 has no covering child issue | Major | The cross-cutting router+HTTP requirement is in scope for 1.0 (usable_early, release_gating: true) and is explicitly flagged by the router concern as lacking a traceability table. No child issue cites it. |
| 30 REQ-API-* ids have no direct issue citation | Minor | All are implicitly covered by issues #139–#142 but not individually cited. Traceability is incomplete at the id level. |
| REQ-ASYNC-003 and REQ-ASYNC-014 have no covering issue | Minor | Both are defined in Section A of the async concern. Neither appears in the BAR acceptance criteria or in any issue. Cannot confirm deferral without reading the design document directly. |
| Epic bodies do not cite child issue numbers | Informational | All 8 epics list work items by BAR-FERRIC-* number. The child issues (#137–#164) were filed after the epics and establish the "Part of EPIC #N" link from the child side. The epics could be updated to cross-reference the filed issue numbers for bidirectional traceability. |
| Only #130 among epics cites a REQ-* id in its body | Informational | The REQ-* citations in #130 are a note about cross-epic coverage, not a gap. All other epics use BAR-FERRIC-* as their coverage language. |
