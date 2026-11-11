### Home timeline — the core reading surface

The **Home timeline** (`/` with a session, the **feed/list** archetype) is the screen chirp opens
to once a person is signed in, and it is the default thing a chirper does: read what is new from
themselves and the people they follow, newest first, and catch up on what arrived while they were
away. It is the most-visited screen in the product, so it has to paint fast, behave sensibly when
there is nothing yet to show, and recover in place when a page fails rather than dropping the reader
on a blank screen.

This design composes the frozen screen inventory and component library by name; it introduces no new
screen or component. The timeline is the signed-in **NavShell** wrapped around a **ListView** of
**ChirpCard**s held to the reading column, with the inventory's pagination and catch-up conventions
and the product-wide empty / loading / error patterns. The per-card actions (open conversation, like,
reply) are the **ChirpCard**'s own; they are designed by the posting-conversation and social-action
surfaces and only composed here.

#### Layout

The screen is the signed-in **NavShell** with the timeline content in the main region:

- **The shell** (`NavShell`, signed-in variant) is the persistent frame around the content: Home (the
  active destination, marked), Explore, Notifications, Profile, the always-available Compose
  affordance, and the account menu. The shell is persistent — moving to a conversation and back never
  blanks it. Marking Home as the current destination is the information architecture's wayfinding
  convention, composed here, not redefined.
- **The content region** is a single reading column held to the `space.measure` (600px) reading
  width, centred on wider viewports with the shell and any secondary rail outside it, and filling the
  viewport with a `space.gutter.mobile` (16px) gutter on a phone. How the shell and the column reflow
  across viewports is the responsive area's decision; this screen fixes the column, not the breakpoints.
- **The catch-up control** sits at the top of the content region, above the first card: a `ListView`
  catch-up affordance in `color.primary` reading "N new chirps", shown only when chirps have arrived
  since the person last looked. Selecting it brings those chirps in at the top and returns the reader
  to the newest.
- **The list** (`ListView`) fills the column below: a bounded page of `ChirpCard`s separated by the
  `color.border.default` hairline, newest first, with a **load-older** control (a `SecondaryButton` or
  text control) at the bottom boundary of the loaded page.

#### Content

- **Order and membership.** The list holds the person's own chirps and those of the accounts they
  follow, newest first. It is not a ranked or algorithmic feed; recency is the order, which is what the
  product requirement fixes and what a reader catching up expects.
- **Each row** is a `ChirpCard` showing, from the component library: the author's `Avatar`
  (`avatar.md`), display name (`type.heading`), handle and a short relative timestamp (`2m`, `4h`,
  then an absolute date) in `type.meta` / `color.text.secondary`, the chirp text in `type.body`, and
  the card's action row (reply, like, more-actions). The whole card is the target that opens the chirp
  in its conversation. Those per-card actions are the `ChirpCard`'s own behaviour; this screen places
  the card and does not redesign them.
- **Bounded pages, not an unbounded load.** The list loads one bounded page and offers an explicit way
  to load older chirps at the boundary; it never attempts to load every chirp at once. The pagination
  convention (bounded pages, an opaque cursor, an explicit load-older) is set by the information
  architecture (REQ-UX-010) and composed here.
- **Catch-up after an absence.** When chirps have been posted since the reader last opened the
  timeline, the top-of-list catch-up control offers to pull them in as a bounded step, so a long
  absence is a bounded catch-up rather than an endless scroll. This, too, is the IA's catch-up
  convention, composed, not redefined.
- **Scroll place is kept.** Returning from a chirp's conversation lands the reader back at their place
  in the list rather than at the top — the `ListView`'s scroll-restoration behaviour, which the IA's
  back-and-forward convention (REQ-UX-009) also requires.

#### Primary action

