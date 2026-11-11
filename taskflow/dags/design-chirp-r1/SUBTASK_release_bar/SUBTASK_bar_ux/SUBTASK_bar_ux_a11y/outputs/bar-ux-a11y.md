# Release bar — accessibility (BAR-275..294)

The accessibility slice of the experience-area release bar. Each `BAR-*` below turns one or more
release-gating accessibility requirements (`REQ-UX-100..119` in `design/experience-design.md`) into a
concrete, testable release condition: it names the specific thing a reviewer checks on the live product and how
they check it, never "accessible" in the abstract. Ids are minted only in `BAR-275..294`. A `BAR-*` references
the requirement(s) it enforces; it does not restate them.

This fragment covers the 19 release-gating requirements in the accessibility band — `REQ-UX-100..104` and
`REQ-UX-106..119`. `REQ-UX-105` (WCAG 2.2 target size, 2.5.8) is **not** covered here: it is non-gating,
adopted ahead of the committed WCAG 2.1 AA floor, and no criterion below rests on it.

Each block carries: **id**, **statement** (the checkable release condition), **references** (the gating
requirement(s) it enforces, and any requirement it composes with), **verification_method** (one of
`manual_user_check` · `automated_test` · `inspection` · `operational_check`), and **proposed_stage**
(`usable_early` | `releasable` — this is the accessibility-area proposal; the UX synthesis gate reconciles the
five sub-areas and the parent release-bar synthesis owns the final cross-area line).

---

## BAR register

### BAR-275 — The committed standard and the gated set are stated by name
- **statement**: The product states its accessibility standard as WCAG 2.1 Level AA by name (not "accessible"
  in the abstract) and names its gated conformance set — the core loop and the get-in screens (sign-up,
  sign-in, recovery, onboarding) with their empty, loading, and error states. A reviewer can find the stated
  standard and the enumerated gated set in the product's accessibility statement.
- **references**: REQ-UX-100, REQ-PROD-036
- **verification_method**: inspection
- **proposed_stage**: releasable

### BAR-276 — The core loop and get-in flows are operable by keyboard alone
- **statement**: With the pointer unused, a keyboard-only user completes every core-loop and get-in action:
  sign in, read the timeline, operate a chirp's reply/like/more controls, compose and post a chirp, follow an
  account, open a profile, and operate a settings sub-section. No action is reachable by pointer only.
- **references**: REQ-UX-101
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-277 — Focus order is logical and focus is always visible
- **statement**: Tabbing through the timeline, a form, and a settings screen, focus moves in each screen's
  reading order and the focused control always shows a visible focus indicator. Opening a dialog moves focus
  into it; closing it returns focus to the opening control; changing route lands focus on the new screen
  rather than on a removed control.
- **references**: REQ-UX-102, REQ-UX-025
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-278 — No keyboard trap; modal focus is held but escapable
- **statement**: No screen leaves keyboard focus stuck with no way out. A modal dialog (compose, a destructive
  confirmation) holds focus while open, cycles focus within itself on Tab, closes on Esc and on its
  close/Cancel control, and returns focus to the control that opened it.
- **references**: REQ-UX-103
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-279 — A skip control bypasses the navigation shell to the content
- **statement**: On a signed-in screen, one Tab from the top reveals a visible "Skip to content" control that
  moves focus past the navigation shell to the main content, and a screen reader can jump to the main landmark
  directly.
- **references**: REQ-UX-104
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-280 — Every control exposes a name, a role, and its state
- **statement**: With a screen reader, each interactive component — chirp card, compose box, text field,
  toggle, button, icon button, dialog — is announced with a sensible accessible name, its correct role
  (button, switch, text box, dialog), and its current state (a like as pressed or not, a toggle as on or off,
  a busy or disabled control as such).
- **references**: REQ-UX-106
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-281 — Each screen exposes landmark regions
- **statement**: With a screen reader, the landing, the timeline, and a settings sub-section each expose a
  navigation landmark, exactly one main landmark, and (on the signed-out shell) a footer landmark, and the
  user can jump between them.
