## Component library

The component library is the set of named, reusable pieces every chirp screen is built from. It is
why the many screens read as one product and not a dozen separately-styled pages: a chirp looks the
same in the timeline, a conversation, and a profile because all three draw the same **ChirpCard**;
a form error reads the same on sign-up and in settings because both use the same **TextField** and
**InlineError**. It is also where the unglamorous states live. Empty, loading, and error are not
left to each screen to improvise — they are built into the components, so every list that uses
**ListView** inherits a designed empty block, a loading skeleton, and a load-failure retry without
re-inventing them.

Every component below names its purpose, the design tokens it is built from (by name — no component
introduces a raw colour, size, space, radius, duration, or elevation), its behavior, and its states.
The siblings that come after this one — the per-screen flows, the responsive layout, and the
accessibility work — refer to these components **by the names in bold**.

**How states are read.** Each component records which of the five shared states apply to it —
**default**, **empty**, **error**, **loading**, **disabled** — and says plainly where a state does
not apply. "Does not apply" is a design decision, not an omission: a **PrimaryButton** has no *empty*
state because a button is never empty of content, and the error of the action it triggers is shown
by a feedback component next to it, not on the button itself. Two cross-cutting rules from the visual
language hold for every component here: meaning is never carried by colour alone (an error is a
`color.danger` border *and* a message; an active state is a colour *and* an icon or label), and every
interactive component shows the `color.border.focus` ring on keyboard focus.

---

### Identity and content

#### Avatar
- **Purpose**: Shows a person wherever they appear — in a **ChirpCard**, a **ProfileHeader**, the
  nav, and dense lists — so the same face is recognisable at a glance across the product.
- **Built from**: `radius.full` (always a circle); `color.border.default` (the 1px ring that lifts
  it off the surface); `avatar.sm` / `avatar.md` / `avatar.lg` / `avatar.xl` for size by context;
  `color.bg.subtle` + `color.text.secondary` + `type.heading` for the initials monogram; the
  monogram fill is derived deterministically from the handle so a person is always the same colour.
- **Behavior**: Renders at the size the context asks for. When it stands in for a link to a profile,
  the whole avatar is the target and it carries the focusable control's focus ring; on its own it is
  decorative and exposes the person's name to assistive technology.
