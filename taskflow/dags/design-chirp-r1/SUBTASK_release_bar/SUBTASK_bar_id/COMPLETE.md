# COMPLETE — SUBTASK_bar_id (release-bar criteria, identity/security/trust, BAR-300..399)

## What was done
Translated the identity & security design's **release-gating** `REQ-ID-*` set into 40 testable
release-bar criteria (`BAR-300 .. BAR-339`), each a checkable release condition rather than a
restatement of the requirement, plus a coverage note mapping every gating `REQ-ID-*` to the `BAR-*`
that holds it.

## Output
- `SUBTASK_bar_id/outputs/bar-id.md` — 40 `BAR-*` blocks (id, statement, references ≥1 `REQ-ID-*`,
  verification_method, proposed_stage) + coverage note + non-gating record + sibling-dependency notes.

## How it composes with the parent
- Composed against the inherited contract (`../../contracts/id_and_traceability_schema.yaml`,
  `design_artifact_map.yaml`) and the subtree sub-contract (`../contracts/bar_partition.yaml`,
  `_MANIFEST.yaml`); no schema redefined.
- Supplies the identity-area slice the synthesis hub (`SUBTASK_bar_synthesis`) folds into
  `release-bar.md`, finalizing the cross-cutting MVP-vs-releasable staging and asserting the
  subtree identities. `proposed_stage` values are proposals from the identity/trust view; the hub owns
  the authoritative cross-cutting stage line.

## Verification performed
- **BAR_RANGE_RESPECTED**: all 40 ids in `BAR-300..399`, none outside. OK.
- **NO_BAR_COLLISION** (within this fragment): no duplicate ids. OK.
- **GATING_REQ_COVERAGE** (identity area): all 63 `release_gating: true` `REQ-ID-*` in the design doc
  referenced by ≥1 `BAR-*` (checked against the authoritative gating set extracted from the doc). OK.
- **BAR_TESTABLE**: every block names a `verification_method` from the closed vocabulary
  (manual_user_check / automated_test / inspection / operational_check) and references ≥1 `REQ-ID-*`. OK.
- **Staging**: every block carries a `proposed_stage` ∈ {usable_early, releasable}. OK.
- **HYGIENE**: deliverable carries no host/system/taskflow detail and no attribution trailer; narrative
  scanned for AI-writing tells (none). OK.

## Scope note
Non-gating `REQ-ID-*` (006, 011, 012, 047, 048, 050, 051, 083, 084, 089) are recorded in the coverage
note as deliberately not bar-gated, each per the design's stated reason, so the synthesis gate sees the
omission is intentional. The block/mute v1 decision (REQ-ID-083/084) is flagged for the hub to resolve;
the reporting floor (BAR-334/335) is gated regardless.

## Constraint recorded (taskflow-internal, kept out of the repository deliverable)
The Phase-B `design` methodology loader was unavailable in this environment (methodology surface returns
`agent_domain_unset`, consistent with the subtree hub's recorded run-wide condition). Applied the
product-design persona's release-definition judgment and the relayed methodology posture (Release
Definition primary; Identity and Trust, Product Strategy supporting) rather than blocking.