- **references**: REQ-UX-107
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-282 — One top-level heading per screen, nested in order
- **statement**: With a screen reader, the heading list for the timeline, a profile, and a settings
  sub-section each shows exactly one top-level heading that names the screen and matches the browser tab
  title, with sub-headings descending in order and no skipped levels.
- **references**: REQ-UX-108
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-283 — Lists and feeds are navigable as lists
- **statement**: With a screen reader on the timeline, the feed is navigable item by item — each chirp is a
  distinguishable list item the reader can tell from the next — and the "load older" and "N new chirps"
  catch-up affordances are reported as named buttons. The conversation, notifications, search-results, and
  followers/following lists expose the same item structure.
- **references**: REQ-UX-109
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-284 — Icon-only controls expose a text label and their active state
- **statement**: With a screen reader, each icon-only control (the compose affordance, a like control, the
  current nav destination) reports a text name; the like reports pressed or not-pressed and the current nav
  destination reports its selected state as a programmatic state, not by colour or fill alone.
- **references**: REQ-UX-110, REQ-UX-028
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-285 — Contrast meets AA in every shipped theme
- **statement**: An automated contrast scan run against the live product in each shipped theme finds normal
  text at or above 4.5:1, large text at or above 3:1 (WCAG 1.4.3), and meaningful control and icon boundaries
  at or above 3:1 (WCAG 1.4.11), with no reported failure.
- **references**: REQ-UX-111, REQ-UX-022
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-286 — Text resizes and the page reflows without loss
- **statement**: At 200% browser zoom the timeline and a form show no clipped content and keep every control
  reachable (WCAG 1.4.4); at a 320-CSS-pixel viewport the reading content reflows to one column with no
  horizontal scrolling (WCAG 1.4.10); and an applied text-spacing override clips or overlaps nothing
  (WCAG 1.4.12).
- **references**: REQ-UX-112
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-287 — No fact is carried by colour alone
- **statement**: Viewed in greyscale or a colour-blindness simulation, a field error, an active like, and the
  current nav destination are each still identifiable without their colour — carried by text, an icon, or a
  label as well (WCAG 1.4.1).
- **references**: REQ-UX-113, REQ-UX-022
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-288 — No content flashes more than three times a second
- **statement**: Through normal use of the product, no content flashes more than three times in any one second
  (WCAG 2.3.1).
- **references**: REQ-UX-113
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-289 — Reduced motion is honoured with no loss of information
- **statement**: With the system reduce-motion setting on, opening and closing a menu and a dialog, triggering
  a toast, and loading a list remove or shorten motion to at most a brief fade; nothing animates continuously
  except a loading indicator that is also announced; and no information is conveyed only by movement.
- **references**: REQ-UX-114, REQ-UX-029
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-290 — Status changes are announced without stealing focus
- **statement**: With a screen reader, posting a chirp, following an account, and saving a setting are each
  announced as a status message through a polite live region without moving focus off the user's current
  control; with the timeline open, the arrival of new chirps behind the catch-up control is announced politely
  (WCAG 4.1.3).
- **references**: REQ-UX-115
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-291 — Errors are announced and tied to their field
- **statement**: With a screen reader on sign-up, submitting a taken handle announces the error, re-reads it
  when the handle field is focused, reports the field invalid, and names the problem and a fix in plain words
  with no error code (WCAG 3.3.1, 3.3.2, 3.3.3); a forced submit failure is announced, not silent.
- **references**: REQ-UX-116, REQ-UX-032
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-292 — Empty, loading, and expired-session states reach assistive technology
- **statement**: With a screen reader, opening a list announces "loading" while its skeletons are hidden from
  the reader; a forced load failure announces an error with a reachable retry; a brand-new empty timeline
  presents a heading and a next-step action rather than silence; and acting with an expired session announces
  the reason and moves focus to the sign-in screen.
- **references**: REQ-UX-117, REQ-UX-008
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-293 — Conformance over the gated set is verified three ways, on a stated matrix
- **statement**: For a release, three recorded checks over the gated conformance set are on file — an
  automated scan in each shipped theme, a keyboard-only walk, and a screen-reader walk of the core loop —
  together with the support matrix they ran on (at least one screen reader per major platform with its common
  browser), and every gated screen appears in each check.
