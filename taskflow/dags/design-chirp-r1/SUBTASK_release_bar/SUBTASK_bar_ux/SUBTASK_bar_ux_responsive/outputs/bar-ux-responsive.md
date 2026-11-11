# Release bar — responsive-layout area (BAR-265..274)

This fragment holds the ten release-gating responsive-layout requirements
`REQ-UX-090..099` (defined in `design/experience-design.md`) to concrete, testable
release conditions on the live product. Each `BAR-*` is a checkable release condition,
not a restatement of the requirement it enforces; it names the concrete viewport or
target measurement a reviewer checks.

Viewport language follows the design's breakpoints and tokens: **compact** (width < 640px,
phone portrait and most phones in landscape), **medium** (640px ≤ width < 1024px),
**wide** (width ≥ 1024px); the reading **measure** is 600px; the compact side **gutter**
is 16px. CSS px throughout.

Each block carries the frozen field set: `id`, `statement`, `references` (≥1 `REQ-UX-*`),
`verification_method` (one of `manual_user_check` | `automated_test` | `inspection` |
`operational_check`), and `proposed_stage` (`usable_early` | `releasable` — this is the
responsive-area view; the within-UX synthesis and then the whole-product synthesis
finalize the cross-area staging line).

---

### BAR-265 — The whole core loop completes on a phone
- **statement**: At a 360×640 CSS-px portrait viewport, signed in, a person completes the
  whole core loop end to end — open and scroll the home timeline, open Compose and post a
  chirp, reply to a chirp, like then unlike a chirp, follow then unfollow an account, and
  open a public profile — and at no step is there horizontal page scrolling, a control
  hidden off-screen, or an action target that cannot be tapped.
- **references**: REQ-UX-090
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-266 — One reading column that reflows, not rescales, across viewports
- **statement**: The content region is a single reading column at every width. At a 360px-wide
  viewport it fills the width inside the 16px gutter with no horizontal scrollbar; at a
  1280px-wide viewport it is held to the 600px measure and horizontally centred, not stretched
  across the window. Neither width requires pinch-zoom or sideways scrolling to read a chirp.
- **references**: REQ-UX-091
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-267 — The signed-in navigation shell adapts and keeps every destination reachable
- **statement**: Signed in, starting from the timeline, a person reaches Home, Explore,
  Notifications, Profile, Settings, and a Compose affordance, and sees the current destination
  marked, at both a compact (< 640px) and a wide (≥ 1024px) viewport: at compact width the
  primary destinations sit in a bottom tab bar and Compose is reachable without opening a menu;
  at wide width the same destinations appear in a persistent side navigation.
- **references**: REQ-UX-092
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-268 — The signed-out shell never dead-ends at any viewport
- **statement**: With no session, the Landing and a public profile link each show a Sign up
  and a Sign in entry without opening a menu, and keep Rules & terms and Help & support
  reachable (at minimum by scrolling to the footer), at both a compact (< 640px) and a wide
  (≥ 1024px) viewport. No viewport presents an authentication wall or hides the path to join.
