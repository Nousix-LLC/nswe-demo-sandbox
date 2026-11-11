## The Chirp / conversation screen — reading in context and replying

This is the screen where a single chirp is read together with the chirp it answers and the replies it
received, and where a reply is written. It is the second half of the core loop's writing-and-reading
surfaces: the compose/post surface (designed separately) is where a chirp starts; this screen is where a
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

### Requirements and acceptance criteria — REQ-UX-057..058

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

---

### Scope and method notes

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
- **Methodology**: designed under Experience Design (primary) with Product Strategy (support). The design
  methodology loader was unavailable in this environment; this screen was designed from those bundles' intent
  and product-design practice, composing the already-frozen screen inventory, component library, and product
  requirements. This limitation did not block the work and is recorded here rather than silently absorbed.
</content>
</invoke>
