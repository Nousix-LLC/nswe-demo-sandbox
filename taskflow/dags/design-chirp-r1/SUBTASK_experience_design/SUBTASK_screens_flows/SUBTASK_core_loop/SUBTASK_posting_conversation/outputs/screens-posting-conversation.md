# Posting and conversation

The writing-and-reading-in-context surfaces: the compose/post surface where a person writes and
publishes a chirp, and the Chirp / conversation screen where a chirp is read in the conversation
it belongs to and answered. These are the two surfaces at the heart of journey J4.

---

## Compose and post a chirp

Writing a chirp is the first thing chirp exists for, and it is the surface a new person uses before
they have followed anyone or read a timeline worth reading. This section designs that surface: where a
person writes a chirp, how the product keeps them inside the published 280-character limit while they
type, how the "Post" action behaves, and what the surface looks like when it is empty, when something
is wrong, and while a chirp is being published.

The surface is one component — **ComposeBox** — shown in three places. It is designed once here, with
its counter, its limit behaviour, its primary action, and its empty, error, and loading states, and
the same component is placed inline at the top of the **Home timeline**, as the body of the **Compose**
dialog (`/compose` and the overlay dialog), and in the reply position on the **Chirp / conversation**
screen. The conversation screen composes the reply-position variant designed here rather than defining
its own writing field. The screens named here are the **Compose** and **Home timeline** and **Chirp /
conversation** entries of the screen inventory; every piece named in bold is a component-library
component used by its name, not a new invention.

This surface serves journey J4 step 2 (compose and post) and the product requirement REQ-PROD-001 (post
a chirp up to 280 characters; an empty or over-limit message is rejected and nothing is posted). The
reply-position variant also carries the writing half of replying (REQ-PROD-003); the conversation
screen owns the rest of that flow.

### Layout and content

The **ComposeBox** reads top to bottom as one block, the same in every placement:

- the composing person's **Avatar** at the leading edge, so a person sees whose voice the
  chirp will carry — this matters most in the reply position, where the draft sits among other people's
  chirps;
- the **draft field** — a multi-line text area on the `color.bg.subtle` draft surface, holding the
  chirp text in `type.body`, growing with the content rather than scrolling a fixed box, with a
  placeholder prompt when empty;
- the **remaining-character affordance** — a live count of characters still available, in
  `type.caption` with `type.numeral.tabular` figures so the number does not shift the layout as it
  changes;
