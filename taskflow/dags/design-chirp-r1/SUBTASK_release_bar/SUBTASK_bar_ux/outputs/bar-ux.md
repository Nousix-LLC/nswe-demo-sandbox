# Release bar — experience area (`BAR-200..299`)

The experience-area slice of chirp's whole-product release bar. Each `BAR-*` states a release condition a
person who was not in the design room can check against the live product, and names the release-gating
`REQ-UX-*` from `design/experience-design.md` it enforces. A criterion states what must be observably true at
release; it does not restate the requirement or prescribe how the product is built. One `BAR-*` may enforce
several closely related requirements and is listed against each.

This fragment consolidates the five experience sub-areas:

| Sub-area | `BAR-*` range | Gating `REQ-UX-*` held |
|----------|---------------|------------------------|
| Information architecture & interaction model | `BAR-200..214` | `REQ-UX-001..014, 016, 017, 018` (17) |
| Visual language & component system | `BAR-215..229` | `REQ-UX-020, 021, 022, 025..029, 031..039` (17) |
| Screens & flows | `BAR-230..264` | `REQ-UX-040..056, 058..063, 065..070, 073..077, 079, 082..089` (43) |
| Responsive layout | `BAR-265..274` | `REQ-UX-090..099` (10) |
| Accessibility | `BAR-275..294` | `REQ-UX-100..104, 106..119` (19) |
| Cross-cutting | `BAR-295..299` | — (unused; see the closing note) |

Every release-gating `REQ-UX-*` (106 of the 119; the other 13 are `release_gating: false` and are not held
here) is referenced by at least one `BAR-*` below; the coverage note at the end records the full mapping.

**Fields.** Each block carries the frozen field set: `id`, `statement`, `references` (≥1 `REQ-UX-*`, and any
requirement it composes with), `verification_method` (one of `manual_user_check`, `automated_test`,
`inspection`, `operational_check`), and `stage` (`usable_early` = holds in the first usable version a person
could adopt for the core loop; `releasable` = required for the public release on top of that). The stage shown
is the reconciled experience-area view; the whole-product usable-early-vs-releasable line is owned by the
release-bar synthesis and may still move a criterion for cross-area coherence.

---

## Information architecture & interaction model — `BAR-200..214`

### BAR-200
- **statement**: With no session, every signed-out screen (at minimum the landing and a public profile opened
  by direct link) carries the chirp wordmark, a Sign in entry, a prominent Sign up entry, and footer access to
  the rules and to help; from each, a person can act (sign in, sign up, read the rules, reach help) without
  first being signed in and without reaching a dead end.
- **references**: REQ-UX-001
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-201
- **statement**: Signed in, a persistent shell exposes Home, Explore, Notifications, Profile, Settings, and a
  Compose affordance, and all six are reachable from every signed-in screen — verified from the timeline, a
  profile, a conversation, and a settings sub-section — without using the browser back control.
