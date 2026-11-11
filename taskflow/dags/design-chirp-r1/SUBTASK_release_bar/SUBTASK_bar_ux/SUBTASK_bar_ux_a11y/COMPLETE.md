# COMPLETE — SUBTASK_bar_ux_a11y

## What was done
Authored the accessibility slice of the experience-area release bar: 20 `BAR-*` criteria in the assigned
sub-range `BAR-275..294`, each holding a release-gating accessibility requirement to a concrete, testable
release condition, plus a coverage note and a staging proposal.

## Output produced
- `SUBTASK_bar_ux_a11y/outputs/bar-ux-a11y.md` — the `BAR-275..294` register (one block per `BAR-*`: id,
  statement, references, verification_method, proposed_stage), the coverage note mapping every gating
  `REQ-UX-*` in the band to its covering `BAR-*`, and the accessibility-area staging proposal.

## How it composes with the parent
- Owns `BAR-275..294` and `bar-ux-a11y.md` exactly as assigned in `contracts/bar_ux_partition.yaml`; mints no
  id outside that sub-range.
- Composes against the three inherited seams (`../contracts/`, `../../contracts/`, `../../../contracts/`):
  uses the `BAR-<NNN>` scheme, the closed `verification_methods` vocabulary, the inherited per-BAR field set,
  and the `{usable_early, releasable}` stage vocabulary; redefines nothing inherited.
- Feeds `SUBTASK_bar_ux_synthesis`, which assembles the five sub-fragments into `outputs/bar-ux.md`, finalizes
  the within-UX staging, and asserts the sub-identities. The coverage note is shaped so the gate can assert
  `UX_GATING_REQ_COVERAGE` for the accessibility sub-area without re-deriving the gating set.

## Coverage and exclusions
- Gating set covered (19): `REQ-UX-100, 101, 102, 103, 104, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115,
  116, 117, 118, 119`. Each is referenced by ≥1 `BAR-*`; `REQ-UX-113` is split across `BAR-287` (no colour
  alone) and `BAR-288` (no flash), using the one spare id in the sub-range.
- Excluded: `REQ-UX-105` (WCAG 2.2 target size, `release_gating: false`) — not covered, referenced by no
  `BAR-*`, and the sole basis of none.

## Sub-identity readiness (for the synthesis gate)
- UX_BAR_RANGE_RESPECTED: all ids in `BAR-275..294`.
- UX_BAR_TESTABLE: every `BAR-*` names a frozen-vocab `verification_method` and references ≥1 `REQ-*`.
- UX_GATING_REQ_COVERAGE: all 19 gating REQ in band covered (see coverage note).
- UX_NONGATING_EXCLUDED: `REQ-UX-105` is the sole basis of no `BAR-*`.
- UX_BAR_STAGED: every `BAR-*` carries one proposed stage.
- UX_HYGIENE: the fragment carries no host/system/taskflow detail and no attribution trailer.

## Note (taskflow-internal)
The Phase-B `design` methodology loader was unavailable run-wide (`agent_domain_unset`), as the subtree hub
recorded. Per the hub's recorded posture, the product-designer persona's release-definition judgment and the
relayed bundle guidance (Release Definition primary; Experience Design, Product Strategy supporting) were
applied rather than blocking. This note is internal and is deliberately kept out of the repository-bound
deliverable.
