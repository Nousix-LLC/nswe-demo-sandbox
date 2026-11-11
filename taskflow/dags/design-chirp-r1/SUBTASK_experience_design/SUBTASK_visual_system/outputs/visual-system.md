## Visual language and design system

chirp is a place where strangers read each other in a running feed. People decide in the first
minute whether it looks like a product they can trust with an account, and they then live in it
for minutes at a time, every day, scanning text. So the visual language has two jobs: look
settled and credible on first sight, and stay calm and legible enough to read for a long time
without fatigue. Everything below serves those two jobs.

Today the product is three screens in the browser's default styling — a system font, a single
column, one underlined blue for links. The release design keeps that restraint and gives it a
system: a type scale, a colour language with a light and a dark theme, a spacing grid, a small
set of radii and elevations, consistent icons, a considered way to show people (avatars), motion
that only ever has a reason, and a voice for the words on screen. The system is expressed as a
named **token set** (further below) so that every screen draws from the same small palette of
decisions, and a stranger moving from the timeline to a profile to settings feels one product
rather than three.

Three principles run through all of it:

- **Text first, chrome last.** The content is the chirps. Colour, borders, and shadow stay quiet
  so the writing carries. Accent colour is spent only where it does work — an action, a link, the
  current place in the nav.
- **One decision, applied everywhere.** There is one type scale, one spacing step, one way to
  show a destructive action. A screen does not invent its own sizes or colours; it references the
  tokens. That is what makes the many screens read as one product.
- **Legible for everyone, in any light.** The language meets an accessibility baseline (WCAG 2.1
  AA) as a floor, not a finish: contrast, visible focus, information never carried by colour
  alone, and motion that can be turned down. This holds in both the light and the dark theme.

### Typography

One typeface family does all the work. chirp uses the platform's native UI sans — the same
`system-ui` lineage the product already loads — because it renders instantly with no web-font
fetch (so the first paint is not a flash of invisible text), it is deeply legible at small sizes,
and it looks native on every device. There is no display or brand face; the restraint is the
brand.

**Family roles**

