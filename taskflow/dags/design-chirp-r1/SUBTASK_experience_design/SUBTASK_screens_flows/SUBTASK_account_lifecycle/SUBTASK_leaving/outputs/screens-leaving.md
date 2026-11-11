### Leaving — export and deletion

These are the two surfaces that let a person take their data and leave chirp cleanly. A product that
people trust with their account is one they can also walk away from: they can obtain a copy of what they
wrote and who they follow, and they can delete the account and have their content removed, with the
consequence stated before anything happens. Neither surface exists in the product today, and their absence
is the gap — a person who cannot get their data out, or cannot close the account they opened, has reason to
doubt the product with their data in the first place.

Both screens live in the signed-in **NavShell** under **Settings**, reached from the **Settings** hub, and
both hold to the reading measure (`space.measure`) the rest of the product uses. Each is described below as
an arrangement of named components from the component library, in their named states; nothing here invents a
screen outside the **Screen inventory** or a component or token outside the visual system. What the product
does with the data — how an export file is assembled, what the removal of content touches — is a build and
privacy-design concern; these screens specify what the person sees, is told, and must confirm.

---

#### Export your data (`/settings/export`)

**Inventory screen**: Export your data · **Route**: `/settings/export` · **Archetype**: settings ·
**Auth**: signed-in · **Journey**: J8 · **Serves**: REQ-PROD-019

**What it is for.** A person obtains their own data — their chirps, their profile, and who they follow — in
a form they can open outside chirp. The screen takes them through three moments: ask for the export, wait
while it is prepared, and obtain the result.

**Layout.** A settings screen rendered in the signed-in **NavShell**, with a labelled way back to the
Settings hub (per the IA wayfinding convention). Top to bottom, within the 600px measure:

- The screen heading in `type.title` — "Export your data" — and a `type.body` `color.text.secondary`
  explanation that says what the export contains (your chirps, your profile, and the accounts you follow)
  and that it arrives as a file you can open and keep outside chirp.
- A short **content summary** built from **SettingRow**s (label + `type.meta` description, no control), one
  row per data kind — *Your chirps*, *Your profile*, *Who you follow* — so the person can see what they are
  about to receive before they ask for it.
- A one-line note, in `type.meta` `color.text.secondary`, that preparing the file can take a little while
  and that they can leave the page and come back.

**Primary action.** A single **PrimaryButton** — "Prepare my data" — is the one primary action on the view.
Requesting the export is the whole job of the screen; obtaining the result is the **SecondaryButton**
("Download your data") that appears once the file is ready.

**States.**

- **Default / empty (no export yet).** On a first visit, no export has been prepared. The content area is
  the **EmptyState** treatment composed into the section: the explanation above, with "Prepare my data" as
  the offered next step — it explains what an export is and how to get one rather than showing a blank
  panel. This resting "nothing yet" view and the screen's default are the same state, which is correct for a
  surface whose job is to start a request.
