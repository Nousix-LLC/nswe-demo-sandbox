# Account settings (`settings_management`)

The account-settings surfaces a releasable chirp needs: the Settings hub and its three
management sub-sections. chirp is a hosted, public, account-based microblog; at the current
commit the live product offers no way to change any account setting, so the defect these
screens close is absence, not styling. Each surface is a designed screen — layout, content, a
primary action, and its empty, error, and loading states — realising a named screen from the
screen inventory and built from named components in the component library. The screens appear
below in screen-inventory order (Settings hub, Account & contact, Notification preferences,
Sessions & devices), followed by the consolidated `REQ-UX-069..074` register. Every screen
serves journey J6 (managing the account); every requirement traces to at least one `REQ-PROD-*`.

---

## Settings hub — `/settings`

The Settings hub is where a signed-in person goes to manage their account. It realises the **Settings**
screen in the screen inventory (`/settings`, **settings** archetype, signed-in) and is the home for the
account-level choices the recovery-contact, sign-out, and notification requirements imply. It is a
navigation surface: it lists every settings sub-section and leads into each, but designs none of their
contents. It serves journey **J6 — Managing the account** and traces to **REQ-PROD-017** (an account
settings surface).

The hub is the small secondary navigation the IA describes (REQ-UX-017): each sub-section it lists is a
screen a person can open directly by its own URL and return from to the hub.

### Layout

The hub renders inside the signed-in **NavShell**, in the 600px reading column (`space.measure`), centred
on wider viewports with the shell and any secondary rail outside it; on a phone it fills the viewport with
a `space.gutter.mobile` (16px) edge. Top to bottom:

- **Screen heading** — "Settings" in `type.title`, the main heading that names the screen (the document
  title names it too, per the wayfinding convention). The active primary-nav destination is marked in the
  shell.
- **Account summary** — a quiet, non-interactive header that names whose account this is: **Avatar** at
  `avatar.lg`, the display name in `type.heading`, and the handle in `type.meta` / `color.text.secondary`.
  It identifies the signed-in account at a glance, which matters on a shared or borrowed device. It is
  context, not a control, and it edits nothing — editing the profile is the first row below.
- **Grouped sub-section list** — the sub-sections as **SettingRow**s, gathered under short section labels
  (`type.heading`, `space.6` above each group) so the list is scannable rather than a flat run of seven
  rows. `color.border.default` hairlines separate the rows; each row has `space.4` padding. The group
  labels are headings drawn from the type scale, not a new component.

There is no secondary content, no form, and no footer action on this screen; it is a list of destinations.

### Content — the sub-sections the hub lists

Every settings sub-section named in the inventory (REQ-UX-017) appears here, each as a **SettingRow** with
a label (`type.body`), a one-line description (`type.meta` / `color.text.secondary`), and a chevron
**IconButton** (`icon.md`) as the drill-in affordance. The row order is grouped by what a person is trying
to do; each row opens the inventory screen named in its route and is independently addressable.

| Group | Row (label) | Description | Opens (inventory screen / route) | Designed by |
|---|---|---|---|---|
| Account | Edit profile | Change your display name and bio. | Edit profile — `/settings/profile` | owned elsewhere (linked only) |
| Account | Account & contact | Your verified contact and your handle. | Account & contact — `/settings/account` | sibling sub-section |
| Notifications | Notification preferences | Choose which activity sends you a notification. | Notification preferences — `/settings/notifications` | sibling sub-section |
| Privacy and safety | Blocked & muted | Accounts you've blocked or muted. | Blocked & muted — `/settings/blocks` | owned elsewhere (linked only) |
| Security | Sessions & devices | Where you're signed in, and signing out. | Sessions & devices — `/settings/sessions` | sibling sub-section |
| Your data | Export your data | Download your chirps, profile, and follows. | Export your data — `/settings/export` | owned elsewhere (linked only) |
| Your data | Delete account | Permanently delete your account. | Delete account — `/settings/delete` | owned elsewhere (linked only) |

Notes on specific rows:

- **Delete account** is the destructive row. Its label uses `color.danger` and it carries no inline
  toggle or value — selecting it routes to the Delete account **confirmation** (owned by the leaving
  sub-section), which names what is and is not kept and points to export first. The hub styles and routes
  this row; it does not design the confirmation. This follows the destructive-confirmation convention
  (REQ-UX-011): the hub never deletes on a row tap.
