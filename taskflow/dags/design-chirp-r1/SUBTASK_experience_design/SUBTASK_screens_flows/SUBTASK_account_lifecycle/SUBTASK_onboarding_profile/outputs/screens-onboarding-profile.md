### Account lifecycle — onboarding and self-presentation

These are the two surfaces a brand-new account meets first: **Onboarding**, the screen a person
lands on the moment their account exists, and **Edit profile**, where they shape how they appear
once they are in. Both are signed-in screens that render inside the signed-in **NavShell**. Each is
described below at wireframe level — its place in the screen inventory, its layout, its content, its
primary action, and its empty, error, and loading states — built only from the named components in
the component library and referring to screens by their inventory names. Where a state is the product
treatment owned elsewhere (session expiry, the product-wide empty/loading/error patterns), it is
referred to, not redesigned.

---

#### Onboarding (`/welcome`)

**Inventory screen**: Onboarding · **Route**: `/welcome` · **Archetype**: empty/landing ·
**Auth**: signed-in · **Realised by**: **EmptyState** inside the signed-in **NavShell**.
**Serves**: J5 (first run) · **REQ-PROD-032**. **Composes with**: the sign-up → onboarding landing
(an IA convention; a completed sign-up establishes the session and lands here, so this screen does
not repeat or redesign sign-up).

Onboarding exists to answer the one question a new account has on its first second — "I'm in, now
what?" — when the home timeline is empty because the person follows no one and has posted nothing.
It replaces the blank timeline with an explanation and a way forward.

**Layout.** The signed-in **NavShell** frames the screen as it does every signed-in surface, so Home,
Explore, Notifications, Profile, Compose, and the account menu are already reachable while the person
is here. Within the 600px reading measure (`space.measure`), a single centred **EmptyState** block:
a calm flat illustration in the brand hues at the top, a headline in `type.title`, a short
explanation in `type.body` / `color.text.secondary` beneath it, and a stacked pair of actions below,
separated by the generous `space.10`/`space.12` vertical rhythm the empty/landing archetype uses. The
screen is explanation and next step — nothing to scroll, nothing to dismiss.

**Content.**
- **Headline** (`type.title`): names where the person is and why it is empty — for example
  *"You're in. Your timeline's empty for now."*
- **Explanation** (`type.body`): one or two plain sentences saying the timeline fills with chirps
  from the people they follow and their own posts, so the two ways to fill it are to follow someone
  or to post.
- **Primary action — "Write your first chirp"** (**PrimaryButton**): opens **Compose**. This is the
  route that is always available: a person can post a first chirp without anyone else existing, so
  onboarding can always offer at least one way to a non-empty timeline even where discovery is not
  present.
- **Secondary action — "Find people to follow"** (**SecondaryButton**): opens **Explore / find
  people** (`/explore`). Explore rides a non-gating product requirement, so this route is offered when
  discovery is present and is the richer path to a non-empty timeline; the "Write your first chirp"
  route above is the guaranteed one that does not depend on it.
- A quiet **"Skip for now"** text control (a **SecondaryButton** in its lowest-weight form) leaves
  onboarding for the home timeline, so the screen never traps a person who would rather look around —
  the empty timeline they then see is the **ListView** *empty* state, which itself points back to
  Explore and compose.

**Primary action**: Write your first chirp → **Compose**.

**States.**
- **Default / empty.** Onboarding is an empty/landing screen, so its resting state *is* the
  explanatory **EmptyState**: illustration, headline, explanation, and the two routes. There is no
  separate "empty" variant to design — the screen is the designed answer to an empty timeline. It is
  never a blank page.
- **Loading.** The static explanation and the two action controls render immediately with the
  **NavShell**, so the screen never blanks while anything resolves. If onboarding shows an optional
  preview of suggested people to follow (where discovery is present), that region alone shows
  **LoadingState** skeleton rows at the size of the coming rows while the rest of the screen is
  already usable; the person can act on either route before the preview settles.
- **Error.** The screen's core — explanation and the two routes — has nothing to fail, so it stays
  up. If an optional suggestions preview fails to load, that region shows the **EmptyState** *error*
  variant ("We couldn't load suggestions — you can still find people or write your first chirp") with
  a retry, and both routes remain present, so a failed preview never costs the person their way
  forward. An expired or invalid session taking them here is handled by the product-wide
  expired-session treatment (routed to sign-in with the reason stated and returned afterward) — that
  pattern is referred to, not redesigned here.

---

#### Edit profile (`/settings/profile`)

**Inventory screen**: Edit profile · **Route**: `/settings/profile` · **Archetype**: form ·
**Auth**: signed-in · **Realised by**: **TextField** + **PrimaryButton** + **SecondaryButton** +
**InlineError** in a form layout, inside the signed-in **NavShell**. **Serves**: J6 (managing the
account) · **REQ-PROD-016**. **Reached from**: the **Settings** hub as a listed sub-section, and from
the "Edit profile" action on the person's **Own profile** (the **ProfileHeader** **SecondaryButton**)
— both entries are designed elsewhere and are referred to here, not redefined.

Edit profile is where a person changes how they appear after sign-up: their display name and their
bio. A change saved here shows on their profile the next time it is viewed.

**Layout.** Inside the signed-in **NavShell**, within the 600px measure, a short form:
- a heading in `type.title` naming the screen ("Edit profile"), which also sets the document title,
  so a person always knows where they are;
