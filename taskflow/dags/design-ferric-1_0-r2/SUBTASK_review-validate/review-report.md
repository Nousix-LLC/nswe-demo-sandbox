# review-report.md

**Produced by**: SUBTASK_synthesis (SUBTASK_review-validate)  
**Conforms to**: `../contracts/_MANIFEST.yaml` §review_report_schema  
**Date**: 2026-11-02

---

## validation_summary

The Ferric 1.0 design on branch `work/design-ferric-1_0` is **mostly-complete with gaps**. Of the nine validated concern areas, three are fully valid (Async resources/forms/events, Release & distribution, Performance & benchmark) and six carry issues that require remediation. Across all ten findings files, five of the nineteen gaps are major: two silent omissions in the framework scope document (accessibility and component error handling with no requirements and no recorded deferrals), one underspecified isolation contract in the SSR document, and two problems in the plan documents (three one_oh REQ-* ids missing from the release-bar coverage map, and release-plan.md issue references that do not match the filed GitHub backlog). A sixth major gap surfaces from the cross-reference check: the cross-cutting REQ-FW-007 requirement has no direct citation in any GitHub issue's "Traces to:" line, leaving router and HTTP delivery without an explicit traceability link to the framework-level requirement. The REQ register itself is clean — no duplicate ids, no orphaned cross-references, and every BAR-FERRIC-* criterion cites at least one REQ-* id from the 193-id inventory. All 28 child issues (#137–#164) carry at least one REQ-* citation. None of the gaps involve requirements that were designed, reviewed, and deliberately deferred; they are omissions or editorial defects the design can absorb without restructuring. SUBTASK_remediate should be able to close all major gaps with targeted additions to five documents, plus two GitHub issue updates.

---

## per_concern_findings

### Concern 1 — Framework Scope & 1.0 Requirements

**Document**: `design/ferric/scope-and-requirements.md`  
**Status**: needs-fix  
**REQ ids found**: REQ-FW-001 through REQ-FW-018 (18 ids; REQ-FW-001–014 are 1.0 gating; REQ-FW-015–018 are post-1.0 deferrals)

**Issues found**:

1. **type**: completeness | **severity**: major  
   No framework-level accessibility requirement appears in REQ-FW-* or in the post-1.0 deferral list. ARIA attribute passthrough on `view!`-macro elements, accessibility-tree integrity under keyed-diff rendering and hydration, and focus management as a framework concern are all unaddressed. The out-of-1.0 list does not mention accessibility, making this a silent omission rather than a deliberate deferral.

2. **type**: completeness | **severity**: major  
   Component-level error handling is not addressed. The document does not say what Ferric does when an error occurs during component rendering — a WASM panic currently aborts the thread, crashing the whole app. This concern appears nowhere in the requirements or the out-of-1.0 deferrals.

3. **type**: testability | **severity**: minor  
   REQ-FW-013 acceptance criterion uses "narrowly-scoped additions justified per crate" without a measurable reference. A reviewer cannot make a reproducible pass/fail determination against this language.

**Gaps**: GAP-001 (major), GAP-002 (major), GAP-003 (minor), GAP-004 (minor)

---

### Concern 2 — Server-Side Rendering & Hydration

**Document**: `design/ferric/ssr-hydration.md`  
**Status**: needs-fix  
**REQ ids found**: REQ-SSR-001 through REQ-SSR-012 (12 ids; all one_oh, all release_gating: true; REQ-SSR-004 is the must-have gating criterion)

**Issues found**:

1. **type**: completeness | **severity**: major  
   The reactive context contract for `render_to_string` is not specified. The document requires per-request reactive isolation (REQ-SSR-003) and states that server render "performs no effects," but does not name "bypass the reactive observer stack" as a design constraint on the API. An implementer who wraps the server render in `create_effect` — as `dom::mount` does — would silently leak subscriptions across requests under concurrent load and violate REQ-SSR-003. The acceptance criterion for REQ-SSR-003 tests the observable output but cannot be satisfied without the API contract being stated.

2. **type**: completeness | **severity**: minor  
   No error-handling bar for component panics during server-side rendering. The document draws a recovery bar for client-side mismatch (§3, REQ-SSR-009) but not for a component panic during `render_to_string`. An Axum handler calling `render_to_string` in production has no specified fallback behaviour.

**Gaps**: GAP-010 (major), GAP-011 (minor)

---

### Concern 3 — Authoring Model

