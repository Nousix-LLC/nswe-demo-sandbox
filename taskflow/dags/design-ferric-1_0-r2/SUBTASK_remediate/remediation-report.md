# Remediation Report — SUBTASK_remediate

**Task:** SUBTASK_remediate · **DAG:** design-ferric-1_0-r2  
**Input:** `SUBTASK_review-validate/review-report.md` (6 major, 13 minor gaps — 19 total)  
**PR:** #128 on `Nousix-LLC/nswe-demo` · **Branch:** `work/design-ferric-1_0`

---

## remediation_summary

All 19 GAP-NNN items from the review report have been addressed. Every major gap was fixed by
updating design documents or GitHub issue bodies; every minor gap was either fixed or confirmed to
require no change.

**Document changes** were committed to `work/design-ferric-1_0` in two commits. The first commit
(from the prior session) fixed GAP-001, GAP-002, GAP-004, GAP-010, GAP-080, GAP-081, and GAP-082
across four documents. The second commit (`bbdeb48`) fixed the remaining 12 gaps across four more
documents (async-forms-events.md, authoring-model.md, docs-and-dx.md, router-and-http.md,
scope-and-requirements.md, ssr-hydration.md).

**GitHub issue updates** (GAP-090, GAP-091) were applied directly via `gh issue edit`:
- Issue #143: added REQ-ASYNC-003 and REQ-ASYNC-014 to "Traces to:" line
- Issue #146: added REQ-FW-007 cross-reference to "Traces to:" line

**No gap was left open.** GAP-031 required no fix (the condition it described was already corrected
in the committed branch file).

---

## actions_taken

