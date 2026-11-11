# COMPLETE — SUBTASK_bar_screens_safety_states

**Task**: Author `BAR-256..263` enforcing the release-gating `REQ-UX-079, 082, 083, 084, 085, 086, 087, 088,
089` (safety/help/rules/not-found + cross-screen state patterns) of the screens-&-flows UX release bar.

**Decompose evaluation**: Atomic. One authoring responsibility (gating REQ → testable BAR criterion), one
output fragment, one shared tight id budget. The two thematic bodies share one id budget, one fragment, and
one coverage note, and the state-pattern criteria are checked on the same safety surfaces — not separable to
parallel specialists. Token/output/tool-call envelopes all cleared; Distinct-Concerns and Single-Responsibility
tests passed. Evaluated independently of the parent's prior split and without reliance on the designer
hold-it-whole instinct.

## Output produced

- `outputs/bar-screens-safety-states.md` — 8 `BAR-*` blocks (`BAR-256..263`) + per-chapter coverage note.
  Repository-ready (no host/system/taskflow detail, no attribution trailer).

## What was done

Turned the chapter's 9 release-gating requirements into 8 checkable release conditions, clustering the
considered-states umbrella (`REQ-UX-085`) with the empty-treatment specific (`REQ-UX-086`) into `BAR-260` to
fit the tight id budget. Each criterion is stated as a fact a stranger can observe on the live product, in the
user's terms, with a verification method from the frozen vocabulary and a proposed stage.

| BAR | Enforces | verification_method | proposed_stage |
|---|---|---|---|
| BAR-256 | REQ-UX-079 (→ REQ-PROD-025, 026) | manual_user_check | releasable |
| BAR-257 | REQ-UX-083 (→ REQ-PROD-026) | manual_user_check | releasable |
| BAR-258 | REQ-UX-082 (→ REQ-PROD-028, 013) | manual_user_check | releasable |
| BAR-259 | REQ-UX-084 (→ REQ-PROD-033) | manual_user_check | usable_early |
| BAR-260 | REQ-UX-085, 086 (→ REQ-PROD-033, 034) | manual_user_check | usable_early |
| BAR-261 | REQ-UX-087 (→ REQ-PROD-033) | manual_user_check | usable_early |
| BAR-262 | REQ-UX-088 (→ REQ-PROD-033) | manual_user_check | usable_early |
| BAR-263 | REQ-UX-089 (→ REQ-PROD-034) | manual_user_check | releasable |

**Staging rationale (proposal only; synthesis finalizes within screens)**: the cross-screen state-pattern
basics and the not-found screen (`BAR-259..262`) are `usable_early` — a product that blanks, hangs, silently
fails, or shows broken pages is not usable even in an early build. The safety/governance surfaces (report,
stated rules, help & support) and the session/transient recovery guarantee (`BAR-256, 257, 258, 263`) are
`releasable` — required before real users and real sessions, but not needed to exercise the core loop early.

`verification_method` is `manual_user_check` across all 8: each criterion is a "person exercises the live
product and observes the designed treatment" release gate, which is exactly what that method denotes and what
the brief's state-pattern constraint calls for.

## Success criteria

- [x] Composes against inherited contracts; `BAR-*` only within `BAR-256..263`; no inherited schema redefined.
- [x] Every release-gating `REQ-UX-079, 082..089` referenced by ≥1 `BAR-*` (9/9).
- [x] Every `BAR-*` names a frozen-vocabulary `verification_method`, references ≥1 `REQ-*`, carries a `proposed_stage`.
- [x] No `BAR-*` justified solely by a non-gating `REQ-UX-*` (078, 080, 081 named as not-covered).
- [x] Coverage note lets the synthesis gate assert chapter gating coverage without re-deriving the set.

## Notes for the synthesis gate (`SUBTASK_bar_screens_synthesis`)

- Ids `BAR-256..263` all within sub-range; no collisions introduced from this chapter.
- Cross-references: `BAR-263` names `REQ-UX-007` and `REQ-UX-008` in prose as the IA conventions it observes;
  these are NOT in its `references` (it enforces `REQ-UX-089`), so they create no coverage claim here.
- Methodology posture: the Phase-B `design` loader was unavailable (`agent_domain_unset`, run-wide, as the hub
  recorded); applied the product-designer persona's release-definition judgment + the relayed bundle guidance.
  This note is taskflow-internal and is kept out of the repository-bound fragment.
