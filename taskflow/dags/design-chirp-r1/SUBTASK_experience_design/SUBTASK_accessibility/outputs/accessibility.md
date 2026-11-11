## Accessibility

Accessibility is part of whether a person can use chirp and trust it with their account, not a
finish applied at the end. A reader who navigates by keyboard, a person using a screen reader, someone
who has zoomed the page to read it, and a reader who has asked their system to stop animating things are
all people chirp is for, and the product is held to a stated standard for them in the same way it is held
to a stated standard for durability or availability.

This section does three things. It names the exact standard chirp conforms to, so "accessible" is a
checkable claim and not a sentiment. It designs to that standard across the seven screen archetypes in
the **Screen inventory** and the named pieces in the **Component library** — rather than re-deciding
accessibility screen by screen, it is decided once per archetype and once per component, which is the
same economy the visual system and the responsive design use. And it says how conformance is verified, so
a tester who never met the author can reach the same verdict. Where the visual system already fixes a
token-level rule that carries accessibility weight — the contrast intents on the palette (REQ-UX-022), the
always-visible focus ring (REQ-UX-025), icons never carrying meaning by colour alone (REQ-UX-028), and the
`motion.reduced` contract (REQ-UX-029) — this section composes against those rules and states the
conformance obligation they serve, rather than restating or redefining them.

### The standard chirp commits to

chirp conforms to the **Web Content Accessibility Guidelines (WCAG) 2.1, Level AA** — every Level A and
every Level AA success criterion in WCAG 2.1, across the product. This is the named, versioned target the
rest of this section is held to, and it is the concrete form of the product-level accessibility baseline
(REQ-PROD-036), which leaves the exact standard to this design to fix. WCAG 2.1 AA is the standard
commonly referenced by consumer and public-sector accessibility obligations, which is why it is the floor
a releasable consumer web product is expected to meet rather than an aspiration above it.

What committing to WCAG 2.1 AA obliges chirp to, in the terms a reader experiences:

- everything a person can do with a pointer, they can do with a keyboard alone, in a sensible order, with
  the focused element always visible and never trapped (WCAG 2.1.1, 2.4.3, 2.4.7, 2.1.2);
- every control has a name, a role, and a state that assistive technology can report (WCAG 4.1.2), and the
  structure of each screen — its regions, its headings, its lists — is conveyed and not merely drawn
  (WCAG 1.3.1, 2.4.6);
- text and meaningful controls meet the contrast ratios in WCAG 1.4.3 and 1.4.11, the page can be enlarged
  and reflowed without loss (WCAG 1.4.4, 1.4.10, 1.4.12), and nothing relies on colour, shape, or motion
  as the only way to carry a fact (WCAG 1.4.1, 1.4.11, 2.3.1);
- the product tells assistive technology when something changed that was not the result of a direct action
  — a chirp posted, a page loaded, an action failed, a session expired (WCAG 4.1.3, 3.3.1).

**The gated conformance set versus the whole product.** The release bar (REQ-PROD-036) gates the
accessibility baseline on the screens a person must pass through to use chirp for what it is for: the core
loop (read the timeline, compose and post, reply, like, follow, view a profile) and the screens that get
them in and oriented (sign-up, sign-in, recovery, onboarding), together with the empty, loading, and error
states those screens present. Those screens MUST meet WCAG 2.1 AA for a release. The same standard applies
to every other screen in the inventory — settings and its sub-sections, export, deletion, report and
block — and they are designed to it here; where such a screen belongs to a product surface the release bar
itself does not gate (notifications and its preferences on REQ-PROD-029, Explore on REQ-PROD-042), its
accessibility requirement inherits that surface's non-gating flag and ships when the surface ships, held to
the same standard when it does.