- **references**: REQ-UX-118
- **verification_method**: inspection
- **proposed_stage**: releasable

### BAR-294 — Accessibility gates the release; failures are fixes, not waivers
- **statement**: The release record shows the gated conformance set has no open Level A or Level AA failure,
  every accessibility failure found on the gated set was fixed rather than waived, and any failure recorded
  against a non-gating surface is tracked with that surface rather than blocking the release.
- **references**: REQ-UX-119
- **verification_method**: inspection
- **proposed_stage**: releasable

---

## Coverage note — every release-gating accessibility requirement maps to a BAR

The 19 release-gating requirements in this band (`REQ-UX-100..104`, `REQ-UX-106..119`) and the `BAR-*` that
holds each to a release condition. This lets the UX synthesis gate assert accessibility-area gating coverage
without re-deriving the gating set.

| Release-gating REQ | Covered by | What the BAR checks |
|--------------------|------------|---------------------|
| REQ-UX-100 | BAR-275 | WCAG 2.1 AA named; gated set enumerated |
| REQ-UX-101 | BAR-276 | Keyboard-only operability of the core loop and get-in flows |
| REQ-UX-102 | BAR-277 | Logical focus order, always-visible focus, deliberate focus moves |
| REQ-UX-103 | BAR-278 | No keyboard trap; escapable, returning modal focus |
| REQ-UX-104 | BAR-279 | Skip-to-content bypass of the nav shell |
| REQ-UX-106 | BAR-280 | Name, role, and state on every control |
| REQ-UX-107 | BAR-281 | Landmark regions per screen |
| REQ-UX-108 | BAR-282 | One nested top-level heading per screen |
| REQ-UX-109 | BAR-283 | Lists and feeds navigable as lists |
| REQ-UX-110 | BAR-284 | Icon-only controls labelled with programmatic active state |
| REQ-UX-111 | BAR-285 | AA contrast in every shipped theme |
| REQ-UX-112 | BAR-286 | Resize to 200%, reflow to 320px, text-spacing override |
| REQ-UX-113 | BAR-287, BAR-288 | No colour-alone (BAR-287); no flash over 3/s (BAR-288) |
| REQ-UX-114 | BAR-289 | Reduced motion honoured without information loss |
| REQ-UX-115 | BAR-290 | Status changes announced politely without stealing focus |
| REQ-UX-116 | BAR-291 | Errors announced and tied to their field |
| REQ-UX-117 | BAR-292 | Empty, loading, and expired-session states reach AT |
| REQ-UX-118 | BAR-293 | Three-way verification over the gated set, with a matrix |
| REQ-UX-119 | BAR-294 | Accessibility gates the release; failures are fixes |

**Excluded as non-gating**: `REQ-UX-105` (WCAG 2.2 target size, 2.5.8) is `release_gating: false` and is not
covered by any `BAR-*` here; no criterion above rests on it.

## Staging proposal — the accessibility-area view

The accessibility-area proposal splits the band on one line: a `BAR-*` is **`usable_early`** when the core loop
and get-in screens cannot be operated or perceived by a keyboard or screen-reader user without it — the
baseline those users need in the first usable version — and **`releasable`** when it completes the committed
WCAG 2.1 AA conformance claim and its release gate. Staging a criterion `usable_early` does not weaken the
release gate: every requirement here remains release-gating, and a `usable_early` criterion must hold by the
first usable version and continue to hold at release.

- **usable_early** (baseline operability and perceivability): BAR-276, BAR-277, BAR-278, BAR-280, BAR-284,
  BAR-285, BAR-287, BAR-291, BAR-292.
- **releasable** (completes the AA claim and the verification gate): BAR-275, BAR-279, BAR-281, BAR-282,
  BAR-283, BAR-286, BAR-288, BAR-289, BAR-290, BAR-293, BAR-294.

The UX synthesis gate reconciles this proposal with the four sibling sub-areas into one coherent per-`BAR-*`
stage, and the parent release-bar synthesis owns the final whole-product line.