- **`type.family.sans`** — all UI and reading text. Realised as the native UI sans stack
  (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`).
- **`type.family.mono`** — a monospaced stack, used only where characters must align or be read
  exactly (a recovery code, a session identifier in settings). Realised as the native monospace
  stack. Not used for chirp text, handles, or counts.

Numerals in counts (followers, likes, remaining characters) use tabular (fixed-width) figures so
a changing number does not shift the layout under the reader's eye.

**Type scale** — a six-step scale on a 16px base. Sizes are in px with the line-height that goes
with each step; line-height is looser for reading sizes and tighter for headings.

| Step | Size / line-height | Weight | Used for |
|---|---|---|---|
| `type.display` | 28 / 34 | 700 | The landing and onboarding headline — one per screen, rarely. |
| `type.title` | 20 / 28 | 700 | A screen's main heading; a profile's display name. |
| `type.heading` | 17 / 24 | 600 | Section headers, a card author's name, dialog titles. |
| `type.body` | 15 / 22 | 400 | Chirp text and primary reading — the default. |
| `type.meta` | 13 / 18 | 400 | Timestamps, secondary handles, labels under a count. |
| `type.caption` | 12 / 16 | 500 | Overlines, badges, the remaining-character counter. |

Body text never goes below `type.body` (15px); 15px at a 1.45 line-height is a comfortable
long-read size at a phone's viewing distance. Weights are drawn from a set of four — 400 regular,
500 medium, 600 semibold, 700 bold — and nothing else. Hierarchy is made with size and weight,
not with colour; colour is reserved for meaning.

### Colour and theming

Colour is used sparingly and by role. A screen does not ask for "blue" or "red"; it asks for
`color.primary` or `color.danger`, and the theme supplies the value. Because every colour is a
role, the whole product themes by swapping one set of values for another: there is a **light
theme** and a **dark theme**, and a screen is authored once against the roles and renders in both.

The brand colour is the chirp blue the product already uses, `#1D9BF0`. It is kept for brand
marks, selection, and the base of the focus ring, but it is deliberately *not* used as a text
colour or a button fill on a light surface, because at that lightness it does not reach the
contrast a stranger with ordinary eyesight needs. The action and link roles use a deeper blue
that does.

Every role below is given a light value, a dark value, and the contrast it must satisfy. The
contrast intents are the rule the product is built and checked against (see REQ-UX-022); the hex
values are the design intent a build realises.

**Surfaces**

| Role | Light | Dark | Intent |
|---|---|---|---|
| `color.bg.canvas` | `#FFFFFF` | `#16202A` | The app background. Dark is a soft navy, not pure black, so long reading is easier on the eye. |
| `color.bg.surface` | `#FFFFFF` | `#1C2732` | A card, menu, or dialog surface; separated from the canvas by a border and/or elevation. |
| `color.bg.subtle` | `#F2F5F7` | `#22303C` | Inset areas, hover fills, skeleton blocks, the compose draft area. |
| `color.bg.scrim` | `rgba(15,20,25,0.40)` | `rgba(0,0,0,0.60)` | The dim behind a modal/dialog, so the layer beneath recedes. |

**Text and on-surface**

| Role | Light | Dark | Intent |
|---|---|---|---|
| `color.text.primary` | `#0F1419` | `#E7E9EA` | Primary reading text; ≥ 7:1 on the canvas (comfortably past AA). |
| `color.text.secondary` | `#536471` | `#8B98A5` | Timestamps, meta, secondary handles; ≥ 4.5:1 on the canvas. |
| `color.text.disabled` | `#8899A6` | `#5B7083` | Disabled labels; not required to meet text contrast, but must read as inactive. |
| `color.text.link` | `#1472C4` | `#4DA3EB` | Links and inline actions; ≥ 4.5:1 on the canvas in its theme. |
| `color.text.on-primary` | `#FFFFFF` | `#FFFFFF` | Text/icon on a `color.primary` fill; ≥ 4.5:1 on that fill. |

**Border**

| Role | Light | Dark | Intent |
|---|---|---|---|
| `color.border.default` | `#CFD9DE` | `#38444D` | The hairline that separates chirps, cards, and inputs. |
| `color.border.strong` | `#AEB9C0` | `#536471` | A field's resting border, a divider that needs more presence. |
| `color.border.focus` | `#1472C4` | `#7CBAF0` | The focus ring; ≥ 3:1 against the adjacent surface in its theme. |

**Semantic roles** — each is a fill with a matching on-colour. Each fill is chosen so its
on-colour meets AA text contrast, and so the fill itself meets ≥ 3:1 against the canvas (so a
coloured control is perceivable as a control).

| Role | Light fill / on | Dark fill / on | Used for |
|---|---|---|---|
| `color.primary` | `#1565C0` / `#FFFFFF` | `#1A6DC2` / `#FFFFFF` | The primary action — Post, Follow, Save, Sign up. One per view where possible. |
| `color.success` | `#1A7F37` / `#FFFFFF` | `#2EA043` / `#FFFFFF` | A completed action's confirmation; a healthy state. |
| `color.warning` | `#B35C00` / `#FFFFFF` | `#E3922B` / `#15202B` | A caution that is not an error — approaching the character limit, an unverified contact. |
| `color.danger` | `#C8372D` / `#FFFFFF` | `#F4564B` / `#15202B` | Destructive actions and errors — delete, block, a failed submit, a field error. |
| `color.info` | `#1472C4` / `#FFFFFF` | `#4DA3EB` / `#15202B` | Neutral, informational banners and tips. |
| `color.like` | `#E8356D` / `#FFFFFF` | `#F91880` / `#FFFFFF` | The active "liked" state only; always paired with a filled heart and a "Liked" label, never colour alone. |
| `color.muted` | `#F2F5F7` / `#536471` | `#22303C` / `#8B98A5` | A quiet, non-primary chip or secondary button fill. |

Semantic colour never carries meaning by itself: an error is a red border *and* an inline
message; the active like is a colour *and* a filled icon *and* a label. The light and dark themes
are a parity pair — every role exists in both, and no screen is authored for only one.

### Spacing and the layout grid

Spacing is built on a **4px base unit**. Every margin, padding, and gap is a step on this scale;
there are no in-between values. Using one rhythm everywhere is most of what makes unrelated
screens feel related.

| Token | Value | Typical use |
|---|---|---|
| `space.0` | 0 | Reset. |
| `space.1` | 4px | Tight gaps inside a control (icon to label). |
| `space.2` | 8px | Gap between related lines; chip padding. |
| `space.3` | 12px | Compact padding; list-item inset. |
| `space.4` | 16px | The default: card/screen padding, the gap between chirps, mobile gutters. |
| `space.5` | 20px | Comfortable control padding. |
| `space.6` | 24px | Section spacing; gutters on wider viewports. |
| `space.8` | 32px | Separation between major blocks. |
| `space.10` | 40px | Generous vertical breaks on landing/onboarding. |
| `space.12` | 48px | Large empty-state and hero spacing. |

**Layout grid.** The reading column — the timeline, a conversation, a profile's chirps, a form —
is held to a **content measure of 600px** (`space.measure`). At the body size this keeps a line
of text near 66–75 characters, the band where lines are easiest to track. On a phone the content
fills the viewport with a `space.4` (16px) gutter on each edge; on wider viewports the content
column stays at the 600px measure, centred, with the navigation shell and any secondary rail
placed outside it. How the shell and rails reflow across viewports is the responsive area's to
decide; this language fixes the measure, the gutters, and the spacing steps they build from.

### Corner radii

A small set of radii, applied by the kind of thing being drawn, so curvature reads as a
deliberate signal and not noise.

| Token | Value | Applied to |
|---|---|---|
| `radius.none` | 0 | Full-bleed dividers, edge-to-edge media. |
| `radius.sm` | 4px | Text fields, small inputs, menu items. |
| `radius.md` | 8px | Cards, menus, dialogs, toasts. |
| `radius.lg` | 16px | Large containers and the onboarding/landing panels. |
| `radius.pill` | 9999px | Buttons and chips — chirp's buttons are fully rounded. |
| `radius.full` | 50% | Avatars — always a circle. |

### Elevation

Elevation separates layers that stack over one another. It is ordered: a thing that sits above
another has a higher elevation token, and the order is never skipped or inverted. In the light
theme, elevation is a soft shadow. In the dark theme shadows read poorly, so a raised surface is
separated mainly by a lighter surface colour and a border, with only a faint shadow — the token
name is the same, the realisation differs by theme.

| Token | Light (shadow) | Dark (treatment) | Used for |
|---|---|---|---|
| `elevation.0` | none | none | Canvas and inline cards, separated by borders only. |
| `elevation.1` | `0 1px 2px rgba(15,20,25,0.08)` | surface `#1C2732` + border | A hovered or pulled-forward card. |
| `elevation.2` | `0 4px 12px rgba(15,20,25,0.12)` | surface + border + `0 2px 6px rgba(0,0,0,0.4)` | Menus, popovers, dropdowns. |
| `elevation.3` | `0 8px 28px rgba(15,20,25,0.18)` | surface + border + `0 8px 28px rgba(0,0,0,0.5)` | Dialogs and modals (over a scrim). |
| `elevation.4` | `0 12px 32px rgba(15,20,25,0.22)` | surface + border + `0 12px 32px rgba(0,0,0,0.55)` | Toasts, which float above everything. |

### Iconography

One icon set, drawn as **outlines** on a 24px grid with a consistent ~2px stroke and rounded
joins, so the icons sit quietly beside the type. A **filled** variant of the same icon marks a
selected or active state — a filled home for the current nav destination, a filled heart for a
liked chirp. Icons take the current text colour by default (so they theme for free) and a
semantic role colour only to carry a state.

| Token | Value | Use |
|---|---|---|
| `icon.sm` | 16px | Inline with meta text. |
| `icon.md` | 20px | The default: buttons, list affordances. |
| `icon.lg` | 24px | Primary navigation, the compose affordance. |

Two rules hold everywhere: an icon-only control always has a text label available to assistive
technology and on hover; and an icon is never the only thing distinguishing a state — the active
nav item is filled *and* marked, not merely a different colour.

### Imagery and avatars

chirp is text-first and ships no media uploads in the release scope, so imagery is deliberately
limited to two things: people (avatars) and the product's own illustration on the
explanatory screens.

**Avatars** are always circular (`radius.full`), carry a 1px `color.border.default` to separate
them from the surface beneath, and come in a fixed set of sizes so a face is the same size
wherever it appears:

| Token | Value | Where |
|---|---|---|
| `avatar.sm` | 24px | Inline mentions, dense lists. |
| `avatar.md` | 40px | The feed and most cards — the default. |
| `avatar.lg` | 48px | A conversation's root author, settings. |
| `avatar.xl` | 96px | The profile header. |

When a person has no picture, the avatar shows their initials (a monogram) on a muted fill
derived deterministically from their handle — so the same person is always the same colour, and a
missing picture is never a broken-image glyph. **Illustration** appears only on the
empty/landing, onboarding, not-found, and empty-list states: a simple flat style in one or two
brand hues, calm and explanatory, never decorative inside the feed.

### Motion

Motion in chirp is functional — it orients (a menu grows from the control that opened it),
confirms (a toast slides in to mark a done action), and shows relationship (a dialog rises over a
dimming scrim). It is never decorative, never looping, and never blocks the reader. Nothing
animates indefinitely except a bounded loading indicator.

| Token | Value | Use |
|---|---|---|
| `motion.fast` | 120ms | Hover, press, toggles, small state flips. |
| `motion.base` | 200ms | Menus, toasts, and dialogs entering and leaving. |
| `motion.slow` | 320ms | Larger section or view transitions. |
| `motion.easing.standard` | `cubic-bezier(0.2, 0, 0, 1)` | The default for most moves. |
| `motion.easing.decelerate` | `cubic-bezier(0, 0, 0, 1)` | Things entering the screen. |
| `motion.easing.accelerate` | `cubic-bezier(0.3, 0, 1, 1)` | Things leaving the screen. |

`motion.reduced` is the contract for a reader who has asked their system to reduce motion: all
non-essential motion is dropped, a transition becomes either instant or a simple ≤120ms opacity
fade, counts do not animate, and nothing conveys required information through movement that has no
static equivalent. Honouring that preference is part of the accessibility baseline, not an extra.

### Tone and voice

The words on screen are part of the visual language — they are read in the same moment as the
type and colour. chirp's voice is plain, warm, and brief. It speaks to the reader as "you", in
the active voice, in **sentence case** throughout (headings, buttons, labels) because sentence
case is calmer and faster to read than Title Case. It names things consistently: a post is a
**chirp**, the actions are **post**, **reply**, **follow**/**unfollow**, and **like**.

The microcopy rules that keep the voice consistent:

- **Buttons are verbs for the action** — "Post", "Follow", "Save changes", "Delete chirp" — never
  "OK" or "Submit".
- **Errors say what happened and what to do**, in plain words, and never blame the reader or
  surface a system or error code: "That handle's already taken — try another", not "Error:
  invalid input". A failure appears where the action was taken.
- **Empty states explain and offer a next step** rather than apologising for being empty.
- **Destructive confirmations name the consequence plainly** and offer a clear way out; the
  account-deletion confirmation says what is and is not kept.
- **Timestamps are short and relative** ("2m", "4h", then an absolute date), and counts are
  spelled the same way everywhere.

### Design tokens

This is the named token set the rest of the product builds from. Each token has a name, a value
(for colour, a light-theme and a dark-theme value), and the intent a reviewer can check it
against. Every component and screen refers to these tokens **by name**; a screen that needs a
colour, a size, a space, a radius, a duration, or an elevation uses the matching token and never
an ad-hoc value. The families are `color.*`, `type.*`, `space.*`, `radius.*`, `elevation.*`, and
`motion.*`.

**`color.*`** — role, light value, dark value, contrast intent. (Values and intents are the
tables under *Colour and theming* above; collected here as the token list.)

| Token | Light | Dark | Contrast intent |
|---|---|---|---|
| `color.brand` | `#1D9BF0` | `#1D9BF0` | Brand mark, selection, focus-ring base; not a text/fill colour on light. |
| `color.bg.canvas` | `#FFFFFF` | `#16202A` | The app background. |
| `color.bg.surface` | `#FFFFFF` | `#1C2732` | Card/menu/dialog surface. |
| `color.bg.subtle` | `#F2F5F7` | `#22303C` | Insets, hovers, skeletons. |
| `color.bg.scrim` | `rgba(15,20,25,0.40)` | `rgba(0,0,0,0.60)` | Dim behind a modal. |
| `color.text.primary` | `#0F1419` | `#E7E9EA` | ≥ 7:1 on canvas. |
| `color.text.secondary` | `#536471` | `#8B98A5` | ≥ 4.5:1 on canvas. |
| `color.text.disabled` | `#8899A6` | `#5B7083` | Reads as inactive. |
| `color.text.link` | `#1472C4` | `#4DA3EB` | ≥ 4.5:1 on canvas. |
| `color.text.on-primary` | `#FFFFFF` | `#FFFFFF` | ≥ 4.5:1 on `color.primary`. |
| `color.border.default` | `#CFD9DE` | `#38444D` | Hairline separators. |
| `color.border.strong` | `#AEB9C0` | `#536471` | Field/divider border. |
| `color.border.focus` | `#1472C4` | `#7CBAF0` | ≥ 3:1 against the adjacent surface. |
| `color.primary` | `#1565C0` | `#1A6DC2` | White on-colour ≥ 4.5:1; fill ≥ 3:1 on canvas. |
| `color.success` | `#1A7F37` | `#2EA043` | On-colour meets AA; fill ≥ 3:1. |
| `color.warning` | `#B35C00` | `#E3922B` | On-colour meets AA; fill ≥ 3:1. |
| `color.danger` | `#C8372D` | `#F4564B` | On-colour meets AA; fill ≥ 3:1. |
| `color.info` | `#1472C4` | `#4DA3EB` | On-colour meets AA; fill ≥ 3:1. |
| `color.like` | `#E8356D` | `#F91880` | Active-like only; paired with icon + label. |
| `color.muted` | `#F2F5F7` | `#22303C` | Quiet chip/secondary fill; its on-colour ≥ 4.5:1. |

**`type.*`**

| Token | Value |
|---|---|
| `type.family.sans` | Native UI sans stack (`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`). |
| `type.family.mono` | Native monospace stack; codes and identifiers only. |
| `type.display` | 28px / 34px, weight 700. |
| `type.title` | 20px / 28px, weight 700. |
| `type.heading` | 17px / 24px, weight 600. |
| `type.body` | 15px / 22px, weight 400. |
| `type.meta` | 13px / 18px, weight 400. |
| `type.caption` | 12px / 16px, weight 500. |
| `type.weight.regular` / `.medium` / `.semibold` / `.bold` | 400 / 500 / 600 / 700. |
| `type.numeral.tabular` | Fixed-width figures for counts. |

**`space.*`** — base unit 4px.

| Token | Value |
|---|---|
| `space.0` … `space.6` | 0, 4, 8, 12, 16, 20, 24px. |
| `space.8` / `space.10` / `space.12` | 32 / 40 / 48px. |
| `space.measure` | 600px — the reading content column's max width. |
| `space.gutter.mobile` / `space.gutter.wide` | 16px / 24px. |

**`radius.*`**

| Token | Value |
|---|---|
| `radius.none` / `radius.sm` / `radius.md` / `radius.lg` | 0 / 4 / 8 / 16px. |
| `radius.pill` | 9999px (buttons, chips). |
| `radius.full` | 50% (avatars). |

**`elevation.*`** — see the *Elevation* table for the per-theme realisation.

| Token | Role |
|---|---|
| `elevation.0` | Flat; borders only. |
| `elevation.1` | Raised/hovered card. |
| `elevation.2` | Menu / popover. |
| `elevation.3` | Dialog / modal. |
| `elevation.4` | Toast. |

**`motion.*`**

| Token | Value |
|---|---|
| `motion.fast` / `motion.base` / `motion.slow` | 120 / 200 / 320ms. |
| `motion.easing.standard` | `cubic-bezier(0.2, 0, 0, 1)`. |
| `motion.easing.decelerate` | `cubic-bezier(0, 0, 0, 1)`. |
| `motion.easing.accelerate` | `cubic-bezier(0.3, 0, 1, 1)`. |
| `motion.reduced` | Drop non-essential motion; ≤120ms opacity fade or instant; no motion-only information. |

**Avatar and icon sizes** are part of the system too: `icon.sm/md/lg` = 16/20/24px;
`avatar.sm/md/lg/xl` = 24/40/48/96px. They are referenced by name like every other token.

### Consistency rules

These are the rules that make two chirp screens feel like one product. They govern how the tokens
above are applied; the component library and the per-screen designs are built to obey them.

1. **No ad-hoc values.** Every colour, type size, space, radius, duration, and elevation on any
   screen is a reference to a token above. A screen never introduces a raw hex, a one-off pixel
   size, or a bespoke duration.
2. **Colour is requested by role, not by hue.** A destructive action asks for `color.danger`; a
   primary action asks for `color.primary`. No screen picks "a red" or "a blue" of its own.
3. **Theming is a token swap, nothing more.** A screen is authored once against the semantic
   roles and renders correctly in both the light and the dark theme. No screen hard-codes a theme
   or a theme-specific colour.
4. **One type scale and one spacing rhythm, everywhere.** Headings, body, and meta come from the
   scale; vertical spacing comes from the `space.*` steps. The 600px reading measure is the same
   across the feed, a conversation, a profile, a form, and settings.
5. **Elevation is ordered and never inverted.** A card is at or below a menu, a menu below a
   dialog, a dialog below a toast. A modal always sits over the `color.bg.scrim`.
6. **Focus is always visible.** Every interactive element shows the `color.border.focus` ring on
   keyboard focus; the ring is never removed, only restyled within the token.
7. **Meaning is never carried by colour alone.** A state that uses a semantic colour also uses an
   icon, a label, or text — the error border has a message, the active like has a filled icon and
   a label.
8. **Motion uses the motion tokens and honours reduced-motion.** No screen defines its own timing
   or easing; every screen degrades to `motion.reduced` when the reader has asked for it.
9. **The voice rules apply to every string.** Sentence case, verbs on buttons, plain and
   actionable errors with no system codes, explanatory empty states.

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

## Requirements and acceptance criteria — REQ-UX-020..039

The complete set of visual-system requirements chirp must meet, consolidated from the two parts of
this subtree: the visual-language requirements (`REQ-UX-020..032`) and the component-library
requirements (`REQ-UX-033..039`). Each is testable by someone who never met its author, exercisable on
the live product; each carries a `release_gating` flag and references the product requirement(s) it
serves. This register is this area's contribution to the experience-design `REQ-UX` set; the other
areas (information architecture, screens & flows, responsive, accessibility) hold their own ranges.

#### REQ-UX-020 — The product reads as one product across screens
- **statement**: Every screen draws its type, colour, spacing, radii, and controls from the one
  published token set, so unrelated screens share the same visual treatment rather than each
  styling itself.
- **acceptance_criteria**: On any three screens of different archetypes (for example the home
  timeline, a profile, and a settings sub-section), body text is the same size and leading,
  the gutters and the spacing rhythm match, buttons share one shape and one primary colour, and
  no screen introduces a colour or control style absent from the others.
- **release_gating**: true
- **references**: REQ-PROD-033, REQ-PROD-030

#### REQ-UX-021 — Text is legible and hierarchy is clear
- **statement**: Reading text is set at a legible size with comfortable line length and leading,
  and a visible hierarchy distinguishes headings, body, and meta.
- **acceptance_criteria**: Chirp and reading text renders at no less than 15px with generous line
  spacing; a reading column's line length stays within a readable band rather than spanning the
  full width of a wide window; a screen's main heading is visibly larger and heavier than its body
  text, and meta text (timestamps, handles) is visibly quieter than body text.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-035

#### REQ-UX-022 — Colour contrast meets WCAG 2.1 AA
- **statement**: Text and interactive elements meet WCAG 2.1 AA contrast — at least 4.5:1 for
  normal text (3:1 for large text) and at least 3:1 for control boundaries and icons that carry
  meaning — in whichever theme(s) the product ships.
- **acceptance_criteria**: Sample body text, secondary text, link text, primary-button text, and
  a field's border on the live product and measure each with a contrast tool; normal text reaches
  ≥ 4.5:1, large text ≥ 3:1, and control/icon boundaries ≥ 3:1. The check passes in each theme the
  product offers.
- **release_gating**: true
- **references**: REQ-PROD-036

#### REQ-UX-023 — A light theme and a dark theme, at parity
- **statement**: The product offers a light theme and a dark theme; every screen renders legibly
  and completely in both, with no element left unthemed, invisible, or failing contrast in either.
- **acceptance_criteria**: Switch between the light and dark themes and walk the core loop (home,
  a profile, compose, a settings sub-section); in each theme every screen is fully styled — no
  element disappears into its background, keeps a wrong-theme colour, or drops below the contrast
  bar.
- **release_gating**: false — the gated bar is legibility and contrast (REQ-UX-021, REQ-UX-022) in
  whatever theme(s) ship; a first release may ship a single theme and add the second as a fast
  follow, provided the shipped theme meets the bar.
- **references**: REQ-PROD-036, REQ-PROD-033

#### REQ-UX-024 — The theme follows the reader's preference and persists
- **statement**: The product defaults to the reader's system light/dark preference, lets them
  override it, and remembers the choice on the next visit.
- **acceptance_criteria**: With the operating system set to dark, open chirp fresh — it opens in
  the dark theme; set a manual override to light and reload — it stays light; clear the override
  and reload — it follows the system again.
- **release_gating**: false — depends on there being more than one theme (REQ-UX-023); ships when
  the second theme ships.
- **references**: REQ-PROD-036

#### REQ-UX-025 — Every interactive element has a visible focus indicator
- **statement**: Every control reachable by keyboard shows a clearly visible focus indicator when
  focused, and the indicator is never suppressed.
- **acceptance_criteria**: Using only the keyboard, tab through a screen's controls (links,
  buttons, fields, menu items); each shows a distinct focus ring that stands out from its
  surroundings, and no focusable control receives focus without a visible indicator.
- **release_gating**: true
- **references**: REQ-PROD-036

#### REQ-UX-026 — Consistent spacing, grid, and reading measure
- **statement**: Spacing and layout follow one spacing scale and one reading-column measure across
  archetypes, so content is neither cramped nor stretched to an unreadable line length.
- **acceptance_criteria**: On a wide window, the reading column (timeline, conversation, profile
  chirps, a form) is held to a bounded measure rather than spanning the whole width; on a phone
  viewport the same content fills the width with a consistent edge gutter; the spacing between
  items is visibly uniform within and across these screens.
- **release_gating**: true
- **references**: REQ-PROD-035, REQ-PROD-033

#### REQ-UX-027 — Layers stack in a consistent, legible order
- **statement**: Overlapping surfaces follow one elevation order — content below menus, menus
  below dialogs, dialogs below toasts — and a modal dialog dims the content behind it.
- **acceptance_criteria**: Open a menu (it sits above the content), then a dialog (it sits above
  the content on a dimmed scrim, and the menu does not show through), then trigger a toast (it
  appears above the dialog); at no point does a lower layer render on top of a higher one.
- **release_gating**: true
- **references**: REQ-PROD-033, REQ-PROD-022

#### REQ-UX-028 — Icons are consistent and never the sole carrier of meaning
- **statement**: Icons come from one consistent set, an active/selected state is shown by more
  than colour, and every icon-only control exposes a text label.
- **acceptance_criteria**: The current primary-nav destination is shown filled and marked, not by
  colour alone (confirm by viewing in greyscale or with a colour-blind simulation — the active
  item is still identifiable); every icon-only control (compose, like, menu) exposes an accessible
  name to a screen reader and a label on hover.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-002

#### REQ-UX-029 — Motion is purposeful, bounded, and respects reduced-motion
- **statement**: Motion is used only to orient, confirm, or show relationship; nothing animates
  indefinitely except a bounded loading indicator; and the product honours a reader's
  reduced-motion preference.
- **acceptance_criteria**: Open and close a menu and a dialog and trigger a toast — each
  transition is brief (well under half a second) and settles; no element animates or blinks
  continuously apart from a loading indicator. With the system's reduce-motion setting on, repeat
  the actions — animation is removed or reduced to a short fade, and no information is lost.
- **release_gating**: true
- **references**: REQ-PROD-036, REQ-PROD-033

#### REQ-UX-030 — People are shown consistently, and a missing picture is never broken
- **statement**: Avatars are rendered consistently (circular, from a fixed set of sizes), and a
  person with no picture is shown a readable initials placeholder rather than a broken-image glyph.
- **acceptance_criteria**: Across the feed, a profile header, and the navigation, the same
  person's avatar is circular and uses the size for that context; open a profile for an account
  with no picture — it shows that account's initials on a coloured fill, never a broken-image icon
  or an empty box.
- **release_gating**: false — the designed avatar system (fixed sizes, deterministic placeholder)
  is polish; the hard minimum, that no state renders a broken image, is carried as part of the
  considered-states requirement (REQ-UX-031 / REQ-PROD-033).
- **references**: REQ-PROD-033, REQ-PROD-007

#### REQ-UX-031 — Empty, loading, and error states have a designed visual treatment
- **statement**: Empty lists, loading content, and failed actions each have a defined visual
  treatment drawn from the system — an explanatory empty block, a loading skeleton, and an inline
  error in the danger role — rather than a blank area, a frozen screen, or a raw failure.
- **acceptance_criteria**: Reach an empty list (for example a brand-new account's timeline), a
  list while it is loading, and a failed action (for example submit a form with a server error);
  the empty list shows an explanatory block with a next step, the loading list shows a skeleton
  placeholder rather than a blank or a spinner-on-blank, and the failure shows an inline message in
  the product's error styling at the point of action — none of the three is a blank area or an
  unstyled error.
- **release_gating**: true
- **references**: REQ-PROD-033, REQ-PROD-032

#### REQ-UX-032 — A consistent voice, with plain and actionable errors
- **statement**: UI copy follows one voice — sentence case, verbs on action buttons, consistent
  product terms — and error messages are in plain language that says what happened and what to do,
  never exposing a system or error code.
- **acceptance_criteria**: Inspect the buttons on several screens — action buttons read as verbs
  ("Post", "Follow", "Save changes") in sentence case, not "OK"/"Submit" or Title Case. Force an
  error (an invalid form entry, then a failed submit); the message is in plain language with a way
  forward, and no raw error code, stack text, or internal identifier is shown to the reader.
- **release_gating**: true
- **references**: REQ-PROD-034, REQ-PROD-030, REQ-PROD-033

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
