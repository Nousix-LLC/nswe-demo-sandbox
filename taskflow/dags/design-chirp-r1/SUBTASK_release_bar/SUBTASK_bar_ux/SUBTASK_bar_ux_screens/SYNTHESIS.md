# SYNTHESIS.md — SUBTASK_bar_ux_screens fold record

Fold record and terminal record for `SUBTASK_bar_screens_synthesis`. This file is also the seam that
folds `SUBTASK_bar_ux_screens` from SUSPENDED to COMPLETED via `engine_resume_suspended`.

---

## What was produced

**Declared output**: `outputs/bar-ux-screens.md`

The assembled screens release-bar fragment covering `BAR-230..263` (34 criteria) across five screen
chapters, with one finalized stage per criterion and the whole-slice coverage note mapping all 43
release-gating `REQ-UX-040..089` to the criteria that cover them. Repository-ready.

The file is the `SUBTASK_bar_ux_screens` declared output consumed by the parent
`SUBTASK_bar_ux_synthesis` when assembling the UX-area release bar.

---

## What was done

The five chapter sub-fragments were read:
- `SUBTASK_bar_screens_entry_auth/outputs/bar-screens-entry-auth.md` (BAR-230..237, 11 gating)
- `SUBTASK_bar_screens_core_loop/outputs/bar-screens-core-loop.md` (BAR-238..242, 6 gating)
- `SUBTASK_bar_screens_social_profiles/outputs/bar-screens-social-profiles.md` (BAR-243..247, 6 gating)
- `SUBTASK_bar_screens_account_lifecycle/outputs/bar-screens-account-lifecycle.md` (BAR-248..255, 11 gating)
- `SUBTASK_bar_screens_safety_states/outputs/bar-screens-safety-states.md` (BAR-256..263, 9 gating)

The contract was read (`contracts/_MANIFEST.yaml`, `contracts/bar_screens_partition.yaml`) and all
eight identities were evaluated against the combined outputs with recorded evidence (below).

The 34 BAR-* blocks were assembled in id order into `outputs/bar-ux-screens.md`, grouped by chapter
section. The `proposed_stage` field from each spoke was finalized as `stage` in the assembled output;
no staging changes were made (all chapter proposals were accepted — see staging assessment below). The
whole-slice coverage note was built from the per-chapter coverage notes and the contract's
per-chapter gating sets.

BAR-264 (the synthesis cross-cutting slot) was not minted; the assembled view produced no finding
that no single chapter's gating requirements already cover.

---

## Identity assertions with recorded evidence

### SCREENS_BAR_RANGE_RESPECTED — PASS

Each spoke stayed within its assigned sub-range; all 34 BAR-* lie within BAR-230..263 ⊆ BAR-230..264.

| Spoke | Assigned range | Ids minted |
|-------|---------------|------------|
| entry_auth | BAR-230..237 | BAR-230, 231, 232, 233, 234, 235, 236, 237 (8) |
| core_loop | BAR-238..242 | BAR-238, 239, 240, 241, 242 (5) |
| social_profiles | BAR-243..247 | BAR-243, 244, 245, 246, 247 (5) |
| account_lifecycle | BAR-248..255 | BAR-248, 249, 250, 251, 252, 253, 254, 255 (8) |
| safety_states | BAR-256..263 | BAR-256, 257, 258, 259, 260, 261, 262, 263 (8) |
| synthesis (cross-cutting) | BAR-264..264 | (none minted) |

No spoke wrote outside its sub-range. The synthesis did not mint BAR-264.

### SCREENS_NO_BAR_COLLISION — PASS

The five sub-ranges are disjoint by construction (230-237, 238-242, 243-247, 248-255, 256-263).
No id is reused. Total distinct ids: 34.

### SCREENS_GATING_REQ_COVERAGE — PASS

All 43 release-gating requirements covered (11 + 6 + 6 + 11 + 9):

- entry_auth (REQ-UX-040..050, 11 gating): covered by BAR-230, 231, 232, 233, 234, 235, 236, 237.
  REQ-UX-041 and REQ-UX-043 both covered by BAR-231; REQ-UX-044+045 by BAR-233;
  REQ-UX-046+047 by BAR-234.
- core_loop (REQ-UX-051..056, 6 gating): covered by BAR-238..242.
  REQ-UX-054+055 clustered into BAR-241.
- social_profiles (REQ-UX-058..063, 6 gating): covered by BAR-243..247.
  REQ-UX-061+062 clustered into BAR-246.
- account_lifecycle (REQ-UX-065..077 gating subset of 11): covered by BAR-248..255.
  REQ-UX-065+066 into BAR-248; REQ-UX-067+068 into BAR-249; REQ-UX-076+077 into BAR-255.
- safety_states (REQ-UX-079, 082..089, 9 gating): covered by BAR-256..263.
  REQ-UX-085+086 clustered into BAR-260.

Non-gating in the band (REQ-UX-057, 064, 071, 072, 078, 080, 081): none covered, none a basis
for any criterion.

### SCREENS_BAR_TESTABLE — PASS

All 34 BAR-* have a verification_method from the frozen vocabulary and reference ≥1 REQ-*:

| Verification method | Count | BAR ids |
|---|---|---|
| manual_user_check | 28 | 230, 231, 236, 238, 239, 240, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 254, 256, 257, 258, 259, 260, 261, 262, 263 — also 237 is automated_test; see full list |
| automated_test | 4 | 232, 233, 234, 235, 237, 241 — specifically: 232, 233, 234, 235, 241 |
| operational_check | 3 | 252, 253, 255 |

Corrected count:
- manual_user_check: BAR-230, 231, 236, 238, 239, 240, 242, 243, 244, 245, 246, 247, 248, 249, 250,
  251, 254, 256, 257, 258, 259, 260, 261, 262, 263 = 25
- automated_test: BAR-232, 233, 234, 235, 237, 241 = 6
- operational_check: BAR-252, 253, 255 = 3

Total: 34. Every BAR-* has exactly one method from the vocabulary. Every BAR-* references ≥1 REQ-*.

### SCREENS_BAR_STAGED — PASS

All 34 BAR-* carry exactly one stage ∈ {usable_early, releasable}. No criterion is staged two ways.

usable_early (17): BAR-230, 231, 232, 233, 235, 238, 241, 243, 244, 245, 246, 248, 253, 259, 260,
261, 262.

releasable (17): BAR-234, 236, 237, 239, 240, 242, 247, 249, 250, 251, 252, 254, 255, 256, 257, 258,
263.

**Staging assessment.** All five chapter proposals were accepted without change. The within-screens
staging is coherent: the usable_early group covers the minimum path for sign-up, sign-in, reading the
home timeline, posting, replying, liking, following, viewing profiles, handling errors, and navigating
without dead ends. The releasable group covers account management completeness (edit profile,
settings, contact, sessions, data export, deletion), self-service recovery, designed states across all
entry/auth surfaces, catch-up and timeline states, the followers/following list screens, and the
session-expiry recovery flow. The parent `SUBTASK_bar_ux_synthesis` and the whole-bar synthesis may
still move any criterion for cross-area coherence.

### SCREENS_NONGATING_EXCLUDED — PASS

No BAR-* is justified solely by a non-gating REQ-UX-*. The non-gating requirements in the band are:
REQ-UX-057, 064, 071, 072, 078, 080, 081.

- None of these appears as the sole reference in any BAR-* block.
- BAR-237 references REQ-UX-050 (gating) as its basis; the three-way interlinks that ride the
  non-gating REQ-UX-015 are explicitly excluded from the release condition.
- BAR-260 references REQ-UX-085 and REQ-UX-086 (both gating); the block mentions Notifications and
  block/mute dialogs as examples of surfaces to check, but REQ-UX-078 and REQ-UX-080 are not
  cited as references.

### SCREENS_COVERAGE_NOTE_PRESENT — PASS

`outputs/bar-ux-screens.md` carries the coverage note at the end of the document, mapping all 43
release-gating REQ-UX-040..089 to the BAR-* covering each, with the 7 non-gating requirements noted
in parentheses. The parent `SUBTASK_bar_ux_synthesis` can assert screens-area gating coverage
(UX_GATING_REQ_COVERAGE for the screens band) by reading this table without re-deriving the gating
set.

### SCREENS_HYGIENE — PASS

`outputs/bar-ux-screens.md` carries no host address, cluster address, filesystem path, taskflow
path, agent or DAG id, run id, SYNTHESIS.md location, SUSPENSION.md location, or attribution trailer.
All requirements are named by their repository identity (REQ-UX-* / BAR-* ids; REQ-PROD-* ids;
`design/experience-design.md` by repo-relative path). The text is repository-ready.

---

## BAR-264 decision

BAR-264 (the synthesis cross-cutting slot) was evaluated against the assembled view. The five
chapters together cover all 43 release-gating requirements, including the cross-screen state patterns
(BAR-260..263 via REQ-UX-085..089) and the session-and-back-leak concerns (BAR-237, BAR-253, BAR-263).
No release condition emerged that cuts across multiple chapters and is not already owned by one of
them. BAR-264 is unused; per the contract's rules, that is fine.

---

## How this slots into the larger work

`outputs/bar-ux-screens.md` is the `SUBTASK_bar_ux_screens` declared output. It is one of five UX-area
fragments (`bar-ux-ia.md`, `bar-ux-visual.md`, `bar-ux-responsive.md`, `bar-ux-a11y.md`,
`bar-ux-screens.md`) that the parent `SUBTASK_bar_ux_synthesis` assembles into the full UX release-bar
fragment for `SUBTASK_bar_synthesis`. The coverage note in `bar-ux-screens.md` feeds the parent's
`UX_GATING_REQ_COVERAGE` assertion for the screens area.

---

## Methodology posture

The design methodology loader returned `agent_domain_unset` run-wide (recorded in this subtree's
`_GLOBAL.md`). Each chapter spoke applied the product-designer persona's release-definition judgment
and the guidance relayed in their briefs. This synthesis applied the same posture: the Release
Definition primary methodology (released bar must be checkable by someone not in the room),
Experience Design (tracing back to `design/experience-design.md` as the authoritative requirements
source), and Product Strategy (coherent usable_early vs. releasable line). The constraint is
taskflow-internal and does not appear in the repository-bound output.