**Document**: `design/ferric/authoring-model.md`  
**Status**: needs-fix  
**REQ ids found**: REQ-API-001 through REQ-API-070 (63 assigned across three bands; REQ-API-053–059 and REQ-API-071–079 are reserved headroom)

**Issues found**:

1. **type**: completeness | **severity**: minor  
   The §2.6 diagnostics table commits to a "Handler value is not a closure" diagnostic at the author's span, but no specific REQ-API-* id covers this case. REQ-API-025 is scoped to wrong-typed attribute or text values; REQ-API-028 is the umbrella trybuild bar but does not state the specific message. The handler-closure type check falls between requirements.

**Gaps**: GAP-020 (minor)

---

### Concern 4 — Async Resources, Events, and Forms

**Document**: `design/ferric/async-forms-events.md`  
**Status**: valid  
**REQ ids found**: REQ-ASYNC-001 through REQ-ASYNC-043 (25 assigned across three sections; unused headroom explicitly marked)

All six validation criteria pass. The 25 requirements cover async resource primitives, suspense boundaries, two-way form binding, full DOM event coverage, and SSR handoff. Every requirement carries acceptance criteria with a named verification method.

**Issues found**: none

**Gaps**: GAP-031 (minor — inconsistent schema path reference within the document), GAP-032 (minor — J1–J7 sub-contract identity assertions condensed without individual auditability evidence)

---

### Concern 5 — Router + HTTP/JSON Client

**Document**: `design/ferric/router-and-http.md`  
**Status**: needs-fix  
**REQ ids found**: REQ-RT-001 through REQ-RT-009 (Part 1, 9 ids) and REQ-HTTP-001 through REQ-HTTP-013 (Part 2, 13 ids)

All eight validation criteria pass — route parameters, nested routes, active-link state, typed JSON, per-request timeouts, additive-surface guarantee, and register prefix correctness. Two editorial issues require remediation.

**Issues found**:

1. **type**: completeness | **severity**: minor  
   The explicit REQ-FW-007 traceability table present in the prior-art draft (`## How the two parts realize REQ-FW-007`) is absent from the branch version. The branch describes coverage in narrative form only; there is no consolidated map showing that the combined registers fully discharge REQ-FW-007.

2. **type**: coherence | **severity**: minor  
   The Metadata section references `SYNTHESIS.md` ("Identities asserted (SI1–SI6): all PASS — see `SYNTHESIS.md` at this workspace for verdicts"). `SYNTHESIS.md` is an internal taskflow artifact; readers outside the taskflow workspace cannot follow this reference.

**Gaps**: GAP-040 (minor), GAP-041 (minor)

---

### Concern 6 — Documentation & Developer Experience

**Document**: `design/ferric/docs-and-dx.md`  
**Status**: needs-fix  
**REQ ids found**: REQ-DX-001 through REQ-DX-010 (10 ids; all release_gating: true)

The document is well-structured and its register is complete. The three gaps are all minor testability refinements; none blocks the design's validity. No accuracy or coherence issues were found.

**Issues found**:

1. **type**: testability | **severity**: minor  
   REQ-DX-001 acceptance criterion references "a stated example" without naming which artifact to run to verify behavioral accuracy.

2. **type**: testability | **severity**: minor  
   REQ-DX-006 acceptance bar ("reaches a running app at each stage") has no effort ceiling, so a painful path through undocumented toolchain steps still passes.

3. **type**: testability | **severity**: minor  
   REQ-DX-008 defers the minimum case list for the troubleshooting section to the build team. A reviewer checking completeness against the design has no reference list.

**Gaps**: GAP-050 (minor), GAP-051 (minor), GAP-052 (minor)

---

### Concern 7 — Release & Distribution

**Document**: `design/ferric/release-and-distribution.md`  
**Status**: valid  
**REQ ids found**: REQ-REL-001–011 (§1), REQ-REL-020–033 (§2), REQ-REL-040–047 (§3) — 33 ids total

All validation criteria pass. The branch document fully reconciles the prior-art (all 33 REQ-REL-* ids present with unchanged acceptance criteria). Semver policy, changelog format, multi-crate workspace versioning, crates.io metadata fields, and testability are all addressed. Every requirement carries a named verification method.

**Issues found**: none  
**Gaps**: none

---

### Concern 8 — Performance & Benchmark

**Document**: `design/ferric/performance-and-benchmark.md`  
**Status**: valid  
**REQ ids found**: REQ-PERF-001 through REQ-PERF-010 (10 ids)

