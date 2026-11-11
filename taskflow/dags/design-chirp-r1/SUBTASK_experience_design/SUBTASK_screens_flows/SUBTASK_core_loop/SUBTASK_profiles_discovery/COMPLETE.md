# COMPLETE — SUBTASK_profiles_discovery

## What this task did
Designed the core loop's **identity-and-find-people** surfaces as a section-part of
`screens-core-loop.md`, and minted the `REQ-UX-061..064` register. Evaluation: **Atomic** — one design
responsibility (the profile/discovery screen cluster), one deliverable; every size trigger cleared or sat
in the non-mandatory band, and both concern tests passed.

## Output produced
- `outputs/screens-profiles-discovery.md` — the Public profile, Own profile, Followers, Following, and
  Explore / find-people surfaces, each at wireframe-level detail (layout, content, primary action, and
  empty / error / loading states), followed by the `REQ-UX-061..064` requirements with testable
  acceptance criteria, `release_gating` flags, and `REQ-PROD` traces.

## How it composes with the subtree
- Owns, per `../contracts/`: surfaces `view_profile` and `discovery_find_people`, and the
  `REQ-UX-061..064` sub-range (4 ids: 061, 062, 063, 064).
- Composes against the frozen screen inventory and component library by name; introduces no screen or
  component outside them.
- Borrows (does not redesign): the follow/unfollow control (social-actions part) and the edit-profile
  screen (account-lifecycle part); aligns per-screen states to the product-wide patterns and
  expired-session recovery (considered-states part).
- Feeds `SUBTASK_synthesis`, which assembles the four spoke outputs into `../outputs/screens-core-loop.md`
  and asserts the subtree identities.

## Identity evidence (for the synthesis gate)
- SURFACE_COVERAGE — view_profile (public/own/followers/following) and discovery_find_people designed with
  their empty/error/loading states; both owned surfaces covered, no hole, no double-write.
- ID_UNIQUE_IN_RANGE — 061, 062, 063, 064: unique, contiguous, within the assigned sub-range.
- NOT_SKELETAL — each surface specifies layout, content, a primary action, and three states.
- UX_TESTABLE_AND_GATED — every entry has a statement, a live-product-checkable acceptance_criteria, and a
  release_gating flag; REQ-UX-064 is false with a recorded reason (rides non-gating REQ-PROD-042).
- UX_TRACES_TO_PROD — 061→REQ-PROD-007; 062→REQ-PROD-007; 063→REQ-PROD-007, REQ-PROD-006; 064→REQ-PROD-042.
- COMPOSES_AGAINST_VOCAB — inventory screens/routes and library components referenced by name; nothing
  redefined or invented.
- STATES_CONSISTENT — per-screen states are the components' own named states, aligned to the global
  patterns.
- HYGIENE — output carries no host/system/taskflow detail, no workspace paths, no run ids, no attribution.

## Notes
- The design methodology loader was unavailable in this environment (agent domain unset); the surfaces
  were designed from the Experience Design intent and Product Strategy framing per the hubs' recorded
  posture. Limitation recorded in the deliverable; did not block.
