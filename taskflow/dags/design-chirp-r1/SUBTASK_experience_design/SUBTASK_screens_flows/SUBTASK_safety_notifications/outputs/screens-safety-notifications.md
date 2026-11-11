### Safety, notifications, and public-explanatory surfaces

chirp is a space where strangers post at each other. That is the product's reason to exist and
also its risk: a person who is replied to by someone they want nothing to do with, or who sees a
chirp that breaks the rules, needs somewhere to turn that is built into the product, not improvised
later. The surfaces in this section are the ones that make chirp feel minded: the place a person sees
what has been directed at them, the place they report a problem, the controls that stop an unwanted
account, the list of who they have shut out, the way to get help, the rules a report points to, and
the screen a person lands on when a link no longer resolves. None of these is the product's headline;
each is part of whether a stranger trusts it.

Every screen below is a screen named in the **Screen inventory** and is assembled from
**Component library** components by name. Two additive controls are used by name and not redefined
here: **ChoiceList** (one-of-many selection, used for the Report reasons and the Notifications
filter) and **UnseenMarker** (the per-item "New" marker, used on Notifications). Each screen is
designed with its layout, its content, its primary action, and its empty, error, and loading states.
A state marked "does not apply" is a design decision with its reason, in the component library's
sense, not an omission. The per-screen states compose the components' own named states and the
product-wide patterns in the empty, error, and loading states section; they do not invent a
conflicting treatment. Two of these surfaces (Notifications and the block/mute controls) ride product
requirements the release bar does not gate; that staging is carried into their `REQ-UX` entries so it
stays explicit.

The notification **preferences** settings sub-section (which activity categories send a
notification) belongs with the account settings screens; this section designs the Notifications
activity surface and cross-references those preferences where a person would reach for them. The
operator's moderation and support tooling is the operational-readiness area's; this section designs
only the **user-facing entry** to help and support, which is where a person's path into that tooling
begins.

---

#### Notifications

The activity surface: the person's own copy of what others have directed at them. It realises the
inventory's **Notifications** screen (`/notifications`, feed/list, signed-in) inside the signed-in
**NavShell**, whose Notifications entry carries the unseen-activity indicator this screen clears.

- **Layout.** The signed-in **NavShell** frames the screen; the Notifications destination is marked
  active. The main column is a **ListView** at the 600px reading measure, titled "Notifications". At
  the head of the list sits a single, quiet **ChoiceList** in its inline row form (All, Replies,
  Follows, Likes) so a person can narrow a busy list without leaving the screen. All is selected on
  arrival; exactly one option is selected at a time, the selected option is marked by more than
  colour, and arrow keys move the selection. Below it, the list of activity, newest first, in bounded
  pages with the ListView's load-older affordance.
- **Content.** Each item is the row kind this list needs (per **ListView**, which hosts the row the
  screen needs): an **Avatar** (`avatar.md`) of the acting person, a line in `type.body` naming the
  activity in chirp's voice ("Dana replied to your chirp", "Sam followed you", "Three people liked
  your chirp"), a short relative timestamp in `type.meta`, and, for a reply, an inline **ChirpCard**
  preview of the reply so the person can read and act on it in place. A follow row carries a
  **SecondaryButton** to follow back; a reply row carries the ChirpCard's own reply and like
  controls. The whole row is a target that opens the chirp in its conversation or the person's
  profile. An unseen item carries the **UnseenMarker**.
- **Primary action.** Read the activity and act on it in place (open a reply's conversation, follow
  back, or like in return) without leaving the list. Opening the screen is itself the act that marks
  the activity seen and clears the shell's unseen indicator.
- **Unseen and cleared states.** Arriving activity raises the NavShell's unseen indicator (that
  indicator is the shell's, cross-referenced here, not redesigned). Opening Notifications marks the
  shown items seen and clears the indicator. A newly-unseen item shows the **UnseenMarker** in its
  shown state: a dot in `color.primary` paired with the text label "New", so colour is never the sole
  carrier. When the item has been seen the marker is hidden.