- **Notification preferences** rides REQ-PROD-029, which the release bar does not gate. The row is present
  when notifications are in the release and absent when they are not; every other row is present in the
  first release. Its absence is the only variation in the list.
- The three sibling sub-sections (Account & contact, Notification preferences, Sessions & devices) and the
  four linked-only ones are referenced here by their inventory name and route; this screen designs none of
  their contents.

### Primary action

The hub's primary action is **opening a settings sub-section** — the drill-in on a **SettingRow**, which
is the repeated, equally-weighted affordance the whole screen is built around. The Account group sits
first because editing the profile and managing the contact are the most common reasons a person opens
settings.

There is deliberately **no single PrimaryButton** on this screen. The settings archetype is a list of
peer destinations, not a form with one submit, so a lone call-to-action would misrepresent what the screen
is for. Sign out is not placed here either: it is reached from the account menu in the **NavShell** and is
designed into the Sessions & devices sub-section, so the hub lists the way to it rather than owning the
action.

### States

**Loading.** The sub-section list is a fixed menu and renders immediately, the same way the **NavShell**
does — moving into settings never blanks the list behind a spinner. The one part that resolves from the
account is the **Account summary** header: while it resolves it shows **LoadingState** — the **Avatar**
*loading* skeleton circle at `avatar.lg` plus two short skeleton lines standing in for the name and handle
at their real size, so the list below does not jump when the summary arrives. The list is usable
throughout.

**Empty.** Does not apply. The hub lists a fixed set of sub-sections that always exists (REQ-UX-017), so
there is no empty variant of the screen. This matches the composed components' own decisions: **SettingRow**
records *empty* as not applying at the row level, and **NavShell** records *empty* as not applying because
its destinations are fixed. (An individual sub-section with nothing in it — no blocked accounts, no other
sessions — shows an **EmptyState** inside that sub-section, which its owning spoke designs; that is not a
state of the hub.)

**Error.** The sub-section list does not fetch, so it has no load-failure of its own — it always renders.
Two error paths are designed, both by composing existing treatments rather than inventing one:

- **Account summary fails to resolve** → the summary degrades and the navigation stays whole. The
  **Avatar** falls back to its *error* treatment (the initials monogram, never a broken-image glyph); if
  the name and handle cannot be read, the summary collapses to a quiet, unobtrusive header rather than
  showing a broken block. The sub-section list below remains fully usable, so a person can always reach
  Sessions & devices or Delete account even when their summary did not load. A cosmetic header never blocks
  the account controls.
- **Reached without a valid session, or the session expires mid-use** → the product routes to **Sign in**
  with the reason stated and returns the person to `/settings` after they sign back in, preserving any
  in-progress input. This is the product-wide auth-gating and session-expiry behaviour (REQ-UX-007,
  REQ-UX-008); the hub composes it and does not redesign it.

### Composition notes

- **Components used** (by name, from the component library): **NavShell** (signed-in), **SettingRow**,
  **IconButton** (chevron drill-in; account menu), **Avatar** (`avatar.lg`), **LoadingState**, and the
  **Dialog** confirmation variant reached by the Delete account row (owned elsewhere). Group labels are
  `type.heading` from the type scale. No component, screen, token, or ad-hoc value is introduced here.
- **Conventions composed** (not redesigned): settings-as-secondary-nav (REQ-UX-017), destructive
  confirmation (REQ-UX-011), the sign-out transition (REQ-UX-016, via the account menu / Sessions &
  devices), auth-gated routing and return-to (REQ-UX-007), and session expiry mid-use (REQ-UX-008).
- **Product-wide state patterns**: the hub's loading and error treatments stay consistent with the
  product-wide empty / loading / error patterns and the expired-session recovery behaviour owned by the
  considered-states area; the hub composes those patterns and does not define a conflicting one.

---

## Account & contact — `/settings/account`

**Screen (inventory):** Account & contact — `/settings/account` — *settings* archetype — signed-in.
**Serves:** Journey J6 (managing the account). **Traces to:** REQ-PROD-017 (an account settings
surface), REQ-PROD-012 (a verified point of contact), REQ-PROD-018 (a stated handle-change position).

This is one sub-section of the Settings secondary navigation (REQ-UX-017): a person opens it directly by
its URL and returns from it to the Settings hub. It lets a signed-in person **see and update the point of
contact the account is recovered and notified through**, complete the step that confirms they control that
contact before the product relies on it, and read where the product stands on changing their handle. It
designs what the person sees and does; the credential, session, and verification *mechanism* is the
identity design's concern (`REQ-ID-*`), not this screen's.

