# COMPLETE — SUBTASK_bar_ops

## What was done
Authored the operational-readiness slice of the release bar: the `BAR-400..499` criteria that enforce every
release-gating `REQ-OPS-*` from the operational-readiness design, plus the coverage note the synthesis gate consumes.

## Output produced
- `SUBTASK_bar_ops/outputs/bar-ops.md` — 49 `BAR-*` criteria (`BAR-400..412`, `BAR-420..432`, `BAR-440..445`,
  `BAR-460..468`, `BAR-480..487`), each carrying the inherited field set (`id`, `statement`, `references` ≥1
  `REQ-OPS-*`, `verification_method`, `proposed_stage`), organized by concern (durable data; backups and recovery;
  limits and quotas; observability; status and incident), followed by a coverage note mapping all 59 release-gating
  `REQ-OPS-*` to the `BAR-*` that holds each.

## How it composes with the parent
Feeds `SUBTASK_bar_synthesis`, which assembles the five area fragments into `outputs/release-bar.md`, finalizes the
cross-cutting MVP-vs-releasable staging line (my `proposed_stage` values are proposals it may move), runs the
whole-design completeness and gap review, and asserts the subtree identities. This fragment supplies the operations
area's inputs to `BAR_RANGE_RESPECTED` (all ids in `BAR-400..499`), `NO_BAR_COLLISION` (49 distinct ids),
`GATING_REQ_COVERAGE` (all 59 gating `REQ-OPS-*` referenced, with the coverage note so the gate need not re-derive the
gating set), `BAR_TESTABLE` (every criterion names a frozen-vocabulary verification method and references ≥1 `REQ-*`),
and `BAR_STAGED` (every criterion carries a proposed stage).

## Contract compliance
- Composed against `../contracts/bar_partition.yaml` and `../../contracts/id_and_traceability_schema.yaml`; minted
  `BAR-*` only within the owned `BAR-400..499` range; redefined no inherited field, vocabulary, or section.
- `verification_method` values drawn only from `{manual_user_check, automated_test, inspection, operational_check}`;
  `proposed_stage` only `{usable_early, releasable}`.
- Referenced `REQ-OPS-*` without re-authoring them; specified release conditions as checkable product/operator
  properties, never implementation.

## Verification performed
- Coverage: cross-checked the fragment's referenced `REQ-OPS-*` against the operational-readiness design's OPS
  traceability table — all 59 `release_gating: true` requirements are referenced by ≥1 `BAR-*`; no non-gating
  `REQ-OPS-*` is referenced.
- Range and collision: the 49 `BAR-*` ids are distinct and all within `BAR-400..499`.
- Field and vocabulary completeness: each of the 49 criteria carries exactly one `statement`, `references`,
  `verification_method`, and `proposed_stage`; all method and stage values are in the frozen vocabularies.

## Notes for the synthesis gate
- The `design` methodology loader was unavailable run-wide (`agent_domain_unset`); applied the product-design persona's
  release-definition judgment plus the relayed bundle guidance (Release Definition primary; Release Readiness, Product
  Strategy support), consistent with the subtree hub's recorded posture and the sibling gates.
- Staging proposals and the two foundational-looking criteria proposed `releasable` on account of dependencies owned
  elsewhere (BAR-405 upgrade path; BAR-485 experience-area degraded states) are explained in the fragment's staging
  note for the cross-cutting finalization.
- The deliverable is repository-ready: no host/system/taskflow detail, no attribution trailer.