- **Empty state.** No activity yet → the ListView's **EmptyState**: a calm illustration, "No activity
  yet", and a one-line explanation that replies, follows, and likes will show up here, with a link to
  Explore so the person has a next step rather than a blank column. When a filter option is selected
  and has no items, the same EmptyState names the filter ("No replies yet") and offers a link back to
  All.
- **Error state.** A page fails to load → the ListView's **InlineError** with a retry in place of the
  missing items; a failure while loading older items shows at the load-more boundary and keeps the
  items already shown. An act-in-place failure (a follow-back that did not take) shows
  **InlineFeedback** at the control in the danger role and reverts.
- **Loading state.** First load shows **LoadingState** skeleton rows at the rows' real height, not a
  spinner on a blank screen; loading older items shows a bounded spinner at the boundary.

#### Report

The way a person reports a chirp or an account that breaks the rules, and is told the report was
received. It realises the inventory's **Report** dialog (modal/dialog, signed-in), opened from the
report action in a **ChirpCard**'s more-actions menu or from a profile's more-actions menu.

- **Layout.** A **Dialog** (modal variant) over the `color.bg.scrim`: `type.heading` title "Report
  this chirp" or "Report this account"; a short line naming what is being reported (the chirp's
  author and a one-line quote, or the handle); a **ChoiceList** in its stacked form holding the
  reasons, drawn from the **Rules & terms** so a report always points at a stated rule; an optional
  **TextField** (multi-line) for "Anything else we should know?"; and the action pair, a
  `color.primary` **PrimaryButton** "Submit report" and a **SecondaryButton** "Cancel". Exactly one
  reason is selected at a time, the selection is reachable and operable by keyboard, and it is
  announced to assistive technology.
- **Content.** The reasons are the rule categories named on Rules & terms, phrased plainly
  ("Harassment or targeting", "Spam", "Something else"). The dialog says, in `type.meta`, that the
  operator reviews reports and that blocking the account is available too (a link that opens the
  **Block / mute** confirmation), so reporting and stopping contact are offered together.
- **Primary action.** Submit the report. On success the dialog resolves to a receipt: a brief
  in-panel confirmation and a **Toast** ("Thanks, we've received your report") so the person knows
  it landed. This acknowledgement is the gated behaviour (a report that is silently swallowed is not
  a report).
- **Empty state.** Does not apply. The dialog always opens with its reasons listed; there is nothing
  for it to be empty of.
- **Disabled state.** No reason chosen yet → "Submit report" is in the **Dialog**'s Disabled state,
  with a `type.meta` hint to choose a reason. If the person tries to submit anyway, the ChoiceList
  shows its error state, an **InlineError** beneath it that says a reason is required. The optional
  detail field shows its placeholder.
- **Error state.** The submit fails → an **InlineError** inside the panel in plain words, the dialog
  stays open, and the chosen reason and any typed detail are preserved so the person can retry. If the
  session has expired at submit, the product routes to Sign in with the reason stated and the report
  draft preserved, per the IA session-expiry convention (cross-referenced, not redesigned).
- **Loading state.** Submit in flight → the confirm button shows its busy state and the dialog does
  not close until the submission resolves; the reason and detail stay locked so the report is not
  sent twice.

#### Block / mute

The controls that stop unwanted interaction, each confirmed with its effect stated plainly before it
takes. It realises the inventory's **Block / mute** screen (confirmation, signed-in), opened from a
profile's or a ChirpCard's more-actions menu.

