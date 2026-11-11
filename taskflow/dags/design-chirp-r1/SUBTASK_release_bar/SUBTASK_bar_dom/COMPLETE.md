# COMPLETE — SUBTASK_bar_dom

## What was done
Authored the domain-area release-bar fragment: the `BAR-100..199` criteria enforcing every
release-gating `REQ-DOM-*` from `design/domain-application-design.md`, plus a coverage note.

## Output produced
- `SUBTASK_bar_dom/outputs/bar-dom.md` — 60 `BAR-*` criteria (`BAR-100..120`, `BAR-130..148`,
  `BAR-160..179`), each with id, statement, references (≥1 `REQ-DOM-*`), a `verification_method`
  from the frozen vocabulary, and a `proposed_stage`; followed by a per-REQ coverage note.

## How it composes with the parent
- Owns the `SUBTASK_bar_dom/outputs/bar-dom.md` artifact and the `BAR-100..199` range per
  `../contracts/bar_partition.yaml`; minted nothing outside the range; redefined no inherited field.
- Feeds `SUBTASK_bar_synthesis`, which assembles the five fragments into `outputs/release-bar.md`,
  finalizes the cross-cutting MVP-vs-releasable staging, and asserts the subtree identities.

## Success criteria met
- Composes against `../contracts/` (BAR partition, fragment format, proposed-stage convention) and
  `../../contracts/` (`BAR-<NNN>` scheme, closed `verification_methods` vocab, `usable_early`/
  `releasable` stages); schema extended only, never redefined.
- All 79 release-gating `REQ-DOM-*` referenced by ≥1 `BAR-*`, the durable-persistence blocker
  included (`REQ-DOM-100` → `BAR-130`; `REQ-DOM-114` → `BAR-144`; `REQ-DOM-113` → `BAR-143`).
- Every `BAR-*` names one verification method from the closed vocabulary, references ≥1 `REQ-*`,
  and carries a `proposed_stage`.
- The coverage note lets the synthesis gate assert `GATING_REQ_COVERAGE` for the domain area
  without re-deriving the gating set; the two non-gating requirements (`REQ-DOM-010`,
  `REQ-DOM-016`) are recorded with the design's stated reason so the whole 81-requirement set is
  accounted for.

## Notes for the synthesis gate
- Staging in the fragment is a proposal from the domain view; the synthesis hub owns the final
  cross-cutting MVP line and may move a `BAR-*` between stages for whole-design coherence.
- `BAR_RANGE_RESPECTED` and `NO_BAR_COLLISION` hold for this fragment (ids `100..120`, `130..148`,
  `160..179`; no duplicates). Cross-area `REQ` references were not needed — every `BAR-*` here
  references `REQ-DOM-*` only.
- Methodology posture: the Phase-B `design` methodology loader was unavailable run-wide
  (`agent_domain_unset`); the fragment was authored by applying the product-design persona's
  release-definition judgment and the relayed bundle guidance, consistent with the subtree hub.
  This note is taskflow-internal; it does not appear in the repository-bound deliverable.
