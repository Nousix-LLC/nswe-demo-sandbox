# Release bar — home timeline & compose core loop (BAR-238..242)

The read-and-post loop is the product's reason to return: a signed-in person reads a timeline of their own and
followed chirps and composes and posts into it. These criteria hold that loop to a checkable release condition.
Each `BAR-*` states a condition someone who was not in the room can confirm against the live product; it
**references** the requirements it enforces rather than restating them. The authoritative requirements are in
`design/experience-design.md` (`REQ-UX-051..056`, all release-gating; `REQ-UX-057`, the navigable conversation
read, is non-gating and is not a basis here).

Fields per criterion: `id`, `statement`, `references` (≥1 `REQ-*`), `verification_method` (one of
`manual_user_check` | `automated_test` | `inspection` | `operational_check`), `proposed_stage`
(`usable_early` | `releasable` — this chapter's proposal; the screens synthesis and the UX and whole-bar
synthesis finalize one coherent line).

## Release-bar criteria

### BAR-238 — The home timeline shows own and followed chirps, newest first, in bounded pages
- **statement**: A signed-in person who opens the home destination sees a timeline carrying their own chirps and
  the chirps of the accounts they follow, ordered newest first, and the signed-in shell marks Home as the current
  destination. The timeline arrives as a bounded first page with a visible control to load older chirps; using
  that control brings in a further bounded page, and at no point does the product load the entire timeline in one
  request. Following at least one account that has posted, the person sees those chirps interleaved with their own
  in newest-first order.
- **references**: REQ-UX-051; REQ-PROD-002
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-239 — Catch-up brings new chirps in as a bounded step, and leaving a conversation keeps the reader's place
- **statement**: When chirps have been posted since the person last viewed the timeline, a catch-up control at the
  top of the list states how many new chirps are waiting and, when used, brings them in as a single bounded step
  that returns the reader to the newest chirps — not an open-ended scroll back through everything missed. Opening
  a chirp's conversation and returning to the timeline leaves the reader at the position they left, not reset to
  the top of the list.
- **references**: REQ-UX-052; REQ-PROD-002
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-240 — The timeline renders designed empty, error, and loading states, never a blank or an endless spinner
- **statement**: The home timeline shows a designed state for empty, for failure, and for loading in place of a
  blank region or an indefinite spinner. An account that follows no one and has posted nothing sees an empty state
  that explains why the timeline is empty and offers a route to Explore and to composing a first chirp. A failed
  first page shows a plain-language message with a retry in place of the list, visibly distinct from the empty
  state; a failed load-older or failed catch-up is shown at the boundary while the chirps already on screen stay
  loaded. A first load shows skeleton rows at the size of real chirp cards while the signed-in shell stays
  visible, and no region of the timeline continues to spin without resolving.
- **references**: REQ-UX-053; REQ-PROD-002
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-241 — Composing enforces the 280-character limit, and publishing never double-posts or loses a draft
- **statement**: The compose surface shows a remaining-character count that warns as the 280-character limit
  nears and marks the draft as over the limit once it is exceeded. The post action is not activatable while the
  draft is empty or over the limit, and an empty or over-limit submission reached by any path creates no chirp.
  While a publish is in flight the post action shows a busy state and the same draft cannot be submitted a second
  time; on success the chirp is published, the field clears, and a brief non-blocking confirmation is shown; on
  failure the draft text is kept exactly as written with an inline error and a retry, so the person can post again
  without retyping. No successful post is duplicated and no failed post loses its draft.
- **references**: REQ-UX-054, REQ-UX-055; REQ-PROD-001
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-242 — The one compose surface appears in its three placements with a placement-labelled action and an empty state
- **statement**: The compose surface is reachable inline at the top of the home timeline, as the Compose dialog
  (opened from the signed-in shell's compose affordance and directly at `/compose`), and in the reply position of
  a chirp's conversation screen, and it behaves the same way in each. In every placement an untouched field shows
  a placeholder prompt, a remaining-character count at the full 280 budget, and a disabled primary action; the
  action is labelled for its placement — "Post" when writing a chirp, "Reply" when answering one. Dismissing the
  Compose dialog with text still in the field and reopening it does not lose the draft.
- **references**: REQ-UX-056; REQ-PROD-001, REQ-PROD-003
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

## Coverage note — core-loop gating requirements → BAR

Every release-gating `REQ-UX-*` in the core-loop band (`051..056`, 6 gating) is referenced by at least one
`BAR-*` in `BAR-238..242`. The screens synthesis gate uses this map to assert core-loop gating coverage without
re-deriving the set.

| REQ-UX | Gating | Covered by | Topic |
|--------|--------|------------|-------|
| REQ-UX-051 | yes | BAR-238 | Home timeline: own + followed, newest first, bounded pages, load-older, Home current |
| REQ-UX-052 | yes | BAR-239 | Catch-up as a bounded step; keep reading position on return from a conversation |
| REQ-UX-053 | yes | BAR-240 | Designed empty, error, and loading states |
| REQ-UX-054 | yes | BAR-241 | 280-character limit enforced while composing, before submission |
| REQ-UX-055 | yes | BAR-241 | Publish locks against double-posting, confirms on success, keeps draft on failure |
| REQ-UX-056 | yes | BAR-242 | One compose surface in three placements, context-labelled action, empty state |
| REQ-UX-057 | no | — (not gated) | Navigable conversation read; rides non-gating REQ-PROD-004, not a basis for any BAR here |

Clustering: the id budget is 5 ids for 6 gating requirements. `REQ-UX-054` and `REQ-UX-055` are the two halves
of one checkable condition — you cannot post something the product forbids, and a post is neither duplicated nor
lost — so they share `BAR-241`. The other four gating requirements map one-to-one.

## Staging-proposal notes (for the screens synthesis gate)

These record why each `proposed_stage` was chosen; the synthesis gate reconciles them into one coherent per-`BAR`
stage across the screens chapters.

- **BAR-238 — usable_early.** Reading own and followed chirps newest-first is the irreducible core; there is no
  product to return to without it.
- **BAR-241 — usable_early.** The primary action is posting a chirp; a build that lets a person post an
  over-limit or empty chirp, double-post, or lose a draft on failure is not usable as a first version. The
  live-count and warning appearance are observable manually, but the gating guarantees (no post by a forbidden
  path, no duplicate, no lost draft) are invariants best pinned by repository tests — hence `automated_test`.
- **BAR-239 — releasable.** The timeline reads without catch-up and without position restoration; both are
  refinements a first usable version can lack and a release should carry.
- **BAR-240 — releasable.** The full set of designed states is a release condition. The early-critical minimum
  inside it is the non-blank empty state (a brand-new timeline must not be a blank); the synthesis gate may split
  that minimum forward if it stages the states separately.
- **BAR-242 — releasable.** A usable-early build needs the compose surface in its primary placements (inline and
  the Compose dialog), which `BAR-241` already exercises; the three-placement consistency — including the reply
  slot, which depends on the conversation screen — is release completeness.
