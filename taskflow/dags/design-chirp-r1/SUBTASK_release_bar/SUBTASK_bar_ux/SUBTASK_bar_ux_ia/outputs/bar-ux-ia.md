# Release bar — experience area: information architecture & interaction model (BAR-200..214)

Release-bar criteria for the IA & interaction slice of the experience design. Each `BAR-*` states a
release condition a person who was not in the room can check against the live product, and names the
release-gating `REQ-UX-*` it enforces. One `BAR-*` may enforce more than one related requirement; it is
listed against every requirement it holds. `proposed_stage` is this area's proposal (`usable_early` = holds
in the first usable version; `releasable` = required for release on top of that); the whole-product line is
reconciled downstream. Requirements are referenced by id and not restated here — their statements and
acceptance criteria live in `design/experience-design.md`.

Gating set covered: `REQ-UX-001..014, 016, 017, 018` (17). Not covered (non-gating, excluded as sole basis):
`REQ-UX-015` (interlinking of auth screens — a convenience a first release may omit while recovery stays
reachable from help) and `REQ-UX-019` (notifications entry/indicator — ships with notifications, which the
bar does not gate).

---

## BAR-200
- **statement**: With no session, every signed-out screen (at minimum the landing and a public profile
  opened by direct link) carries the chirp wordmark, a Sign in entry, a prominent Sign up entry, and
  footer access to the rules and to help; from each, a person can act (sign in, sign up, read the rules,
  reach help) without first being signed in and without reaching a dead end.
- **references**: REQ-UX-001
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-201
- **statement**: Signed in, a persistent shell exposes Home, Explore, Notifications, Profile, Settings, and
  a Compose affordance, and all six are reachable from every signed-in screen — verified from the timeline,
  a profile, a conversation, and a settings sub-section — without using the browser back control.