- **references**: REQ-UX-002
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-202
- **statement**: On every screen the product shows where the person is: navigating to Home, Explore,
  Notifications, Profile, and a settings sub-section in turn, the active primary-nav destination is visibly
  marked and the browser tab title (and the screen's main heading) names the current screen.
- **references**: REQ-UX-003
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-203
- **statement**: Every screen the product presents, signed-out and signed-in, matches a published
  screen-inventory entry (route, exactly one archetype, declared auth state); no presented screen is absent
  from the inventory, and every signed-in-reachable inventory screen can in fact be reached.
- **references**: REQ-UX-004
- **verification_method**: inspection
- **stage**: releasable

### BAR-204
- **statement**: Signed in and starting from the home timeline, a person reaches each of compose, their own
  profile, notifications, settings, explore, help, and the rules in no more than two steps through the
  product, without holding an external link.
- **references**: REQ-UX-005
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-205
- **statement**: A public profile and an individual chirp's conversation each resolve from a stable, shareable
  URL that, opened directly in a fresh browser context, lands on that exact profile / that exact chirp — not
  on a generic home or a redirect to sign-in for public content.
- **references**: REQ-UX-006
- **verification_method**: automated_test
- **stage**: usable_early

### BAR-206
- **statement**: Opening a signed-in-only URL (for example a settings sub-section) with no session routes the
  person to sign-in, and after a successful sign-in lands them on that originally requested screen rather than
  on a default screen such as the home timeline.
- **references**: REQ-UX-007
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-207
- **statement**: An action taken with an expired or invalid session (for example opening the timeline or
  submitting a drafted chirp) routes the person to sign-in with the reason stated, does not lose their
  in-progress input, and returns them to where they were after they sign back in.
- **references**: REQ-UX-008
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-208
- **statement**: The browser back control returns to the previous screen without re-submitting the prior
  action and without losing the person's place in a scrolled timeline, and a dialog counts as one step so that
  back dismisses it by closing it; pressing back after posting a chirp does not re-post it.
- **references**: REQ-UX-009
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-209
- **statement**: A list with more items than one page loads a bounded first page rather than every item at
  once, offers an explicit way to load older items, and — on the timeline — offers a way to pull in chirps
  posted since the person opened it.
- **references**: REQ-UX-010
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-210
- **statement**: Every irreversible or destructive action — delete account, delete a chirp, block or mute, end
  a session, sign out of all sessions — presents an explicit confirmation that names the consequence and
  offers a cancel before it proceeds, and cancelling changes nothing; the account-deletion confirmation
  additionally states what is and is not retained and points to data export.
- **references**: REQ-UX-011
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-211
- **statement**: Every completed action (for example publishing a chirp, following an account, saving a
  setting) shows brief, non-blocking confirmation, and every failed action is shown at the point it was taken
  — against the field for a form, against the control for an in-place action — with enough to understand and
  retry; no action completes or fails silently.
- **references**: REQ-UX-012
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-212
- **statement**: A signed-in person can start composing a chirp from any screen through a persistent compose
  affordance without navigating away first (verified from the timeline, a profile, and notifications), and
  opening the dedicated compose URL directly opens the compose surface.
- **references**: REQ-UX-013
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-213
- **statement**: A completed sign-up establishes the session and lands the person on onboarding — not on a
  repeated sign-in prompt and not on a blank timeline; and signing out ends the session, returns the person to
  the signed-out landing, and leaves the browser back control unable to re-expose a protected screen's content.
- **references**: REQ-UX-014, REQ-UX-016
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-214
- **statement**: Account-level choices live under one settings area with labelled sub-sections (edit profile,
  account & contact, notification preferences, sessions & devices, blocked & muted, export, delete), each
  opening directly by its own URL and each returning to the settings hub; and the rules/terms and a
  user-facing help & support entry are reachable from both the signed-out shell and the signed-in shell.
- **references**: REQ-UX-017, REQ-UX-018
- **verification_method**: manual_user_check
- **stage**: releasable

---

## Visual language & component system — `BAR-215..229`

### BAR-215 — Unrelated screens share one visual treatment
- **statement**: On three screens of different archetypes on the live product (for example the home timeline,
  a profile, and a settings sub-section), body text is the same size and leading, the gutters and spacing
  rhythm match, buttons share one shape and one primary colour, and no screen introduces a colour or control
  style absent from the others.
- **references**: REQ-UX-020
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-216 — Reading text is legible and hierarchy is visible
- **statement**: On the live product, chirp and reading text renders at no less than 15px with visibly
  generous line spacing; on any screen the main heading is visibly larger and heavier than its body text, and
  meta text (timestamps, handles) is visibly quieter than body text.
- **references**: REQ-UX-021
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-217 — Colour contrast meets WCAG 2.1 AA, measured
- **statement**: On the live product, sample body text, secondary text, link text, primary-button text, and a
  field border and measure each with a contrast tool: normal text reaches ≥ 4.5:1, large text ≥ 3:1, and
  control and meaningful-icon boundaries ≥ 3:1. The measurement passes in each theme the product ships.
- **references**: REQ-UX-022
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-218 — Every keyboard-reachable control shows a visible focus indicator
- **statement**: Using only the keyboard on the live product, tabbing through a screen's links, buttons,
  fields, and menu items shows a distinct focus indicator on each that stands out from its surroundings, and
  no focusable control takes focus without a visible indicator.
- **references**: REQ-UX-025
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-219 — Spacing, grid, and reading measure are consistent and bounded
- **statement**: On the live product, the reading column (timeline, conversation, profile chirps, a form) is
  held to a bounded measure on a wide window rather than spanning the whole width; on a phone viewport the same
  content fills the width with a consistent edge gutter; and the spacing between items is visibly uniform
  within and across these screens.
- **references**: REQ-UX-026
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-220 — Overlapping surfaces stack in a consistent order
- **statement**: On the live product, opening a menu places it above content; opening a dialog places it above
  content on a dimmed scrim with the menu not showing through; triggering a toast places it above the dialog.
  At no point does a lower layer render on top of a higher one.
- **references**: REQ-UX-027
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-221 — Icons are consistent and meaning never rides on colour alone
- **statement**: On the live product, icons come from one consistent set; the current primary-nav destination
  reads as active by more than colour, confirmed still identifiable in greyscale or a colour-blind simulation;
  and every icon-only control (compose, like, menu) exposes an accessible name to a screen reader and a label
  on hover.
- **references**: REQ-UX-028
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-222 — Motion is bounded and respects reduced-motion
- **statement**: On the live product, opening and closing a menu and a dialog and triggering a toast each
  complete a brief transition (well under half a second) that settles, with nothing animating or blinking
  continuously apart from a bounded loading indicator; with the system reduce-motion setting on, the same
  actions remove or reduce animation to a short fade and no information is lost.
- **references**: REQ-UX-029
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-223 — One voice, with plain and actionable errors
- **statement**: On the live product, action buttons across several screens read as sentence-case verbs (for
  example "Post", "Follow", "Save changes") rather than "OK"/"Submit" or Title Case; and a forced error (an
  invalid form entry, then a failed submit) shows a plain-language message with a way forward and no raw error
  code, stack text, or internal identifier.
- **references**: REQ-UX-032
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-224 — Screens are assembled from the named components, and components come from the tokens
- **statement**: On three screens of different archetypes on the live product, a chirp, buttons, text fields,
  and error messages each render from one shared treatment with no bespoke control standing in for a library
  component; and inspecting a chirp card, a primary button, a text field, and a dialog in each shipped theme
  shows colours matching the token roles (a primary action is the one primary colour, a destructive one the
  danger colour), text sizes matching the type scale, and no colour or size that is absent from the token set.
- **references**: REQ-UX-033, REQ-UX-034
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-225 — The chirp card and compose box hold the core-loop contract
- **statement**: On the live product, typing past the character limit in compose turns the counter to the
  danger treatment and disables Post; an empty draft leaves Post disabled and posts nothing; a valid chirp
  posts and appears as a chirp card showing avatar, author, handle, relative time, text, and the
  like / reply / more-actions row; and liking a chirp shows a filled icon and a "Liked" label together, still
  identifiable as liked in greyscale.
- **references**: REQ-UX-035
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-226 — Empty, loading, and failure states carry a designed treatment
- **statement**: On the live product, a brand-new account's empty timeline shows an explanatory block with a
  next step rather than a blank area; a list while loading shows skeleton rows at the real item size rather
  than a spinner on a blank screen; a forced page-load failure shows an inline message with a retry in place
  of the missing items while keeping any items already shown; and a failed action shows an inline error in the
  product's danger styling at the point of action. None of these renders a blank area, a frozen screen, or a
  raw failure.
- **references**: REQ-UX-031, REQ-UX-036
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-227 — Forms validate inline at the field, in plain language
- **statement**: On the live product sign-up, submitting a handle already in use shows a plain-language error
  against the handle field naming the handle (not in a distant summary and not as a code); submitting a
  mis-formatted handle shows a field-level validation error that explains the rule; and while a handle's
  availability is being checked the field shows a pending state rather than flicking prematurely to valid or
  invalid.
- **references**: REQ-UX-037
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-228 — Consequential actions are confirmed before they happen
- **statement**: On the live product, initiating deletion of a chirp, blocking an account, and deleting the
  account each present a confirmation that names what will happen and offers a plain cancel, and nothing
  changes on cancel; the account-deletion confirmation additionally states what is and is not retained and
  points to data export before proceeding.
- **references**: REQ-UX-038
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-229 — The result of every action is shown through the feedback components
- **statement**: On the live product, publishing a chirp, following an account, and saving a setting each show
  a brief, non-blocking confirmation; an action in flight shows its control in a busy state that cannot be
  re-triggered; and a forced in-place failure (acting while offline, or a transient server error while
  posting) shows the failure at the control with a way to retry and does not lose the drafted text.
- **references**: REQ-UX-039
- **verification_method**: manual_user_check
- **stage**: usable_early

---

## Screens & flows — `BAR-230..264`

### BAR-230
- **statement**: With no session, opening the site root reaches a Landing that says what chirp is and shows
  both a Sign up and a Sign in action, each reachable without first signing in. Where a public sample is
  served it shows real public chirps; where none is served the Landing still explains chirp and offers both
  actions rather than a blank area.
- **references**: REQ-UX-040 (REQ-PROD-030, REQ-PROD-031)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-231
- **statement**: The Sign up screen collects a handle, a display name, an optional bio marked optional, a
  credential, and a point of contact — and no fields beyond these — and on submit with valid values creates
  the account and signs the person in. The contact is shown as pending verification and is not treated as
  confirmed until it is verified.
- **references**: REQ-UX-041, REQ-UX-043 (REQ-PROD-008, REQ-PROD-012, REQ-PROD-031)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-232
- **statement**: On the Sign up screen a handle that is already taken, or that breaks the rule (more than 15
  characters, or anything other than letters, numbers, or underscores), is reported inline against the handle
  field so the person can fix it before submitting, and a valid unused handle resolves to accepted. The check
  does not disclose which other handles exist beyond the conflict it reports.
- **references**: REQ-UX-042 (REQ-PROD-009)
- **verification_method**: automated_test
- **stage**: usable_early

### BAR-233
- **statement**: Signing in requires the credential set at sign-up or recovery — a known handle alone never
  grants a session. A handle that matches no account returns a not-found result with a path to Sign up; a real
  handle with a wrong credential returns a failed sign-in the person can retry or recover from, with a path to
  Recover access. Neither result reveals account existence beyond what a public profile already shows, and
  neither shows a system code.
- **references**: REQ-UX-044, REQ-UX-045 (REQ-PROD-010, REQ-PROD-011)
- **verification_method**: automated_test
- **stage**: usable_early

### BAR-234
- **statement**: A person who cannot sign in can start recovery themselves from a Recover access screen that
  runs through the account's verified contact. Submitting a contact returns the same neutral acknowledgement
  whether or not it matches an account, so the response discloses no account existence. Following a valid
  recovery step opens a Set new credential screen, and after setting a new credential the person is routed to
  Sign in and can sign in with it. An expired or already-used recovery link is explained with a path back to
  Recover access rather than a dead end.
- **references**: REQ-UX-046, REQ-UX-047 (REQ-PROD-013, REQ-PROD-012)
- **verification_method**: automated_test
- **stage**: releasable

### BAR-235
- **statement**: Signing out is confirmed before it proceeds; the confirmation names the consequence and
  offers both a cancel and an option to end sessions on all other devices. Confirming ends the current session
  on the server — the prior session can no longer be used — and lands the person on the signed-out Landing.
  Cancelling changes nothing. A sign-out that fails is reported and leaves the person signed in rather than
  appearing to succeed.
- **references**: REQ-UX-048 (REQ-PROD-014)
- **verification_method**: automated_test
- **stage**: usable_early

### BAR-236
- **statement**: Each of the Landing, Sign up, Sign in, Recover access, Set new credential, and Sign out
  surfaces presents a designed state for empty, loading, and error — a field-level message, a busy control, a
  skeleton, or an explained error with a next step — rather than a blank area, a hang, or a silent failure.
  Where a state does not apply to a surface, that is stated rather than left undesigned.
- **references**: REQ-UX-049 (REQ-PROD-033, REQ-PROD-034)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-237
- **statement**: A completed sign-up lands the person on the onboarding screen, not a sign-in prompt or a
  blank page. A person routed from a signed-in-only screen to Sign in lands back on the screen they asked for
  after signing in. After signing out, pressing back does not show the protected screen's content. (The
  three-way links among Sign in, Sign up, and Recover access ride the non-gating REQ-UX-015 and are not part
  of this release condition; a first release may omit them provided Recover access stays reachable from
  Help & support.)
