# Release bar — screens & flows: social interactions & profiles (BAR-243..247)

Release-gating criteria for the social-interactions and profiles/discovery-list chapter. Each `BAR-*`
enforces one or more release-gating `REQ-UX-*` from `design/experience-design.md` and states a release
condition as a fact a stranger can check against the live product, not as an implementation. Sub-range
`BAR-243..247` (owned by this chapter); ids are not reused by sibling chapters.

Field set per block (inherited schema): `id`, `statement`, `references`, `verification_method`,
`proposed_stage`. Verification methods are drawn from the closed vocabulary
(`manual_user_check`, `automated_test`, `inspection`, `operational_check`). `proposed_stage` is this
chapter's view (`usable_early` | `releasable`); the screens synthesis gate reconciles one coherent stage
per `BAR-*` across the five chapters, and the UX and whole-bar syntheses own the wider line.

---

## BAR-243 — A reply is written and published from the conversation, and a reply to a gone chirp is reported

- **id**: BAR-243
- **statement**: Signed in on a chirp's conversation, a person can write a reply within the character
  limit and publish it from the conversation's reply control; the published reply then appears in that
  conversation shown as answering the chirp, and its publication is confirmed. Attempting to reply to a
  chirp that no longer exists reports not-found at the reply control and keeps the typed draft, rather
  than appearing to send. Opened without a session, the conversation presents a visible way to sign in
  or sign up in place of the reply control, not a dead or silent one.
- **references**: REQ-UX-058, REQ-PROD-003
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-244 — Like is an idempotent toggle whose count only ever reflects what took, shown by more than colour

- **id**: BAR-244
- **statement**: A chirp's like control toggles between not-liked and liked, with the liked state
  distinguished by more than colour (a filled heart and a "Liked" label). Liking an already-liked chirp,
  or reloading the screen, does not raise the count a second time; unliking returns the count to its
  earlier value. When a like or unlike cannot be completed, the control returns to its prior state, the
  count is left unchanged (it never shows a like that did not take), and the failure is reported at the
  control with a way to retry. The control looks and behaves the same wherever the chirp is shown — in the
  timeline, in its conversation, and on a profile.
- **references**: REQ-UX-059, REQ-PROD-005
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-245 — Follow is an idempotent control that cannot start a follow of your own account

- **id**: BAR-245
- **statement**: On another person's profile header or in a person row, the follow control toggles
  between "Follow" and "Following"; following the same account again, or reloading, leaves exactly one
  follow in place with the control reading "Following", and unfollowing returns it to "Follow". A person's
  own identity never presents a Follow control — the own-identity action is "Edit profile" — so a
  self-follow cannot be started, and any attempt is refused and shown at the control. When a follow or
  unfollow cannot be completed, the control returns to its prior label, any follower count is unchanged,
  and the failure is reported at the control with a way to retry. The control looks and behaves the same
  wherever it appears (profile header and person rows).
- **references**: REQ-UX-060, REQ-PROD-006
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-246 — A profile shows identity and chirps to anyone, and its owner gets an edit entry in place of follow

- **id**: BAR-246
- **statement**: A person's profile at its handle URL shows their avatar, display name, handle, bio, and
  follower and following counts, above that person's own chirps in newest-first bounded pages with a way
  to load older ones, and loads both without a session and with one; signed in, the header also carries
  the follow control. When the signed-in owner opens their own profile, they see the same public face a
  visitor sees, with an "Edit profile" entry in place of the follow control that opens the edit-profile
  screen, and no follow control is shown on their own profile.
- **references**: REQ-UX-061, REQ-UX-062, REQ-PROD-007
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-247 — Followers and following open as addressable, paginated lists with a per-row follow control

- **id**: BAR-247
- **statement**: A profile's follower and following counts open the followers list and the following list,
  each at its own URL. Each list shows one person per row with enough to recognise the account (avatar,
  display name, handle, bio) in a bounded page with a way to load more, a labelled way back to the
  profile, and — for a signed-in viewer — a follow control on each row. Each list's URL, opened directly,
  lands on that list.
- **references**: REQ-UX-063, REQ-PROD-007, REQ-PROD-006
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

---

## Staging rationale (chapter view; synthesis finalizes)

- `usable_early` — reply (BAR-243), like (BAR-244), follow (BAR-245), and the profile surface
  (BAR-246) are the social core of the product: follow is what populates the followed timeline, and
  reply/like are the in-conversation actions that make it more than a broadcast feed. A first usable
  version needs these for the product to be the product.
- `releasable` — the dedicated followers/following **list pages** (BAR-247) are a completeness surface:
  the follower and following **counts** on the profile (BAR-246) carry the early need, so the addressable
  paginated list screens are proposed for the full release rather than the first usable version. The
  screens synthesis gate may move this for coherence with the rest of the screens area.

## Coverage note — every release-gating REQ-UX-058..063 → the BAR-* that covers it

| REQ-UX | Gating | Covered by | What the bar holds |
|--------|--------|------------|--------------------|
| REQ-UX-058 | yes | BAR-243 | Reply written/published from the conversation; reply-to-gone reported not-found with draft kept; signed-out sign-in/up path in place of the reply control |
| REQ-UX-059 | yes | BAR-244 | Like is an idempotent toggle; count reflects only what took; liked state by more than colour; reverts and reports on failure; consistent across placements |
| REQ-UX-060 | yes | BAR-245 | Follow is an idempotent control; no self-follow (own identity shows "Edit profile"); reverts and reports on failure; consistent across placements |
| REQ-UX-061 | yes | BAR-246 | Public profile shows identity + chirps with or without a session; follow control in header when signed in |
| REQ-UX-062 | yes | BAR-246 | Owner's own profile is their public face with an "Edit profile" entry in place of the follow control |
| REQ-UX-063 | yes | BAR-247 | Followers/following are addressable, paginated lists; per-row follow control signed in; way back to the profile |

All six release-gating `REQ-UX-058..063` in this chapter are referenced by at least one `BAR-*`. No
`BAR-*` in this fragment is justified solely by a non-gating requirement.

**Non-gating in the adjacent band, deliberately not covered here**: REQ-UX-057 (reading replies as a
navigable conversation — rides the non-gated REQ-PROD-004; the gating reply action is held by BAR-243)
and REQ-UX-064 (finding people to follow / Explore — rides the non-gated REQ-PROD-042). REQ-UX-064's
author recorded that a first release may ship follow-by-profile and follow-from-a-reply and add discovery
as a near-term follow-up; whether a minimum discovery surface is in scope is a whole-bar decision, not
this chapter's to gate.