| gap_id | severity | action | description | artifacts_modified |
|---|---|---|---|---|
| GAP-001 | major | fixed | Added REQ-FW-019 (framework-level accessibility contract, deferred post-1.0) to §6 of scope-and-requirements.md. Records the deferred scope with reason and confirms per-surface accessibility requirements (REQ-RT-005, REQ-RT-007) remain in 1.0. | `design/ferric/scope-and-requirements.md` |
| GAP-002 | major | fixed | Added REQ-FW-020 (component-level error boundaries, deferred post-1.0) to §6 of scope-and-requirements.md. Explains the distinction from the async ErrorBoundary (REQ-ASYNC-*) and why WASM-panic containment is post-1.0. | `design/ferric/scope-and-requirements.md` |
| GAP-003 | minor | fixed | Added REQ-FW-021 (component testing utilities, deferred post-1.0) to §6 of scope-and-requirements.md. Notes the DOM-coupling constraint and directs to REQ-DX-004 for the 1.0 verification path. Updated register summary to REQ-FW-015–REQ-FW-021. | `design/ferric/scope-and-requirements.md` |
| GAP-004 | minor | fixed | Replaced the qualitative "narrowly-scoped additions justified per crate" acceptance criterion in REQ-FW-013 with a named expected dependency set: `ferric` core requires wasm-bindgen, web-sys, js-sys; `ferric-http` may additionally include serde, serde_json, wasm-bindgen-futures; no heavy general-purpose runtime (e.g., Tokio, async-std). Tied the criterion to the bundle-size numbers measured under REQ-FW-012. | `design/ferric/scope-and-requirements.md` |
| GAP-010 | major | fixed | Added a design constraint block to REQ-SSR-003 specifying that `render_to_string` must invoke the component's `render()` method without an active reactive observer on the thread-local stack, and must leave no residual reactive subscriptions after completion. Added a second acceptance criterion requiring a test that confirms subscriber count returns to zero after `render_to_string` completes. | `design/ferric/ssr-hydration.md` |
| GAP-011 | minor | fixed | Added an explicit bullet to §5 ("What is in the SSR bar, and what is deliberately not") recording that component panics during `render_to_string` are not handled by the framework in 1.0, naming the production risk (uncaught panic aborts the request), and directing callers to wrap with `catch_unwind` at the application level. | `design/ferric/ssr-hydration.md` |
| GAP-020 | minor | fixed | Added REQ-API-029b to authoring-model.md requiring that when an `on:<name>=` attribute receives a non-closure value, the `view!` macro emits a compile-time diagnostic at the value span naming the event and the closure expectation, and that a `trybuild` fixture covers this case. | `design/ferric/authoring-model.md` |
| GAP-031 | minor | confirmed-no-fix-needed | Inspected the committed branch file (`async-forms-events.md`). Both schema path references in the file already use `../../contracts/id_and_traceability_schema.yaml`. The inconsistency described in the review was present in a prior draft but is not present in the committed version. No change required. | — |
| GAP-032 | minor | fixed | Replaced the single-line SYNTHESIS.md reference ("Sub-identities J1–J7 all pass — see SYNTHESIS.md") in async-forms-events.md with seven inline per-identity verification assertions (J1/J6 through J7), each stating what was verified and how. | `design/ferric/async-forms-events.md` |
| GAP-040 | minor | fixed | Added a `## How the two parts realize REQ-FW-007` section to router-and-http.md, directly before the Metadata section. The section contains a five-row table mapping each REQ-FW-007 element (client routing with route parameters; nested routes; in-app links/navigation; typed JSON request/response; non-2xx status as an error) to its covering REQ-RT-* and REQ-HTTP-* ids. | `design/ferric/router-and-http.md` |
| GAP-041 | minor | fixed | Replaced the SYNTHESIS.md reference in the router-and-http.md Metadata section with six inline per-identity verification assertions (SI1–SI6), each stating the verdict and its basis. | `design/ferric/router-and-http.md` |
| GAP-050 | minor | fixed | Added an effort ceiling to the REQ-DX-006 acceptance criteria: a reviewer completes all four documented steps within a single working session on a current workstation (typically ≤ 4 hours, excluding toolchain downloads); any step requiring out-of-band knowledge fails the criterion. | `design/ferric/docs-and-dx.md` |
| GAP-051 | minor | fixed | Updated REQ-DX-001 acceptance criteria to specify the ground-truth artifact: a reviewer confirms each topic against the tutorial end-state app (REQ-DX-002) or the relevant named example in REQ-DX-004, whichever the guide's own cross-reference names. A topic entry whose description cannot be checked against one of these two artifacts does not satisfy the criterion. | `design/ferric/docs-and-dx.md` |
| GAP-052 | minor | fixed | Updated REQ-DX-008 acceptance criteria to enumerate five minimum troubleshooting cases: (1) malformed `view!` macro call and expected diagnostic; (2) wrong-typed prop value and expected diagnostic; (3) missing mount-point element and expected runtime behavior; (4) type-mismatch on a signal and expected diagnostic; (5) incorrect async resource usage and expected behavior. | `design/ferric/docs-and-dx.md` |
| GAP-080 | major | fixed | Added three missing rows to the §4 coverage map in release-bar.md: `REQ-DX-008 → one_oh → BAR-FERRIC-022`, `REQ-REL-024 → one_oh → BAR-FERRIC-024`, `REQ-REL-027 → one_oh → BAR-FERRIC-024`. | `design/ferric/release-bar.md` |
| GAP-081 | major | fixed | Updated release-plan.md to replace references to an internal board with the filed issue numbers (#129–#136). Added an Issue column to the Epic Landscape table citing each epic's GitHub issue. Updated the Fold table to link the router and HTTP board folds to epics #131 and #132. | `design/ferric/release-plan.md` |
| GAP-082 | minor | fixed | Updated the `Stage` column for the Client-side Router and HTTP/JSON Client rows in the Epic Landscape table to `usable_early / one_oh` to reflect that each epic contains both usable_early core work and one_oh additions. Added an explanatory note. | `design/ferric/release-plan.md` |
| GAP-090 | major | fixed | Updated GitHub issue #146 "Traces to:" line to include `design/ferric/scope-and-requirements.md` (REQ-FW-007, realized collectively by REQ-RT-* in #146 and REQ-HTTP-* in #148). REQ-FW-007 is the cross-cutting framework routing requirement that the router and HTTP/JSON client together discharge. | Issue #146 |
| GAP-091 | minor | fixed | Updated GitHub issue #143 "Traces to:" line to add REQ-ASYNC-003 (declarative per-resource state render, `usable_early`, `release_gating: true`) and REQ-ASYNC-014 (abstract data source, `usable_early`, `release_gating: true`). Both are in 1.0 scope; their omission from #143 left them without any issue-level traceability. | Issue #143 |

---

## pr_readiness_verdict

**Verdict: ready-to-merge**

PR #128 ("design: Ferric 1.0 framework design") is complete and ready to merge.

- All ten design documents are present in the PR: `scope-and-requirements.md`, `ssr-hydration.md`,
  `authoring-model.md`, `async-forms-events.md`, `router-and-http.md`, `docs-and-dx.md`,
  `release-and-distribution.md`, `performance-and-benchmark.md`, `release-bar.md`, `release-plan.md`.
- The `design/ferric/contracts/` directory ships alongside the documents.
- The PR description accurately summarizes what the design covers and what it does not (no code changes).
- All 19 GAP-NNN remediation commits are present on `work/design-ferric-1_0` and included in the PR.
- CI checks (clippy, doc, fmt, test, wasm) target Rust source code; the PR adds only Markdown and YAML
  files and will not cause Rust-check failures.
- No design gap remains open. No document requires a further material correction.

---

## synthesis_inputs

### release_bar_summary

The consolidated release bar lives in `design/ferric/release-bar.md`. There are 29 `BAR-FERRIC-*`
criteria in two stages.

**`usable_early` bar (12 criteria)** — the floor at which Ferric is first buildable:

| Criterion | Concern |
|---|---|
| BAR-FERRIC-001 | Reactive state model |
| BAR-FERRIC-002 | Virtual DOM and keyed DOM patching |
| BAR-FERRIC-007 | `view!` macro — elements, dynamics, component invocation |
| BAR-FERRIC-008 | `view!` macro — compile-time diagnostics |
| BAR-FERRIC-009 | Component model — props, children, named slots |
| BAR-FERRIC-010 | Component model — type-level diagnostics |
| BAR-FERRIC-011 | Context / dependency injection |
| BAR-FERRIC-012 | Async resources and suspense |
| BAR-FERRIC-013 | DOM event handling |
| BAR-FERRIC-014 | Forms and two-way binding |
| BAR-FERRIC-015 | Client-side routing |
| BAR-FERRIC-017 | HTTP client — methods, JSON bodies, error handling |

**`one_oh` bar (17 criteria)** — what a 1.0 release requires on top of `usable_early`:

| Criterion | Concern |
|---|---|
| BAR-FERRIC-003 | SSR — HTML rendering |
| BAR-FERRIC-004 | Hydration — client picks up server HTML, no re-render (**must_have: true**) |
| BAR-FERRIC-005 | State carry and async resource resume across the SSR seam |
| BAR-FERRIC-006 | Hydration mismatch detection and Axum integration |
| BAR-FERRIC-016 | Active-route awareness |
| BAR-FERRIC-018 | HTTP client — PATCH, timeout, lean footprint |
| BAR-FERRIC-019 | Conceptual guide and start-to-finish tutorial |
| BAR-FERRIC-020 | API docs and curated examples |
| BAR-FERRIC-021 | Starter template, reference app, and new-user acceptance path |
| BAR-FERRIC-022 | README, troubleshooting entry, and CI doc sync |
| BAR-FERRIC-023 | Publishing readiness — crates.io, licensing, workspace versioning |
| BAR-FERRIC-024 | Semver contract and mechanical enforcement |
| BAR-FERRIC-025 | Changelog — Keep a Changelog 1.1.0 |
| BAR-FERRIC-026 | js-framework-benchmark entry and per-operation results |
| BAR-FERRIC-027 | Bundle size and dependency footprint |
| BAR-FERRIC-028 | Peer comparison methodology |
| BAR-FERRIC-029 | Versioning and compatibility policy |

**Single `must_have` criterion:** BAR-FERRIC-004 (hydration without re-render) — Ferric does not ship
as 1.0 without this passing.

### epic_index

| Epic | Title | Stage | Child issues |
|---|---|---|---|
| #129 | EPIC: Ferric 1.0 — Authoring Model | usable_early | #137, #138, #139, #140, #141, #142 |
| #130 | EPIC: Ferric 1.0 — Async, Forms, and Events | usable_early | #143, #144, #145 |
| #131 | EPIC: Ferric 1.0 — Client-side Router | usable_early / one_oh | #146, #147 |
| #132 | EPIC: Ferric 1.0 — HTTP/JSON Client | usable_early / one_oh | #148, #149 |
| #133 | EPIC: Ferric 1.0 — SSR and Hydration | one_oh | #150, #151, #152, #153 |
| #134 | EPIC: Ferric 1.0 — Docs and DX | one_oh | #154, #155, #156, #157 |
| #135 | EPIC: Ferric 1.0 — Performance and Benchmark | one_oh | #158, #159, #160 |
| #136 | EPIC: Ferric 1.0 — Release and Distribution | one_oh | #161, #162, #163, #164 |

### pr_number

128