- **Loading.** Two distinct loads. (1) The screen's own first paint uses **LoadingState** skeleton rows at
  the real dimensions of the summary rows, so the frame does not jump when content arrives. (2) After the
  person asks, the **preparing** state: the **PrimaryButton** shows its busy state and the section shows a
  bounded **LoadingState** spinner with a `type.body` status line ("Preparing your data…"), repeating that
  they can leave and come back. When the file is ready, the preparing state resolves to the default view
  with the **SecondaryButton** "Download your data" present and a **Toast** ("Your data is ready to
  download") confirming without stealing focus. Nothing spins indefinitely — a preparation that fails hands
  off to the error state.
- **Error.** A failed preparation shows an **InlineError** in the section, in plain words with a retry
  ("We couldn't prepare your export — try again"), and the **PrimaryButton** returns to its resting label so
  the person can ask again; no partial or broken file is offered. If the screen itself fails to load, the
  content area shows the **EmptyState** error variant ("We couldn't load this — try again") with a retry,
  which is how a load failure stays distinct from the genuinely-nothing-yet empty state.

---

#### Delete account (`/settings/delete`)

**Inventory screen**: Delete account · **Route**: `/settings/delete` · **Archetype**: confirmation ·
**Auth**: signed-in · **Journey**: J8 · **Serves**: REQ-PROD-020, REQ-PROD-021, REQ-PROD-022

**What it is for.** A person deletes their account and has their content removed, after a confirmation that
names the consequence, states what is and is not retained, points them to export first, and proceeds only
once they have explicitly confirmed. Cancelling leaves everything exactly as it was.

**Layout.** This surface realises the confirmation archetype as the **Dialog** confirmation variant, opened
over the Settings context and dimmed behind the `color.bg.scrim` (per the IA destructive-confirmation
convention). It is reached either from the destructive **SettingRow** on the Settings hub (a `color.danger`
"Delete account" row that opens this confirmation) or directly at `/settings/delete`, which opens the
confirmation over the settings surface. Within the panel, top to bottom:

- A `type.heading` title that names the action as a question — "Delete your account?"
- A `type.body` **consequence** statement in plain words: your account and your chirps will be removed, you
  will not be able to sign in again, and this cannot be undone.
- A **what is and is not retained** block that renders the product's defined deletion outcome
  (REQ-PROD-021 — the specific policy is set by the privacy and identity designs, not invented here). The
  block has a fixed shape so the person always sees the same three points, filled from that stated outcome:
  *What is removed* (your account, profile, and chirps), *What may remain* (what becomes of chirps that
  others have replied to or liked, stated as the product's outcome defines it), and *Your handle* (whether
  the handle becomes available for someone else to register again). Where the product has not yet stated one
  of these, the screen states that plainly rather than implying a guarantee it cannot make.
- A **pointer to export first**, as a `type.body` line and a **SecondaryButton** / link — "Export your data
  first" → `/settings/export` — presented as the person's chance to keep a copy before the account goes.
- An **explicit-confirmation** step: a **TextField** asking the person to type their handle to confirm (or
  an "I understand this can't be undone" acknowledgement). The destructive action stays disabled until this
  is given, so deletion is never one stray click.

**Primary action.** The destructive **PrimaryButton** (danger variant, `color.danger`) — "Delete my
account". Its calm counterpart is the **SecondaryButton** "Cancel", which closes the confirmation and
returns the person to Settings with nothing changed. On a confirmed deletion the session ends and the person
is returned to the signed-out **Landing** (the IA sign-out-to-signed-out-shell convention), with a brief
confirmation that the account was deleted; protected screens are no longer reachable.

**States.**

- **Default.** The panel open over the dimmed Settings surface, showing the consequence, the retained /
  not-retained block, the export pointer, the confirmation field, and the Delete / Cancel pair.
- **Disabled.** The destructive **PrimaryButton** is disabled until the explicit-confirmation step is
  satisfied (the handle typed, or the acknowledgement given) — the Dialog's disabled-confirm state. Cancel
  is always available.
- **Loading.** On confirm, the destructive **PrimaryButton** shows its busy state and the dialog stays open
  until the deletion resolves, so the action is not re-triggerable and the person is not left guessing.
  Reaching `/settings/delete` opens the confirmation immediately over the settings context, so there is no
  separate screen skeleton.
- **Error.** A failed deletion shows an **InlineError** inside the panel, in plain words with a way to
  retry; the dialog stays open, the account is not deleted, and Cancel still leaves everything intact. The
  person is never told the account was removed when it was not.
- **Empty.** Does not apply — a confirmation always opens with its content; there is no empty variant of
  this surface.

---

### Requirements and acceptance criteria — REQ-UX-075..077

Each requirement below is testable by someone who never met its author, exercisable on the live product;
each carries a `release_gating` flag and references the product requirement(s) it serves. These cover the
leaving surfaces (`REQ-UX-075..077`); the rest of the account-lifecycle register is held by the sibling
areas.

#### REQ-UX-075 — A person can request and obtain their own data in a portable form
- **statement**: From a dedicated export screen, a signed-in person can request their data and obtain their
  chirps, profile, and follow list in a form they can open outside chirp, with the request, the preparing
  state, and the obtainable result each shown.
- **acceptance_criteria**: Signed in, open the export screen; it names what the export contains and offers a
  single request action. Request the export; the screen shows a preparing state (not a frozen or blank
  screen) and, when ready, offers a way to download the file. Open the downloaded file outside chirp; it
  contains your chirps, your profile, and who you follow. Force a preparation failure; the screen says so in
  plain words and lets you retry, and offers no broken file.
- **release_gating**: true
- **references**: REQ-PROD-019

#### REQ-UX-076 — Deletion is confirmed with its consequence, its retained/not-retained outcome, and a pointer to export
- **statement**: The delete-account confirmation names the consequence plainly, states what is and is not
  retained per the product's defined deletion outcome (including what becomes of replied-to or liked chirps
  and whether the handle frees up), and points the person to export their data first — all before any
  deletion occurs.
- **acceptance_criteria**: Signed in, open the delete-account confirmation. It states that the account and
  chirps are removed and that this cannot be undone; it shows what is removed, what may remain, and what
  happens to the handle, matching the product's stated deletion outcome; and it offers a way to export your
  data first. None of this requires having deleted anything to see it.
- **release_gating**: true
- **references**: REQ-PROD-021, REQ-PROD-022

#### REQ-UX-077 — Deletion proceeds only on explicit confirmation, and cancelling leaves everything intact
- **statement**: Account deletion proceeds only after the person explicitly confirms (the destructive action
  stays disabled until confirmation is given); on deletion the person is signed out to the signed-out shell,
  and cancelling at any point leaves the account and its content unchanged.
- **acceptance_criteria**: Open the delete-account confirmation; the delete action is unavailable until you
  give the explicit confirmation it asks for. Cancel; you return to settings and the account still signs in
  with its content intact. Give the confirmation and delete; afterward the account can no longer sign in and
  you are returned to the signed-out landing, and the browser back control does not re-expose the deleted
  account's screens.
- **release_gating**: true
- **references**: REQ-PROD-020, REQ-PROD-022