- **references**: REQ-UX-093
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-269 — Feed and list screens adapt without losing their controls or scroll place
- **statement**: On a compact (< 640px) viewport, a feed/list screen longer than one page
  (home timeline, a chirp's conversation, notifications, search results, followers, following)
  keeps its load-older control and its "N new chirps" catch-up reachable without horizontal
  scrolling and keeps each chirp card's reply, like, and more controls tappable; opening an
  item and pressing back restores the list at its prior scroll position.
- **references**: REQ-UX-094
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-270 — Form screens are usable with the on-screen keyboard
- **statement**: On a compact (< 640px) viewport with the on-screen keyboard open, a form
  screen (sign up, sign in, recover access, set new credential, edit profile) shows the focused
  field, its label, and any inline error together; keeps its primary submit reachable by
  scrolling the form without first dismissing the keyboard; and never requires horizontal
  scrolling or a side-by-side field layout. An invalid field's error shows with the field,
  not in a summary elsewhere.
- **references**: REQ-UX-095
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

### BAR-271 — Profile and settings screens stack and keep a labelled way back
- **statement**: On a compact (< 640px) viewport a public profile shows the header's avatar,
  display name, handle, bio, counts, and its context action (Follow, or Edit profile on one's
  own profile) without horizontal scrolling, with the chirps list in one column below; the
  Settings hub and each sub-section are full screens, and a labelled back returns from a
  sub-section to the hub.
- **references**: REQ-UX-096
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-272 — Overlays present as full-height surfaces on a phone with their actions reachable
- **statement**: On a compact (< 640px) viewport, Compose and Report present as a full-screen
  or bottom-sheet surface whose input and primary action stay visible and operable with the
  keyboard open, and every destructive confirmation (delete account, delete chirp, block or
  mute, end a session, sign out) shows both its confirm and its cancel fully visible and
  tappable without clipping at the screen edge; the browser back control dismisses the overlay
  without leaving the underlying screen.
- **references**: REQ-UX-097
- **verification_method**: manual_user_check
- **proposed_stage**: releasable

### BAR-273 — Touch targets are large enough and within thumb reach
- **statement**: On a touch viewport every interactive control renders a tap target of at
  least 44×44 CSS px with at least 8 CSS px between adjacent targets, and the core-loop primary
  actions (the Compose affordance, a chirp card's like and reply controls, and the primary
  navigation) render within the lower portion of the screen rather than only at the top.
- **references**: REQ-UX-098
- **verification_method**: automated_test
- **proposed_stage**: usable_early

### BAR-274 — No auto-zoom and no horizontal scroll, portrait and landscape
- **statement**: Walking the signed-in core loop at a supported phone viewport in portrait and
  then in landscape, the page never scrolls horizontally and never needs pinch-zoom, and
  focusing a sign-in or compose text field does not trigger the browser's automatic zoom;
  content reflows to the narrower dimension rather than overflowing it.
- **references**: REQ-UX-099
- **verification_method**: manual_user_check
- **proposed_stage**: usable_early

---

## Coverage note — responsive-area release-gating REQ-UX-* → BAR-*

Every release-gating `REQ-UX-*` in this area (`REQ-UX-090..099`, all ten gating; none
non-gating) is referenced by at least one `BAR-*` above. This lets the within-UX synthesis
gate assert `UX_GATING_REQ_COVERAGE` for the responsive area without re-deriving the set.

| REQ-UX-* | release_gating | Covered by | Proposed stage |
|----------|----------------|------------|----------------|
| REQ-UX-090 — core loop usable on a phone | true | BAR-265 | usable_early |
| REQ-UX-091 — one reading column, reflowed not rescaled | true | BAR-266 | usable_early |
| REQ-UX-092 — signed-in nav shell adapts, destinations reachable | true | BAR-267 | usable_early |
| REQ-UX-093 — signed-out shell never dead-ends | true | BAR-268 | usable_early |
| REQ-UX-094 — feed/list screens adapt without losing controls | true | BAR-269 | releasable |
| REQ-UX-095 — form screens usable with the on-screen keyboard | true | BAR-270 | usable_early |
| REQ-UX-096 — profile and settings stack with a way back | true | BAR-271 | releasable |
| REQ-UX-097 — overlays full-height on a phone, actions reachable | true | BAR-272 | releasable |
| REQ-UX-098 — touch targets large enough and reachable | true | BAR-273 | usable_early |
| REQ-UX-099 — no auto-zoom, no horizontal scroll, portrait and landscape | true | BAR-274 | usable_early |

**Range check**: all ids lie within the assigned sub-range BAR-265..274. **Coverage**: 10/10
gating requirements referenced. **Non-gating in band**: none. No `BAR-*` here is justified
solely by a non-gating requirement.
