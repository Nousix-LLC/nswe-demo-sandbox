# Release bar — visual language & component system (BAR-215..229)

Release-bar criteria for the visual-language and component-system area. Each `BAR-*` is a checkable
release condition someone who was not in the design room can test against the live product, and it
enforces one or more release-gating `REQ-UX-*` from `design/experience-design.md`. A criterion states
what must be observably true at release; it does not restate the requirement or prescribe how the
product is built. One `BAR-*` may enforce several closely related requirements.

`verification_method` is drawn from the closed vocabulary `{ manual_user_check, automated_test,
inspection, operational_check }`. `proposed_stage` is this area's view of when the criterion must hold
(`usable_early` = the first version a person could adopt for the core loop; `releasable` = the bar the
public release must additionally clear); the cross-area line is finalized downstream.

---

### BAR-215 — Unrelated screens share one visual treatment
- **statement**: On three screens of different archetypes on the live product (for example the home
  timeline, a profile, and a settings sub-section), body text is the same size and leading, the gutters
  and spacing rhythm match, buttons share one shape and one primary colour, and no screen introduces a
  colour or control style absent from the others.
- **references**: REQ-UX-020
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-216 — Reading text is legible and hierarchy is visible
- **statement**: On the live product, chirp and reading text renders at no less than 15px with visibly
  generous line spacing; on any screen the main heading is visibly larger and heavier than its body
  text, and meta text (timestamps, handles) is visibly quieter than body text.
- **references**: REQ-UX-021
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-217 — Colour contrast meets WCAG 2.1 AA, measured
- **statement**: On the live product, sample body text, secondary text, link text, primary-button text,
  and a field border and measure each with a contrast tool: normal text reaches ≥ 4.5:1, large text
  ≥ 3:1, and control and meaningful-icon boundaries ≥ 3:1. The measurement passes in each theme the
  product ships.
- **references**: REQ-UX-022
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-218 — Every keyboard-reachable control shows a visible focus indicator
- **statement**: Using only the keyboard on the live product, tabbing through a screen's links, buttons,
  fields, and menu items shows a distinct focus indicator on each that stands out from its surroundings,
  and no focusable control takes focus without a visible indicator.
- **references**: REQ-UX-025
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-219 — Spacing, grid, and reading measure are consistent and bounded
- **statement**: On the live product, the reading column (timeline, conversation, profile chirps, a
  form) is held to a bounded measure on a wide window rather than spanning the whole width; on a phone
  viewport the same content fills the width with a consistent edge gutter; and the spacing between items
  is visibly uniform within and across these screens.
- **references**: REQ-UX-026
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-220 — Overlapping surfaces stack in a consistent order
- **statement**: On the live product, opening a menu places it above content; opening a dialog places it
  above content on a dimmed scrim with the menu not showing through; triggering a toast places it above
  the dialog. At no point does a lower layer render on top of a higher one.
- **references**: REQ-UX-027
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-221 — Icons are consistent and meaning never rides on colour alone
- **statement**: On the live product, icons come from one consistent set; the current primary-nav
  destination reads as active by more than colour, confirmed still identifiable in greyscale or a
  colour-blind simulation; and every icon-only control (compose, like, menu) exposes an accessible name
  to a screen reader and a label on hover.
- **references**: REQ-UX-028
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-222 — Motion is bounded and respects reduced-motion
- **statement**: On the live product, opening and closing a menu and a dialog and triggering a toast
  each complete a brief transition (well under half a second) that settles, with nothing animating or
  blinking continuously apart from a bounded loading indicator; with the system reduce-motion setting
  on, the same actions remove or reduce animation to a short fade and no information is lost.
- **references**: REQ-UX-029
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-223 — One voice, with plain and actionable errors
- **statement**: On the live product, action buttons across several screens read as sentence-case verbs
  (for example "Post", "Follow", "Save changes") rather than "OK"/"Submit" or Title Case; and a forced
  error (an invalid form entry, then a failed submit) shows a plain-language message with a way forward
  and no raw error code, stack text, or internal identifier.