The screen's one prominent, screen-level action is **bring the timeline current and read the newest
chirps**: when there is new activity, the catch-up control ("N new chirps") is the primary action a
reader reaches for; when there is none, the primary act is to read and scan the page. Loading older
chirps is the secondary action at the list boundary. Composing is always available from the shell's
Compose affordance (the IA's persistent compose convention) rather than being a control this screen
owns, so the reading surface stays a reading surface.

#### States

The timeline's empty, error, and loading states are the relevant components' own named states
(`ListView`, `ChirpCard`, `EmptyState`, `LoadingState`, `InlineError`) composed with the product-wide
empty / loading / error patterns. They are not new treatments invented for this screen.

**Empty — a brand-new timeline that explains and points onward.** A reader who follows no one and has
posted nothing has an empty timeline. The `ListView` *empty* state shows the `EmptyState` block — a
calm illustration, one line explaining that the timeline fills as they follow people and post, and a
next step: a link to **Explore** to find people and a way to compose a first chirp. It is never a
blank region and never a spinner that has finished on nothing. First-run **Onboarding** (`/welcome`)
is the account-lifecycle surface that greets a newly-created account and moves it off the empty state;
this screen designs only the timeline's own empty treatment and leaves onboarding to that surface, so
a reader who lands on an empty timeline later (for example after unfollowing everyone) meets the same
explained empty state rather than nothing.

**Error — a failed page or catch-up fetch, recovered in place.** A failure is shown where it happened,
in plain words, with a retry, and already-shown chirps are never discarded:

- A **first page** that fails to load shows the `ListView` *error*: an `InlineError` with a retry in
  place of the missing list, distinct from the empty treatment so "we couldn't load this" and "there
  is nothing here" are never confused.
- A failure while **loading older** chirps shows the `InlineError` at the load-more boundary and keeps
  the chirps already on screen; the reader retries from the boundary without losing their place.
- A failed **catch-up** fetch shows the failure on the catch-up control with a retry and leaves the
  current list intact, so a broken catch-up never clears what the reader was already reading.
- An **expired session** met on the timeline is the product-wide expiry pattern, not a timeline-local
  error: the reader is routed to **Sign in** with the reason stated and returned to the timeline at
  their place afterwards (the IA's session-expiry and auth-gated-return conventions, REQ-UX-008 /
  REQ-UX-007). The timeline does not dress an expiry up as a retryable load error.

**Loading — the shape of the page, not a spinner on a blank screen.** A **first load** shows
`LoadingState` skeleton rows at the real dimensions of a `ChirpCard` — a skeleton avatar circle, two
text lines, and a short meta line — so the column does not jump when real chirps arrive and the reader
sees the page forming. Loading **older** chirps shows a bounded spinner at the list's load-more
boundary with the already-loaded chirps left in place. The persistent `NavShell` never participates in
loading — only the content region shows a loading state; the frame around it stays put. Nothing spins
forever: a load that does not resolve hands off to the list's *error* state with a retry. Under a
reduced-motion preference the skeletons are static and the spinner stays bounded, so the loading state
never relies on movement to be understood.

---

### Requirements and acceptance criteria — REQ-UX-051..053

Each requirement is testable by someone who never met the author, exercisable on the live product,
carries a `release_gating` flag, and references the product requirement(s) it serves.

#### REQ-UX-051 — The home timeline reads own and followed chirps, newest first, in bounded pages
- **statement**: The signed-in home timeline shows the person's own chirps and those of the accounts
  they follow, ordered newest first, loaded in bounded pages with an explicit way to load older
  chirps — never as a single unbounded load — inside the persistent signed-in shell with Home marked
  as the current destination.
- **acceptance_criteria**: Signed in and following at least one account that has posted, open `/`: the
  timeline shows recent chirps from you and the people you follow, newest first, as a bounded page,
  with the Home destination marked in the shell. Use the load-older control; older chirps load as a
  further bounded page and the product does not attempt to fetch every chirp at once.
- **release_gating**: true
- **references**: REQ-PROD-002

#### REQ-UX-052 — A catch-up affordance brings in chirps posted since the last look
- **statement**: When chirps have been posted since the person last viewed the timeline, the screen
  offers a catch-up control ("N new chirps") at the top of the list that pulls those chirps in as a
  bounded step and returns the reader to the newest, so a long absence is a bounded catch-up rather
  than an endless scroll; returning from a chirp's conversation keeps the reader's place in the list.
- **acceptance_criteria**: Open the timeline, then have another account you follow post while it is
  open: a catch-up control stating how many new chirps are available appears at the top. Select it;
  the new chirps load in at the top without an unbounded scroll. Open a chirp from the list and press
  back; you return to the timeline at the position you left, not at the top.
- **release_gating**: true
- **references**: REQ-PROD-002

#### REQ-UX-053 — The timeline has designed empty, error, and loading states
- **statement**: The timeline presents a designed empty state (a brand-new or emptied timeline
  explains why it is empty and points to Explore and to composing a first chirp, never a blank), a
  designed error state (a failed first page, a failed load-older, or a failed catch-up is shown in
  place with a retry and already-loaded chirps are not discarded), and a designed loading state (a
  first load shows skeleton rows at real card dimensions, not a spinner on a blank screen; loading
  older shows a bounded spinner at the boundary; the navigation frame never blanks and nothing spins
  forever).
- **acceptance_criteria**: With an account that follows no one and has posted nothing, open the
  timeline: it explains the empty state and offers a route to Explore and to composing, rather than a
  blank area. Force the first page to fail: a plain-words message with a retry is shown in place of
  the list, visibly different from the empty state. Force a load-older to fail: the failure shows at
  the boundary and the chirps already on screen remain. Open the timeline on a slow connection: the
  content region shows skeleton rows at the size of real chirps while the shell stays visible.
- **release_gating**: true
- **references**: REQ-PROD-002

---

*Composition note: this surface composes the frozen screen inventory (Home timeline, `/`, feed/list)
and component library (`NavShell`, `ListView`, `ChirpCard`, `EmptyState`, `LoadingState`,
`InlineError`, `Avatar`) by name, the information architecture's pagination / catch-up / back and
session-expiry conventions (REQ-UX-010, REQ-UX-009, REQ-UX-008, REQ-UX-007), and the product-wide
empty / loading / error patterns (REQ-UX-086..089) — none redefined.*
