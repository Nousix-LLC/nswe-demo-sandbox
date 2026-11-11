# Core loop — screens and flows

This section covers the social loop a chirper runs every day: reading the home timeline, composing and
posting, reading and replying in a conversation, deleting one's own chirp, liking, following, finding
people to follow, and viewing a profile. Each surface is designed as a screen or control with layout,
content, a primary action, and the empty, error, and loading states it meets in ordinary use, not a route
with a name under it.

Everything here composes two vocabularies that are frozen upstream and are referred to by name, never
redefined: the **screen inventory** (Home timeline, Compose, Chirp / conversation, Delete chirp, Explore /
find people, Public profile, Own profile, Followers, Following, with their routes and auth states) and the
**component library** (`NavShell`, `ListView`, `ChirpCard`, `ComposeBox`, `ProfileHeader`, `Avatar`,
`IconButton`, `PrimaryButton`, `SecondaryButton`, `TextField`, `Dialog`, `Toast`, `InlineFeedback`,
`InlineError`, `EmptyState`, `LoadingState`, and their named states). A screen's empty, error, and loading
states are the relevant components' own named states composed with the product-wide empty / loading /
error patterns and the expired-session / keep-the-draft recovery set out in the states section; they are
not treatments invented per screen. The surfaces are presented in the order a chirper lives them: reading,
writing, reacting, identity and finding. The requirements register (`REQ-UX-051..064`) follows the
screens.

---

## Home timeline — the core reading surface

The **Home timeline** (`/` with a session, the **feed/list** archetype) is the screen chirp opens to
once a person is signed in, and it is the default thing a chirper does: read what is new from themselves
and the people they follow, newest first, and catch up on what arrived while they were away. It is the
most-visited screen in the product, so it has to paint fast, behave sensibly when there is nothing yet to
show, and recover in place when a page fails rather than dropping the reader on a blank screen.

The timeline is the signed-in **NavShell** wrapped around a **ListView** of **ChirpCard**s held to the
reading column, with the inventory's pagination and catch-up conventions and the product-wide
empty / loading / error patterns. The per-card actions (open conversation, like, reply) are the
**ChirpCard**'s own; they are designed in the Posting and conversation and Social actions sections below and
only composed here.

### Layout

The screen is the signed-in **NavShell** with the timeline content in the main region:

- **The shell** (`NavShell`, signed-in variant) is the persistent frame around the content: Home (the
  active destination, marked), Explore, Notifications, Profile, the always-available Compose affordance,
  and the account menu. The shell is persistent — moving to a conversation and back never blanks it.
  Marking Home as the current destination is the information architecture's wayfinding convention,
  composed here, not redefined.
- **The content region** is a single reading column held to the `space.measure` (600px) reading width,
  centred on wider viewports with the shell and any secondary rail outside it, and filling the viewport
  with a `space.gutter.mobile` (16px) gutter on a phone. How the shell and the column reflow across
  viewports is the responsive area's decision; this screen fixes the column, not the breakpoints.
- **The catch-up control** sits at the top of the content region, above the first card: a `ListView`
  catch-up affordance in `color.primary` reading "N new chirps", shown only when chirps have arrived
  since the person last looked. Selecting it brings those chirps in at the top and returns the reader to
  the newest.
- **The list** (`ListView`) fills the column below: a bounded page of `ChirpCard`s separated by the
  `color.border.default` hairline, newest first, with a **load-older** control (a `SecondaryButton` or
  text control) at the bottom boundary of the loaded page.

### Content

- **Order and membership.** The list holds the person's own chirps and those of the accounts they
  follow, newest first. It is not a ranked or algorithmic feed; recency is the order, which is what the
  product requirement fixes and what a reader catching up expects.
- **Each row** is a `ChirpCard` showing, from the component library: the author's `Avatar`, display name
  (`type.heading`), handle and a short relative timestamp (`2m`, `4h`, then an absolute date) in
  `type.meta` / `color.text.secondary`, the chirp text in `type.body`, and the card's action row (reply,
  like, more-actions). The whole card is the target that opens the chirp in its conversation. Those
  per-card actions are the `ChirpCard`'s own behaviour; this screen places the card and does not redesign
  them.
- **Bounded pages, not an unbounded load.** The list loads one bounded page and offers an explicit way to
  load older chirps at the boundary; it never attempts to load every chirp at once. The pagination
  convention (bounded pages, an opaque cursor, an explicit load-older) is set by the information
  architecture and composed here.
- **Catch-up after an absence.** When chirps have been posted since the reader last opened the timeline,
  the top-of-list catch-up control offers to pull them in as a bounded step, so a long absence is a
  bounded catch-up rather than an endless scroll. This, too, is the IA's catch-up convention, composed,
  not redefined.
- **Scroll place is kept.** Returning from a chirp's conversation lands the reader back at their place in
  the list rather than at the top — the `ListView`'s scroll-restoration behaviour, which the IA's
  back-and-forward convention also requires.

### Primary action