- **Layout.** A **Dialog** (confirmation variant) over the scrim: `type.heading` title ("Block
  @handle?" / "Mute @handle?"); `type.body` content stating exactly what the action does; and the
  action pair, a `color.danger` **PrimaryButton** ("Block" / "Mute") and a **SecondaryButton**
  "Cancel".
- **Content.** The effect is stated without euphemism. Block: "They won't be able to follow you, see
  your chirps while signed in, or reply to you, and you won't see them. They aren't told you blocked
  them." Mute: "You'll stop seeing their chirps and replies in your timeline and notifications. They
  can still see and reply to you, and they aren't told." A single line notes where to undo it: the
  **Blocked & muted** settings screen.
- **Primary action.** Confirm the block or the mute. On success the dialog closes and a **Toast**
  confirms it ("@handle blocked") with an inline undo; the person is returned to where they were.
- **Empty state.** Does not apply. A confirmation always opens with its stated consequence and its
  two choices; there is nothing for it to be empty of.
- **Disabled state.** Does not apply. Both choices are available as soon as the dialog opens; no
  input is required first.
- **Error state.** The action fails → an **InlineError** inside the panel; the dialog stays open so
  the person can retry, and nothing has changed until it succeeds (the control never reports an effect
  that did not take).
- **Loading state.** Confirm in flight → the confirm button shows its busy state and the dialog holds
  open until the action resolves.

#### Blocked & muted

The settings screen where a person sees and manages the accounts they have blocked or muted. It
realises the inventory's **Blocked & muted** screen (`/settings/blocks`, settings, signed-in),
reached from the **Settings** hub (the hub itself is an account settings screen, cross-referenced
here) and framed by the signed-in **NavShell**.

- **Layout.** A settings screen at the reading measure with two labelled sections, "Blocked" and
  "Muted", each a list of **SettingRow**s. Each row carries the account's **Avatar** (`avatar.md`),
  display name and handle, and a **SecondaryButton** ("Unblock" or "Unmute") in the row's control
  slot. A back affordance returns to the Settings hub.
- **Content.** One row per blocked or muted account, the two kinds kept visually separate so a person
  can tell at a glance what each account's status is. A row's meta line notes when the account was
  blocked or muted, in `type.meta`.
- **Primary action.** Unblock or unmute an account from its row. The change takes effect immediately
  and confirms on the row with **InlineFeedback**; an unblocked or unmuted account leaves its list.
- **Empty state.** No blocked or muted accounts → an **EmptyState** within the section ("You haven't
  blocked or muted anyone") that explains why the lists are empty and how they fill: a person blocks
  or mutes from the more-actions menu on a profile or a chirp. The next step is a link, "Go to your
  timeline", where that menu is reachable. Each section shows its own empty block so one being empty
  does not hide the other.
- **Error state.** The list fails to load → the section's **InlineError** with a retry; an unblock or
  unmute that fails → **InlineFeedback** in the danger role on that row with the prior status restored.
- **Loading state.** **LoadingState** skeleton rows while the lists resolve; a row saving an
  unblock/unmute shows a brief pending treatment on its control.

#### Help & support

The user-facing entry to getting help: recovering access, reporting a problem, and reaching the
operator. It realises the inventory's **Help & support** screen (`/help`, empty/landing, reachable in
both shells), rendered in whichever **NavShell** the person is in. This is the entry only; the
operator's support and moderation tooling is the operational-readiness area's.

- **Layout.** An **EmptyState**-style explanatory screen at the reading measure: a `type.title`
  heading "Help & support", a short `type.body` intro, and a small set of labelled entries, each a
  heading and a sentence with a link or action.
- **Content.** The entries are the things a person actually comes here for: "Can't get in?" linking to
  **Recover access** (an entry-and-authentication surface, cross-referenced) so recovery is reachable
  from help even when the sign-in cross-links are not shipped; "Report a problem" explaining how to
  report a chirp or account and linking to the **Rules & terms**; "Managing your account" linking to
  Settings; and "Contact support", the user-facing way to reach the operator for something the
  self-service paths do not cover, which is where a person's path into the supported operator surface
  begins. A signed-out visitor sees the same page in the signed-out shell, with the recovery and
  contact entries foremost.
- **Primary action.** Reach the right help path, most often **Recover access** or **Contact
  support**; the screen leads with those so the common need is one step away.
- **Empty state.** Does not apply. This is an explanatory page whose content is always present; it is
  itself an empty/landing screen, so there is no data-empty variant to show.
- **Error state.** If the page's content is served and fails to load, the **EmptyState** error variant
  ("We couldn't load this. Try again.") with a retry; the shell and its recovery and contact entries
  remain reachable so a person is never stranded on a failed help page. A "Contact support" submission
  that fails shows an **InlineError** at the point of the action with the message preserved.
- **Loading state.** The persistent shell renders immediately; while the page body resolves it shows a
  brief **LoadingState**, not a blank panel.

#### Rules & terms

The stated rules (what is and is not allowed) that a report points at, together with the product's
terms. It realises the inventory's **Rules & terms** screen (`/rules`, empty/landing, reachable in
both shells), rendered in whichever **NavShell** the person is in.

