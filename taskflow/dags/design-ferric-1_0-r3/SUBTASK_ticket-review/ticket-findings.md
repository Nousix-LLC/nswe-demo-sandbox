spoke: ticket-review
concern_ids: [5]

findings:
  - id: TR-001
    severity: non-blocking
    concern: 3
    location: "issues #161, #162, #164"
    statement: >
      Issues #161 (Publishing readiness), #162 (Semver contract and CI enforcement), and #164
      (Versioning and compatibility policy) use hyphenated range notation for their REQ-* trace
      IDs — "REQ-REL-001–REQ-REL-011", "REQ-REL-020–REQ-REL-029", "REQ-REL-040–REQ-REL-047" —
      rather than citing each ID individually. Every other feature issue and the corresponding
      BAR-FERRIC criteria (BAR-023, BAR-024, BAR-029) list IDs one by one. Range notation
      is readable but imprecise: it does not identify which IDs within the range are absent
      (REQ-REL-017, for example, falls outside any cited range and is not accounted for), and
      it makes it harder to verify that the work item covers exactly the IDs the BAR criterion
      references.
    recommendation: >
      Expand the range notations to individual IDs matching the BAR-023, BAR-024, and BAR-029
      citation format. Issue #163 (Changelog) already cites REQ-REL-030, REQ-REL-031,
      REQ-REL-032, REQ-REL-033 individually and provides the correct model for its siblings.

  - id: TR-002
    severity: non-blocking
    concern: 4
    location: "issue #149; epic issue #132"
    statement: >
      Issue #149 (PATCH method, per-request timeout, and lean dependency footprint) declares a
      dependency on issue #159 (Bundle size and dependency footprint), which belongs to the
      Performance and Benchmark epic (#135). This cross-epic dependency is correctly documented
      in release-plan.md and is coherent — #149's acceptance criterion that "the HTTP client's
      dependency footprint is reflected in the performance benchmark numbers" can only be verified
      after #159 has produced those numbers. However, the dependency is not visible from epic
      issue #132 itself: that issue lists "Depends on: Authoring Model (#129)" with no mention of
      the Performance epic. A developer reviewing #132's work item list would not see that its
      one_oh item (#149) is gated on a cross-epic dependency outside #132's own chain.
    recommendation: >
      Add a note to epic issue #132 stating that its one_oh work item (BAR-018, issue #149)
      depends on issue #159 (Performance and Benchmark epic), so the cross-epic ordering
      constraint is visible at the epic level and not only in the individual work item.

summary:
  blocking_count: 0
  non_blocking_count: 2
  notes: >
    All 36 issues read (#129–#164: 8 epics, 28 feature issues). Epic–feature alignment is
    correct across all 28 feature issues; each appears under the right epic and the work item
    count matches the release-plan. All 29 BAR-FERRIC-* criteria have a corresponding feature
    issue. Wave plan independence of usable_early epics (#129–#132) from SSR (#133) is confirmed
    at the epic level; the one_oh item in #132 (#149) has a documented cross-epic dependency on
    #159, which is handled correctly by its stage label. No invented REQ-* IDs found: contested
    IDs REQ-ASYNC-003, REQ-ASYNC-014 (in issue #143), and REQ-FW-007 (in issue #146) are all
    confirmed real requirements in their respective design documents and correctly scoped to those
    issues. All feature issues carry testable acceptance criteria; no issue lacks criteria
    sufficient to verify the work. No BLOCKING findings.
