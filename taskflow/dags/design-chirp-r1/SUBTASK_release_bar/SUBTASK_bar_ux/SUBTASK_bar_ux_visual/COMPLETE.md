# COMPLETE — SUBTASK_bar_ux_visual

**Task**: Author the visual-language & component-system release-bar fragment `BAR-215..229`
enforcing every release-gating `REQ-UX-020..039`.

**Decompose evaluation**: Atomic. One experience area (visual language & component system), one
kind of change (author BAR criteria), one declared output fragment. Token/Scope/Output-Size triggers
and both concern tests cleared against this brief; "already a spoke" was not cited as grounds.

**Resumption note**: This node was reconstructed from its file image. A prior invocation had authored
`outputs/bar-ux-visual.md` but published no terminal record, so the node was non-terminal. This
invocation re-ran the boot/evaluation contract, verified the existing output against the authoritative
experience design and the three inherited contracts, found it correct and compliant, and drove the
node to a clean `completed` terminal. No revision of the fragment was warranted.

## Output
- `SUBTASK_bar_ux_visual/outputs/bar-ux-visual.md` — 15 `BAR-215..229` blocks (each: id, statement,
  references ≥1 `REQ-UX-*`, verification_method from the closed vocab, proposed_stage) plus the
  sub-area coverage note. Repository-ready.

## Verification against success criteria
- **Composes against contracts** (`../contracts/`, `../../contracts/`, `../../../contracts/`): `BAR-<NNN>`
  3-digit ids all within `BAR-215..229`; closed `verification_methods` vocabulary; stage ∈
  {usable_early, releasable}; per-BAR field set as inherited. No inherited schema redefined.
- **Gating coverage**: the 17 release-gating `REQ-UX-*` in this band (020, 021, 022, 025–029, 031–039),
  confirmed from the design's per-REQ `release_gating` flag, are each referenced by ≥1 `BAR-*`:
  020→215, 021→216, 022→217, 025→218, 026→219, 027→220, 028→221, 029→222, 031→226, 032→223,
  033→224, 034→224, 035→225, 036→226, 037→227, 038→228, 039→229.
- **Testable**: every `BAR-*` names a verification method and references ≥1 `REQ-*`; every statement is
  a concrete live-product check (e.g. BAR-217 measures ≥4.5:1 normal / ≥3:1 large & control boundaries),
  not a requirement restatement.
- **Non-gating excluded**: no `BAR-*` is justified solely (or at all) by a non-gating `REQ-UX-*`
  (023, 024, 030); the coverage note records them as accounted-for context only.
- **Coverage note present**: lets `SUBTASK_bar_ux_synthesis` assert UX_GATING_REQ_COVERAGE for the
  visual sub-area without re-deriving the gating set.
- **Hygiene**: no host/system/taskflow detail; only repo-relative `design/experience-design.md`
  referenced; no attribution trailer.

## Methodology posture
The `design` methodology loader is unavailable run-wide (`agent_domain_unset`); as the hub and parent
recorded, the product-designer persona's release-definition judgment plus the relayed bundle guidance
(Release Definition primary; Experience Design, Product Strategy supporting) were applied. Recorded in
this internal record only; kept out of the repository-bound deliverable.

## Hand-off
`SUBTASK_bar_ux_synthesis` (dependent) assembles this fragment with the four sibling sub-fragments into
`SUBTASK_bar_ux/outputs/bar-ux.md`, finalizes the within-UX stage line, and asserts the subtree
identities.
