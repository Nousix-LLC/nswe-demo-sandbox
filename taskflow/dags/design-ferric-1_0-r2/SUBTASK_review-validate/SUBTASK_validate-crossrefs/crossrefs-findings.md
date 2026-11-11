# crossrefs-findings.md

**Produced by**: SUBTASK_validate-crossrefs (SUBTASK_synthesis-crossrefs)  
**Conforms to**: `../contracts/_MANIFEST.yaml` §crossrefs_findings_schema  
**Inputs**: `SUBTASK_req-reconciliation/req-reconciliation.md`, `SUBTASK_issue-traceability/issue-traceability.md`  
**Date**: 2026-11-02

---

## req_register_reconciliation

Cross-reference check across all nine concern documents, assembled from `SUBTASK_req-reconciliation/req-reconciliation.md`.

### duplicate_ids

None.

Each of the nine REQ-* prefixes is owned exclusively by one source document. No id appears in more than one document's `req_ids_found` list. The prefix-to-owner mapping:

| Prefix | Owner document |
|---|---|
| REQ-FW-* | scope-and-requirements.md (18 ids) |
| REQ-SSR-* | ssr-hydration.md (12 ids) |
| REQ-API-* | authoring-model.md (63 ids) |
| REQ-ASYNC-* | async-forms-events.md (25 ids) |
| REQ-RT-* | router-and-http.md Part 1 (9 ids) |
| REQ-HTTP-* | router-and-http.md Part 2 (13 ids) |
| REQ-DX-* | docs-and-dx.md (10 ids) |
| REQ-REL-* | release-and-distribution.md (33 ids) |
| REQ-PERF-* | performance-and-benchmark.md (10 ids) |

Total: 193 assigned REQ-* ids across 9 prefixes.

### orphaned_references

None.

Spot-checks against design documents on branch `work/design-ferric-1_0` found no cross-reference citations pointing to undefined ids. Range notations in several documents (e.g., "REQ-API-071–079 reserved headroom", "REQ-ASYNC-025..039 unused headroom") are namespace declarations, not citations of undefined ids — confirmed by reading the document bodies.

Spot-checks performed: ssr-hydration.md (refs to REQ-FW-003, 004, 008, 009, 014), authoring-model.md (refs to REQ-FW-005, 006, 009, 014), async-forms-events.md (refs to REQ-FW-006, 009, 013 and namespace refs to REQ-SSR-*, REQ-HTTP-*), router-and-http.md (refs to REQ-FW-007, 008, 009, 010, 013). All cited ids present in the owning documents' registers.

### bar_without_req

None.

All 29 BAR-FERRIC-* criteria cite REQ-* ids present in the full 193-id inventory. Spot-checked against each prefix group: REQ-FW-* (11 ids cited), REQ-SSR-* (all 12), REQ-API-* (28 ids from assigned bands), REQ-ASYNC-* (21 ids from assigned sections), REQ-RT-* (8 of 9), REQ-HTTP-* (all 13), REQ-DX-* (all 10), REQ-REL-* (all 33), REQ-PERF-* (all 10). No criterion references a reserved or undefined id.

Note: GAP-080 (from SUBTASK_validate-plan) identifies three ids (REQ-DX-008, REQ-REL-024, REQ-REL-027) missing from the §4 coverage map in release-bar.md. This is a coverage-map completeness issue in that document, not an inventory gap — all three ids exist in their owning documents' registers and the BAR check here passes.

**Status: clean**

---

## issue_traceability