The screen's one prominent, screen-level action is **bring the timeline current and read the newest
chirps**: when there is new activity, the catch-up control ("N new chirps") is the primary action a
reader reaches for; when there is none, the primary act is to read and scan the page. Loading older
chirps is the secondary action at the list boundary. Composing is always available from the shell's
Compose affordance (the IA's persistent compose convention) rather than being a control this screen owns,
so the reading surface stays a reading surface.

### States

The timeline's empty, error, and loading states are the relevant components' own named states
(`ListView`, `ChirpCard`, `EmptyState`, `LoadingState`, `InlineError`) composed with the product-wide
empty / loading / error patterns. They are not new treatments invented for this screen.

**Empty — a brand-new timeline that explains and points onward.** A reader who follows no one and has
posted nothing has an empty timeline. The `ListView` *empty* state shows the `EmptyState` block — a calm
illustration, one line explaining that the timeline fills as they follow people and post, and a next
step: a link to **Explore** to find people and a way to compose a first chirp. It is never a blank region
and never a spinner that has finished on nothing. First-run **Onboarding** (`/welcome`) is the
Onboarding screen that greets a newly-created account and moves it off the empty state; this
screen designs only the timeline's own empty treatment and leaves onboarding to that surface, so a reader
who lands on an empty timeline later (for example after unfollowing everyone) meets the same explained
empty state rather than nothing.

**Error — a failed page or catch-up fetch, recovered in place.** A failure is shown where it happened, in
plain words, with a retry, and already-shown chirps are never discarded:

- A **first page** that fails to load shows the `ListView` *error*: an `InlineError` with a retry in
  place of the missing list, distinct from the empty treatment so "we couldn't load this" and "there is
  nothing here" are never confused.
- A failure while **loading older** chirps shows the `InlineError` at the load-more boundary and keeps
  the chirps already on screen; the reader retries from the boundary without losing their place.
- A failed **catch-up** fetch shows the failure on the catch-up control with a retry and leaves the
  current list intact, so a broken catch-up never clears what the reader was already reading.
- An **expired session** met on the timeline is the product-wide expiry pattern, not a timeline-local
  error: the reader is routed to **Sign in** with the reason stated and returned to the timeline at their
  place afterwards (the IA's session-expiry and auth-gated-return conventions). The timeline does not
  dress an expiry up as a retryable load error.

**Loading — the shape of the page, not a spinner on a blank screen.** A **first load** shows
`LoadingState` skeleton rows at the real dimensions of a `ChirpCard` — a skeleton avatar circle, two text
lines, and a short meta line — so the column does not jump when real chirps arrive and the reader sees
the page forming. Loading **older** chirps shows a bounded spinner at the list's load-more boundary with
the already-loaded chirps left in place. The persistent `NavShell` never participates in loading — only
the content region shows a loading state; the frame around it stays put. Nothing spins forever: a load
that does not resolve hands off to the list's *error* state with a retry. Under a reduced-motion
preference the skeletons are static and the spinner stays bounded, so the loading state never relies on
movement to be understood.

---

## Posting and conversation

This section covers where a chirper writes and reads what was written in context:
composing and publishing a chirp inside the 280-character limit, and the Chirp / conversation screen
where a chirp is read alongside the chirp it answers and its replies, and where a reply is written. Two
surfaces are designed here — a writing surface and a reading-in-context screen — each with its layout,
content, primary action, and its empty, error, and loading states. The single writing control,
**ComposeBox**, is designed once in the compose surface and composed by name in the conversation screen's
reply slot.

### Compose and post a chirp

Writing a chirp is the first thing chirp exists for, and it is the surface a new person uses before they
have followed anyone or read a timeline worth reading. This section designs that surface: where a person
writes a chirp, how the product keeps them inside the published 280-character limit while they type, how
the "Post" action behaves, and what the surface looks like when it is empty, when something is wrong, and
while a chirp is being published.

The surface is one component — **ComposeBox** — shown in three places. It is designed once here, with its
counter, its limit behaviour, its primary action, and its empty, error, and loading states, and the same
component is placed inline at the top of the **Home timeline**, as the body of the **Compose** dialog
(`/compose` and the overlay dialog), and in the reply position on the **Chirp / conversation** screen.
The conversation screen composes the reply-position variant designed here rather than defining its own
writing field.

This surface serves journey J4 step 2 (compose and post). The reply-position variant also carries the
writing half of replying; the conversation screen owns the rest of that flow.

#### Layout and content

The **ComposeBox** reads top to bottom as one block, the same in every placement:

- the composing person's **Avatar** at the leading edge, so a person sees whose voice the chirp will
  carry — this matters most in the reply position, where the draft sits among other people's chirps;
- the **draft field** — a multi-line text area on the `color.bg.subtle` draft surface, holding the chirp
  text in `type.body`, growing with the content rather than scrolling a fixed box, with a placeholder
  prompt when empty;
- the **remaining-character affordance** — a live count of characters still available, in `type.caption`
  with `type.numeral.tabular` figures so the number does not shift the layout as it changes;
- the **primary action** — a **PrimaryButton** labelled for the placement ("Post" when writing a new
  chirp, "Reply" in the conversation's reply position).

The draft field is the focus of the surface and takes the most width; the avatar, counter, and action sit
around it without competing for attention. In the dialog placement the box is the dialog's content and
the action pair sits at the dialog's foot; inline and in the reply position the action sits with the box.
Nothing else lives in this surface — no formatting toolbar, no media controls, no audience picker —
because a chirp in this product is plain text up to 280 characters, and the surface shows only what that
needs.

#### The character budget, enforced before submission

The product does not let a person write past the limit and only discover it when they try to post. The
counter is live: as the person types, the remaining-character count updates, and it changes appearance
before and at the boundary so the limit is felt, not just stated.

- While there is comfortable room, the counter is quiet (`color.text.secondary`), showing the number of
  characters still available.
- As the draft **nears** the limit, the counter moves to the warning role (`color.warning`) so the
  person sees the boundary coming while they still have room to adjust.
- When the draft is **over** the limit, the counter moves to the danger role (`color.danger`), the
  over-limit characters are distinguished in the field so the person can see exactly what to cut, and the
  primary action is disabled.

The primary action is disabled whenever the draft is empty or over the limit, so the ordinary way to
reach an invalid post — an empty field or too many characters — is closed before the person can act on
it. If an empty or over-limit submit is reached by any other route (a keyboard shortcut, say), it is
rejected and no chirp is created. The limit value shown and enforced is the product's published 280,
which the ComposeBox reads from the product requirement rather than inventing.

Colour never carries the limit state on its own: the warning and danger states of the counter are a
colour **and** the changing number (and, over the limit, the marked-over characters and the disabled
action), so a person who does not distinguish the colours still sees the boundary.

#### The primary action

The primary action is a single **PrimaryButton**, one per surface, labelled with the verb for what it
does — "Post" for a new chirp, "Reply" in the conversation's reply position — never a bare "Submit" or
"OK". It has three conditions a person can reach:

- **disabled** — the draft is empty or over the limit; the button reads as inactive and cannot be
  triggered. This is the resting state of an empty compose surface.
- **ready** — the draft holds between one character and the limit; the button is active and posting is
  the obvious next step.
- **busy** — a publish is in flight; the button shows its loading state in place, holding its label and
  width so the surface does not jump, and it cannot be triggered again.

In the **Compose** dialog the primary action is paired with a **SecondaryButton** ("Cancel") and a close
control, following the Dialog's action-pair convention; inline and in the reply position the primary
action stands with the box and the person leaves the draft by navigating away (which preserves it,
below).

#### States

The surface is designed for the states a person actually meets, not only the happy path. Each state below
is the relevant component's own named state, composed here. Where a failure needs to keep a person's
draft safe, this surface composes the product-wide keep-the-draft recovery rather than redefining it.

**Empty.** No text yet. The draft field shows a placeholder prompt ("What's happening?" for a new chirp;
a reply placeholder that names who is being answered in the reply position), the counter sits at the full
budget, and the primary action is disabled. The empty surface is calm and ready, not an error — a person
who has not typed anything has done nothing wrong, so nothing is marked red. This is the ComposeBox
*empty* state with the PrimaryButton in its *disabled* state.

**Error.** Two different things can be wrong, and they are shown differently because the person does
something different about each:

- *Over the limit* — the draft is longer than 280 characters. This is shown while typing: the counter is
  in the danger role, the over-limit characters are distinguished in the field, and the primary action is
  disabled. There is no separate error message to dismiss; the fix is visible in the field and the
  counter, and the person edits the draft down. This is the ComposeBox *error* state for the over-limit
  case.
- *The publish failed* — the person posted a valid draft and the publish did not succeed (the network
  dropped, the server refused, the session expired mid-submit). The draft is kept exactly as written, an
  **InlineError** appears below the field in plain words with a way to try again, and the primary action
  returns to its ready state so the person can retry without retyping. A failed publish never clears or
  loses the draft. When the cause is an expired session, the surface follows the product's session-expiry
  convention — the person is routed to sign in with the reason stated, their draft is preserved, and they
  return to it afterwards. In the **Compose** dialog this error shows inside the panel and the dialog
  stays open with the draft intact, per the Dialog's *error* state.

**Loading.** A publish is in flight. The primary action shows its busy state and the draft field locks
briefly so the chirp cannot be edited or submitted again mid-publish — this is what stops a double tap
from posting the same chirp twice. The lock is brief and tied to the in-flight publish, not a general
disabling of the surface. This is the ComposeBox *loading* state with the PrimaryButton in its *loading*
state. On success the chirp is published, the field clears to its empty state, and the result is
confirmed with a brief, non-blocking **Toast** ("Chirp posted") that does not interrupt what the person
does next; the new chirp appears in the places the timeline and conversation screens own. On failure the
surface moves to the publish-failed error above.

#### The three placements

The same ComposeBox, with everything above, appears in three places. The behaviour — the counter, the
280-character limit, the disabled/empty/error/loading treatment, and the keep-the-draft recovery — is
identical in all three; what differs is where the box sits and what its action is called.

- **Inline, at the top of the Home timeline.** The box sits above the timeline feed so a signed-in person
  can write without leaving home. Its action is "Post"; on success the posted chirp appears at the top of
  the timeline and the box returns to empty.
- **The Compose dialog (`/compose` and the overlay dialog).** The box is the body of the **Dialog**
  (modal variant), reachable from the always-available compose affordance in the signed-in **NavShell**
  and directly at the `/compose` URL. The dialog traps focus while open, the browser back control
  dismisses it (closing the dialog, not leaving the underlying screen), and a dismissed dialog with a
  non-empty draft follows the keep-the-draft convention rather than discarding the writing. Its action is
  "Post".
- **The reply position on the Chirp / conversation screen.** The box sits in the conversation's reply
  slot, its placeholder names the chirp being answered, and its action is "Reply". The **Chirp /
  conversation** screen composes this variant by name; the counter, the limit, the disabled/error/loading
  behaviour, and the keep-the-draft recovery are all as designed here. Posting a reply from this position
  is the writing half of replying; the conversation screen owns reading the conversation and reporting a
  reply to a chirp that is gone.

### The Chirp / conversation screen — reading in context and replying

This is the screen where a single chirp is read together with the chirp it answers and the replies it
received, and where a reply is written. It is the second half of the core loop's writing-and-reading
surfaces: the compose/post surface above is where a chirp starts; this screen is where a chirp is read in
the conversation it belongs to and answered. It is reached by opening a chirp from the timeline, a
profile, a notification, or a shared link, and it has a stable address so any of those routes — and an
outside link — land on the same place.

The bar here is a designed screen, not a route with a list under it: the focused chirp, the chirp it
answers, the replies, and the place to reply are all laid out and specified, and the screen is designed
for the cases that are not the happy path — a chirp with no replies yet, a chirp that has been removed, a
page that fails to load, and the moment before anything has loaded at all.

The reply control is the shared **ComposeBox** in its reply-position placement — it is composed here by
name, and its character counter, its 280-character limit, its disabled/empty/error/loading behaviour, and
its keep-the-draft recovery are the component library's and the compose/post surface's to specify, not
this screen's.

#### Screen

- **Inventory name**: Chirp / conversation
- **Route**: `/@:handle/chirp/:id` — a stable, shareable address (per the IA's addressable-chirp
  convention); opening it directly lands the person on this chirp in its conversation, not on a generic
  home.
- **Archetype**: feed/list
- **Auth**: both — it renders inside the **signed-out shell** for a visitor on a shared link and inside
  the **signed-in shell** for a member. The conversation reads the same in both; the one difference is
  the reply slot (below).
- **Reached from**: a **ChirpCard** opened in the home timeline, a profile, the notifications list,
  search results, or an outside link. Per the IA wayfinding convention the screen offers a labelled way
  back to where the person came from, and the browser back control returns them to that place without
  re-submitting anything and without losing their scroll position in the list they left.

#### Layout (default)

Top to bottom, within the appropriate **NavShell**:

1. **Wayfinding** — the shell marks where the person is; the document title and the main heading name the
   screen (the focused chirp's author and a short form of its text), and a labelled back control sits at
   the top of the content column (per the IA back/wayfinding convention — composed, not redesigned here).
2. **The chirp being answered (parent context)** — when the focused chirp is itself a reply, the chirp it
   answers is shown directly above it as a **ChirpCard**, introduced by a quiet relation line ("Replying
   to @handle"). The parent card is a target that opens *its* conversation, so a person can walk up the
   thread one step. When the focused chirp is a top-level chirp (answers nothing), this region is simply
   absent — not an empty slot.
3. **The focused chirp** — the subject of the screen, rendered as a **ChirpCard** given the visual weight
   of the thing the screen is about (the root of this view): author **Avatar**, display name, handle,
   relative timestamp, the chirp text, and the action row (**IconButton**s for reply, like, and
   more-actions; on the person's own chirp the more-actions menu opens **Delete chirp**, designed above). The reply action here scrolls to and focuses the reply slot below.
4. **The reply slot** — the primary writing affordance on this screen:
   - *Signed in*: the shared **ComposeBox** in its reply-position placement, pre-framed with "Replying to
     @handle" so it is clear what the reply answers, and carrying its own "Reply" **PrimaryButton**. The
     box, its counter, its limit, and its keep-the-draft behaviour are composed by name from the component
     library and the compose/post surface — not restated here.
   - *Signed out*: the box is replaced by a short "Sign in to reply" prompt leading to **Sign in** /
     **Sign up** in the signed-out shell, so a visitor who wants to answer is given the path to an account
     rather than a dead control or a silent one. (This composes the **ComposeBox**'s "composing not
     permitted in the current state" case together with the signed-out shell's own entries.)
5. **The replies** — a **ListView** of **ChirpCard**s, in oldest-first (chronological) order so the
   exchange reads the way it happened, with a reply count heading it ("12 replies"). It loads in bounded
   pages with the IA's load-older affordance for a long thread; it is never one unbounded load. Each reply
   card is a target that opens that reply in its own conversation, so a reply with replies of its own can
   be drilled into.

#### Content

- The focused chirp and every reply show author name, handle, relative timestamp (`2m`, `4h`, then an
  absolute date), and text, from the **ChirpCard** vocabulary.
- The parent-context relation ("Replying to @handle") and, on a reply card, the same relation where a
  reply answers another reply, so a reply is always presented as answering its parent rather than
  stranded in a flat list.
- The reply count above the list.
- In the reply slot, the "Replying to @handle" framing and the live remaining-character affordance that
  the **ComposeBox** owns.

#### Primary action

**Reply** — writing and publishing a reply from the reply slot, via the **ComposeBox**'s "Reply"
**PrimaryButton**. A published reply records the chirp it answers and appears in the replies list in its
chronological place; brief non-blocking feedback (the **Toast** / **InlineFeedback** pattern) confirms
it, per the product-wide "the result of every action is shown" convention.

#### States

- **empty** — a chirp that has no replies yet. The focused chirp and any parent context render normally;
  the replies region shows the **ListView** *empty* state as an **EmptyState** block that invites the
  first reply ("No replies yet — be the first to reply") and points at the reply slot, rather than a blank
  area. The reply slot (the **ComposeBox**, signed in) is present as the next step, so an empty
  conversation still offers the one thing to do on it. A signed-out visitor sees the "Sign in to reply"
  prompt in that position, so the next step is signing in or signing up.
- **error** — three distinct failures, each shown where it happens rather than as a silent drop:
  - *The focused chirp has been removed* (deleted, blocked, or otherwise unavailable): it renders as the
    **ChirpCard** *error* tombstone ("This chirp isn't available") in place of the card, rather than an
    empty gap, and the reply slot is withdrawn, because there is nothing to answer. The replies that were
    already part of the thread stay visible around the tombstone. This is the in-place treatment for a
    removed chirp inside a thread. An address with no thread context (a chirp id that never resolves, or
    a link to a chirp that was removed before anything could be shown) goes to the inventory's **Not
    found** screen, which states "This chirp isn't available" and routes the person back to a known
    place.
  - *Replying to a chirp that has gone away between opening the screen and sending* (the parent was
    deleted while the reply was being written): the reply is reported through an
    **InlineError** at the **ComposeBox** reading "This chirp isn't available" (and the focused chirp
    flips to the tombstone), and the draft is kept so the words are not lost — never a reply that appears to send into nothing.
  - *The replies fail to load* while the focused chirp loaded fine: the **ListView** *error* state shows
    an **InlineError** with a retry in place of the missing replies; the focused chirp, the parent
    context, and the reply slot stay usable, and a failure while loading *older* replies shows at the
    load-more boundary without discarding the replies already on screen.
- **loading** — the first load shows the **LoadingState** skeleton rather than a spinner on a blank
  screen: a skeleton **ChirpCard** at the focused chirp's real dimensions (and one in the parent-context
  slot when the chirp is known to be a reply), and **ListView** skeleton reply rows, so the layout does
  not jump when the content arrives. The reply slot renders immediately — the **ComposeBox** needs no data
  to appear — so the person can begin writing before the replies finish loading.

A failed reply publish keeps the draft, and an expired session mid-reply routes to sign-in with the
reason stated and the draft preserved, returning the person here afterwards — both are composed from the
product-wide treatment and the **ComposeBox**'s own behaviour, not reinvented on this screen.
Addressability, deep-linking, pagination/catch-up, and back/forward behaviour are the IA's conventions,
applied here by name.

### Delete chirp

The **Delete chirp** dialog (inventory: confirmation, signed-in) is how a person removes a chirp they
posted. It is a **Dialog** in its confirmation variant, so it names the consequence plainly, always offers
a clear way out, and never removes anything until the person confirms.

**Where it opens.** From the more-actions menu of a person's own **ChirpCard**, wherever that card is drawn:
the Home timeline, the Chirp / conversation screen, and Own profile. The menu entry is labelled "Delete
chirp". Another person's card never offers it; the menu on those cards carries the actions that apply to
other people's chirps.

**Layout and content.**

- Title (`type.heading`): "Delete this chirp?"
- A compact preview of the chirp, its text and relative timestamp, so the person can see which chirp is
  about to go. Long text is shortened to its first lines in the preview.
- Consequence line (`type.body`): "This removes the chirp from your profile and from everyone's timelines.
  Replies to it stay, and show 'This chirp isn't available' where it was. This can't be undone."
- The **Dialog** action pair: a destructive **PrimaryButton** in `color.danger` labelled "Delete chirp"
  (a verb and its object, never "OK"), and a **SecondaryButton** "Cancel". The close **IconButton** does
  the same as Cancel.
- No acknowledgement checkbox. Removing one chirp is a small, contained loss, and the preview plus the
  stated consequence is the safeguard; the acknowledgement control is reserved for Delete account.

**Primary action.** Delete the chirp. Initial focus lands on "Cancel", not on the destructive action, so a
stray Enter keypress does not delete anything. Focus is trapped while the dialog is open, Escape and the
browser back control dismiss it without deleting, and focus returns to the control that opened it.

**States.** These are the **Dialog** component's own named states.

- **Default.** The panel is open over the dimmed screen with the preview, the consequence line, and both
  buttons active.
- **Disabled.** Does not apply. The confirm needs no required input, so it is active as soon as the dialog
  opens.
- **Empty.** Does not apply. The dialog always opens with its content.
- **Loading.** The person confirmed and the delete is running. The "Delete chirp" button shows its busy
  state, holding its label and width. The dialog does not close until the request resolves, and a second
  activation of the button does nothing, so one delete is sent.
- **Error.** The delete failed (the network dropped, the server refused). An **InlineError** appears inside
  the panel in plain words: "We couldn't delete this chirp. It's still there. Try again." The dialog stays
  open, the chirp stays in place on the screen behind it, and the confirm button returns to its active
  state as the retry. Cancel remains available. An expired session is the product-wide expiry pattern:
  the person is routed to Sign in with the reason stated and returned to the chirp afterwards, with
  nothing deleted.

**On success.** The dialog closes and a brief **Toast** reads "Chirp deleted". The result is shown where
the person was:

- On the Home timeline and on Own profile, the card leaves the list in place and focus moves to the next
  card (or to the list heading if it was the last).
- On the Chirp / conversation screen, when the deleted chirp is the focused one, the screen shows the
  "This chirp isn't available" tombstone with its replies still listed, the same in-place treatment any
  viewer of that thread would see. When it was one of the replies, that reply leaves the list.

If the chirp was already gone when the person confirms (deleted from another device, say), the delete is
treated as done: the dialog closes, the card is removed as above, and no error is shown. A delete is never
reported as failed when the chirp is no longer there.

---

## Social actions — the in-place like and follow controls

Liking a chirp and following a person are the two reactions in the core loop. Neither is a screen: each
is a control that lives on another screen's component — the like control on every **ChirpCard**, the
follow control on a **ProfileHeader** and on the person rows the discovery and list screens present. This
part specifies how those two controls read and behave wherever they appear, built from the frozen
component library and composed against the per-screen states its components already carry. It does not
redefine **ChirpCard**, **ProfileHeader**, **IconButton**, **PrimaryButton**, **SecondaryButton**, or
**InlineFeedback**, and it does not design the cards, headers, or lists the controls sit on — those are
the timeline, conversation, profile, and discovery surfaces.

### The behaviour both controls share

Both controls act in place — the person stays on the screen they are on, and nothing navigates. Both are
**idempotent**: the control holds exactly two mutually exclusive states (liked / not-liked; Following /
not-following), so repeating the same intent cannot stack. The value the control shows is the resolved
result, not a client-side tally — a like count is the server's count for that chirp, and a follow is
either on or off, never counted twice.

The response is immediate and optimistic, then reconciled:

- On activation the control flips to the target state at once (the heart fills and the count moves; the
  button becomes "Following") and shows its own in-flight **loading** treatment while the change settles.
- On success the optimistic state stands; the state change is itself the confirmation, so no extra toast
  is raised for a result that already shows on the control (per the product's transient-feedback
  convention, a result that belongs against a specific control is shown at that control, not in a
  **Toast**).
- On failure the optimistic change is reverted — the control returns to the state it held before, and any
  count returns to its prior value — and an **InlineFeedback** in the danger role appears at the control,
  in plain words, with the action still available to retry. The control never shows a like or a follow
  that did not take.

Meaning is never carried by colour alone: every active state is a colour together with an icon or a
label, matching the library's rule for its components.

### Like / unlike

**Where it sits.** The like control is the like **IconButton** in the action row of every **ChirpCard** —
the same control wherever a ChirpCard is drawn: the Home timeline, the Chirp / conversation screen, a
profile's chirps, and search and notification results. It reads and behaves identically in all of them.

**Content.** The heart **IconButton** and, beside it, the chirp's like count in tabular numerals so a
changing count does not shift the row. The control exposes a text label to assistive technology in both
states ("Like" / "Liked").

**Primary action.** Toggle this chirp's like for the signed-in person: like it when not liked, unlike it
when liked.

**States.**

- **default / active.** Two states. *Not liked* — the outline heart at rest, the current like count.
  *Liked* — the active treatment the **ChirpCard** defines: `color.like`, a filled heart, and a "Liked"
  label together (never colour alone), with the count raised by this person's like. The two states are
  mutually exclusive, which is what makes a second "like" impossible — activating an already-liked control
  unlikes it rather than liking again, so the count cannot double-count.
- **error.** A like or unlike that fails: the optimistic flip is reverted (the heart returns to its prior
  fill, the count returns to its prior value) and the like **IconButton** shows **InlineFeedback** in the
  danger role at the control with a plain reason and a retry. The count shown always matches the result
  that actually happened.
- **loading.** The request is in flight: the like **IconButton** shows its own busy treatment (a bounded
  spinner in place of the heart) and is not re-triggerable until it resolves, so a rapid double activation
  cannot post two conflicting changes.

### Follow / unfollow

**Where it sits.** The follow control is the context action on a **ProfileHeader** and the follow action
on each person row the Explore / find-people, Followers, and Following screens present (those rows are the
discovery-and-lists surface; this section specifies only the control that sits on them). It is the same
control in every place.

**Content.** A single context action: a **PrimaryButton** labelled "Follow" when the person is not
followed, a **SecondaryButton** labelled "Following" when they are (the calmer weight signals the
already-done state and carries the unfollow affordance). On a **ProfileHeader**, the follower and
following counts sit beside it in tabular numerals so the layout holds as a count changes.

**Primary action.** Toggle whether the signed-in person follows this account: follow to bring that
account's new chirps into the home timeline, unfollow to remove them.

**Cannot follow yourself.** Your own identity never presents a Follow control. On your own
**ProfileHeader** the context action is "Edit profile" (a **SecondaryButton**), not "Follow", and a
person row that represents you offers no follow affordance. Because no surface draws a Follow control for
your own account, a self-follow cannot be started from the product. If one is nonetheless submitted (for
example from a stale row), it is refused: the control does not enter the Following state, it returns to
"Follow", and **InlineFeedback** in the danger role states plainly that you cannot follow your own
account.

**States.**

- **default / active.** Two states. *Not following* — the "Follow" **PrimaryButton**. *Following* — the
  "Following" **SecondaryButton**. The two are mutually exclusive, so following an account you already
  follow does not stack a second follow; the control simply stays "Following".
- **error.** A follow or unfollow that fails: the optimistic label flip is reverted (back to its prior
  "Follow" or "Following"), any affected follower count returns to its prior value, and the control shows
  **InlineFeedback** in the danger role with a plain reason and a retry. The self-follow refusal above
  uses this same treatment.
- **loading.** The request is in flight: the button shows its busy treatment (a bounded spinner, label
  and width held so the row does not jump) and is not re-triggerable until it resolves.

---

## Profiles, followers/following, and discovery

This section covers how a chirper meets other people: the profile where someone's identity
and chirps live, the followers and following lists that hang off it, and the Explore screen where a
person looks for someone to follow in the first place. These are the screens a stranger uses to decide who
is worth following and to find their way to those accounts, so each is designed as a real screen —
layout, content, one clear primary action, and the empty, error, and loading states it meets in ordinary
use — not a route with a name.

Two behaviours that appear on these screens are owned elsewhere and are composed, not redesigned here: the
**follow / unfollow** control (specified under Social actions above) and **edit profile** (the Edit profile
screen). Where a screen here shows one of them, it places the existing control and links to the existing
screen.

### Public profile — `/@:handle` (profile archetype; reachable signed-out and signed-in)

A profile is the public face of one account and the thing a person reads before deciding to follow. It is
reachable without a session, because people arrive here from shared links and from replies, and a visitor
on such a link should land on content with a visible way to join rather than an auth wall.

**Layout.** The reading column at `space.measure`, inside the shell for the current auth state (`NavShell`
signed-out for a visitor, signed-in for a member). Top to bottom:

- **`ProfileHeader`** — `Avatar` at `avatar.xl`, the display name in `type.title`, the `@handle` and bio
  in `type.body` / `color.text.secondary`, and the follower and following counts in
  `type.meta` + `type.numeral.tabular` so a changing count does not shift the layout. Each count is a
  labelled link that opens the Followers or Following list.
- Below it, a **`ListView`** of the account's own chirps as `ChirpCard`s, newest first, in bounded pages
  with the load-older affordance — the same `ListView` and `ChirpCard` the timeline uses, so a chirp reads
  the same here as anywhere.

**Content.** Handle, display name, bio, the two counts, and the person's chirps. Nothing here needs a
session to be shown.

**Primary action.** The header's context action: for another account, the **follow control** owned by the
Social actions section (`PrimaryButton` "Follow" / `SecondaryButton` "Following"), placed in the header and
behaving as specified there; it is not redesigned here. A signed-out visitor who presses it is
routed to sign-in and returned to the profile (the IA's auth-gated routing), so follow is never a silent
dead-end for someone without a session.

**States.**
- **Empty** — a sparse profile (no bio, zero followers and following, no chirps yet): the `ProfileHeader`
  *empty* state renders the bio space and the counts as calm, labelled zeros ("0 followers", "0
  following") with a one-line note rather than blank gaps, and the chirp `ListView` shows its `EmptyState`
  ("@handle hasn't chirped yet") instead of an empty column. The header is never shown as broken just
  because it is sparse. The next step is the header's follow control: a signed-in viewer can follow now and
  see the first chirp arrive in their timeline, a signed-out visitor is offered Sign up, and the empty
  block links to **Explore** for other people to follow.
- **Error** — three cases, each distinct from empty so the two are never confused: (1) the profile fails
  to load → the `ProfileHeader` *error* state via an `EmptyState` error variant ("We couldn't load this
  profile — try again") with a retry; (2) the account is not available, handled by one rule: an address for
  an account that does not exist or was deleted goes to the **Not found** screen, which states "This
  account doesn't exist"; an account that exists but is blocked or suspended stays on the profile route
  with the statement "This account is unavailable" in place of the header, because the viewer's
  relationship to the account is part of the screen (a viewer who blocked it keeps the way to manage
  blocked accounts). Neither case shows a half-drawn header; (3) a page of chirps fails while the
  header loaded fine → the chirp `ListView` *error* state (`InlineError` with retry) in place of the
  missing page, keeping any chirps already shown.
- **Loading** — the `ProfileHeader` *loading* skeleton (skeleton avatar, name line, bio line, count line)
  above the `ListView` *loading* skeleton rows, both at their real dimensions so the screen does not jump
  when content arrives. A first load shows skeletons, not a spinner on a blank column.

### Own profile — `/@:handle` for the signed-in owner (profile archetype; signed-in)

The same screen a member's own account presents to the world, shown to the owner with the one thing a
visitor does not get: the way in to change it.

**Layout and content.** Identical to the public profile — `ProfileHeader` over a `ListView` of the
owner's own chirps — so a person sees exactly their own public face. The difference is confined to the
header's action and the per-chirp actions.

**Primary action.** In place of Follow, the header shows **"Edit profile"** as a `SecondaryButton` that
opens the Edit profile screen (`/settings/profile`). Edit profile is its own screen; this screen places the
entry and links to it, and does not design the editing form. On the owner's own `ChirpCard`s, the
more-actions menu exposes **Delete chirp**, the confirmation `Dialog` designed under Posting and
conversation above.

**States.**
- **Empty** — a brand-new owner who has not chirped: the chirp `ListView` *empty* state speaks to the
  owner rather than about a third party ("You haven't chirped yet — write your first one") and offers the
  Compose affordance as the next step; the header shows the owner's actual counts (possibly zero) as
  labelled zeros. This complements onboarding (the Onboarding screen); it does not replace it.
- **Error** — as the public profile (profile fails to load → `EmptyState` error variant with retry; a
  chirp page fails → `ListView` error with retry). The blocked/suspended case does not arise for one's own
  account; a session that has expired routes to sign-in per the IA and returns the owner here.
- **Loading** — as the public profile: header skeleton over `ListView` skeleton rows.

### Followers and Following — `/@:handle/followers` and `/@:handle/following` (feed/list; signed-out and signed-in)

The two lists that hang off a profile: who follows this account, and who this account follows. They are
one designed pattern used at two routes, each addressable so a person can link to or bookmark the exact
list. Both are reachable from the profile's count links and carry a labelled way back to the profile.

**Layout.** The reading column, a `type.title` heading naming the list and whose account it belongs to
("People who follow @handle" / "People @handle follows"), then a **`ListView`** of **person rows**. Each
row is `Avatar` at `avatar.md`, display name in `type.heading`, `@handle` in `type.meta`, a one-line bio
in `type.body` / `color.text.secondary`, and — for a signed-in viewer — the **follow control** (the
control specified under Social actions) on the trailing edge. The whole row, excluding the follow control, is a
target that opens that person's profile. Loaded in bounded pages with load-older, per the IA's pagination
convention.

**Content.** One row per account, with enough to recognise the person and decide whether to follow them,
and the follow control to act on that decision in place.

**Primary action.** Open a person's profile (the row), or follow/unfollow them from the row's follow
control without leaving the list. A signed-out viewer sees the rows and the counts but is routed to
sign-in if they try to follow.

**States.**
- **Empty** — the `ListView` *empty* state, worded for which list it is, and each variant names its next
  step:
  - A followers list with no one, on another account: "@handle doesn't have any followers yet", with the
    follow control for that account as the next step (a signed-out visitor is offered Sign up).
  - A followers list with no one, on the owner's own account: "No one follows you yet", with Explore
    offered as the next step.
  - A following list with no one, on another account: "@handle isn't following anyone yet". Nothing on
    this list can be acted on, so the next step is the labelled way back to the profile, and this is the
    one case where returning to the parent screen is the whole next step.
  - A following list with no one, on the owner's own account: "You're not following anyone yet", with
    Explore offered as the next step, so an empty following list points at the way to fix it.
- **Error** — a page fails to load → the `ListView` *error* state (`InlineError` with retry) in place of
  the missing rows; a failure while loading an older page shows at the load-more boundary and keeps the
  rows already shown.
- **Loading** — the `ListView` *loading* skeleton rows at person-row dimensions on first load; a bounded
  spinner at the boundary when loading older rows.

### Explore / find people — `/explore` (feed/list; signed-in)

Where a chirper finds someone to follow when they do not already hold a link to a profile. Today a person
can only reach an account through an external link or a reply; Explore is the surface that closes that
gap. It is in scope and fully designed here; the release bar decides whether a first release ships it (see
the gating note on REQ-UX-064).

**Layout.** The signed-in shell with Explore marked as the active destination, then the reading column:

- A **`TextField`** search input at the top (label "Find people", a plain placeholder), the one input on
  the screen.
- Below it, a **`ListView`** of results as person rows (the same row as the followers/following lists —
  `Avatar`, name, handle, bio snippet, and the follow control), in bounded pages.

**Content.** A query field and a list of people who match it, each with enough to recognise them and the
follow control to act. Before any query, the screen shows whatever suggestions the product can offer (for
example, a short list of accounts to follow); if it can offer none, it shows the prompt alone.

**Primary action.** Search for a person, then follow a result from its row (the control specified under Social actions) or
open their profile — without leaving Explore.

**States.**
- **Empty** — two distinct cases: (1) no query entered yet → a prompt to search, plus any available
  suggestions; if there are no suggestions, the `EmptyState` prompt stands alone ("Search for people to
  follow") rather than a blank screen, and the focused search field is the next step; (2) a query that matches no one → the `ListView` *empty* state as a
  "no results" block ("No people found for that search") with a way to refine the query. The no-query and
  no-results states read differently so a person can tell "nothing searched yet" from "nothing found".
- **Error** — the search request fails → the `ListView` *error* state (`InlineError` with retry) in place
  of results, the query preserved so the person can retry without retyping.
- **Loading** — `ListView` *loading* skeleton rows while a search resolves; a bounded spinner at the
  boundary when loading further pages of results.

---

## Requirements register — REQ-UX-051..064

Each requirement is testable by someone who never met the author, exercisable on the live product, carries
a `release_gating` flag (a `false` flag carries a one-line reason), and references at least one product
requirement it serves.

### REQ-UX-051 — The home timeline reads own and followed chirps, newest first, in bounded pages
- **statement**: The signed-in home timeline shows the person's own chirps and those of the accounts they
  follow, ordered newest first, loaded in bounded pages with an explicit way to load older chirps — never
  as a single unbounded load — inside the persistent signed-in shell with Home marked as the current
  destination.
- **acceptance_criteria**: Signed in and following at least one account that has posted, open `/`: the
  timeline shows recent chirps from you and the people you follow, newest first, as a bounded page, with
  the Home destination marked in the shell. Use the load-older control; older chirps load as a further
  bounded page and the product does not attempt to fetch every chirp at once.
- **release_gating**: true
- **references**: REQ-PROD-002

### REQ-UX-052 — A catch-up affordance brings in chirps posted since the last look
- **statement**: When chirps have been posted since the person last viewed the timeline, the screen offers
  a catch-up control ("N new chirps") at the top of the list that pulls those chirps in as a bounded step
  and returns the reader to the newest, so a long absence is a bounded catch-up rather than an endless
  scroll; returning from a chirp's conversation keeps the reader's place in the list.
- **acceptance_criteria**: Open the timeline, then have another account you follow post while it is open:
  a catch-up control stating how many new chirps are available appears at the top. Select it; the new
  chirps load in at the top without an unbounded scroll. Open a chirp from the list and press back; you
  return to the timeline at the position you left, not at the top.
- **release_gating**: true
- **references**: REQ-PROD-002

### REQ-UX-053 — The timeline has designed empty, error, and loading states
- **statement**: The timeline presents a designed empty state (a brand-new or emptied timeline explains
  why it is empty and points to Explore and to composing a first chirp, never a blank), a designed error
  state (a failed first page, a failed load-older, or a failed catch-up is shown in place with a retry and
  already-loaded chirps are not discarded), and a designed loading state (a first load shows skeleton rows
  at real card dimensions, not a spinner on a blank screen; loading older shows a bounded spinner at the
  boundary; the navigation frame never blanks and nothing spins forever).
- **acceptance_criteria**: With an account that follows no one and has posted nothing, open the timeline:
  it explains the empty state and offers a route to Explore and to composing, rather than a blank area.
  Force the first page to fail: a plain-words message with a retry is shown in place of the list, visibly
  different from the empty state. Force a load-older to fail: the failure shows at the boundary and the
  chirps already on screen remain. Open the timeline on a slow connection: the content region shows
  skeleton rows at the size of real chirps while the shell stays visible.
- **release_gating**: true
- **references**: REQ-PROD-002

### REQ-UX-054 — The 280-character limit is enforced while composing, before submission
- **statement**: The compose surface shows a live remaining-character count that warns as the published
  280-character limit nears and marks the draft as over the limit once it is exceeded, and it keeps a
  person from posting an empty or over-limit chirp — the primary action is disabled while the draft is
  empty or over the limit, and an empty or over-limit submit reached by any means is rejected with no
  chirp created.
- **acceptance_criteria**: Signed in, open the compose surface and type. The remaining-character count
  decreases as you type and changes to a warning appearance as you approach 280. Type past 280: the count
  shows an over-limit state, the excess is distinguished in the field, and the "Post" action is not
  activatable. Empty the field: "Post" is again not activatable. Reduce a valid draft and post it: the
  chirp is published. At no point can an empty or over-limit chirp be posted.
- **release_gating**: true
- **references**: REQ-PROD-001

### REQ-UX-055 — Publishing locks against double-posting, confirms on success, and keeps the draft on failure; removing your own chirp is confirmed first
- **statement**: While a publish is in flight the primary action shows a busy state and the draft field is
  briefly locked so the same chirp cannot be posted twice; on success the chirp is published, the field
  clears, and a brief non-blocking confirmation is shown; on failure the draft is kept exactly as written,
  an inline error states what happened with a way to retry, and the person can post again without
  retyping. A person removes their own chirp from its more-actions menu through the Delete chirp
  confirmation, which shows the chirp, states that the removal cannot be undone and that replies stay,
  deletes only on confirmation, shows a busy state while the delete runs, and on failure keeps the dialog
  open with an inline error and leaves the chirp in place.
- **acceptance_criteria**: Compose a valid chirp and post it: the action shows a busy state, the field
  does not accept a second submit of the same draft during the publish, and on success the chirp appears,
  the field clears, and a brief confirmation is shown. Force a publish failure (for example post while
  offline): the draft text remains in the field, an inline error explains the failure with a retry, and
  retrying with connectivity restored posts the chirp. No successful post is duplicated and no failed post
  loses the draft. Open the more-actions menu on your own chirp and choose Delete chirp: a dialog shows
  the chirp and says the removal cannot be undone, and Cancel (or Escape) leaves the chirp in place.
  Confirm: the dialog shows a busy state, then closes, the chirp is gone from the list, and "Chirp
  deleted" is shown. Force the delete to fail: the dialog stays open with an inline error, the chirp is
  still on the screen behind it, and retrying with connectivity restored deletes it. The more-actions
  menu on another person's chirp does not offer Delete chirp.
- **release_gating**: true
- **references**: REQ-PROD-001

### REQ-UX-056 — One compose surface in three placements, with a context-labelled action and an empty state
- **statement**: The compose surface is the one ComposeBox component, presented inline at the top of the
  home timeline, as the body of the Compose dialog (at `/compose` and as an overlay dialog opened from the
  persistent compose affordance), and in the reply position of the Chirp / conversation screen; its
  primary action is labelled for the placement ("Post" when writing a chirp, "Reply" when answering one);
  and its empty state shows a placeholder prompt with the counter at the full budget and the action
  disabled, in every placement.
- **acceptance_criteria**: Signed in, reach the compose surface three ways — inline at the top of the home
  timeline, by opening the Compose dialog from the shell and by opening `/compose` directly, and in the
  reply position on a chirp's conversation screen. In each, an untouched field shows a placeholder prompt,
  the remaining-character count at 280, and a disabled primary action; the action reads "Post" in the
  timeline and dialog and "Reply" in the conversation. Dismiss the Compose dialog with text in the field
  and reopen it: the draft is not lost.
- **release_gating**: true
- **references**: REQ-PROD-001, REQ-PROD-003

### REQ-UX-057 — A chirp is read in the conversation it belongs to
- **statement**: The Chirp / conversation screen presents a chirp together with the chirp it answers (when
  it is a reply) and its replies, each reply shown as answering its parent, so the exchange is read in
  context rather than as a flat, unrelated list. The replies load in bounded pages, oldest-first, with a
  way to load older replies.
- **acceptance_criteria**: Open a chirp that is a reply and that has replies of its own. The chirp it
  answers is shown above it with a "Replying to" relation and is itself openable; the focused chirp is
  shown as the subject of the screen; its replies appear below in chronological order with a reply count,
  and a long thread offers a way to load older replies rather than loading everything at once.
- **release_gating**: false — reading replies as a navigable conversation rides REQ-PROD-004, which the
  release bar does not gate; the parent reference itself is already recorded by the gating reply
  requirement (REQ-UX-058 / REQ-PROD-003), so a first release may ship the reply action without the
  navigable conversation read.
- **references**: REQ-PROD-004

### REQ-UX-058 — A reply is written from the conversation, and a reply to a gone chirp is reported
- **statement**: A signed-in person can write and publish a reply from the conversation screen's reply
  slot using the shared compose control; the reply records the chirp it answers and appears in the
  conversation. Replying to a chirp that no longer exists is reported as "This chirp isn't available", with the draft kept,
  rather than appearing to send. A signed-out visitor sees a path to sign in or sign up in place of the
  reply control rather than a dead or silent one.
- **acceptance_criteria**: Signed in on a chirp's conversation, write a reply within the character limit
  and publish it; it appears in the replies as answering that chirp and its publication is confirmed.
  Attempt to reply to a chirp that has been deleted; the product reports "This chirp isn't available" at the compose control
  and keeps the drafted text rather than appearing to succeed. Open the same conversation with no session;
  in place of the reply control there is a visible way to sign in or sign up to reply.
- **release_gating**: true
- **references**: REQ-PROD-003

### REQ-UX-059 — Like is an in-place, idempotent toggle with an accurate count
- **statement**: The like control on every **ChirpCard** is an in-place toggle with two states —
  not-liked and liked — where the liked state is shown by colour together with a filled heart and a
  "Liked" label (never colour alone); liking is idempotent and the like count shown reflects the resolved
  result; a failed like or unlike reverts the optimistic change and reports at the control, and an
  in-flight change shows the control's busy state.
- **acceptance_criteria**: On any chirp, activate like: the control shows the liked state (filled heart,
  like colour, and a "Liked" label — not colour alone) and the count rises by one. Activate like again on
  the now-liked chirp, or reload the screen: the count does not rise a second time. Unlike it: the control
  returns to not-liked and the count returns to its earlier value. Force a like to fail (for example act
  while offline): the control returns to its prior state, the count is unchanged, and a danger message
  appears at the control with a way to retry — the count never shows a like that did not take. Open the
  same chirp in the timeline, in its conversation, and on the author's profile: the like control looks and
  behaves the same in each.
- **release_gating**: true
- **references**: REQ-PROD-005

### REQ-UX-060 — Follow is an in-place, idempotent control that cannot follow yourself
- **statement**: The follow control on a **ProfileHeader** and on the person rows of the discovery and
  list screens is an in-place control with two states — "Follow" (a **PrimaryButton**) and "Following" (a
  **SecondaryButton**); following is idempotent; a person's own identity never presents a Follow control
  (the own-profile action is "Edit profile") so a self-follow cannot be started, and any attempt is
  refused and shown at the control; a failed follow or unfollow reverts and reports at the control, and an
  in-flight change shows the control's busy state.
- **acceptance_criteria**: On another person's profile, activate "Follow": the control becomes "Following"
  and that account's new chirps appear in your home timeline. Activate it again, or reload: nothing is
  duplicated — one follow holds and the control stays "Following". Unfollow: the control returns to
  "Follow" and their chirps leave your timeline. Open your own profile: the context action is "Edit
  profile", never "Follow", and no screen offers a control to follow your own account. Force a follow to
  fail: the control returns to its prior label, any follower count is unchanged, and a danger message
  appears at the control with a way to retry. Find the follow control on a profile header and on a person
  row in Explore or a followers/following list: it looks and behaves the same in each.
- **release_gating**: true
- **references**: REQ-PROD-006

### REQ-UX-061 — A public profile shows identity and chirps, with or without a session
- **statement**: A user's profile at `/@:handle` shows their avatar, display name, handle, bio, and
  follower and following counts, above their own chirps in newest-first bounded pages, and is reachable
  both signed-out and signed-in. A profile address for an account that does not exist or was deleted
  goes to the Not found screen ("This account doesn't exist"); an account that is blocked or suspended
  stays on the profile route with "This account is unavailable" in place of the header.
- **acceptance_criteria**: With no session, open a profile link; the header shows the handle, display
  name, bio, and the follower and following counts, and the person's chirps load below in a bounded page
  with a way to load older ones. Signed in, open the same profile and see the same content plus the follow
  control in the header. Open `/@` followed by a handle that does not exist: the Not found screen states
  "This account doesn't exist". Open the profile of a suspended account: the profile route stays and
  reads "This account is unavailable", with no header drawn.
- **release_gating**: true
- **references**: REQ-PROD-007

### REQ-UX-062 — The owner's profile is their public face with a way to edit it
- **statement**: When the signed-in owner opens their own profile, they see the same public profile anyone
  else sees, with an "Edit profile" entry in place of the follow control that opens the edit-profile
  screen.
- **acceptance_criteria**: Signed in, open your own profile; it shows your avatar, display name, handle,
  bio, counts, and your chirps as a visitor would see them, and an "Edit profile" control that opens the
  edit-profile screen. The follow control is not shown on your own profile.
- **release_gating**: true
- **references**: REQ-PROD-007

### REQ-UX-063 — Followers and following are addressable, paginated lists
- **statement**: A profile's follower and following counts open the `/@:handle/followers` and
  `/@:handle/following` lists, each an addressable, paginated list of people showing enough to recognise
  each account, with the follow control on each row for a signed-in viewer and a labelled way back to the
  profile.
- **acceptance_criteria**: From a profile, open the followers list by its count; it shows one row per
  follower (avatar, name, handle, bio) in a bounded page with a way to load more, a way back to the
  profile, and — signed in — a follow control per row. Open the following list the same way with the same
  behaviour. Open each list's URL directly; it lands on that list.
- **release_gating**: true
- **references**: REQ-PROD-007, REQ-PROD-006

### REQ-UX-064 — A way to find people to follow
- **statement**: A signed-in person can find accounts to follow from within the product at `/explore`, by
  searching for people and following a result in place, without already holding a link to a profile.
- **acceptance_criteria**: Signed in and holding no external link, open Explore, search for a person, and
  follow at least one result from the list without leaving the screen; a search that matches no one shows
  a "no results" state with a way to refine, distinct from the before-you-search prompt.
- **release_gating**: false — Explore implements REQ-PROD-042, which the product requirements do not gate;
  a first release may ship with follow-by-profile and follow-from-a-reply and add discovery as a near-term
  follow-up. The release bar should decide explicitly what minimum discovery v1 includes.
- **references**: REQ-PROD-042