- **States**:
  - **default** — the person's picture, circular, with the hairline border.
  - **empty** — no picture: a readable initials monogram on the deterministic fill, never a blank
    circle.
  - **error** — the picture fails to load: falls back to the same monogram as *empty*, never a
    broken-image glyph.
  - **loading** — a `color.bg.subtle` skeleton circle at the target size while the picture resolves.
  - **disabled** — does not apply (an avatar is not a control; when used as a link it takes the
    link's disabled treatment).

#### ChirpCard
- **Purpose**: One chirp, rendered the same way everywhere it appears — the timeline, a conversation,
  search and notification results, and a profile's chirps. The single most-repeated object in the
  product.
- **Built from**: `type.body` (the chirp text), `type.heading` (author display name), `type.meta`
  + `color.text.secondary` (handle and relative timestamp); `Avatar` at `avatar.md`; `space.4`
  padding and `space.2` internal gaps; `color.border.default` hairline between cards; `color.bg.surface`;
  `IconButton`s for reply, like, and a more-actions menu, laid out with `space.3` gaps.
- **Behavior**: The whole card is a target that opens the chirp in its conversation; the action
  controls inside it act in place without leaving the current screen. The like control uses
  `color.like` with a filled heart and a "Liked" label together (never colour alone). Timestamps are
  short and relative (`2m`, `4h`, then an absolute date). The author's own chirp exposes delete in the
  more-actions menu, which opens the **Dialog** confirmation variant.
- **States**:
  - **default** — avatar, author, handle, timestamp, chirp text, and the action row.
  - **empty** — does not apply (a card always carries a chirp; an empty *list* is the **ListView**'s
    *empty* state, not the card's).
  - **error** — two cases: an in-place action fails (the like or follow) → the control shows
    **InlineFeedback** in the danger role and reverts, draft of any reply preserved; or the chirp is
    gone (deleted, blocked, or unavailable) → a quiet tombstone row ("This chirp isn't available")
    rather than an empty gap.
  - **loading** — a skeleton card (`LoadingState`): a `color.bg.subtle` avatar circle, two
    text lines, and a short meta line, at the card's real dimensions so the list does not jump when
    content arrives.
  - **disabled** — does not apply (the card is not itself a single control; its individual actions
    carry their own disabled state).

#### ProfileHeader
- **Purpose**: The identity block at the top of a **profile** screen — the person's public face.
  Realises the profile archetype together with a **ListView** of their chirps below.
- **Built from**: `Avatar` at `avatar.xl`; `type.title` (display name), `type.body`
  (`color.text.secondary` handle and bio); `type.meta` + `type.numeral.tabular` for the follower and
  following counts so a changing count does not shift the layout; a `PrimaryButton` ("Follow") or
  `SecondaryButton` ("Following", "Edit profile" on one's own profile); `space.6` block spacing;
  `color.bg.canvas`.
- **Behavior**: Shows handle, display name, bio, and follower/following counts (the public profile
  needs no session). The primary action is context-dependent: Follow/Following for another account,
  Edit profile for one's own. The follow action is idempotent and acts in place.
- **States**:
  - **default** — full identity with picture, bio, counts, and the context action.
  - **empty** — a sparse profile: no bio and zero counts render as calm, labelled zeros and a
    one-line prompt rather than blank space; no picture uses the `Avatar` *empty* monogram.
  - **error** — the profile fails to load → an **EmptyState** error variant with retry; a
    blocked/suspended/not-found account states that plainly rather than showing a broken header.
  - **loading** — a skeleton header: skeleton avatar, name line, bio line, and count line.
  - **disabled** — does not apply (the header is a surface; its one action button carries its own
    disabled state).

---

### Input and composition

#### ComposeBox
- **Purpose**: Write and publish a chirp, or a reply to a named chirp. Used inline at the top of the
  timeline, as the body of the **Compose** dialog, and in a conversation's reply position.
- **Built from**: `type.body` for the draft text; `color.bg.subtle` draft area with `radius.md`;
  `space.4` padding; a remaining-character affordance in `type.caption` + `type.numeral.tabular`
  that moves to `color.warning` as the limit nears and `color.danger` when exceeded; a `PrimaryButton`
  ("Post" / "Reply"); `Avatar` at `avatar.md` for the composing person.
- **Behavior**: Enforces the published 280-character limit with a visible remaining-character count.
  The Post button is disabled while the draft is empty or over the limit; an empty or over-limit
  submit is rejected and nothing is posted. A drafted chirp is preserved across an interruption (an
  expired session routes to sign-in and returns the draft). The counter and the limit are the
  component's contract; the exact limit value comes from the product requirement, not from this
  component.
- **States**:
  - **default** — resting with a drafted-or-empty field and the live counter.
  - **empty** — no text: a placeholder prompt ("What's happening?"), counter at full, Post disabled.
  - **error** — over the limit (counter in `color.danger`, Post disabled) or a failed publish (an
    **InlineError** below the field in plain words, the draft kept so the person can retry).
  - **loading** — publishing in flight: Post shows its busy state and the field locks briefly so the
    chirp is not double-posted.
  - **disabled** — the whole box is unavailable (for example, composing is not permitted in the
    current state); the field and Post read as inactive.

#### TextField
- **Purpose**: One-line and multi-line text input with a label, optional hint, and inline,
  field-level validation. The building block of every **form** screen — sign-up, sign-in, recovery,
  edit profile.
- **Built from**: `type.meta` label; `type.body` input text; `radius.sm`; `space.3` inner padding;
  `color.border.strong` resting border, `color.border.focus` ring on focus, `color.danger` border in
  error; `color.text.secondary` hint; `type.family.mono` only where a value must be read exactly (a
  recovery code).
- **Behavior**: Validates at the field level and reports against the field, not in a summary far from
  the input. Messages say what to do in plain words and never surface a system or error code. A field
  whose validity needs a server check (handle availability and format at sign-up) shows a pending
  affordance while the check runs and resolves to a clear accepted or field-level error.
- **States**:
  - **default** — labelled, with the resting border, holding valid or in-progress input.
  - **empty** — label and placeholder/hint visible, no value yet; a required-but-empty field is not
    shown as an error until the person has had a chance to fill it.
  - **error** — `color.danger` border and an **InlineError** beneath, naming the problem and the fix
    ("That handle's already taken — try another").
  - **loading** — an async check is pending (for example handle uniqueness): a quiet pending
    indicator, the field not yet marked valid or invalid.
  - **disabled** — reads as inactive (`color.text.disabled`), not focusable, not submitted.

#### Toggle
- **Purpose**: An immediate on/off choice — notification categories, and other settings that take
  effect on change rather than on a separate Save. Used in **SettingRow**s.
- **Built from**: `color.primary` on-fill and `color.muted` off-fill; `color.text.on-primary`;
  `radius.pill`; `motion.fast` + `motion.easing.standard` for the thumb move (dropped under
  `motion.reduced`); a visible on/off label so state is never colour-or-position alone.
- **Behavior**: Flips immediately and persists the change, confirming with **InlineFeedback** on its
  row. If the save fails it reverts to the prior value and shows the failure, so the control never
  lies about the stored state.
- **States**:
  - **default** — on or off, with its label.
  - **empty** — does not apply (a toggle is always on or off).
  - **error** — the save failed → reverts and shows **InlineFeedback** in the danger role.
  - **loading** — saving: a brief pending treatment while the change is written.
  - **disabled** — a choice not currently available (for example a dependent preference), shown
    inactive with its reason where one is useful.

---

### Actions

#### PrimaryButton
- **Purpose**: The one most-important action on a view — Post, Follow, Save changes, Sign up, Delete
  (in a confirmation). One per view where possible, so the eye knows where the main action is.
- **Built from**: `color.primary` fill with `color.text.on-primary`; `radius.pill` (chirp's buttons
  are fully rounded); `type.body` `type.weight.semibold`; `space.3`/`space.5` padding;
  `color.border.focus` ring; `motion.fast` press. A destructive primary (Delete) uses `color.danger`
  in place of `color.primary`.
- **Behavior**: The label is a verb for the action in sentence case ("Save changes", "Delete chirp"),
  never "OK" or "Submit". While its action runs it shows a busy state in place, keeping its label and
  holding its width so the layout does not jump.
- **States**:
  - **default** — the resting filled button.
  - **empty** — does not apply (a button is never empty of content).
  - **error** — does not apply on the button itself; the action's failure is shown by **InlineError**
    or **InlineFeedback** at the point of action.
  - **loading** — busy/in-flight: a bounded spinner replaces or accompanies the label, the button is
    not re-triggerable, width is stable.
  - **disabled** — the action is not currently available (incomplete form, empty draft); the fill
    reads as inactive and the button is not focusable-to-activate.

#### SecondaryButton
- **Purpose**: A secondary or non-destructive alternative action — Cancel, Following (the unfollow
  affordance), secondary links styled as buttons. Lower weight than **PrimaryButton** so it never
  competes with the main action.
- **Built from**: `color.muted` fill (or a bordered-transparent variant on `color.border.strong`)
  with `color.text.primary`; `radius.pill`; `type.body` `type.weight.medium`; `space.3`/`space.5`
  padding; `color.border.focus` ring.
- **Behavior**: Same label and busy conventions as **PrimaryButton**. Paired with a PrimaryButton in
  a dialog or form, it is the calm way out (Cancel) and is never the destructive one.
- **States**:
  - **default** — the resting secondary button.
  - **empty** — does not apply.
  - **error** — does not apply on the button itself (see **PrimaryButton**).
  - **loading** — busy/in-flight, as **PrimaryButton**.
  - **disabled** — inactive treatment when unavailable.

#### IconButton
- **Purpose**: An icon-only control where space is tight and the action is well-known — reply, like,
  and more-actions on a **ChirpCard**, the compose affordance, the nav destinations, a dialog's
  close.
- **Built from**: `icon.md` (or `icon.lg` for the primary nav and compose affordance) from the one
  outline icon set, filled variant for an active/selected state; current text colour by default and a
  semantic role colour only to carry a state (`color.like` for an active like); `space.2` hit-area
  padding to a comfortable target; `radius.pill` hover/press fill in `color.bg.subtle`;
  `color.border.focus` ring.
- **Behavior**: Always exposes a text label to assistive technology and on hover — an icon is never
  the only thing a person or a screen reader has to go on. An active/selected state is shown by the
  filled icon *and* a mark or label, not by colour alone.
- **States**:
  - **default** — the outline icon at rest; plus an **active/selected** treatment (filled icon + mark)
    for the current nav destination or a liked chirp.
  - **empty** — does not apply.
  - **error** — does not apply on the control; the action's failure shows via **InlineFeedback** at
    the control.
  - **loading** — busy/in-flight: a bounded spinner in place of the icon for the running action.
  - **disabled** — inactive icon treatment, not activatable.

---

### Structure and navigation

#### NavShell
- **Purpose**: The persistent frame a person lives in. Two shells: the **signed-out shell** a visitor
  meets, and the **signed-in shell** a member uses. The transition between them is the
  sign-up / sign-in / sign-out boundary.
- **Built from**: the chirp wordmark in `type.title`; `IconButton`s + `type.meta` labels for
  destinations; `Avatar` at `avatar.sm` in the account entry; `color.bg.canvas` / `color.bg.surface`;
  `color.border.default` edge; `elevation.0` (it is part of the frame, separated by a border); the
  active destination marked with a filled `IconButton` + `color.primary` accent *and* a mark.
- **Behavior**:
  - *Signed-out shell*: carries the wordmark (to the Landing), a clear **Sign in** and a prominent
    **Sign up**, and footer access to **Rules & terms** and **Help & support** — on every signed-out
    screen, so a visitor on a shared link never dead-ends at an auth wall.
  - *Signed-in shell*: exposes **Home**, **Explore**, **Notifications** (with an unseen-activity
    indicator), **Profile**, an always-available **Compose** affordance, and an account menu reaching
    **Settings**, **Help & support**, **Rules & terms**, and **Sign out** — reachable from every
    signed-in screen.
  - The active destination is always marked; how the shell reflows between a phone and a wider
    viewport is the responsive area's decision and how it is operated and announced is the
    accessibility area's — this component fixes the destinations and the markings, not the layout.
- **States**:
  - **default** — the shell with its destinations and the active one marked; the signed-in shell may
    show the Notifications unseen-activity indicator.
  - **empty** — does not apply (the shell always has its fixed destinations).
  - **error** — does not apply to the frame; a destination's screen holds its own error.
  - **loading** — does not apply; the shell is persistent and renders immediately, so moving between
    screens never blanks the frame.
  - **disabled** — does not apply (individual entries unavailable in a state read as inactive, but
    the shell is always present).

#### ListView
- **Purpose**: The paginated container behind every **feed/list** screen — the home timeline, a
  conversation's replies, notifications, search results, and followers/following. Hosts **ChirpCard**s
  (or the row kind the screen needs) and owns the list-level empty, loading, and error treatments.
- **Built from**: `space.measure` (the 600px reading column); `space.4` gutters on a phone;
  `color.border.default` separators; `space.4` inter-item gap; `SecondaryButton` or a text control
  for "load older"; a catch-up control ("N new chirps") in `color.primary`; **LoadingState**,
  **EmptyState**, and **InlineError** for its own states.
- **Behavior**: Loads in bounded pages, never one unbounded load. Offers an explicit way to load
  older items, and the timeline offers a way to pull in chirps posted since the person last looked.
  Keeps the person's scroll place when they return from drilling into an item.
- **States**:
  - **default** — a bounded page of items with the load-older (and, for the timeline, catch-up)
    affordances.
  - **empty** — the list has no items → an **EmptyState** block explaining why and offering a next
    step (a brand-new timeline points to Explore and compose), never a blank area.
  - **error** — a page fails to load → an **InlineError** with a retry in place of the missing items;
    a failure while loading *older* items shows at the load-more boundary without discarding the items
    already shown.
  - **loading** — first load shows **LoadingState** skeleton rows (not a spinner on a blank screen);
    loading older items shows a bounded spinner at the boundary.
  - **disabled** — does not apply.

#### SettingRow
- **Purpose**: One labelled choice within a **settings** screen — a value to view or change, a
  **Toggle**, or a link into a sub-section. The repeated unit that realises the settings archetype
  across the settings hub and its sub-sections (edit profile, account & contact, notification
  preferences, sessions & devices, blocked & muted, export, delete).
- **Built from**: `type.body` label and `type.meta` + `color.text.secondary` description; a control
  slot holding a `Toggle`, a `SecondaryButton`, a value, or a chevron **IconButton** for a drill-in;
  `space.4` row padding; `color.border.default` separators; `color.danger` label for a destructive
  row (Delete account), which opens the **Dialog** confirmation variant.
- **Behavior**: Each row is independently operable and, where it drills in, is an addressable
  sub-section a person can open directly and return from to the hub. A change that takes effect
  immediately confirms on the row with **InlineFeedback**; a destructive row routes through a
  confirmation.
- **States**:
  - **default** — label, description, and its control or value.
  - **empty** — does not apply at the row level; a sub-section with nothing in it (no blocked
    accounts, no other sessions) shows an **EmptyState** within the section, not an empty row.
  - **error** — a change made on the row failed → **InlineFeedback** in the danger role on that row,
    prior value restored.
  - **loading** — the change is saving → a brief pending treatment on the row's control.
  - **disabled** — a choice not available in the current state, shown inactive with a reason where
    one helps.

---

### Overlays

#### Dialog
- **Purpose**: A focused task or decision layered over the current screen without leaving it. Two
  variants cover two archetypes: a **modal/dialog** (Compose, Report) and a **confirmation** (delete
  account, delete chirp, block/mute, end a session, sign out of all sessions).
- **Built from**: `color.bg.surface` panel at `radius.md` and `elevation.3`, over the
  `color.bg.scrim`; `type.heading` title; `type.body` content; a `PrimaryButton` + `SecondaryButton`
  action pair (the destructive confirm uses the `color.danger` primary, Cancel is the secondary);
  a close `IconButton`; `motion.base` rise-over-scrim (dropped to a fade under `motion.reduced`);
  `space.6` padding.
- **Behavior**: Traps focus while open and returns focus to the control that opened it on close. The
  browser back control dismisses it (closing the dialog, not leaving the underlying screen). The
  *confirmation* variant names the consequence plainly and always offers a clear way out; the
  account-deletion confirmation additionally states what is and is not kept and points to data export
  first. The *modal* variant hosts a task component such as **ComposeBox**.
- **States**:
  - **default** — the panel open over the dimmed screen, title and action pair visible.
  - **empty** — does not apply (a dialog always opens with its content).
  - **error** — the dialog's action failed → an **InlineError** inside the panel; the dialog stays
    open with any draft preserved so the person can retry.
  - **loading** — the confirm action is running → the confirm button shows its busy state; the dialog
    does not close until the action resolves.
  - **disabled** — the confirm is disabled until a required input or acknowledgement is given.

---

### Feedback and status

#### Toast
- **Purpose**: Brief, non-blocking confirmation that an action completed — a chirp published, a
  follow, a saved setting, a received report — shown without interrupting what the person is doing.
- **Built from**: `color.bg.surface` at `radius.md` and `elevation.4` (it floats above everything);
  `type.body` message; an optional inline undo/dismiss as a text control; `motion.base` slide-in and
  auto-dismiss (a fade under `motion.reduced`); `color.success` / `color.info` / `color.danger`
  accent by kind, always paired with a word, never colour alone.
- **Behavior**: Appears, is readable without stealing focus, and dismisses itself after a bounded time
  (or on an explicit dismiss). Used for results that do not belong against a specific control; a
  failure tied to a specific control uses **InlineFeedback** at the control instead.
- **States**:
  - **default** — a success or neutral confirmation.
  - **empty** — does not apply.
  - **error** — a danger-accented variant for a background failure that has no single on-screen
    control to attach to.
  - **loading** — does not apply (a toast marks a resolved result, not an in-flight one).
  - **disabled** — does not apply.

#### InlineFeedback
- **Purpose**: The result of an in-place action shown against the control that triggered it — a like
  that took, a follow that failed — so the feedback is where the person's attention already is.
- **Built from**: `type.meta`; `color.success` or `color.danger` with an icon and a word (never
  colour alone); `space.2` gap from its control; `motion.fast`.
- **Behavior**: Appears next to the control, confirms or reports the result, and clears on its own.
  On failure it accompanies a revert of the optimistic change, so the control never shows a result
  that did not happen.
- **States**:
  - **default** — a success/neutral in-place confirmation.
  - **empty** — does not apply.
  - **error** — a failure against the control in the danger role, with a plain reason and the state
    reverted.
  - **loading** — does not apply (it reports a resolved action; the in-flight state belongs to the
    control's own *loading*).
  - **disabled** — does not apply.

#### InlineError
- **Purpose**: The field- or control-level error message — the plain-words explanation of what went
  wrong and what to do, shown at the point of the problem. The error carrier for **TextField**,
  **ComposeBox**, **Dialog**, and **ListView**.
- **Built from**: `type.meta` in `color.danger`; a danger icon beside the text (so the error is not
  colour alone); `space.1`/`space.2` gap below the field or control it belongs to.
- **Behavior**: Names what happened and what to do in plain language, never a system or error code,
  and never blames the reader ("That handle's already taken — try another"). It appears where the
  action was taken and is associated with its field for assistive technology.
- **States**:
  - **default** — the error message shown; this component *is* the error treatment, so its resting
    state is the error being presented.
  - **empty** — does not apply (absent when there is no error).
  - **error** — this component is itself the error presentation; there is no second error-of-the-error.
  - **loading** — does not apply.
  - **disabled** — does not apply.

---

### State blocks

#### EmptyState
- **Purpose**: The designed treatment for a surface with nothing in it — a brand-new timeline, an
  empty notifications list, no blocked accounts, a not-found page, and the explanatory landing and
  onboarding screens. Realises the **empty/landing** archetype and supplies the *empty* state other
  components (notably **ListView**) compose in.
- **Built from**: a simple flat illustration in one or two brand hues (calm and explanatory, never
  decorative in the feed); `type.title` headline; `type.body` `color.text.secondary` explanation; a
  `PrimaryButton` or link for the next step; `space.10`/`space.12` generous vertical spacing;
  `color.bg.canvas`.
- **Behavior**: Explains why the surface is empty and offers a next step rather than apologising for
  being empty — a new timeline points to Explore and composing a first chirp; onboarding explains the
  empty timeline and offers at least one route to a non-empty one. It is never a blank area.
- **States**:
  - **default** — the explanatory empty block with its illustration and next step.
  - **empty** — this component *is* the empty treatment; the empty surface is its purpose.
  - **error** — an error-flavoured variant: "We couldn't load this — try again" with a retry, which
    is how a failed load differs from a genuinely-empty surface so the two are never confused.
  - **loading** — does not apply (a surface that is loading shows **LoadingState**, not EmptyState).
  - **disabled** — does not apply.

#### LoadingState
- **Purpose**: The designed treatment for content that is on its way — a skeleton that holds the
  shape of what is coming, and a bounded spinner for smaller in-place loads. Supplies the *loading*
  state other components compose in (**ListView**, **ChirpCard**, **ProfileHeader**, **Avatar**).
- **Built from**: `color.bg.subtle` skeleton blocks at the real dimensions of the content, with a
  subtle `motion.base` shimmer that honours `motion.reduced` (a static block when motion is reduced);
  `radius.sm`/`radius.md`/`radius.full` matching the shapes being stood in for; a bounded spinner
  (the only element permitted to animate continuously, per the motion rules).
- **Behavior**: Stands in for content at its true size so the layout does not jump when real content
  arrives. A first load uses skeletons rather than a spinner on a blank screen; a small or in-place
  load uses a bounded spinner. Nothing loads forever — a load that fails hands off to the owning
  component's *error* state.
- **States**:
  - **default** — the skeleton (or bounded spinner) shown while content resolves; this component *is*
    the loading treatment.
  - **empty** — does not apply.
  - **error** — does not apply here; a failed load becomes the owning component's *error* state
    (**ListView** error, **InlineError**, or an **EmptyState** error variant).
  - **loading** — this component is itself the loading presentation.
  - **disabled** — does not apply.

---

### Archetype coverage

Every screen archetype in the IA screen inventory is furnished by at least one named component or a
documented composition of them, so no archetype is left without a designed treatment:

| Archetype | Furnished by | Example screens |
|---|---|---|
| feed/list | **ListView** hosting **ChirpCard**s, with **LoadingState**, **EmptyState**, and **InlineError** for its states | Home timeline, Chirp / conversation, Notifications, Explore, Followers, Following |
| form | **TextField** + **Toggle** + **PrimaryButton** + **SecondaryButton** + **InlineError**, in a form layout | Sign up, Sign in, Recover access, Set new credential, Edit profile |
| profile | **ProfileHeader** + a **ListView** of **ChirpCard**s | Public profile, Own profile |
| settings | a list of **SettingRow**s inside the signed-in **NavShell** | Settings hub, Account & contact, Notification preferences, Sessions & devices, Blocked & muted, Export, (Delete routes to a confirmation) |
| modal/dialog | **Dialog** (modal variant), hosting **ComposeBox** for Compose | Compose, Report |
| confirmation | **Dialog** (confirmation variant) | Delete account, Delete chirp, Block / mute, Sign out |
| empty/landing | **EmptyState** | Landing, Onboarding, Rules & terms, Help & support, Not found |

The two shells themselves — signed-out and signed-in — are the **NavShell** component, inside which
every signed-in archetype renders.

---

## Requirements and acceptance criteria — REQ-UX-033..039

The component-library requirements chirp must meet. Each is testable by someone who never met the
author, against the live product; each carries a `release_gating` flag and references the product
requirement(s) it serves. These are this area's entries in the consolidated `REQ-UX` register; the
visual-system synthesis assembles them with the visual-language entries (`REQ-UX-020..032`).

#### REQ-UX-033 — Screens are built from the named component vocabulary, not one-off controls
- **statement**: Every screen is assembled from the named components in this library — one chirp card,
  one compose box, one button set, one text field, one dialog, and so on — rather than each screen
  introducing its own version of the same thing.
- **acceptance_criteria**: On three screens of different archetypes (for example the home timeline, a
  profile, and a settings sub-section), a chirp is rendered the same way, buttons share one shape and
  one primary colour, and text fields and error messages share one treatment; no screen shows a
  bespoke control that does the job of a library component but looks or behaves differently.
- **release_gating**: true
- **references**: REQ-PROD-033

#### REQ-UX-034 — Every component is built from the published design tokens
- **statement**: Each component draws its colour, type, spacing, radii, elevation, and motion from the
  published token set by name; no component introduces a raw hex, a one-off size, or a bespoke
  duration.
- **acceptance_criteria**: Inspect a chirp card, a primary button, a text field, and a dialog on the
  live product in both offered themes; their colours match the token roles (a primary action is the
  one `color.primary`, a destructive one `color.danger`), their text sizes match the type scale, and
  nothing renders a colour or size that is absent from the token set.
- **release_gating**: true
- **references**: REQ-PROD-033

#### REQ-UX-035 — The chirp card and compose box behave to the product's core-loop contract
- **statement**: The compose box enforces the published character limit with a visible
  remaining-character affordance and rejects an empty or over-limit chirp; the chirp card shows the
  author, handle, relative timestamp, chirp text, and the like, reply, and more-actions controls, and
  shows the active-like state with a filled icon and label, not colour alone.
- **acceptance_criteria**: Open compose, type past the limit — the counter turns to the danger
  treatment and Post is disabled; clear to an empty draft — Post is disabled and nothing posts; post a
  valid chirp — it appears as a chirp card with avatar, author, handle, relative time, text, and the
  action row. Like a chirp — it shows a filled heart and a "Liked" label together, and is still
  identifiable as liked in greyscale.
- **release_gating**: true
- **references**: REQ-PROD-001, REQ-PROD-005

#### REQ-UX-036 — Every list has designed empty, loading, and load-failure states
- **statement**: Lists are rendered by the list component, which shows a loading skeleton on first
  load, an explanatory empty block when there is nothing to show, and an inline retry when a page
  fails — never a blank area, a spinner on a blank screen, or a raw failure.
- **acceptance_criteria**: Reach a brand-new account's empty timeline — it shows an explanatory block
  with a next step, not a blank page. Open a list while it loads — it shows skeleton rows at the real
  item size, not a spinner on blank. Force a page-load failure — the list shows an inline message with
  a retry in place of the missing items, keeping any items already shown.
- **release_gating**: true
- **references**: REQ-PROD-002, REQ-PROD-033

#### REQ-UX-037 — Forms validate inline at the field level, in plain language
- **statement**: Form inputs use the text-field component with field-level validation and an inline
  error in the danger role; error messages say what happened and what to do, never a system or error
  code, and an input that needs a server check shows a pending state before resolving.
- **acceptance_criteria**: On sign-up, submit a handle already in use — the error appears against the
  handle field in plain words naming the handle, not in a distant summary and not as a code; submit a
  mis-formatted handle — a field-level validation error explains the rule; while a handle is being
  checked for availability, the field shows a pending state rather than flicking prematurely to valid
  or invalid.
- **release_gating**: true
- **references**: REQ-PROD-009, REQ-PROD-001

#### REQ-UX-038 — Consequential actions are confirmed through the dialog confirmation variant
- **statement**: Every destructive or irreversible action is confirmed through the dialog confirmation
  variant that names the consequence and offers a cancel; the account-deletion confirmation also
  states what is and is not kept and points to data export first.
- **acceptance_criteria**: Initiate deleting a chirp, blocking an account, and deleting the account;
  each presents a confirmation that names what will happen and offers a plain cancel, and nothing
  changes on cancel. The account-deletion confirmation additionally states what is and is not retained
  and points to export before proceeding.
- **release_gating**: true
- **references**: REQ-PROD-022

#### REQ-UX-039 — The result of every action is shown through the feedback components
- **statement**: A completed action is confirmed with a brief, non-blocking toast or inline feedback;
  an in-flight action shows its control's busy state; a failed in-place action shows inline feedback at
  the control and preserves any in-progress work rather than failing silently or discarding a draft.
- **acceptance_criteria**: Publish a chirp, follow an account, and save a setting — each shows brief,
  non-blocking confirmation. Trigger an action and observe its control while it runs — the control
  shows a busy state and is not re-triggerable. Force an in-place failure (act while offline, or a
  transient server error while posting) — the failure is shown at the control with a way to retry and
  the drafted text is not lost.
- **release_gating**: true
- **references**: REQ-PROD-001, REQ-PROD-034

---

*Design-methodology note: this component library was designed to the Experience Design bundle's
intent (design systems and component design) and general product-design practice; the design-domain
methodology loader was unavailable in the reconstructed environment, so the work draws on that bundle
intent and product-design competence rather than a loaded methodology file. The library composes
against the published design-token vocabulary (`color.*`, `type.*`, `space.*`, `radius.*`,
`elevation.*`, `motion.*`) and the IA screen inventory and archetypes, and does not redefine either.*