**The near-term direction** is WCAG 2.2 AA, which adds criteria chirp should adopt as a fast follow — a
minimum target size (2.2's 2.5.8), focus never hidden behind sticky chrome (2.4.11), and no need to
remember information across steps of a flow (3.3.7). One of these, the minimum target size, is designed in
below ahead of a full 2.2 move because it matters most on a phone; it is marked as the beyond-2.1 commitment
it is, so the staging is explicit.

### Operability — the product works without a mouse

Operability is the half of accessibility a keyboard user and most switch and voice users depend on
entirely: if a thing can only be done by pointing at it, it cannot be done by them at all.

**Everything is keyboard-operable.** Every action the product offers through a pointer is reachable and
operable with the keyboard alone, on every archetype. Concretely: in a **feed/list** a person can move
through the chirps and operate each **ChirpCard**'s reply, like, and more-actions controls and open a chirp
into its conversation; in a **form** they can reach and complete every **TextField**, **Toggle**, and
button and submit; in **settings** they can operate every **SettingRow**; the **modal/dialog** and
**confirmation** **Dialog**s and the **ComposeBox** are fully operable; and the signed-out and signed-in
**NavShell**s — every destination, the compose affordance, and the account menu — are operated from the
keyboard. No chirp feature is pointer-only (WCAG 2.1.1).

**Focus order follows the reading order, and focus is always visible.** As a person tabs through a screen,
focus moves in the order the screen reads — the nav shell, then the screen's heading and content, then its
actions — so the sequence makes sense without sight of the pointer (WCAG 2.4.3). The focused element always
shows the `color.border.focus` ring the visual system guarantees (REQ-UX-025); this section's obligation is
that focus order is logical and that focus is never lost to an invisible or off-screen element (WCAG
2.4.7). When a view changes — a **Dialog** opens, a route changes, the catch-up control loads new chirps —
focus is moved deliberately to a sensible place (the dialog's first control or its heading; the new
screen's main heading) rather than left stranded on a control that no longer exists.

**No keyboard trap, and overlays return focus.** A keyboard user can move into and out of every component
with the keyboard; nothing captures the Tab key with no way out (WCAG 2.1.2). The **Dialog** is the one
place focus is deliberately held — a modal traps focus within the open panel so Tab cycles inside it, which
is correct modal behaviour — but it is always escapable: Esc closes it, the close control and Cancel are in
the cycle, and on close focus returns to the control that opened it (composing with the component's stated
focus-return behaviour).

**Bypass to content.** Because the **NavShell** repeats its destinations at the top of every signed-in
screen, a keyboard or screen-reader user is given a way to skip past it straight to the screen's main
content, so they are not tabbing through the whole shell on every screen (WCAG 2.4.1). This is satisfied by
a visible-on-focus "Skip to content" control at the top of the tab order together with the landmark and
heading structure below, either of which lets assistive technology jump to `main`.

**Targets are big enough to hit.** Pointer and touch targets for the product's controls are at least 24×24
CSS pixels, and the primary touch targets on a phone — the **NavShell** destinations, the compose
affordance, and a **ChirpCard**'s action row — are sized to the comfortable minimum the responsive design
sets, so a control is not a pixel-perfect tap. This adopts WCAG 2.2's Target Size (Minimum) (2.5.8) ahead
of a full move to 2.2; it is a commitment beyond the 2.1 AA floor, and it serves the product's phone
requirement (REQ-PROD-035).

### Semantics — the product makes sense to assistive technology

A screen reader does not see chirp's layout; it reads the names, roles, states, and structure the product
exposes. Semantics is making sure what a sighted person perceives from position and styling is also present
as information a screen reader can report (WCAG 1.3.1, 4.1.2).

**Every component carries a name, a role, and its state.** The component library is the right place to fix
this once, because the same component carries the same semantics everywhere it appears. Each piece in the
library exposes the following to assistive technology:

| Component | Role exposed | Accessible name | States exposed |
|---|---|---|---|
| **NavShell** | `navigation` landmark (signed-out and signed-in); account entry is a menu button | "Primary" / "Account" | the current destination is marked programmatically (not colour alone); unseen-activity on Notifications is announced, not only dotted |
| **ChirpCard** | an `article` with the author and time in its label; the card's open-conversation target is a link; reply/like/more are buttons | author + relative time; each action button names its action and its subject | like exposes pressed/not-pressed; a removed chirp is announced as a labelled "not available" row, not a silent gap |
| **ProfileHeader** | a labelled header region | the person's display name and handle | the follow control exposes following / not-following; counts are read with their labels |
| **ComposeBox** | a multi-line text box with a visible, associated label | "Post a chirp" / "Reply to @handle" | the remaining-character count is associated with the field and announced as it nears and passes the limit; Post exposes disabled and busy |
| **TextField** | a labelled single- or multi-line input | its visible label | hint and error associated via description; invalid and required are exposed; a pending async check is announced |
| **Toggle** | a `switch` | its row label | on / off exposed as the switch state, with a visible on/off label as well |
| **PrimaryButton** / **SecondaryButton** | `button` | its visible verb label ("Post", "Save changes", "Delete chirp") | disabled and busy exposed; a destructive primary is named by its action, not by colour |
| **IconButton** | `button` (or a link where it navigates) | a text label always present, never the icon alone | active/selected (e.g. the current nav item, a liked chirp) exposed programmatically |
| **ListView** | a list / feed structure; "load older" and the catch-up control are buttons | the list's purpose; "Load older chirps"; "N new chirps" | its empty, loading, and load-failure states are conveyed to assistive technology (see Feedback and errors) |
| **SettingRow** | a labelled row grouping its control with its description | the setting's label | the inner control's own state; a destructive row names its consequence |
| **Dialog** | `dialog`, modal, labelled by its title | the dialog title | open/closed via presence; the confirm control exposes disabled and busy |
| **Toast** / **InlineFeedback** | a status region (see Feedback and errors) | the message text | success vs failure carried by text and icon, not colour alone |
| **InlineError** | an alert associated with its field or control | the error text | — (its presence is the error state; it is tied to the field as that field's description and invalidity) |
| **EmptyState** | a region with a heading and an action; its error variant is an alert | the headline | genuinely-empty vs failed-to-load distinguished in text, not only by illustration |
| **LoadingState** | a busy indication with a polite "loading" message; decorative skeletons are hidden from assistive technology | "Loading" | resolves to the owning component's content or its error state |
| **Avatar** | an image with the person's name as its text alternative, or marked decorative when an adjacent text name already carries it | the person's display name | the initials-monogram and load-failure fallbacks carry the same name, never a "broken image" |

**Regions and headings give each screen a shape.** Every screen exposes landmark regions — a banner and
the primary `navigation` for the **NavShell**, a single `main` for the screen's content, and a
`contentinfo` footer where the signed-out shell carries one — so a screen-reader user can jump between the
parts of the page (WCAG 1.3.1). Every screen has exactly one top-level heading that names it and matches the
document title the wayfinding model sets, and sub-headings nest in order without skipping a level (WCAG
1.3.1, 2.4.6). The settings hub and its sub-sections, which are a small secondary navigation, expose their
grouping so a person knows they are inside a sub-section and how to get back.

**Lists are exposed as lists.** The **feed/list** archetype — the home timeline, a conversation, the
notifications list, search results, and followers/following — is conveyed with its item structure, so a
screen-reader user can move item by item and knows where they are in the set rather than meeting an
undifferentiated run of text (WCAG 1.3.1). The pagination and catch-up affordances are named controls, not
mystery widgets.

**Icon-only controls always have words.** Every **IconButton** exposes a text label to assistive technology
and on hover, composing with the visual system's rule that an icon is never the only carrier of meaning
(REQ-UX-028); an active or selected state (the current nav destination, a liked chirp) is exposed as a
state and not inferred from a colour or a fill alone (WCAG 1.1.1, 4.1.2).

### Perception — the product is perceivable for different sight and motion needs

**Contrast.** chirp meets WCAG 1.4.3 for text (at least 4.5:1 for body text, 3:1 for large text) and WCAG
1.4.11 for the boundaries of meaningful controls and icons (at least 3:1), in each theme the product ships.
This is fixed at the token level by the palette's contrast intents and verified by the visual system's
contrast requirement (REQ-UX-022); the accessibility obligation stated here is that meeting those ratios is
a condition of WCAG 2.1 AA conformance and is part of the gated baseline, checked on the live product in
whatever theme(s) ship.

**Enlarging and reflowing the page.** A person can enlarge text to 200% without content being clipped or
controls becoming unreachable (WCAG 1.4.4), and the product reflows to a 320-CSS-pixel-wide viewport
without a second scrollbar in the reading direction and without loss of content or function — the single
600px reading column and phone-first layout the visual and responsive designs set is what makes this hold
(WCAG 1.4.10). Overriding text spacing (line height, paragraph, letter, and word spacing) does not clip or
overlap content (WCAG 1.4.12).

**No fact is carried by colour alone.** Composing with the visual system's rule (REQ-UX-022 / consistency
rule 7), every state that uses a semantic colour also uses text, an icon, or a label: a field error is a
`color.danger` border and an **InlineError** message; an active like is the `color.like` colour and a
filled heart and a "Liked" label; the current nav destination is a fill and a mark. A person who cannot
distinguish those colours still gets the fact (WCAG 1.4.1). The product does not restrict itself to a single
screen orientation.

**Motion is safe and can be turned down.** Nothing in chirp flashes more than three times in any one second,
so no content poses a seizure risk (WCAG 2.3.1). When a reader has asked their system to reduce motion, the
product honours it through the `motion.reduced` contract the visual system defines (REQ-UX-029): transitions
become an instant change or a short opacity fade, counts do not animate, and nothing conveys required
information only through movement. The bounded loading indicator is the one thing permitted to animate, and
it has a static, announced equivalent.

### Feedback and errors — the product speaks its state

A sighted person sees a toast slide in, a skeleton fill with chirps, or an error appear under a field. A
screen-reader user perceives none of that unless the product announces it. This is the accessible
counterpart of the considered-states work: the same empty, loading, error, and status moments the product
is required to show (REQ-PROD-033, REQ-PROD-034) must also be spoken.

**Status messages are announced without stealing focus.** When something changes that was not a direct
keystroke — a chirp is published, a follow is saved, a report is received, new chirps arrive behind the
catch-up control — the product announces it through a polite live region so a screen-reader user hears it
without being yanked away from what they are doing (WCAG 4.1.3). This is how **Toast** and **InlineFeedback**
reach assistive technology: the confirmation is spoken, and the success-versus-failure distinction is in the
words, not the colour.

**Errors are announced and tied to their cause.** A failed action is announced, and a field-level error is
both associated with its field (so moving to the field re-reads the problem) and names the field as invalid,
so a screen-reader user reaches the problem and understands it without hunting (WCAG 3.3.1). The
**InlineError** text says what happened and what to do in plain words with no system or error code
(composing with the voice rules, REQ-UX-032), which satisfies both error identification and a suggestion for
fixing it (WCAG 3.3.1, 3.3.3); every **TextField** keeps its visible, associated label and any instruction
(WCAG 3.3.2). A failure that has no single control to attach to is announced through the status region
rather than left silent.

**Empty, loading, and expired states reach assistive technology.** A **ListView**'s loading state announces
that content is loading while its decorative skeletons are hidden from the screen reader, and resolves to
either the arrived content or an announced error with a reachable retry — never silence, and never a
skeleton read out as gibberish. An **EmptyState** is a real heading and an action a screen-reader user lands
on and can act on, and its error variant is announced as an alert so a failed load is told apart from a
genuinely empty surface. When a session expires mid-action, the interception the interaction model performs
(REQ-UX-008) is announced with its reason and focus is moved to the sign-in screen, so an expired session is
a spoken, recoverable event and not a silent dead end (WCAG 3.3.1; REQ-PROD-034).

### Verification — how conformance is checked

A conformance claim is only as good as the check behind it. chirp's accessibility is verified, before a
release, by exercising the gated conformance set — the core loop and the get-in screens with their empty,
loading, and error states — three complementary ways, because no one way catches everything:

1. **An automated check** across the gated screens in each shipped theme, to catch the machine-detectable
   failures (missing names, invalid roles, contrast below ratio, missing labels). Automated tools find a
   minority of issues but find them cheaply and repeatably; a clean automated pass is necessary, not
   sufficient.
2. **A keyboard-only pass**: with the pointer unused, complete the core loop and the get-in flows — reach
   and operate every control, confirm focus order reads sensibly, focus is always visible, no component
   traps focus, the skip-to-content path works, and every **Dialog** is escapable and returns focus.
3. **A screen-reader pass** of the core loop on at least the matrix below: confirm every control is reported
   with a sensible name, role, and state; headings and regions let the reader navigate; lists are navigable
   as lists; and the posted / saved / failed / loading / expired-session moments are all announced.

**The support matrix** the screen-reader and keyboard passes are run against is at least one screen reader
per major platform with its common browser pairing — a desktop screen reader with a current browser, and a
mobile screen reader with the mobile browser — since chirp is a responsive web product people reach from
both. The matrix is stated with the release so the claim names what it was checked against.

**The gate.** A release is blocked until the gated conformance set passes all three checks with no
outstanding Level A or Level AA failure; a failure found is a fix, not a waiver. An accessibility issue on a
non-gating surface (a notifications or Explore screen) is tracked against that surface and travels with it.
This is the concrete acceptance behind the product baseline (REQ-PROD-036): the standard is WCAG 2.1 AA, the
evidence is the three passes over the gated set, and the matrix records what the evidence was gathered on.

### Requirements and acceptance criteria — REQ-UX-100..119

The accessibility requirements chirp must meet. Each is testable by someone who never met the author,
against the live product; each carries a `release_gating` flag (a `false` flag carries a one-line reason)
and references the product requirement(s) it serves. These compose with — and do not redefine — the
visual-system requirements that carry accessibility weight (REQ-UX-022 contrast, REQ-UX-025 focus ring,
REQ-UX-028 icon labelling, REQ-UX-029 reduced motion); where a requirement below depends on one of those, it
references it rather than restating it.

#### REQ-UX-100 — A named, versioned accessibility standard: WCAG 2.1 AA
- **statement**: chirp commits to conform to WCAG 2.1 Level AA (every Level A and AA success criterion)
  across the product; the core loop and the get-in screens (sign-up, sign-in, recovery, onboarding) with
  their empty/loading/error states are the gated conformance set that must meet it for a release, and the
  same standard applies to every other screen, inheriting the non-gating flag of any surface the release bar
  itself does not gate.
- **acceptance_criteria**: Find chirp's stated accessibility standard; it names WCAG 2.1 and Level AA, not
  "accessible" in the abstract. Walk the core loop and confirm its screens are held to that standard (the
  checks in REQ-UX-118 pass over them).
- **release_gating**: true
- **references**: REQ-PROD-036

#### REQ-UX-101 — Every action is operable by keyboard alone
- **statement**: Every action available with a pointer is reachable and operable with the keyboard alone, on
  every screen archetype and both navigation shells; no feature is pointer-only.
- **acceptance_criteria**: With the pointer unused, sign in, read the timeline, open and operate a
  **ChirpCard**'s reply/like/more controls, compose and post a chirp, follow an account, open a profile, and
  operate a settings sub-section — each action completes using only the keyboard.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-001, REQ-PROD-002

#### REQ-UX-102 — Focus order is logical and focus is always visible
- **statement**: Keyboard focus moves in an order that matches each screen's reading order, the focused
  element always shows the visible focus indicator (REQ-UX-025), and when a view changes (a dialog opens, a
  route changes, new content loads) focus is moved deliberately to a sensible target rather than lost.
- **acceptance_criteria**: Tab through the timeline, a form, and a settings screen; focus moves in a sensible
  order and the focused control is always visibly indicated. Open a dialog — focus moves into it; close it —
  focus returns to the control that opened it. Change route — focus lands on the new screen, not on a
  vanished control.
- **release_gating**: true
- **references**: REQ-PROD-036

#### REQ-UX-103 — No keyboard trap; modal focus is held but escapable
- **statement**: A keyboard user can move into and out of every component; only a modal **Dialog**
  deliberately holds focus while open, and it is always escapable (Esc, a close control, and Cancel in the
  cycle) and returns focus on close.
- **acceptance_criteria**: Tab through each screen; focus never becomes stuck with no way out. Open the
  compose dialog and a confirmation dialog; Tab cycles within the open dialog, Esc closes it, and focus
  returns to the opener.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-022

#### REQ-UX-104 — A way to bypass the navigation shell to the content
- **statement**: A keyboard or screen-reader user is given a way to skip the repeated **NavShell** and reach
  a screen's main content directly, via a visible-on-focus skip control at the top of the tab order and the
  landmark/heading structure.
- **acceptance_criteria**: On a signed-in screen, Tab once from the top; a "Skip to content" control appears
  and, activated, moves focus past the nav to the main content. A screen reader can also jump to the `main`
  region directly.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-002

#### REQ-UX-105 — Controls meet a minimum target size
- **statement**: Pointer and touch targets for the product's controls are at least 24×24 CSS pixels, and the
  primary phone touch targets (nav destinations, the compose affordance, a chirp's action row) meet the
  comfortable minimum the responsive design sets.
- **acceptance_criteria**: On a phone viewport, measure the nav destinations, the compose affordance, and a
  chirp card's like/reply controls; each meets at least the 24×24 CSS-pixel minimum and the primary targets
  meet the responsive design's larger touch minimum.
- **release_gating**: false — target size is a WCAG 2.2 criterion (2.5.8) adopted ahead of a full move to
  2.2 and beyond the committed 2.1 AA floor; it is an expected mobile-ergonomics improvement a first release
  can stage.
- **references**: REQ-PROD-035, REQ-PROD-036

#### REQ-UX-106 — Every control exposes a name, a role, and its state
- **statement**: Every interactive component in the library exposes an accessible name, a correct role, and
  its current state to assistive technology, per the component-semantics mapping in this section.
- **acceptance_criteria**: With a screen reader, move through a chirp card, the compose box, a text field, a
  toggle, a button, an icon button, and a dialog; each is announced with a sensible name, the right role
  (button, switch, text box, dialog, …), and its state (a like as pressed/not, a toggle as on/off, a busy or
  disabled button as such).
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-001

#### REQ-UX-107 — Each screen exposes landmark regions
- **statement**: Every screen exposes landmark regions — a banner and the primary navigation for the nav
  shell, a single `main` for the content, and a footer region where the signed-out shell carries one — so an
  assistive-technology user can move between the parts of the page.
- **acceptance_criteria**: With a screen reader, list the landmarks on the landing, the timeline, and a
  settings sub-section; each exposes a navigation region, exactly one main region, and (on the signed-out
  shell) a footer, and the user can jump between them.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-030

#### REQ-UX-108 — One top-level heading per screen, in a nested order
- **statement**: Every screen has exactly one top-level heading naming it (matching the document title from
  the wayfinding model), with sub-headings nested in order and no skipped levels.
- **acceptance_criteria**: With a screen reader, bring up the heading list for the timeline, a profile, and a
  settings sub-section; each has a single top-level heading that names the screen and matches the browser tab
  title, and the sub-headings descend in order.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-002

#### REQ-UX-109 — Lists and feeds are exposed as navigable lists
- **statement**: The feed/list archetype (timeline, conversation, notifications, search results,
  followers/following) exposes its item structure, so a screen-reader user can move item by item and tell
  where they are in the set; the pagination and catch-up affordances are named controls.
- **acceptance_criteria**: With a screen reader on the timeline, navigate by item; each chirp is a
  distinguishable list item and the reader can tell one from the next, and the "load older" and "N new
  chirps" controls are reported as named buttons.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-002

#### REQ-UX-110 — Icon-only controls expose text labels and their active state
- **statement**: Every icon-only control exposes a text label to assistive technology, and an active or
  selected state (current nav destination, liked chirp) is exposed as a programmatic state, not inferred from
  colour or fill — composing with REQ-UX-028.
- **acceptance_criteria**: With a screen reader, focus the compose affordance, a like control, and the
  current nav destination; each reports a text name, the like reports pressed/not-pressed, and the current
  nav destination reports its selected state.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-005

#### REQ-UX-111 — Contrast meets WCAG 2.1 AA in every shipped theme
- **statement**: Text meets WCAG 1.4.3 (≥ 4.5:1, or ≥ 3:1 for large text) and meaningful control and icon
  boundaries meet WCAG 1.4.11 (≥ 3:1), in each theme the product ships — the token-level contrast fixed and
  verified by REQ-UX-022, carried here as a condition of the committed standard.
- **acceptance_criteria**: On the live product, sample body text, secondary text, link text, primary-button
  text, and a field border with a contrast tool in each shipped theme; normal text reaches ≥ 4.5:1, large
  text ≥ 3:1, and control/icon boundaries ≥ 3:1 (as REQ-UX-022 requires), confirming the AA contrast
  criteria.
- **release_gating**: true
- **references**: REQ-PROD-036

#### REQ-UX-112 — Text resizes and the page reflows without loss
- **statement**: Text can be enlarged to 200% without clipped content or unreachable controls (WCAG 1.4.4),
  the product reflows to a 320-CSS-pixel viewport without a second scroll direction or loss of content/function
  (WCAG 1.4.10), and overridden text spacing does not clip or overlap content (WCAG 1.4.12).
- **acceptance_criteria**: Zoom the browser to 200% and read the timeline and a form — no content is cut off
  and every control is still reachable. Narrow the viewport to 320 CSS pixels — content reflows into one
  column with no horizontal scrolling of the reading content. Apply a text-spacing override — nothing
  overlaps or is clipped.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-035

#### REQ-UX-113 — No fact is carried by colour alone, and no content flashes
- **statement**: Every state that uses a semantic colour also carries text, an icon, or a label so the fact
  survives without colour perception (WCAG 1.4.1, composing with REQ-UX-022), and no content flashes more
  than three times in any one second (WCAG 2.3.1).
- **acceptance_criteria**: View the core loop in greyscale or a colour-blindness simulation; a field error,
  an active like, and the current nav destination are each still identifiable without their colour. Observe
  the product through normal use; nothing flashes more than three times per second.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-033

#### REQ-UX-114 — Reduced motion is honoured with no loss of information
- **statement**: When a reader has asked their system to reduce motion, the product honours it through the
  `motion.reduced` contract (REQ-UX-029) — transitions become instant or a short fade, counts do not animate,
  and no required information is conveyed only by movement; the bounded loading indicator has an announced,
  static equivalent.
- **acceptance_criteria**: With the system reduce-motion setting on, open and close a menu and a dialog,
  trigger a toast, and load a list; motion is removed or reduced to a short fade, nothing animates
  continuously except a loading indicator that is also announced, and no information is lost.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-033

#### REQ-UX-115 — Status changes are announced without stealing focus
- **statement**: A change not caused by a direct keystroke — a chirp posted, a follow or setting saved, a
  report received, new chirps arriving behind the catch-up control — is announced through a polite live
  region, so a screen-reader user is told without being moved off what they are doing; this is how **Toast**
  and **InlineFeedback** reach assistive technology (WCAG 4.1.3).
- **acceptance_criteria**: With a screen reader, post a chirp, follow an account, and save a setting; each
  result is spoken as a status message and focus is not moved away from the person's current control. Leave
  the timeline open while new chirps arrive; the catch-up availability is announced politely.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-001, REQ-PROD-033

#### REQ-UX-116 — Errors are announced and tied to their field
- **statement**: A failed action is announced; a field-level error is associated with its field (so focusing
  the field re-reads the problem) and marks the field invalid, and the message says what happened and what to
  do with no system or error code (WCAG 3.3.1, 3.3.2, 3.3.3; composing with REQ-UX-032's voice rules).
- **acceptance_criteria**: With a screen reader on sign-up, submit a taken handle; the error is announced, is
  read when the handle field is focused, the field is reported invalid, and the message names the problem and
  a fix in plain words with no error code. Force a submit failure; the failure is announced, not silent.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-034

#### REQ-UX-117 — Empty, loading, and expired-session states reach assistive technology
- **statement**: A list's loading state announces that content is loading while its decorative skeletons are
  hidden from the screen reader and resolves to content or an announced error with a reachable retry; an
  **EmptyState** is a heading and action a screen-reader user lands on, with a failed load announced as an
  alert distinct from a genuinely empty surface; and an expired session mid-action is announced with its
  reason and moves focus to sign-in (REQ-UX-008).
- **acceptance_criteria**: With a screen reader, open a list while it loads — "loading" is announced and the
  skeletons are not read out; force a load failure — an error with a retry is announced. Reach a brand-new
  empty timeline — a heading and a next-step action are presented, not silence. Act with an expired session —
  the reason is announced and focus moves to the sign-in screen.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-033, REQ-PROD-034

#### REQ-UX-118 — Conformance is verified three ways over the gated set
- **statement**: Before a release, the gated conformance set (the core loop and the get-in screens with their
  empty/loading/error states) is verified by an automated check in each shipped theme, a keyboard-only pass,
  and a screen-reader pass of the core loop, against a stated support matrix of at least one screen reader per
  major platform with its common browser.
- **acceptance_criteria**: For a release, find the three recorded checks over the gated set — an automated
  scan per theme, a keyboard-only walk, and a screen-reader walk — and the support matrix they were run on;
  each gated screen appears in each check.
- **release_gating**: true
- **references**: REQ-PROD-036

#### REQ-UX-119 — Accessibility gates the release, and failures are fixes not waivers
- **statement**: A release is blocked until the gated conformance set passes the three checks (REQ-UX-118)
  with no outstanding Level A or AA failure; an accessibility failure is remedied, not waived, and a failure
  on a non-gating surface is tracked against that surface and ships with it.
- **acceptance_criteria**: Confirm that for a release the gated set has no open Level A or AA accessibility
  failure, and that any issue recorded against a non-gating surface (notifications, Explore) is tracked with
  that surface rather than blocking unrelated release work.
- **release_gating**: true
- **references**: REQ-PROD-036