All five validation criteria pass. The js-framework-benchmark entry is required as a 1.0 gate with stated methodology. Peer comparisons are grounded and hedged appropriately (no measured data asserted). Bundle-size and dependency-footprint requirements have a measurable bar. Benchmark methodology is reproducible. The document's hedging is exemplary — every target is explicitly labeled as an expectation, not a measured result.

**Issues found**: none  
**Gaps**: none

---

### Concern 9 — Consolidated Release Bar and Release Plan

**Documents**: `design/ferric/release-bar.md`, `design/ferric/release-plan.md`  
**Status**: needs-fix  
**REQ ids found**: Cross-references to all eight spoke registers (193 ids); release-bar.md and release-plan.md are consolidation documents and do not own any REQ-* register

The 29 BAR-FERRIC-* criteria all cite at least one REQ-* id, the staging principle is clearly defined, every criterion is testable, the epic delivery sequence is logical, and work items trace to REQ-* and BAR-FERRIC-* ids. Three issues require remediation.

**Issues found**:

1. **type**: completeness | **severity**: major  
   The §4 Coverage Map in release-bar.md is missing three one_oh REQ-* ids (REQ-DX-008, REQ-REL-024, REQ-REL-027) that are cited in BAR-FERRIC-022 and BAR-FERRIC-024 but absent from the map. The coverage map is the primary cross-reference input for cross-reference checking; the omissions leave these ids unverified.

