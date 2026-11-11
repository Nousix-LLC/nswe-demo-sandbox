## Empty, loading, and error states

A screen is not always showing content. Besides its working state, every surface in chirp spends
time in one of three other conditions: it has nothing to show (**empty**), it is fetching what it
will show (**loading**), or something it tried to do failed (**error**). One further condition cuts
across all three: the person's session ends, or a request fails for a moment, while they have work
in progress. Left to each screen to handle on its own, these conditions get improvised differently
from screen to screen, or skipped until a demo hits them. This section sets them once, as the
product-wide patterns every screen obeys, so a person meets the same treatment on the timeline, on a
profile, in settings, and inside a dialog.

The patterns here are not new components. They are expressed over the component library's named
states (`EmptyState`, `LoadingState`, `InlineError`, `InlineFeedback`, `Toast`, and the
`ListView` / `ChirpCard` / `ProfileHeader` / `Avatar` states) and over the information
architecture's conventions for session expiry and auth-gated return. Each screen design sets its
own empty, error, and loading states by composing those component states with the patterns below;
none invents a per-screen treatment that conflicts with them.

One rule governs all four conditions: **a person can always tell which condition a surface is in,
why, and what to do next.** That signal is never carried by colour alone. It is carried by an
illustration and words, a skeleton shape, an icon and a message, or a plain sentence.

### Empty: explain and offer a next step, never a blank

A surface with nothing in it shows the `EmptyState` block, or the owning component's own *empty*
state, which is the same treatment: a calm illustration, one line explaining why the surface is
empty, and a next step the person can take. It is never a bare blank region, and never a spinner
that has already finished spinning on nothing.

A next step is an action or a route the person can take from that surface. Going back to the parent
screen counts only when nothing else applies, and the screen's design says so when it relies on it.

Where this applies, by screen and component, with the next step each one names:

- A **brand-new home timeline** (`ListView` *empty*) explains that the timeline fills as the
  person follows people and posts. Next steps: go to **Explore**, or compose a first chirp.
- An **empty notifications** surface (`ListView` *empty*) says that activity about the person
  will appear here. Next step: go to **Explore** to find people and chirps to engage with.
- An **empty followers / following** list (`ListView` *empty*) explains the absence in words fitted
  to the list. Next step on the person's own list: find people on **Explore**. On someone else's
  list nothing else applies, so the next step is the way back to that person's profile, and the
  screen says so.
- An **Explore / find people** search with no results (`ListView` *empty*) explains that nothing
  matched, without implying failure. Next step: change or broaden the query, which stays in the
  field.
- A **blocked & muted** sub-section with nothing in it shows an `EmptyState` inside the section, not
  an empty `SettingRow`. Next step: the way back to Settings, because nothing else applies there and
  the screen says so. The same holds for any settings sub-section, such as sessions & devices, that
  can legitimately have no entries: the `EmptyState` names its next step, or states that returning
  to Settings is the only one.
- A **sparse profile** (`ProfileHeader` *empty*) renders a missing bio and zero counts as calm,
  labelled zeros and a short prompt, not as blank space. Next step: on the person's own profile,
  edit the profile or compose a chirp; on someone else's, follow them.
- A person with **no picture** (`Avatar` *empty*) shows their initials monogram, never a
  broken-image glyph. This is a fallback inside a surface, not an empty surface, so it needs no
  next step.

An empty surface and a failed-to-load surface are never shown as the same thing. A surface with no
content uses the *empty* treatment above; a surface that tried to load and failed uses the
`EmptyState` *error* variant described below, with a retry. "There is nothing here" and "we could
not load this" are different facts and lead to different next steps, so they read differently.

### Loading: show the shape of what is coming, and never spin forever

A **first load** of a surface shows `LoadingState` skeletons at the real dimensions of the content
on its way: skeleton `ChirpCard`s in a `ListView`, a skeleton `ProfileHeader`, a skeleton `Avatar`
circle at its target size. Holding the true size means the layout does not jump when real content
arrives, and the person sees the shape of the page forming rather than a spinner on a blank screen.

An **in-place or incremental load** shows a bounded indicator at the point of the action, not a
full-screen takeover:

- loading older items at a list boundary: a bounded spinner at the `ListView` load-more boundary,
  with the already-loaded items left in place;
- a running action: the `PrimaryButton` / `SecondaryButton` busy state, holding its label and its
  width so nothing shifts, and locking briefly so the action is not double-fired;
- a setting saving: the `Toggle` / `SettingRow` pending treatment on that row;
- an async field check (handle availability at sign-up): the `TextField` pending indicator, the
  field not yet marked valid or invalid.

**Nothing loads forever.** A bounded spinner is the only element permitted to animate continuously,
per the motion rules; a load that does not resolve hands off to the owning component's *error* state
rather than spinning on. When the reader has asked their system to reduce motion, a skeleton is
static and the spinner remains bounded, so the loading state never relies on movement to be
understood.

The persistent `NavShell` does not participate in any of this: moving between screens never blanks
the frame. Only the destination's content region shows a loading state; the navigation around it
stays put.

### Error: shown where the action was taken, in plain words, with a way forward

A failure is reported at the point of the action, in plain language, with something the person can
do about it. It is never a silent no-op (an action that quietly does nothing), never a raw system
message or error code, and never phrased to blame the person.

The level of the error decides which component carries it:

- **Field level:** a `TextField` validation failure or a failed field check shows `InlineError`
  beneath the field, naming the problem and the fix ("That handle's already taken — try another"),
  tied to the field for assistive technology.
- **Control level, in place:** a like, follow, or setting change that fails shows `InlineFeedback`
  in the danger role at the control and reverts the optimistic change, so the control never shows a
  result that did not happen; any drafted reply next to it is kept.
- **List level:** a list that fails to load, in any screen including a settings list such as
  sessions & devices, shows the `ListView` *error*: an `InlineError` with a retry in place of the
  missing items. A failure while loading *older* items shows at the load-more boundary and keeps the
  items already on screen.
- **Surface level:** a whole surface that fails to load (a profile, a settings page) shows the
  `EmptyState` *error* variant with a retry. The `EmptyState` *error* variant is reserved for the
  whole surface; it is also how a failed load is told apart from an empty surface.
- **Task / dialog level:** a `Dialog` action that fails shows an `InlineError` inside the panel and
  leaves the dialog open with any draft preserved, so the person can retry without starting over.
  Dialogs use the `Dialog` component's own state names. *Empty* does not apply to a dialog. A
  confirm that stays unavailable until a required input is given is the *Disabled* state, named
  *Disabled*.
- **Background, no on-screen control:** a failure with no single control to attach to shows a
  danger-role `Toast` carrying a word as well as the colour, never colour alone.

Every one of these leaves the person a way forward (retry, correct, or a clear way out) and
preserves whatever they had entered.