Assembled from `SUBTASK_issue-traceability/issue-traceability.md`. GitHub issues checked: 8 epics (#129–#136) and 28 child issues (#137–#164).

### epics_summary

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

Epic bodies for #129, #131–#136 list work items by BAR-FERRIC-* number only; no REQ-* ids appear in those epic bodies. Epic #130 is the exception: its body cites REQ-ASYNC-012 and REQ-ASYNC-013 in a cross-coverage note (those requirements are tracked under #133, SSR and Hydration).

### issues_without_req

None. All 28 child issues (#137–#164) contain at least one REQ-* citation in their "Traces to:" line.

### requirements_without_issue

**Tier 1 — In-scope requirement, no direct issue citation:**

**REQ-FW-007** — the cross-cutting framework requirement that Ferric provides both a client-side router and an HTTP/JSON client — has no child issue citing it in a "Traces to:" line. It is classified `usable_early`, `release_gating: true` in the scope concern document. The four issues that together deliver this requirement (#146, #147, #148, #149) each cite REQ-RT-* or REQ-HTTP-* ids; none cites REQ-FW-007. The router concern document also flags the absence of a REQ-FW-007 coherence table in the branch design document.

Suggested action: add REQ-FW-007 to the "Traces to:" line of issue #146 or #148 (or both epics #131 and #132), or add a cross-reference note explaining how REQ-FW-007 is collectively satisfied by those issues.

**Tier 2 — Incomplete citation (implicitly covered, not directly cited):**

30 REQ-API-* ids have no direct issue citation:
- Band A (16 ids): REQ-API-005, 007, 008, 009, 010, 011, 013, 014, 016, 017, 018, 019, 020, 021, 022, 029 (parent issue: #139)
- Band B (8 ids): REQ-API-036, 039, 040, 042, 043, 044, 046, 048 (parent issues: #140, #141)
- Band C (6 ids): REQ-API-062, 064, 065, 067, 069, 070 (parent issue: #142)

The acceptance criteria of issues #139–#142 are broad enough to cover these ids implicitly. The BAR-FERRIC-* acceptance criteria gate on representative subsets rather than individual ids. This is traceability incompleteness at the id level, not an untracked delivery gap.

REQ-ASYNC-003 and REQ-ASYNC-014 appear in Section A of the async concern document (assigned range 001–016) but are not cited by any issue and are not marked as deferred in the concern findings. Issue #143 (async resources and suspense) covers Section A but omits these two ids. Deferral status cannot be confirmed without reading `design/ferric/async-forms-events.md` directly.

**Deferred — no issue warranted:**  
REQ-FW-015–018 (post-1.0 deferrals), REQ-RT-009 (post-1.0 deferral), REQ-REL-012–019/034–039/048+ (reserved headroom), REQ-ASYNC-017–019/025–039/044–059 (unused headroom per manifest).

### issue_137_check

Issue #137 ("Reactive state primitives") belongs to **Epic #129 — Ferric 1.0 — Authoring Model (usable_early)**. Its acceptance criteria cover `create_signal`, `create_memo`, `create_effect`, `batch`, and scoped cleanup, tracing to REQ-FW-003, REQ-FW-005, and REQ-FW-009.

**Scope is correctly bounded.** The reactive engine primitives that #137 delivers are the foundation both the authoring-model concern (REQ-API-*) and the async-forms-events concern (REQ-ASYNC-*) build on. But #137 does not claim ids from either register and its acceptance criteria do not describe component authoring, view! macro behavior, async resource loading, or event handling. No overlap exists between #137's scope and those two concerns.

**Boundary gap noted.** REQ-ASYNC-003 and REQ-ASYNC-014 (both Section A of the async concern, the range that issue #143 otherwise covers) have no covering issue. This is not a #137 scoping problem — those ids are not REQ-FW-* ids — but it is an open traceability question: they may represent a coordination point between the async and SSR concerns that no issue currently surfaces.

**Status: has-issues**

| Finding | Severity | Detail |
|---|---|---|
| REQ-FW-007 has no covering child issue | Major | Cross-cutting router+HTTP requirement; usable_early; release_gating: true; no "Traces to:" citation in any issue |
| 30 REQ-API-* ids have no direct issue citation | Minor | Implicitly covered by issues #139–#142; traceability incomplete at the id level |
| REQ-ASYNC-003 and REQ-ASYNC-014 have no covering issue | Minor | Section A ids; deferral status unconfirmed |
| Epic bodies do not cross-reference filed child issue numbers | Informational | All 8 epics use BAR-FERRIC-* as coverage language; child issues establish the parent link unidirectionally |
| Only epic #130 cites REQ-* ids in its body | Informational | Those citations are a cross-epic coverage note; no gap |

---

## gaps

Additional gaps found during cross-reference synthesis, not already captured in the nine concern-findings.md files. IDs assigned in range GAP-090 through GAP-099.

### GAP-090

**id**: GAP-090  
**description**: REQ-FW-007 (the cross-cutting "provides both client-side router and HTTP/JSON client" framework requirement) has no direct citation in any GitHub issue's "Traces to:" line. Issues #146–#149 collectively deliver this requirement but each cites only REQ-RT-* or REQ-HTTP-* ids. The result is a broken traceability link: there is no way to verify from the issue board, without cross-issue reasoning, that REQ-FW-007 is covered. The router concern (SUBTASK_validate-router) separately flagged the absence of a REQ-FW-007 coherence table in the design document; this gap is the corresponding issue-level traceability gap.  
**severity**: major  
**action_required**: Add REQ-FW-007 to the "Traces to:" line of issue #146 or #148 (or both), or add a cross-reference note to Epics #131 and #132 explaining how REQ-FW-007 is collectively satisfied. Consider also adding the coherence table to the design document as flagged by the router concern.

### GAP-091

**id**: GAP-091  
**description**: REQ-ASYNC-003 and REQ-ASYNC-014, both defined in Section A of the async-forms-events concern document (assigned range REQ-ASYNC-001–016), are not cited by any GitHub issue and are not marked as deferred or reserved by the async concern findings. Issue #143 (async resources and suspense), which covers Section A, omits both from its "Traces to:" line. The async concern does not flag these two ids as intentionally excluded headroom — unlike REQ-ASYNC-017–019 and REQ-ASYNC-025–039, which are explicitly marked "unused headroom." This leaves their 1.0 scope status unconfirmed.  
**severity**: minor  
**action_required**: Read REQ-ASYNC-003 and REQ-ASYNC-014 in `design/ferric/async-forms-events.md` on branch `work/design-ferric-1_0`, confirm whether they are in scope for Ferric 1.0, and either add them to issue #143's "Traces to:" line or document the deferral explicitly in the async concern findings.

---

**Contract identity assertions:**
- GAP-NNN ids in this file are all in range GAP-090–GAP-099: ✓ (GAP-090, GAP-091)
- No GAP id duplicates ids from the nine concern-findings.md files (range GAP-001–GAP-089): ✓
- All three required sections present (req_register_reconciliation, issue_traceability, gaps): ✓