- **references**: REQ-UX-032
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-224 — Screens are assembled from the named components, and components come from the tokens
- **statement**: On three screens of different archetypes on the live product, a chirp, buttons, text
  fields, and error messages each render from one shared treatment with no bespoke control standing in
  for a library component; and inspecting a chirp card, a primary button, a text field, and a dialog in
  each shipped theme shows colours matching the token roles (a primary action is the one primary colour,
  a destructive one the danger colour), text sizes matching the type scale, and no colour or size that
  is absent from the token set.
- **references**: REQ-UX-033, REQ-UX-034
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-225 — The chirp card and compose box hold the core-loop contract
- **statement**: On the live product, typing past the character limit in compose turns the counter to
  the danger treatment and disables Post; an empty draft leaves Post disabled and posts nothing; a valid
  chirp posts and appears as a chirp card showing avatar, author, handle, relative time, text, and the
  like / reply / more-actions row; and liking a chirp shows a filled icon and a "Liked" label together,
  still identifiable as liked in greyscale.
- **references**: REQ-UX-035
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-226 — Empty, loading, and failure states carry a designed treatment
- **statement**: On the live product, a brand-new account's empty timeline shows an explanatory block
  with a next step rather than a blank area; a list while loading shows skeleton rows at the real item
  size rather than a spinner on a blank screen; a forced page-load failure shows an inline message with
  a retry in place of the missing items while keeping any items already shown; and a failed action shows
  an inline error in the product's danger styling at the point of action. None of these renders a blank
  area, a frozen screen, or a raw failure.
- **references**: REQ-UX-031, REQ-UX-036
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-227 — Forms validate inline at the field, in plain language
- **statement**: On the live product sign-up, submitting a handle already in use shows a plain-language
  error against the handle field naming the handle (not in a distant summary and not as a code);
  submitting a mis-formatted handle shows a field-level validation error that explains the rule; and
  while a handle's availability is being checked the field shows a pending state rather than flicking
  prematurely to valid or invalid.
- **references**: REQ-UX-037
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-228 — Consequential actions are confirmed before they happen
- **statement**: On the live product, initiating deletion of a chirp, blocking an account, and deleting
  the account each present a confirmation that names what will happen and offers a plain cancel, and
  nothing changes on cancel; the account-deletion confirmation additionally states what is and is not
  retained and points to data export before proceeding.
- **references**: REQ-UX-038
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-229 — The result of every action is shown through the feedback components
- **statement**: On the live product, publishing a chirp, following an account, and saving a setting
  each show a brief, non-blocking confirmation; an action in flight shows its control in a busy state
  that cannot be re-triggered; and a forced in-place failure (acting while offline, or a transient
  server error while posting) shows the failure at the control with a way to retry and does not lose the
  drafted text.
- **references**: REQ-UX-039
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

---

## Coverage note — visual & component area

Every release-gating `REQ-UX-*` in the `REQ-UX-020..039` band (`release_gating: true`) and the `BAR-*`
that enforces it. The synthesis gate asserts gating coverage for this sub-area against this map without
re-deriving the gating set.

| Release-gating REQ-UX-* | Covered by |
|-------------------------|------------|
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

All 17 release-gating requirements in this band (020, 021, 022, 025–029, 031–039) are referenced by at
least one `BAR-*`.

**Not covered — non-gating in this band** (`release_gating: false`; carried here only so the gate sees
the whole band accounted for, never as the sole basis of any `BAR-*`): REQ-UX-023 (light and dark theme
at parity), REQ-UX-024 (theme follows and persists the reader's preference), REQ-UX-030 (consistent
avatar rendering with an initials placeholder). The legibility and contrast bars (BAR-216, BAR-217)
hold in whichever theme the product ships, and the no-broken-state bar (BAR-226) carries the hard
minimum behind REQ-UX-030; the designed theme and avatar systems themselves are out of the gating set.