- **references**: REQ-UX-050 (REQ-PROD-032, REQ-PROD-014)
- **verification_method**: automated_test
- **stage**: releasable

### BAR-238
- **statement**: A signed-in person who opens the home destination sees a timeline carrying their own chirps
  and the chirps of the accounts they follow, ordered newest first, and the signed-in shell marks Home as the
  current destination. The timeline arrives as a bounded first page with a visible control to load older
  chirps; using that control brings in a further bounded page, and at no point does the product load the
  entire timeline in one request. Following at least one account that has posted, the person sees those chirps
  interleaved with their own in newest-first order.
- **references**: REQ-UX-051 (REQ-PROD-002)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-239
- **statement**: When chirps have been posted since the person last viewed the timeline, a catch-up control at
  the top of the list states how many new chirps are waiting and, when used, brings them in as a single
  bounded step that returns the reader to the newest chirps — not an open-ended scroll back through everything
  missed. Opening a chirp's conversation and returning to the timeline leaves the reader at the position they
  left, not reset to the top of the list.
- **references**: REQ-UX-052 (REQ-PROD-002)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-240
- **statement**: The home timeline shows a designed state for empty, for failure, and for loading in place of
  a blank region or an indefinite spinner. An account that follows no one and has posted nothing sees an empty
  state that explains why the timeline is empty and offers a route to Explore and to composing a first chirp.
  A failed first page shows a plain-language message with a retry in place of the list, visibly distinct from
  the empty state; a failed load-older or failed catch-up is shown at the boundary while the chirps already on
  screen stay loaded. A first load shows skeleton rows at the size of real chirp cards while the signed-in
  shell stays visible, and no region of the timeline continues to spin without resolving.
- **references**: REQ-UX-053 (REQ-PROD-002)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-241
- **statement**: The compose surface shows a remaining-character count that warns as the 280-character limit
  nears and marks the draft as over the limit once it is exceeded. The post action is not activatable while
  the draft is empty or over the limit, and an empty or over-limit submission reached by any path creates no
  chirp. While a publish is in flight the post action shows a busy state and the same draft cannot be
  submitted a second time; on success the chirp is published, the field clears, and a brief non-blocking
  confirmation is shown; on failure the draft text is kept exactly as written with an inline error and a
  retry, so the person can post again without retyping. No successful post is duplicated and no failed post
  loses its draft.
- **references**: REQ-UX-054, REQ-UX-055 (REQ-PROD-001)
- **verification_method**: automated_test
- **stage**: usable_early