- **references**: REQ-UX-002
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-202
- **statement**: On every screen the product shows where the person is: navigating to Home, Explore,
  Notifications, Profile, and a settings sub-section in turn, the active primary-nav destination is visibly
  marked and the browser tab title (and the screen's main heading) names the current screen.
- **references**: REQ-UX-003
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-203
- **statement**: Every screen the product presents, signed-out and signed-in, matches a published
  screen-inventory entry (route, exactly one archetype, declared auth state); no presented screen is absent
  from the inventory, and every signed-in-reachable inventory screen can in fact be reached.
- **references**: REQ-UX-004
- **verification_method**: inspection
- **proposed_stage**: releasable

## BAR-204
- **statement**: Signed in and starting from the home timeline, a person reaches each of compose, their own
  profile, notifications, settings, explore, help, and the rules in no more than two steps through the
  product, without holding an external link.
- **references**: REQ-UX-005
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-205
- **statement**: A public profile and an individual chirp's conversation each resolve from a stable,
  shareable URL that, opened directly in a fresh browser context, lands on that exact profile / that exact
  chirp — not on a generic home or a redirect to sign-in for public content.
- **references**: REQ-UX-006
- **verification_method**: automated_test
- **proposed_stage**: usable_early

## BAR-206
- **statement**: Opening a signed-in-only URL (for example a settings sub-section) with no session routes
  the person to sign-in, and after a successful sign-in lands them on that originally requested screen
  rather than on a default screen such as the home timeline.
- **references**: REQ-UX-007
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

## BAR-207
- **statement**: An action taken with an expired or invalid session (for example opening the timeline or
  submitting a drafted chirp) routes the person to sign-in with the reason stated, does not lose their
  in-progress input, and returns them to where they were after they sign back in.
- **references**: REQ-UX-008
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

## BAR-208
- **statement**: The browser back control returns to the previous screen without re-submitting the prior
  action and without losing the person's place in a scrolled timeline, and a dialog counts as one step so
  that back dismisses it by closing it; pressing back after posting a chirp does not re-post it.
- **references**: REQ-UX-009
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

## BAR-209
- **statement**: A list with more items than one page loads a bounded first page rather than every item at
  once, offers an explicit way to load older items, and — on the timeline — offers a way to pull in chirps
  posted since the person opened it.
- **references**: REQ-UX-010
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-210
- **statement**: Every irreversible or destructive action — delete account, delete a chirp, block or mute,
  end a session, sign out of all sessions — presents an explicit confirmation that names the consequence
  and offers a cancel before it proceeds, and cancelling changes nothing; the account-deletion confirmation
  additionally states what is and is not retained and points to data export.
- **references**: REQ-UX-011
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

## BAR-211
- **statement**: Every completed action (for example publishing a chirp, following an account, saving a
  setting) shows brief, non-blocking confirmation, and every failed action is shown at the point it was
  taken — against the field for a form, against the control for an in-place action — with enough to
  understand and retry; no action completes or fails silently.
- **references**: REQ-UX-012
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-212
- **statement**: A signed-in person can start composing a chirp from any screen through a persistent
  compose affordance without navigating away first (verified from the timeline, a profile, and
  notifications), and opening the dedicated compose URL directly opens the compose surface.
- **references**: REQ-UX-013
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-213
- **statement**: A completed sign-up establishes the session and lands the person on onboarding — not on a
  repeated sign-in prompt and not on a blank timeline; and signing out ends the session, returns the person
  to the signed-out landing, and leaves the browser back control unable to re-expose a protected screen's
  content.
- **references**: REQ-UX-014, REQ-UX-016
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

## BAR-214
- **statement**: Account-level choices live under one settings area with labelled sub-sections (edit
  profile, account & contact, notification preferences, sessions & devices, blocked & muted, export, delete),
  each opening directly by its own URL and each returning to the settings hub; and the rules/terms and a
  user-facing help & support entry are reachable from both the signed-out shell and the signed-in shell.
- **references**: REQ-UX-017, REQ-UX-018
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

---

## Coverage note — IA-area release-gating `REQ-UX-*` → `BAR-*`

Every release-gating requirement in this band (`REQ-UX-001..014, 016, 017, 018`) is enforced by at least one
`BAR-*` in the `BAR-200..214` range. The synthesis gate can assert IA-area `UX_GATING_REQ_COVERAGE` directly
from this table without re-deriving the gating set.

| release-gating REQ-UX | covered by | concern |
|---|---|---|
| REQ-UX-001 | BAR-200 | signed-out shell, never dead-ends |
| REQ-UX-002 | BAR-201 | signed-in shell exposes every primary destination |
| REQ-UX-003 | BAR-202 | current location always indicated |
| REQ-UX-004 | BAR-203 | built from the published screen inventory |
| REQ-UX-005 | BAR-204 | every required surface reachable (≤2 steps, no external link) |
| REQ-UX-006 | BAR-205 | profiles & chirps addressable and shareable |
| REQ-UX-007 | BAR-206 | auth-gated routing returns to the requested screen |
| REQ-UX-008 | BAR-207 | expired session intercepted, explained, recovered |
| REQ-UX-009 | BAR-208 | predictable browser back/forward |
| REQ-UX-010 | BAR-209 | bounded-page list loading with catch-up |
| REQ-UX-011 | BAR-210 | destructive actions confirmed |
| REQ-UX-012 | BAR-211 | result of every action is shown |
| REQ-UX-013 | BAR-212 | compose reachable from anywhere, and addressable |
| REQ-UX-014 | BAR-213 | sign-up lands in the product, onboarding first |
| REQ-UX-016 | BAR-213 | sign-out returns to the signed-out shell, no leak-back |
| REQ-UX-017 | BAR-214 | settings groups addressable account-level choices |
| REQ-UX-018 | BAR-214 | rules and help reachable from both shells |

Non-gating in this band and deliberately not minted as a `BAR-*` basis: `REQ-UX-015` (auth-screen
interlinking — a first release may omit the cross-links while recovery stays reachable from help) and
`REQ-UX-019` (notifications entry and unseen-activity indicator — ships with notifications, which the bar
does not gate). Both may be referenced for context elsewhere but are not the sole basis of any `BAR-*` here.
