## Responsive layout

chirp is read on a phone more than anywhere else, so the design is phone-first: every screen is drawn
for a narrow, one-handed, portrait screen first, and wider viewports are treated as that same design
given more room — never as the "real" layout that a phone is a cut-down copy of. The product is one
reading column of text with a navigation frame around it; responsive design decides how that frame
reflows and how far the column is allowed to grow, so the same product feels native on a phone, a
tablet, and a laptop without being rebuilt three times.

This section owns how the product adapts across viewports. It composes against the screen inventory and
its seven archetypes from the information-architecture section, and against the component library and
design tokens from the visual-language section — in particular the 600px reading measure
(`space.measure`), the phone and wide gutters (`space.gutter.mobile` 16px, `space.gutter.wide` 24px),
and the `NavShell`, `ListView`, `ChirpCard`, `ComposeBox`, `Dialog`, `ProfileHeader`, and `SettingRow`
components. It does not redefine any of them; it says where they move, what they collapse to, what
stacks, and what must stay reachable, so that the behaviours the other sections specify hold at every
width. The non-negotiable floor is REQ-PROD-035: the core loop — read the timeline, compose and post,
reply, like, follow, view a profile — works in a phone browser with no broken layout and no unreachable
control.

### Breakpoints and the layout strategy

Adaptation happens at three ranges, anchored to the reading measure rather than to any particular
device. These breakpoints are design intent in CSS pixels; a build realises them with whatever
mechanism it prefers.

| Token | Range | What it is | What the layout does |
|---|---|---|---|
| `breakpoint.compact` | width < 640px | Phone portrait, and most phones in landscape | One column filling the viewport inside a 16px (`space.gutter.mobile`) side gutter; navigation as a bottom tab bar plus a slim top bar. |
| `breakpoint.medium` | 640px ≤ width < 1024px | Large phones, tablets, split or small desktop windows | The 600px reading measure is reached and the column centres with a 24px (`space.gutter.wide`) gutter; navigation moves to a side column, collapsed to icons when width is tight. |
| `breakpoint.wide` | width ≥ 1024px | Laptop and desktop | The reading column stays at the 600px measure, centred; a persistent left navigation shows icons with labels; a secondary rail (for example discovery entries) MAY sit outside the measure where there is room, and the core loop never depends on it. |

640px is where the 600px measure plus two comfortable gutters first fits, so below it the column fills
the screen and at or above it the column settles to the measure. The strategy is the same at every
range: **one reading column, reflowed to the width available, never widened past the measure, and never
made to scroll sideways or demand a pinch-zoom.** Growing the window gives the navigation frame and an
optional secondary rail more room; it does not stretch a line of chirp text to the full width of a
desktop, because long lines are harder to track and the product would stop feeling like itself.

### How the navigation shell adapts

The `NavShell` keeps the same set of destinations the information-architecture section fixed; only its
presentation reflows. The active destination is marked in every presentation, and the accessibility
section owns how each presentation is operated and announced.

**The signed-in shell.**

- *Compact.* A **bottom tab bar** carries the primary destinations — Home, Explore, Notifications (with
  its unseen-activity indicator), and Profile — within thumb reach, and a prominent **Compose**
  affordance is present without opening a menu. A slim top bar carries the wordmark or the current
  screen's title and the entry to the account menu (Settings, Help & support, Rules & terms, Sign out).
  No primary destination is buried behind a hamburger: the loop's everyday moves are one tap from the
  bottom of the screen.
- *Medium.* The destinations move to a **left navigation column**, shown as icons when width is tight
  and as icons with labels as room allows; Compose becomes a prominent button in that column; the bottom
  bar retires once the side navigation is present, so there is never both at once.
- *Wide.* The left navigation is **persistent with labels**, Compose sits in it as a primary button, and
  a secondary rail MAY appear opposite the reading column for discovery or supplementary content where
  the window is wide enough — the reading column stays centred at its measure between them.

**The signed-out shell.** At every width the wordmark, a **Sign in** entry, and a prominent **Sign up**
entry stay visible without opening a menu, and **Rules & terms** and **Help & support** stay reachable
(at the footer at minimum). A visitor who arrives on a shared public link lands on the content inside
this shell with the join path in sight — a narrow screen never collapses the shell into an
authentication wall or hides Sign up behind a menu.

