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

## Requirements and acceptance criteria — REQ-UX-020..032

The visual-language requirements chirp must meet. Each is testable by someone who never met the
author, against the live product; each carries a `release_gating` flag and references the product
requirement(s) it serves. These are this area's entries in the consolidated `REQ-UX` register;
the component-library entries (`REQ-UX-033..039`) and the assembled register are consolidated by
the visual-system synthesis.

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

---

*Design-methodology note: this visual language was designed to the Experience Design bundle's
intent (visual design and design systems) and general product-design practice. Where it fixes an
accessibility standard it names WCAG 2.1 AA explicitly so the bar is checkable.*