**A removed or missing item follows one rule.** Inside a surface that already shows the item's
neighbours, such as a conversation thread or a list, a removed chirp stays as an in-place tombstone
reading "This chirp isn't available". An address that opens directly onto something that does not
exist or was removed goes to the **Not found** screen, with the same "This chirp isn't available"
for a chirp and "This account doesn't exist" for a profile. An account that exists but is blocked or
suspended stays on its **Public profile**, with an in-place statement ("This account is
unavailable" when suspended), because the viewer's relationship to that account is part of the
screen.

### Expired session and transient error: recover without losing work

This pattern composes against the information architecture's session-expiry convention (REQ-UX-008)
and its auth-gated return (REQ-UX-007). It does not redefine them; it states how the product's state
treatment carries a person through an expiry or a passing failure without costing them their work.

- **An expired or invalid session** routes the person to **Sign in** with the reason stated plainly
  ("Your session's expired — sign in to pick up where you left off") rather than failing silently
  or showing a generic error. After signing back in, they return to where they were: the screen and
  the position they asked for, not a default landing screen.
- **The draft survives the round-trip.** A chirp or reply drafted in the `ComposeBox` is preserved
  across the interruption: the person is routed to sign-in and the draft is handed back to the
  `ComposeBox` when they return, so an expiry never costs them their words. This is the
  `ComposeBox`'s draft-preservation behaviour, held as a product-wide guarantee wherever a person can
  have in-progress input.
- **A transient error** (a server hiccup while posting, a dropped request) is retryable in place
  without losing in-progress work. The `ComposeBox` keeps the draft and shows an `InlineError` with
  a retry; a `Dialog` stays open with its content; a list keeps what it already displayed. The retry
  succeeds without the person re-entering anything.
- **The two are never shown as each other.** An expired session is an authentication condition:
  route to sign-in, explain, return. A transient error is a retry condition: stay on the screen,
  retry in place. A passing hiccup does not dump the person to sign-in, and an expiry is not dressed
  up as a retryable error that quietly keeps failing.

### How per-screen states compose against these patterns

The screen designs for getting in, the core loop, the account lifecycle, and safety and
notifications each specify their own screens' empty, error, and loading states. They do so by
composing the component library's named states with the four patterns above, not by inventing a
conflicting treatment. The result is one product: a person reaching an empty list, a slow load, a failed action, or a lapsed
session meets the same designed behaviour on the home timeline, a profile, a settings sub-section,
and a dialog.

## Requirements and acceptance criteria — REQ-UX-086..089

These four requirements fix the product-wide state treatment. Each is testable by someone who never
met its author, exercisable on the live product, carries a `release_gating` flag, and references the
product requirement it serves.

#### REQ-UX-086 — Empty surfaces are explained, never blank
- **statement**: Every surface that has nothing to show presents a designed empty treatment: a
  short explanation of why it is empty and at least one next step (an action or a route the person
  can take from that surface), rather than a blank area. An empty surface is visibly distinct from
  one that failed to load.
- **acceptance_criteria**: Reach a brand-new home timeline, an empty notifications surface, and an
  empty followers list; each shows an explanation and at least one next step (for example, the new
  timeline points to Explore and to composing a first chirp, and the empty notifications surface
  points to Explore), not a blank region. Then cause a
  surface to fail loading; it shows a distinct "couldn't load — try again" treatment with a retry,
  clearly different from the empty treatment.
- **release_gating**: true
- **references**: REQ-PROD-033

#### REQ-UX-087 — Loading shows the shape of what is coming and never runs forever
- **statement**: A first load shows skeletons at the real dimensions of the content, an in-place or
  incremental load shows a bounded indicator at the point of the action, the persistent navigation
  frame never blanks, and no load spins indefinitely. A load that does not resolve becomes an error
  with a way forward.
- **acceptance_criteria**: Open the home timeline on a slow connection; the content area shows
  skeleton rows at the size of real chirps rather than a spinner on a blank page, and the navigation
  frame stays visible. Load older items; a bounded spinner appears at the list boundary while the
  already-loaded items remain on screen. Force a load to fail; it stops and offers a retry rather
  than spinning without end.
- **release_gating**: true
- **references**: REQ-PROD-033

#### REQ-UX-088 — Failures appear where the action was taken, in plain words, with a way forward
- **statement**: Every failure is reported at the point of the action (field, control, list,
  surface, dialog, or a toast where there is no on-screen control) in plain language with no system
  or error code, never as a silent no-op, and always leaves the person a way to retry or correct
  with their input preserved.
- **acceptance_criteria**: Trigger a field error (for example a taken handle at sign-up), a failed
  in-place action (for example a like or follow that fails), and a failed list page; each shows a
  plain-words message at the point of the problem with a retry or correction, no error code and no
  blank, and the optimistic in-place action reverts rather than showing a result that did not
  happen.
- **release_gating**: true
- **references**: REQ-PROD-033

#### REQ-UX-089 — An expired session and a transient error both recover without losing work
- **statement**: An action taken with an expired or invalid session routes the person to sign-in
  with the reason stated and returns them to where they were afterwards, and a transient error is
  retryable in place; in both cases in-progress work such as a drafted chirp is preserved. This
  composes against the information architecture's session-expiry convention (REQ-UX-008) and
  auth-gated return (REQ-UX-007) and does not redefine them.
- **acceptance_criteria**: With a session expired, draft a chirp and try to post; you are routed to
  sign-in with a stated reason rather than a silent failure, and after signing in your drafted text
  is intact and you are back where you were. Separately, cause a transient server error while
  posting; you can retry in place and the post succeeds without re-typing the draft.
- **release_gating**: true
- **references**: REQ-PROD-034