- **Layout.** A reading-measure document screen: a `type.title` heading "Rules & terms", a short
  `type.body` preamble, then the rules as named, numbered sections in `type.heading` + `type.body`,
  the categories the **Report** dialog's reasons map to, followed by the terms.
- **Content.** Each rule is a plain statement of a behaviour that is not allowed (harassment and
  targeting, spam, impersonation, and the like) in chirp's voice, written so a person can tell whether
  a chirp broke it and so a report can point at it. The terms state the ordinary expectations of using
  the service. A line at the foot links to **Report** for acting on a rule and to **Help & support**.
- **Primary action.** Read and, where the person arrived to act, report a problem. A "Report a
  problem" link opens the **Report** dialog against the chirp or account they came from. For a
  signed-out visitor the shell's Sign up remains the prominent action.
- **Empty state.** Does not apply. The rules are always present content; an empty/landing screen has
  no data-empty variant.
- **Error state.** If the content fails to load, the **EmptyState** error variant with a retry, inside
  the persistent shell so the footer and navigation stay reachable.
- **Loading state.** The shell renders immediately; a brief **LoadingState** stands in for the body
  while it resolves.

#### Not found

The screen a person lands on when an address opens onto something that does not exist or has been
removed: a mistyped URL, a deleted chirp opened directly, a profile that no longer exists. It explains
the absence and routes back to a known place rather than dead-ending. It realises the inventory's
**Not found** screen (any unresolved path, empty/landing, both shells).

One rule decides where a missing or removed resource appears:

- An address that opens directly onto a resource that does not exist or was removed (a chirp, a
  profile, or any route) goes to this screen.
- Inside a surface that already shows the resource's neighbours (a conversation thread, a list), a
  removed chirp is an in-place tombstone, handled where it occurs.
- An account that exists but is blocked or suspended stays on its Public profile route with an
  in-place statement, because the viewer's relationship to it is part of that screen. It is handled
  there, not here.

- **Layout.** An **EmptyState** at generous spacing inside whichever **NavShell** applies: a calm
  illustration, a `type.title` heading "This isn't here", a `type.body` line explaining that the page,
  chirp, or account could not be found or has been removed, and a **PrimaryButton** back to a known
  place.
- **Content.** The explanation names the case plainly without exposing anything private. A route that
  never existed or was mistyped reads "We couldn't find this page". A chirp that was removed reads
  "This chirp isn't available", the same words as the tombstone a **ChirpCard** shows in place, so the
  two never contradict each other. A profile address for an account that does not exist or was
  deleted reads "This account doesn't exist". Blocked and suspended accounts do not appear here; the
  Public profile screen states "This account is unavailable" in place.
- **Primary action.** Go to a known place: "Go to your timeline" for a signed-in person, "Go to
  chirp" (the Landing) for a signed-out one, so the screen is always a way back, never a wall. A
  secondary link reaches **Help & support**.
