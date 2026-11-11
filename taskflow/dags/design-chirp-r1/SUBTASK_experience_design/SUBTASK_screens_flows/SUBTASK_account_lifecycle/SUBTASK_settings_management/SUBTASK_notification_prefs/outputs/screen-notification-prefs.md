# Notification preferences — `/settings/notifications`

The settings sub-section where a signed-in person chooses which kinds of activity send them a
notification. It serves journey **J6 (managing the account)** and the account-settings surface
**REQ-PROD-017**, and it is the place **REQ-PROD-029** (activity notifications with preferences) puts
its "set which of these you are notified about" control.

This is the **Notification preferences** screen in the screen inventory (`/settings/notifications`,
**settings** archetype, signed-in). It is built only from named components in the component library; it
invents no screen or component.

## What the screen is for

A person who gets replies, follows, and likes wants to decide which of those are worth a notification.
This screen lets them turn each activity category on or off. A category left on sends a notification
when that activity happens; a category turned off stops notifying — the activity still occurs and still
appears in the person's own view of it, but it no longer produces a new notification.

The preferences here decide **which activity notifies**. The notifications themselves — the activity
list a person reads — are the **Notifications** surface (`/notifications`), designed in the safety &
notifications area. This screen links to and refers to that surface; it does not redesign it (see
*Cross-reference* below).

## Layout

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

## Content — the rows

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

## Primary action

The screen's primary action is **choosing whether an activity category sends a notification** — flipping
a category's **Toggle**. The choice takes effect immediately and is confirmed on its own row; there is
**no separate Save button**, because the **Toggle** persists its change on change (its documented
immediate-effect behaviour). Each row is independently operable, so a person can change one category
without touching the others.

## Immediate-save behaviour (success, in-flight, failure)

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

## Addressability and return

- Reachable directly at `/settings/notifications`, and listed as a sub-section in the Settings hub.
- Returns to the **Settings hub** (settings-as-secondary-nav); the browser back control behaves per the
  IA convention for a settings sub-section.

## Cross-reference (not redesigned): the Notifications activity surface

The **Notifications** list (`/notifications`, feed/list archetype) — the activity directed at the person
(replies, follows, likes) — is designed in the safety & notifications area and reached from the
signed-in shell's Notifications entry. This preferences screen only refers to it: a category turned
**off** here means that category stops producing new entries in that list; the list itself, its layout,
and its states are not designed here.

## States

### Loading — first load of the screen

The saved preference values are being read. The **NavShell** renders immediately; in the content area
the three rows show **LoadingState** skeleton rows at the real dimensions of a label-plus-Toggle row
(skeletons, not a spinner on a blank panel), so the layout does not jump when the real rows arrive.

### Error — the preferences fail to load

If the saved preferences cannot be loaded, the content area shows an **EmptyState** error variant —
"We couldn't load your notification settings — try again" — with a retry, in place of the rows. This is
how a failed load is told apart from a genuinely empty surface. (A failure of an individual *save* is
not this screen-level error: it is handled on the row by the Toggle revert plus danger
**InlineFeedback**, described above.) An action taken on an expired or invalid session follows the
product-wide session-expiry recovery — routed to **Sign in** with the reason stated and returned here
afterward. That recovery pattern is owned by the considered-states area; this screen composes it and
does not redefine it.

### Empty — does not apply

The three activity categories are a fixed, known set that always render, so there is no condition in
which this screen has "no items" to show. This matches the composed components' own not-applicable
decisions: the **Toggle** records *empty* as not applying ("a toggle is always on or off"), and the
**SettingRow** records *empty* as not applying at the row level (an empty sub-section would show an
**EmptyState** within the section — but this sub-section's categories are never absent). There is
therefore no empty state to design for this surface.

## Accessibility and responsive (composed, not owned)

How the **Toggle**'s on/off state is announced (by text, never colour or thumb-position alone), how the
rows are operated by keyboard and assistive technology, and how the screen reflows between a phone and a
wider viewport are owned by the accessibility and responsive areas. This screen composes their
treatments of **NavShell**, **SettingRow**, and **Toggle**; it does not restate or redefine them.

## Requirement

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

## Composition provenance (checkable)

- **Screen (inventory):** Notification preferences — `/settings/notifications`, settings archetype,
  signed-in.
- **Components (library), with the states used:** NavShell (signed-in, persistent); SettingRow
  (default, loading, error — empty not applicable); Toggle (default, loading, error; immediate-save with
  revert-on-failure); InlineFeedback (success and danger roles, on the row); EmptyState (error variant,
  for a failed screen load); LoadingState (skeleton rows, first load).
- **Conventions composed, not redefined:** settings-as-secondary-nav; the product-wide session-expiry
  recovery; the cross-reference to the Notifications activity surface.
- **Methodology:** Experience Design (primary); Product Strategy (support).
