# Concern Findings: Consolidated Release Bar and Release Plan

## concern_name

Consolidated release bar and release plan

---

## document_validated

- `design/ferric/release-bar.md` (branch `work/design-ferric-1_0`)
- `design/ferric/release-plan.md` (branch `work/design-ferric-1_0`)

---

## req_ids_found

REQ-* ids cited in BAR-FERRIC-* criteria (collected from the criteria body of all 29 BAR-FERRIC-* entries in release-bar.md):

**REQ-FW-*:** REQ-FW-001, REQ-FW-002, REQ-FW-004, REQ-FW-005, REQ-FW-006, REQ-FW-008, REQ-FW-009, REQ-FW-010, REQ-FW-011, REQ-FW-012, REQ-FW-013

**REQ-SSR-*:** REQ-SSR-001, REQ-SSR-002, REQ-SSR-003, REQ-SSR-004, REQ-SSR-005, REQ-SSR-006, REQ-SSR-007, REQ-SSR-008, REQ-SSR-009, REQ-SSR-010, REQ-SSR-011, REQ-SSR-012

**REQ-API-*:** REQ-API-001, REQ-API-002, REQ-API-003, REQ-API-004, REQ-API-006, REQ-API-012, REQ-API-015, REQ-API-023, REQ-API-024, REQ-API-025, REQ-API-026, REQ-API-027, REQ-API-028, REQ-API-030, REQ-API-031, REQ-API-032, REQ-API-033, REQ-API-034, REQ-API-035, REQ-API-037, REQ-API-038, REQ-API-041, REQ-API-045, REQ-API-047, REQ-API-049, REQ-API-050, REQ-API-051, REQ-API-052, REQ-API-060, REQ-API-061, REQ-API-063, REQ-API-066, REQ-API-068

**REQ-ASYNC-*:** REQ-ASYNC-001, REQ-ASYNC-002, REQ-ASYNC-004, REQ-ASYNC-005, REQ-ASYNC-006, REQ-ASYNC-007, REQ-ASYNC-008, REQ-ASYNC-009, REQ-ASYNC-010, REQ-ASYNC-011, REQ-ASYNC-012, REQ-ASYNC-013, REQ-ASYNC-015, REQ-ASYNC-016, REQ-ASYNC-020, REQ-ASYNC-021, REQ-ASYNC-022, REQ-ASYNC-023, REQ-ASYNC-024, REQ-ASYNC-040, REQ-ASYNC-041, REQ-ASYNC-042, REQ-ASYNC-043

**REQ-RT-*:** REQ-RT-001, REQ-RT-002, REQ-RT-003, REQ-RT-004, REQ-RT-005, REQ-RT-006, REQ-RT-007, REQ-RT-008

**REQ-HTTP-*:** REQ-HTTP-001, REQ-HTTP-002, REQ-HTTP-003, REQ-HTTP-004, REQ-HTTP-005, REQ-HTTP-006, REQ-HTTP-007, REQ-HTTP-008, REQ-HTTP-009, REQ-HTTP-010, REQ-HTTP-011, REQ-HTTP-012, REQ-HTTP-013

**REQ-DX-*:** REQ-DX-001, REQ-DX-002, REQ-DX-003, REQ-DX-004, REQ-DX-005, REQ-DX-006, REQ-DX-007, REQ-DX-008, REQ-DX-009, REQ-DX-010

**REQ-REL-*:** REQ-REL-001, REQ-REL-002, REQ-REL-003, REQ-REL-004, REQ-REL-005, REQ-REL-006, REQ-REL-007, REQ-REL-008, REQ-REL-009, REQ-REL-010, REQ-REL-011, REQ-REL-020, REQ-REL-021, REQ-REL-022, REQ-REL-023, REQ-REL-024, REQ-REL-025, REQ-REL-026, REQ-REL-027, REQ-REL-028, REQ-REL-029, REQ-REL-030, REQ-REL-031, REQ-REL-032, REQ-REL-033, REQ-REL-040, REQ-REL-041, REQ-REL-042, REQ-REL-043, REQ-REL-044, REQ-REL-045, REQ-REL-046, REQ-REL-047

**REQ-PERF-*:** REQ-PERF-001, REQ-PERF-002, REQ-PERF-003, REQ-PERF-004, REQ-PERF-005, REQ-PERF-006, REQ-PERF-007, REQ-PERF-008, REQ-PERF-009, REQ-PERF-010

Note for SUBTASK_validate-crossrefs: release-bar.md and release-plan.md are consolidation documents — they do not own any REQ-* register. The REQ-* ids above are cross-references to the eight spoke design documents; the owning validators for each namespace are listed in the design document register.

---

## status

needs-fix

---

## specific_issues

### Issue 1 — §4 coverage map missing three one_oh REQ-* ids

**type:** completeness  
**severity:** major

release-bar.md §4 Coverage Map is intended to list every `one_oh`-gating REQ-* id mapped to the BAR-FERRIC-* criterion that enforces it. Three one_oh REQ-* ids that are cited in BAR criteria are absent from the map:

- **REQ-DX-008** — cited in BAR-FERRIC-022 (README, troubleshooting entry, and CI doc sync), which is a one_oh criterion. The map has rows for REQ-DX-009 and REQ-DX-010 from the same criterion, but not REQ-DX-008.
- **REQ-REL-024** — cited in BAR-FERRIC-024 (Semver contract and mechanical enforcement), which is a one_oh criterion. The map has rows for REQ-REL-020 through REQ-REL-029 with gaps at REQ-REL-024 and REQ-REL-027.
- **REQ-REL-027** — cited in BAR-FERRIC-024, same situation as REQ-REL-024.

