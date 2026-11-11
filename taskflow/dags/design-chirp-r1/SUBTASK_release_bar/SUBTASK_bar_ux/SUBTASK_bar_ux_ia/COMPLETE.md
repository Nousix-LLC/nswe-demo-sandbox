# COMPLETE — SUBTASK_bar_ux_ia

## What was done
Authored the IA & interaction-model slice of the experience-area release bar: `BAR-200..214` holding every
release-gating `REQ-UX-*` in the band `REQ-UX-001..014, 016, 017, 018` (17 gating) to a concrete, testable
release condition, plus a coverage note mapping each gating requirement to the `BAR-*` that covers it.

## Output
- `SUBTASK_bar_ux_ia/outputs/bar-ux-ia.md` — 15 `BAR-*` blocks (`BAR-200..214`) + the IA-area coverage note.

## Decompose evaluation
`Atomic`. One homogeneous release-definition pass over one coherent experience area (IA/interaction): one
methodology, one kind of transformation (release-gating `REQ-UX-*` → checkable `BAR-*`), one output file.
Token/scope/output triggers all cleared; Distinct-Concerns and Single-Responsibility tests both passed
(evaluated independently against this brief, not on the ground that a parent already fanned out by area).

## How it composes with the parent
- Composes against `../contracts/bar_ux_partition.yaml` (my sub-range `BAR-200..214`; the per-area gating
  set; the per-BAR field set; the `proposed_stage` convention), `../../contracts/bar_partition.yaml`
  (the `SUBTASK_release_bar` `BAR-200..299` partition), and `../../../contracts/id_and_traceability_schema.yaml`
  (the `BAR-<NNN>` scheme, the closed `verification_methods` vocab, the stage vocab). No inherited schema
  redefined.
- `SUBTASK_bar_ux_synthesis` assembles this fragment with the four sibling area fragments into
  `SUBTASK_bar_ux/outputs/bar-ux.md`, reconciles the within-UX stages, and asserts the subtree identities.
  This fragment supplies the IA-area rows of `UX_GATING_REQ_COVERAGE` and stays within its sub-range
  (`UX_BAR_RANGE_RESPECTED`), with distinct ids (`UX_NO_BAR_COLLISION`).

## Coverage / identity readiness
- Every gating `REQ-UX-001..014, 016, 017, 018` referenced by ≥1 `BAR-*` (coverage note is authoritative).
- Every `BAR-*` names a `verification_method` from the frozen vocabulary (`manual_user_check`, `inspection`,
  `automated_test`) and references ≥1 `REQ-*` and carries a `proposed_stage` ∈ {`usable_early`,`releasable`}.
- No `BAR-*` is justified solely by non-gating `REQ-UX-015` or `REQ-UX-019`; neither is referenced.
- One `BAR-*` enforces multiple related requirements where they form one checkable condition: BAR-213
  (REQ-UX-014 sign-up landing + REQ-UX-016 sign-out no-leak) and BAR-214 (REQ-UX-017 settings grouping +
  REQ-UX-018 rules/help reachability).

## Notes
- Methodology posture: the `design` methodology loader was unavailable in this environment
  (`agent_domain_unset`, run-wide, as the subtree hub recorded). Applied the product-designer persona's
  release-definition judgment with the relayed bundle posture (Release Definition primary; Experience Design,
  Product Strategy supporting) rather than blocking. Recorded here (taskflow-internal); kept out of the
  repository-bound deliverable.
- The deliverable is repository-ready: no host/system/taskflow detail, no attribution trailer.