- **Empty state.** Does not apply. This screen is itself the treatment for an absent resource; it has
  no further empty variant.
- **Error state.** Does not apply as a distinct state. Not found is already the product's answer to an
  unresolved or removed resource; a load failure of a resource that does exist is that resource's own
  error state (a ListView InlineError, a ProfileHeader error), not this screen.
- **Loading state.** Does not apply. Not found is a resolved outcome, not a surface awaiting content;
  the shell renders it immediately. While a route is still resolving, the destination screen shows its
  own **LoadingState**, and Not found appears only once resolution has concluded the resource is
  absent, so a slow load is never mistaken for a missing resource.

---

#### Requirements and acceptance criteria: REQ-UX-078..085

The safety, notifications, and public-explanatory requirements chirp must meet. Each is testable by
someone who never met the author, against the live product; each carries a `release_gating` flag and
references the product requirement(s) it serves. Where a requirement implements a non-gating product
requirement, its gating follows the product requirement's own staging, and the reason is stated.

##### REQ-UX-078 — A notifications surface that shows directed activity and clears when seen
- **statement**: The signed-in Notifications screen shows activity directed at the person (replies,
  follows, and likes) newest first in bounded pages, lets them act on an item in place, can be
  narrowed to one kind of activity, marks unseen items with a labelled "New" marker, and opening it
  marks the shown activity seen and clears the shell's unseen-activity indicator.
- **acceptance_criteria**: Have another account reply to, follow, and like you; the shell's
  Notifications entry shows an unseen indicator. Open Notifications; the three activities appear
  newest-first, each unseen item carries a marker with the text "New", a reply can be opened in its
  conversation and a follow followed back from the row, and the unseen indicator clears. Choose
  Replies in the filter; only replies show and the selected option is distinguishable without colour.
  Confirm the list loads a bounded page with a way to load older items, not every item at once.
- **release_gating**: false: notifications ride REQ-PROD-029, which the release bar does not gate; the
  surface and its indicator ship when notifications ship.
- **references**: REQ-PROD-029

##### REQ-UX-079 — Reporting a chirp or account, acknowledged as received
- **statement**: A signed-in person can report a chirp or an account against a stated rule, optionally
  add detail, and on submission sees that the report was received; a report is never silently
  swallowed.
- **acceptance_criteria**: From a chirp's and from an account's more-actions menu, open the report
  dialog, choose a reason drawn from the rules, and submit; each submission is acknowledged as received
  (an in-product confirmation). Open the dialog and attempt to submit with no reason chosen; the
  submit button is disabled until a reason is chosen, and the reasons can be chosen and changed with
  the keyboard alone.
- **release_gating**: true
- **references**: REQ-PROD-025, REQ-PROD-026

##### REQ-UX-080 — Block and mute, each confirmed with its effect stated
- **statement**: A signed-in person can block or mute another account through a confirmation that
  states plainly what the action does before it takes, with a way to cancel, and a confirmation that it
  took.
