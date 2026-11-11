# COMPLETE — SUBTASK_bar_screens_core_loop

**Task**: Author `BAR-238..242` — the release-bar criteria enforcing every release-gating `REQ-UX-051..056`
(home timeline & compose core loop).
**Decompose evaluation**: Atomic (one coherent chapter, one output file, ~5 clustered criteria; all triggers
cleared, both concern tests passed).

## What was produced

`outputs/bar-screens-core-loop.md` — the core-loop chapter of the screens release-bar fragment: five `BAR-*`
blocks (`BAR-238..242`) each carrying the inherited field set (`id`, `statement`, `references`,
`verification_method`, `proposed_stage`), a coverage note mapping every core-loop gating `REQ-UX-*` to its
covering `BAR-*`, and staging-proposal notes for the screens synthesis gate.

## BAR → REQ mapping (6 gating REQs clustered into 5 ids)

| BAR | References | Verification | Proposed stage |
|-----|------------|--------------|----------------|
| BAR-238 | REQ-UX-051; REQ-PROD-002 | manual_user_check | usable_early |
| BAR-239 | REQ-UX-052; REQ-PROD-002 | manual_user_check | releasable |
| BAR-240 | REQ-UX-053; REQ-PROD-002 | manual_user_check | releasable |
| BAR-241 | REQ-UX-054, REQ-UX-055; REQ-PROD-001 | automated_test | usable_early |
| BAR-242 | REQ-UX-056; REQ-PROD-001, REQ-PROD-003 | manual_user_check | releasable |

Clustering rationale: `REQ-UX-054` (280-char enforcement) and `REQ-UX-055` (publish lock/confirm/keep-draft) are
the two halves of one checkable condition on the post action and share `BAR-241`; the other four gating
requirements map one-to-one. `REQ-UX-057` is non-gating and is referenced as a basis by no `BAR-*`.

## Success criteria — verified

- [x] Composes against the inherited contracts; `BAR-*` only within `BAR-238..242`; no inherited schema redefined.
- [x] Every release-gating `REQ-UX-051..056` is referenced by ≥1 `BAR-*`.
- [x] Every `BAR-*` names a `verification_method` from the frozen vocabulary, references ≥1 `REQ-*`, carries a `proposed_stage`.
- [x] No `BAR-*` is justified solely by the non-gating `REQ-UX-057`.
- [x] The coverage note lets the synthesis gate assert core-loop gating coverage without re-deriving the set.

## Notes for the synthesis gate (`SUBTASK_bar_screens_synthesis`)

- Staging proposals are this chapter's view; the gate reconciles them into one coherent per-`BAR` stage. The one
  early-critical element inside a `releasable`-proposed bar is the non-blank empty state in `BAR-240`.
- `BAR-242` is proposed `releasable` because its reply-slot placement depends on the conversation screen
  (owned by `SUBTASK_bar_screens_social_profiles` / `REQ-UX-058`); the inline + Compose-dialog placements are the
  usable-early minimum, already exercised by `BAR-241`.
- Methodology posture: the Phase-B `design` methodology loader was unavailable run-wide (`agent_domain_unset`);
  applied the product-designer persona's release-definition judgment plus the relayed bundle guidance (Release
  Definition primary; Experience Design, Product Strategy supporting), consistent with recorded ancestor practice.

The deliverable `outputs/bar-screens-core-loop.md` is repository-ready (no host/system/taskflow detail, no
attribution trailer).