SUBTASK_validate-crossrefs checks that every one_oh REQ-* id in the coverage map exists in its owning document. These three ids are correctly cited in criteria but will be invisible to the crossrefs check because they are missing from the coverage map. The map needs three additional rows.

---

### Issue 2 — Release plan does not reference the filed GitHub issue numbers

**type:** cross-reference  
**severity:** major

release-plan.md describes eight epics under "board issue #1" and references "#5" (ferric-router scaffold) and "#6" (ferric-http scaffold). None of these numbers match the filed issues: the filed epics are #129–#136 and the child issues are #137–#164 (as stated in the parent subtree hub). Someone tracking delivery against the filed GitHub backlog cannot match release-plan.md epics to specific issue numbers without a separate mapping.

The plan was authored before the issues were filed, so this is an expected sequencing gap rather than an authoring error — but it leaves the plan and the issue backlog unlinked. A mapping table (or updated issue references in the plan) is needed for the plan to serve as a trackable delivery reference.

---

### Issue 3 — Epic Landscape table mislabels two epics' stage

**type:** coherence  
**severity:** minor

The Epic Landscape table in release-plan.md labels the Client-side Router and HTTP/JSON Client epics as `usable_early`. Each epic contains one one_oh work item:

- Client-side Router: "Active-route awareness" covers BAR-FERRIC-016, which is staged `one_oh` in release-bar.md.
- HTTP/JSON Client: "PATCH method, per-request timeout, and lean dependency footprint" covers BAR-FERRIC-018, which is staged `one_oh` in release-bar.md.

The individual work-item entries within each epic correctly tag these items as `(one_oh)`. However, a reader looking only at the Epic Landscape summary would conclude that both epics are fully usable_early, which understates the one_oh work they contain. The `Stage` column should indicate the mixed staging (e.g., `usable_early / one_oh`) or the table should add a note.

---

## gaps

### GAP-080

**id:** GAP-080  
**description:** Three one_oh REQ-* ids (REQ-DX-008, REQ-REL-024, REQ-REL-027) are cited in BAR-FERRIC-022 and BAR-FERRIC-024 but are missing from the §4 coverage map in release-bar.md. The map is the primary cross-reference input for SUBTASK_validate-crossrefs; the omissions leave these ids unverified.  
**severity:** major  
**action_required:** Add three rows to the §4 coverage map: `REQ-DX-008 → one_oh → BAR-FERRIC-022`, `REQ-REL-024 → one_oh → BAR-FERRIC-024`, `REQ-REL-027 → one_oh → BAR-FERRIC-024`.

---

### GAP-081

**id:** GAP-081  
**description:** release-plan.md references issue numbers (#1, #5, #6) that do not match the filed GitHub issues (#129–#136 for epics, #137–#164 for child issues). The plan is not usable as a direct tracking reference against the filed backlog without a mapping.  
**severity:** major  
**action_required:** Update release-plan.md to reference the filed epic issue numbers (#129–#136) in the Epic Landscape table and the fold section. For the fold items (#5 and #6), confirm the corresponding filed issues (if any) and add those numbers. At minimum, add a mapping table that links plan epics to filed issues.

---

### GAP-082

**id:** GAP-082  
**description:** The Epic Landscape table in release-plan.md labels the Client-side Router and HTTP/JSON Client epics as `usable_early`, but each contains a one_oh work item (Active-route awareness / BAR-016 and PATCH+timeout / BAR-018). The individual work items are correctly staged, but the summary table presents both epics as fully usable_early.  
**severity:** minor  
**action_required:** Update the `Stage` column for these two epics in the Epic Landscape table to reflect their mixed staging (e.g., `usable_early / one_oh`), or add a column or note that calls out which BAR criteria within the epic are one_oh.

---

## Checks passed (for the record)

The following checks from the validation brief passed without issues:

- **All 29 BAR-FERRIC-* criteria cite at least one REQ-* id.** Verified: every criterion has a non-empty References field. No BAR criterion is unanchored to requirements.

- **Staging principle is clearly defined.** release-bar.md §2 defines usable_early and one_oh in concrete, checkable terms. The 12 usable_early criteria cover the core client-side capability (signals, components, async resources, forms, routing, HTTP). The 17 one_oh criteria cover SSR/hydration (must-have), docs/DX, performance, release/distribution, and compatibility policy. The assignments are logically consistent with the stated principle.

- **Each BAR criterion is testable.** Every criterion has a verification method from the closed vocabulary (`automated_test`, `example_build`, `doc_inspection`, `benchmark_run`, `publishability`) and a statement phrased as a condition a stranger can check without reading author notes.

- **Epic delivery sequence is logical.** Authoring Model first (no dependencies); Async/Forms/Events, Client-side Router, and HTTP/JSON Client each depend on Authoring Model and are parallelizable; SSR and Hydration (must-have) depends on Authoring Model and Async/Forms/Events; Docs and DX and Performance and Benchmark can run in parallel after SSR lands; Release and Distribution closes last. The sequence is sensible and matches the staged dependencies.

- **Individual work items reference REQ-* and BAR-FERRIC-* ids.** Each work item in release-plan.md carries a "Traces to:" section with design document section, REQ-* ids, and BAR-FERRIC-* ids. The traceability chain from work item to requirement to bar criterion is present throughout.

- **Cross-document staging is consistent at the work-item level.** Every BAR-FERRIC-* criterion's stage in release-bar.md is correctly reproduced in the corresponding work item in release-plan.md. The three issues above are at the epic-summary and coverage-map level, not at the work-item level.

- **BAR-FERRIC-004 (must_have: true) is correctly identified as the gating criterion.** Both documents single it out — release-bar.md §2 and §3, release-plan.md SSR and Hydration epic heading and the Epic Landscape table footnote.