### How each screen archetype adapts

The seven archetypes are designed once here for the whole product rather than screen by screen.

- **feed/list** (home timeline, a chirp's conversation, notifications, search results, followers and
  following). One column at every width — it *is* the reading column. On a compact viewport it fills the
  width inside the gutter; the `ListView`'s load-older control and the timeline's "N new chirps" catch-up
  stay reachable without horizontal scrolling; each `ChirpCard`'s reply, like, and more-actions controls
  stay full-size and tappable; and the person's scroll position is kept when they return from drilling
  into a chirp. Nothing in a list reflows into side-by-side columns on a phone.
- **form** (sign up, sign in, recover access, set new credential, edit profile). `TextField`s stack
  full-width within the gutter, one field per row — never a two-column form on a phone. Each field keeps
  its label and its `InlineError` with it, so a validation message is read at the field, not in a summary
  pushed off-screen. The primary submit stays reachable when the on-screen keyboard is open: the person
  can scroll the form to the submit without first dismissing the keyboard, and the keyboard never
  permanently hides the action.
- **profile** (public and own). The `ProfileHeader` stacks on a compact viewport — avatar, display name,
  handle, bio, and the follower/following counts — with its context action (Follow, or Edit profile on
  one's own profile) visible without horizontal scrolling. The person's chirps render in the single
  column below as an ordinary feed/list.
- **settings** (the hub and its sub-sections). The Settings hub is a single column of `SettingRow`s. On
  a compact viewport the hub and each sub-section are **separate full screens**, and a sub-section
  carries a labelled way back to the hub; the browser back control does the same. A two-pane
  hub-and-detail presentation is permitted on a wide viewport but is not required, and the phone
  behaviour is the baseline.
- **modal/dialog** (Compose, Report). On a compact viewport the `Dialog` modal variant presents as a
  **full-screen or bottom-sheet surface** rather than a small centred panel, so its hosted task — the
  `ComposeBox`, for instance — and its Post or submit button are comfortably usable with the keyboard
  open. The close affordance stays reachable and the browser back control dismisses the overlay without
  leaving the underlying screen. On medium and wide viewports the centred panel over the scrim (per the
  component) is used.
- **confirmation** (delete account, delete chirp, block or mute, end a session, sign out). On a compact
  viewport a confirmation presents as a bottom sheet or a full-width dialog with **both** actions fully
  visible — the destructive confirm and the plain cancel — so neither is clipped at the screen edge and
  the safe way out is always tappable. The consequence text stays legible; a long explanation scrolls
  within the surface rather than pushing the actions off-screen.
- **empty/landing** (Landing, Onboarding, Rules & terms, Help & support, Not found). The `EmptyState`
  block — illustration, headline, explanation, and next step — scales down to the narrow column with its
  next-step action kept prominent. On the signed-out Landing, Sign up and Sign in stay prominent and
  reachable on a phone.

### Touch targets, reachability, and input ergonomics

On a touch viewport the product is operated with a thumb, so size and placement are part of whether it
works at all.

- **Target size.** Every interactive control presents a touch target of at least 44×44 CSS px, with at
  least `space.2` (8px) between adjacent targets so neighbours are not mis-tapped. The `IconButton`'s
  built-in `space.2` hit padding already serves this; dense rows (a `ChirpCard`'s action row, a
  `SettingRow`'s control) keep their controls to the minimum. This is the responsive ergonomic floor; the
  accessibility section owns the formal conformance target-size success criterion and does not conflict
  with it.
- **Reachability.** The core-loop primary actions — the Compose affordance, a `ChirpCard`'s like and
  reply, and primary navigation — sit within comfortable thumb reach on a tall phone, which is why the
  signed-in shell puts navigation and Compose at the bottom on a compact viewport rather than only at the
  top. A destructive confirmation places its actions where a thumb rests, with the safe action no harder
  to reach than the destructive one.
- **Input ergonomics.** Focusing a text field does not trigger the browser's automatic zoom, and the core
  loop works in both portrait and landscape on a phone. Content reflows to the narrower dimension; the
  page never scrolls horizontally and never requires a pinch-zoom to read a chirp or operate a control.
  A drafted chirp survives an orientation change (it is already preserved across an interruption per the
  `ComposeBox`), so rotating the phone does not lose work.

### What must hold on a phone for the core loop

This is the release floor the rest of the section serves. On a phone-sized viewport in portrait, a
signed-in person can, end to end: read the home timeline and page through it; open Compose and post a
chirp within the character limit; reply to a chirp; like and unlike; follow and unfollow; and open and
read a public profile. At no step is the page scrolled horizontally, a control placed off-screen, an
action target too small to tap, or a layout broken by the narrow width. If any one of those moves cannot
be completed on a phone, the product is not releasable, regardless of how well it behaves on a desktop.

### Requirements and acceptance criteria — REQ-UX-090..099

The responsive requirements chirp must meet. Each is testable by someone who never met the author,
exercisable on the live product; each carries a `release_gating` flag and references the product
requirement(s) it serves. These compose against the screen inventory, the component library, and the
design tokens; they do not redefine them.

#### REQ-UX-090 — The core loop is fully usable on a phone
- **statement**: On a phone-sized viewport in portrait, a signed-in person can complete the whole core
  loop — read the home timeline, compose and post a chirp, reply, like and unlike, follow and unfollow,
  and view a public profile — with no broken layout, no horizontally-clipped content, and no control that
  is off-screen or too small to operate.
- **acceptance_criteria**: On a 360×640 CSS-px portrait viewport, signed in: open and scroll the home
  timeline; open Compose and post a chirp; reply to a chirp; like then unlike a chirp; follow then
  unfollow an account; open a public profile. Every step completes, and at no step is there horizontal
  page scrolling, a control hidden off-screen, or an action target that cannot be tapped.
- **release_gating**: true
- **references**: REQ-PROD-035, REQ-PROD-001, REQ-PROD-002

#### REQ-UX-091 — One reading column, reflowed not rescaled, across viewports
- **statement**: The reading column is a single column at every viewport — filling the width inside the
  phone gutter on a compact screen and held to the 600px measure, centred, on wider screens — so content
  reflows to the available width and never requires horizontal scrolling or pinch-zoom to read.
- **acceptance_criteria**: Open the timeline at a 360px-wide viewport and at a 1280px-wide viewport. At
  360px the column fills the width inside a side gutter with no horizontal scrollbar; at 1280px the
  reading column is about 600px wide and centred, not stretched across the whole window. Neither width
  requires zooming or sideways scrolling to read a chirp.
- **release_gating**: true
- **references**: REQ-PROD-035, REQ-PROD-033

#### REQ-UX-092 — The signed-in navigation shell adapts and keeps every destination reachable
- **statement**: The signed-in navigation shell presents as a bottom tab bar with a slim top bar on a
  compact viewport and as a side navigation on medium and wide viewports; in every presentation Home,
  Explore, Notifications, Profile, Settings, and a Compose affordance are present and reachable, and the
  active destination is marked.
- **acceptance_criteria**: Signed in, at a phone width the primary destinations appear in a bottom bar
  reachable with the thumb and Compose is reachable without opening a menu; at a desktop width the same
  destinations appear in a persistent side navigation. At both widths, starting from the timeline, reach
  Home, Explore, Notifications, Profile, Settings, and Compose, and see the current destination marked.
- **release_gating**: true
- **references**: REQ-PROD-002, REQ-PROD-035

#### REQ-UX-093 — The signed-out shell never dead-ends at any viewport
- **statement**: On a compact viewport the signed-out navigation shell keeps the chirp wordmark, a Sign
  in entry, and a prominent Sign up entry visible without opening a menu, and keeps Rules & terms and
  Help & support reachable; a visitor on a shared public link reaches the content and a path to join at
  any width.
- **acceptance_criteria**: With no session, open the Landing and a public profile link at a phone width
  and at a desktop width. On each, Sign up and Sign in are visible without opening a menu, and Rules &
  terms and Help & support are reachable (by scrolling to the footer at minimum). No width presents an
  authentication wall or hides the join path.
- **release_gating**: true
- **references**: REQ-PROD-030, REQ-PROD-035

#### REQ-UX-094 — feed/list screens adapt without losing their controls
- **statement**: Every feed/list screen (home timeline, a chirp's conversation, notifications, search
  results, followers and following) is one column at every viewport, keeps its load-older and timeline
  catch-up affordances reachable, keeps each chirp card's reply/like/more controls tappable, and
  preserves the person's scroll place when they return from drilling into an item.
- **acceptance_criteria**: On a phone viewport, open a timeline longer than one page: the load-older
  control and the "N new chirps" catch-up are reachable without horizontal scrolling, and a chirp card's
  reply, like, and more controls are each tappable. Open a chirp, then press back; the timeline is
  restored at the prior scroll position.
- **release_gating**: true
- **references**: REQ-PROD-002, REQ-PROD-035

#### REQ-UX-095 — form screens are usable with the on-screen keyboard
- **statement**: Every form screen (sign up, sign in, recover access, set new credential, edit profile)
  stacks its text fields full-width within the gutter, keeps each field's label and its inline error with
  the field, and keeps the primary submit reachable when the on-screen keyboard is open; no form requires
  horizontal scrolling or a side-by-side layout on a phone.
- **acceptance_criteria**: On a phone viewport, open sign up and focus a field so the on-screen keyboard
  appears: the field, its label, and any error message are visible, and the submit can be reached (by
  scrolling the form) without dismissing the keyboard first. Submit an invalid field; its error shows
  with the field, not in a summary elsewhere. No field is cut off horizontally.
- **release_gating**: true
- **references**: REQ-PROD-008, REQ-PROD-035

#### REQ-UX-096 — profile and settings screens stack and keep their way back
- **statement**: On a compact viewport the profile header stacks avatar, display name, handle, bio, and
  counts with its context action (Follow, or Edit profile on one's own profile) visible, and the Settings
  hub and each sub-section are full screens with a labelled way back to the hub; a two-pane presentation
  is permitted on wide viewports but not required.
- **acceptance_criteria**: On a phone viewport open a public profile: the header's avatar, display name,
  bio, counts, and the Follow (or Edit profile) action are all visible without horizontal scrolling, with
  the chirps list in one column below. Open Settings, open a sub-section, and return: the sub-section is a
  full screen and a labelled back returns to the Settings hub.
- **release_gating**: true
- **references**: REQ-PROD-007, REQ-PROD-017, REQ-PROD-035

#### REQ-UX-097 — overlays present as full-height surfaces on a phone with their actions reachable
- **statement**: On a compact viewport the dialog's modal variant (Compose, Report) and confirmation
  variant (delete account, delete chirp, block or mute, end a session, sign out) present as a full-screen
  or bottom-sheet surface whose content and action pair are fully visible and operable — the confirm and
  the cancel/close are both reachable without being clipped — and the browser back control dismisses the
  overlay; on wider viewports the centred panel over the scrim is used.
- **acceptance_criteria**: On a phone viewport, open Compose: the compose box and its Post button are
  visible and usable with the keyboard open, and back closes it without leaving the underlying screen.
  Open a destructive confirmation: both the confirm and the cancel are fully visible and tappable, and
  neither is cut off at the screen edge.
- **release_gating**: true
- **references**: REQ-PROD-001, REQ-PROD-022, REQ-PROD-035

#### REQ-UX-098 — touch targets are large enough and reachable
- **statement**: On a touch viewport every interactive control presents a touch target of at least 44×44
  CSS px with at least 8px between adjacent targets, and the core-loop primary actions (the Compose
  affordance, a chirp card's like and reply, and primary navigation) sit within comfortable thumb reach
  rather than only at the top of a tall screen.
- **acceptance_criteria**: On a phone viewport, measure the tap targets of the Compose affordance, a chirp
  card's like and reply controls, and the primary navigation: each occupies at least 44×44 px and adjacent
  targets do not abut. The Compose affordance and primary navigation are reachable in the lower portion of
  the screen, not only at the top.
- **release_gating**: true
- **references**: REQ-PROD-035, REQ-PROD-033

#### REQ-UX-099 — no auto-zoom, no horizontal scroll, portrait and landscape
- **statement**: The product fits the viewport width at every supported size so the core loop needs
  neither pinch-zoom nor horizontal page scrolling, focusing a text field does not trigger the browser's
  automatic zoom, and the core loop works in both portrait and landscape on a phone.
- **acceptance_criteria**: On a phone viewport, walk the core loop in portrait and then in landscape: at
  no point does the page scroll horizontally or require a pinch-zoom, and focusing a sign-in or compose
  field does not zoom the page. Content reflows to the narrower dimension rather than overflowing it.
- **release_gating**: true
- **references**: REQ-PROD-035, REQ-PROD-033
