## Account & contact

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

## Requirements

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