### Composition

Built from the frozen component library, in the *settings* archetype's furnishing — a list of
**SettingRow**s inside the signed-in **NavShell** (per the library's archetype-coverage table). No new
screen or component is introduced. Components used: **NavShell** (signed-in), **SettingRow**, **TextField**,
**PrimaryButton**, **SecondaryButton**, **InlineFeedback**, **InlineError**, **EmptyState**,
**LoadingState**, **Toast**, and the `color.warning` token for the unverified-contact caution.

### Layout

Inside the persistent signed-in **NavShell**, the main region carries:

- A main heading **"Account & contact"**, which is also the browser document title, and a labelled **Back
  to settings** control returning to the Settings hub (wayfinding, REQ-UX-003 / REQ-UX-017). The NavShell
  keeps every primary destination reachable; it is not redesigned here.
- A short lead line naming what this screen is for ("The contact we use to help you recover your account
  and to reach you about it.").
- A list of **SettingRow**s, in this order:

  1. **Contact** — a SettingRow whose value slot shows the current point of contact (or its not-set
     treatment, below) together with a **verification-status** indicator:
     - *Verified* — a neutral/`color.success` mark reading "Verified", paired with the word, never colour
       alone.
     - *Unverified / not yet confirmed* — a `color.warning` caution reading "Not verified yet", paired with
       the word. This is a **caution, not an error**: the contact is present and usable to change, it has
       simply not been confirmed, so it is not shown with the `color.danger` error treatment.
     The row's control slot holds a **SecondaryButton "Change"**. Activating it reveals an inline
     **TextField** (labelled "Contact", holding the current value) with a **PrimaryButton "Save changes"**
     and a **SecondaryButton "Cancel"**. When the contact is unverified, the row also offers a
     **"Verify now"** action (a SecondaryButton) that starts the control-you-own verification step and then
     shows the contact as pending confirmation. What that step does under the hood — the code, link, token,
     or timeout — is the identity design's `REQ-ID-*`; this screen shows only the person-facing states: an
     action to start verification, a pending/"check your contact to confirm" indication, and the resolution
     to Verified or back to a caution with a plain reason.

  2. **Handle** — a SettingRow whose value slot shows the person's `@handle`, with a description that
     **states the product's position on changing it**. For a first release the product's stated position is
     that **the handle is fixed**: the description reads "Your handle is the name others follow you by. It
     can't be changed after sign-up." — and the row offers **no change control** (it carries no edit
     affordance; where a disabled control is shown, it carries this reason). If a later release decides a
     handle may change, this same row is where the working change control lives and the stated position
     updates to match. The screen's behaviour always matches the position it states (REQ-PROD-018).

### Primary action

**Save the updated contact** — the **PrimaryButton "Save changes"** in the Contact row's edit mode. Saving a
new or changed contact records it and moves it to the unverified/pending state, from which the person
completes verification. Viewing and updating the verified contact is this screen's reason to exist, so this
is its one primary action; the handle row is a stated-position read, not a competing action.

### Feedback conventions composed here

- A completed save is confirmed with brief, non-blocking feedback — a **Toast** ("Contact saved") or
  **InlineFeedback** on the Contact row — per the transient-feedback convention (REQ-UX-012). The row then
  reflects the new value and its unverified status.
- A started verification shows a pending indication in place ("We've sent a confirmation to your contact —
  confirm it to finish"), with a way to resend; the person-facing resolution, not the mechanism, is what
  this screen shows.
- Destructive or irreversible actions are not part of this screen (there is none here), so the
  destructive-confirmation convention (REQ-UX-011) is not invoked on it.

### States

The screen composes the components' own named states and the product-wide empty / loading / error patterns
and the expired-session keep-the-draft recovery owned by the shared *empty, error & loading states* work
(REQ-UX-008). It does not invent a per-screen pattern that conflicts with them.

**Loading** — First load of the screen, while the current contact and its verification status are being
fetched: a **LoadingState** skeleton standing in for the SettingRow list at its true dimensions (a skeleton
value block for the Contact row, one for the Handle row), rendered inside the **NavShell**, which itself
renders immediately (the NavShell records *loading* as "does not apply" — the frame never blanks). A small
in-place save or verify uses the control's own *loading* state — the **PrimaryButton** busy state and the
**SettingRow** pending treatment — not the whole-screen skeleton.

**Empty** — The meaningful empty case is **no contact on file yet** (the person has not provided one). The
Contact row does not render blank: it shows a `color.warning` caution reading "No contact set yet", a plain
line on why it matters ("Add a contact so you can recover your account and we can reach you about it" —
REQ-PROD-012), and a **PrimaryButton "Add contact"** opening the same inline **TextField** used for a
change. The whole-screen **EmptyState** block *does not apply* here, and the reason matches that component's
own definition: EmptyState is the treatment for a surface with nothing in it, and this settings sub-section
is not a list that can be empty — it always renders its Contact and Handle rows inside the NavShell. The
empty case lives inside the Contact row, not as a blank surface. (SettingRow likewise records row-level
*empty* as "does not apply"; the not-set treatment is row content plus a caution, consistent with that.)

**Error** — Three person-facing failures, each shown where its action was taken, never as a silent no-op
(REQ-UX-012):
- *The screen fails to load* its current contact/status → an **EmptyState error variant** ("We couldn't
  load your account settings — try again") with a **retry**, inside the NavShell. This is how a failed load
  is told apart from a contact that is simply not set yet, so the two are never confused.
- *A save fails* → a `color.danger` **TextField** border and an **InlineError** beneath the Contact field in
  plain words ("We couldn't save that — check the contact and try again"), with the person's typed value
  kept so they can retry. No system or error code is surfaced.
- *A verification action fails* → **InlineFeedback** in the danger role at the control that started it, with
  a plain reason and a way to try again; the contact reverts to its prior status rather than showing a
  result that did not happen.
- *The session expires mid-edit* → the person is routed to **Sign in** with the reason stated, their
  in-progress contact edit is preserved, and they are returned here afterward (REQ-UX-008). This screen
  composes that convention; it does not redesign it.

---

## Notification preferences — `/settings/notifications`

The settings sub-section where a signed-in person chooses which kinds of activity send them a
notification. It serves journey **J6 (managing the account)** and the account-settings surface
**REQ-PROD-017**, and it is the place **REQ-PROD-029** (activity notifications with preferences) puts
its "set which of these you are notified about" control.

This is the **Notification preferences** screen in the screen inventory (`/settings/notifications`,
**settings** archetype, signed-in). It is built only from named components in the component library; it
invents no screen or component.

### What the screen is for

A person who gets replies, follows, and likes wants to decide which of those are worth a notification.
This screen lets them turn each activity category on or off. A category left on sends a notification
when that activity happens; a category turned off stops notifying — the activity still occurs and still
appears in the person's own view of it, but it no longer produces a new notification.

The preferences here decide **which activity notifies**. The notifications themselves — the activity
list a person reads — are the **Notifications** surface (`/notifications`), designed in the safety &
notifications area. This screen links to and refers to that surface; it does not redesign it (see
*Cross-reference* below).

### Layout

Realised as the **settings** archetype: a list of **SettingRow**s inside the signed-in **NavShell**.

- **NavShell (signed-in), persistent.** The shell frames the screen and renders immediately, so moving
  into this sub-section never blanks the frame. Its **Settings** entry is marked as the active area, and
  its **Notifications** destination (with its unseen-activity indicator) remains reachable from here.
- **Settings as secondary navigation.** This screen is one sub-section of the settings hub, opened
  directly by its own URL and offering a clear way back to the **Settings hub**. It does not restate the
  settings-hub listing; it is a leaf a person reaches from the hub and returns to.
- **Heading.** The main heading and the document title both name the screen ("Notification
  preferences"), so a person always knows where they are.
- **Lead line.** One line under the heading states what the choices do — that these control which
  activity sends a notification — and links to the **Notifications** list where those notifications
  appear.
- **The choices.** A short list of three **SettingRow**s, one per activity category, each carrying a
  **Toggle** in its control slot.

### Content — the rows

Three rows, one per activity category chirp notifies on (replies, follows, likes). Each row is a
**SettingRow**: a `type.body` label, a `type.meta` / `color.text.secondary` description, and a control
slot holding a **Toggle** with its visible on/off label.

| Category | Row label | Description | Control | Default |
|----------|-----------|-------------|---------|---------|
| Replies | Replies | When someone replies to your chirps. | Toggle (on/off) | On |
| Follows | Follows | When someone follows you. | Toggle (on/off) | On |
| Likes | Likes | When someone likes your chirps. | Toggle (on/off) | On |

The three categories match the activity REQ-PROD-029 names (replies, follows, likes). Each defaults to
**on**: the baseline notifications story is to be notified of relevant activity, and the person turns
off what they do not want rather than opting in to each. The set of categories is fixed and known — it
does not grow or shrink at runtime.

### Primary action

The screen's primary action is **choosing whether an activity category sends a notification** — flipping
a category's **Toggle**. The choice takes effect immediately and is confirmed on its own row; there is
**no separate Save button**, because the **Toggle** persists its change on change (its documented
immediate-effect behaviour). Each row is independently operable, so a person can change one category
without touching the others.

### Immediate-save behaviour (success, in-flight, failure)

The screen composes the **Toggle**'s and **SettingRow**'s own named behaviours; it defines no new ones.

- **On change** — the **Toggle** flips immediately and persists the new value.
- **Success** — the change is confirmed in place with **InlineFeedback** in the success role on that
  row. The row now reflects the stored value. A category switched off stops notifications of that
  category from that point; switched on, they resume.
- **In-flight (loading)** — while the change is being written, the row's **Toggle** shows its brief
  pending treatment (the Toggle's *loading* state) and is not re-triggerable until the save resolves.
- **Failure** — the save fails → the **Toggle** reverts to its prior value and the row shows
  **InlineFeedback** in the danger role, in plain words, saying the setting is unchanged and inviting a
  retry. The control never shows a result that did not happen.

### Addressability and return

- Reachable directly at `/settings/notifications`, and listed as a sub-section in the Settings hub.
- Returns to the **Settings hub** (settings-as-secondary-nav); the browser back control behaves per the
  IA convention for a settings sub-section.

### Cross-reference (not redesigned): the Notifications activity surface

The **Notifications** list (`/notifications`, feed/list archetype) — the activity directed at the person
(replies, follows, likes) — is designed in the safety & notifications area and reached from the
signed-in shell's Notifications entry. This preferences screen only refers to it: a category turned
**off** here means that category stops producing new entries in that list; the list itself, its layout,
and its states are not designed here.

### States

**Loading — first load of the screen.** The saved preference values are being read. The **NavShell**
renders immediately; in the content area the three rows show **LoadingState** skeleton rows at the real
dimensions of a label-plus-Toggle row (skeletons, not a spinner on a blank panel), so the layout does not
jump when the real rows arrive.

**Error — the preferences fail to load.** If the saved preferences cannot be loaded, the content area
shows an **EmptyState** error variant — "We couldn't load your notification settings — try again" — with
a retry, in place of the rows. This is how a failed load is told apart from an empty surface. (A
failure of an individual *save* is not this screen-level error: it is handled on the row by the Toggle
revert plus danger **InlineFeedback**, described above.) An action taken on an expired or invalid session
follows the product-wide session-expiry recovery — routed to **Sign in** with the reason stated and
returned here afterward. That recovery pattern is owned by the considered-states area; this screen
composes it and does not redefine it.

**Empty — does not apply.** The three activity categories are a fixed, known set that always render, so
there is no condition in which this screen has "no items" to show. This matches the composed components'
own not-applicable decisions: the **Toggle** records *empty* as not applying ("a toggle is always on or
off"), and the **SettingRow** records *empty* as not applying at the row level (an empty sub-section would
show an **EmptyState** within the section — but this sub-section's categories are never absent). There is
therefore no empty state to design for this surface.

### Accessibility and responsive (composed, not owned)

How the **Toggle**'s on/off state is announced (by text, never colour or thumb-position alone), how the
rows are operated by keyboard and assistive technology, and how the screen reflows between a phone and a
wider viewport are owned by the accessibility and responsive areas. This screen composes their
treatments of **NavShell**, **SettingRow**, and **Toggle**; it does not restate or redefine them.

### Composition provenance (checkable)

- **Screen (inventory):** Notification preferences — `/settings/notifications`, settings archetype,
  signed-in.
- **Components (library), with the states used:** NavShell (signed-in, persistent); SettingRow
  (default, loading, error — empty not applicable); Toggle (default, loading, error; immediate-save with
  revert-on-failure); InlineFeedback (success and danger roles, on the row); EmptyState (error variant,
  for a failed screen load); LoadingState (skeleton rows, first load).
- **Conventions composed, not redefined:** settings-as-secondary-nav; the product-wide session-expiry
  recovery; the cross-reference to the Notifications activity surface.

---

## Sessions & devices — `/settings/sessions`

**Screen**: Sessions & devices — **Route**: `/settings/sessions` — **Archetype**: settings — **Auth**:
signed-in. **Journey**: J6 (managing the account). **Serves**: REQ-PROD-017 (the account settings
surface must let a person view and end active sessions), REQ-PROD-014 (sign-out that ends the session
server-side).

This is where a signed-in person sees every place their account is currently signed in, ends a session
on a device that is not the one in front of them, and signs out. It is a sub-section of **Settings**:
reached from the Settings hub, opened directly at its own URL, and offering a labelled way back to the
hub (the settings-as-secondary-nav convention, REQ-UX-017). It is built as a list of **SettingRow**s
inside the signed-in **NavShell** — the settings archetype — against the 600px reading measure
(`space.measure`).

### What the person can see and do

- **See their active sessions.** Each session the account currently holds is listed, with enough to
  recognise it: the device and browser (for example "Chrome on macOS"), an approximate location, and
  when it was last active. The session the person is using right now is marked as the current one.
- **End a session on another device.** Any session other than the current one can be ended. This is a
  destructive action, so it is confirmed through the **Dialog** confirmation variant that names the
  effect before it proceeds (the destructive-confirmation convention, REQ-UX-011). Once ended, that
  session can no longer be used on its device.
- **Sign out.** The person can sign out of the current session. Sign-out ends the session server-side
  and leads into the product's sign-out transition — back to the signed-out Landing, with no protected
  screen reachable afterwards (the sign-out transition, REQ-UX-016).

It designs what the person sees and does. How a session or token is represented, validated, or
invalidated is the identity design's concern (`REQ-ID-*`), not this screen's.

### Layout and content

Top to bottom, inside the signed-in NavShell with the screen's main heading "Sessions & devices"
(`type.title`) and a labelled back control to the Settings hub:

1. **Intro line** — one `type.body` line in `color.text.secondary` explaining the screen in plain words:
   "These are the places you're signed in to chirp. End any you don't recognise, or sign out below."
2. **This device** — a single **SettingRow** for the current session, marked "This device · current
   session" with a label and a marker (a mark and words, never colour alone). Its content: the device
   and browser, the approximate location, and "signed in <relative time>" / "active now". This row has
   **no End session control** — the way to end the current session is Sign out, below — so the row's
   control slot carries only the current-session marker, keeping the one destructive per-row action
   ("End session") reserved for other devices.
3. **Other sessions** — a **ListView** of **SettingRow**s, one per other active session. Each row's
   label is the device and browser; its description (`type.meta`, `color.text.secondary`) carries the
   approximate location, the relative "last active" time, and a short session identifier set in
   `type.family.mono` so a person can tell two similar sessions apart by reading it exactly. Each row's
   control slot holds an **End session** **SecondaryButton** (or an **IconButton** carrying the "End
   session" label where the row is tight). The ListView owns the list-level empty, loading, and error
   treatments (below) and loads in bounded pages if the list is long (the pagination convention,
   REQ-UX-010).
4. **Sign out** — the screen's primary action (below), presented as a prominent entry beneath the list.

### Primary action

The screen's primary action is **Sign out**. It is the decisive action a person comes here to take on
their own session, and it is the action the release bar gates (REQ-PROD-014). Ending another device's
session is the row-level destructive action within the Other sessions list; it is confirmed the same
way but is not the screen's single primary action.

### Ending a session on another device (the confirmed, destructive flow)

1. The person activates **End session** on another session's row.
2. A **Dialog** confirmation variant opens over the `color.bg.scrim`. Title: "End this session?" Body
   names the effect plainly: "The session on <device>, <approximate location>, will be signed out.
   Whoever is using chirp there will have to sign in again." The action pair is a destructive confirm —
   a `color.danger` **PrimaryButton** labelled "End session" — and a **SecondaryButton** "Cancel", the
   calm way out. Cancel closes the dialog and changes nothing.
3. On confirm, the dialog shows its loading state (the confirm button is busy and the dialog stays open
   until the action resolves). The end is server-side, so the ended session can no longer be used on its
   device.
4. On success, the dialog closes, the row leaves the list, and the result is shown — **InlineFeedback**
   in the success role at the list, or a **Toast** confirming "Session ended" (the result-of-every-action
   convention, REQ-UX-012). On failure, an **InlineError** appears inside the dialog in plain words and
   the dialog stays open so the person can retry; nothing is ended until it succeeds.

### Signing out (into the sign-out transition)

1. The person activates **Sign out**.
2. A **Dialog** confirmation variant opens. Title: "Sign out?" Body: "You'll be signed out on this
   device and returned to the chirp landing." When the account is signed in elsewhere, the dialog also
   offers "Also sign out of my other N sessions" (a **Toggle** within the dialog) — this is the
   inventory's Sign out dialog "confirm when ending sessions on other devices too", composed here, not a
   new pattern. The confirm is a **PrimaryButton** "Sign out" (destructive styling when "also end
   others" is on); Cancel is a **SecondaryButton**.
3. On confirm, the current session ends server-side and the screen leads into the product's existing
   sign-out transition: the person lands on the signed-out Landing, and the browser back control does
   not re-expose this settings screen (REQ-UX-016). This screen designs the sign-out entry *into* that
   transition; it does not redesign the transition.
4. The server-side end means the session that was in use is rejected afterward, and the next person at
   that device is not signed in as this account (REQ-PROD-014). A failed sign-out shows an
   **InlineError** in the dialog with a retry; the person is not left in a half-signed-out state.

### Empty, error, and loading states

| State | Treatment |
|---|---|
| **Loading** | First load of the sessions list shows the **ListView** / **LoadingState** skeleton rows at the rows' real dimensions, not a spinner on a blank screen, so the layout does not jump when the sessions arrive; the skeleton honours `motion.reduced`. The **NavShell** and the screen heading render immediately (the shell has no loading state), and the **This device** row renders as soon as the current session is known, while the other sessions resolve. |
| **Empty** (the "only this session" case) | When the account is signed in only on the current device, the Other sessions list has no items, so the **ListView** shows its **EmptyState**: a calm, explanatory block — "You're only signed in here. When you sign in on another device, it'll show up in this list." — never a blank area and never an apology. The **This device** row and **Sign out** remain present and usable. |
| **Error** | If the sessions list fails to load, the **ListView** shows its error treatment — an **EmptyState** error variant (or **InlineError**) with a retry: "We couldn't load your sessions — try again." The **This device** row still renders if the current session is known, so the person can still sign out. A failed End session or Sign out is shown as an **InlineError** inside the open **Dialog** (its error state), with the action retryable and nothing changed until it succeeds. An action attempted on an expired or invalid session follows the product-wide session-expiry convention (REQ-UX-008): the person is routed to **Sign in** with the reason stated and returned afterwards — that pattern is composed here, owned by the product-wide considered-states work, not redefined on this screen. |

Each state above is one of the composed components' own named states; this screen invents no per-screen
state treatment of its own, and stays consistent with the product-wide empty / loading / error patterns.

### Out of scope for this screen

The session, token, and verification **mechanism** (identity design, `REQ-ID-*`); the sign-out
**transition** itself (composed here, owned by the IA/interaction model and the screens-and-flows
sign-out design); and the other settings sub-sections the Settings hub links to. Those are referenced
by name and designed elsewhere.

---

## Requirements register — `REQ-UX-069..074`

The consolidated register for the account-settings surfaces. Each entry carries a statement, a
stranger-checkable acceptance criterion exercisable on the live product, a `release_gating` flag (a
`false` carries its one-line reason), and the `REQ-PROD-*` it traces to.

### REQ-UX-069 — The settings hub lists every account sub-section, each addressable and returning to the hub

- **statement**: Signed in, a Settings hub at `/settings` presents a labelled list of every account
  settings sub-section — edit profile, account & contact, notification preferences, sessions & devices,
  blocked & muted, export your data, and delete account — each a row the person can open from the hub and
  by the sub-section's own URL, with a labelled way back to the hub from each. The delete-account row is
  shown as destructive and opens a confirmation rather than deleting on selection. Where notifications are
  not in the release, the notification-preferences row is absent; every other row is present.
- **acceptance_criteria**: Signed in, open `/settings`. The sub-sections above are listed as openable
  rows. Open each by selecting its row, and again by entering its URL directly in a fresh tab; each lands
  on that sub-section, not on a generic home. From each sub-section, use the on-screen way back and the
  browser back control; both return to the hub. Confirm the delete-account row is visibly destructive and,
  when selected, presents a confirmation that can be cancelled — selecting the row does not delete the
  account. If the account summary fails to load, confirm every sub-section row is still reachable.
- **release_gating**: true
- **references**: REQ-PROD-017

### REQ-UX-070 — View, update, and confirm control of the verified contact

- **statement**: From the Account & contact screen (`/settings/account`), a signed-in person can see their
  current point of contact with its verification status, change it, and — because the product relies only on
  a contact it has confirmed the person controls — complete a control-you-own verification step for a new or
  unverified contact. An unverified contact is shown as a caution, not an error.
- **acceptance_criteria**: Signed in, open `/settings/account`; the current contact and a verification
  status of either "Verified" or "Not verified yet" are shown. Change the contact and save; the product
  confirms the save and shows the new contact as not-yet-verified, and offers a way to complete a step that
  confirms you control it before it is used for recovery. Confirm that an unverified contact is presented as
  a caution (a non-error treatment), and that a save failure is shown against the contact field with your
  typed value preserved to retry. A person who has not completed verification cannot have that contact
  treated as verified.
- **release_gating**: true
- **references**: REQ-PROD-012, REQ-PROD-017

### REQ-UX-071 — The handle-change position is stated on the account screen and the screen matches it

- **statement**: The Account & contact screen states the product's position on whether and how the account
  handle can change after sign-up, shown with the handle, and the screen behaves consistently with that
  stated position.
- **acceptance_criteria**: On `/settings/account`, find the product's stated position on handle changes
  presented with your `@handle`. Confirm the screen's behaviour matches the stated position: either a change
  control is offered and works, or the handle is stated as fixed and the screen offers no path that changes
  it. If stated as fixed, confirm no control on the screen changes the handle.
- **release_gating**: false — rides REQ-PROD-018, a decision-and-consistency requirement; a first release
  may state the handle as fixed provided that position is stated on the screen.
- **references**: REQ-PROD-018, REQ-PROD-017

### REQ-UX-072 — Per-category notification preferences, saved immediately

- **statement**: On the Notification preferences screen (`/settings/notifications`) a signed-in person
  can choose, for each activity category — replies, follows, and likes — whether that category sends a
  notification. A change takes effect immediately and is confirmed on its row with no separate save;
  turning a category off stops notifications of that category and turning it on resumes them. If a
  change cannot be saved, the control returns to its previous state and says so.
- **acceptance_criteria**: Signed in, open `/settings/notifications` directly by its URL. The screen
  lists Replies, Follows, and Likes, each with an on/off control that shows its current state, and
  offers a way back to the settings hub. Turn Likes off; the row confirms the change in place, with no
  separate Save step. Have another account both like and reply to one of your chirps; a reply
  notification appears in the Notifications list and no like notification does. Turn Likes back on; a
  later like produces a notification again. With saving forced to fail, flip a toggle: it returns to its
  previous position and shows a plain message that the setting is unchanged.
- **release_gating**: false — notification preferences ride REQ-PROD-029, which the release bar does not
  gate; a first release may ship without notifications, and these preferences ship when notifications
  ship.
- **references**: REQ-PROD-029 (activity notifications with preferences), REQ-PROD-017 (an account
  settings surface); journey J6.

### REQ-UX-073 — See active sessions and end another device's session

- **statement**: A signed-in person can open Sessions & devices and see each place the account is
  currently signed in — each with enough to recognise it (device and browser, approximate location,
  last-active time) and the current session clearly marked — and can end any other session through a
  confirmation that names the effect, after which that session can no longer be used on its device.
- **acceptance_criteria**: Signed in on two devices, open `/settings/sessions`; both sessions are
  listed, the one you are using is marked as the current device, and each other session shows its
  device, an approximate location, and a last-active time. Choose End session on the other device; a
  confirmation states what will happen and offers a cancel. Confirm it: the session leaves the list, the
  result is shown, and on the other device the next action on that session is rejected and requires a
  fresh sign-in.
- **release_gating**: true
- **references**: REQ-PROD-017, REQ-PROD-014

### REQ-UX-074 — Sign out ends the session server-side and does not leak back

- **statement**: A signed-in person can sign out from Sessions & devices; sign-out ends the current
  session server-side so it can no longer be used, returns the person to the signed-out landing, and
  leaves no protected screen reachable with the browser back control. Where the account is signed in
  elsewhere, the sign-out confirmation offers to end those other sessions too.
- **acceptance_criteria**: Signed in, open `/settings/sessions` and choose Sign out; a confirmation
  states you will be signed out and, when other sessions exist, offers to end them too. Confirm it: you
  land on the signed-out landing; pressing browser back does not re-expose the settings screen; and
  replaying the request from the session that was in use is rejected, so the next person at that device
  is not signed in as you.
- **release_gating**: true
- **references**: REQ-PROD-014
