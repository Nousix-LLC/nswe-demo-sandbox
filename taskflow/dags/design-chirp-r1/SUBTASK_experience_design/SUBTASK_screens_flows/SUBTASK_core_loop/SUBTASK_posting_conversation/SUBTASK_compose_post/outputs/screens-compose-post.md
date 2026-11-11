### Compose and post a chirp

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

#### Layout and content

The **ComposeBox** reads top to bottom as one block, the same in every placement:

- the composing person's **Avatar** (`avatar.md`) at the leading edge, so a person sees whose voice the
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

#### The character budget, enforced before submission

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

In the **Compose** dialog the primary action is paired with a **SecondaryButton** ("Cancel") and a
close control, following the Dialog's action-pair convention; inline and in the reply position the
primary action stands with the box and the person leaves the draft by navigating away (which preserves
it, below).

#### States

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

#### The three placements

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

### Requirements and acceptance criteria — REQ-UX-054..056

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
