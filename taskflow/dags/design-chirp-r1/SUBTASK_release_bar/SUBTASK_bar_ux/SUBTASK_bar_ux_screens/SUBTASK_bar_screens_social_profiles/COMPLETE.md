# COMPLETE — SUBTASK_bar_screens_social_profiles

**Task Kind**: standard · **Depends on**: none · **Evaluation**: Atomic

## What was done
Authored the social-interactions & profiles chapter of the screens release-bar fragment: `BAR-243..247`
holding every release-gating `REQ-UX-058..063` to a checkable release condition, plus a per-chapter
coverage note, composed against the inherited contracts.

## Output produced
- `SUBTASK_bar_screens_social_profiles/outputs/bar-screens-social-profiles.md` — five `BAR-*` blocks
  (inherited field set: `id`, `statement`, `references`, `verification_method`, `proposed_stage`), a
  staging rationale, and the coverage note. Repository-ready.

## BAR → gating REQ map (the clustering, 5 ids for 6 gating REQs)
- BAR-243 ← REQ-UX-058 (reply from conversation; reply-to-gone; signed-out sign-in path) · REQ-PROD-003
- BAR-244 ← REQ-UX-059 (idempotent like toggle; accurate count; more-than-colour; revert on failure) · REQ-PROD-005
- BAR-245 ← REQ-UX-060 (idempotent follow; no self-follow; revert on failure) · REQ-PROD-006
- BAR-246 ← REQ-UX-061 + REQ-UX-062 (public profile with/without session; owner edit entry) · REQ-PROD-007
- BAR-247 ← REQ-UX-063 (addressable paginated followers/following lists; per-row follow) · REQ-PROD-007, 006

Clustered 061+062 into BAR-246 (public and owner views of the one profile surface) to fit the tight
5-id budget over 6 gating requirements, as the brief invited.

## Success criteria — self-check
- [x] Composes against inherited contracts; `BAR-*` only within `BAR-243..247`; no inherited schema redefined.
- [x] Every release-gating `REQ-UX-058..063` referenced by ≥1 `BAR-*` (verified: 058→243, 059→244, 060→245, 061/062→246, 063→247).
- [x] Every `BAR-*` names a frozen-vocabulary `verification_method` (all `manual_user_check` — each criterion is a behaviour a person exercises on the live product), references ≥1 `REQ-*`, carries a `proposed_stage`.
- [x] No `BAR-*` justified solely by non-gating `REQ-UX-064` (it appears only in the non-gating note).
- [x] Coverage note lets `SUBTASK_bar_screens_synthesis` assert social-&-profiles gating coverage without re-deriving the set.

## Staging proposal (chapter view; synthesis finalizes)
usable_early: BAR-243, BAR-244, BAR-245, BAR-246 (the social core). releasable: BAR-247 (dedicated
followers/following list pages; profile counts carry the early need).

## Notes for the synthesis gate
- Verification method is `manual_user_check` throughout: these are observable UI behaviours checked on
  the live product, kept in the designer's lane (what, not how) rather than prescribing repo tests.
- The Phase-B `design` methodology loader was unavailable run-wide (`agent_domain_unset`); applied the
  product-designer persona's release-definition judgment and the relayed bundle guidance per the hub's
  recorded posture. This note is taskflow-internal and is kept out of the repository-bound deliverable.