### BAR-242
- **statement**: The compose surface is reachable inline at the top of the home timeline, as the Compose
  dialog (opened from the signed-in shell's compose affordance and directly at `/compose`), and in the reply
  position of a chirp's conversation screen, and it behaves the same way in each. In every placement an
  untouched field shows a placeholder prompt, a remaining-character count at the full 280 budget, and a
  disabled primary action; the action is labelled for its placement — "Post" when writing a chirp, "Reply"
  when answering one. Dismissing the Compose dialog with text still in the field and reopening it does not
  lose the draft.
- **references**: REQ-UX-056 (REQ-PROD-001, REQ-PROD-003)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-243
- **statement**: Signed in on a chirp's conversation, a person can write a reply within the character limit
  and publish it from the conversation's reply control; the published reply then appears in that conversation
  shown as answering the chirp, and its publication is confirmed. Attempting to reply to a chirp that no
  longer exists reports not-found at the reply control and keeps the typed draft, rather than appearing to
  send. Opened without a session, the conversation presents a visible way to sign in or sign up in place of
  the reply control, not a dead or silent one.
- **references**: REQ-UX-058 (REQ-PROD-003)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-244
- **statement**: A chirp's like control toggles between not-liked and liked, with the liked state
  distinguished by more than colour (a filled heart and a "Liked" label). Liking an already-liked chirp, or
  reloading the screen, does not raise the count a second time; unliking returns the count to its earlier
  value. When a like or unlike cannot be completed, the control returns to its prior state, the count is left
  unchanged (it never shows a like that did not take), and the failure is reported at the control with a way
  to retry. The control looks and behaves the same wherever the chirp is shown — in the timeline, in its
  conversation, and on a profile.
- **references**: REQ-UX-059 (REQ-PROD-005)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-245
- **statement**: On another person's profile header or in a person row, the follow control toggles between
  "Follow" and "Following"; following the same account again, or reloading, leaves exactly one follow in place
  with the control reading "Following", and unfollowing returns it to "Follow". A person's own identity never
  presents a Follow control — the own-identity action is "Edit profile" — so a self-follow cannot be started,
  and any attempt is refused and shown at the control. When a follow or unfollow cannot be completed, the
  control returns to its prior label, any follower count is unchanged, and the failure is reported at the
  control with a way to retry. The control looks and behaves the same wherever it appears (profile header and
  person rows).
- **references**: REQ-UX-060 (REQ-PROD-006)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-246
- **statement**: A person's profile at its handle URL shows their avatar, display name, handle, bio, and
  follower and following counts, above that person's own chirps in newest-first bounded pages with a way to
  load older ones, and loads both without a session and with one; signed in, the header also carries the
  follow control. When the signed-in owner opens their own profile, they see the same public face a visitor
  sees, with an "Edit profile" entry in place of the follow control that opens the edit-profile screen, and no
  follow control is shown on their own profile.
- **references**: REQ-UX-061, REQ-UX-062 (REQ-PROD-007)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-247
- **statement**: A profile's follower and following counts open the followers list and the following list,
  each at its own URL. Each list shows one person per row with enough to recognise the account (avatar,
  display name, handle, bio) in a bounded page with a way to load more, a labelled way back to the profile,
  and — for a signed-in viewer — a follow control on each row. Each list's URL, opened directly, lands on that
  list.
- **references**: REQ-UX-063 (REQ-PROD-007, REQ-PROD-006)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-248
- **statement**: After a fresh sign-up, a brand-new account lands on the onboarding screen and sees, in plain
  language, why its timeline is empty and at least one working control that opens compose to write a first
  chirp (and, wherever discovery is present, a control to find people to follow). The explanation and the
  compose route appear immediately and stay usable while any suggestions preview is still loading — shown as
  placeholders, not a blank region — and after that preview fails or comes back empty. The screen is never a
  blank page and never leaves the person without a next step.
- **references**: REQ-UX-065, REQ-UX-066 (REQ-PROD-032, REQ-PROD-033)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-249
- **statement**: A signed-in person can reach edit profile from the settings hub and from the edit action on
  their own profile, change their display name and bio, and save; the saved values then show on their profile.
  An empty required display name or a rejected value is reported against the field in plain words and no save
  is made; a save that fails is reported at the form with the person's edited values still present so they can
  retry; a save that succeeds is confirmed. The screen never reports success or failure silently and never
  shows a raw system or error code.
- **references**: REQ-UX-067, REQ-UX-068 (REQ-PROD-016, REQ-PROD-033, REQ-PROD-034)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-250
- **statement**: A signed-in person opening settings sees a labelled row for every account section in the
  release — edit profile, account & contact, sessions & devices, blocked & muted, export your data, and
  delete account (the notification-preferences row appears only where notifications are in the release). Each
  row opens its section both by selection and by entering the section's own URL directly in a fresh tab, and
  each section offers a labelled way back to the hub that works alongside the browser back control. The
  delete-account row is shown as destructive and opens a confirmation rather than deleting when selected. If
  the account summary fails to load, every section row is still reachable.
- **references**: REQ-UX-069 (REQ-PROD-017)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-251
- **statement**: On the account & contact screen a signed-in person sees their current point of contact with a
  status of either "Verified" or "Not verified yet". They can change the contact and save; the change is
  confirmed, the new contact shows as not-yet-verified, and the screen offers a step that confirms the person
  controls it before it is used for account recovery. An unverified contact is presented as a caution, not an
  error, and is not treated as verified until that step is completed. A failed save is shown against the
  contact field with the typed value preserved for retry.
- **references**: REQ-UX-070 (REQ-PROD-012, REQ-PROD-017)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-252
- **statement**: A signed-in person opening sessions & devices sees every place the account is currently
  signed in, each with enough to recognise it — device and browser, approximate location, last-active time —
  and the current session marked. Ending another session goes through a confirmation that names the effect;
  after confirming, that session leaves the list and the next action attempted from the ended session on its
  own device is refused and requires a fresh sign-in.
- **references**: REQ-UX-073 (REQ-PROD-017, REQ-PROD-014)
- **verification_method**: operational_check
- **stage**: releasable

### BAR-253
- **statement**: A signed-in person can sign out from sessions & devices through a confirmation that, where
  the account is signed in elsewhere, offers to end those other sessions too. After sign-out the person is on
  the signed-out landing; the browser back control does not re-expose any protected screen; and replaying the
  signed-out session's request is refused, so the next person at that device is not signed in as them.
- **references**: REQ-UX-074 (REQ-PROD-014)
- **verification_method**: operational_check
- **stage**: usable_early

### BAR-254
- **statement**: From the export screen a signed-in person sees what the export contains and a single request
  action. After requesting, the screen shows a preparing state rather than freezing or blanking, and when
  ready offers a way to download the file; the downloaded file opens outside chirp and contains the person's
  chirps, their profile, and who they follow. A preparation that fails is explained in plain words with a
  retry, and no broken file is offered.
- **references**: REQ-UX-075 (REQ-PROD-019)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-255
- **statement**: The delete-account confirmation, shown before anything is deleted, states plainly that the
  account and its chirps are removed and cannot be recovered, shows what is and is not retained and what
  happens to the handle (matching the product's stated deletion outcome), and points the person to export
  their data first. The delete action stays unavailable until the person gives the explicit confirmation it
  asks for. Cancelling at any point returns to settings with the account and its content unchanged and still
  able to sign in. Giving the confirmation and deleting signs the person out to the signed-out landing, after
  which the account can no longer sign in and the browser back control does not re-expose the deleted
  account's screens.
- **references**: REQ-UX-076, REQ-UX-077 (REQ-PROD-020, REQ-PROD-021, REQ-PROD-022)
- **verification_method**: operational_check
- **stage**: releasable

### BAR-256
- **statement**: Signed in, a person can open the report action from both a chirp's and an account's
  more-actions menu, choose a reason, add optional detail, and submit, and sees an in-product confirmation
  that the report was received; and when no reason is chosen the submit control does not send the report. No
  report path ends in a silent no-op.
- **references**: REQ-UX-079 (REQ-PROD-025, REQ-PROD-026)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-257
- **statement**: From both the signed-out and the signed-in shell, a person can reach a Rules & terms screen
  that lists the product's rules as named categories; and the reasons offered in the report action correspond
  to those same named categories, so a submitted report points at a stated rule rather than an unlabelled
  choice.
- **references**: REQ-UX-083 (REQ-PROD-026)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-258
- **statement**: A Help & support entry is reachable with no session from the signed-out shell and, signed in,
  from the account menu; from it a person can reach the recover-access path ("Can't get in?") and a way to
  contact the operator ("Contact support") for what self-service does not cover.
- **references**: REQ-UX-082 (REQ-PROD-028, REQ-PROD-013)
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-259
- **statement**: Opening an address that does not resolve — a mistyped path, a deleted chirp, an unavailable
  account — shows a not-found screen that states the resource is missing (consistent with the in-place
  tombstone used elsewhere), reveals no private detail about a removed or restricted resource, and offers a
  route to a known place (the home timeline when signed in, the landing when signed out) rather than a broken
  page.
- **references**: REQ-UX-084 (REQ-PROD-033)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-260
- **statement**: On each surface in this area a person can force an empty result, a failed load, and a first
  load and sees, respectively, an explained empty treatment carrying at least one next step (never a blank
  region), a distinct "couldn't load — try again" treatment with a retry, and a loading treatment — with the
  empty treatment and the failed treatment visibly different from each other; a surface to which one of these
  states does not apply says so rather than showing nothing. Checked across, for example, Notifications, the
  report and block/mute dialogs on a failed submit (the dialog stays open with its input preserved and an
  inline error), the blocked & muted screen when empty, a brand-new home timeline, and an empty followers
  list.
- **references**: REQ-UX-085, REQ-UX-086 (REQ-PROD-033, REQ-PROD-034)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-261
- **statement**: On a slow connection a first load of a content surface shows skeletons sized to the real
  content — not a spinner on a blank page — while the persistent navigation frame stays visible; an
  incremental load, such as loading older items, shows a bounded indicator at the point of the action while
  the already-loaded content stays on screen; and a load that cannot resolve stops and becomes an error with a
  retry rather than spinning without end.
- **references**: REQ-UX-087 (REQ-PROD-033)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-262
- **statement**: A person who triggers a field error (for example a taken handle at sign-up), a failed
  in-place action (for example a like or follow that fails), and a failed list page sees in each case a
  plain-language message at the point of the problem — no system or error code, never a silent no-op and never
  a blank — with a way to retry or correct and their input preserved; an optimistic in-place action that fails
  reverts to its prior state rather than showing a result that did not happen.
- **references**: REQ-UX-088 (REQ-PROD-033)
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-263
- **statement**: With a session expired, a person who drafts a chirp and tries to post is routed to sign-in
  with the reason stated — not a silent failure — and, after signing in, is returned to where they were with
  the drafted text intact; and a transient server error during the same post can be retried in place and
  succeeds without re-typing the draft. This observes, and does not redefine, the information architecture's
  session-expiry (REQ-UX-008) and auth-gated-return (REQ-UX-007) conventions.
- **references**: REQ-UX-089 (REQ-PROD-034)
- **verification_method**: manual_user_check
- **stage**: releasable

*(`BAR-264`, the screens slice's reserved cross-cutting slot, is unused: on assembly every release-gating
`REQ-UX-*` in `040..089` is held by a chapter criterion and each cross-screen pattern is already owned by the
chapter holding its gating requirement.)*

---

## Responsive layout — `BAR-265..274`

Viewport language follows the design's breakpoints: **compact** (width < 640px, phone portrait and most phones
in landscape), **medium** (640px ≤ width < 1024px), **wide** (width ≥ 1024px); the reading **measure** is
600px; the compact side **gutter** is 16px. CSS px throughout.

### BAR-265 — The whole core loop completes on a phone
- **statement**: At a 360×640 CSS-px portrait viewport, signed in, a person completes the whole core loop end
  to end — open and scroll the home timeline, open Compose and post a chirp, reply to a chirp, like then
  unlike a chirp, follow then unfollow an account, and open a public profile — and at no step is there
  horizontal page scrolling, a control hidden off-screen, or an action target that cannot be tapped.
- **references**: REQ-UX-090
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-266 — One reading column that reflows, not rescales, across viewports
- **statement**: The content region is a single reading column at every width. At a 360px-wide viewport it
  fills the width inside the 16px gutter with no horizontal scrollbar; at a 1280px-wide viewport it is held to
  the 600px measure and horizontally centred, not stretched across the window. Neither width requires
  pinch-zoom or sideways scrolling to read a chirp.
- **references**: REQ-UX-091
- **verification_method**: automated_test
- **stage**: usable_early

### BAR-267 — The signed-in navigation shell adapts and keeps every destination reachable
- **statement**: Signed in, starting from the timeline, a person reaches Home, Explore, Notifications,
  Profile, Settings, and a Compose affordance, and sees the current destination marked, at both a compact
  (< 640px) and a wide (≥ 1024px) viewport: at compact width the primary destinations sit in a bottom tab bar
  and Compose is reachable without opening a menu; at wide width the same destinations appear in a persistent
  side navigation.
- **references**: REQ-UX-092
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-268 — The signed-out shell never dead-ends at any viewport
- **statement**: With no session, the Landing and a public profile link each show a Sign up and a Sign in
  entry without opening a menu, and keep Rules & terms and Help & support reachable (at minimum by scrolling
  to the footer), at both a compact (< 640px) and a wide (≥ 1024px) viewport. No viewport presents an
  authentication wall or hides the path to join.
- **references**: REQ-UX-093
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-269 — Feed and list screens adapt without losing their controls or scroll place
- **statement**: On a compact (< 640px) viewport, a feed/list screen longer than one page (home timeline, a
  chirp's conversation, notifications, search results, followers, following) keeps its load-older control and
  its "N new chirps" catch-up reachable without horizontal scrolling and keeps each chirp card's reply, like,
  and more controls tappable; opening an item and pressing back restores the list at its prior scroll
  position.
- **references**: REQ-UX-094
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-270 — Form screens are usable with the on-screen keyboard
- **statement**: On a compact (< 640px) viewport with the on-screen keyboard open, a form screen (sign up,
  sign in, recover access, set new credential, edit profile) shows the focused field, its label, and any
  inline error together; keeps its primary submit reachable by scrolling the form without first dismissing the
  keyboard; and never requires horizontal scrolling or a side-by-side field layout. An invalid field's error
  shows with the field, not in a summary elsewhere.
- **references**: REQ-UX-095
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-271 — Profile and settings screens stack and keep a labelled way back
- **statement**: On a compact (< 640px) viewport a public profile shows the header's avatar, display name,
  handle, bio, counts, and its context action (Follow, or Edit profile on one's own profile) without
  horizontal scrolling, with the chirps list in one column below; the Settings hub and each sub-section are
  full screens, and a labelled back returns from a sub-section to the hub.
- **references**: REQ-UX-096
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-272 — Overlays present as full-height surfaces on a phone with their actions reachable
- **statement**: On a compact (< 640px) viewport, Compose and Report present as a full-screen or bottom-sheet
  surface whose input and primary action stay visible and operable with the keyboard open, and every
  destructive confirmation (delete account, delete chirp, block or mute, end a session, sign out) shows both
  its confirm and its cancel fully visible and tappable without clipping at the screen edge; the browser back
  control dismisses the overlay without leaving the underlying screen.
- **references**: REQ-UX-097
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-273 — Touch targets are large enough and within thumb reach
- **statement**: On a touch viewport every interactive control renders a tap target of at least 44×44 CSS px
  with at least 8 CSS px between adjacent targets, and the core-loop primary actions (the Compose affordance,
  a chirp card's like and reply controls, and the primary navigation) render within the lower portion of the
  screen rather than only at the top.
- **references**: REQ-UX-098
- **verification_method**: automated_test
- **stage**: usable_early

### BAR-274 — No auto-zoom and no horizontal scroll, portrait and landscape
- **statement**: Walking the signed-in core loop at a supported phone viewport in portrait and then in
  landscape, the page never scrolls horizontally and never needs pinch-zoom, and focusing a sign-in or compose
  text field does not trigger the browser's automatic zoom; content reflows to the narrower dimension rather
  than overflowing it.
- **references**: REQ-UX-099
- **verification_method**: manual_user_check
- **stage**: usable_early

---

## Accessibility — `BAR-275..294`

The committed standard is WCAG 2.1 Level AA over the gated conformance set (the core loop and the get-in
screens with their empty, loading, and error states). Each criterion names the specific thing a reviewer
checks on the live product and how, never "accessible" in the abstract.

### BAR-275 — The committed standard and the gated set are stated by name
- **statement**: The product states its accessibility standard as WCAG 2.1 Level AA by name (not "accessible"
  in the abstract) and names its gated conformance set — the core loop and the get-in screens (sign-up,
  sign-in, recovery, onboarding) with their empty, loading, and error states. A reviewer can find the stated
  standard and the enumerated gated set in the product's accessibility statement.
- **references**: REQ-UX-100, REQ-PROD-036
- **verification_method**: inspection
- **stage**: releasable

### BAR-276 — The core loop and get-in flows are operable by keyboard alone
- **statement**: With the pointer unused, a keyboard-only user completes every core-loop and get-in action:
  sign in, read the timeline, operate a chirp's reply/like/more controls, compose and post a chirp, follow an
  account, open a profile, and operate a settings sub-section. No action is reachable by pointer only.
- **references**: REQ-UX-101
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-277 — Focus order is logical and focus is always visible
- **statement**: Tabbing through the timeline, a form, and a settings screen, focus moves in each screen's
  reading order and the focused control always shows a visible focus indicator. Opening a dialog moves focus
  into it; closing it returns focus to the opening control; changing route lands focus on the new screen
  rather than on a removed control.
- **references**: REQ-UX-102, REQ-UX-025
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-278 — No keyboard trap; modal focus is held but escapable
- **statement**: No screen leaves keyboard focus stuck with no way out. A modal dialog (compose, a destructive
  confirmation) holds focus while open, cycles focus within itself on Tab, closes on Esc and on its
  close/Cancel control, and returns focus to the control that opened it.
- **references**: REQ-UX-103
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-279 — A skip control bypasses the navigation shell to the content
- **statement**: On a signed-in screen, one Tab from the top reveals a visible "Skip to content" control that
  moves focus past the navigation shell to the main content, and a screen reader can jump to the main landmark
  directly.
- **references**: REQ-UX-104
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-280 — Every control exposes a name, a role, and its state
- **statement**: With a screen reader, each interactive component — chirp card, compose box, text field,
  toggle, button, icon button, dialog — is announced with a sensible accessible name, its correct role
  (button, switch, text box, dialog), and its current state (a like as pressed or not, a toggle as on or off,
  a busy or disabled control as such).
- **references**: REQ-UX-106
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-281 — Each screen exposes landmark regions
- **statement**: With a screen reader, the landing, the timeline, and a settings sub-section each expose a
  navigation landmark, exactly one main landmark, and (on the signed-out shell) a footer landmark, and the
  user can jump between them.
- **references**: REQ-UX-107
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-282 — One top-level heading per screen, nested in order
- **statement**: With a screen reader, the heading list for the timeline, a profile, and a settings
  sub-section each shows exactly one top-level heading that names the screen and matches the browser tab title,
  with sub-headings descending in order and no skipped levels.
- **references**: REQ-UX-108
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-283 — Lists and feeds are navigable as lists
- **statement**: With a screen reader on the timeline, the feed is navigable item by item — each chirp is a
  distinguishable list item the reader can tell from the next — and the "load older" and "N new chirps"
  catch-up affordances are reported as named buttons. The conversation, notifications, search-results, and
  followers/following lists expose the same item structure.
- **references**: REQ-UX-109
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-284 — Icon-only controls expose a text label and their active state
- **statement**: With a screen reader, each icon-only control (the compose affordance, a like control, the
  current nav destination) reports a text name; the like reports pressed or not-pressed and the current nav
  destination reports its selected state as a programmatic state, not by colour or fill alone.
- **references**: REQ-UX-110, REQ-UX-028
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-285 — Contrast meets AA in every shipped theme
- **statement**: An automated contrast scan run against the live product in each shipped theme finds normal
  text at or above 4.5:1, large text at or above 3:1 (WCAG 1.4.3), and meaningful control and icon boundaries
  at or above 3:1 (WCAG 1.4.11), with no reported failure.
- **references**: REQ-UX-111, REQ-UX-022
- **verification_method**: automated_test
- **stage**: usable_early

### BAR-286 — Text resizes and the page reflows without loss
- **statement**: At 200% browser zoom the timeline and a form show no clipped content and keep every control
  reachable (WCAG 1.4.4); at a 320-CSS-pixel viewport the reading content reflows to one column with no
  horizontal scrolling (WCAG 1.4.10); and an applied text-spacing override clips or overlaps nothing
  (WCAG 1.4.12).
- **references**: REQ-UX-112
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-287 — No fact is carried by colour alone
- **statement**: Viewed in greyscale or a colour-blindness simulation, a field error, an active like, and the
  current nav destination are each still identifiable without their colour — carried by text, an icon, or a
  label as well (WCAG 1.4.1).
- **references**: REQ-UX-113, REQ-UX-022
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-288 — No content flashes more than three times a second
- **statement**: Through normal use of the product, no content flashes more than three times in any one second
  (WCAG 2.3.1).
- **references**: REQ-UX-113
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-289 — Reduced motion is honoured with no loss of information
- **statement**: With the system reduce-motion setting on, opening and closing a menu and a dialog, triggering
  a toast, and loading a list remove or shorten motion to at most a brief fade; nothing animates continuously
  except a loading indicator that is also announced; and no information is conveyed only by movement.
- **references**: REQ-UX-114, REQ-UX-029
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-290 — Status changes are announced without stealing focus
- **statement**: With a screen reader, posting a chirp, following an account, and saving a setting are each
  announced as a status message through a polite live region without moving focus off the user's current
  control; with the timeline open, the arrival of new chirps behind the catch-up control is announced politely
  (WCAG 4.1.3).
- **references**: REQ-UX-115
- **verification_method**: manual_user_check
- **stage**: releasable

### BAR-291 — Errors are announced and tied to their field
- **statement**: With a screen reader on sign-up, submitting a taken handle announces the error, re-reads it
  when the handle field is focused, reports the field invalid, and names the problem and a fix in plain words
  with no error code (WCAG 3.3.1, 3.3.2, 3.3.3); a forced submit failure is announced, not silent.
- **references**: REQ-UX-116, REQ-UX-032
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-292 — Empty, loading, and expired-session states reach assistive technology
- **statement**: With a screen reader, opening a list announces "loading" while its skeletons are hidden from
  the reader; a forced load failure announces an error with a reachable retry; a brand-new empty timeline
  presents a heading and a next-step action rather than silence; and acting with an expired session announces
  the reason and moves focus to the sign-in screen.
- **references**: REQ-UX-117, REQ-UX-008
- **verification_method**: manual_user_check
- **stage**: usable_early

### BAR-293 — Conformance over the gated set is verified three ways, on a stated matrix
- **statement**: For a release, three recorded checks over the gated conformance set are on file — an
  automated scan in each shipped theme, a keyboard-only walk, and a screen-reader walk of the core loop —
  together with the support matrix they ran on (at least one screen reader per major platform with its common
  browser), and every gated screen appears in each check.
- **references**: REQ-UX-118
- **verification_method**: inspection
- **stage**: releasable

### BAR-294 — Accessibility gates the release; failures are fixes, not waivers
- **statement**: The release record shows the gated conformance set has no open Level A or Level AA failure,
  every accessibility failure found on the gated set was fixed rather than waived, and any failure recorded
  against a non-gating surface is tracked with that surface rather than blocking the release.
- **references**: REQ-UX-119
- **verification_method**: inspection
- **stage**: releasable

---

## Cross-cutting — `BAR-295..299`

Reserved for a release condition the assembled experience-area view needs that no single sub-area's gating
requirements already hold. On assembly, every release-gating `REQ-UX-*` in `001..119` is held by a sub-area
criterion, and every pattern that spans the experience areas is already owned by the sub-area that holds its
gating requirement:

- the one compose surface across its three placements and the like/follow controls behaving the same
  everywhere — owned by screens (`BAR-242`, `BAR-244`, `BAR-245`);
- the product-wide empty / error / loading / failure-at-point-of-action treatment — owned jointly by the
  visual component system (`BAR-226`) and screens (`BAR-260`, `BAR-261`, `BAR-262`);
- its reach to assistive technology — owned by accessibility (`BAR-292`);
- one consistent visual treatment, type scale, and token set across unrelated screens — owned by the visual
  system (`BAR-215`, `BAR-224`);
- the navigation shell staying coherent and every destination reachable as the viewport changes — owned by IA
  (`BAR-201`, `BAR-202`) and responsive (`BAR-267`, `BAR-268`).

No cross-area gap remains that rests on a release-gating requirement, so `BAR-295..299` are unused. (Minting
one here would either duplicate a sub-area criterion or rest solely on a non-gating requirement, which the
fragment excludes.)

---

## Coverage note — every release-gating `REQ-UX-*` → the `BAR-*`(s) covering it

All 106 release-gating `REQ-UX-*` (the `release_gating: true` set; the other 13 are listed as excluded below),
each referenced by at least one `BAR-*` above. The release-bar synthesis can assert experience-area
`GATING_REQ_COVERAGE` from this map without re-deriving the gating set.

### Information architecture & interaction (`REQ-UX-001..014, 016, 017, 018`)

| release-gating REQ-UX | covered by |
|---|---|
| REQ-UX-001 | BAR-200 |
| REQ-UX-002 | BAR-201 |
| REQ-UX-003 | BAR-202 |
| REQ-UX-004 | BAR-203 |
| REQ-UX-005 | BAR-204 |
| REQ-UX-006 | BAR-205 |
| REQ-UX-007 | BAR-206 |
| REQ-UX-008 | BAR-207 |
| REQ-UX-009 | BAR-208 |
| REQ-UX-010 | BAR-209 |
| REQ-UX-011 | BAR-210 |
| REQ-UX-012 | BAR-211 |
| REQ-UX-013 | BAR-212 |
| REQ-UX-014 | BAR-213 |
| REQ-UX-016 | BAR-213 |
| REQ-UX-017 | BAR-214 |
| REQ-UX-018 | BAR-214 |

### Visual language & component system (`REQ-UX-020, 021, 022, 025..029, 031..039`)

| release-gating REQ-UX | covered by |
|---|---|
| REQ-UX-020 | BAR-215 |
| REQ-UX-021 | BAR-216 |
| REQ-UX-022 | BAR-217 |
| REQ-UX-025 | BAR-218 |
| REQ-UX-026 | BAR-219 |
| REQ-UX-027 | BAR-220 |
| REQ-UX-028 | BAR-221 |
| REQ-UX-029 | BAR-222 |
| REQ-UX-031 | BAR-226 |
| REQ-UX-032 | BAR-223 |
| REQ-UX-033 | BAR-224 |
| REQ-UX-034 | BAR-224 |
| REQ-UX-035 | BAR-225 |
| REQ-UX-036 | BAR-226 |
| REQ-UX-037 | BAR-227 |
| REQ-UX-038 | BAR-228 |
| REQ-UX-039 | BAR-229 |

### Screens & flows (`REQ-UX-040..056, 058..063, 065..070, 073..077, 079, 082..089`)

| release-gating REQ-UX | covered by |
|---|---|
| REQ-UX-040 | BAR-230 |
| REQ-UX-041 | BAR-231 |
| REQ-UX-042 | BAR-232 |
| REQ-UX-043 | BAR-231 |
| REQ-UX-044 | BAR-233 |
| REQ-UX-045 | BAR-233 |
| REQ-UX-046 | BAR-234 |
| REQ-UX-047 | BAR-234 |
| REQ-UX-048 | BAR-235 |
| REQ-UX-049 | BAR-236 |
| REQ-UX-050 | BAR-237 |
| REQ-UX-051 | BAR-238 |
| REQ-UX-052 | BAR-239 |
| REQ-UX-053 | BAR-240 |
| REQ-UX-054 | BAR-241 |
| REQ-UX-055 | BAR-241 |
| REQ-UX-056 | BAR-242 |
| REQ-UX-058 | BAR-243 |
| REQ-UX-059 | BAR-244 |
| REQ-UX-060 | BAR-245 |
| REQ-UX-061 | BAR-246 |
| REQ-UX-062 | BAR-246 |
| REQ-UX-063 | BAR-247 |
| REQ-UX-065 | BAR-248 |
| REQ-UX-066 | BAR-248 |
| REQ-UX-067 | BAR-249 |
| REQ-UX-068 | BAR-249 |
| REQ-UX-069 | BAR-250 |
| REQ-UX-070 | BAR-251 |
| REQ-UX-073 | BAR-252 |
| REQ-UX-074 | BAR-253 |
| REQ-UX-075 | BAR-254 |
| REQ-UX-076 | BAR-255 |
| REQ-UX-077 | BAR-255 |
| REQ-UX-079 | BAR-256 |
| REQ-UX-082 | BAR-258 |
| REQ-UX-083 | BAR-257 |
| REQ-UX-084 | BAR-259 |
| REQ-UX-085 | BAR-260 |
| REQ-UX-086 | BAR-260 |
| REQ-UX-087 | BAR-261 |
| REQ-UX-088 | BAR-262 |
| REQ-UX-089 | BAR-263 |

### Responsive layout (`REQ-UX-090..099`)

| release-gating REQ-UX | covered by |
|---|---|
| REQ-UX-090 | BAR-265 |
| REQ-UX-091 | BAR-266 |
| REQ-UX-092 | BAR-267 |
| REQ-UX-093 | BAR-268 |
| REQ-UX-094 | BAR-269 |
| REQ-UX-095 | BAR-270 |
| REQ-UX-096 | BAR-271 |
| REQ-UX-097 | BAR-272 |
| REQ-UX-098 | BAR-273 |
| REQ-UX-099 | BAR-274 |

### Accessibility (`REQ-UX-100..104, 106..119`)

| release-gating REQ-UX | covered by |
|---|---|
| REQ-UX-100 | BAR-275 |
| REQ-UX-101 | BAR-276 |
| REQ-UX-102 | BAR-277 |
| REQ-UX-103 | BAR-278 |
| REQ-UX-104 | BAR-279 |
| REQ-UX-106 | BAR-280 |
| REQ-UX-107 | BAR-281 |
| REQ-UX-108 | BAR-282 |
| REQ-UX-109 | BAR-283 |
| REQ-UX-110 | BAR-284 |
| REQ-UX-111 | BAR-285 |
| REQ-UX-112 | BAR-286 |
| REQ-UX-113 | BAR-287, BAR-288 |
| REQ-UX-114 | BAR-289 |
| REQ-UX-115 | BAR-290 |
| REQ-UX-116 | BAR-291 |
| REQ-UX-117 | BAR-292 |
| REQ-UX-118 | BAR-293 |
| REQ-UX-119 | BAR-294 |

### Excluded as non-gating (`release_gating: false`, 13)

These are not held by any `BAR-*` and are never the sole basis of one; where a criterion names one it is
context only: `REQ-UX-015` (auth-screen interlinking), `REQ-UX-019` (notifications entry/indicator),
`REQ-UX-023` (light/dark theme parity), `REQ-UX-024` (theme follows and persists preference), `REQ-UX-030`
(avatar rendering with initials placeholder), `REQ-UX-057` (navigable conversation read), `REQ-UX-064` (find
people to follow / Explore), `REQ-UX-071` (handle-change position), `REQ-UX-072` (notification preferences),
`REQ-UX-078` (notifications surface), `REQ-UX-080` (block & mute), `REQ-UX-081` (managing blocked & muted),
`REQ-UX-105` (WCAG 2.2 target size, adopted ahead of the committed 2.1 AA floor).

---

## Staging summary (experience-area view)

The usable-early-vs-releasable split below is the reconciled experience-area proposal across the five
sub-areas; the release-bar synthesis owns the final whole-product line and may still move a criterion.

- **usable_early (51)** — the bar a first adoptable version must clear: the signed-out and signed-in shells
  that never dead-end and always show location; reachability of every core surface; the read-and-post core
  loop (bounded timeline, compose within the limit without double-posting or draft loss); reply / like /
  follow / profile; a non-dead-ended new account; the product-wide floor that no surface is a blank, an
  endless spinner, or a silent failure; the whole core loop on a phone; and the keyboard / screen-reader
  baseline that core-loop and get-in users need from day one.
  BAR-200, 201, 202, 204, 205, 209, 211, 212, 213, 216, 217, 218, 223, 225, 226, 227, 228, 229, 230, 231, 232,
  233, 235, 238, 241, 243, 244, 245, 246, 248, 253, 259, 260, 261, 262, 265, 266, 267, 268, 270, 273, 274,
  276, 277, 278, 280, 284, 285, 287, 291, 292.
- **releasable (43)** — the bar the public release must additionally clear: auth-gated routing and
  session-expiry recovery; predictable browser history; the full designed-state treatment on every entry/auth
  and timeline surface; catch-up and reading-position; the compose surface across all three placements;
  addressable follower/following lists; full account management (edit, settings hub, contact control,
  sessions, export, self-serve deletion); reporting and the rules/help surfaces; the responsive polish on
  feed/profile/overlay screens; and the WCAG 2.1 AA completion and its verified, no-open-failure release gate.
  BAR-203, 206, 207, 208, 210, 214, 215, 219, 220, 221, 222, 224, 234, 236, 237, 239, 240, 242, 247, 249, 250,
  251, 252, 254, 255, 256, 257, 258, 263, 269, 271, 272, 275, 279, 281, 282, 283, 286, 288, 289, 290, 293,
  294.

(51 `usable_early` + 43 `releasable` = 94 criteria, `BAR-200..294` less the unused `BAR-264`.)
