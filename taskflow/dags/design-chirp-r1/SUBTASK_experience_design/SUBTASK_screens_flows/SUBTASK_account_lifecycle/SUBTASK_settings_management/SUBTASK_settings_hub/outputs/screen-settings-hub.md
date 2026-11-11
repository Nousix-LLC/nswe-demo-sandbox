### Settings hub — `/settings`

The Settings hub is where a signed-in person goes to manage their account. It realises the **Settings**
screen in the screen inventory (`/settings`, **settings** archetype, signed-in) and is the home for the
account-level choices the recovery-contact, sign-out, and notification requirements imply. It is a
navigation surface: it lists every settings sub-section and leads into each, but designs none of their
contents. It serves journey **J6 — Managing the account** and traces to **REQ-PROD-017** (an account
settings surface).

The hub is the small secondary navigation the IA describes (REQ-UX-017): each sub-section it lists is a
screen a person can open directly by its own URL and return from to the hub.

#### Layout

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

#### Content — the sub-sections the hub lists

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

#### Primary action

The hub's primary action is **opening a settings sub-section** — the drill-in on a **SettingRow**, which
is the repeated, equally-weighted affordance the whole screen is built around. The Account group sits
first because editing the profile and managing the contact are the most common reasons a person opens
settings.

There is deliberately **no single PrimaryButton** on this screen. The settings archetype is a list of
peer destinations, not a form with one submit, so a lone call-to-action would misrepresent what the screen
is for. Sign out is not placed here either: it is reached from the account menu in the **NavShell** and is
designed into the Sessions & devices sub-section, so the hub lists the way to it rather than owning the
action.

#### States

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

#### Composition notes

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

#### Requirement

##### REQ-UX-069 — The settings hub lists every account sub-section, each addressable and returning to the hub

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
