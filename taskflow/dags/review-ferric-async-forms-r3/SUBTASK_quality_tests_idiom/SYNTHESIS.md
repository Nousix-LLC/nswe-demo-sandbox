# SYNTHESIS — SUBTASK_qti_synthesis

## Verdict
gate: PASS
round: 1

## Checks

| Check | Result | Mechanical evidence | Notes |
|---|---|---|---|
| contract | pass | Schema read of four partial_findings.md against contracts/findings_format.md: both required sections present in all four spokes; severity values from allowed set (blocker/non-blocker/clean) in all four; concern labels match spoke assignments in all four; all location fields are repository-relative or "structural" | One Concern 2 finding excluded from findings.md (see advisory below); contract schema itself is satisfied |
| wiring | pass | Coverage checked by reading each spoke's "What was examined" sub-question checklist against the parent brief's concern sections: C2 Q1–Q4 all marked [x] with evidence; C3 Q1–Q4 all marked [x] with evidence; C6 Q1–Q4 (closure.forget/private-field/unsafe/unwrap) all marked [x] with evidence; C7 Q1–Q3 all marked [x] with evidence | No sub-question found unaddressed; all 15 concern-section sub-questions have at least one entry (blocker, non-blocker, or clean) in the combined output |
| duplication | pass | All four partial_findings.md read and compared by location and issue: no finding appears at the same repository-relative location with the same stated issue in more than one spoke; overlapping subject matter (generation counter, on_input_event_handler, prelude gaps) is examined from distinct angles producing non-overlapping findings; one advisory exclusion noted below | Advisory: Concern 2 finding at dom.rs static_event_kinds addresses the same surface as issue #198 ("static_event_kinds sync"); excluded from findings.md per inherited constraint; recorded here, not silently dropped |
| code-review | pass | Combined output read holistically: single blocker (C3, REQ-ASYNC-016 test gap) is correctly calibrated — a stated requirement has no test that would fail if the guard were removed; all non-blockers are proportionate (documentation gaps, missing convenience API, missing advisory tests, forward-proofing attributes); no style preference elevated to blocker; all clean entries state what was examined and why it is sound; combined findings tell a consistent story; each entry is actionable with a stated satisfying condition | No severity inflation or deflation detected; combined document is coherent and self-consistent |

## Findings

### Advisory — Concern 2 finding excluded from findings.md

- [ADV-1] excluded from findings.md
  - check=contract/duplication
  - location=`crates/ferric/src/dom.rs` (static_event_kinds function)
  - reason: This finding proposes adding a test to guard `static_event_kinds()` array/enum sync. Issue #198 is titled "static_event_kinds sync" and tracks the same gap. Per the inherited constraint "Issues #196–#201 MUST NOT appear in findings.md," this entry is excluded. It is recorded here rather than silently dropped. The Concern 2 spoke was not aware of #198 when it authored this finding. The array is noted as currently correct (47 matches the non-Custom variant count); the finding is a forward-proofing request, not a correctness gap.

## Coverage assertion

- ownership coverage: every declared artifact has exactly one producer — four spokes each produced their own partial_findings.md; SUBTASK_qti_synthesis produced findings.md and SYNTHESIS.md; no ownership violations detected ✓
- wiring: every sub-question registered in the parent brief's four concern sections has at least one addressed entry in the combined output ✓
- identities: every contract identity from contracts/_MANIFEST.yaml evaluated:
  - "Every partial_findings.md must contain ## Findings and ## What was examined sections" — PASS: all four spokes ✓
  - "severity values must be one of: blocker, non-blocker, clean" — PASS: all four spokes ✓
  - "concern value in each spoke must match its assigned concern label" — PASS: all four spokes ✓
  - "All paths in location fields are repository-relative" — PASS: all four spokes ✓
  - "No finding duplicates issues #196-#201" — PASS: one Concern 2 finding excluded per this constraint (ADV-1); no other overlaps detected ✓
  - "Combined output addresses every sub-question in the parent brief's four concern sections" — PASS ✓
- review: combined output reviewed holistically; no block-severity finding from code-review synthesis; severity calibration consistent; no open block-severity concern ✓