- **acceptance_criteria**: From an account's more-actions menu, choose block; a confirmation states the
  effect (they can't see or interact with you; you won't see them; they aren't told) and offers cancel.
  Cancel; nothing changes. Choose mute; a confirmation states its distinct effect. Confirm either; it
  takes and is confirmed, and the account appears on the blocked & muted screen.
- **release_gating**: false: block/mute ride REQ-PROD-027, which the release bar does not gate;
  reporting (REQ-UX-079) is the gated safety floor and these controls ship as the expected near-term
  addition.
- **references**: REQ-PROD-027

##### REQ-UX-081 — Managing the accounts a person has blocked or muted
- **statement**: A signed-in person can see the accounts they have blocked and the accounts they have
  muted, told apart, and can unblock or unmute any of them, with the change taking effect immediately.
- **acceptance_criteria**: Block one account and mute another, then open the blocked & muted settings
  screen; each appears under the right heading. Unblock the first and unmute the second; each leaves its
  list and the change is confirmed. With none blocked or muted, the screen explains the lists are empty
  rather than showing blank rows, says how they fill, and offers a link to the timeline.
- **release_gating**: false: the management screen serves the block/mute controls of REQ-PROD-027,
  which the release bar does not gate; it ships with those controls.
- **references**: REQ-PROD-027

##### REQ-UX-082 — A user-facing help & support entry reachable from both shells
- **statement**: A help & support screen, reachable from both the signed-out and the signed-in shell,
  gives a person the way to recover access, to report a problem, and to contact the operator for what
  self-service does not cover.
- **acceptance_criteria**: With no session, open Help & support from the signed-out shell; a path to
  recover access and a way to contact support are present. Signed in, open it from the account menu;
  the same entries plus account management are present, and "Can't get in?" reaches recovery and
  "Contact support" reaches the operator contact path.
- **release_gating**: true
- **references**: REQ-PROD-028, REQ-PROD-013

##### REQ-UX-083 — Stated rules a report can point to
- **statement**: The product states its rules (what is and is not allowed) as named categories a
  person can read and a report can reference, reachable from both shells.
- **acceptance_criteria**: Open Rules & terms from the shell; the rules are present as named
  categories. Open the report dialog; its reasons correspond to those stated rule categories, so a
  report points at a stated rule rather than an unexplained choice.
- **release_gating**: true
- **references**: REQ-PROD-026

##### REQ-UX-084 — A not-found screen that explains and routes back
- **statement**: An address that opens onto a resource that does not exist or was removed (a mistyped
  path, a deleted chirp, a profile that no longer exists) lands the person on a not-found screen that
  explains the absence without exposing private detail and offers a way back to a known place. A
  removed chirp inside a conversation is an in-place tombstone, and a blocked or suspended account
  stays on its profile with an in-place statement; both use the same words as this screen.
- **acceptance_criteria**: Open a URL that does not resolve; a not-found screen says "We couldn't find
  this page" and offers a way to a known place (the timeline when signed in, the landing when signed
  out). Open the address of a removed chirp directly; the screen says "This chirp isn't available".
  Open the profile address of an account that does not exist; the screen says "This account doesn't
  exist". View a removed chirp inside a conversation; the in-place tombstone reads "This chirp isn't
  available". Open the profile of a suspended account; it stays on the profile and reads "This account
  is unavailable".
- **release_gating**: true
- **references**: REQ-PROD-033

##### REQ-UX-085 — Every safety and notification surface presents considered empty, error, and loading states
- **statement**: Each surface in this section presents a considered empty, error, and loading state
  (composed from the component library's named states and the product-wide patterns), or states plainly
  where a state does not apply, rather than a blank area or a silent failure. Where a surface is empty
  because nothing exists yet, it explains why and offers a next step.
- **acceptance_criteria**: On the Notifications screen force each of an empty list, a failed page load,
  and a first load; each shows an understandable state (an explained empty block with a link to
  Explore, an inline error with retry, skeleton rows) rather than a blank or a hang. On the report and
  block/mute dialogs force a failed submission; each keeps the dialog open with its input preserved and
  an inline error. On the blocked & muted screen with nothing blocked, an explained empty state appears
  with a next step.
- **release_gating**: true
- **references**: REQ-PROD-033, REQ-PROD-034

---

*Composition note.* Every screen above is a Screen-inventory screen referred to by name, assembled
from Component-library components by name, using those components' own named states, plus the
additive controls ChoiceList and UnseenMarker. The Notifications row is the "row kind the screen
needs" that **ListView** provides for, composed from existing components, not a new component. The
notification **preferences** sub-section, the **Settings** hub, and the **Recover access** screen
belong to other sections and are cross-referenced here, not redesigned. The per-screen empty, error,
and loading states compose the product-wide patterns in the empty, error, and loading states section.