- a labelled way back to the **Settings** hub, consistent with how every settings sub-section returns
  to the hub;
- a **TextField** for the **display name** — single-line, labelled, required;
- a multi-line **TextField** for the **bio** — labelled, optional, showing its length allowance where
  one applies (the exact limit is a domain decision, surfaced on the field, not invented here);
- the handle is shown as a read-only value with a one-line note that it is managed under **Account &
  contact** (where the product states its position on whether a handle can change) — this screen does
  not edit the handle;
- an action row pinned below the fields: **"Save changes"** (**PrimaryButton**) and **"Cancel"**
  (**SecondaryButton**).

**Content.** The current display name and bio are pre-filled so the person edits rather than retypes.
Labels and the Save verb follow the voice rules — sentence case, a verb for the action ("Save
changes", not "Submit"). Field hints say what a field is for in plain words.

**Primary action**: Save changes → persists the display name and bio and confirms the save; the new
values show on the person's profile on the next view.

**States.**
- **Default.** The form pre-filled with the current display name and bio. **Save changes** is
  disabled (its **PrimaryButton** *disabled* state) until the person makes a change, so the control
  never offers to save nothing; **Cancel** returns to the hub (or to the profile, when the person
  arrived from the "Edit profile" action) without writing anything.
- **Empty.** The optional **bio** left empty is valid — the field shows its label and hint, not an
  error (the **TextField** *empty* state). The required **display name** emptied is not flagged while
  the person is still working; only on a save attempt with an empty display name does it enter the
  error state below.
- **Error.** Two cases, each shown where the problem is, in plain words, with no system code and no
  blame, and without discarding what the person typed:
  - *Field-level* — an empty required display name, or a value the product rejects (for example too
    long), shows the **TextField** *error* state: a `color.danger` border and an **InlineError**
    beneath naming the problem and the fix ("Add a display name so people can recognise you").
  - *Save-level* — a save that fails on a transient or server condition shows an **InlineError** at
    the form with a plain reason and keeps every edited value so the person can retry; this is
    consistent with the product-wide keep-the-draft recovery for a transient error, which is referred
    to, not redesigned.
- **Loading.** On open, if the current values are still being fetched, the field region shows
  **LoadingState** skeletons at the fields' size while the form chrome and the **NavShell** render
  immediately. On save, **Save changes** shows its **PrimaryButton** *loading* (busy) state and the
  fields lock briefly so a change is not double-submitted; on success the save is confirmed with a
  **Toast** ("Saved") — or **InlineFeedback** at the action row — and the updated values are what the
  profile then shows.

---

### Requirements — REQ-UX-065..068

Each requirement is testable by someone who never met the author, exercisable on the live product.
Each carries a `release_gating` flag and references the product requirement(s) it serves.

#### REQ-UX-065 — Onboarding explains the empty timeline and offers a way off it
- **statement**: A brand-new account landing on Onboarding (`/welcome`) sees an explanation of why
  the timeline is empty and at least one actionable route to a non-empty timeline — composing a first
  chirp, and, where discovery is present, finding people to follow — rather than a blank page. The
  compose route is always offered, so the screen meets this bar even where discovery is not yet
  present.
- **acceptance_criteria**: Complete a fresh sign-up; you land on `/welcome` and see text explaining
  the empty timeline and a control that opens Compose to write a first chirp. Where Explore is
  present, a second control opens it to find people to follow. At no point is the screen a blank page.
- **release_gating**: true
- **references**: REQ-PROD-032

#### REQ-UX-066 — Onboarding never blanks or dead-ends across its states
- **statement**: Onboarding's explanation and its routes render immediately and stay available across
  its loading and error states: a loading suggestions preview shows skeletons rather than blanking the
  screen, and a failed or empty suggestions preview still leaves at least the compose route in place,
  so the person always has a way forward.
- **acceptance_criteria**: Open `/welcome` and, while any suggestions preview is still loading,
  confirm the explanation and the "Write your first chirp" route are already usable and no region is
  blank. Force the suggestions preview to fail; it shows an error with retry and the compose route is
  still present and works.
- **release_gating**: true
- **references**: REQ-PROD-032, REQ-PROD-033

#### REQ-UX-067 — Edit profile changes display name and bio and persists them
- **statement**: A signed-in person can open Edit profile (`/settings/profile`) from the Settings hub
  or from the "Edit profile" action on their own profile, change their display name and bio, and save;
  the saved values show on their profile on the next view.
- **acceptance_criteria**: Signed in, open Edit profile from the Settings hub; change the display name
  and the bio and save. The save is confirmed. Open your own profile; the new display name and bio are
  shown. Repeat reaching Edit profile from the "Edit profile" action on your own profile.
- **release_gating**: true
- **references**: REQ-PROD-016

#### REQ-UX-068 — Edit profile validates, reports failures in place, and keeps the person's input
- **statement**: Edit profile reports a field-level problem (an empty required display name, or a
  rejected value) against the field in plain words, reports a failed save at the form without
  discarding edited values so the person can retry, and confirms a successful save — never a silent
  success or a silent failure, and never a system or error code.
- **acceptance_criteria**: Clear the display name and attempt to save; the field shows an error naming
  the problem and no save occurs. Cause a save to fail (for example act during a transient server
  error); the failure is shown at the form, your edited display name and bio are still there, and
  retrying saves. A successful save shows a confirmation.
- **release_gating**: true
- **references**: REQ-PROD-016, REQ-PROD-033, REQ-PROD-034