- the **primary action** — a **PrimaryButton** labelled for the placement ("Post" when writing a new
  chirp, "Reply" in the conversation's reply position).

The draft field is the focus of the surface and takes the most width; the avatar, counter, and action
sit around it without competing for attention. In the dialog placement the box is the dialog's content
and the action pair sits at the dialog's foot; inline and in the reply position the action sits with
the box. Nothing else lives in this surface — no formatting toolbar, no media controls, no audience
picker — because a chirp in this product is plain text up to 280 characters, and the surface shows only
what that needs.

### The character budget, enforced before submission

The product does not let a person write past the limit and only discover it when they try to post. The
counter is live: as the person types, the remaining-character count updates, and it changes appearance
before and at the boundary so the limit is felt, not just stated.

- While there is comfortable room, the counter is quiet (`color.text.secondary`), showing the number of
  characters still available.
- As the draft **nears** the limit, the counter moves to the warning role (`color.warning`) so the
  person sees the boundary coming while they still have room to adjust.
- When the draft is **over** the limit, the counter moves to the danger role (`color.danger`), the
  over-limit characters are distinguished in the field so the person can see exactly what to cut, and
  the primary action is disabled.

The primary action is disabled whenever the draft is empty or over the limit, so the ordinary way to
reach an invalid post — an empty field or too many characters — is closed before the person can act on
it. If an empty or over-limit submit is reached by any other route (a keyboard shortcut, say), it is
rejected and no chirp is created, matching REQ-PROD-001's rule that nothing is posted in that case. The
limit value shown and enforced is the product's published 280, which the ComposeBox reads from the
product requirement rather than inventing.

Colour never carries the limit state on its own: the warning and danger states of the counter are a
colour **and** the changing number (and, over the limit, the marked-over characters and the disabled
action), so a person who does not distinguish the colours still sees the boundary.

### The primary action

The primary action is a single **PrimaryButton**, one per surface, labelled with the verb for what it
does — "Post" for a new chirp, "Reply" in the conversation's reply position — never a bare "Submit" or
"OK". It has three conditions a person can reach:

- **disabled** — the draft is empty or over the limit; the button reads as inactive and cannot be
  triggered. This is the resting state of an empty compose surface.
- **ready** — the draft holds between one character and the limit; the button is active and posting is
  the obvious next step.
- **busy** — a publish is in flight; the button shows its loading state in place, holding its label and
  width so the surface does not jump, and it cannot be triggered again.

In the **Compose** dialog the primary action is paired with a **SecondaryButton** ("Cancel") and a
close control, following the Dialog's action-pair convention; inline and in the reply position the
primary action stands with the box and the person leaves the draft by navigating away (which preserves
it, below).

### States

The surface is designed for the states a person actually meets, not only the happy path. Each state
below is the relevant component's own named state, composed here — the surface does not improvise its
own empty, error, or loading treatment. Where a failure needs to keep a person's draft safe, this
surface composes the product-wide keep-the-draft recovery rather than redefining it; that global
pattern is set elsewhere in the experience design and this surface follows it.

**Empty.** No text yet. The draft field shows a placeholder prompt ("What's happening?" for a new
chirp; a reply placeholder that names who is being answered in the reply position), the counter sits at
the full budget, and the primary action is disabled. The empty surface is calm and ready, not an error
— a person who has not typed anything has done nothing wrong, so nothing is marked red. This is the
ComposeBox *empty* state with the PrimaryButton in its *disabled* state.

**Error.** Two different things can be wrong, and they are shown differently because the person does
something different about each:

- *Over the limit* — the draft is longer than 280 characters. This is shown while typing: the counter
  is in the danger role, the over-limit characters are distinguished in the field, and the primary
  action is disabled. There is no separate error message to dismiss; the fix is visible in the field
  and the counter, and the person edits the draft down. This is the ComposeBox *error* state for the
  over-limit case.
- *The publish failed* — the person posted a valid draft and the publish did not succeed (the network
  dropped, the server refused, the session expired mid-submit). The draft is kept exactly as written,
  an **InlineError** appears below the field in plain words with a way to try again, and the primary
  action returns to its ready state so the person can retry without retyping. A failed publish never
  clears or loses the draft. When the cause is an expired session, the surface follows the product's
  session-expiry convention — the person is routed to sign in with the reason stated, their draft is
  preserved, and they return to it afterwards — which this surface composes rather than redefines. In
  the **Compose** dialog this error shows inside the panel and the dialog stays open with the draft
  intact, per the Dialog's *error* state.

**Loading.** A publish is in flight. The primary action shows its busy state and the draft field locks
briefly so the chirp cannot be edited or submitted again mid-publish — this is what stops a double
tap from posting the same chirp twice. The lock is brief and tied to the in-flight publish, not a
general disabling of the surface. This is the ComposeBox *loading* state with the PrimaryButton in its
*loading* state. On success the chirp is published, the field clears to its empty state, and the result
is confirmed with a brief, non-blocking **Toast** ("Chirp posted") that does not interrupt what the
person does next; the new chirp appears in the places the timeline and conversation screens own. On
failure the surface moves to the publish-failed error above.

### The three placements

The same ComposeBox, with everything above, appears in three places. The behaviour — the counter, the
280-character limit, the disabled/empty/error/loading treatment, and the keep-the-draft recovery — is
identical in all three; what differs is where the box sits and what its action is called.

- **Inline, at the top of the Home timeline.** The box sits above the timeline feed so a signed-in
  person can write without leaving home. Its action is "Post"; on success the posted chirp appears at
  the top of the timeline and the box returns to empty.
- **The Compose dialog (`/compose` and the overlay dialog).** The box is the body of the **Dialog**
  (modal variant), reachable from the always-available compose affordance in the signed-in **NavShell**
  and directly at the `/compose` URL. The dialog traps focus while open, the browser back control
  dismisses it (closing the dialog, not leaving the underlying screen), and a dismissed dialog with a
  non-empty draft follows the keep-the-draft convention rather than discarding the writing. Its action
  is "Post".
- **The reply position on the Chirp / conversation screen.** The box sits in the conversation's reply
  slot, its placeholder names the chirp being answered, and its action is "Reply". The **Chirp /
  conversation** screen composes this variant by name; the counter, the limit, the disabled/error/
  loading behaviour, and the keep-the-draft recovery are all as designed here. Posting a reply from
  this position is the writing half of REQ-PROD-003; the conversation screen owns reading the
  conversation and reporting a reply to a chirp that is gone.

### Requirements — REQ-UX-054..056

Each requirement is testable by someone who never met the author, exercisable on the live product, and
references the product requirement(s) it serves.

#### REQ-UX-054 — The 280-character limit is enforced while composing, before submission

- **statement**: The compose surface shows a live remaining-character count that warns as the published
  280-character limit nears and marks the draft as over the limit once it is exceeded, and it keeps a
  person from posting an empty or over-limit chirp — the primary action is disabled while the draft is
  empty or over the limit, and an empty or over-limit submit reached by any means is rejected with no
  chirp created.
- **acceptance_criteria**: Signed in, open the compose surface and type. The remaining-character count
  decreases as you type and changes to a warning appearance as you approach 280. Type past 280: the
  count shows an over-limit state, the excess is distinguished in the field, and the "Post" action is
  not activatable. Empty the field: "Post" is again not activatable. Reduce a valid draft and post it:
  the chirp is published. At no point can an empty or over-limit chirp be posted.
- **release_gating**: true
- **references**: REQ-PROD-001

#### REQ-UX-055 — Publishing locks against double-posting, confirms on success, and keeps the draft on failure

- **statement**: While a publish is in flight the primary action shows a busy state and the draft field
  is briefly locked so the same chirp cannot be posted twice; on success the chirp is published, the
  field clears, and a brief non-blocking confirmation is shown; on failure the draft is kept exactly as
  written, an inline error states what happened with a way to retry, and the person can post again
  without retyping.
- **acceptance_criteria**: Compose a valid chirp and post it: the action shows a busy state, the field
  does not accept a second submit of the same draft during the publish, and on success the chirp
  appears, the field clears, and a brief confirmation is shown. Force a publish failure (for example
  post while offline): the draft text remains in the field, an inline error explains the failure with a
  retry, and retrying with connectivity restored posts the chirp. No successful post is duplicated and
  no failed post loses the draft.
- **release_gating**: true
- **references**: REQ-PROD-001

#### REQ-UX-056 — One compose surface in three placements, with a context-labelled action and an empty state

- **statement**: The compose surface is the one ComposeBox component, presented inline at the top of
  the home timeline, as the body of the Compose dialog (at `/compose` and as an overlay dialog opened
  from the persistent compose affordance), and in the reply position of the Chirp / conversation
  screen; its primary action is labelled for the placement ("Post" when writing a chirp, "Reply" when
  answering one); and its empty state shows a placeholder prompt with the counter at the full budget
  and the action disabled, in every placement.
- **acceptance_criteria**: Signed in, reach the compose surface three ways — inline at the top of the
  home timeline, by opening the Compose dialog from the shell and by opening `/compose` directly, and
  in the reply position on a chirp's conversation screen. In each, an untouched field shows a
  placeholder prompt, the remaining-character count at 280, and a disabled primary action; the action
  reads "Post" in the timeline and dialog and "Reply" in the conversation. Dismiss the Compose dialog
  with text in the field and reopen it: the draft is not lost.
- **release_gating**: true
- **references**: REQ-PROD-001, REQ-PROD-003

---

## The Chirp / conversation screen — reading in context and replying

This is the screen where a single chirp is read together with the chirp it answers and the replies it
received, and where a reply is written. It is the second half of the core loop's writing-and-reading
surfaces: the compose/post surface (designed above) is where a chirp starts; this screen is where a
chirp is read in the conversation it belongs to and answered. It is reached by opening a chirp from the
timeline, a profile, a notification, or a shared link, and it has a stable address so any of those routes —
and an outside link — land on the same place.

The bar here is a designed screen, not a route with a list under it: the focused chirp, the chirp it
answers, the replies, and the place to reply are all laid out and specified, and the screen is designed for
the cases that are not the happy path — a chirp with no replies yet, a chirp that has been removed, a page
that fails to load, and the moment before anything has loaded at all.

Everything below is built from screens named in the screen inventory and components named in the component
library; nothing here redefines either. The reply control is the shared **ComposeBox** in its
reply-position placement — it is composed here by name, and its character counter, its 280-character limit,
its disabled/empty/error/loading behaviour, and its keep-the-draft recovery are the component library's and
the compose/post surface's to specify, not this screen's.

---

### Screen: Chirp / conversation

- **Inventory name**: Chirp / conversation
- **Route**: `/@:handle/chirp/:id` — a stable, shareable address (per the IA's addressable-chirp
  convention); opening it directly lands the person on this chirp in its conversation, not on a generic
  home.
- **Archetype**: feed/list
- **Auth**: both — it renders inside the **signed-out shell** for a visitor on a shared link and inside the
  **signed-in shell** for a member. The conversation reads the same in both; the one difference is the
  reply slot (below).
- **Reached from**: a **ChirpCard** opened in the home timeline, a profile, the notifications list, search
  results, or an outside link. Per the IA wayfinding convention the screen offers a labelled way back to
  where the person came from, and the browser back control returns them to that place without re-submitting
  anything and without losing their scroll position in the list they left.

#### Layout (default)

Top to bottom, within the appropriate **NavShell**:

1. **Wayfinding** — the shell marks where the person is; the document title and the main heading name the
   screen (the focused chirp's author and a short form of its text), and a labelled back control sits at the
   top of the content column (per the IA back/wayfinding convention — composed, not redesigned here).
2. **The chirp being answered (parent context)** — when the focused chirp is itself a reply, the chirp it
   answers is shown directly above it as a **ChirpCard**, introduced by a quiet relation line ("Replying to
   @handle"). The parent card is a target that opens *its* conversation, so a person can walk up the thread
   one step. When the focused chirp is a top-level chirp (answers nothing), this region is simply absent —
   not an empty slot.
3. **The focused chirp** — the subject of the screen, rendered as a **ChirpCard** given the visual weight of
   the thing the screen is about (the root of this view): author **Avatar**, display name, handle, relative
   timestamp, the chirp text, and the action row (**IconButton**s for reply, like, and more-actions). The
   reply action here scrolls to and focuses the reply slot below.
4. **The reply slot** — the primary writing affordance on this screen:
   - *Signed in*: the shared **ComposeBox** in its reply-position placement, pre-framed with "Replying to
     @handle" so it is clear what the reply answers, and carrying its own "Reply" **PrimaryButton**. The box,
     its counter, its limit, and its keep-the-draft behaviour are composed by name from the component
     library and the compose/post surface — not restated here.
   - *Signed out*: the box is replaced by a short "Sign in to reply" prompt leading to **Sign in** / **Sign
     up** in the signed-out shell, so a visitor who wants to answer is given the path to an account rather
     than a dead control or a silent one. (This composes the **ComposeBox**'s "composing not permitted in
     the current state" case together with the signed-out shell's own entries.)
5. **The replies** — a **ListView** of **ChirpCard**s, in oldest-first (chronological) order so the
   exchange reads the way it happened, with a reply count heading it ("12 replies"). It loads in bounded
   pages with the IA's load-older affordance for a long thread; it is never one unbounded load. Each reply
   card is a target that opens that reply in its own conversation, so a reply with replies of its own can be
   drilled into.

#### Content

- The focused chirp and every reply show author name, handle, relative timestamp (`2m`, `4h`, then an
  absolute date), and text, from the **ChirpCard** vocabulary.
- The parent-context relation ("Replying to @handle") and, on a reply card, the same relation where a reply
  answers another reply, so a reply is always presented as answering its parent rather than stranded in a
  flat list.
- The reply count above the list.
- In the reply slot, the "Replying to @handle" framing and the live remaining-character affordance that the
  **ComposeBox** owns.

#### Primary action

**Reply** — writing and publishing a reply from the reply slot, via the **ComposeBox**'s "Reply"
**PrimaryButton**. A published reply records the chirp it answers and appears in the replies list in its
chronological place; brief non-blocking feedback (the **Toast** / **InlineFeedback** pattern) confirms it,
per the product-wide "the result of every action is shown" convention.

#### States

- **empty** — a chirp that has no replies yet. The focused chirp and any parent context render normally; the
  replies region shows the **ListView** *empty* state as an **EmptyState** block that invites the first
  reply ("No replies yet — be the first to reply") and points at the reply slot, rather than a blank area.
  The reply slot (the **ComposeBox**, signed in) is present as the next step, so an empty conversation still
  offers the one thing to do on it.
- **error** — three distinct failures, each shown where it happens rather than as a silent drop:
  - *The focused chirp has been removed* (deleted, blocked, or otherwise unavailable): it renders as the
    **ChirpCard** *error* tombstone ("This chirp isn't available") in place of the card, rather than an
    empty gap, and the reply slot is withdrawn — there is nothing to answer. A completely unresolved address
    (no such chirp id) falls through to the inventory's **Not found** screen, which explains the resource is
    missing and routes the person back to a known place.
  - *Replying to a chirp that has gone away between opening the screen and sending* (the parent was deleted
    while the reply was being written): the reply is reported as not-found through an **InlineError** at the
    **ComposeBox** (and the focused chirp flips to the tombstone), and the draft is kept so the words are
    not lost — never a reply that appears to send into nothing.
  - *The replies fail to load* while the focused chirp loaded fine: the **ListView** *error* state shows an
    **InlineError** with a retry in place of the missing replies; the focused chirp, the parent context, and
    the reply slot stay usable, and a failure while loading *older* replies shows at the load-more boundary
    without discarding the replies already on screen.
- **loading** — the first load shows the **LoadingState** skeleton rather than a spinner on a blank screen:
  a skeleton **ChirpCard** at the focused chirp's real dimensions (and one in the parent-context slot when
  the chirp is known to be a reply), and **ListView** skeleton reply rows, so the layout does not jump when
  the content arrives. The reply slot renders immediately — the **ComposeBox** needs no data to appear — so
  the person can begin writing before the replies finish loading.

#### Consistency notes (composed, not redefined)

- The per-screen empty / error / loading states above are the named states of the components that build the
  screen (**ChirpCard**, **ListView**, **ComposeBox**, **EmptyState**, **LoadingState**, **InlineError**)
  together with the product-wide empty / loading / error patterns and the keep-the-draft recovery owned by
  the considered-states surface. In particular, a failed reply publish keeps the draft, and an expired
  session mid-reply routes to sign-in with the reason stated and the draft preserved, returning the person
  here afterwards — both are composed from that global treatment and the **ComposeBox**'s own behaviour, not
  reinvented on this screen.
- Addressability, deep-linking, pagination/catch-up, and back/forward behaviour are the IA's conventions,
  applied here by name.

---

### Requirements — REQ-UX-057..058

Each requirement is testable by someone who never met the author, on the live product; each carries a
`release_gating` flag and names at least one product requirement it serves.

#### REQ-UX-057 — A chirp is read in the conversation it belongs to

- **statement**: The Chirp / conversation screen presents a chirp together with the chirp it answers (when
  it is a reply) and its replies, each reply shown as answering its parent, so the exchange is read in
  context rather than as a flat, unrelated list. The replies load in bounded pages, oldest-first, with a way
  to load older replies.
- **acceptance_criteria**: Open a chirp that is a reply and that has replies of its own. The chirp it
  answers is shown above it with a "Replying to" relation and is itself openable; the focused chirp is
  shown as the subject of the screen; its replies appear below in chronological order with a reply count,
  and a long thread offers a way to load older replies rather than loading everything at once.
- **release_gating**: false — reading replies as a navigable conversation rides REQ-PROD-004, which the
  release bar does not gate; the parent reference itself is already recorded by the gating reply requirement
  (REQ-UX-058 / REQ-PROD-003), so a first release may ship the reply action without the navigable
  conversation read.
- **references**: REQ-PROD-004

#### REQ-UX-058 — A reply is written from the conversation, and a reply to a gone chirp is reported

- **statement**: A signed-in person can write and publish a reply from the conversation screen's reply slot
  using the shared compose control; the reply records the chirp it answers and appears in the conversation.
  Replying to a chirp that no longer exists is reported as not-found, with the draft kept, rather than
  appearing to send. A signed-out visitor sees a path to sign in or sign up in place of the reply control
  rather than a dead or silent one.
- **acceptance_criteria**: Signed in on a chirp's conversation, write a reply within the character limit and
  publish it; it appears in the replies as answering that chirp and its publication is confirmed. Attempt to
  reply to a chirp that has been deleted; the product reports not-found at the compose control and keeps the
  drafted text rather than appearing to succeed. Open the same conversation with no session; in place of the
  reply control there is a visible way to sign in or sign up to reply.
- **release_gating**: true
- **references**: REQ-PROD-003

### Scope notes

- **Surface owned**: `reply_and_conversation` (the Chirp / conversation screen) and `REQ-UX-057..058`, per
  the subtree contract. The compose/post surface, the home timeline, likes, follows, profiles, discovery,
  the IA/screen inventory, the component library, and the product-wide empty/loading/error patterns are
  owned elsewhere and are composed here by name, not redefined.
- **Shared component**: the **ComposeBox** is designed by the compose/post surface (including its
  reply-position placement); this screen places it in the reply slot and refers to its counter, limit, and
  keep-the-draft recovery by name — it does not redesign the component.
- **Staging**: reading-in-context rides the non-gating REQ-PROD-004 (reflected in REQ-UX-057's
  `release_gating: false`); the reply action rides the gating REQ-PROD-003 (REQ-UX-058,
  `release_gating: true`).

---

## Consolidated requirements register — REQ-UX-054..058

All five requirements for the posting-and-conversation surfaces, in id order.

| id | statement (short form) | release_gating | references |
|----|------------------------|----------------|------------|
| REQ-UX-054 | The 280-character limit is enforced live while composing; empty or over-limit post is blocked before submission. | true | REQ-PROD-001 |
| REQ-UX-055 | Publishing locks against double-posting, confirms success with a non-blocking Toast, and keeps the draft with an inline retry on failure. | true | REQ-PROD-001 |
| REQ-UX-056 | One ComposeBox in three placements (inline timeline, Compose dialog, reply position); action labelled for placement; empty state in each. | true | REQ-PROD-001, REQ-PROD-003 |
| REQ-UX-057 | The Chirp / conversation screen reads a chirp with its parent and replies in context, oldest-first, in bounded pages. | false (rides REQ-PROD-004, non-gating) | REQ-PROD-004 |
| REQ-UX-058 | A reply is written from the conversation; a reply to a gone chirp is reported with the draft kept; signed-out visitors see a sign-in path. | true | REQ-PROD-003 |

Full requirements (with acceptance criteria) appear in the sections above.
