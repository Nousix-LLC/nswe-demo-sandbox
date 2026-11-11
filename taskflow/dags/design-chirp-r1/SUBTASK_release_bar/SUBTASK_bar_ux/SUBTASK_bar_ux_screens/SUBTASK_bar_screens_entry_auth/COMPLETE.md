# COMPLETE — SUBTASK_bar_screens_entry_auth

## What was done
Authored the entry & auth chapter of the screens release bar: `BAR-230..237`, enforcing every
release-gating `REQ-UX-040..050` (11 requirements) from `design/experience-design.md`. Composed
against the inherited contracts (`../contracts/bar_screens_partition.yaml` and its ancestors for the
`BAR-<NNN>` scheme, the per-BAR field set, the closed `verification_methods` vocabulary, and the
`usable_early | releasable` stage vocabulary). No inherited schema redefined.

## Decompose evaluation
Atomic. One coherent chapter (the entry-auth flow) authored into one fragment; the tight id budget
(8 ids for 11 gating requirements) forces cross-screen clustering a single author must hold whole,
so the Scope / Distinct-Concerns triggers did not fire. Token, output-size, and single-responsibility
checks all cleared. Reached independently on this brief's own merits, not because a parent split.

## Output
- `SUBTASK_bar_screens_entry_auth/outputs/bar-screens-entry-auth.md` — 8 `BAR-*` blocks
  (`BAR-230..237`), each with `id`, `statement`, `references`, `verification_method`,
  `proposed_stage`, plus the per-chapter coverage note mapping every gating `REQ-UX-040..050` to its
  covering `BAR-*`. Repository-ready (no host/system/taskflow detail, no attribution trailer).

## Clustering (8 ids, 11 gating requirements)
- BAR-230 ← REQ-UX-040 (Landing)
- BAR-231 ← REQ-UX-041, 043 (sign-up create + to-be-verified contact)
- BAR-232 ← REQ-UX-042 (handle format/uniqueness, field-level)
- BAR-233 ← REQ-UX-044, 045 (sign-in own-credential + no-leak distinction)
- BAR-234 ← REQ-UX-046, 047 (self-service recovery + set new credential)
- BAR-235 ← REQ-UX-048 (sign-out)
- BAR-236 ← REQ-UX-049 (designed empty/error/loading states)
- BAR-237 ← REQ-UX-050 (land-right + no-leak; gating basis only, not the non-gating interlinks)

## Proposed staging (chapter view; screens synthesis finalizes)
- usable_early: BAR-230, 231, 232, 233, 235 (the get-in/get-out path and account integrity)
- releasable: BAR-234, 236, 237 (self-service recovery, designed states across every surface, the
  full land-right/no-leak routing)

## Verification against success criteria
- [x] Composes against inherited contracts; `BAR-*` only within `BAR-230..237`; nothing redefined.
- [x] Every release-gating `REQ-UX-040..050` referenced by ≥1 `BAR-*`.
- [x] Every `BAR-*` names a frozen `verification_method`, references ≥1 `REQ-*`, carries a `proposed_stage`.
- [x] Coverage note present; the synthesis gate can assert entry-auth gating coverage without re-deriving.
- [x] No `BAR-*` rests on a non-gating `REQ-UX-*` (none fall in 040..050).

## Note for the synthesis gate
This fragment feeds `SUBTASK_bar_screens_synthesis`, which assembles the five chapter sub-fragments
into `outputs/bar-ux-screens.md`, finalizes one coherent per-`BAR-*` stage across screens, and
asserts SCREENS_* identities. The `proposed_stage` values above are this chapter's proposal only.

## Environment note (taskflow-internal)
The `design` methodology loader was unavailable in this environment (`agent_domain_unset`, recorded
run-wide by ancestors). Applied the product-designer persona's release-definition judgment plus the
relayed hub guidance (Release Definition primary; Experience Design, Product Strategy supporting),
as the hub directed. This note is taskflow-internal and is kept out of the repository-bound output.