2. **type**: cross-reference | **severity**: major  
   release-plan.md references issue numbers (#1, #5, #6) that do not match the filed GitHub issues (#129–#136 for epics, #137–#164 for child issues). The plan cannot be used as a direct tracking reference against the filed backlog without a mapping.

3. **type**: coherence | **severity**: minor  
   The Epic Landscape table labels the Client-side Router and HTTP/JSON Client epics as `usable_early`, but each contains a one_oh work item (Active-route awareness → BAR-FERRIC-016; PATCH+timeout+footprint → BAR-FERRIC-018). The individual work items are correctly staged but the epic summary table understates the one_oh content.

**Gaps**: GAP-080 (major), GAP-081 (major), GAP-082 (minor)

---

## req_register_reconciliation

*Drawn from `SUBTASK_validate-crossrefs/crossrefs-findings.md` §req_register_reconciliation.*

### duplicate_ids

None. Each of the nine REQ-* prefixes is owned exclusively by one source document. The 193 assigned REQ-* ids span 9 prefixes with no overlap.

| Prefix | Owner document | Count |
|---|---|---|
| REQ-FW-* | scope-and-requirements.md | 18 |
| REQ-SSR-* | ssr-hydration.md | 12 |
| REQ-API-* | authoring-model.md | 63 |
| REQ-ASYNC-* | async-forms-events.md | 25 |
| REQ-RT-* | router-and-http.md (Part 1) | 9 |
| REQ-HTTP-* | router-and-http.md (Part 2) | 13 |
| REQ-DX-* | docs-and-dx.md | 10 |
| REQ-REL-* | release-and-distribution.md | 33 |
| REQ-PERF-* | performance-and-benchmark.md | 10 |

### orphaned_references

None. Spot-checks across all cross-reference citations in ssr-hydration.md, authoring-model.md, async-forms-events.md, and router-and-http.md found no citations pointing to undefined ids. Range notations (e.g., "REQ-API-071–079 reserved headroom") are namespace declarations, not citations.

### BAR-FERRIC-* without REQ-* citations

None. All 29 BAR-FERRIC-* criteria cite REQ-* ids present in the full 193-id inventory. Spot-checked across all nine prefix groups.

**Note**: GAP-080 (from SUBTASK_validate-plan) identifies three ids (REQ-DX-008, REQ-REL-024, REQ-REL-027) missing from the §4 coverage map in release-bar.md. This is a coverage-map completeness issue in that document, not an inventory gap — all three ids exist in their owning documents' registers. The BAR check above passes; the coverage-map defect is tracked as GAP-080.

**Status: clean**

---

## issue_traceability

*Drawn from `SUBTASK_validate-crossrefs/crossrefs-findings.md` §issue_traceability.*

### Per-epic summary

| Epic | Title | Children | All children with REQ-* citation |
|---|---|---|---|
| #129 | Ferric 1.0 — Authoring Model (usable_early) | #137, #138, #139, #140, #141, #142 | Yes — all 6 |
| #130 | Ferric 1.0 — Async, Forms, and Events (usable_early) | #143, #144, #145 | Yes — all 3 |
| #131 | Ferric 1.0 — Client-side Router (usable_early) | #146, #147 | Yes — both |
| #132 | Ferric 1.0 — HTTP/JSON Client (usable_early) | #148, #149 | Yes — both |
| #133 | Ferric 1.0 — SSR and Hydration (one_oh, must-have) | #150, #151, #152, #153 | Yes — all 4 |
| #134 | Ferric 1.0 — Docs and DX (one_oh) | #154, #155, #156, #157 | Yes — all 4 |
| #135 | Ferric 1.0 — Performance and Benchmark (one_oh) | #158, #159, #160 | Yes — all 3 |
| #136 | Ferric 1.0 — Release and Distribution (one_oh) | #161, #162, #163, #164 | Yes — all 4 |

All 28 child issues (#137–#164) contain at least one REQ-* citation in their "Traces to:" line.

### Issues without REQ-* citation

None at the child-issue level. All 28 child issues carry at least one REQ-* citation.

### Requirements without a covering issue

**Tier 1 — In-scope requirement with no direct issue citation (major):**

REQ-FW-007 (cross-cutting "provides both client-side router and HTTP/JSON client" framework requirement; `usable_early`, `release_gating: true`) has no child issue citing it in a "Traces to:" line. Issues #146–#149 collectively deliver this requirement but each cites only REQ-RT-* or REQ-HTTP-* ids. No way exists to verify from the issue board, without cross-issue reasoning, that REQ-FW-007 is covered.

**Tier 2 — Incomplete citation (implicitly covered, not directly cited; minor):**

30 REQ-API-* ids have no direct issue citation (Band A: 16 ids, parent #139; Band B: 8 ids, parents #140–#141; Band C: 6 ids, parent #142). These are implicitly covered by the broad acceptance criteria of #139–#142 and gated via BAR-FERRIC-* representative subsets. This is traceability incompleteness at the id level, not an untracked delivery gap.

REQ-ASYNC-003 and REQ-ASYNC-014 have no covering issue and are not marked as deferred or reserved in the async concern findings (unlike REQ-ASYNC-017–019 and REQ-ASYNC-025–039, which are explicitly unused headroom). Issue #143 covers Section A but omits these two ids.

### Issue #137 special check

Issue #137 ("Reactive state primitives") belongs to Epic #129 — Authoring Model (usable_early). Its acceptance criteria cover `create_signal`, `create_memo`, `create_effect`, `batch`, and scoped cleanup, tracing to REQ-FW-003, REQ-FW-005, and REQ-FW-009. Scope is correctly bounded: #137 does not claim ids from REQ-API-* or REQ-ASYNC-* and its acceptance criteria do not describe component authoring, view! macro behavior, async resource loading, or event handling. No scope overlap exists with concern 3 (authoring model) or concern 4 (async/forms/events).

A boundary gap exists independently of #137: REQ-ASYNC-003 and REQ-ASYNC-014 have no covering issue. This is not a #137 scoping problem; it is a traceability question for issue #143.

**Status: has-issues**

| Finding | Severity |
|---|---|
| REQ-FW-007 has no covering child issue | Major |
| 30 REQ-API-* ids have no direct issue citation | Minor |
| REQ-ASYNC-003 and REQ-ASYNC-014 have no covering issue | Minor |
| Epic bodies use BAR-FERRIC-* as coverage language; child issues establish parent link unidirectionally | Informational |
| Only epic #130 cites REQ-* ids in its body (a cross-epic coverage note, not a gap) | Informational |

---

## gaps_for_remediation

All 19 GAP-NNN items from all ten findings files, consolidated and prioritized by severity.

### Major gaps (6 items)

| id | description | severity | action_required |
|---|---|---|---|
| GAP-001 | Accessibility requirements absent from framework scope. The document does not address ARIA attribute support on `view!`-macro elements, accessibility-tree integrity under keyed-diff rendering and hydration, or focus management as a framework-level concern. Not listed in the out-of-1.0 deferrals — a silent omission, not a deliberate deferral. | major | Add a cross-cutting framework-level accessibility statement to scope-and-requirements.md: either a REQ-FW-* requirement or an explicit post-1.0 deferral in §6. The statement must address (a) whether ARIA attributes on `view!`-macro elements are preserved to the real DOM, (b) whether the keyed diff and hydration pass maintain accessibility-tree integrity, and (c) whether focus management is in scope for 1.0 or deferred. |
| GAP-002 | Component error handling / error boundaries not addressed or explicitly deferred. WASM panics abort the thread; without an error-boundary mechanism one component error crashes the whole app. Not in requirements and not in the post-1.0 deferrals. | major | Add either (a) a cross-cutting REQ-FW-* requirement for component-level error containment, or (b) an explicit post-1.0 deferral entry in §6 of scope-and-requirements.md acknowledging that WASM-thread panics are not yet bounded and stating the intended post-1.0 direction. |
| GAP-010 | Reactive context contract for `render_to_string` not specified. The design requires per-request isolation (REQ-SSR-003) but does not name "bypass the reactive observer stack" as a design constraint on the API. An implementer following `mount`'s pattern of wrapping in `create_effect` would silently leak subscriptions across requests. | major | Add a named design constraint to REQ-SSR-001 and §2.1 of ssr-hydration.md stating that `render_to_string` MUST call `component.render()` without an active reactive observer on the thread-local stack — outside of any `create_effect` — so signal reads during server render do not register subscriptions. This is the mechanism that satisfies REQ-SSR-003 and must appear in the acceptance criteria or as a named isolation contract in §2.1. |
| GAP-080 | Three one_oh REQ-* ids (REQ-DX-008, REQ-REL-024, REQ-REL-027) cited in BAR-FERRIC-022 and BAR-FERRIC-024 are missing from the §4 coverage map in release-bar.md. The map is the primary cross-reference input for cross-reference validation; these omissions leave the three ids unverified. | major | Add three rows to the §4 coverage map in release-bar.md: `REQ-DX-008 → one_oh → BAR-FERRIC-022`, `REQ-REL-024 → one_oh → BAR-FERRIC-024`, `REQ-REL-027 → one_oh → BAR-FERRIC-024`. |
| GAP-081 | release-plan.md references issue numbers (#1, #5, #6) that do not match the filed GitHub issues (#129–#136 for epics, #137–#164 for child issues). The plan is not usable as a direct tracking reference against the filed backlog without a mapping. | major | Update release-plan.md to reference the filed epic issue numbers (#129–#136) in the Epic Landscape table and the fold section. For the folded items (#5 and #6), confirm the corresponding filed issues and add those numbers. At minimum, add a mapping table linking plan epics to filed issues. |
| GAP-090 | REQ-FW-007 (cross-cutting "provides both client-side router and HTTP/JSON client" framework requirement; `usable_early`; `release_gating: true`) has no direct citation in any GitHub issue's "Traces to:" line. Issues #146–#149 collectively deliver it but each cites only REQ-RT-* or REQ-HTTP-* ids. Traceability from the issue board to this requirement is broken. | major | Add REQ-FW-007 to the "Traces to:" line of issue #146 or #148 (or both), or add a cross-reference note to Epics #131 and #132 explaining how REQ-FW-007 is collectively satisfied. Consider also adding the REQ-FW-007 coherence coverage map to router-and-http.md as noted in GAP-040. |

---

### Minor gaps (13 items)

| id | description | severity | action_required |
|---|---|---|---|
| GAP-003 | Testing utilities not mentioned or explicitly deferred in scope-and-requirements.md. Its absence from §6 is a silent omission. | minor | Add an entry to §6 explicitly deferring component testing utilities to post-1.0 (with a reason), or add a minimal cross-cutting requirement noting the framework's position on running rendering outside a browser context. |
| GAP-004 | REQ-FW-013 acceptance criterion "narrowly-scoped additions justified per crate" is not reproducibly testable. Pass/fail depends on reviewer judgment without a concrete reference. | minor | Replace the qualitative phrase with a named expected dependency set (e.g., list `ferric`'s required transitive dependencies) or a measurable threshold. Tie the criterion to the bundle-size numbers required by REQ-FW-012 so "lean" is falsifiable against a measured result. |
| GAP-011 | No error-handling bar for component panics during server-side rendering. The document draws a recovery bar for client-side mismatch but not for a component panic during `render_to_string`. An Axum handler calling `render_to_string` in production has no specified fallback behaviour. | minor | Add a requirement (or an explicit recorded deferral) for error handling during server render: either `render_to_string` returns `Result<String, ...>` and callers handle the error, or ssr-hydration.md explicitly defers panic handling and notes the production risk. |
| GAP-020 | The §2.6 diagnostics table in authoring-model.md includes "Handler value is not a closure" as a named expected diagnostic, but no REQ-API-* id specifies the required message text or requires a trybuild fixture for this case. | minor | Add a requirement (e.g., REQ-API-029b, or widen REQ-API-025) stating: when the value on an `on:<name>=` binding is not `Fn()`, the macro emits a diagnostic at the value span naming the event and stating the closure expectation; a trybuild fixture covers this case. |
| GAP-031 | Inconsistent schema path reference in async-forms-events.md. Inline requirements prose cites `contracts/id_and_traceability_schema.yaml` (no directory prefix, ambiguous); the metadata table cites `../../contracts/id_and_traceability_schema.yaml`. One path is wrong; the prior-art used the `../../contracts/` form consistently. | minor | Standardize the schema path reference to `../../contracts/id_and_traceability_schema.yaml` throughout async-forms-events.md so both references resolve to the same file. |
| GAP-032 | The prior-art's dedicated identity-verification section named and verified each sub-contract identity (J1–J7) individually. The branch version condenses this to one line citing SYNTHESIS.md, which a reviewer outside the taskflow workspace cannot access. | minor | Either restore the named per-identity assertions in the register summary (J1 through J7 each with a one-line verification statement), or confirm SYNTHESIS.md is available alongside the document and add a cross-reference note directing reviewers there. |
| GAP-040 | The REQ-FW-007 explicit coverage map table is absent from router-and-http.md. The prior-art draft included a dedicated section mapping each REQ-FW-007 element to its covering REQ-RT-* or REQ-HTTP-* id(s). The branch addresses this only in an Overview paragraph. | minor | Add a `## How the two parts realize REQ-FW-007` section to router-and-http.md, mapping each REQ-FW-007 element to its covering requirement(s). The prior-art table (lines 739–751) is the correct model. |
| GAP-041 | The Metadata section of router-and-http.md references `SYNTHESIS.md` as the source for identity verdicts. `SYNTHESIS.md` is the taskflow fold record, not a deliverable or companion file. Readers outside the taskflow workspace cannot follow this reference. | minor | Either remove the `SYNTHESIS.md` reference and record the identity verdicts inline in the Metadata section (matching the prior-art version's style), or reword to omit the external-artifact reference while preserving the provenance note. |
| GAP-050 | REQ-DX-006 acceptance bar ("completes the four documented steps and reaches a running app at each stage") has no effort ceiling. A painful path taking a full day of debugging still satisfies the criterion as written. | minor | Add an effort bound to the REQ-DX-006 acceptance criteria — for example: "a reviewer unfamiliar with Ferric completes all four steps within [N hours / one working session] on a current workstation following only the documented path, with no steps that require out-of-band knowledge." |
| GAP-051 | REQ-DX-001 acceptance criterion references "a stated example" for behavioral verification without naming which artifact to run. A reviewer checking independently has no anchor. | minor | Specify in REQ-DX-001 acceptance criteria which artifact supplies the behavioral ground truth — e.g., "a reviewer reads the guide's description of a named capability and confirms the behavior against the tutorial end-state app or against the relevant example in REQ-DX-004." |
| GAP-052 | REQ-DX-008 defers the minimum case list for the troubleshooting section to the build — "a stated set of common mistakes" means the section itself declares the set, not that the design has declared it. A reviewer checking completeness against the design has no reference list. | minor | Enumerate in REQ-DX-008 the minimum set of common mistakes the troubleshooting section must cover (e.g., malformed `view!` macro, misused prop type, missing mount-point element, type-mismatch on a signal, incorrect async resource usage). |
| GAP-082 | The Epic Landscape table in release-plan.md labels the Client-side Router and HTTP/JSON Client epics as `usable_early`, but each contains a one_oh work item (Active-route awareness → BAR-FERRIC-016; PATCH+timeout+footprint → BAR-FERRIC-018). The individual work items are correctly staged, but the summary table understates the one_oh content. | minor | Update the `Stage` column for these two epics in the Epic Landscape table to reflect mixed staging (e.g., `usable_early / one_oh`), or add a note calling out which BAR criteria within each epic are one_oh. |
| GAP-091 | REQ-ASYNC-003 and REQ-ASYNC-014, both defined in Section A of async-forms-events.md (assigned range REQ-ASYNC-001–016), are not cited by any GitHub issue and are not marked as deferred or reserved in the async concern findings. Issue #143 (async resources and suspense) covers Section A but omits both ids. Their 1.0 scope status is unconfirmed. | minor | Read REQ-ASYNC-003 and REQ-ASYNC-014 in async-forms-events.md on branch `work/design-ferric-1_0`, confirm whether they are in scope for Ferric 1.0, and either add them to issue #143's "Traces to:" line or document the deferral explicitly. |
